# ---------------#
# MODULE IMPORT #
# ---------------#
import requests
import os
from Utils.arguments import parse_arguments
from Utils.read_files import read_config_file, read_dork_file
from Utils.github import github
from Utils.utils import print_beginning
import sys
from rich.console import Console
from rich.panel import Panel


# ---------------#
# GLOBAL VARS    #
# ---------------#

VERSION = "2.0"
GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')  # Get the GitHub API key from the environment variable
SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
GOOGLE_API_KEYS = os.getenv('GOOGLE_API_KEYS')


# ---------------#
# FUNCTIONS      #
# ---------------#


def format_dork(unformatted_dork):
    formatted_dork = unformatted_dork.replace("/", "%2F")
    formatted_dork = formatted_dork.replace(":", "%3A")
    formatted_dork = formatted_dork.replace("\\", "%5C")
    formatted_dork = formatted_dork.replace("|", "%7C")
    formatted_dork = formatted_dork.replace(" ", "+")

    return formatted_dork


def main(company="", domain=None, debug_mode=False, dork_file="", quiet_mode=False, verbose_mode=False,
         search_engine_id="", api_keys="", config_file="", github_token=""):
    if not company and not domain:
        (company, domain, debug_mode, list_of_dorks, quiet_mode, verbose_mode,
         search_engine_id, api_keys, config_file, github_token) = parse_arguments()

    print_beginning(VERSION)
    console = Console()

    valid_results = 0
    # If no API keys or config file specified, see if there's a config file in the local directory. Else error.
    if not api_keys or not search_engine_id:
        search_engine_id, api_keys, github_token = read_config_file(config_file, github_token)
    if not api_keys and GOOGLE_API_KEYS:
        api_keys = GOOGLE_API_KEYS.split(",")
    if not search_engine_id:
        search_engine_id = SEARCH_ENGINE_ID
    if not github_token:
        github_token = GITHUB_API_KEY

    if not api_keys or not search_engine_id:
        console.print(
            Panel(
                f"[bold red]No API keys or search engine ID found. Please specify them in the config file or as arguments.[/]",
                title="Error",
                border_style="red"
            )
        )
        sys.exit(1)

    list_of_dorks = read_dork_file(dork_file, company, domain, verbose_mode)  # Read list of Dorks in

    github(github_token, company, domain, quiet_mode)

    for unformatted_dork in list_of_dorks:  # Iterate through dorks
        search_complete = False

        for api_key in api_keys[:]:
            if verbose_mode and not company and "{company}" in unformatted_dork['Dork']:
                print("Skipping dork because no company name was specified.")

            formatted_dork = format_dork(unformatted_dork['Dork'])

            # Run the search query
            url = (f"https://www.googleapis.com/customsearch/v1?key={api_key}"
                   f"&cx={search_engine_id}&q={formatted_dork}&start={1}")
            data = requests.get(url).json()
            search_items = data.get("items")
            # Check to see if the quota has been exceeded. Will return -1 it isn't.
            if str(data).find('Quota exceeded') > 0:
                if verbose_mode:
                    print(f"API Key Exhausted: {api_key}")
                continue

            if search_items:  # True if there were any results
                link = search_items[0].get("link")
                console.print(f"[bold green]Success![/] - {unformatted_dork['Dork']}")
                valid_results += 1
            else:
                if quiet_mode is False:
                    console.print(f"Failure - {unformatted_dork['Dork']}")

            if debug_mode:
                sys.exit()
            else:
                search_complete = True
                break

        if not search_complete:
            console.print(
                f"[red]Error![/] - All {len(api_keys)} API keys exhausted. "
                f"Wait until tomorrow or create more Google Custom search keys."
            )
            break

    console.print(
        f"\n[cyan]Google Dorking complete. {len(list_of_dorks)} dorks attempted, "
        f"{valid_results} succeeded.[/]"
    )


# ---------------#
# MAIN           #
# ---------------#

if __name__ == "__main__":
    main()
