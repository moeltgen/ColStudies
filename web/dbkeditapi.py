"""
    colstudies application
"""

import json
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
        
        URL = g.dbkediturl+"getFileList.asp?study=" + studyno + "&format=txt"
                
        response = requests.get(URL, headers=dbkeditheaders, verify=False)
        if response.ok:
            return [response.status_code, response.text]
        else:
            return [response.status_code, '']


def postFileList(studyno, filelist):
        """
          
            post the files for a study to DBKEdit
            active logged in session for DBKEdit required
            
            parse result: 'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>
                
            Request Type: POST
            URL: https://svko-dbk-test03.gesis.intra/dbkedit/getFileList.asp?study=0017&format=txt
        """
        
        dbkeditheaders = {"Content-Type": "application/xml;charset=UTF-8"}
        
        URL = g.dbkediturl+"postFileList.asp"
                
        username = g.dbkeditusername
        password = g.dbkeditpassword
        
        response = requests.post(URL, headers=dbkeditheaders, auth=(username, password), json=filelist, verify=False)
        if response.ok:
            #print(response.text)
            return [response.status_code, response.text]
        else:
            #print(response.text)
            return [response.status_code, response.text]
        
        print(response)
            
            