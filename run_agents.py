# Agent执行脚本 - 集成记忆系统
# 运行整个学习Agent团队

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from learning_coordinator import LearningCoordinator
from researcher_agent import ResearcherAgent
from implementer_agent import ImplementerAgent
from documenter_agent import DocumenterAgent
from memory_system import AgentMemorySystem

def run_learning_coordinator():
    """运行学习协调Agent"""
    print("=" * 60)
    print("Starting Learning Coordinator with Memory System")
    print("=" * 60)

    # 获取项目路径
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 初始化协调器（包含记忆系统）
    coordinator = LearningCoordinator(project_path)

    # 获取学习摘要
    print("\n📊 Learning Summary:")
    summary = coordinator.get_learning_summary()
    print(f"  Total Papers: {summary['total_papers']}")
    print(f"  Completed: {summary['completed']}")
    print(f"  In Progress: {summary['in_progress']}")
    print(f"  Pending: {summary['pending']}")
    print(f"  Total Concepts: {summary['total_concepts']}")

    # 分配任务
    print("\n📋 Assigning tasks...")
    tasks = coordinator.assign_tasks()
    print(f"  Assigned {len(tasks)} tasks")

    if not tasks:
        print("  No pending tasks. All papers have been processed!")
    else:
        # 执行任务
        print("\n🚀 Executing tasks in parallel...")
        results = coordinator.execute_tasks()
        print(f"  Completed {len(results)} subtasks")

    # 生成报告
    print("\n📝 Generating report...")
    report = coordinator.generate_report()
    print(f"  Report saved with {len(report.get('papers', []))} papers")
    print(f"  Total concepts documented: {len(report.get('concepts', []))}")

    return coordinator

def test_search_functionality():
    """测试搜索功能"""
    print("\n" + "=" * 60)
    print("Testing Search Functionality")
    print("=" * 60)

    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    coordinator = LearningCoordinator(project_path)

    # 测试搜索
    search_keywords = ['attention', 'transformer', 'neural', 'memory']

    for keyword in search_keywords:
        print(f"\n🔍 Searching for '{keyword}'...")
        results = coordinator.search_knowledge(keyword)
        print(f"  Concepts found: {len(results['concepts'])}")
        print(f"  Tasks found: {len(results['tasks'])}")
        print(f"  Analysis found: {len(results['analysis'])}")

def show_memory_stats():
    """显示记忆系统统计"""
    print("\n" + "=" * 60)
    print("Memory System Statistics")
    print("=" * 60)

    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    memory = AgentMemorySystem(project_path)

    # 统计各类数据
    papers = memory.get_all_papers()
    concepts = memory.get_all_concepts()

    print(f"\n📊 Database Statistics:")
    print(f"  Total Papers: {len(papers)}")

    # 按状态统计论文
    completed = len([p for p in papers if p.get('status') == 'completed'])
    in_progress = len([p for p in papers if p.get('status') == 'in_progress'])
    pending = len([p for p in papers if p.get('status') == 'pending'])

    print(f"  - Completed: {completed}")
    print(f"  - In Progress: {in_progress}")
    print(f"  - Pending: {pending}")
    print(f"  Total Concepts: {len(concepts)}")

    # 获取学习进度
    progress = memory.get_learning_progress()
    print(f"  Total Progress Records: {len(progress)}")

    # 获取任务记录
    tasks = memory.get_task_records()
    print(f"  Total Task Records: {len(tasks)}")

    memory.close()

def main():
    """主函数"""
    print("\n🤖 AI Agent Learning Team - Memory System Integration")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 运行学习协调器
    coordinator = run_learning_coordinator()

    # 测试搜索功能
    test_search_functionality()

    # 显示记忆系统统计
    show_memory_stats()

    print("\n" + "=" * 60)
    print("Learning Session Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()