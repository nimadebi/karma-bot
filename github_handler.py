import os
import json
from dotenv import load_dotenv
from github import Github, GithubIntegration

load_dotenv()
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
    return readme.decoded_content.decode()


def is_in_identities(discord_id):
    """
    Checks if the discord id is in the list of contributors. These are added by the whitelist command.
    :param discord_id: discord id of user. Using this over name because of name changes.
    :return: True if in list, False if not.
    """
    identities = json.loads(get_identities())
    for i in identities:
        if i["details"]["discordId"] == discord_id:
            return True
    return False


def push_identities(identities):
    git_connection = get_token()
    repo = git_connection.get_repo("nimadebi/karma-bot")
    readme = repo.get_contents("data/contributors_test.json")  # change this location after testing phase
    repo.update_file(readme.path, "updated identity", json.dumps(identities, indent=2), readme.sha)

def add_identity(account, type, discord_id, discord_name, github_id, twitter_id):
    """
    Adds a new identity to the json file and pushes it to github.
    :param account: 0L address
    :param type: type of identity:
        0 = contributor: optional fields = 'githubId', 'twitterId', 'discordId', 'discordName', ...
        1 = team: optional fields = 'name', 'description', 'members', ... (not yet implemented)
    :param discord_id: discord id.
    :param discord_name: current discord name
    :param github_id: github username
    :param twitter_id: twitter username
    """
    identities = json.loads(get_identities())

    details = {}
    if discord_id is not None:
        details["discordId"] = discord_id
    if discord_name is not None:
        details["discordName"] = discord_name
    if twitter_id is not None:
        details["twitterId"] = twitter_id
    if github_id is not None:
        details["githubId"] = github_id

    # TODO: add more details for team type.

    new_identity = {"account": account,
                    "type": type,
                    "details": details
                    }

    identities.append(new_identity)
    push_identities(identities)

