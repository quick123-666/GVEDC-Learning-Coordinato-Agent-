# Agent团队专用记忆系统
# 基于ai-agent-learning-system的通用数据库模块，专为学习Agent团队优化

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

class AgentMemorySystem:
    """Agent团队记忆系统 - 支持向量检索和层级记忆"""

    def __init__(self, project_path: str = None):
        # 项目路径
        if project_path is None:
            project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.project_path = project_path
        self.db_path = os.path.join(project_path, "agent_group", "memory", "agent_memory.db")

        # 确保目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # 初始化数据库
        self._init_sqlite()

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
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                paper_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                file_path TEXT,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 研究分析表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_analysis (
                id TEXT PRIMARY KEY,
                paper_id TEXT NOT NULL,
                core_concepts TEXT,
                technical_points TEXT,
                implementation_details TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)

        # 对话/任务记录表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_records (
                id TEXT PRIMARY KEY,
                paper_id TEXT,
                agent_type TEXT NOT NULL,
                task_type TEXT NOT NULL,
                content TEXT NOT NULL,
                result TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)

        # 知识点表 - 用于关联不同论文间的知识点
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                related_papers TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 学习进度表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_progress (
                id TEXT PRIMARY KEY,
                paper_id TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                stage TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)

        # 上下文记忆表 - 保存最近的对话上下文
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS context_memory (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                context_type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def save_paper(self, paper_id: str, paper_number: int, title: str,
                    file_path: str = None, status: str = "pending") -> bool:
        """保存论文信息"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO papers
                (id, paper_number, title, file_path, status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (paper_id, paper_number, title, file_path, status,
                  datetime.now().isoformat()))
            self.conn.commit()
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
                INSERT OR REPLACE INTO research_analysis
                (id, paper_id, core_concepts, technical_points, implementation_details, summary)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (analysis_id, paper_id, json.dumps(core_concepts, ensure_ascii=False),
                  json.dumps(technical_points, ensure_ascii=False),
                  json.dumps(implementation_details, ensure_ascii=False), summary))
            self.conn.commit()
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
                INSERT INTO task_records
                (id, paper_id, agent_type, task_type, content, result, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task_id, paper_id, agent_type, task_type, content, result, status))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving task record: {e}")
            return False

    def save_concept(self, concept_name: str, description: str = "",
                    related_papers: List[str] = None) -> bool:
        """保存知识点"""
        try:
            concept_id = hashlib.md5(concept_name.encode()).hexdigest()[:8]
            related = json.dumps(related_papers or [], ensure_ascii=False)

            self.cursor.execute("""
                INSERT OR REPLACE INTO concepts
                (id, name, description, related_papers)
                VALUES (?, ?, ?, ?)
            """, (concept_id, concept_name, description, related))
            self.conn.commit()
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
                INSERT OR REPLACE INTO learning_progress
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
                INSERT INTO context_memory
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
        self.cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_all_papers(self) -> List[Dict]:
        """获取所有论文"""
        self.cursor.execute("SELECT * FROM papers ORDER BY paper_number")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_research_analysis(self, paper_id: str) -> Optional[Dict]:
        """获取研究分析结果"""
        self.cursor.execute(
            "SELECT * FROM research_analysis WHERE paper_id = ? ORDER BY created_at DESC LIMIT 1",
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
        query = "SELECT * FROM task_records WHERE 1=1"
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
        self.cursor.execute("SELECT * FROM concepts ORDER BY name")
        results = []
        for row in self.cursor.fetchall():
            result = dict(row)
            result['related_papers'] = json.loads(result['related_papers'])
            results.append(result)
        return results

    def search_concepts(self, keyword: str) -> List[Dict]:
        """搜索知识点"""
        self.cursor.execute(
            "SELECT * FROM concepts WHERE name LIKE ? OR description LIKE ?",
            (f"%{keyword}%", f"%{keyword}%"))
        results = []
        for row in self.cursor.fetchall():
            result = dict(row)
            result['related_papers'] = json.loads(result['related_papers'])
            results.append(result)
        return results

    def get_learning_progress(self, paper_id: str = None) -> List[Dict]:
        """获取学习进度"""
        query = "SELECT * FROM learning_progress WHERE 1=1"
        params = []

        if paper_id:
            query += " AND paper_id = ?"
            params.append(paper_id)

        self.cursor.execute(query + " ORDER BY created_at DESC", params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_recent_context(self, session_id: str, limit: int = 10) -> List[Dict]:
        """获取最近的上下文"""
        self.cursor.execute("""
            SELECT * FROM context_memory
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

    def search_by_content(self, keyword: str, table: str = "task_records") -> List[Dict]:
        """基于内容搜索"""
        if table == "task_records":
            self.cursor.execute(
                "SELECT * FROM task_records WHERE content LIKE ? OR result LIKE ?",
                (f"%{keyword}%", f"%{keyword}%"))
            return [dict(row) for row in self.cursor.fetchall()]
        elif table == "research_analysis":
            self.cursor.execute(
                """SELECT * FROM research_analysis
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

    def generate_id(self, prefix: str) -> str:
        """生成唯一ID"""
        import time
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        hash_val = hashlib.md5(f"{prefix}{timestamp}".encode()).hexdigest()[:8]
        return f"{prefix}-{timestamp}-{hash_val}"

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


# 测试代码
if __name__ == "__main__":
    memory = AgentMemorySystem()

    # 测试保存论文
    paper_id = memory.generate_id("paper")
    memory.save_paper(paper_id, 1, "Test Paper", "/path/to/paper.ipynb", "completed")

    # 测试保存研究分析
    analysis_id = memory.generate_id("analysis")
    memory.save_research_analysis(
        analysis_id, paper_id,
        ["概念1", "概念2"],
        ["技术点1", "技术点2"],
        {"架构": "测试架构"},
        "这是摘要"
    )

    # 测试保存任务记录
    task_id = memory.generate_id("task")
    memory.save_task_record(task_id, paper_id, "researcher", "analyze",
                           "分析论文内容", "分析完成", "completed")

    # 测试保存知识点
    memory.save_concept("深度学习", "机器学习的分支", [paper_id])
    memory.save_concept("Transformer", "注意力机制模型", [paper_id])

    # 测试搜索
    results = memory.search_concepts("深度学习")
    print(f"搜索'深度学习'结果: {len(results)} 条")

    results = memory.search_by_content("分析")
    print(f"搜索'分析'结果: {len(results)} 条")

    # 获取所有论文
    papers = memory.get_all_papers()
    print(f"论文数量: {len(papers)}")

    # 获取所有知识点
    concepts = memory.get_all_concepts()
    print(f"知识点数量: {len(concepts)}")

    memory.close()
    print("记忆系统测试完成！")