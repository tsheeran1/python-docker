#! /usr/bin/env python3

import requests
import json
import re


def getToken(u: str, p: str):

    logindBlock = {'username': u, 'password': p}
    loginUrl = 'https://hub.docker.com/v2/users/login/'

    response = requests.post(loginUrl, data= logindBlock)

    jTOKEN = json.loads(response.content)
    return jTOKEN['token']

def getImageTags(repoName: str, pgNum: int):

    rTagInfo = {}
    tagUrl=f'https://registry.hub.docker.com/v2/repositories/{repoName}/tags/?page={pgNum}'
    response = requests.get(tagUrl).json()
    for result in response['results']:
        currentTag = result['name']
        currentDigest = result['images'][0]['digest']
#        currentTuple = (currentTag, currentDigest)
        rTagInfo.update({currentTag: currentDigest})

    return rTagInfo

def getStableVersion(repoName: str):

    pg = 0
    stableFound = False
    while not stableFound:
        pg = pg+1
        tagList = getImageTags(repoName, pg)
#        print(f'got Page number {pg}')
        
        for tagKey in tagList:
#            print(f'Tag = {tagKey} %t Digest = {tagList[tagKey]}')
            if tagKey =='stable':
                stableDigest = tagList[tagKey]
            if  not (re.search(r"[^0-9.]", tagKey)) and (tagList[tagKey] == stableDigest):
                stableVersion = tagKey
                stableFound = True
                return stableVersion

def main():

    print(f'{getStableVersion("homeassistant/raspberrypi3-homeassistant")}')

    return

main()    

