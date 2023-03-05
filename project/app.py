import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from controllers import index_controller, event_controller, map_controller, summary_controller, timeline_controller, login_controller, logout_controller, register_controller

# Configure application, flaskのインスタンス化 (https://teratail.com/questions/356066)
app = Flask(__name__)

# Ensure templates are auto-reloaded, Trueにすると、テンプレートが変更されたときに再読み込みする。
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Flaskのデフォルトである(デジタル署名された)cookie内に格納するのではなく、ローカルファイルシステム(ディスク)に格納するようにFlaskを構成
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# リクエストを送った後受け取ったレスポンスがcacheされないように設定している
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return index_controller.index()

@app.route("/event")
def event():
    return event_controller.event()

@app.route("/map")
def map():
    return map_controller.map()

@app.route("/summary")
def summary():
    return summary_controller.summary()

@app.route("/timeline")
def timeline():
    return timeline_controller.timeline()

@app.route("/login", methods=["GET", "POST"])
def login():
    return login_controller.login()

@app.route("/logout")
def logout():
    return logout_controller.logout()

@app.route("/register", methods=["GET", "POST"])
def register():
    return register_controller.register()
