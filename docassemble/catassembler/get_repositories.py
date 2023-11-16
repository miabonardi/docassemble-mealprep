from github import Github, Auth
from docassemble.base.util import get_config

def fetch_bellingcat_repos():
    repos = []

    with GithubClient() as gh:
        for repo in gh.get_organization(login="bellingcat").get_repos():
            if "python" and "command-line" in repo.get_topics():
                repos.append(repo)

    print(repos)
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

