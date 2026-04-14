import requests
from time import sleep
from rich.console import Console

def github_search(github_token, url, query, per_page=30, page=1):
    # Search parameters
    params = {
        'q': f'"{query} -user:cirosantilli"',
        'per_page': per_page,
        'page': page
    }
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the request to GitHub API
    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 and "rate limit" in response.text:
            sleep(60)
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None



def print_github_results(results):
    if not results:
        print(f"No results found from GitHub.")

    for item in results['items']:
        try:
            email = item['author']['email']
        except TypeError:
            email = item['commit']['author']['email']
        except KeyError:
            email = item['commit']['author']['email']

        message = item['commit']['message'].split('\n')[0]

        try:
            print(f"{email} - {message} - {item['html_url']}")
        except KeyError as e:
            print("-------------------------------------")
            print(e)
            for key, value in item.items():
                print(f"{key}: {value}")
            print("-------------------------------------")
        #repo_name = item['repository']['full_name']
        #file_name = item['name']
        #file_url = item['html_url']
        #print(f"Repository: {repo_name}")
        #print(f"File: {file_name}")
        #print(f"URL: {file_url}")
    #    print(item)
    #    print("-" * 50)


def github(github_token, company, domain, silent_mode=False):
    if not github_token:
        return
    if not silent_mode:
        Console().print("\nSearching GitHub...", style="cyan")

    code_search_url = 'https://api.github.com/search/code'
    commits_search_url = 'https://api.github.com/search/commits'

    if company:
        company_code_results = github_search(github_token, code_search_url, company)['total_count']
        if company_code_results:
            print(f"{company_code_results} code results for {company}: "
                  f"https://github.com/search?q=%22{company.replace(' ', '+')}%22&type=code")
    if domain:
        domain_code_results = github_search(github_token, code_search_url, domain)['total_count']
        if domain_code_results:
            print(f"{domain_code_results} code results for {domain}: https://github.com/search?q=%22{domain}%22&type=code")
    if company:
        company_commit_results = github_search(github_token, commits_search_url, company)['total_count']
        if company_commit_results:
            print(f"{company_commit_results} code results for {company}: "
                  f"https://github.com/search?q=%22{company.replace(' ', '+')}%22&type=commits")
    if domain:
        domain_commit_results = github_search(github_token, commits_search_url, domain)['total_count']
        if domain_commit_results:
            print(f"{domain_commit_results} code results for {domain}: "
                  f"https://github.com/search?q=%22{domain}%22&type=commits")