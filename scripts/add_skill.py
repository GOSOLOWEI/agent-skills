import json
import os
import shutil
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "skills_db.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"
TEMPLATE_DIR = Path(__file__).parent.parent / "skill_templates" / "template_skill"

def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_skill(name, category, tags, description, dependencies, version="1.0.0", use_template=True):
    data = load_db()
    
    for skill in data["skills"]:
        if skill["name"] == name:
            print(f"错误：技能 '{name}' 已存在")
            return False
    
    skill_path = SKILLS_DIR / name
    
    if skill_path.exists():
        print(f"错误：技能文件夹 '{skill_path}' 已存在")
        return False
    
    os.makedirs(skill_path, exist_ok=True)
    
    if use_template and TEMPLATE_DIR.exists():
        for item in TEMPLATE_DIR.iterdir():
            if item.is_file():
                shutil.copy2(item, skill_path / item.name)
    
    skill_info = {
        "name": name,
        "category": category,
        "tags": tags if isinstance(tags, list) else [tag.strip() for tag in tags.split(",")],
        "description": description,
        "path": f"skills/{name}",
        "dependencies": dependencies if isinstance(dependencies, list) else [dep.strip() for dep in dependencies.split(",")],
        "version": version,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    data["skills"].append(skill_info)
    save_db(data)
    
    print(f"✅ 技能 '{name}' 已成功添加")
    print(f"   路径: {skill_path}")
    print(f"   分类: {category}")
    print(f"   标签: {', '.join(skill_info['tags'])}")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="添加新技能到数据库")
    parser.add_argument("--name", required=True, help="技能名称")
    parser.add_argument("--category", required=True, help="技能分类")
    parser.add_argument("--tags", required=True, help="技能标签（逗号分隔）")
    parser.add_argument("--description", required=True, help="技能描述")
    parser.add_argument("--dependencies", default="", help="依赖列表（逗号分隔）")
    parser.add_argument("--version", default="1.0.0", help="版本号")
    parser.add_argument("--no-template", action="store_true", help="不使用模板")
    
    args = parser.parse_args()
    
    add_skill(
        name=args.name,
        category=args.category,
        tags=args.tags,
        description=args.description,
        dependencies=args.dependencies,
        version=args.version,
        use_template=not args.no_template
    )