import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "skills_db.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"

def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_skill(name, category=None, tags=None, description=None, dependencies=None, version=None):
    data = load_db()
    
    skill = None
    for s in data["skills"]:
        if s["name"] == name:
            skill = s
            break
    
    if not skill:
        print(f"错误：未找到技能 '{name}'")
        return False
    
    if category:
        skill["category"] = category
    if tags:
        skill["tags"] = tags if isinstance(tags, list) else [tag.strip() for tag in tags.split(",")]
    if description:
        skill["description"] = description
    if dependencies:
        skill["dependencies"] = dependencies if isinstance(dependencies, list) else [dep.strip() for dep in dependencies.split(",")]
    if version:
        skill["version"] = version
    
    skill["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    save_db(data)
    
    print(f"✅ 技能 '{name}' 已成功更新")
    print(f"   分类: {skill['category']}")
    print(f"   标签: {', '.join(skill['tags'])}")
    print(f"   描述: {skill['description']}")
    print(f"   版本: {skill['version']}")
    print(f"   更新时间: {skill['last_updated']}")
    return True

def delete_skill(name):
    data = load_db()
    
    skill_index = None
    for i, s in enumerate(data["skills"]):
        if s["name"] == name:
            skill_index = i
            break
    
    if skill_index is None:
        print(f"错误：未找到技能 '{name}'")
        return False
    
    skill = data["skills"].pop(skill_index)
    save_db(data)
    
    print(f"✅ 技能 '{name}' 已从数据库中删除")
    print(f"   提示：技能文件夹仍保留在 {skill['path']}")
    return True

def rename_skill(old_name, new_name):
    data = load_db()
    
    skill = None
    for s in data["skills"]:
        if s["name"] == new_name:
            print(f"错误：技能 '{new_name}' 已存在")
            return False
    
    for s in data["skills"]:
        if s["name"] == old_name:
            skill = s
            break
    
    if not skill:
        print(f"错误：未找到技能 '{old_name}'")
        return False
    
    old_path = SKILLS_DIR / old_name
    new_path = SKILLS_DIR / new_name
    
    if not old_path.exists():
        print(f"警告：技能文件夹不存在: {old_path}")
    else:
        import shutil
        shutil.move(str(old_path), str(new_path))
        print(f"✅ 技能文件夹已重命名: {old_path} -> {new_path}")
    
    skill["name"] = new_name
    skill["path"] = f"skills/{new_name}"
    skill["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    save_db(data)
    
    print(f"✅ 技能 '{old_name}' 已重命名为 '{new_name}'")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="更新技能信息")
    parser.add_argument("--name", required=True, help="技能名称")
    parser.add_argument("--category", help="更新分类")
    parser.add_argument("--tags", help="更新标签（逗号分隔）")
    parser.add_argument("--description", help="更新描述")
    parser.add_argument("--dependencies", help="更新依赖（逗号分隔）")
    parser.add_argument("--version", help="更新版本号")
    parser.add_argument("--delete", action="store_true", help="删除技能")
    parser.add_argument("--rename", help="重命名技能")
    
    args = parser.parse_args()
    
    if args.delete:
        delete_skill(args.name)
    elif args.rename:
        rename_skill(args.name, args.rename)
    else:
        update_skill(
            name=args.name,
            category=args.category,
            tags=args.tags,
            description=args.description,
            dependencies=args.dependencies,
            version=args.version
        )