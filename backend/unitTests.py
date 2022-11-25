from server1 import *
import requests
import unittest
import pytest


def test_dict_of_issues_not_null():
    issues_list = dict_of_issues
    assert issues_list != []


def test_dict_of_commits_not_null():
    commits_list = dict_of_commits
    assert commits_list != []


def test_dict_of_pull_requests_not_null():
    pull_requests_list = dict_of_pull_requests
    assert pull_requests_list != []


def test_dict_of_collab_issues_not_null():
    collab_issues_list = dict_of_collab_issues
    assert collab_issues_list != []

if __name__ == "__main__":
    pytest.main(['./'])

