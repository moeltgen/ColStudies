"""
    colstudies application
"""

import json
import globalvars as g

import requests


def get_jwtToken(hostname, username, password):
    """
    todo

    """

    import urllib3

    urllib3.disable_warnings()

    tokenEndpoint = "https://" + hostname + "/token/createtoken"
    response = requests.post(
        tokenEndpoint,
        json={"username": username, "password": password},
        allow_redirects=True,
        verify=False,
    )

    if response.ok is not True:
        print("Could not get token. Status code: ", response.status_code)
        tokenHeader = ""
        return tokenHeader

    jsonResponse = response.json()
    jwtToken = jsonResponse["access_token"]
    tokenHeader = {"Authorization": "Bearer " + jwtToken}

    # get Repository information
    # response = requests.get("https://"+self.host+"/api/v1/repository/info", headers=tokenHeader, verify=False)
    return tokenHeader


def getFileList(studyno):
    """

    get the files for a study from DBKEdit
    no authentication required

    parse result: 'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>

    Request Type: GET
    URL: https://svko-dbk-test03.gesis.intra/dbkedit/getFileList.asp?study=0017&format=txt
    """

    dbkeditheaders = {"Content-Type": "application/xml;charset=UTF-8"}

    URL = g.dbkediturl + "getFileList.asp?study=" + studyno + "&format=txt"

    response = requests.get(URL, headers=dbkeditheaders, verify=False)
    if response.ok:
        return [response.status_code, response.text]
    else:
        return [response.status_code, ""]


def postFileList(studyno, filelist):
    """

    post the files for a study to DBKEdit
    active logged in session for DBKEdit required

    parse result: 'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>

    Request Type: POST
    URL: https://svko-dbk-test03.gesis.intra/dbkedit/getFileList.asp?study=0017&format=txt
    """

    dbkeditheaders = {"Content-Type": "application/xml;charset=UTF-8"}

    URL = g.dbkediturl + "postFileList.asp"

    username = g.dbkeditusername
    password = g.dbkeditpassword

    response = requests.post(
        URL,
        headers=dbkeditheaders,
        auth=(username, password),
        json=filelist,
        verify=False,
    )
    if response.ok:
        # print(response.text)
        return [response.status_code, response.text]
    else:
        # print(response.text)
        return [response.status_code, response.text]

    print(response)
