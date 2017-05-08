# -*- coding: utf-8 -*-
from lxml import html
from bs4 import BeautifulSoup
import requests
import argparse
import json
import re



def parseDate(date):
    if date is not None:

        print date
        darr = ''
        if '/' in date:
            darr = date.split('/')
        elif '-' in date:
            darr = date.split('-')
        return darr[2] + darr[0] + darr[1]


def getMatchResult(score):
    if score[0] > score[1]:
        return ["Win", "Loss"]
    elif score[1] > score[0]:
        return ["Loss", "Win"]
    else:
        return ["tie", "tie"]

def parse(date):
    lines = getWebPage(date)

    # matches = []
    # for line in lines:
    #
    #     print line.contents[0].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text + ' ' + \
    #           line.contents[0].find_all("span", {"class": "record"})[0].find_all("a")[0].text + ' ' + \
    #           line.contents[1].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text
    #
    #     home = line.contents[0].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text
    #     away = line.contents[1].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text
    #     score = line.contents[0].find_all("span", {"class": "record"})[0].find_all("a")[0].text.split(' - ')
    #
    #     homeRes, awayRes = getMatchResult(score)
    #
    #     if len(score) > 1:
    #         gameObj = {'home': {'name': home, 'score': score[0], 'result': homeRes },
    #                    'away': {'name': away, 'score': score[1], 'result': awayRes }}
    #     else:
    #         gameObj = {'home': {'name': home, 'score': 0, 'result': "tie" },
    #                    'away': {'name': away, 'score': 0, 'result': "tie"}}
    #
    #     matches.append(gameObj)
    #
    # # Write matches to json file
    # with open('data.json', 'w') as outfile:
    #     json.dump(matches, outfile)
    # return matches

def parseMatch(lines):
    matches = []
    for line in lines:

        print line.contents[0].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text + ' ' + \
              line.contents[0].find_all("span", {"class": "record"})[0].find_all("a")[0].text + ' ' + \
              line.contents[1].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text

        home = line.contents[0].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text
        away = line.contents[1].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text
        score = line.contents[0].find_all("span", {"class": "record"})[0].find_all("a")[0].text.split(' - ')

        homeRes, awayRes = getMatchResult(score)

        if len(score) > 1:
            gameObj = {'home': {'name': home, 'score': score[0], 'result': homeRes },
                       'away': {'name': away, 'score': score[1], 'result': awayRes }}
        else:
            gameObj = {'home': {'name': home, 'score': 0, 'result': "tie" },
                       'away': {'name': away, 'score': 0, 'result': "tie"}}

        matches.append(gameObj)
    return matches


def getWebPage(date):
    if date is None:
        return None
    date = parseDate(date)
    url = 'http://espndeportes.espn.com/futbol/fixtures/_/fecha/' + date + '/liga/mex.1'
    print 'fetching data from...'
    print url

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")

    acutalDate = soup.findAll("div", {"id" : "sched-container"})
    print acutalDate[0].contents[0].find_all("a", {"class": "team-name"})
    print acutalDate[0].contents[1]

    matches = {}
    currentDate = ""
    for content in acutalDate[0].contents:

        if re.match(".+,\s[0-3][0-9]\s.+", content.text):
            currentDate = content.text
        else:
            teams = content.find_all("tr", {"class": ["odd", "even"]})
            if len(teams) > 0:
                matches[currentDate] = parseMatch(teams)


    #lines = soup.find_all("tr", {"class": ["odd", "even"]})
    with open('data.json', 'w') as outfile:
        json.dump(matches, outfile)
    return matches


def writeMatchesToFile(date):
    lines = getWebPage(date)

    matches = []
    for line in lines:
        home = cleanUpTeamName(line.contents[0].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text) + ','
        score = line.contents[0].find_all("span", {"class": "record"})[0].find_all("a")[0].text + ','
        away = cleanUpTeamName(
            line.contents[1].find_all("a", {"class": "team-name"})[0].find_all("span")[0].text) + ',\n'
        match = home + score + away

        print match
        matches.append(match)

    writeToFile(matches)

def writeToFile(lines):
    file = 'matches.txt'
    with open(file, 'w') as f:
        for line in lines:
            print line
            f.write(line.encode('utf8'))
    print 'Information saved to ' + file

# Needed for some unicode characters from mexican teams
def cleanUpTeamName(teamName):
    if not teamName.isalpha():
        if teamName.startswith('Q'):
            return 'Queretaro'
        if teamName.startswith('L'):
            return 'Leon'
    return teamName


d = "04/23/2016"  # input("Date of the page you want parsed, is the following format mm/dd/yyyy\n")
parse(d)

#def parseYear():


''' REMOVE THIS WHEN I WANT TO USE ON IT'S OWN
parser = argparse.ArgumentParser()
parser.add_argument("date", help="Date of the page you want parsed, is the following format mm/dd/yyyy",
                    type=str)
args = parser.parse_args()

#parse(args.date)
print args.date
parse(args.date)
#writeMatchesToFile(args.date)

#cleanUpTeamName('Querétaro')
'''
