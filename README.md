# cite_paper_downloader

## What we can do

- Find all articles that have cited your article
- Get links to all articles and PDF download links (if available)
- Get the author names of all articles

## How to use

1. Confirm that Google Scholar can be accessed directly without using VPN

2. Download repository

 `pip install -r requirements.txt`

For simply start:

 `python ./get_cite_papers.py --paper_name 'Your Paper Name'`

Paper info will save in `./{paper_name}_full_report.csv`

Authors info will save in `./{paper_name}_authors.csv`

| args |  | desc |
|-------|-------|-------|
| -p | --paper_name | Paper Name |
| -d | --base_dir | Save Path |
| -dp | --is_download_pdf | Set True to download PDF |
| -da | --is_authors | Set True to get authors info |
| -m | --max_wait | Max Waitting Time |
| -b | --debug | Debug mode |


