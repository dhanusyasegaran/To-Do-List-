from jinja2 import Environment, FileSystemLoader
import sys
import os

def check_templates(template_dir):
    env = Environment(loader=FileSystemLoader(template_dir))
    errors = 0
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                try:
                    env.get_template(rel_path)
                    print(f"OK: {rel_path}")
                except Exception as e:
                    print(f"ERROR in {rel_path}: {e}")
                    errors += 1
    return errors

if __name__ == "__main__":
    t_dir = sys.argv[1] if len(sys.argv) > 1 else 'templates'
    sys.exit(check_templates(t_dir))
