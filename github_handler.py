import os
import dotenv
from github import Github, GithubIntegration

dotenv.load_dotenv()
app_id = os.getenv("github-app-id")  # is this really necessary to be in .env?

# Read the bot certificate
with open(
        os.path.normpath(os.path.expanduser('~/.certs/github/ol-karma-bot.pem')),
        'r'
) as cert_file:
    app_key = cert_file.read()

# Create a GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)


def get_token():
    return Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation("nimadebi", "karma-bot").id
        ).token
    )


def get_issues():
    git_connection = get_token()

    repo = git_connection.get_repo("nimadebi/karma-bot")
    for i in repo.get_issues():
        print(i.body)
    return repo.get_issues()


def get_identities():
    git_connection = get_token()

    repo = git_connection.get_repo("nimadebi/karma-bot")
    readme = repo.get_contents("data/contributors_test.json")  # change this location after testing phase
    return readme

