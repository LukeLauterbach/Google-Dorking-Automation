<div id="top"></div>

<h3 align="center">Google Dorking Automation</h3>

  <p align="center">
    <a href="https://github.com/LukeLauterbach/Google-Dorking-Automation">View Demo</a>
    ·
    <a href="https://github.com/LukeLauterbach/Google-Dorking-Automation/issues">Report Bug</a>
    ·
    <a href="https://github.com/LukeLauterbach/Google-Dorking-Automation/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Using API Keys</a>
      <ul>
        <li><a href="#using-api-keys">Using API Keys</a></li>
      </ul>
    </li>
    <li><a href="#options">Options</a></li>
    <li><a href="#list-of-dorks">List of Dorks</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This script will automatically run through a list of Google searches, in order to automate Google Dorks for pen testing engagements.

![Script Screenshot](https://github.com/LukeLauterbach/Google-Dorking-Automation/blob/main/Images/Example.png)

### Built With

* [Python](https://www.python.org/)
* [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This script relies on Google's Programmable Search Engine, which will require a short setup in order to get an ID and API key. After initial setup is complete, running the script is a simple command.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/LukeLauterbach/Google-Dorking-Automation.git
   ```
2. Get a free [Google Programmable Search Engine ID](https://programmablesearchengine.google.com/about/)
3. Get a free [Google Custom Search API key](https://developers.google.com/custom-search/v1/introduction). Note: Free keys can only run 100 searches per day. A paid account can be set up to run more than 100 searches per day. Multiple free API keys could also be generated and inserted into this list, which the script would then iterate through.
4. Note your Search Engine ID and API Key(s) for later. 

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

```shell
python3 GoogleDorking.py [TARGET_DOMAIN] [OPTIONAL OPTIONS] 
```

The script will look for a file in the current directory named "ListOfDorks.csv," and will iterate through each line in the CSV. A different list of dorks can be specified with the `-l FILENAME` option.

A domain name is the only required arugment. A company name can also be specified with the `-c COMPANY_NAME` option. If no company name is specified, any dorks referencing company name will be skipped.

### Using API Keys

There are three options for using the API key and Search Engine ID that were created during the installation steps. 

#### Config File
The Search Engine ID and all API keys can be stored in a config file, which can be imported into the script using the `-cf {FILENAME}` parameter. With this option, the Search Engine ID must be on the first line, and all API keys must be on their own subsequent lines.

#### Modify The Script
Don't like keeping track of a config file? You can put your Search Engine ID and API keys directly in the script, starting on line 17. API Keys should be appended to the keyList variable and your Search Engine ID can simply go in the SEARCH_ENGINE_ID string. 

```py
keyList = []
keyList.append("")
SEARCH_ENGINE_ID = ""
```

#### Parameters
The `-se {SEARCH ENGINE ID}` and `-ak {API KEY}` parameters can be used to directly input your Search Engine ID and API keys in the command line. However, this is not recommended, as this will only allow for one API key. 

<p align="right">(<a href="#top">back to top</a>)</p>

## Options
Options | Description
-|-
-d | Specify a domain
-c | Specify a company name. If no company name is specified, dorks referencing company name will be skipped. If the company name has a space in it, the name should be encased in quotes.
-l | Filename with list of dorks (defaults to ListOfDorks.csv in current folder)
-cf | Config Filename
-se | Search Engine ID (only needed if API keys aren't in a config file or in the script)
-ak | API Key (only needed if API keys aren't in a config file or in the script)
-q | Quiet Mode (only outputs successful dorks)
-v | Verbose Mode (outputs Google APAI key alerts)
-db | Debug Mode (only runs one dork)

## List of Dorks

The script will read a CSV containing a list of Google Dorks to run. An example is available [here](https://github.com/LukeLauterbach/Google-Dorking-Automation/blob/main/ListOfDorks.csv).

Dorks can contain two variables: `{domain}` (the domain name you would like to restrict searches to), and `{company}` (the company name). If a dork contains `{company}`, but no company name is specified through the `-c` option, it will be skipped.

The CSV contains three columns. 
* *Dork Name* is required and will be the search that the script will run.
* *Description* is optional and will be ignored by the script.
* *Who Added* is optional and will be ignored by the script. This is intended for teams, who might have multiple people adding to a central list.

<p align="right">(<a href="#top">back to top</a>)</p>
