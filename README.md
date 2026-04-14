


<!-- ABOUT THE PROJECT -->
## About The Project

This script will automatically run through a list of Google searches, in order to automate Google Dorks for pen testing engagements.

![Script Screenshot](https://github.com/LukeLauterbach/Google-Dorking-Automation/blob/main/Images/Example.png)

### Built With

* [Python](https://www.python.org/)
* [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/)


<!-- GETTING STARTED -->
## Getting Started

This script relies on Google's Programmable Search Engine, which will require a short setup in order to get an ID and API key. After initial setup is complete, running the script is a simple command.

### Installation

1. Install with pipx: `pipx install git+https://github.com/LukeLauterbach/Google-Dorking-Automation`
   1. Or with uv: `uv tool install git+https://github.com/LukeLauterbach/Google-Dorking-Automation`
2. Get a free [Google Programmable Search Engine ID](https://programmablesearchengine.google.com/about/)
3. Get a free [Google Custom Search API key](https://developers.google.com/custom-search/v1/introduction). Note: Free keys can only run 100 searches per day. A paid account can be set up to run more than 100 searches per day. Multiple free API keys could also be generated and inserted into this list, which the script would then iterate through.
4. Either:
   1. Note your Search Engine ID and API key for later.
   2. Add Environment variables for your Search Engine ID and API keys:
      1. `export GOOGLE_SEARCH_ENGINE_ID=YOUR_SEARCH_ENGINE_ID`
      2. `export GOOGLE_API_KEYS=YOUR_API_KEY`

## Usage

```shell
dork -d example.com [OPTIONS]
```

The script uses a pre-packaged `ListOfDorks.csv` by default. A different list of dorks can be specified with the `-l FILENAME` option.

A domain should be passed with `-d DOMAIN` (comma-separated for multiple domains). A company name can also be specified with `-c COMPANY_NAME`. If no company name is specified, any dorks referencing company name will be skipped.

## Options
Options | Description
-|-
-d, --domains | Domain(s) to dork. Use commas for multiple domains.
-c, --company | Company name. If omitted, dorks containing `{company}` are skipped.
-l, --list-of-dorks | CSV file containing dorks. Defaults to packaged `ListOfDorks.csv`.
-cf, --config-file | Config filename.
-se, --search-engine-id | Search Engine ID (if not provided via config/environment).
-ak, --api-key | API key(s) (if not provided via config/environment).
-g, --github-api-key | GitHub API token for GitHub dork checks.
-q, --quiet | Quiet mode (only outputs successful dorks).
-v, --verbose | Verbose mode.
-db, --debug | Debug mode (runs one dork then exits).

## List of Dorks

The script will read a CSV containing a list of Google Dorks to run. An example is available [here](https://github.com/LukeLauterbach/Google-Dorking-Automation/blob/main/Utils/ListOfDorks.csv).

Dorks can contain two variables: `{domain}` (the domain name you would like to restrict searches to), and `{company}` (the company name). If a dork contains `{company}`, but no company name is specified through the `-c` option, it will be skipped.

The CSV contains three columns. 
* *Dork Name* is required and will be the search that the script will run.
* *Description* is optional and will be ignored by the script.
* *Who Added* is optional and will be ignored by the script. This is intended for teams, who might have multiple people adding to a central list.
