import argparse
from argparse import RawTextHelpFormatter

def parse_arguments():
    parser = argparse.ArgumentParser(description="Title: Google Dork Automation\n "
                                                 "Author: Luke Lauterbach - Sentinel Technologies",
                                     epilog="The file list of dorks should have one dork per line. Dorks can use "
                                            "{domain} or {company} as variables.\n"
                                            "EX: site:{domain} inurl:wp-content/plugins/Ultimate-member\n\n"
                                            "Does not require any dependencies.",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", "--company", type=str, help="Company name to dork")
    parser.add_argument("-d", "--domains", type=str, help="Domain to dork (comma separated if multiple)")
    parser.add_argument("-db", "--debug", action="store_true", default=False, help="Debug mode")
    parser.add_argument("-l", "--list-of-dorks", type=str, help="Filename with list of dorks")
    parser.add_argument("-q", "--quiet", action="store_true", default=False,
                        help="Quiet Mode (only output successful dorks")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Verbose Mode")
    parser.add_argument("-g", "--github-api-key", default='')
    parser.add_argument("-se", "--search-engine-id", type=str, help="Search Engine ID (only needed if API "
                                                                    "keys aren't in a config file or in the script)")
    parser.add_argument("-ak", "--api-key", type=str, help="API Key (only needed if API keys aren't in a "
                                                           "config file or in the script)")
    parser.add_argument("-cf", "--config-file", type=str, help="Config File (contains Search Engine ID and"
                                                               " API Keys, one per line)")

    args = parser.parse_args()

    args.domains = args.domains.split(",")

    return (args.company, args.domains, args.debug, args.list_of_dorks, args.quiet, args.verbose, args.search_engine_id,
            args.api_key, args.config_file, args.github_api_key)