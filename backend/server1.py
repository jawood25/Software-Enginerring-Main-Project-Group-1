from flask import Flask
import requests
import json

app = Flask(__name__)  # creating instance of the flask app

JSON_FILE_PATH = "./myData"
#user = input('Please input the user name')
#repo = input('Please input the repo name')
user = 'microsoft'
repo = 'Docker-Provider'
url = f"https://api.github.com/repos/{user}/{repo}/"

dict_of_pull_requests = {}
dict_of_issues = {}
dict_of_commits = {}
sha_list = []

headers = {"Authorization" : "Token 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", "Accept": "application/vnd.github+json"}


def commits(url):
    commits_url = url + "commits?per_page=100&direction=asc&page="
    page = 1
    index = 1
    response = requests.get(commits_url+str(page), headers=headers)
    while response.json():
        data = json.loads(response.content)
        for item in data:
            sha = item['sha']
            sha_list.append(sha)
            index += 1
        page += 1
        response = requests.get(commits_url + str(page), headers=headers)
    
    for sha in sha_list:
        commit_url = url + 'commits/' + sha
        response = requests.get(commit_url, headers=headers)
        data = json.loads(response.content)
        author = data['commit']['author']['name']
        date = data['commit']['author']['date']
        total_change = data['stats']
        if 'files' in data:
            file_dict = {}
            for file in data['files']:
                filename = file['filename'].split('/')[-1]
                additions = file['additions']
                deletions = file['deletions']
                file_dict[filename] = {'additions': additions, 'deletions': deletions}
        dict_of_commits[sha_list.index(sha)+1] = {'author:': author, 'date:': date, 'total_change': total_change,  'files': file_dict}
    #print(dict_of_commits)
    


def pull_requests(url):
    pull_url = url + "pulls?state=all&per_page=100&direction=asc&page="
    page = 1
    index = 1
    response = requests.get(pull_url + str(page), headers=headers)
    while response.json():
        data = response.json()
        for item in data:
            user = item['user']['login']
            comment = item['title']
            state = item['state']
            create_time = item['created_at']
            close_time = item['closed_at']
            dict_of_pull_requests[index] = {'user:': user, 'comment:': comment, 'state': state,
                                            'create_time:': create_time, 'close_time:': close_time}
            index += 1
        page += 1
        response = requests.get(pull_url + str(page), headers=headers)
    #print(dict_of_pull_requests)


def issues(url):
    issues_url = url + "issues?state=all&per_page=100&direction=asc&page="
    page = 1
    index = 1
    response = requests.get(issues_url + str(page), headers=headers)
    while response.json():
        data = response.json()
        for item in data:
            if 'pull_request' not in item:
                user = item['user']['login']
                title = item['title']
                state = item['state']
                create_time = item['created_at']
                close_time = item['closed_at']
                dict_of_issues[index] = {'user:': user, 'title:': title, 'state': state,
                                         'create_time:': create_time, 'close_time:': close_time}
                index += 1
        page += 1
        response = requests.get(issues_url + str(page), headers=headers)
    #print(dict_of_issues)


def write():
    with open(f'{JSON_FILE_PATH}.json', 'w') as file:
        json.dump(dict_of_pull_requests, file)
        json.dump(dict_of_issues, file)


@app.route("/commit")
def commit():
    return dict_of_commits


@app.route("/PR")
def PR():
    return dict_of_pull_requests


@app.route("/issue")
def issue():
    return dict_of_issues


if __name__ == '__main__':
    pull_requests(url)
    #issues(url)
    #commits(url)
    write()
    #app.run(debug=True)