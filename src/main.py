import os
import shutil
import sys
from generate_page import generate_page_recursive


def copy_files(source_dir, dest_dir):
    for i in os.listdir(source_dir):
        source = os.path.join(source_dir, i)
        dest = os.path.join(dest_dir, i)

        print(f"Copying {source} to {dest}")

        if os.path.isfile(source):
            shutil.copy(source, dest)
        else:
            os.mkdir(dest)
            copy_files(source, dest)


def static_to_public():
    public_dir_abs = os.path.abspath("./docs")
    static_dir_abs = os.path.abspath("./static")

    if os.path.exists(public_dir_abs):
        shutil.rmtree(public_dir_abs)
    os.makedirs(public_dir_abs, exist_ok=True)

    copy_files(static_dir_abs, public_dir_abs)


def main():
    public_dir_abs = os.path.abspath("./docs")
    dir_path_content = os.path.abspath("./content")
    template_path = os.path.abspath("./template.html")
    basepath = None

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    static_to_public()
    generate_page_recursive(
        dir_path_content,
        template_path,
        public_dir_abs,
        basepath,
    )


if __name__ == "__main__":
    main()
