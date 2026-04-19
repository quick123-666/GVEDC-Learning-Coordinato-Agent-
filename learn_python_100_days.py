# Python-100-Days项目学习脚本
# 使用学习Agent组深度学习jackfrued-Python-100-Days项目

import os
import sys
import json
import glob
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from learning_coordinator import LearningCoordinator
from unified_memory_system import UnifiedMemorySystem

# 项目路径
PROJECT_PATH = r"C:\Users\Administrator\Desktop\jackfrued-Python-100-Days-master"

def analyze_project_structure():
    """分析项目结构"""
    print("=" * 60)
    print("Analyzing Python-100-Days Project Structure")
    print("=" * 60)

    # 查找所有目录
    days = []
    for i in range(1, 101):
        day_pattern = f"Day{i:02d}-*"
        matches = glob.glob(os.path.join(PROJECT_PATH, day_pattern))
        if matches:
            days.append({
                'day': i,
                'path': matches[0],
                'name': os.path.basename(matches[0])
            })
        else:
            # 尝试单个Day目录
            day_dir = os.path.join(PROJECT_PATH, f"Day{i:02d}-15")
            if os.path.exists(day_dir):
                days.append({
                    'day': i,
                    'path': day_dir,
                    'name': os.path.basename(day_dir)
                })

    print(f"\nFound {len(days)} learning modules")
    return days

def extract_core_concepts():
    """提取核心概念"""
    concepts = {
        "基础语法": ["变量", "数据类型", "运算符", "控制流程", "函数", "模块"],
        "数据结构": ["列表", "元组", "字典", "集合", "字符串"],
        "面向对象": ["类", "对象", "继承", "多态", "封装", "设计模式"],
        "高级特性": ["生成器", "迭代器", "装饰器", "上下文管理器", "元类"],
        "并发编程": ["多线程", "多进程", "异步编程", "协程", "并发队列"],
        "网络编程": ["Socket", "HTTP", "FTP", "TCP/UDP", "Web服务器"],
        "数据库": ["SQL", "MySQL", "MongoDB", "Redis", "ORM"],
        "Web开发": ["Django", "Flask", "REST API", "前端基础", "Vue.js"],
        "数据科学": ["NumPy", "Pandas", "Matplotlib", "机器学习", "深度学习"],
        "工具": ["Git", "Docker", "Linux", "正则表达式", "测试"]
    }
    return concepts

