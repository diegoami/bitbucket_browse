import requests
import os
# Constants
BASE_URL = "https://api.github.com"

from dotenv import load_dotenv

load_dotenv()


USERNAME = os.environ.get('GITHUB_USERNAME')
TOKEN = os.environ.get('GITHUB_TOKEN')

def get_all_repositories(username, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    all_repos = []
    page = 1

    while True:
        # Endpoint to fetch the repositories of the given user with pagination
        url = f"{BASE_URL}/users/{username}/repos?page={page}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            repos = response.json()
            if not repos:  # No more repositories to fetch
                break
            all_repos.extend([repo['name'] for repo in repos])
            page += 1
        else:
            print(f"Error {response.status_code}: {response.text}")
            break

    return all_repos



if __name__ == "__main__":
    repos = get_all_repositories(USERNAME, TOKEN)
    if repos:
        print("Repositories List:")
        for repo in repos:
            print(repo)

