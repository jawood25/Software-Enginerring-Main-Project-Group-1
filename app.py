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
        previous_time = ""

        for item in data:
            open_time = data[item]['create_time:'][0:10]
            if open_time != previous_time:
                previous_time = open_time
                if data[item]['state'] == "open":
                    amount_open += 1

                if data[item]['state'] == "closed":
                    amount_closed += 1

                open_issues.append(amount_open)
                closed_issues.append(amount_closed)
                create_times.append(open_time)

    l = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(create_times)
        .add_yaxis("Currently Open Issues", open_issues, is_smooth=True,
                   itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
        .add_yaxis("Currently Closed Issues", closed_issues, is_smooth=True,
                   itemstyle_opts=opts.ItemStyleOpts(color="#FF0000"))
        .set_global_opts(title_opts=opts.TitleOpts(title="Issues"))
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
        previous_time = ""

        for item in data:
            open_time = data[item]['create_time:'][0:10]
            if open_time != previous_time:
                previous_time = open_time
                if data[item]['state'] == "open":
                    amount_open += 1

                if data[item]['state'] == "closed":
                    amount_closed += 1

                open_pull_requests.append(amount_open)
                closed_pull_requests.append(amount_closed)
                create_times.append(open_time)

    l = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(create_times)
        .add_yaxis("Currently Open Pull Requests", open_pull_requests, is_smooth=True,
                   itemstyle_opts=opts.ItemStyleOpts(color="#00FF00"))
        .add_yaxis("Currently Closed Pull Requests", closed_pull_requests, is_smooth=True,
                   itemstyle_opts=opts.ItemStyleOpts(color="#A020F0"))
        .set_global_opts(title_opts=opts.TitleOpts(title="Pull Requests"))
    )
    return l


def bar_base_commits() -> Bar:
    with open(f'{backend.server1.JSON_COMMITS}.json', 'r') as f:
        data = json.loads(f.read())
        contributors = []
        additions = []
        deletions = []

        for item in data:
            if len(data[item]) > 0:
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
            ),
            title_opts=opts.TitleOpts(title="Commits")
        )
    )
    return b


def bar_base_standard_metrics() -> Bar:
    with open(f'{backend.server1.JSON_STANDARD}.json', 'r') as f:
        data = json.loads(f.read())
        metrics = [data['0']['Number of commits: '], data['0']['Number of pull requests:'], data['0']['Number of issues raised']]
        titles = ["Commits", "Pull Requests", "Issues Raised"]

    b = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(titles)
        .add_yaxis("Standard Metrics", metrics, category_gap='10%',
                   itemstyle_opts=opts.ItemStyleOpts(color="#FF0000"))
        .reversal_axis()
        .set_global_opts(title_opts=opts.TitleOpts(title="Standard Metrics"))
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
def home():
    return render_template("home.html")


@app.route("/standard_metrics")
def standard_metrics():
    return render_template("standardMetrics.html")


@app.route("/standardMetrics")
def standard_metrics_graph():
    sb = bar_base_standard_metrics()
    return sb.dump_options_with_quotes()


@app.route("/productivity_measurements")
def main():
    return render_template("main.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
