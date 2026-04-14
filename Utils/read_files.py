import csv
import os

def read_config_file(l_config_filename, github_token=''):
    if not l_config_filename:
        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GoogleDorking.config')):
            l_config_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GoogleDorking.config')
        else:
            return "", "", github_token

    l_search_engine_id = ''
    l_key_list = []
    with open(l_config_filename, 'r', encoding='UTF-8') as l_file:
        while config_line := l_file.readline().rstrip():
            if config_line.startswith("github"):
                github_token = config_line
            elif len(config_line) < 20:
                l_search_engine_id = config_line
            else:
                l_key_list.append(config_line)

    return l_search_engine_id, l_key_list, github_token


def format_domain_string(domain):
    if len(domain) == 1:
        return f"site:{domain[0]}", domain[0]


    site_string = f"(site:{domain[0]}"
    for domain_string in domain[1:]:
        site_string +=  f" OR site:{domain_string}"
    site_string += ")"

    intext_string = f"({domain[0]}"
    for domain_string in domain[1:]:
        intext_string += f" OR {domain_string}"
    intext_string += ")"

    return site_string, intext_string

def read_dork_file(dorkfile="", company="", domains=None, verbose_mode=False):
    if domains:
        domain_site_string, domain_intext_string = format_domain_string(domains)
    else:
        domain_site_string, domain_intext_string = "", ""

    if not dorkfile:
        dorkfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ListOfDorks.csv")
    dork_list = []
    with open(dorkfile, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dork_text = (row.get("Dork Name") or row.get("Dork") or "").strip()
            description = (row.get("Description") or row.get(" Description") or "").strip()
            owner = (row.get("Who Added") or row.get(" Who Added") or row.get("Owner") or "").strip()

            if not dork_text:
                continue

            if company:
                dork_text = dork_text.replace("{company}", company)
            elif "{company}" in dork_text:
                continue

            if domains:
                dork_text = dork_text.replace("site:{domain}", domain_site_string)
                dork_text = dork_text.replace("{domain}", domain_intext_string)

            dork_list.append({"Dork": dork_text, "Description": description, "Owner": owner})

    if verbose_mode:
        print(f"Dorks Read From File: {len(dork_list)}")
    return dork_list
