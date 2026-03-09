import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "skills_db.json"

def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def list_all_skills():
    data = load_db()
    skills = data["skills"]
    
    print(f"\n📋 共有 {len(skills)} 个技能\n")
    print("=" * 80)
    
    for skill in skills:
        print(f"\n📌 {skill['name']}")
        print(f"   分类: {skill['category']}")
        print(f"   描述: {skill['description']}")
        print(f"   标签: {', '.join(skill['tags'])}")
        print(f"   版本: {skill['version']}")
        print(f"   路径: {skill['path']}")
        print(f"   依赖: {', '.join(skill['dependencies'])}")
        print(f"   更新: {skill['last_updated']}")
        print("-" * 80)

def list_by_category(category):
    data = load_db()
    skills = [s for s in data["skills"] if s["category"] == category]
    
    if not skills:
        print(f"未找到分类 '{category}' 的技能")
        return
    
    print(f"\n📋 分类 '{category}' 下有 {len(skills)} 个技能\n")
    print("=" * 80)
    
    for skill in skills:
        print(f"\n📌 {skill['name']}")
        print(f"   描述: {skill['description']}")
        print(f"   标签: {', '.join(skill['tags'])}")
        print(f"   版本: {skill['version']}")
        print("-" * 80)

def list_by_tag(tag):
    data = load_db()
    skills = [s for s in data["skills"] if tag in s["tags"]]
    
    if not skills:
        print(f"未找到标签 '{tag}' 的技能")
        return
    
    print(f"\n📋 标签 '{tag}' 下有 {len(skills)} 个技能\n")
    print("=" * 80)
    
    for skill in skills:
        print(f"\n📌 {skill['name']}")
        print(f"   分类: {skill['category']}")
        print(f"   描述: {skill['description']}")
        print(f"   版本: {skill['version']}")
        print("-" * 80)

def list_categories():
    data = load_db()
    categories = sorted(set(s["category"] for s in data["skills"]))
    
    print(f"\n📋 共有 {len(categories)} 个分类\n")
    print("=" * 80)
    
    for category in categories:
        count = sum(1 for s in data["skills"] if s["category"] == category)
        print(f"   {category} ({count} 个技能)")

def list_tags():
    data = load_db()
    all_tags = set()
    for skill in data["skills"]:
        all_tags.update(skill["tags"])
    tags = sorted(all_tags)
    
    print(f"\n📋 共有 {len(tags)} 个标签\n")
    print("=" * 80)
    
    for tag in tags:
        count = sum(1 for s in data["skills"] if tag in s["tags"])
        print(f"   {tag} ({count} 个技能)")

def search_skill(keyword):
    data = load_db()
    keyword = keyword.lower()
    
    skills = [
        s for s in data["skills"]
        if keyword in s["name"].lower() or 
           keyword in s["description"].lower() or
           keyword in s["category"].lower() or
           any(keyword in tag.lower() for tag in s["tags"])
    ]
    
    if not skills:
        print(f"未找到包含关键词 '{keyword}' 的技能")
        return
    
    print(f"\n📋 找到 {len(skills)} 个包含关键词 '{keyword}' 的技能\n")
    print("=" * 80)
    
    for skill in skills:
        print(f"\n📌 {skill['name']}")
        print(f"   分类: {skill['category']}")
        print(f"   描述: {skill['description']}")
        print(f"   标签: {', '.join(skill['tags'])}")
        print(f"   版本: {skill['version']}")
        print("-" * 80)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="查询技能列表")
    parser.add_argument("--all", action="store_true", help="列出所有技能")
    parser.add_argument("--category", help="按分类查询")
    parser.add_argument("--tag", help="按标签查询")
    parser.add_argument("--search", help="关键词搜索")
    parser.add_argument("--categories", action="store_true", help="列出所有分类")
    parser.add_argument("--tags", action="store_true", help="列出所有标签")
    
    args = parser.parse_args()
    
    if args.all:
        list_all_skills()
    elif args.category:
        list_by_category(args.category)
    elif args.tag:
        list_by_tag(args.tag)
    elif args.search:
        search_skill(args.search)
    elif args.categories:
        list_categories()
    elif args.tags:
        list_tags()
    else:
        list_all_skills()