import json
import shutil
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "skills_db.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"

def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def import_skill(skill_name, project_path, new_name=None):
    data = load_db()
    
    skill = None
    for s in data["skills"]:
        if s["name"] == skill_name:
            skill = s
            break
    
    if not skill:
        print(f"错误：未找到技能 '{skill_name}'")
        return False
    
    skill_source = Path(__file__).parent.parent / skill["path"]
    
    if not skill_source.exists():
        print(f"错误：技能源文件夹不存在: {skill_source}")
        return False
    
    project_dir = Path(project_path)
    if not project_dir.exists():
        print(f"错误：项目路径不存在: {project_path}")
        return False
    
    target_name = new_name if new_name else skill_name
    target_path = project_dir / target_name
    
    if target_path.exists():
        print(f"错误：目标文件夹已存在: {target_path}")
        return False
    
    shutil.copytree(skill_source, target_path)
    
    print(f"✅ 技能 '{skill_name}' 已成功导入到项目")
    print(f"   源路径: {skill_source}")
    print(f"   目标路径: {target_path}")
    print(f"   版本: {skill['version']}")
    print(f"   依赖: {', '.join(skill['dependencies'])}")
    return True

def import_multiple_skills(skill_names, project_path):
    success_count = 0
    for skill_name in skill_names:
        if import_skill(skill_name, project_path):
            success_count += 1
        print()
    
    print(f"导入完成：成功 {success_count}/{len(skill_names)} 个技能")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="将技能导入到项目")
    parser.add_argument("--name", help="要导入的技能名称")
    parser.add_argument("--project", required=True, help="项目路径")
    parser.add_argument("--new-name", help="导入后的新名称（可选）")
    parser.add_argument("--list", help="导入多个技能，用逗号分隔")
    
    args = parser.parse_args()
    
    if args.list:
        skill_names = [name.strip() for name in args.list.split(",")]
        import_multiple_skills(skill_names, args.project)
    elif args.name:
        import_skill(args.name, args.project, args.new_name)
    else:
        print("错误：必须指定 --name 或 --list 参数")
        parser.print_help()