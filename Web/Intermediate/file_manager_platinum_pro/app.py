#!/usr/bin/env python3

import functools
import os
from uuid import uuid4

from flask import Flask, request, render_template, redirect, url_for, send_file
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = uuid4().hex

pg_user, pg_password = os.getenv("PG_USER"), os.getenv("PG_PASSWORD")
pg_host, pg_database = os.getenv("PG_HOST", "localhost"), os.getenv("PG_DATABASE", "database")

app.config["DEBUG"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}/{pg_database}"

login_mgr = LoginManager()
login_mgr.init_app(app)

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    download_limit = Column(Integer, nullable=False, default=5)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False, unique=True)


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return str(e), 400


@login_mgr.user_loader
def load_user(user_id):
    with Session() as session:
        return session.query(User).filter_by(id=user_id).first()


@login_mgr.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("files"))

    if request.method == "GET":
        return render_template("login.html")

    username, password = request.form.get("username"), request.form.get("password")
    if not username or not password:
        return render_template("login.html", user_message="Username and password are required.")

    with Session() as session:
        user = session.query(User).filter_by(username=username).first()

    if user and user.verify_password(password):
        login_user(user)
        return redirect(url_for("files"))

    return render_template("login.html", user_message="Login failed")


@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/files")
@login_required
def files():
    try:
        count = request.args.get("count", default=12, type=int)
        page = request.args.get("page", default=0, type=int)
        if count < 0 or page < 0:
            raise BadRequest(f"count and page must be non-negative")
        if query := request.args.get("query", default="", type=str):
            where_clause = f"and filename like '%{query}%   '"
        else:
            where_clause = ""
    except Exception as e:
        raise BadRequest(str(e))

    with Session() as session:
        files = session.execute(
            text(f"select "
                 f"ROW_NUMBER() OVER (ORDER BY id) AS row, "
                 f"* from files "
                 f"where user_id = '{current_user.id}' {where_clause} "
                 f"limit {count} offset {page * count}")
        ).fetchall()

        return render_template("files.html",
                               files=files,
                               query=query,
                               count=count,
                               page=page)


@app.route("/files/<user_id>/<file_name>")
@login_required
def get_file(user_id, file_name):
    if os.path.exists(f"public/{user_id}/{file_name}"):
        return send_file(f"public/{user_id}/{file_name}")
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
