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

    # Loop through each workspace
    for workspace in workspaces:
        workspace_slug = workspace['slug']

        # Fetch projects in each workspace
        projects_response = requests.get(
            f"https://api.bitbucket.org/2.0/workspaces/{workspace_slug}/projects",
            auth=(username, app_password)
        )

        if projects_response.status_code == 200:
            projects = projects_response.json()['values']

            # Loop through each project in the workspace
            for project in projects:
                project_name = project['name']
                project_key = project['key']

                # Fetch repositories in each project
                repos_response = requests.get(
                    f"https://api.bitbucket.org/2.0/repositories/{workspace_slug}?q=project.key=\"{project_key}\"",
                    auth=(username, app_password)
                )

                if repos_response.status_code == 200:
                    repositories = repos_response.json()['values']

                    # Loop through each repository in the project
                    for repo in repositories:
                        all_repositories.append({
                            'workspace': workspace_slug,
                            'project': project_name,
                            'repository_name': repo['name']
                        })

    # Sort all repositories by their name, case-insensitively
    sorted_repositories = sorted(all_repositories, key=lambda x: x['repository_name'].lower())

    # Print the header for the table
    print(f"{'Repository':<50}{'Project':<30}{'Workspace':<30}")

    # Print the sorted list of repositories along with their projects and workspaces
    for repo in sorted_repositories:
        print(f"{repo['repository_name']:<70}{repo['project']:<30}{repo['workspace']:<30}")

else:
    print("Failed to fetch workspaces.")
