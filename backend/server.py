from flask import Flask
import requests
import json

app = Flask(__name__)  # creating instance of the flask app

JSON_FILE_PATH = "./myData"

# makes the url connection from the server and puts it in the json format (gitConnection is an object)
url = "https://api.github.com/repos/microsoft/pxt-arcade/commits"

# including parameters as the name of the author who made a commit is in a section called sha, and the author name
# is all we want
params = {"q": "sha"}
response = requests.get(url, params)
byteStream = response.content

# if a difference response code is returned then the right connection was not made
if response.status_code == 200:
    data = json.loads(byteStream)
#  print(data)  -this is all the data retreived from out get request

listOfContributors = {}
listOfContributorsWithCount = {}
listOfActionsPerCommit={}
listOfCommitID=[]


for item in data:
    ## creates list of ID's for each commit made
    commitHeader=item["sha"]
    listOfCommitID.append(commitHeader)
    commiter = item["commit"]["author"]  # commit is the variable name for the line in the data that shows the author's name
    authorName = commiter["name"]
    listOfContributors[authorName] = authorName
    listOfContributorsWithCount[authorName] = listOfContributorsWithCount[
                                                  authorName] + 1 if authorName in listOfContributorsWithCount.keys() else 1

for commitMade in listOfCommitID:
    newURL = url +'/'+ commitMade
    response= requests.get(newURL)
    data2 = json.loads(response.content)
    nameOfCommitter = data2['commit']['author']
    nameCommiter=nameOfCommitter['name']
    totalChanges=data2["stats"]["total"]
    totalAdditions=data2["stats"]["additions"]
    totalDeletions=data2["stats"]["deletions"]
    listOfActionsPerCommit[nameCommiter]= totalChanges + totalAdditions + totalDeletions


print(listOfCommitID)
#print(listOfActionsPerCommit)
print(listOfContributors)
print(listOfContributorsWithCount)
with open(f'{JSON_FILE_PATH}.json', 'w') as f:
    json.dump(listOfContributorsWithCount, f)

# Users api router
@app.route("/contributors")   #this is essentially a web page for just the information about the users and commits
def contributors():
    return listOfContributorsWithCount


if __name__ == "__main__":      #setup information for the flask app
    app.run(debug=True)