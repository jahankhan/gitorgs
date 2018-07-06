from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/org/<org_name>')
def org(org_name):
    org_url = f'https://api.github.com/orgs/{org_name}/repos?per_page=100'
    headers = {"user-agent": "jahankhan"}
    response = requests.get(org_url, headers=headers)
    forked = response.json()
    starred = forked.copy()
    forked.sort(key=lambda repo: repo["forks"], reverse=True)
    starred.sort(key=lambda repo: repo["stargazers_count"], reverse=True)
    contributed_to = dict()
    contributors = dict()
    # Go through each repo and count contributors to a repo and overall contributions
    # (api rate limit causes a lot of problems here)
    for repo in starred:
        contributors_url = f'https://api.github.com/repos/{org_name}/{repo["name"]}/contributors?per_page=100'
        response2 = requests.get(contributors_url, headers=headers)
        response2 = response2.json()
        contributed_to[f'{repo["name"]}'] = contributed_to.get(f'{repo["name"]}', 0) + len(response2)
        stats_url = f'https://api.github.com/repos/{org_name}/{repo["name"]}/stats/contributors'
        response3 = requests.get(stats_url, headers=headers)
        response3 = response3.json()
        for contributor in response3:
            # check if we hit api rate limit
            if contributor == 'message':
                break
            contributors[f'{contributor["author"]["login"]}'] = contributors.get(f'{contributor["author"]["login"]}', 0) + contributor["total"]

    contributed_to = sorted(contributed_to.items(), key=lambda repo: repo[1], reverse=True)
    contributors = sorted(contributors.items(), key=lambda contributor: contributor[1], reverse=True)

    return render_template('org.html', org=org_name, forked=forked, starred=starred, contributed_to=contributed_to, contributors=contributors)
