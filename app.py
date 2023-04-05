from flask import Flask, render_template
from multiprocessing import Value
import subprocess

app = Flask(__name__)
counter = Value('i', 0)
 
def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

@app.route('/')
def index():
    return ""

@app.route('/healthz')
def healthz():
    return render_template('healthz.html')

@app.route('/alert')
def alert(alert=None):
    with counter.get_lock():
        counter.value += 1
        out = counter.value
    return ""

@app.route('/counter')
def count(alert=None):
    return render_template('counter.html', alert=counter.value)

@app.route('/version')
def version(git_sort_hash=None):
    return render_template('version.html', git_sort_hash=get_git_revision_short_hash())
 
if __name__ == '__main__':
    app.run()