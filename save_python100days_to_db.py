# Python-100-Days 数据保存脚本
# 将学习成果保存到GVEDC统一数据库

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_memory_system import UnifiedMemorySystem

# 项目路径
PROJECT_PATH = r"C:\Users\Administrator\Desktop\jackfrued-Python-100-Days-master"

def save_to_database():
    """保存Python-100-Days学习成果到数据库"""
    print("=" * 60)
    print("Saving Python-100-Days Learning to GVEDC Database")
    print("=" * 60)

    # 初始化统一记忆系统
    memory = UnifiedMemorySystem()

    # 生成项目ID
    project_id = memory.generate_id("python100days")

    # 保存项目信息
    memory.save_paper(
        paper_id=project_id,
        paper_number=0,
        title="Python-100-Days",
        file_path=PROJECT_PATH,
        status="completed",
        wing_id="python100days",
        room_id="main"
    )

    print(f"\n[OK] 项目信息已保存: {project_id}")

    # 核心概念分类
    concepts = {
        "基础语法": ["变量", "数据类型", "运算符", "控制流程", "函数", "模块"],
        "数据结构": ["列表", "元组", "字典", "集合", "字符串"],
        "面向对象": ["类", "对象", "继承", "多态", "封装", "设计模式"],
        "高级特性": ["生成器", "迭代器", "装饰器", "上下文管理器", "元类"],
        "并发编程": ["多线程", "多进程", "异步编程", "协程", "asyncio"],
        "网络编程": ["Socket", "HTTP", "TCP/UDP", "Web服务器", "requests"],
        "数据库": ["MySQL", "Redis", "MongoDB", "ORM", "SQL"],
        "Web开发": ["Django", "Flask", "REST API", "Vue.js", "HTML/CSS"],
        "数据科学": ["NumPy", "Pandas", "Matplotlib", "scikit-learn", "TensorFlow"],
        "工具": ["Git", "Docker", "Linux", "正则表达式", "pytest"]
    }

    # 保存所有概念
    print(f"\n[BOOKS] 保存核心概念...")
    concept_ids = []
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
            concept_ids.append(concept_id)

    print(f"   已保存 {len(concept_ids)} 个核心概念")

    # 保存研究分析
    print(f"\n[SEARCH] 保存研究分析...")
    analysis_id = memory.generate_id("analysis")
    memory.save_research_analysis(
        analysis_id=analysis_id,
        paper_id=project_id,
        core_concepts=[f"{k}: {', '.join(v)}" for k, v in concepts.items()],
        technical_points=[
            "100天完整学习路径",
            "涵盖Python基础到高级应用",
            "包含大量实践代码和项目",
            "配套Markdown文档和练习题",
            "中文友好，易于学习"
        ],
        implementation_details={
            "days_count": 100,
            "language": "Python",
            "format": "Day-based learning",
            "topics": list(concepts.keys()),
            "difficulty": "入门到精通"
        },
        summary="Python-100-Days是jackfrued创建的完整Python学习项目，通过100天的系统学习，帮助学习者从入门走向精通。涵盖Python基础、Web开发、数据科学、运维部署等各个方面。"
    )
    print(f"   已保存研究分析: {analysis_id}")

    # 保存学习路径
    print(f"\n[CALENDAR] 保存学习路径...")
    learning_groups = [
        ("Python基础", "Day01-15", 15, ["基础语法", "数据结构", "面向对象"]),
        ("Python进阶", "Day16-20", 5, ["高级特性", "算法"]),
        ("Web基础", "Day21-30", 10, ["Web开发", "前端基础"]),
        ("Python高级", "Day31-50", 20, ["数据库", "网络编程", "并发编程"]),
        ("框架开发", "Day51-70", 20, ["Django", "Flask", "REST API"]),
        ("项目实战", "Day71-100", 30, ["系统设计", "项目架构", "团队协作"])
    ]

    for group_name, day_range, days_count, topics in learning_groups:
        path_id = memory.generate_id("path")
        memory.save_learning_progress(
            progress_id=path_id,
            paper_id=project_id,
            agent_type="coordinator",
            stage=group_name,
            status="completed",
            result=json.dumps({
                "group": group_name,
                "day_range": day_range,
                "days_count": days_count,
                "topics": topics
            }, ensure_ascii=False)
        )
        print(f"   已保存学习路径: {group_name}")

    # 保存文档引用
    print(f"\n[DOC] 保存文档引用...")
    docs = [
        ("python-100-days研究报告.md", "研究报告", "深度学习报告"),
        ("python-100-days百科.md", "百科", "项目百科")
    ]

    for doc_name, doc_type, description in docs:
        doc_id = memory.generate_id("doc")
        memory.save_task_record(
            task_id=doc_id,
            paper_id=project_id,
            agent_type="documenter",
            task_type="documentation",
            content=f"生成{doc_type}: {doc_name}",
            result=json.dumps({
                "doc_name": doc_name,
                "doc_type": doc_type,
                "description": description,
                "path": f"agent_group/{doc_name}"
            }, ensure_ascii=False),
            status="completed"
        )

    # 保存上下文
    memory.save_context(
        session_id="python100days_learning",
        context_type="learning_complete",
        content="完成Python-100-Days项目深度学习",
        metadata={
            "project_id": project_id,
            "concepts_count": len(concept_ids),
            "learning_groups": [g[0] for g in learning_groups],
            "completion_time": "2026-04-18"
        }
    )

    # 保存任务记录
    task_id = memory.generate_id("task")
    memory.save_task_record(
        task_id=task_id,
        paper_id=project_id,
        agent_type="coordinator",
        task_type="full_learning",
        content="完成Python-100-Days项目完整学习",
        result=json.dumps({
            "project_id": project_id,
            "concepts_saved": len(concept_ids),
            "learning_groups": len(learning_groups),
            "status": "completed"
        }, ensure_ascii=False),
        status="completed"
    )

    print(f"\n[OK] 所有数据已保存到GVEDC数据库!")
    print(f"\n[STATS] 数据库统计:")
    print(f"   - 项目ID: {project_id}")
    print(f"   - 核心概念: {len(concept_ids)} 个")
    print(f"   - 学习路径: {len(learning_groups)} 组")
    print(f"   - 文档: {len(docs)} 个")

    memory.close()

    return project_id

if __name__ == "__main__":
    save_to_database()