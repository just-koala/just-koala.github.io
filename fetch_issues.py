import requests
from jinja2 import Template

GITHUB_REPO = 'just-koala/just-koala.github.io'  # Replace 'username' with your GitHub username
GITHUB_TOKEN = 'KOALA_TOKEN'

def fetch_issues(repo):
    url = f'https://api.github.com/repos/{repo}/issues'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_post(issue):
    template = Template(open('template.html').read())
    return template.render(title=issue['title'], content=issue['body'])

def main():
    issues = fetch_issues(GITHUB_REPO)
    for issue in issues:
        with open(f'_posts/{issue["title"].replace(" ", "_")}.html', 'w') as f:
            f.write(generate_post(issue))

if __name__ == '__main__':
    main()
