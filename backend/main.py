import requests
import json

# makes the url connection from the server and puts it in the json format (gitConnection is an object)
url = "https://api.github.com/repos/microsoft/pxt-arcade/commits"

# including parameters as the name of the author who made a commit is in a section called sha, and the author name
# is all we want
params = {"q": "sha"}
response = requests.get(url, params)
byteStream=response.content

# if a difference response code is returned then the right connection was not made
if response.status_code == 200:
    data = json.loads(byteStream)
#  print(data)  -this is all the data retreived from out get request

listOfContributors= {}
listOfContributorsWithCount = {}

for item in data:
    commit = item["commit"]["author"]   #commit is the variable name for the line in the data that shows the author's name
    authorName = commit["name"]
    listOfContributors[authorName]=authorName
    listOfContributorsWithCount[authorName]=listOfContributorsWithCount[authorName]+1 if authorName in listOfContributorsWithCount.keys() else 1

print(listOfContributors)
print(listOfContributorsWithCount)