import os
import requests
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get('BITBUCKET_USERNAME')
app_password = os.environ.get('BITBUCKET_PASSWORD')
auth = (username, app_password)

def fetch_all_pages(url, auth):
    items = []
    while url:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            data = response.json()
            items.extend(data['values'])
            url = data.get('next', None)
        else:
            print(f"Failed to fetch data from {url}")
            break
    return items

workspaces = fetch_all_pages("https://api.bitbucket.org/2.0/workspaces", auth)
all_repositories = []
all_repo_list = []

for workspace in workspaces:
    workspace_slug = workspace['slug']
    projects = fetch_all_pages(f"https://api.bitbucket.org/2.0/workspaces/{workspace_slug}/projects", auth)

    for project in projects:
        project_name = project['name']
        project_key = project['key']

        repositories = fetch_all_pages(
            f"https://api.bitbucket.org/2.0/repositories/{workspace_slug}?q=project.key=\"{project_key}\"", auth
        )

        for repo in repositories:
            all_repositories.append({
                'workspace': workspace_slug,
                'project': project_name,
                'repository_name': repo['name']
            })
            all_repo_list.append(repo['name'])

sorted_repositories = sorted(all_repositories, key=lambda x: x['repository_name'].lower())
sorted_repo_list = sorted(all_repo_list, key=str.casefold)

print("==============================================================================")
print(f"{'Repository':<50}{'Project':<30}{'Workspace':<30}")

for repo in sorted_repositories:
    print(f"{repo['repository_name']:<50}{repo['project']:<30}{repo['workspace']:<30}")
print("==============================================================================")

for repo in sorted_repo_list:
    print(repo)