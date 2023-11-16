from github import Github, Auth
from docassemble.base.util import get_config

fetched_repos = [] # basic in-memory cache so we don't have to fetch repos every time

def fetch_bellingcat_repos():
    repos = []

    global fetched_repos

    if len(fetched_repos) > 0:
        return fetched_repos

    with GithubClient() as gh:
        for repo in gh.get_organization(login="bellingcat").get_repos():
            if "python" and "command-line" in repo.get_topics():
                data = {
                    "name": repo.name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "license": repo.get_license().license.name,
                    "stars": repo.stargazers_count,
                    "readme": repo.get_readme().decoded_content.decode("utf-8"),
                    "archive_url": repo.get_archive_link("zipball")
                }
                repos.append(data)

    fetched_repos = repos

    return repos


class GithubClient(Github):
    def __enter__(self):
        username = get_config("oauth", {}).get("github", {}).get("id")
        password = get_config("oauth", {}).get("github", {}).get("secret")

        if username is None or password is None:
            raise Exception("Missing Github OAuth credentials")

        auth = Auth.Login(username, password)
        self = Github(auth=auth)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

