from flask import Flask, render_template, request
from multiprocessing import Value
from dotenv import load_dotenv
import subprocess
import redis
import os

app = Flask(__name__)
load_dotenv()
counter = Value('i', 0)

try:
    r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), \
        password=os.environ["REDIS_PASSWORD"])
    r.ping()
except Exception as ex:
    exit('Failed to connect, terminating.')
 
def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

@app.route('/')
def index():
    return ""

@app.route('/healthz')
def healthz():
    return render_template('healthz.html')

@app.route('/alert', methods=['GET', 'POST'])
def alert(alert=None):
    with counter.get_lock():
        counter.value += 1
        out = counter.value
    r.mset({"counter": out})
    return ""

@app.route('/counter')
def count(alert=None):
    if r.exists("runner"):
        out = r.get("counter").decode("utf-8")
    else:
        out = counter.value

    return render_template('counter.html', alert=out)

@app.route('/version')
def version(git_sort_hash=None):
    return render_template('version.html', git_sort_hash=get_git_revision_short_hash())
 
if __name__ == '__main__':
    app.run()