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

headers = {"Accept": "application/vnd.github+json"}


def pull_request(url):
    pull_url = url + "pulls?state=all&per_page=100&direction=asc&page="
    count = 1
    response = requests.get(pull_url+str(count), headers=headers)
    data = json.loads(response.content)
    for item in data:
        index = item['number']
        user = item['user']['login']
        comment = item['title']
        create_time = item['created_at']
        close_time = item['closed_at']
        dict_of_pull_requests[index] = {'user:': user, 'comment:': comment, 'create_time:': create_time, 'close_time:': close_time}
    #print(dict_of_pull_requests)


def issues(url):
    issues_url = url + "issues?state=all&per_page=100&direction=asc&page="
    count = 1
    response = requests.get(issues_url+str(count), headers=headers)
    data = json.loads(response.content)
    for item in data:
        index = item['number']
        user = item['user']['login']
        title = item['title']
        create_time = item['created_at']
        close_time = item['closed_at']
        dict_of_issues[index] = {'user:': user, 'title:': title, 'create_time:': create_time, 'close_time:': close_time}
    #print(dict_of_issues)


def write():
    with open(f'{JSON_FILE_PATH}.json', 'w') as file:
        json.dump(dict_of_pull_requests, file)
        json.dump(dict_of_issues, file)


@app.route("/PR")
def PR():
    return dict_of_pull_requests


@app.route("/issue")   #this is essentially a web page for just the information about the users and commits
def issue():
    return dict_of_issues


if __name__ == '__main__':
    pull_request(url)
    issues(url)
    write()
    app.run(debug=True)