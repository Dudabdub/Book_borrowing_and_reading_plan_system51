# BookTrack - 图书借阅与读书计划系统（增强版）

## 快速开始

1. 创建虚拟环境并激活
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. 初始化数据库（会创建示例用户和样例数据）
```bash
python init_db.py
```

默认演示用户：`demo@example.com` / 密码：`password`

3. 运行应用
```bash
python run.py
```

4. 在浏览器打开 http://127.0.0.1:5000
