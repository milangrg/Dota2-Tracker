from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import time

app = Flask(__name__)
with open("static/heroes.json", "r") as f:
    hero_db = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/searchresult", methods=["POST"])
def searchresult():
    accountid = request.form["id"]
    if not accountid:
        return redirect(url_for("home"))
    
    url = f"https://api.opendota.com/api/players/{accountid}/recentMatches"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data:
        matchid = []
        hero = []
        kills = []
        deaths = []
        assists = []
        duration = []
        xp = []
        gold = []
        for i in range(10):
            matchid.append(data[i]['match_id'])
            hero.append(data[i]['hero_id'])
            kills.append(data[i]['kills'])
            deaths.append(data[i]['deaths'])
            assists.append(data[i]['assists'])
            duration.append(data[i]['duration'])
            xp.append(data[i]['xp_per_min'])
            gold.append(data[i]['gold_per_min'])
        return render_template("searchresult.html", count=len(matchid), matchid=matchid, hero=hero, kills=kills, deaths=deaths, assists=assists, duration=duration, xp=xp, gold=gold, accountid=accountid)
    else:
        return redirect(url_for("home"))
    
@app.route("/matchdetails/<matchid>")
def matchdetails(matchid):
    url = f"https://api.opendota.com/api/matches/{matchid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hero = []
        player = []
        level = []
        kills = []
        deaths = []
        assists = []
        lh = []
        dn = []
        net = []
        gpm = []
        xpm = []
        for i in range(10):
            accountid = data['players'][i]['account_id']
            if accountid:
                player.append(data['players'][i]['personaname'])
            else:
                player.append('Anonymous')
            hero.append(hero_db[data['players'][i]['hero_id']-1]['localized_name'])
            level.append(data['players'][i]['level'])
            kills.append(data['players'][i]['kills'])
            deaths.append(data['players'][i]['deaths'])
            assists.append(data['players'][i]['assists'])
            lh.append(data['players'][i]['last_hits'])
            dn.append(data['players'][i]['denies'])
            net.append(data['players'][i]['net_worth'])
            gpm.append(data['players'][i]['gold_per_min'])
            xpm.append(data['players'][i]['xp_per_min'])
        score = (data['radiant_score'], data['dire_score'])
        win = data['radiant_win']
        return render_template("matchdetails.html", matchid=matchid, hero=hero, player=player, level=level, kills=kills, deaths=deaths, assists=assists, lh=lh, dn=dn, net=net, gpm=gpm, xpm=xpm, score=score, win=win)

@app.route("/teams")
def teams():
    url = "https://api.opendota.com/api/teams"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        logos = []
        names = []
        ids = []
        ratings = []
        wins = []
        losses = []
        for i in range(30):
            logos.append(data[i]['logo_url'])
            names.append(data[i]['name'])
            ids.append(data[i]['team_id'])
            ratings.append(data[i]['rating'])
            wins.append(data[i]['wins'])
            losses.append(data[i]['losses'])
        return render_template("teams.html", count=len(logos), logos=logos, names=names, ids=ids, ratings=ratings, wins=wins, losses=losses)

@app.route("/promatches")
def promatches():
    url = "https://api.opendota.com/api/proMatches"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        matchid = []
        radiant_name = []
        dire_name = []
        radiant_win = []
        duration = []
        start_time = []
        league_name = []
        for i in range(30):
            matchid.append(data[i]['match_id'])
            radiant_name.append(data[i]['radiant_name'])
            dire_name.append(data[i]['dire_name'])
            radiant_win.append(data[i]['radiant_win'])
            mins = data[i]['duration'] // 60
            secs = data[i]['duration'] % 60
            duration.append(f"{mins}:{secs:02d}")
            ts = time.time() - 1800
            diff = ts - data[i]['start_time']
            if diff >= 86400:
                diff = int(diff // 86400)
                start_time.append(f"{diff} day(s) ago")
            elif diff >= 3600:
                diff = int(diff // 3600)
                start_time.append(f"{diff} hours(s) ago")
            else:
                diff = int(diff // 60)
                start_time.append(f"{diff} minute(s) ago")
            league_name.append(data[i]['league_name'])
        return render_template("promatches.html", count=len(matchid), id=matchid, radiant=radiant_name, dire=dire_name, radiant_win=radiant_name, start_time=start_time, duration=duration, league=league_name)

@app.route("/promatchdetails/<matchid>")
def promatchdetails(matchid):
    url = f"https://api.opendota.com/api/matches/{matchid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hero = []
        player = []
        level = []
        kills = []
        deaths = []
        assists = []
        lh = []
        dn = []
        net = []
        gpm = []
        xpm = []
        for i in range(10):
            name = data['players'][i]['name']
            if not name:
                name = data['players'][i]['personaname']
            if not name:
                player.append('Anonymous')
            player.append(name)
            
            hero.append(hero_db[data['players'][i]['hero_id']-1]['localized_name'])
            level.append(data['players'][i]['level'])
            kills.append(data['players'][i]['kills'])
            deaths.append(data['players'][i]['deaths'])
            assists.append(data['players'][i]['assists'])
            lh.append(data['players'][i]['last_hits'])
            dn.append(data['players'][i]['denies'])
            net.append(data['players'][i]['net_worth'])
            gpm.append(data['players'][i]['gold_per_min'])
            xpm.append(data['players'][i]['xp_per_min'])
        score = (data['radiant_score'], data['dire_score'])
        win = data['radiant_win']
        radiant = "Anonymous"
        if data['radiant_team_id'] and 'radiant_team' in data:
            radiant = data['radiant_team']['name']
        dire = "Anonymous"
        if data['dire_team_id'] and 'dire_team' in data:
            dire = data['dire_team']['name']
        return render_template("promatchdetails.html", matchid=matchid, hero=hero, player=player, level=level, kills=kills, deaths=deaths, assists=assists, lh=lh, dn=dn, net=net, gpm=gpm, xpm=xpm, score=score, win=win, radiant=radiant, dire=dire)

@app.route("/proplayers")
def proplayers():
    url = "https://api.opendota.com/api/proPlayers"
    response = requests.get(url)
    if response.status_code == 200:
        # data = json.loads(response.text)
        data = response.json()
        list_name = []
        list_steam_id = []
        list_avatar = []
        list_team_id = []
        list_team_name = []
        for i in range(10):
            list_name.append(data[i]['name'])
            list_steam_id.append(data[i]['steamid'])
            list_avatar.append(data[i]['avatar'])
            list_team_id.append(data[i]['steamid'])
            list_team_name.append(data[i]['team_name'])
        return render_template("proplayers.html", count=len(list_name), names=list_name, steamids=list_steam_id, avatars=list_avatar, teamids=list_team_id, teams=list_team_name)

# testing/debugging purpose
# @app.route("/search", methods=["POST", "GET"])
# def search():
#     if request.method == "POST":
#         accountid = request.form["id"]
#         return redirect(url_for("test", testid=accountid))
#     return render_template("search.html")

# @app.route("/<testid>")
# def test(testid):
#     return f"<h1>{testid}</h1>"

if __name__ == '__main__':
    app.run(debug=True)