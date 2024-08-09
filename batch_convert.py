import os
import argparse
from conversion import convert_logseq_to_obsidian
import shutil

# copy all .md from a folder to another and convert them
def copy_all_md(src_folder, dest_folder):
    for file in os.listdir(src_folder):
        if file.endswith(".md"):
            src_file = os.path.join(src_folder, file)
            dest_file = os.path.join(dest_folder, file)
            print(f"Copying {src_file} to {dest_file}")
            shutil.copy(src_file, dest_file)
            convert_logseq_to_obsidian(dest_file)

# copy all files from a folder to another
def copy_whole_folder(src_folder, dest_folder):
    # delete dest_folder if it exists
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    
    # copy all files from src_folder to dest_folder
    shutil.copytree(src_folder, dest_folder)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert all Logseq notes to Obsidian notes.")
    parser.add_argument("--file_path", help="Path to the Logseq notes directory to process")
    parser.add_argument("--dest_path", help="Path to the destination directory")
    args = parser.parse_args()
    
    src_folder = args.file_path # e.g. /path/to/graph
    dest_folder = args.dest_path # e.g. /path/to/obsidian_vault
    
    if not os.path.exists(src_folder):
        print(f"Error: The folder {src_folder} does not exist.")
    else:
        for folder_name in ["pages", "journals"]:
            # if {dest_folder}/pages exists, delete it
            if os.path.exists(os.path.join(dest_folder, folder_name)):
                shutil.rmtree(os.path.join(dest_folder, folder_name))
            # create {dest_folder}/pages
            os.makedirs(os.path.join(dest_folder, folder_name))
            # copy all .md from {src_folder}/pages to {dest_folder}/pages and convert them
            copy_all_md(os.path.join(src_folder, folder_name), os.path.join(dest_folder, folder_name))

        copy_whole_folder(os.path.join(src_folder, "assets"), os.path.join(dest_folder, "assets"))

# icloud /Users/tracywong/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tracy's Repository