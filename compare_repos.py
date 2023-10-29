def read_repositories_from_file(filename):
    with open(filename, 'r') as file:
        # Read each line, strip leading/trailing whitespaces, normalize names, and filter out empty lines
        return [normalize_repo_name(line.strip()) for line in file.readlines() if line.strip()]


def normalize_repo_name(repo_name):
    if repo_name.endswith('.git'):
        return repo_name[:-4]
    return repo_name
def find_differences(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    only_in_set1 = set1 - set2
    only_in_set2 = set2 - set1

    return only_in_set1, only_in_set2


if __name__ == "__main__":
    # Read repositories from files
    github_repos = read_repositories_from_file('github_repos.txt')
    bitbucket_repos = read_repositories_from_file('bitbucket_repos.txt')

    # Find differences
    github_only, bitbucket_only = find_differences(github_repos, bitbucket_repos)

    # Display the results
    if github_only:
        print("Repositories only on GitHub:")
        for repo in github_only:
            print(repo)

    if bitbucket_only:
        print("\nRepositories only on Bitbucket:")
        for repo in bitbucket_only:
            print(repo)
