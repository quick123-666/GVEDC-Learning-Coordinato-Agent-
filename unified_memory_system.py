# Agent团队统一记忆系统
# 整合到GVEDC数据库，支持向量检索和层级记忆

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


class UnifiedMemorySystem:
    """Agent团队统一记忆系统 - 整合GVEDC数据库"""

    def __init__(self, project_path: str = None, gvedc_path: str = None):
        # 项目路径
        if project_path is None:
            project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.project_path = project_path

        # GVEDC数据库路径
        if gvedc_path is None:
            gvedc_path = os.path.join(os.path.dirname(project_path), "Graph-Vector-Encyclopedia-Database-Context")

        self.gvedc_path = gvedc_path
        self.db_path = os.path.join(gvedc_path, "db", "gvced.db")
        self.chroma_path = os.path.join(gvedc_path, "db", "chroma")
        self.storage_path = os.path.join(gvedc_path, "gvced-storage", "drawers")

        # 确保目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.chroma_path, exist_ok=True)
        os.makedirs(self.storage_path, exist_ok=True)

        # 初始化数据库
        self._init_sqlite()
        self._init_chroma()

    def _init_sqlite(self):
        """初始化SQLite数据库"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        # 创建表
        self._create_tables()

    def _create_tables(self):
        """创建记忆数据库表"""
        # 项目/论文表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_papers (
                id TEXT PRIMARY KEY,
                paper_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                file_path TEXT,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0,
                wing_id TEXT,
                room_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 研究分析表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_research (
                id TEXT PRIMARY KEY,
                paper_id TEXT NOT NULL,
                core_concepts TEXT,
                technical_points TEXT,
                implementation_details TEXT,
                summary TEXT,
                wing_id TEXT,
                room_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES agent_papers(id)
            )
        """)

        # 任务记录表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_tasks (
                id TEXT PRIMARY KEY,
                paper_id TEXT,
                agent_type TEXT NOT NULL,
                task_type TEXT NOT NULL,
                content TEXT NOT NULL,
                result TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES agent_papers(id)
            )
        """)

        # 知识点表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_concepts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                related_papers TEXT,
                wing_id TEXT,
                room_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 学习进度表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_progress (
                id TEXT PRIMARY KEY,
                paper_id TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                stage TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES agent_papers(id)
            )
        """)

        # 上下文记忆表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_context (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                context_type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def _init_chroma(self):
        """初始化Chroma向量数据库"""
        if not CHROMADB_AVAILABLE:
            print("ChromaDB not available, vector search disabled")
            self.chroma_client = None
            self.papers_collection = None
            self.concepts_collection = None
            self.tasks_collection = None
            return

        try:
            self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)

            # 创建集合
            self.papers_collection = self.chroma_client.get_or_create_collection(
                name="agent_papers",
                metadata={"description": "Agent papers collection"}
            )
            self.concepts_collection = self.chroma_client.get_or_create_collection(
                name="agent_concepts",
                metadata={"description": "Agent concepts collection"}
            )
            self.tasks_collection = self.chroma_client.get_or_create_collection(
                name="agent_tasks",
                metadata={"description": "Agent tasks collection"}
            )
        except Exception as e:
            print(f"ChromaDB initialization error: {e}")
            self.chroma_client = None

    def save_paper(self, paper_id: str, paper_number: int, title: str,
                   file_path: str = None, status: str = "pending",
                   wing_id: str = "sutskever", room_id: str = "papers") -> bool:
        """保存论文信息"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO agent_papers
                (id, paper_number, title, file_path, status, updated_at, wing_id, room_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (paper_id, paper_number, title, file_path, status,
                  datetime.now().isoformat(), wing_id, room_id))
            self.conn.commit()

            # 保存到向量数据库
            if self.papers_collection:
                content = f"Paper {paper_number}: {title}"
                if file_path:
                    content += f" - File: {file_path}"

                self.papers_collection.add(
                    documents=[content],
                    metadatas=[{
                        "paper_id": paper_id,
                        "paper_number": paper_number,
                        "title": title,
                        "status": status
                    }],
                    ids=[paper_id]
                )

            return True
        except Exception as e:
            print(f"Error saving paper: {e}")
            return False

    def save_research_analysis(self, analysis_id: str, paper_id: str,
                               core_concepts: List, technical_points: List,
                               implementation_details: Dict, summary: str = "") -> bool:
        """保存研究分析结果"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO agent_research
                (id, paper_id, core_concepts, technical_points, implementation_details, summary)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (analysis_id, paper_id, json.dumps(core_concepts, ensure_ascii=False),
                  json.dumps(technical_points, ensure_ascii=False),
                  json.dumps(implementation_details, ensure_ascii=False), summary))
            self.conn.commit()

            # 保存核心概念到向量数据库
            if self.concepts_collection:
                for i, concept in enumerate(core_concepts):
                    concept_id = f"{analysis_id}_concept_{i}"
                    self.concepts_collection.add(
                        documents=[concept],
                        metadatas=[{
                            "analysis_id": analysis_id,
                            "paper_id": paper_id,
                            "concept": concept
                        }],
                        ids=[concept_id]
                    )

            return True
        except Exception as e:
            print(f"Error saving research analysis: {e}")
            return False

    def save_task_record(self, task_id: str, paper_id: str, agent_type: str,
                        task_type: str, content: str, result: str = None,
                        status: str = "pending") -> bool:
        """保存任务记录"""
        try:
            self.cursor.execute("""
                INSERT INTO agent_tasks
                (id, paper_id, agent_type, task_type, content, result, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task_id, paper_id, agent_type, task_type, content, result, status))
            self.conn.commit()

            # 保存到向量数据库
            if self.tasks_collection:
                full_content = f"{agent_type} - {task_type}: {content}"
                if result:
                    full_content += f" - Result: {result}"

                self.tasks_collection.add(
                    documents=[full_content],
                    metadatas=[{
                        "task_id": task_id,
                        "paper_id": paper_id,
                        "agent_type": agent_type,
                        "task_type": task_type,
                        "status": status
                    }],
                    ids=[task_id]
                )

            return True
        except Exception as e:
            print(f"Error saving task record: {e}")
            return False

    def save_concept(self, concept_name: str, description: str = "",
                    related_papers: List[str] = None,
                    wing_id: str = "sutskever", room_id: str = "concepts") -> bool:
        """保存知识点"""
        try:
            concept_id = hashlib.md5(concept_name.encode()).hexdigest()[:8]
            related = json.dumps(related_papers or [], ensure_ascii=False)

            self.cursor.execute("""
                INSERT OR REPLACE INTO agent_concepts
                (id, name, description, related_papers, wing_id, room_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (concept_id, concept_name, description, related, wing_id, room_id))
            self.conn.commit()

            # 保存到向量数据库
            if self.concepts_collection:
                full_content = f"{concept_name}: {description}"
                self.concepts_collection.add(
                    documents=[full_content],
                    metadatas=[{
                        "concept_id": concept_id,
                        "name": concept_name,
                        "related_papers": related
                    }],
                    ids=[concept_id]
                )

            return True
        except Exception as e:
            print(f"Error saving concept: {e}")
            return False

    def save_learning_progress(self, progress_id: str, paper_id: str, agent_type: str,
                               stage: str, status: str = "pending",
                               result: str = None) -> bool:
        """保存学习进度"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO agent_progress
                (id, paper_id, agent_type, stage, status, result, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (progress_id, paper_id, agent_type, stage, status, result,
                  datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving learning progress: {e}")
            return False

    def save_context(self, session_id: str, context_type: str, content: str,
                    metadata: Dict = None) -> bool:
        """保存上下文记忆"""
        try:
            context_id = hashlib.md5(f"{session_id}{content[:50]}".encode()).hexdigest()[:16]
            metadata_json = json.dumps(metadata or {}, ensure_ascii=False)

            self.cursor.execute("""
                INSERT INTO agent_context
                (id, session_id, context_type, content, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (context_id, session_id, context_type, content, metadata_json))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving context: {e}")
            return False

    def get_paper(self, paper_id: str) -> Optional[Dict]:
        """获取论文信息"""
        self.cursor.execute("SELECT * FROM agent_papers WHERE id = ?", (paper_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_all_papers(self) -> List[Dict]:
        """获取所有论文"""
        self.cursor.execute("SELECT * FROM agent_papers ORDER BY paper_number")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_research_analysis(self, paper_id: str) -> Optional[Dict]:
        """获取研究分析结果"""
        self.cursor.execute(
            "SELECT * FROM agent_research WHERE paper_id = ? ORDER BY created_at DESC LIMIT 1",
            (paper_id,))
        row = self.cursor.fetchone()
        if row:
            result = dict(row)
            result['core_concepts'] = json.loads(result['core_concepts'])
            result['technical_points'] = json.loads(result['technical_points'])
            result['implementation_details'] = json.loads(result['implementation_details'])
            return result
        return None

    def get_task_records(self, paper_id: str = None, agent_type: str = None) -> List[Dict]:
        """获取任务记录"""
        query = "SELECT * FROM agent_tasks WHERE 1=1"
        params = []

        if paper_id:
            query += " AND paper_id = ?"
            params.append(paper_id)
        if agent_type:
            query += " AND agent_type = ?"
            params.append(agent_type)

        self.cursor.execute(query + " ORDER BY created_at DESC", params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_concepts(self) -> List[Dict]:
        """获取所有知识点"""
        self.cursor.execute("SELECT * FROM agent_concepts ORDER BY name")
        results = []
        for row in self.cursor.fetchall():
            result = dict(row)
            result['related_papers'] = json.loads(result['related_papers'])
            results.append(result)
        return results

    def search_concepts(self, keyword: str) -> List[Dict]:
        """搜索知识点"""
        # SQLite搜索
        self.cursor.execute(
            "SELECT * FROM agent_concepts WHERE name LIKE ? OR description LIKE ?",
            (f"%{keyword}%", f"%{keyword}%"))
        results = []
        for row in self.cursor.fetchall():
            result = dict(row)
            result['related_papers'] = json.loads(result['related_papers'])
            results.append(result)

        # 向量搜索
        if self.concepts_collection:
            try:
                vector_results = self.concepts_collection.query(
                    query_texts=[keyword],
                    n_results=5
                )
                for i, doc in enumerate(vector_results["documents"][0]):
                    metadata = vector_results["metadatas"][0][i]
                    if metadata not in [r.get('metadata') for r in results]:
                        results.append({
                            'id': metadata.get('concept_id'),
                            'name': metadata.get('name'),
                            'description': doc,
                            'source': 'vector',
                            'score': vector_results["distances"][0][i] if "distances" in vector_results else 0
                        })
            except Exception as e:
                print(f"Vector search error: {e}")

        return results

    def get_learning_progress(self, paper_id: str = None) -> List[Dict]:
        """获取学习进度"""
        query = "SELECT * FROM agent_progress WHERE 1=1"
        params = []

        if paper_id:
            query += " AND paper_id = ?"
            params.append(paper_id)

        self.cursor.execute(query + " ORDER BY created_at DESC", params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_recent_context(self, session_id: str, limit: int = 10) -> List[Dict]:
        """获取最近的上下文"""
        self.cursor.execute("""
            SELECT * FROM agent_context
            WHERE session_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (session_id, limit))
        results = []
        for row in self.cursor.fetchall():
            result = dict(row)
            result['metadata'] = json.loads(result['metadata']) if result['metadata'] else {}
            results.append(result)
        return results

    def search_by_content(self, keyword: str, table: str = "tasks") -> List[Dict]:
        """基于内容搜索"""
        if table == "tasks":
            self.cursor.execute(
                "SELECT * FROM agent_tasks WHERE content LIKE ? OR result LIKE ?",
                (f"%{keyword}%", f"%{keyword}%"))
            return [dict(row) for row in self.cursor.fetchall()]
        elif table == "research":
            self.cursor.execute(
                """SELECT * FROM agent_research
                   WHERE core_concepts LIKE ? OR technical_points LIKE ?
                   OR implementation_details LIKE ?""",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            results = []
            for row in self.cursor.fetchall():
                result = dict(row)
                result['core_concepts'] = json.loads(result['core_concepts'])
                result['technical_points'] = json.loads(result['technical_points'])
                result['implementation_details'] = json.loads(result['implementation_details'])
                results.append(result)
            return results
        return []

    def semantic_search(self, query: str, collection: str = "concepts", top_k: int = 5) -> List[Dict]:
        """语义搜索（向量检索）"""
        if not self.chroma_client:
            return []

        collection_map = {
            "papers": self.papers_collection,
            "concepts": self.concepts_collection,
            "tasks": self.tasks_collection
        }

        target_collection = collection_map.get(collection)
        if not target_collection:
            return []

        try:
            results = target_collection.query(
                query_texts=[query],
                n_results=top_k
            )

            search_results = []
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]
                search_results.append({
                    'content': doc,
                    'metadata': metadata,
                    'score': results["distances"][0][i] if "distances" in results else 0
                })
            return search_results
        except Exception as e:
            print(f"Semantic search error: {e}")
            return []

    def dual_search(self, query: str, top_k: int = 5) -> Dict:
        """双检索：图谱 + 向量"""
        # SQLite搜索
        sq_results = self.search_concepts(query)

        # 向量搜索
        vector_results = self.semantic_search(query, "concepts", top_k)

        return {
            "sqlite_results": sq_results,
            "vector_results": vector_results,
            "total_sqlite": len(sq_results),
            "total_vector": len(vector_results)
        }

    def generate_id(self, prefix: str) -> str:
        """生成唯一ID"""
        import time
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        hash_val = hashlib.md5(f"{prefix}{timestamp}".encode()).hexdigest()[:8]
        return f"{prefix}-{timestamp}-{hash_val}"

    def get_learning_summary(self) -> Dict:
        """获取学习摘要"""
        papers = self.get_all_papers()
        completed = len([p for p in papers if p.get('status') == 'completed'])
        in_progress = len([p for p in papers if p.get('status') == 'in_progress'])
        pending = len([p for p in papers if p.get('status') == 'pending'])
        concepts = self.get_all_concepts()

        return {
            'total_papers': len(papers),
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'total_concepts': len(concepts)
        }

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


# 测试代码
if __name__ == "__main__":
    print("Testing Unified Memory System with GVEDC...")
    memory = UnifiedMemorySystem()

    print(f"Database path: {memory.db_path}")
    print(f"Chroma path: {memory.chroma_path}")

    # 测试保存论文
    paper_id = memory.generate_id("paper")
    memory.save_paper(paper_id, 1, "Test Paper", "/path/to/paper.ipynb", "completed")

    # 测试保存研究分析
    analysis_id = memory.generate_id("analysis")
    memory.save_research_analysis(
        analysis_id, paper_id,
        ["深度学习", "神经网络"],
        ["反向传播", "梯度下降"],
        {"framework": "PyTorch"},
        "测试摘要"
    )

    # 测试保存知识点
    memory.save_concept("Transformer", "注意力机制模型", [paper_id])
    memory.save_concept("LSTM", "长短期记忆网络", [paper_id])

    # 测试搜索
    print("\nTesting SQLite search:")
    results = memory.search_concepts("深度学习")
    print(f"  Found {len(results)} concepts")

    # 测试双检索
    print("\nTesting dual search:")
    results = memory.dual_search("深度学习")
    print(f"  SQLite results: {results['total_sqlite']}")
    print(f"  Vector results: {results['total_vector']}")

    # 获取摘要
    print("\nLearning summary:")
    summary = memory.get_learning_summary()
    print(f"  Total papers: {summary['total_papers']}")
    print(f"  Completed: {summary['completed']}")
    print(f"  Total concepts: {summary['total_concepts']}")

    memory.close()
    print("\nUnified Memory System test completed!")