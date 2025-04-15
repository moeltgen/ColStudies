"""
    colstudies application
"""

import globalvars as g

import requests


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

    import urllib3

    urllib3.disable_warnings()
    
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
        #print(response.text)
        return [response.status_code, response.text]
    else:
        #print(response.text)
        return [response.status_code, response.text]

    print(response)

def LoginTest(username, password):
    """

    Test the login by using the postFileList page at DBKEdit
    
    Request Type: POST
    
    """

    import urllib3

    urllib3.disable_warnings()

    #create empty filelist 
    filelist = []
    fileinfo = {
                    "id": "(0)",
                    "file": 'nn',
                    "SN": 'ZA0000',
                    "size": '0',
                    "dbksize": '0',
                    "type": '0',
                    "dbktype": '0',
                    "pub": False,
                    "datapub": False,
                    "col": '',
                    "dbk": '',
                    "commentde": '',
                    "commenten": '',
                }
    filelist.append(fileinfo)                    

    dbkeditheaders = {"Content-Type": "application/xml;charset=UTF-8"}

    URL = g.dbkediturl + "postFileList.asp"
    
    response = requests.post(
        URL,
        headers=dbkeditheaders,
        auth=(username, password),
        json=filelist,
        verify=False,
    )
    if response.status_code==200:
        # print("SUCCESS")
        return ["1","SUCCESS"]
    else:
        # print("FAILED")   
        print(response)
        return ["0","FAILED"]
