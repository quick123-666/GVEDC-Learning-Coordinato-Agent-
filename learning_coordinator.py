# 主协调Agent - 集成记忆系统
# 负责协调多个子Agent的工作，管理任务分配和执行

import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class LearningCoordinator:
    def __init__(self, project_path):
        self.project_path = project_path
        self.papers = self._load_papers()

        # 初始化记忆系统
        from memory_system import AgentMemorySystem
        self.memory = AgentMemorySystem(project_path)

        # 从记忆系统加载论文状态
        self._load_from_memory()

        self.tasks = []

    def _load_papers(self):
        papers = []
        import glob

        print(f"Searching for papers in: {self.project_path}")

        for i in range(2, 31):  # Paper 2-30
            paper_file = os.path.join(self.project_path, f"{i:02d}_*.ipynb")
            matching_files = glob.glob(paper_file)

            # 尝试查找markdown文件
            if not matching_files:
                md_file = os.path.join(self.project_path, f"{i:02d}_*.md")
                matching_files = glob.glob(md_file)

            if matching_files:
                papers.append({
                    'id': i,
                    'file': matching_files[0],
                    'status': 'pending',
                    'progress': 0
                })

        print(f"Found {len(papers)} papers")
        return papers

    def _load_from_memory(self):
        """从记忆系统加载状态"""
        for paper in self.papers:
            paper_id = f"paper-{paper['id']}"
            existing = self.memory.get_paper(paper_id)

            if existing:
                paper['status'] = existing.get('status', 'pending')
                paper['progress'] = existing.get('progress', 0)

            # 获取研究分析
            analysis = self.memory.get_research_analysis(paper_id)
            if analysis:
                paper['analysis'] = analysis

    def assign_tasks(self):
        tasks = []
        for paper in self.papers:
            if paper['status'] == 'pending':
                tasks.append({
                    'paper_id': paper['id'],
                    'paper_file': paper['file'],
                    'subtasks': [
                        {'type': 'research', 'status': 'pending'},
                        {'type': 'implementation', 'status': 'pending'},
                        {'type': 'documentation', 'status': 'pending'}
                    ]
                })
        self.tasks = tasks
        return tasks

    def execute_tasks(self):
        results = []

        # 记录开始状态到记忆系统
        self.memory.save_context(
            session_id="learning_session",
            context_type="task_start",
            content=f"开始执行 {len(self.tasks)} 个任务",
            metadata={"task_count": len(self.tasks)}
        )

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_task = {}

            for task in self.tasks:
                # 并行执行三个子任务
                future_research = executor.submit(self._execute_subtask, 'research', task)
                future_implementation = executor.submit(self._execute_subtask, 'implementation', task)
                future_documentation = executor.submit(self._execute_subtask, 'documentation', task)

                future_to_task[future_research] = ('research', task)
                future_to_task[future_implementation] = ('implementation', task)
                future_to_task[future_documentation] = ('documentation', task)

            for future in as_completed(future_to_task):
                subtask_type, task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)

                    # 保存到记忆系统
                    task_id = self.memory.generate_id(f"task_{subtask_type}")
                    self.memory.save_task_record(
                        task_id=task_id,
                        paper_id=f"paper-{task['paper_id']}",
                        agent_type=subtask_type,
                        task_type='execute',
                        content=f"{subtask_type}任务执行",
                        result=json.dumps(result, ensure_ascii=False),
                        status='completed'
                    )

                    print(f"Completed {subtask_type} for Paper {task['paper_id']}")

                    # 更新论文进度
                    self._update_paper_progress(task['paper_id'], result)

                except Exception as e:
                    print(f"Error in {subtask_type} for Paper {task['paper_id']}: {e}")

                    # 保存错误到记忆系统
                    error_task_id = self.memory.generate_id("error_task")
                    self.memory.save_task_record(
                        task_id=error_task_id,
                        paper_id=f"paper-{task['paper_id']}",
                        agent_type=subtask_type,
                        task_type='execute',
                        content=f"{subtask_type}任务执行",
                        result=str(e),
                        status='failed'
                    )

        # 记录完成状态到记忆系统
        self.memory.save_context(
            session_id="learning_session",
            context_type="task_complete",
            content=f"完成 {len(results)} 个任务",
            metadata={"success_count": len(results)}
        )

        return results

    def _execute_subtask(self, subtask_type, task):
        paper_id = task['paper_id']
        paper_file = task['paper_file']

        if subtask_type == 'research':
            from researcher_agent import ResearcherAgent
            agent = ResearcherAgent(self.project_path, self.memory)
            return agent.analyze_paper(paper_id, paper_file)

        elif subtask_type == 'implementation':
            from implementer_agent import ImplementerAgent
            agent = ImplementerAgent(self.project_path, self.memory)
            return agent.implement_paper(paper_id, paper_file)

        elif subtask_type == 'documentation':
            from documenter_agent import DocumenterAgent
            agent = DocumenterAgent(self.project_path, self.memory)
            return agent.document_paper(paper_id, paper_file)

    def _update_paper_progress(self, paper_id, result):
        """更新论文进度"""
        paper_identifier = f"paper-{paper_id}"

        # 获取当前论文
        existing = self.memory.get_paper(paper_identifier)
        current_progress = existing.get('progress', 0) if existing else 0
        new_progress = min(current_progress + 33, 100)

        status = 'in_progress' if new_progress < 100 else 'completed'

        # 更新记忆系统
        self.memory.save_paper(
            paper_id=paper_identifier,
            paper_number=paper_id,
            title=result.get('title', f'Paper {paper_id}'),
            file_path=result.get('file', None),
            status=status
        )

        # 更新进度
        progress_id = self.memory.generate_id("progress")
        self.memory.save_learning_progress(
            progress_id=progress_id,
            paper_id=paper_identifier,
            agent_type='coordinator',
            stage='execution',
            status=status,
            result=json.dumps(result, ensure_ascii=False)
        )

    def generate_report(self):
        """生成学习报告"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'papers': [],
            'tasks': self.tasks,
            'summary': f"Processed {len(self.tasks)} papers with parallel execution"
        }

        # 从记忆系统获取所有论文状态
        all_papers = self.memory.get_all_papers()
        report['papers'] = all_papers

        # 获取所有知识点
        concepts = self.memory.get_all_concepts()
        report['concepts'] = concepts

        # 保存报告到文件
        report_path = os.path.join(self.project_path, 'agent_group', 'learning_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # 同时保存到记忆系统
        self.memory.save_context(
            session_id="learning_session",
            context_type="report_generated",
            content=json.dumps(report, ensure_ascii=False),
            metadata={"report_path": report_path}
        )

        return report

    def search_knowledge(self, keyword: str):
        """搜索知识点"""
        # 搜索概念
        concept_results = self.memory.search_concepts(keyword)

        # 搜索任务记录
        task_results = self.memory.search_by_content(keyword)

        # 搜索研究分析
        analysis_results = self.memory.search_by_content(keyword, "research_analysis")

        return {
            'concepts': concept_results,
            'tasks': task_results,
            'analysis': analysis_results
        }

    def get_learning_summary(self):
        """获取学习摘要"""
        papers = self.memory.get_all_papers()
        completed = len([p for p in papers if p.get('status') == 'completed'])
        in_progress = len([p for p in papers if p.get('status') == 'in_progress'])
        pending = len([p for p in papers if p.get('status') == 'pending'])

        concepts = self.memory.get_all_concepts()

        return {
            'total_papers': len(papers),
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'total_concepts': len(concepts)
        }


if __name__ == "__main__":
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    coordinator = LearningCoordinator(project_path)

    print("Learning Summary:")
    summary = coordinator.get_learning_summary()
    print(f"  Total Papers: {summary['total_papers']}")
    print(f"  Completed: {summary['completed']}")
    print(f"  In Progress: {summary['in_progress']}")
    print(f"  Pending: {summary['pending']}")
    print(f"  Total Concepts: {summary['total_concepts']}")

    print("\nAssigning tasks...")
    tasks = coordinator.assign_tasks()
    print(f"Assigned {len(tasks)} tasks")

    print("\nExecuting tasks in parallel...")
    results = coordinator.execute_tasks()

    print("\nGenerating report...")
    report = coordinator.generate_report()
    print("Report generated successfully!")

    # 测试搜索功能
    print("\nSearching for 'attention'...")
    search_results = coordinator.search_knowledge('attention')
    print(f"  Found {len(search_results['concepts'])} concepts")
    print(f"  Found {len(search_results['tasks'])} tasks")
    print(f"  Found {len(search_results['analysis'])} analysis results")