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
├── assets/
│   ├── image.png
│   └── ...
├── journals/
│   ├── 2024_08_08.md
│   └── ...
└── pages/
    ├── notes.md
    └── ...
```

- The `assets` directory, along with its contents, will be copied to the destination without changes.
- The `pages` and `journals` directories contain markdown files to be converted.

> [!Note] 
> This script is experimental and may not work for all cases.
>
> Note that the script will delete existing content in the destination directory.
> 
> Recommend you copy the `assets`, `journals` and `pages` directories to a newly created directory named graph in this current directory.
> 
> And keep using `--dest_path obsidian_vault` which create a new directory named obsidian_vault in this current directory to store all the converted markdown files.

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

## Automation (Optional)
`automation.sh` is a script that perform conversion automatically. You just need to change `LOGSEQ_SOURCE` and `OBSIDIAN_DESTINATION` to the path to your Logseq directory and Obsidian directory respectively.

```sh
LOGSEQ_SOURCE="/Users/tracywong/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents"
OBSIDIAN_DESTINATION="/Users/tracywong/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tracy's Notes"
```

>[!Caution]
> This script will delete asset, journals, pages folder inside your Obsidian directory if any.
> Please be careful and backup your files before running this script.

### Schedule with Cron: (Optional)
If you want to run `automation.sh` every day, then schedule with Cron.

1. Make the script executable:
```sh
chmod +x automation.sh
```

2. Open the crontab file for editing:
```sh
crontab -e
```

3. Add the following line to run the script every midnight:
```sh
0 0 * * * /path/to/run_conversion.sh
```

> [!Note]
> `0 0`: At minute 0 and hour 0 (midnight).
> 
> `* * *`: Every day of the month, every month, and every day of the week.
