import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from learning_coordinator import LearningCoordinator
from researcher_agent import ResearcherAgent
from implementer_agent import ImplementerAgent
from documenter_agent import DocumenterAgent

def test_researcher():
    print("Testing ResearcherAgent...")
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    agent = ResearcherAgent(project_path)
    
    # 测试分析Paper 24
    paper_file = os.path.join(project_path, "24_machine_super_intelligence.ipynb")
    if os.path.exists(paper_file):
        result = agent.analyze_paper(24, paper_file)
        print(f"✓ ResearcherAgent test passed: {result['core_concepts'][:3]}...")
    else:
        print("⚠ Paper 24 file not found, skipping test")

def test_implementer():
    print("\nTesting ImplementerAgent...")
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    agent = ImplementerAgent(project_path)
    
    # 测试验证Paper 24
    paper_file = os.path.join(project_path, "24_machine_super_intelligence.ipynb")
    if os.path.exists(paper_file):
        result = agent.implement_paper(24, paper_file)
        print(f"✓ ImplementerAgent test passed: integrity_score={result['code_check']['integrity_score']:.1f}%")
    else:
        print("⚠ Paper 24 file not found, skipping test")

def test_documenter():
    print("\nTesting DocumenterAgent...")
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    agent = DocumenterAgent(project_path)
    
    # 测试生成文档
    paper_file = os.path.join(project_path, "24_machine_super_intelligence.ipynb")
    if os.path.exists(paper_file):
        result = agent.document_paper(24, paper_file)
        print(f"✓ DocumenterAgent test passed: generated files at {result['paper_path']}")
    else:
        print("⚠ Paper 24 file not found, skipping test")

def test_coordinator():
    print("\nTesting LearningCoordinator...")
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    coordinator = LearningCoordinator(project_path)
    
    tasks = coordinator.assign_tasks()
    print(f"✓ LearningCoordinator test passed: assigned {len(tasks)} tasks")

def main():
    print("======================================")
    print("Testing Agent Group Functionality")
    print("======================================")
    
    test_researcher()
    test_implementer()
    test_documenter()
    test_coordinator()
    
    print("\n======================================")
    print("All tests completed!")
    print("======================================")

if __name__ == "__main__":
    main()