def learn_python_100_days():
    """学习Python-100-Days项目"""
    print("\n" + "=" * 60)
    print("Starting Python-100-Days Learning Session")
    print("=" * 60)

    # 初始化统一记忆系统
    memory = UnifiedMemorySystem()

    # 项目ID
    project_id = memory.generate_id("python100days")

    # 保存项目信息
    memory.save_paper(
        paper_id=project_id,
        paper_number=0,
        title="Python-100-Days",
        file_path=PROJECT_PATH,
        status="in_progress",
        wing_id="python100days",
        room_id="main"
    )

    # 分析项目结构
    days = analyze_project_structure()

    # 提取核心概念
    concepts = extract_core_concepts()

    # 保存核心概念
    for category, items in concepts.items():
        for item in items:
            concept_id = memory.generate_id("concept")
            memory.save_concept(
                concept_name=item,
                description=f"{category}: {item}",
                related_papers=[project_id],
                wing_id="python100days",
                room_id=category
            )

    # 保存研究分析
    analysis_id = memory.generate_id("analysis")
    memory.save_research_analysis(
        analysis_id=analysis_id,
        paper_id=project_id,
        core_concepts=[f"{k}: {', '.join(v)}" for k, v in concepts.items()],
        technical_points=[
            f"共{len(days)}个学习模块",
            "涵盖Python基础到高级应用",
            "包含大量实践代码",
            "配套Markdown文档"
        ],
        implementation_details={
            "days_count": len(days),
            "language": "Python",
            "format": "Day-based learning",
            "topics": list(concepts.keys())
        },
        summary=f"Python-100-Days是一个完整的Python学习项目，包含{len(days)}个学习模块，涵盖{len(concepts)}个核心主题"
    )

    # 分类学习（按主题分组）
    topic_groups = {
        "Python基础 (Day01-15)": {
            "days": list(range(1, 16)),
            "concepts": ["基础语法", "数据结构", "面向对象"],
            "description": "Python编程基础"
        },
        "Python进阶 (Day16-20)": {
            "days": list(range(16, 21)),
            "concepts": ["高级特性", "算法"],
            "description": "Python语言进阶"
        },
        "Web基础 (Day21-30)": {
            "days": list(range(21, 31)),
            "concepts": ["Web开发", "前端基础"],
            "description": "Web前端开发"
        },
        "Python高级 (Day31-50)": {
            "days": list(range(31, 51)),
            "concepts": ["数据库", "网络编程", "并发编程"],
            "description": "Python高级应用"
        },
        "框架开发 (Day51-70)": {
            "days": list(range(51, 71)),
            "concepts": ["Django", "Flask", "REST API"],
            "description": "Web框架开发"
        },
        "项目实战 (Day71-100)": {
            "days": list(range(71, 101)),
            "concepts": ["项目架构", "团队协作", "部署运维"],
            "description": "项目实战"
        }
    }

    # 为每个主题组生成学习路径
    for group_name, group_info in topic_groups.items():
        steps = []
        for day in group_info["days"]:
            steps.append({
                "step": day,
                "title": f"Day{day:02d}",
                "description": f"学习第{day}天的内容",
                "concepts": group_info["concepts"]
            })

        path_id = memory.generate_id("learning_path")
        memory.save_learning_path(
            progress_id=path_id,
            paper_id=project_id,
            agent_type="coordinator",
            stage=group_name,
            status="pending",
            result=json.dumps({
                "group": group_name,
                "days_count": len(group_info["days"]),
                "description": group_info["description"]
            }, ensure_ascii=False)
        )

    # 保存上下文
    memory.save_context(
        session_id="python100days_learning",
        context_type="learning_session",
        content=f"开始学习Python-100-Days项目，共{len(days)}个模块，{len(concepts)}个核心主题",
        metadata={
            "days_count": len(days),
            "topics_count": len(concepts),
            "start_time": datetime.now().isoformat()
        }
    )

    # 保存任务记录
    task_id = memory.generate_id("task")
    memory.save_task_record(
        task_id=task_id,
        paper_id=project_id,
        agent_type="coordinator",
        task_type="project_analysis",
        content="分析Python-100-Days项目结构和核心概念",
        result=json.dumps({
            "days_found": len(days),
            "concepts_found": len(concepts),
            "topics": list(concepts.keys())
        }, ensure_ascii=False),
        status="completed"
    )

    # 保存学习进度
    progress_id = memory.generate_id("progress")
    memory.save_learning_progress(
        progress_id=progress_id,
        paper_id=project_id,
        agent_type="coordinator",
        stage="project_analysis",
        status="completed",
        result=json.dumps({
            "analysis_completed": True,
            "project_id": project_id
        }, ensure_ascii=False)
    )

    print(f"\n✅ 项目信息已保存到数据库:")
    print(f"   Project ID: {project_id}")
    print(f"   Days Found: {len(days)}")
    print(f"   Concepts: {len(concepts)} 个核心主题")

    # 打印学习摘要
    print(f"\n📚 学习内容概览:")
    for category, items in concepts.items():
        print(f"\n   {category}:")
        for item in items[:3]:
            print(f"      - {item}")
        if len(items) > 3:
            print(f"      ... 共 {len(items)} 项")

    # 打印主题分组
    print(f"\n📅 学习路径分组:")
    for group_name, group_info in topic_groups.items():
        print(f"   {group_name}: Day{group_info['days'][0]}-{group_info['days'][-1]}")

    memory.close()

    return {
        "project_id": project_id,
        "days_found": len(days),
        "concepts_found": concepts,
        "topic_groups": topic_groups
    }

def search_concepts(keyword):
    """搜索相关概念"""
    memory = UnifiedMemorySystem()

    print(f"\n🔍 搜索关键词: {keyword}")

    # SQLite搜索
    sq_results = memory.search_concepts(keyword)
    print(f"   SQLite搜索: {len(sq_results)} 条结果")

    # 向量搜索
    vector_results = memory.semantic_search(keyword, "concepts", top_k=5)
    print(f"   向量搜索: {len(vector_results)} 条结果")

    memory.close()

    return {
        "sqlite_results": sq_results,
        "vector_results": vector_results
    }

if __name__ == "__main__":
    print("\n🎯 Python-100-Days 深度学习系统")
    print("=" * 60)

    # 学习项目
    result = learn_python_100_days()

    # 测试搜索功能
    print("\n" + "=" * 60)
    print("Testing Search Functionality")
    print("=" * 60)

    search_concepts("面向对象")
    search_concepts("Django")
    search_concepts("并发")

    print("\n" + "=" * 60)
    print("Learning Session Complete!")
    print("=" * 60)