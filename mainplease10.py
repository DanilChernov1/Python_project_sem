from datetime import datetime
import requests
import json
import pickle
from jinja2 import Template
import plotly.graph_objects as go
ownurl = "http://94.79.54.21:3000"
token = "dIlUIIpKrjCcrmmM"
email = "dvchernov_1@miem.hse.ru"
myname = "Чернов Даниил Викторович"
dataGit = {
            "studEmail": email,
            "beginDate": "2022-01-01" ,
            "endDate": "2022-04-01",
            "timeRange": 1,
            "hideMerge": True,
            "token": token
            }
dataZulip = {"studEmail": email,
             "beginDate": "2022-01-01",
             "endDate": "2022-04-01",
             "timeRange": 1,
             "token": token}
dataJitsi = {"studEmail": email,
             "beginDate": "2021-01-09",
             "endDate": "2022-04-01",
             "beginTime": "10:00:00.000",
             "endTime": "21:00:00.000",
             "token": token}
def Git():
    EndComits ={}
    CircleCommits = {}
    response = requests.post(ownurl + r"/api/git/getDataPerWeek", json=dataGit).json()
    AllCommits =0
    for index in response["projects"]:
        Commits = {}
        for index1 in index["commits_stats"]:
            Commits[index1["beginDate"][:15]] = index1["commitCount"]
            AllCommits += index1["commitCount"]
        EndComits[index["name"]] = Commits
        CircleCommits[index["name"]] = index['commitCount']
    EEndComits = {}
    for index in EndComits.values():
        for index1 in (index.keys()):
            EEndComits[index1] = 0

    for index in EEndComits.keys():
        count = 0
        for i in EndComits.values():
            for index1 in i.keys():
                if index == index1:
                    count+=i[index1]
        EEndComits[index] = count
    LinCommits = {}
    count = 0
    for index in EEndComits.keys():
        count+=EEndComits[index]
        LinCommits[index] = count
    count2 = 0
    LinEndCommits ={}
    for index in EndComits['ivt21-miniproject / Даниил Чернов'].keys():
        count2+=EndComits['ivt21-miniproject / Даниил Чернов'][index]
        LinEndCommits[index]=count2
    return EEndComits, AllCommits, LinCommits, CircleCommits, EndComits['ivt21-miniproject / Даниил Чернов'], LinEndCommits, count2

def Taiga():
    taiga= {}
    for i in range(1, 4):
        if i == 2:
            for j in range(1, 29):
                if j < 10:
                    taiga[f'2022-0{i}-0{j}'] = 0
                else:
                    taiga[f'2022-0{i}-{j}'] = 0
        else:
            for j in range(1, 32):
                if j < 10:
                    taiga[f'2022-0{i}-0{j}'] = 0
                else:
                    taiga[f'2022-0{i}-{j}'] = 0
    story = list()
    tasks = list()
    name = 'Даниил Чернов'
    Taiga1= requests.get("https://track.miem.hse.ru/api/v1/userstories", headers={"x-disable-pagination": "true"}).json()
    Taiga2 = requests.get("https://track.miem.hse.ru/api/v1/tasks", headers={"x-disable-pagination": "true"}).json()

    for index in Taiga1:
        try:
            if index['assigned_to_extra_info']['full_name_display'] == name:
                story.append(index)
        except:
            pass
    for index in Taiga2:
        try:
            if index['assigned_to_extra_info']['full_name_display'] == name:
                tasks.append(index)
        except:
            pass
    for item in taiga.keys():
        for task in tasks:
            if str(task['created_date'][:10]) == item:
                taiga[item] += 1
    taigaLin ={}
    count = 0
    for index in taiga.keys():
        count+=taiga[index]
        taigaLin[index]=count
    return len(story), len(tasks), taigaLin




def Zulip():
    response = requests.post(ownurl + r'/api/zulip/getData', json=dataZulip).json()
    Zulip = {}
    ZulipCount ={}
    chan = []
    count = 0

    for index in response["stats"]:
        if index["messageCount"] != 0:
            Zulip[index["beginDate"][:15]] = index["messageCount"]
            count += index["messageCount"]
            ZulipCount[index["beginDate"][:15]] = count
    for index in response["messages"]:
        if not(index["name"] in chan):
            chan.append(index["name"])

    return Zulip, chan, ZulipCount, count


def Jitsi():
    response = requests.post(ownurl + r'/api/jitsi/sessions', json=dataJitsi).json()
    jitsi = {}
    jitsiL ={}
    room ={}
    for index in response:
        room[index["room"]] = index["room"]
        jitsi[index["date"]] = jitsi.setdefault(index["date"], 0) + 1
    count=0
    for index in jitsi.keys():
        count+=jitsi[index]
        jitsiL[index]=count
    return jitsi, room, jitsiL, count

Commits, AllCommits, LinCommits, CircleCommits, EndCommits, LinEndCommits, CountCommitsPr= Git()

story, task, DataTaiga = Taiga()
FirstFile = open('/home/prsem/dvchernov_1/dvchernov_1/lab_5.html', encoding='utf8').read()
tp = Template(FirstFile)
zulip, chan, zulipCount, ZC = Zulip()
jitsiG, rooms, jitsiL, countJitsi = Jitsi()
with open('/var/www/html/students/dvchernov_1/dvchernov_1.html', 'w', encoding='utf8') as f:
    f.write(tp.render(ProjCount=CountCommitsPr,GitLinGrafProject = go.Figure([go.Scatter(x = list(LinEndCommits.keys()), y= list(LinEndCommits.values()))], layout=go.Layout(template='plotly_dark') ).to_html(),GitGrafProject=go.Figure([go.Bar(x = list(EndCommits.keys()), y= list(EndCommits.values()))], layout=go.Layout(template='plotly_dark') ).to_html(),story=story, tasksT=task,JitsiCount= countJitsi,CountZulip=ZC,DataLenJitsi = go.Figure([go.Scatter(x=list(jitsiL.keys()), y=list(jitsiL.values()))], layout=go.Layout(template='plotly_dark')).to_html(),data=datetime.now().isoformat(),DataLinZulip= go.Figure([go.Scatter(x = list(zulipCount.keys()), y = list(zulipCount.values()))],layout=go.Layout(template='plotly_dark')).to_html(),ZulipChanels=chan,JitsiRooms = list(rooms.values()),GitCircle= go.Figure([go.Pie(values=list(CircleCommits.values()), labels=list(CircleCommits.keys()))], layout=go.Layout(template='plotly_dark')).to_html(),GitLinGraf=go.Figure([go.Scatter(x = list(LinCommits.keys()), y = list(LinCommits.values()))], layout=go.Layout(template='plotly_dark')).to_html() ,gitLin = AllCommits, GitGraf = go.Figure([go.Bar(x = list(Commits.keys()), y = list(Commits.values()))],layout=go.Layout(template='plotly_dark')).to_html(), DataTaiga = go.Figure(go.Scatter(x = list(DataTaiga.keys()), y = list(DataTaiga.values())), layout=go.Layout(template='plotly_dark')).to_html(), DataZulip = go.Figure([go.Bar(x = list(zulip.keys()), y = list(zulip.values()))],layout=go.Layout(template='plotly_dark')).to_html(), DataJitsi = go.Figure(go.Bar(x = list(jitsiG.keys()), y = list(jitsiG.values())), layout=go.Layout(template='plotly_dark')).to_html()))
f.close()
