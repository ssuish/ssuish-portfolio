import os
import shutil
from textnode import TextNode, TextType


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
    public_dir_abs = os.path.abspath("./public")
    static_dir_abs = os.path.abspath("./static")

    if os.path.exists(public_dir_abs):
        shutil.rmtree(public_dir_abs)
    os.makedirs(public_dir_abs, exist_ok=True)

    copy_files(static_dir_abs, public_dir_abs)


def main():
    static_to_public()


if __name__ == "__main__":
    main()
