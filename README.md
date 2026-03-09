# Agent Skills 管理系统

一个高效管理和组织 Agent 技能的本地仓库，支持版本控制和协作。

## 目录结构

```
agent_skills/
├── skills_db.json              # 全部技能的元数据（分类、描述、标签、依赖等）
├── README.md                   # 总览和使用说明
├── skill_templates/            # 技能模板
│   └── template_skill/
│       ├── main.py            # 主程序模板
│       ├── config.yaml        # 配置文件模板
│       └── README.md          # 文档模板
├── skills/                     # 所有技能的实际文件夹
│   ├── weather_query/
│   └── email_sender/
└── scripts/                    # 管理脚本（Python）
    ├── add_skill.py           # 新增技能到数据库和文件夹
    ├── import_skill.py        # 从 skills_db.json 导入技能到项目
    ├── list_skills.py         # 查询技能（按分类、标签等）
    └── update_skill.py        # 更新技能信息
```

## 快速开始

### 1. 添加新技能

使用 `add_skill.py` 脚本添加新技能：

```bash
python scripts/add_skill.py \
  --name "my_skill" \
  --category "信息查询" \
  --tags "Python,API" \
  --description "技能描述" \
  --dependencies "requests,json" \
  --version "1.0.0"
```

参数说明：
- `--name`: 技能名称（必需）
- `--category`: 技能分类（必需）
- `--tags`: 技能标签，逗号分隔（必需）
- `--description`: 技能描述（必需）
- `--dependencies`: 依赖列表，逗号分隔（可选）
- `--version`: 版本号（默认：1.0.0）
- `--no-template`: 不使用模板创建文件

### 2. 查询技能

使用 `list_skills.py` 脚本查询技能：

```bash
# 列出所有技能
python scripts/list_skills.py --all

# 按分类查询
python scripts/list_skills.py --category "信息查询"

# 按标签查询
python scripts/list_skills.py --tag "Python"

# 关键词搜索
python scripts/list_skills.py --search "天气"

# 列出所有分类
python scripts/list_skills.py --categories

# 列出所有标签
python scripts/list_skills.py --tags
```

### 3. 导入技能到项目

使用 `import_skill.py` 脚本将技能导入到项目：

```bash
# 导入单个技能
python scripts/import_skill.py \
  --name "weather_query" \
  --project "C:\Users\YourName\my_project\skills"

# 导入多个技能
python scripts/import_skill.py \
  --list "weather_query,email_sender" \
  --project "C:\Users\YourName\my_project\skills"

# 导入并重命名
python scripts/import_skill.py \
  --name "weather_query" \
  --project "C:\Users\YourName\my_project\skills" \
  --new-name "weather"
```

### 4. 更新技能信息

使用 `update_skill.py` 脚本更新技能信息：

```bash
# 更新技能信息
python scripts/update_skill.py \
  --name "weather_query" \
  --category "新分类" \
  --tags "新标签1,新标签2" \
  --description "新描述" \
  --version "2.0.0"

# 重命名技能
python scripts/update_skill.py \
  --name "old_name" \
  --rename "new_name"

# 删除技能
python scripts/update_skill.py \
  --name "skill_name" \
  --delete
```

## skills_db.json 格式

`skills_db.json` 是核心文件，记录每个技能的信息：

```json
{
  "skills": [
    {
      "name": "weather_query",
      "category": "信息查询",
      "tags": ["Python", "API", "天气"],
      "description": "根据城市获取天气信息",
      "path": "skills/weather_query",
      "dependencies": ["requests", "json"],
      "version": "1.0.0",
      "last_updated": "2026-03-09"
    }
  ]
}
```

字段说明：
- `name`: 技能名称（唯一标识）
- `category`: 技能分类
- `tags`: 技能标签列表
- `description`: 技能描述
- `path`: 技能文件夹路径
- `dependencies`: 依赖列表
- `version`: 版本号
- `last_updated`: 最后更新日期

## 技能模板

使用 `skill_templates/template_skill` 作为新技能的模板：

- `main.py`: 主程序模板
- `config.yaml`: 配置文件模板
- `README.md`: 文档模板

## Git + GitHub 管理

### 初始化仓库

```bash
cd agent_skills
git init
git add .
git commit -m "初始化 agent skills 仓库"
```

### 推送到 GitHub

```bash
git remote add origin https://github.com/你的用户名/agent_skills.git
git branch -M main
git push -u origin main
```

### 后续更新

每次新增或更新技能后：

```bash
git add .
git commit -m "添加/更新 skill: 技能名称"
git push
```

## 使用建议

1. **快速查找**: 使用 `list_skills.py` 按分类/标签查询需要的技能
2. **快速导入**: 使用 `import_skill.py` 将技能复制到当前项目
3. **版本管理**: 每次更新 skill 文件或 skills_db.json 都用 Git 提交
4. **协作开发**: 通过 GitHub 进行团队协作和代码审查

## 系统要求

- Python 3.7+
- Windows 操作系统
- Git（用于版本控制）

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！