import psutil
import logging
import datetime
import threading
import os
import json
import backend.server

from flask.json import jsonify
from flask import Flask, render_template, request, url_for

from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts .charts import Bar, Bar3D

app = Flask(__name__)


def bar_base() -> Bar:
    with open(f'{backend.server.JSON_FILE_PATH}.json', 'r') as f:
        data = json.loads(f.read())
        print(f.read())
        contributors = []
        commits = []

        for item in data:
            contrib = item
            coms = data[item]
            contributors.append(contrib)
            commits.append(coms)
    b = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(contributors)
        .add_yaxis("Commits", commits, category_gap="10%", itemstyle_opts=opts.ItemStyleOpts(color="#000000"))
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(
                is_show=True
            )
        )
    )
    return b


@app.route("/contributors")
def get_contributor_stat_data():
    b = bar_base()
    return b.dump_options_with_quotes()


@app.route("/")
def main():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()
