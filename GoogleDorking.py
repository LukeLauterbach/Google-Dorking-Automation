#---------------#
# MODULE IMPORT #
#---------------#
import requests
import sys
import csv

#---------------#
# FUNCTIONS     #
#---------------#

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
    print("")
    print("")
    print("The file list of dorks should have one dork per line.")
    print("Dorks can use {domain} or {company} as variables.")
    print("EX: site:{domain} inurl:wp-content/plugins/Ultimate-member")
    print("")
    print("Does not require any dependencies.")
    quit()

#----------------------#
# GLOBAL VARIABLES     #
#----------------------#

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

# API Keys
keyList = ["INSERT_KEY_HERE", "INSERT_ADDITIONAL_KEY_HERE"]
SEARCH_ENGINE_ID = "INSERT_ID_HERE" # Your Engine ID. New ID can be generated https://programmablesearchengine.google.com/about/
keyNumber = 0
keyMax = len(keyList)
API_KEY = str(keyList[keyNumber]) # Your API key. New key can be generated at https://developers.google.com/custom-search/v1/introduction

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

#---------------#
# EXECUTION     #
#---------------#

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
        domain = sys.argv[index+2]
    elif argument == "-o" or argument == "--out-file":
        outFilename = sys.argv[index+2]
        outFileMode = True
    elif argument == "-l" or argument == "--list":
        dorkListFile = sys.argv[index+2]
    elif argument == "-c" or argument == "--company-name":
        companyName = sys.argv[index+2]
        companyMode = True
    elif sys.argv[index] == "-d" or sys.argv[index] == "-c":
        pass
    else:
        domain = argument

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

with open(dorkListFile, 'rt') as csvfile: # Open dork list file
    dorkList = csv.reader(csvfile)
    for row in dorkList: # Iterate through dorks
        searchSuccess = False
        if rowNumber != 0: # This is lazy programming. It exists solely to skip the header row of the CSV
            while searchSuccess is False: # If we exhaust our API key, we need to run the row again with a new API key
                dork = row[0]
                formattedDork = ''

                if companyIndicator in dork and companyMode is False:
                    if debugMode is True:
                        print("Skipping dork because no company name was specified.")
                        searchSuccess = True
                else:
                    if debugMode == True and rowNumber == 2:
                        print("")
                        print(f"{bColors.OKCYAN}Google Dorking complete. " + str(rowNumber-1) + " dorks attempted, " + str(successCount) + " succeeded.")
                        quit()

                    # Manipulate Dork to match Google's syntax
                    dork = dork.format(domain=domain, company=companyName)
                    formattedDork = dork.replace("/", "%2F")
                    formattedDork = formattedDork.replace(":", "%3A")
                    formattedDork = formattedDork.replace("\\", "%5C")
                    formattedDork = formattedDork.replace("|", "%7C")
                    formattedDork = formattedDork.replace(" ", "+")

                    # Run the search query
                    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={formattedDork}&start={1}"
                    data = requests.get(url).json()
                    search_items = data.get("items")
                    quotaCheck = str(data).find('Quota exceeded') # Check to see if we exceeded the quota. Will return -1 if we didn't.

                    if quotaCheck > 1:
                        keyNumber += 1
                        if keyNumber == keyMax: # We currently have 20 API keys. Will trigger if more than 2000 searches are run in a day.
                            print(f"{bColors.WARNING}Error!  {bColors.ENDC} - All " + str(keyNumber) + " API keys exhausted. Wait until tomorrow or create more Google Custom search keys.")
                        else:
                            API_KEY = str(keyList[keyNumber]) # Switch to the next API key.
                            if verboseMode is True:
                                print(f"{bColors.WARNING}Error!  {bColors.ENDC} - Quota exceeded, trying key " + str(keyNumber))
                    else:
                        if search_items: # True if there were any results
                            title = search_items[0].get("title")
                            snippet = search_items[0].get("snippet")
                            link = search_items[0].get("link")
                            print(f"{bColors.OKGREEN}Success!{bColors.ENDC}" + " - " + dork.strip("\n") + " - " + link)
                            searchSuccess = True
                            successCount += 1

                            # Write success to file, if an outfile is requested
                            if outFileMode is True:
                                with open(outFilename, 'a') as fd:
                                    fd.write(dork + "," + link + "," + row[1]+ "\n") # Yes, I should use CSV writer instead of file writer, but I'm lazy.

                        else: # True if there were no results
                            searchSuccess = True
                            if quietMode is False:
                                print(f"{bColors.FAIL}Failure{bColors.ENDC}" + "  - " + dork.strip("\n"))

        rowNumber += 1 # Keeping track for final output.

print ("")
print(f"{bColors.OKCYAN}Google Dorking complete. " + str(rowNumber-1) + " dorks attempted, " + str(successCount) + " succeeded.")
