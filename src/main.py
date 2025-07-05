from convert_markdown import markdown_to_html_node, extract_tile

import os
import shutil

def generate_page(source, template_path, destination):
    print(f"Generating page from {source} to {destination} using {template_path}")

    markdown = ""
    with open(source, "r") as file:
        markdown = "".join(file.readlines())

    template = ""
    with open(template_path, "r") as file:
        template = "\n".join(file.readlines())
    
    root_node = markdown_to_html_node(markdown)
    html_content = root_node.to_html()
    page_title = extract_tile(markdown)
    
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", html_content)

    with open(destination, "w") as file:
        file.write(template)

def generate_pages_recursive(source_path, template_path, destination_path):
    for item in os.listdir(source_path):
        item_path = os.path.join(source_path, item)
        dest_path = os.path.join(destination_path, item)
        if os.path.isfile(item_path) and item_path.endswith(".md"):
            generate_page(item_path, template_path, dest_path.replace(".md", ".html"))
        elif os.path.isdir(item_path):
            os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path)

def copy_folder(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    if not os.path.exists(source):
        raise Exception("Source path does not exist - nothing to copy!")
    
    for entry in os.listdir(source):
        full_source_path = os.path.join(source, entry)
        full_destination_path = os.path.join(destination, entry)
        if os.path.isfile(full_source_path):
            print(f"Copying file {full_source_path}")
            shutil.copy(full_source_path, full_destination_path)
        else:
            copy_folder(full_source_path, full_destination_path)


def main():
    public_folder = os.path.abspath("public")
    static_folder = os.path.abspath("static")

    if os.path.exists(public_folder):
        shutil.rmtree(public_folder)

    copy_folder(static_folder, public_folder)

    content_folder = os.path.abspath("content")
    template = os.path.abspath("template.html")
    generate_pages_recursive(content_folder, template, public_folder)

if __name__ == "__main__":
    main()