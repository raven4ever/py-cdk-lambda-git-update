import json
import logging as log

from github import Github

GITHUB_TOKEN = ''
REPO_NAME = 'py-cdk-lambda-git-update'
TARGET_BRANCH_NAME = 'programatic_branch'
FILE_TO_UPDATE = 'to_update.json'


def lambda_handler(event, context):
    data_update = event['data']

    log.basicConfig(level=log.INFO)

    g = Github(GITHUB_TOKEN)

    log.info(f'Getting the {REPO_NAME} repository...')
    repo = g.get_user().get_repo(REPO_NAME)

    log.info(f'Creating the {TARGET_BRANCH_NAME} branch...')
    sb = repo.get_branch(repo.default_branch)
    repo.create_git_ref(ref='refs/heads/' + TARGET_BRANCH_NAME, sha=sb.commit.sha)

    log.info(f'Updating the {FILE_TO_UPDATE} file...')
    contents = repo.get_contents(FILE_TO_UPDATE, ref=TARGET_BRANCH_NAME)
    json_content = json.loads(contents.decoded_content)
    blocklist = json_content['blocklist']
    blocklist.extend(data_update)
    json_content['blocklist'] = blocklist
    repo.update_file(contents.path, "le update", json.dumps(json_content, indent=3, sort_keys=True),
                     contents.sha, branch=TARGET_BRANCH_NAME)

    log.info(f'Creating PR from {TARGET_BRANCH_NAME} to {repo.default_branch}...')
    pr = repo.create_pull(title='updated file', body='', head=TARGET_BRANCH_NAME, base=str(repo.default_branch))

    log.info(f'PR URL is: {pr.html_url}')

    return {
        "pr_url": pr.html_url
    }
