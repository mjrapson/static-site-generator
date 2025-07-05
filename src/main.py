from convert_markdown import markdown_to_html_node, extract_tile

import os
import shutil

def generate_page(source, template_path, destination):
    print(f"Generating page from {source} to {destination} using {template_path}")

    markdown = ""
    with open(source, "r") as file:
        markdown = "\n".join(file.readlines())

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

    content = os.path.join(os.path.abspath("content"), "index.md")
    template = os.path.abspath("template.html")
    destination_page = os.path.join(public_folder, "index.html")
    
    generate_page(content, template, destination_page)

if __name__ == "__main__":
    main()