import os
import requests
from jinja2 import Template

# Configuration
GITHUB_REPO = "just-koala/just-koala.github.io" 
GITHUB_TOKEN = os.getenv("KOALA_TOKEN")

# Fetch issues from GitHub
def fetch_issues(repo):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Generate posts from issues
def generate_post(issue):
    with open("template.html") as template_file:
        template = Template(template_file.read())

    title = issue["title"]
    body = issue["body"]

    return template.render(title=title, content=body)

# Main function
def main():
    issues = fetch_issues(GITHUB_REPO)
    
    if not os.path.exists("posts"):
        os.makedirs("posts")

    for issue in issues:
        for label in issue.get("labels", []):
            if label["name"] == "blog":
                filename = f"posts/{issue['title'].replace(' ', '_')}.html"
                with open(filename, "w") as post_file:
                    post_file.write(generate_post(issue))

if __name__ == "__main__":
    main()
