import os
from block import markdown_to_html_node


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip(" ")
    raise ValueError("There's no title")


def generate_page_recursive(from_dir, template, dest_dir, basepath="/"):
    for fp in os.listdir(from_dir):
        from_path = os.path.join(from_dir, fp)
        dest_path = os.path.join(dest_dir, fp)

        if os.path.isfile(from_path):
            new_dest = dest_path.replace(".md", ".html")
            generate_page(from_path, template, new_dest, basepath)
        else:
            generate_page_recursive(from_path, template, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = None
    template = None

    try:
        with open(from_path, "r") as f:
            md = f.read()
    except FileNotFoundError:
        print(f"Missing file at {from_path}")

    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Missing file at {template_path}")

    html_str = markdown_to_html_node(md).to_html()

    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dir_path = os.path.dirname(dest_path)
    os.makedirs(os.path.abspath(dir_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)
