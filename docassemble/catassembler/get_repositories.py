from github import Github, Auth
from docassemble.base.util import get_config, DARedis, log

r = DARedis()

def fetch_bellingcat_repos():
    repos = []

    fetched_repos = r.get_data("bellingcat_repos")

    if fetched_repos is not None and len(fetched_repos) > 0:
        log("Using cached repos", priority="console")
        return fetched_repos

    with GithubClient() as gh:
        log("Fetching repos from Github", priority="console")
        for repo in gh.get_organization(login="bellingcat").get_repos():
            tags = repo.get_topics()
            if "python" and "command-line" in tags and "gui" not in tags: # grab all python clis excluding ones with gui
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

    r.set_data("bellingcat_repos", repos)

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

