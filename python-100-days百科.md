# Python-100-Days 百科

## 基本信息

- **项目名称**: Python-100-Days
- **作者**: jackfrued (骆昊)
- **GitHub**: https://github.com/jackfrued/Python-100-Days
- **学习周期**: 100天
- **编程语言**: Python
- **项目类型**: Python编程学习教程
- **受众**: Python初学者、有志于提升的开发者

## 核心概念

### 1. Python基础 (Day 01-15)

| 概念 | 说明 | 代码示例 |
|------|------|---------|
| 变量 | 数据存储容器 | `name = "Python"` |
| 数据类型 | 整数、浮点数、字符串、布尔 | `type(42) -> int` |
| 运算符 | 算术、比较、逻辑运算符 | `a + b`, `a > b` |
| 控制流程 | if/elif/else条件语句 | `if x > 0:` |
| 循环 | for/while循环 | `for i in range(10):` |
| 函数 | 代码复用和模块化 | `def greet(name):` |
| 列表 | 有序可变序列 | `[1, 2, 3]` |
| 元组 | 有序不可变序列 | `(1, 2, 3)` |
| 字典 | 键值对映射 | `{"name": "Tom"}` |
| 集合 | 无序不重复元素 | `{1, 2, 3}` |
| 类和对象 | 面向对象基础 | `class Dog:` |
| 继承 | 类复用和扩展 | `class Cat(Animal):` |
| 文件操作 | 读写文本和二进制文件 | `with open("f.txt") as f:` |
| 异常处理 | try/except捕获错误 | `try: ... except:` |
| 正则表达式 | 模式匹配和文本处理 | `re.match(pattern, text)` |

### 2. Python进阶 (Day 16-20)

| 概念 | 说明 | 代码示例 |
|------|------|---------|
| Lambda | 匿名函数 | `lambda x: x**2` |
| map/filter/reduce | 函数式编程三剑客 | `map(str, nums)` |
| 装饰器 | 函数包装和增强 | `@decorator` |
| 闭包 | 函数和其引用环境的组合 | 嵌套函数 |
| 迭代器 | 可迭代对象协议 | `__iter__`, `__next__` |
| 生成器 |惰性迭代器 | `yield x` |
| 时间复杂度 | 算法效率度量 | O(1), O(n), O(n²) |
| 排序算法 | 冒泡、快排、归并 | `sorted(list)` |
| 查找算法 | 二分、顺序查找 | `bisect.bisect()` |

### 3. Web基础 (Day 21-30)

| 概念 | 说明 |
|------|------|
| HTML | 超文本标记语言 |
| CSS | 层叠样式表 |
| JavaScript | 浏览器脚本语言 |
| DOM | 文档对象模型 |
| Vue.js | 渐进式JavaScript框架 |
| npm | Node.js包管理器 |
| 前端工程化 | 模块化、组件化、自动化 |

### 4. Python高级 (Day 31-50)

| 概念 | 说明 |
|------|------|
| MySQL | 关系型数据库 |
| Redis | 内存键值数据库 |
| MongoDB | 文档数据库 |
| SQL | 结构化查询语言 |
| Django | Python Web框架 |
| Flask | 轻量级Web框架 |
| 多线程 | threading模块 |
| 多进程 | multiprocessing模块 |
| 异步编程 | asyncio、aiohttp |
| 单元测试 | pytest、unittest |
| Docker | 容器化技术 |

### 5. 框架开发 (Day 51-70)

| 概念 | 说明 |
|------|------|
| Django ORM | 对象关系映射 |
| REST Framework | RESTful API开发 |
| Scrapy | Python爬虫框架 |
| Selenium | 浏览器自动化测试 |
| NumPy | 数值计算库 |
| Pandas | 数据分析库 |
| scikit-learn | 机器学习库 |
| TensorFlow | 深度学习框架 |
| PyTorch | 深度学习框架 |

### 6. 项目实战 (Day 71-100)

