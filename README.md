# Logseq2Obsidian

This is a simple Python script to convert Logseq markdown to syntax that looks also good in Obsidian.

I love using Logseq to take note. But I am a bit not satisfied (I am greedy 😎) when Obsidian has very fluent mobile experience and a cool graph view. So, I want both 😙. This script lets me take notes in Logseq and easily convert them for Obsidian. That way, I can check my notes on my phone or enjoy the graph view whenever I want 😆. 

## How to run
```
python batch_convert.py --file_path graph --dest_path obsidian_vault
```

Flags:
- `--file_path`: Path to the Logseq notes directory to process. (The script will not change anything in this directory.)
- `--dest_path`: Path to the destination directory. (If this directory exists, the script will delete it and create a new one.)

Your Logseq notes directory will be like this:
```plaintext
graph/
├── pages/
│   ├── notes.md
│   └── ...
├── journals/
│   ├── 2024_08_08.md
│   └── ...
└── assets/
    ├── image.png
    └── ...
```

- The `pages` and `journals` directories contain markdown files to be converted.
- The `assets` directory, along with its contents, will be copied to the destination without changes.

> [!Note] This script is experimental and may not work for all cases. 
> Please backup your files before running this script.
> The script will delete existing content in the destination directory.

## Conversion Process
For each .md in `pages`, `journals`, the script:

1. Processes the properties in the beginning of the file
2. Removes the leading '-', indentation but preserving code block indentation
3. Converts or delete special syntax
    It caters to the following syntax:
    - Convert special syntax:
        - `![image.jpg](image.jpg){:height 300, :width 600}` to `![image.jpg|600](image.jpg)`
        - `{{cloze XXX}}` to `XXX`
        - `DONE` to `- [X]`
        - `TODO` to `- [ ]`
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

## Example Result

#### **Original Logseq Note**
```
- Sample
	- This is a ordered list
	  logseq.order-list-type:: number
	- This is a ordered list
	  logseq.order-list-type:: number
		- This is another ordered list
		  logseq.order-list-type:: number
			- This is also another ordered list
			  logseq.order-list-type:: number
	- This is level-2
- This is level-1
	- ```py
	  # Python code in level-2
	  def func(a, b):
	  	return a, b
	  ```
	- This is table in level-2
	  |Column header1| Column header2|
	  |--|--|
	  |Column1 content|Column2 content|
- $a$
```

#### **Converted Note**
View [here](result.txt).


