# ---------------#
# MODULE IMPORT #
# ---------------#
import requests
import sys
import csv


# ---------------#
# API Keys       #
# ---------------#

# The -cf option can be used to import the Search Engine ID and API keys. Alternatively, the -se and -ak parameters
#   can be used to import your ID/keys directly from the command line. However, if you want to make your command
#   look prettier for a report, you can add keys directly into the code here. If you are using multiple API keys,
#   they can be appended to the keyList variable.
keyList = []
keyList.append("")
SEARCH_ENGINE_ID = ""  # Your Engine ID. New ID can be generated https://programmablesearchengine.google.com/about/

# ---------------#
# FUNCTIONS      #
# ---------------#

def help_menu():
    print("Title: Google Dork Automation")
    print("Author: Luke Lauterbach - Sentinel Technologies")
    print("")
    print("Usage: python3 [script] [domain to dork]")
    print("")
    print("Optional Options:")
    print("    -d:  Domain to dork")
    print("    -c:  Company name to dork")
    print("    -l:  Filename with list of dorks (defaults to ListOfDorks.csv in current folder)")
    print("    -q:  Quiet Mode (only outputs successful dorks)")
    print("    -v:  Verbose Mode (outputs Google API key alerts)")
    print("    -db: Debug Mode (only runs one dork)")
    print("    -se: Search Engine ID (only needed if API keys aren't in a config file or in the script)")
    print("    -ak: API Key (only needed if API keys aren't in a config file or in the script)")
    print("    -cf: Config File (contains Search Engine ID and API Keys, one per line)")
    print("")
    print("")
    print("The file list of dorks should have one dork per line.")
    print("Dorks can use {domain} or {company} as variables.")
    print("EX: site:{domain} inurl:wp-content/plugins/Ultimate-member")
    print("")
    print("Does not require any dependencies.")
    quit()


def read_config_file(l_config_filename):
    l_search_engine_id = ''
    l_key_list = []
    with open(l_config_filename, 'r', encoding='UTF-8') as l_file:
        i = 0
        while config_line := l_file.readline().rstrip():
            if i == 0:
                l_search_engine_id = config_line
            else:
                l_key_list.append(config_line)
            i += 1

    return l_search_engine_id, l_key_list


# ----------------------#
# GLOBAL VARIABLES     #
# ----------------------#

# Define colors used for console output
class bColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


rowNumber = 0
successCount = 0
companyIndicator = "{company}"

# Arguments
debugMode = False
quietMode = False
verboseMode = False
companyMode = False
domain = ""
outFilename = "NoOutFile"
outFileMode = False
companyName = ""
dorkListFile = "ListOfDorks.csv"

# ---------------#
# EXECUTION     #
# ---------------#

# Assign arguments to variables
for index, argument in enumerate(sys.argv[1:]):
    if argument == "--help" or argument == "-h":
        help_menu()
    elif argument == "-db" or argument == "--debug":
        debugMode = True
    elif argument == "-q" or argument == "--quiet":
        quietMode = True
    elif argument == "-v" or argument == "--verbose":
        verboseMode = True
    elif argument == "-d" or argument == "--domain":
        domain = sys.argv[index + 2]
    elif argument == "-o" or argument == "--out-file":
        outFilename = sys.argv[index + 2]
        outFileMode = True
    elif argument == "-se" or argument == "--search-engine-id":
        SEARCH_ENGINE_ID = sys.argv[index + 2]
    elif argument == "-ak" or argument == "--api-key":
        keyList = [sys.argv[index + 2]]
    elif argument == "-cf" or argument == "--config-file":
        SEARCH_ENGINE_ID, keyList = read_config_file(sys.argv[index + 2])
    elif argument == "-l" or argument == "--list":
        dorkListFile = sys.argv[index + 2]
    elif argument == "-c" or argument == "--company-name":
        companyName = sys.argv[index + 2]
        companyMode = True
    elif sys.argv[index] in {'-ak', '-c', '-cf', '-d', '-l', '-o', '-se', '-v'}:
        pass
    else:
        if not domain:
            domain = argument
        print(sys.argv[index])

