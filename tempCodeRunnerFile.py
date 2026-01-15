from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
import mysql.connector
import bcrypt
import boto3
import json
import subprocess
from config import Config

# ---------------- APP SETUP ----------------
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = "login"

# ---------------- AWS S3 ----------------
s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)

# ---------------- DATABASE HELPER ----------------
def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

# ---------------- USER MODEL ----------------
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    conn.close()
    return User(user[0], user[1]) if user else None

# ---------------- DOCKER (CLI BASED) ----------------
def start_lab_container():
    """
    Starts a Docker container using Docker CLI.
    This is Windows-safe and reliable.
    """
    try:
        container_id = subprocess.check_output(
            [
                "docker", "run",
                "-d",
                "--memory=128m",
                "--network=bridge",
                "net_explorerlearning-node"
            ],
            stderr=subprocess.STDOUT,
            text=True
        ).strip()
        return container_id
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.output}"

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        hashed_password = bcrypt.hashpw(
            password, bcrypt.gensalt()
        ).decode()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[2].encode()):
            login_user(User(user[0], user[1]))
            return redirect(url_for("lab"))

    return render_template("login.html")

# -------- LOGOUT --------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# ---------------- LAB ----------------
@app.route("/lab")
@login_required
def lab():
    return render_template("lab.html")

@app.route("/start-lab", methods=["POST"])
@login_required
def start_lab():
    container_id = start_lab_container()
    return jsonify({"container_id": container_id})

@app.route("/validate", methods=["POST"])
@login_required
def validate():
    data = request.json
    is_correct = data.get("subnet") == "255.255.255.0"
    return jsonify({"result": is_correct})

@app.route("/complete-lab", methods=["POST"])
@login_required
def complete_lab():
    report = {
        "user": current_user.username,
        "score": 100,
        "topology": "192.168.1.0/24"
    }

    s3.put_object(
        Bucket=Config.S3_BUCKET_NAME,
        Key=f"reports/{current_user.id}/report.json",
        Body=json.dumps(report),
        ContentType="application/json"
    )

    return jsonify({"uploaded": True})

@app.route("/history")
@login_required
def history():
    response = s3.list_objects_v2(
        Bucket=Config.S3_BUCKET_NAME,
        Prefix=f"reports/{current_user.id}/"
    )

    files = [obj["Key"] for obj in response.get("Contents", [])]
    return render_template("history.html", files=files)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
