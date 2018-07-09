import argparse
import csv
import subprocess
import tempfile
import sys
import os
import yaml

from datetime import datetime
from jinja2 import Template
from weasyprint import HTML, CSS

class Chdir(object):
    """ Context manager for changing the current working directory """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="Path to configuration file", required=True)
parser.add_argument("--after", help="Start date in format: 2017-12-20", required=True, type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
parser.add_argument("--before", help="End date in format: 2017-12-20", required=True, type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
parser.add_argument("--pdf", help="Path where the generated PDF is saved, default is report.pdf in current directory")
parser.add_argument("--csv", help="Path where the generated CSV is saved, default is report.csv in current directory")
args = parser.parse_args()

tmp_dir = tempfile.mkdtemp(prefix="git-scrapper-")
repo_dir = "%s/repo" % tmp_dir

repos = {}

with open(args.config, 'r') as f:
    config = yaml.load(f)

if not args.pdf or args.csv:
    print "WARNING! No report will be generated, please use --csv or --pdf or both if you want to save the report!\n"

try:
    for repo in config['repos']:
        print "Working with %s repository\n" % repo

        subprocess.check_output(["rm", "-rf", repo_dir])
        subprocess.check_output(["git", "-c", "http.sslVerify=false", "clone", "--bare", repo, repo_dir], stderr=subprocess.STDOUT)

        log_cmd = ["git", "--no-pager", "log", "--all", "--after=%s" % datetime.strftime(args.after, '%Y-%m-%d'), "--before=%s" % datetime.strftime(args.before, '%Y-%m-%d'), "--pretty=format:%ae|%H|%cd"]

        for email in config['emails']:
            log_cmd.append("--author=%s" % email)

        with Chdir(repo_dir):
            commits = subprocess.check_output(log_cmd)

        if not commits.strip():
            print "No commits found\n"
            continue

        repos[repo] = []

        for line in commits.split("\n"):
            commit_data = line.split("|")

            print commit_data

            repos[repo].append({"email": commit_data[0], "hash": commit_data[1], "date": commit_data[2], "repo": repo})

        print "\nDone\n"


    if args.pdf:
        print "Generating PDF..."

        with open("template.html") as f:
            template = Template(f.read())

        rendered = template.render(repos=repos, name=config['name'], date_after = args.after, date_before = args.before)
        html = HTML(string=rendered)
        css = CSS(filename="style.css")
        html.write_pdf(args.pdf, stylesheets=[css])

        print "Done"

    if args.csv:
        print "Generating CSV..."

        with open(args.csv, 'wb') as csvfile:
            fieldnames = ['email', 'hash', 'date', 'repo']

            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()

            for key, repo in repos.items():
                for commit in repo:
                    writer.writerow(commit)

        print "Done"

finally:
    subprocess.call(["rm", "-rf", tmp_dir])