# Error condition if no API Key or Search Engine ID has been imported.
if not keyList or not SEARCH_ENGINE_ID:
    print(f"{bColors.FAIL}ERROR - No API keys defined. Read the help documentation for more information.")
    exit()

keyNumber = 0
keyMax = len(keyList)
API_KEY = str(keyList[keyNumber])  # Your API key. New key can be generated at
#                                   https://developers.google.com/custom-search/v1/introduction

# See if there is an existing results CSV, and create one if there isn't.
if outFileMode is True:
    try:
        open(outFilename)
    except:
        open(outFilename, "x")
        with open(outFilename, 'a') as fd:
            fd.write("Dork,Link,Description\n")

# Print Header
print("")
print(f"{bColors.OKCYAN}Running common Google Dorks...{bColors.ENDC}")
print("")

with open(dorkListFile, 'rt') as csvfile:  # Open dork list file
    dorkList = csv.reader(csvfile)
    for row in dorkList:  # Iterate through dorks
        searchSuccess = False
        if rowNumber != 0:  # This is lazy programming. It exists solely to skip the header row of the CSV
            while searchSuccess is False:  # If we exhaust our API key, we need to run the row again with a new API key
                dork = row[0]
                formattedDork = ''

                if companyIndicator in dork and companyMode is False:
                    if debugMode is True:
                        print("Skipping dork because no company name was specified.")
                        searchSuccess = True
                else:
                    if debugMode == True and rowNumber == 2:
                        print("")
                        print(f"{bColors.OKCYAN}Google Dorking complete. {str(rowNumber - 1)} dorks attempted,"
                              f"{str(successCount)} succeeded.")
                        quit()

                    # Manipulate Dork to match Google's syntax
                    dork = dork.format(domain=domain, company=companyName)
                    formattedDork = dork.replace("/", "%2F")
                    formattedDork = formattedDork.replace(":", "%3A")
                    formattedDork = formattedDork.replace("\\", "%5C")
                    formattedDork = formattedDork.replace("|", "%7C")
                    formattedDork = formattedDork.replace(" ", "+")

                    # Run the search query
                    url = (f"https://www.googleapis.com/customsearch/v1?key={API_KEY}"
                           f"&cx={SEARCH_ENGINE_ID}&q={formattedDork}&start={1}")
                    data = requests.get(url).json()
                    search_items = data.get("items")
                    quotaCheck = str(data).find(
                        'Quota exceeded')  # Check to see if the quota has been exceeded. Will return -1 it isn't.

                    if quotaCheck > 1:
                        keyNumber += 1
                        if keyNumber == keyMax:  # If API keys have been exhausted
                            print(f"{bColors.WARNING}Error!  {bColors.ENDC} - All {keyNumber} API keys exhausted. "
                                  f"Wait until tomorrow or create more Google Custom search keys.")
                        else:
                            API_KEY = str(keyList[keyNumber])  # Switch to the next API key.
                            if verboseMode is True:
                                print(f"{bColors.WARNING}Error!  {bColors.ENDC} - Quota exceeded, trying key " + str(
                                    keyNumber))
                    else:
                        if search_items:  # True if there were any results
                            title = search_items[0].get("title")
                            snippet = search_items[0].get("snippet")
                            link = search_items[0].get("link")
                            print(f"{bColors.OKGREEN}Success!{bColors.ENDC}" + " - " + dork.strip("\n") + " - " + link)
                            searchSuccess = True
                            successCount += 1

                            # Write success to file, if an outfile is requested
                            if outFileMode is True:
                                with open(outFilename, 'a') as fd:
                                    fd.write(dork + "," + link + "," + row[
                                        1] + "\n")  # Yes, I should use CSV writer instead of file writer, but I'm lazy.

                        else:  # True if there were no results
                            searchSuccess = True
                            if quietMode is False:
                                print(f"{bColors.FAIL}Failure{bColors.ENDC}" + "  - " + dork.strip("\n"))

        rowNumber += 1  # Keeping track for final output.

print("")
print(f"{bColors.OKCYAN}Google Dorking complete. {rowNumber - 1} dorks attempted, {successCount} succeeded.")
