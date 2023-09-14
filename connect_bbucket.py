import os
import requests
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get('BITBUCKET_USERNAME')
app_password = os.environ.get('BITBUCKET_PASSWORD')

# Fetch all workspaces the user has access to
workspaces_response = requests.get(
    "https://api.bitbucket.org/2.0/workspaces",
    auth=(username, app_password)
)

if workspaces_response.status_code == 200:
    workspaces = workspaces_response.json()['values']

    all_repositories = []

    # Loop through each workspace and list its repositories
    for workspace in workspaces:
        workspace_slug = workspace['slug']

        repos_response = requests.get(
            f"https://api.bitbucket.org/2.0/repositories/{workspace_slug}",
            auth=(username, app_password)
        )

        if repos_response.status_code == 200:
            repositories = repos_response.json()['values']

            for repo in repositories:
                all_repositories.append({
                    'workspace': workspace_slug,
                    'repository_name': repo['name']
                })
        else:
            print(f"Failed to fetch repositories for workspace {workspace_slug}")

    # Sort all repositories by their name, case-insensitively
    sorted_repositories = sorted(all_repositories, key=lambda x: x['repository_name'].lower())

    # Print the header for the table
    print(f"{'Repository':<50}{'Workspace':<30}")

    # Print the sorted list of repositories along with their workspaces in tabular format
    for repo in sorted_repositories:
        print(f"{repo['repository_name']:<60}{repo['workspace']:<30}")

else:
    print("Failed to fetch workspaces.")