| 概念 | 说明 |
|------|------|
| 系统架构 | MVC、微服务 |
| 用户认证 | JWT、OAuth |
| 权限管理 | RBAC |
| 高并发 | 缓存、队列、负载均衡 |
| 支付集成 | 支付宝、微信支付 |
| 日志监控 | ELK、Prometheus |
| 安全加固 | XSS、CSRF防护 |
| Kubernetes | 容器编排 |
| DevOps | 开发运维一体化 |

## 技术栈全景

```
Python-100-Days 技术栈

├── 基础层
│   ├── Python语法
│   │   ├── 数据类型
│   │   ├── 控制流程
│   │   ├── 函数
│   │   └── 模块
│   ├── 面向对象
│   │   ├── 类和对象
│   │   ├── 继承
│   │   └── 多态
│   └── 数据结构
│       ├── 列表/元组
│       ├── 字典/集合
│       └── 栈/队列
│
├── 进阶层
│   ├── 函数式编程
│   │   ├── Lambda
│   │   ├── map/filter/reduce
│   │   └── 生成器
│   ├── 并发编程
│   │   ├── 多线程
│   │   ├── 多进程
│   │   └── 异步
│   ├── 数据库
│   │   ├── MySQL
│   │   ├── Redis
│   │   └── MongoDB
│   └── 测试
│       ├── 单元测试
│       └── 集成测试
│
├── Web层
│   ├── 前端
│   │   ├── HTML/CSS
│   │   ├── JavaScript
│   │   └── Vue.js
│   ├── 后端
│   │   ├── Django
│   │   └── Flask
│   └── API
│       ├── REST
│       └── GraphQL
│
├── 数据科学层
│   ├── NumPy
│   ├── Pandas
│   ├── Matplotlib
│   ├── scikit-learn
│   ├── TensorFlow
│   └── PyTorch
│
└── 运维层
    ├── Docker
    ├── Kubernetes
    ├── Linux
    ├── Nginx
    └── CI/CD
```

## 学习路径图

```
                    Python-100-Days 学习路径

    ┌─────────────────────────────────────────────────────┐
    │                    Day 01-15                       │
    │                   Python基础                         │
    │  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐      │
    │  │语法 │函数 │数据结构│OOP │文件 │异常 │正则 │      │
    │  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘      │
    └──────────────────────┬──────────────────────────────┘
                           │
    ┌──────────────────────▼──────────────────────────────┐
    │                   Day 16-20                          │
    │                  Python进阶                          │
    │  ┌─────┬─────┬─────┬─────┬─────┐                   │
    │  │Lambda│装饰器│迭代器│算法 │设计 │                   │
    │  └─────┴─────┴─────┴─────┴─────┘                   │
    └──────────────────────┬──────────────────────────────┘
                           │
    ┌──────────────────────▼──────────────────────────────┐
    │                   Day 21-30                          │
    │                   Web基础                           │
    │  ┌─────┬─────┬─────┬─────┬─────┐                   │
    │  │HTML │CSS  │ JS  │Vue.js│工程化│                   │
    │  └─────┴─────┴─────┴─────┴─────┘                   │
    └──────────────────────┬──────────────────────────────┘
                           │
    ┌──────────────────────▼──────────────────────────────┐
    │                   Day 31-50                          │
    │                  Python高级                         │
    │  ┌─────┬─────┬─────┬─────┬─────┬─────┐             │
    │  │数据库│ Web │并发 │测试 │部署 │ Linux│             │
    │  └─────┴─────┴─────┴─────┴─────┴─────┘             │
    └──────────────────────┬──────────────────────────────┘
                           │
    ┌──────────────────────▼──────────────────────────────┐
    │                   Day 51-70                         │
    │                  框架开发                            │
    │  ┌─────┬─────┬─────┬─────┬─────┬─────┐             │
    │  │Django│ Flask│爬虫 │数据 │机器 │深度 │             │
    │  │     │     │    │科学 │学习 │学习 │             │
    │  └─────┴─────┴─────┴─────┴─────┴─────┘             │
    └──────────────────────┬──────────────────────────────┘
                           │
    ┌──────────────────────▼──────────────────────────────┐
    │                   Day 71-100                        │
    │                   项目实战                           │
    │  ┌─────┬─────┬─────┬─────┬─────┬─────┐             │
    │  │架构 │用户 │权限 │高并发│监控 │ K8s │             │
    │  │设计 │系统 │管理 │     │安全 │    │             │
    │  └─────┴─────┴─────┴─────┴─────┴─────┘             │
    └─────────────────────────────────────────────────────┘
```

