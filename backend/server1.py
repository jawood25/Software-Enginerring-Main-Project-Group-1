from flask import Flask
import requests
import json

app = Flask(__name__)  # creating instance of the flask app

JSON_COLLAB_ISSUES = "./collabIssues"
JSON_PULL = "./pullRequests"
JSON_ISSUES = "./issues"
JSON_COMMITS = "./commits"
JSON_STANDARD = "./standardMetrics"

# user = input('Please input the user name')
# repo = input('Please input the repo name')
user = 'microsoft'
repo = 'ConnectedServicesSdkSamples'
url = f"https://api.github.com/repos/{user}/{repo}/"

dict_of_pull_requests = {}
dict_of_issues = {}
dict_of_commits = {}
dict_of_collab_issues = {}
dict_of_standard_metrics = {}
sha_list = []

# headers = {"Authorization" : "token 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"}
with open("token", 'r') as f:
    token = f.read()
    print(token)

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
}


def commits(url):
    commits_url = url + "commits?per_page=100&direction=asc&page="
    page = 1
    index = 1
    try:
        response = requests.get(commits_url + str(page), headers=headers)
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
            dict_of_commits[sha_list.index(sha) + 1] = {'author:': author, 'date:': date, 'total_change': total_change,
                                                        'files': file_dict}
    except ValueError as ve:
        print("Invalid JSON returned")
    except requests.RequestException as reqEx:
        print(reqEx)


def pull_requests(url):
    pull_url = url + "pulls?state=all&per_page=100&direction=asc&page="
    page = 1
    index = 1
    try:
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
    except ValueError as ve:
        print("Invalid JSON returned")
    except requests.RequestException as reqEx:
        print(reqEx)


def issues(url):
    issues_url = url + "issues?state=all&per_page=100&direction=asc&page="
    page = 1
    index = 1
    try:
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
    except ValueError as ve:
        print("Invalid JSON returned")
    except requests.RequestException as reqEx:
        print(reqEx)


def collaberatedIssues(url):
    collabIssues = url + "issues?state=all&per_page=100&direction=asc&page="
    page = 1
    collabCount = 0
    try:
        response = requests.get(collabIssues + str(page), headers=headers)
        index = 0
        while response.json():
            data = response.json()
            for item in data:
                issueTitle = item['title']
                personIssuer = item['user']['login']
                personAssigned = item['assignee']
                if personAssigned is not None:
                    personAssigned = personAssigned['login']
                    collabCount += 1
                index += 1  # issue number
                dict_of_collab_issues[index] = {'Title of issue': issueTitle, 'author of issues ': personIssuer,
                                                'Issue collaberate by ': personAssigned}

            page += 1
            response = requests.get(collabIssues + str(page), headers=headers)
        return collabCount
    # print(collabIssues)
    except ValueError as ve:
        print("Invalid JSON returned")
    except requests.RequestException as reqEx:
        print(reqEx)

def standardMetrics(collabFromFunction):
        dict_of_standard_metrics[0] = {"Number of commits: ": len(dict_of_commits),
                                       "Number of pull requests:": len(dict_of_pull_requests)
            , "Number of issues raised": len(dict_of_issues), "Number of collaborated issues": collabFromFunction}


def write():
    with open(f'{JSON_COLLAB_ISSUES}.json', 'w') as file:
        json.dump(dict_of_collab_issues, file, indent=3)

    with open(f'{JSON_PULL}.json', 'w') as file:
        json.dump(dict_of_pull_requests, file, indent=3)

    with open(f'{JSON_ISSUES}.json', 'w') as file:
        json.dump(dict_of_issues, file, indent=3)

    with open(f'{JSON_COMMITS}.json', 'w') as file:
        json.dump(dict_of_commits, file, indent=3)

    with open(f'{JSON_STANDARD}.json', 'w') as file:
        json.dump(dict_of_standard_metrics, file, indent=3)


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
    issues(url)
    collab = collaberatedIssues(url)
    commits(url)
    standardMetrics(collab)
    write()
    # app.run(debug=True)