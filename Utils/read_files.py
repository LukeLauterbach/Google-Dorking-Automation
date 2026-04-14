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
        return f"site:{domain[0]}", f'"{domain[0]}"'


    site_string = f"(site:{domain[0]}"
    for domain_string in domain[1:]:
        site_string +=  f" OR site:{domain_string}"
    site_string += ")"

    intext_string = f'("{domain[0]}"'
    for domain_string in domain[1:]:
        intext_string += f' OR "{domain_string}"'
    intext_string += ')'

    return site_string, intext_string

def read_dork_file(dorkfile="", company="", domains=None, verbose_mode=False):
    domain_site_string, domain_intext_string = format_domain_string(domains)

    if not dorkfile:
        dorkfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ListOfDorks.csv")
    dork_list = []
    with open(dorkfile, 'r') as file:
        next(file)  # Skip the header row
        for line in file:
            line = line.rstrip()
            line = line.split(",")
            if company:
                line[0] = line[0].replace("{company}", company)
            elif "{company}" in line[0]:
                continue
            if domains:
                line[0] = line[0].replace("site:{domain}", domain_site_string)
                line[0] = line[0].replace("{domain}", domain_intext_string)
            dork_list.append({'Dork': line[0], 'Description': line[1], 'Owner': line[2]})

    if verbose_mode:
        print(f"Dorks Read From File: {len(dork_list)}")
    return dork_list
