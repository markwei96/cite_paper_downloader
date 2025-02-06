# cite_paper_downloader

## What we can do

- Find all articles that have cited your article
- Get links to all articles and PDF download links (if available)
- Get the author names of all articles
- Get the author's personal links, positions, citation counts, and the number of publications in Nature, Science, and PNAS journals

## How to use

1. Confirm that Google Scholar can be accessed directly without using VPN

2. Download repository

 `pip install -r requirements.txt`

For simply start:

 `python ./get_cite_papers.py --paper_name 'Your Paper Name'`


| args |  | desc |
|-------|-------|-------|
| -p | --paper_name | Paper Name |
| -d | --base_dir | Save Path |
| -dp | --is_download_pdf | Set True to download PDF |
| -da | --is_authors | Set True to get authors info |
| -m | --max_wait | Max Waitting Time |
| -b | --debug | Debug mode |

## Outputs

 File will save in path: `./Your_Paper_Name/`


- **authors_full_info.csv**: This file contains detailed information about the authors, including their names, positions, personal links, citation counts, and the number of publications in Nature, Science, and PNAS journals.
- **authors_nature_list.csv, pnas, science**: These files are used to verify the authenticity of publications in high-impact journals. For example, journals like Nature Communications might be mistakenly categorized as Nature. These files help identify and correct such misclassifications.
- **authors.csv**: This file lists the authors of each cited paper.
- **full_report.csv**: This file contains the names of all the cited papers.