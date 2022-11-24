import psutil
import logging
import datetime
import threading
import os
import json
import backend.server1

from flask.json import jsonify
from flask import Flask, render_template, request, url_for

from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Bar3D, Line

app = Flask(__name__)


def line_base_issues() -> Line:
    with open(f'{backend.server1.JSON_ISSUES}.json', 'r') as f:
        data = json.loads(f.read())
        create_times = []
        open_issues = []
        amount_open = 0
        closed_issues = []
        amount_closed = 0

        for item in data:
            open_time = data[item]['create_time:']
            if data[item]['state'] == "open":
                amount_open += 1
            create_times.append(open_time)
            open_issues.append(amount_open)
            if data[item]['state'] == "closed":
                amount_closed += 1
            closed_issues.append(amount_closed)

    l = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(create_times)
        .add_yaxis("Currently Open Issues", open_issues,
                   itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
        .add_yaxis("Currently Closed Issues", closed_issues,
                   itemstyle_opts=opts.ItemStyleOpts(color="#FF0000"))

    )
    return l

def line_base_pull_requests() -> Line:
    with open(f'{backend.server1.JSON_PULL}.json', 'r') as f:
        data = json.loads(f.read())
        create_times = []
        open_pull_requests = []
        closed_pull_requests = []
        amount_open = 0
        amount_closed = 0

        for item in data:
            open_time = data[item]['create_time:']
            if data[item]['state'] == "open":
                amount_open += 1
            create_times.append(open_time)
            open_pull_requests.append(amount_open)
            if data[item]['state'] == "closed":
                amount_closed += 1
            closed_pull_requests.append(amount_closed)

    l = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(create_times)
        .add_yaxis("Currently Open Pull Requests", open_pull_requests,
                   itemstyle_opts=opts.ItemStyleOpts(color="#00FF00"))
        .add_yaxis("Currently Closed Pull Requests", closed_pull_requests,
                   itemstyle_opts=opts.ItemStyleOpts(color="#A020F0"))
    )
    return l


def bar_base_commits() -> Bar:
    with open(f'{backend.server1.JSON_COMMITS}.json', 'r') as f:
        data = json.loads(f.read())
        contributors = []
        additions = []
        deletions = []

        for item in data:
            contrib = data[item]['author:']
            adds = data[item]['total_change']['additions']
            deletes = data[item]['total_change']['deletions']
            contributors.append(contrib)
            additions.append(adds)
            deletions.append(-deletes)
    b = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(contributors)
        .add_yaxis("Additions", additions, stack="stack1", category_gap=0,
                   itemstyle_opts=opts.ItemStyleOpts(color="#0e960e"),
                   label_opts=opts.LabelOpts(position="top"))
        .add_yaxis("Deletions", deletions, stack="stack1", category_gap=0,
                   itemstyle_opts=opts.ItemStyleOpts(color="#c41212"),
                   label_opts=opts.LabelOpts(position="bottom"))
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(
                is_show=True,
                range_start=0,
                range_end=20
            )
        )
    )
    return b


@app.route("/contributors")
def get_contributor_stat_data():
    b = bar_base_commits()
    return b.dump_options_with_quotes()


@app.route("/issues")
def get_issues_stat_data():
    l = line_base_issues()
    return l.dump_options_with_quotes()

@app.route("/pullRequests")
def get_pull_requests_stat_data():
    l = line_base_pull_requests()
    return l.dump_options_with_quotes()

@app.route("/")
def main():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()
