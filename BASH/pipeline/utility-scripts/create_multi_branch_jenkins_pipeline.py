import requests
import argparse

def create_folder(job_name, username, password, project_repo, project_repo_name, project_jenkins_file):
    
    #https://orchestrator1.orchestrator-v2.sunvalle.net/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV-SuperPipeline/
    url = 'https://orchestrator1.orchestrator-v2.sunvalle.net/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-SuperPipeline/createItem?name=' + str(job_name)
    
    
    config_file = readXML('multi-branch-config.xml').replace("PROJECT_REPO", project_repo).replace("PROJECT_JENKINS_FILE", project_jenkins_file) \
        .replace("PROJECT_NAME", project_repo_name)

    print('Multi branch pipeline url:', url)
    print('Project repo name:', project_repo_name)
    print('Multi branch pipeline xml:', config_file)
    
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(url, auth=(username, password), verify=False, data=config_file, headers=headers)
    code = r.status_code
    response = r.text

    if code == 200:
        print('Create MUltibranch pipeleine: [200]')
        return True
    else:
        print('Create MUltibranch pipeleine: [' + str(code) + ']')
        print(response)
        raise Exception('Failed to create the jenkins job. Result: ' + str(response))
    
    

def add_webhook(github_username, github_password, repo_name, repo_owner="svci"):
    data = {
        "name": "web",
        "events": [
            "push",
            "pull_request"
        ],
        "config": {
            "content_type": "form",
            "insecure_ssl": "0",
            "url": "https://orchestrator1.orchestrator-v2.sunvalle.net/github-webhook/"
        }
    }
    headers = {'Content-Type': 'application/json'}
    url = "https://github.sunvalle.net/api/v3/repos/{repo_owner}/{repo_name}/hooks".format(repo_owner=repo_owner, repo_name=repo_name)
    print("Create webhook url", url)
    r = requests.post(url, auth=(github_username, github_password), verify=False, json=data)
    code = r.status_code
    response = r.text

    if code == 201:
        print('Added webhook: [201]')
        return
    else:
        print('Add webhook: [' + str(code) + ']')
        print(response)
        raise Exception('Failed to add the webhook. Result: ' + str(response))
    

def delete_job(job_name, job_folder_path, username, password):
    folder_path = '/job/'.join(job_folder_path.split('/'))
    url = 'http://d-imjenkins.sunvalle.net:8080/job/' + str(folder_path) + '/job/' + str(job_name) + '/doDelete'

    print('Delete Job:', url)

    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, auth=(username, password), verify=False, headers=headers)
    code = r.status_code
    response = r.text

    if code == 200:
        print('Delete Job: [200]')
        return
    else:
        print('Delete Job: [' + str(code) + ']')
        print(response)
        raise Exception('Failed to delete the job. Result: ' + str(response))

def readXML(file):
    with open(file, 'r') as f:
        data = f.read()
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--job_name', '-j', help='REQUIRED: The name of the job to be created.', type=str, required=True)
    parser.add_argument('--username', '-u', help='REQUIRED: The username associated with the namespace in Jenkins.', type=str, required=True)
    parser.add_argument('--password', '-p', help='REQUIRED: The password associated with the namespace in Jenkins.', type=str, required=True)
    parser.add_argument('--github_username',  help='REQUIRED:Github username.', type=str, required=True)
    parser.add_argument('--github_password',  help='REQUIRED: Github password.', type=str, required=True)
    parser.add_argument('--project_repo', '-r', help='REQUIRED: Project repository.', type=str, required=True)
    parser.add_argument('--project_jenkins_file', '-f', help='REQUIRED: Project Jenkins File.', type=str, required=True)
    parser.add_argument('--delete', '-d', help='OPTIONAL: A flag to indicate whether or not to delete a folder. Defaults to false.', type=bool, required=False, default=False)
    args = parser.parse_args()

    if args.delete:
        delete_job(args.job_name, args.username, args.password)
    else:
        project_repo = args.project_repo.strip().strip("/")
        project_repo_name = project_repo.split("/")[-1].replace(".git", "")
        status = create_folder(args.job_name, args.username, args.password, project_repo, project_repo_name, args.project_jenkins_file)
        if status:
            add_webhook(args.github_username, args.github_password, project_repo_name)
       

if __name__ == '__main__':
    main()
