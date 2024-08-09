"""
1. processes the properties in the beginning of the file
2. removes the leading '-', indentation but preserving code block indentation
3. converts or delete special syntax
    It caters to the following syntax:
    - Convert special syntax:
        - ![image.jpg](image.jpg){:height 300, :width 600} to ![image.jpg|600](image.jpg)
        - {{cloze XXX}} to XXX
        - DONE to - [X]
        - TODO to - [ ]
    - Deletes syntax that is not used in Obsidian:
        - collapsed:: true
        - logseq.order-list-type:: number
        - background-color:: XXX
        - card-last-score:: XXX
        - card-repeats:: XXX
        - card-next-schedule:: XXX
        - card-last-interval:: XXX
        - card-ease-factor:: XXX
        - card-last-reviewed:: XXX
    - Converts syntax of callouts
"""

import os
import argparse
import re


def convert_special_syntax(line: str) -> str:
    # ![image.jpg](image.jpg){:height 300, :width 600} to ![image.jpg|600](image.jpg)
    line = re.sub(
        r"!\[(.*?)]\((.*?)\){:height \d*, :width (\d*)}",
        lambda match: f"![{match[1]}|{match[3]}]({match[2]})",
        line,
    )
    # replace {{cloze XXX}} with XXX
    line = re.sub(r"{{cloze (.*?)}}", r"\1", line)

    # replace TODO/DONE with - [ ]/- [X]
    line = re.sub(r"^DONE", "- [X]", line)
    line = re.sub(r"^TODO", "- [ ]", line)
    
    return line


def delete_syntax(line: str) -> str:
    original_line = line

    # Deletes syntax that is not used in Obsidian
    line = re.sub(r"\s*collapsed:: true\s*", "", line)
    line = re.sub(r"\s*logseq.order-list-type:: number\s*", "", line)
    line = re.sub(r"\s*background-color:: yellow\s*", "", line)
    line = re.sub(r"\s*background-color:: red\s*", "", line)
    line = re.sub(r"\s*background-color:: pink\s*", "", line)
    line = re.sub(r"\s*background-color:: green\s*", "", line)
    line = re.sub(r"\s*background-color:: blue\s*", "", line)
    line = re.sub(r"\s*background-color:: purple\s*", "", line)
    line = re.sub(r"\s*background-color:: gray\s*", "", line)

    # delete the following lines
    # card-last-score:: 5
    # card-repeats:: 1
    # card-next-schedule:: 2024-05-09T11:21:17.527Z
    # card-last-interval:: 4
    # card-ease-factor:: 2.6
    # card-last-reviewed:: 2024-05-05T11:21:17.528Z
    line = re.sub(r"card-last-score:: \d", "", line)
    line = re.sub(r"card-repeats:: \d", "", line)
    line = re.sub(r"card-next-schedule:: .*", "", line)
    line = re.sub(r"card-last-interval:: \d", "", line)
    line = re.sub(r"card-ease-factor:: \d.\d", "", line)
    line = re.sub(r"card-last-reviewed:: .*", "", line)

    # Remove the line if it's empty
    if line != original_line:
        line = ""

    return line


def convert_callouts(input_text):
    # Convert syntax of callouts

    # Updated pattern to include NOTE, TIP, QUOTE, IMPORTANT, CAUTION, EXAMPLE
    pattern = r"\#\+BEGIN_(NOTE|TIP|QUOTE|IMPORTANT|CAUTION|EXAMPLE)\n(.*?)\n\#\+END_\1"
    matches = re.findall(pattern, input_text, re.DOTALL)

    for callout_type, match in matches:
        lines = match.split("\n")
        formatted_lines = [f">{line}" for line in lines]
        formatted_text = "\n".join(formatted_lines)
        formatted_block = f">[!{callout_type.capitalize()}]\n{formatted_text}\n"

        # Replace the entire block with the formatted block
        input_text = input_text.replace(
            f"#+BEGIN_{callout_type}\n{match}\n#+END_{callout_type}", formatted_block
        )

    return input_text


def convert_logseq_to_obsidian(file_path):
    inside_code_block = False
    code_block_indent = 0
    # Store the lines after processing properties, removing the leading '-', indentation but preserving code block indentation
    output_lines = []
    updated_lines = []  # Store the lines after processing the content
    modified_lines = []  # Store the lines after processing the content

    with open(file_path, "r") as file:
        lines = file.readlines()

        """
        First loop: Process the properties
        alias:: abc, def 
        becomes
        ---
        alias: 
         - abc
         - def
        ---
        """
        metadata = {}
        has_metadata = False
        line_after_metadata = 0

        for idx, line in enumerate(lines):
            match = re.match(r"(.*?)::[\s]*(.*)", line)
            if match is not None:
                has_metadata = True
                metadata[match[1]] = match[2]
                line_after_metadata = idx + 1
            else:
                break

        if has_metadata:
            output_lines.append("---\n")
            for key, value in metadata.items():
                if ", " in value:
                    value = value.split(", ")
                    output_lines.append(f"{key}:\n")
                    for v in value:
                        output_lines.append(f"  - {v}\n")
                else:
                    output_lines.append(f"{key}: {value}\n")
            
            output_lines.append("---\n")

        # Second loop: Remove "-" and all indentation, but preserving indentation in code block
        for line in lines[line_after_metadata:]:
            # Check if we're entering or exiting a code block
            stripped_line = line.lstrip().lstrip("-").lstrip()
            if stripped_line.startswith("```"):
                inside_code_block = not inside_code_block
                code_block_indent = len(line) - len(stripped_line)
                print(f"Code block indent: {code_block_indent}")
                # 3: \t, -, space
                code_block_indent = code_block_indent - 2
                output_lines.append(stripped_line)
                continue

            if inside_code_block:
                # Remove the calculated indentation for code blocks
                if code_block_indent > 0:
                    output_lines.append(
                        line[code_block_indent:].lstrip("  ")
                    )  # Remove the tab in the front and two spaces if any
                else:
                    output_lines.append(line)

            else:
                # add space between blocks
                # if line.lstrip().startswith('-'):
                #     output_lines.append("\n")

                # Remove leading '-' and any indentation
                stripped_line = line.lstrip("-").lstrip().lstrip("-").lstrip()

                # Add newline if it's not there because lstrip() removes empty lines
                if not stripped_line.endswith("\n"):
                    stripped_line += "\n"

                output_lines.append(stripped_line)

        # Third loop: Convert special syntax
        for line in output_lines:
            line = convert_special_syntax(line)

            updated_lines.append(line)

        # Fourth loop: Delete syntax that is not used in Obsidian
        for line in updated_lines:
            modified_line = delete_syntax(line)

            if line.isspace() or not modified_line.isspace() or line == "\n":
                modified_lines.append(modified_line)

        all_lines = "".join(modified_lines)

        all_lines = convert_callouts(all_lines)

    # Write the processed lines back to the file
    with open(file_path, "w") as file:
        file.writelines(all_lines)


if __name__ == "__main__":
    # Example usage: python auto_convert_notes.py --file_path /path/to/note.md --dest_path /path/to/converted_note.md
    parser = argparse.ArgumentParser(
        description="Convert a single Logseq note to syntax that looks good in Obsidian."
    )
    parser.add_argument("--input_path", help="Path to the Logseq note to process")
    parser.add_argument("--output_path", help="Path to the destination file")
    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"Error: The file '{args.file_path}' does not exist.")
    else:
        convert_logseq_to_obsidian(args.file_path)
