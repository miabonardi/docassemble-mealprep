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
        username = get_config("oauth github id")
        password = get_config("oauth github secret")

        auth = Auth.Login(username, password)
        self = Github(auth=auth)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

