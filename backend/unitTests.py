from server1 import *
import requests
import unittest
import pytest

def dict_of_issues_not_null():
     issues_array = issues(url)
     assert issues_array != 0

def dict_of_commits_not_null():
     commits_array = commits(url)
     assert commits_array != 0

def dict_of_pull_requests_not_null():
     pull_requests_array = pull_requests(url)
     assert pull_requests_array != 0

def dict_of_collab_issues_not_null():
     collab_issues_array = collaberatedIssues(url)
     assert collab_issues_array != 0