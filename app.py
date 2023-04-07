from flask import Flask, render_template, request
from dotenv import load_dotenv
import subprocess
import redis
import os

app = Flask(__name__)
load_dotenv()

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
def alert():
    r.incr('counter')
    return 'Counter incremented'

@app.route('/counter')
def count(alert=None):
    if r.exists("counter"):
        counter = r.get("counter").decode("utf-8")
    else:
        counter = 0

    return render_template('counter.html', alert=counter)

@app.route('/version')
def version(git_sort_hash=None):
    return render_template('version.html', git_sort_hash=get_git_revision_short_hash())
 
if __name__ == '__main__':
    app.run()