## 核心概念详解

### 1. 变量和数据类型

Python是动态类型语言，变量不需要声明类型。

```python
# 基本类型
整数 = 42
浮点数 = 3.14
字符串 = "Hello, Python!"
布尔值 = True

# 容器类型
列表 = [1, 2, 3, 4, 5]
元组 = (1, 2, 3)
字典 = {"name": "Python", "version": "3.9"}
集合 = {1, 2, 3, 4, 5}

# 类型检查
print(type(整数))  # <class 'int'>
```

### 2. 面向对象

```python
class Animal:
    """动物基类"""
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    """狗类"""
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    """猫类"""
    def speak(self):
        return f"{self.name} says Meow!"

# 多态
animals = [Dog("Buddy"), Cat("Whiskers")]
for animal in animals:
    print(animal.speak())
```

### 3. 函数式编程

```python
# Lambda表达式
square = lambda x: x ** 2
numbers = [1, 2, 3, 4, 5]
squared = list(map(square, numbers))

# filter
evens = list(filter(lambda x: x % 2 == 0, numbers))

# reduce
from functools import reduce
product = reduce(lambda x, y: x * y, numbers)
```

### 4. 装饰器

```python
def timer(func):
    """计时装饰器"""
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"
```

### 5. 并发编程

```python
import threading
import asyncio

# 多线程
def worker(n):
    print(f"Worker {n} started")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# 异步编程
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### 6. Web开发

```python
# Django
from django.views import View
from django.shortcuts import render

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {'title': 'Home'})

# Flask
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return jsonify({'data': [1, 2, 3]})
```

## 学习建议

### 1. 循序渐进

- **Day 01-15**: 打好Python基础，多动手练习
- **Day 16-20**: 理解高级特性，阅读优秀源码
- **Day 21-30**: 前端配合后端，全面了解Web开发
- **Day 31-50**: 深入数据库和并发编程
- **Day 51-70**: 掌握主流框架，积累项目经验
- **Day 71-100**: 独立完成项目，提升综合能力

### 2. 动手实践

每个知识点都要亲手敲代码：
- 基础语法：100+练习题
- 数据结构：手写链表、树等
- 算法：实现各种排序算法
- Web开发：完成小型博客系统
- 项目实战：完整项目开发

### 3. 代码规范

从一开始就养成好习惯：
- PEP 8代码规范
- 编写文档字符串
- 使用版本控制Git
- 代码注释和命名规范

## 项目价值

### 对个人的价值

1. **系统学习**: 100天完整的学习路径
2. **技能提升**: 从入门到精通
3. **项目经验**: 积累多个完整项目
4. **就业竞争力**: 掌握企业级开发技能

### 对企业的价值

1. **培训教材**: 可作为内部培训材料
2. **技能评估**: 用人参考标准
3. **知识沉淀**: 企业技术知识库

## 相关资源

- GitHub: https://github.com/jackfrued/Python-100-Days
- 作者博客: https://github.com/jackfrued
- Python官方文档: https://docs.python.org/3/
- Django文档: https://docs.djangoproject.com/
- Flask文档: https://flask.palletsprojects.com/

---

*百科创建时间: 2026-04-18*
*项目来源: jackfrued/Python-100-Days*