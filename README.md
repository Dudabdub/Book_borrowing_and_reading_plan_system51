
# 📚 BookTrack 图书借阅与读书计划系统
一个基于 **Python + Flask** 开发的轻量级图书借阅管理与读书计划跟踪系统。
系统支持图书管理、借阅记录、用户登录注册、读书计划创建与阅读进度可视化，适用于个人读书管理、图书室、小规模书库等场景。

---

# 📖 项目概述

BookTrack 是一个 Web 应用程序，通过 Flask 框架实现。
系统采用模块化设计，支持图书信息管理、借阅逻辑处理、个人阅读计划跟踪以及图表展示等功能。
项目界面简洁易用，是学习 Flask Web 开发与图书管理逻辑的优秀示例项目。

---

# ✨ 功能特性

### 📘 图书管理

* 添加图书（名称、作者、描述、库存）
* 查看全部图书
* 编辑 / 删除图书
* 查看图书详情页

### 🔖 图书借阅管理

* 支持借阅书籍
* 借阅前自动检查库存
* 显示借阅历史记录

### 📝 阅读计划管理

* 创建阅读计划（目标页数、计划时间）
* 更新阅读进度
* 自动计算完成百分比
* 进度条形式展示效果

### 📊 阅读可视化仪表盘

* 每本书阅读进度图表
* 总阅读概览统计
* 可视化阅读趋势（折线图、饼图）

### 🔐 用户认证模块

* 用户注册
* 用户登录
* 访问权限控制
* Session 管理

---

# 🛠️ 技术栈

* **语言：Python 3.9+**
* **Web 框架：Flask**
* **前端：HTML + CSS + JavaScript + Chart.js**
* **数据库：SQLite**
* **环境管理：pip / venv**
* **数据结构：SQLAlchemy ORM**

---

# 🚀 快速开始

## 环境要求

* Python 3.9 或以上版本
* pip 套件管理工具
* 建议安装虚拟环境（venv）

---

## 📥 安装与运行

### ① 克隆项目

```bash
git clone https://github.com/yourname/BookTrack.git
cd BookTrack
```

### ② 安装依赖

```bash
pip install -r requirements.txt
```

### ③ 初始化数据库

```bash
python init_db.py
```

### ④ 启动项目

```bash
python run.py
```

然后访问：

```
http://127.0.0.1:5000
```

---

# 📁 项目结构

```
BookTrack/
├── app/
│   ├── __init__.py               # Flask应用工厂
│   ├── main.py                   # 应用入口
│   ├── models.py                 # 数据库模型
│   ├── routes.py                 # 路由管理
│   ├── auth.py                   # 用户认证模块
│   ├── utils/
│   │   ├── __init__.py
│   │   └── progress_calculator.py  # 阅读进度计算工具
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── books.html
│   │   ├── book_detail.html
│   │   ├── book_form.html
│   │   ├── plans.html
│   │   ├── plan_form.html
│   │   └── auth/
│   │       ├── login.html
│   │       └── register.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
│
├── config.py                     # 系统配置
├── init_db.py                    # 初始化数据库脚本
├── run.py                        # 启动程序入口
├── requirements.txt              # 依赖文件
├── README.md                     # 项目说明文档
└── .gitignore
```

---

# 💻 使用指南

启动系统后，首页会显示阅读仪表盘和功能入口。

📌 可用功能包括：

* **查看全部图书**
* **添加新图书**
* **借阅图书**
* **管理阅读计划**
* **查看阅读图表统计**
* **登录 / 注册用户**

所有操作都通过直观的网页界面完成，无需命令行操作。

---

# 📄 许可证

本项目遵循 **MIT License**。

---


