# JS Finding

JS Finding is a Python tool for extracting JavaScript (JS) files from a given list of domains. This tool utilizes various utilities such as `waybackurls`, `gauplus`, and `subjs` to perform JS file extraction from the specified domains.

## Features

- Extract JavaScript (JS) files from a list of url/domains
- Supports extraction through `waybackurls`, `gauplus`, and `subjs`
- Option to download the successfully extracted JS files
- Option to create wordlists from the downloaded JS file contents

## Requirements

- Python 3.x

## Installation
```
git clone https://github.com/pikpikcu/js-finding.git
cd js-finding
pip install -r requirements.txt
```
## Usage

![JS Finding Usage](images/usage.png)

JS Finding can be used to extract JavaScript (JS) files from either a single domain URL or a list of domains. The tool supports various extraction methods and provides additional options for file download and wordlists creation.

### Single Domain Extraction

To extract JS files from a single domain, use the following command:

`python3 js.py -u <url> -o <output_file> [options]`

- `-u` or `--url`: The URL of the single domain to extract JS files from.
- `-o` or `--output`: The output file name to store the extraction results.
- `[options]`: Additional options such as `-d`, `-download`, `-output-dir`, and `-create-lists`.

### Multiple Domains Extraction

To extract JS files from a list of domains, create a file containing the list of domains (one domain per line) and use the following command:
`python3 js.py -l <list_file> -o <output_file> [options]`


- `-l` or `--list`: The file name containing the list of domains.
- `-o` or `--output`: The output file name to store the extraction results.
- `[options]`: Additional options such as `-d`, `-download`, `-output-dir`, and `-create-lists`.

### Additional Options

- `-d` or `--debug`: Enable debug mode to print additional debug information.
- `-download`: Enable downloading of the successfully extracted JS files.
- `-output-dir`: The directory to store the downloaded JS files.
- `-create-lists`: Enable creation of wordlists from the downloaded JS file contents.

### Examples

Extract JS files from a single domain and create wordlists:

`python3 js.py -u example.com -o output.txt -d -download -output-dir files/ -create-lists`

### JS Analyse with nuclei

![JS Analyse with nuclei](images/nuclei.png)

## Notes

- Make sure to install all the required dependencies before running this tool.
- Verify that commands such as `waybackurls`, `gauplus`, and `subjs` are already in your system's PATH.
