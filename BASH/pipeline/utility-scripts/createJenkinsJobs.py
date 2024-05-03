import requests
import json
import argparse

def create_jobs(api_url, api_token, project_name, branch, git_url):
    updated_branch = '-'.join(branch.split('/'))
    obj = {
        'action': 'create',
        'branch': branch,
        'jobName': project_name,
        'folderName': project_name + '-' + updated_branch,
        'person': 'BOT',
        'lanid': 'BOT',
        'path': 'NA',
        'url': git_url,
        'sshURL': git_url
    }

    r = requests.post(api_url, data=json.dumps(obj), headers={ 'Content-Type': 'application/json', 'X-Webhook-Token': str(api_token) }, verify=False)
    code = r.status_code
    response = r.text

    if code == 200:
        print('Create Job: [200] for branch [' + branch + '].')
    else:
        print('Create Job: [' + str(code) + '] for branch [' + branch + '].')
        print('Response:', response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_url', '-a', help='REQUIRED: The url for the API which creates the Jenkins jobs.', type=str, required=True)
    parser.add_argument('--api_token', '-t', help='REQUIRED: The token required to access the API.', type=str, required=True)
    parser.add_argument('--project_name', '-p', help='REQUIRED: The name of the git repo being associated with the Jenkins jobs.', type=str, required=True)
    parser.add_argument('--branch', '-b', help='REQUIRED: The branch to use with the Jenkins jobs.', type=str, required=True)
    parser.add_argument('--git_url', '-g', help='REQUIRED: The url of the git repo to link with the Jenkins jobs.', type=str, required=True)
    args = parser.parse_args()

    create_jobs(args.api_url, args.api_token, args.project_name, args.branch, args.git_url)
