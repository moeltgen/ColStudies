"""
    colstudies application
"""

import json
import globalvars as g

import requests
    
def get_jwtToken(hostname, username, password):
    """
        First obtain a JWT access token
        documented at https://docs.colectica.com/portal/technical/deployment/local-jwt-provider/#usage
    """
    
    import urllib3
    urllib3.disable_warnings()

    tokenEndpoint = "https://" + hostname + "/token/createtoken"
    response = requests.post(tokenEndpoint, json={'username': username, 'password': password}, allow_redirects=True, verify=False)
    
    if response.ok is not True:
        print("Could not get token. Status code: ", response.status_code)
        tokenHeader = ''
        return tokenHeader

    jsonResponse = response.json()
    jwtToken = jsonResponse["access_token"]
    tokenHeader = {'Authorization': 'Bearer ' + jwtToken}

    # get Repository information
    #response = requests.get("https://"+self.host+"/api/v1/repository/info", headers=tokenHeader, verify=False)
    return tokenHeader
    
def general_search(item_type, search_term, MaxResults=1, RankResults=True, SearchDepricatedItems=False, SearchLatestVersion=True):
        """
            Perform a general search: https://docs.colectica.com/portal/api/examples/search/
            Request Type: POST
            URL: /api/v1/_query
        """
        

        # MaxResults=0 returns all results
        jsonquery =  {
             "Cultures": [
                 "en-US"
             ],
             "ItemTypes": [
                 item_type
             ],
             "LanguageSortOrder": [
                 "en-US"
             ],
             "MaxResults": MaxResults,
             "RankResults": RankResults,
             "ResultOffset": 0,
             "ResultOrdering": "None",
             "SearchDepricatedItems": SearchDepricatedItems,
             "SearchTerms": [
                 search_term
             ],
             "SearchLatestVersion": SearchLatestVersion
         }
        tokenHeader = g.session_data['tokenHeader']
        URL = "https://"+g.colecticahostname+"/api/v1/_query/"
                
        response = requests.post(URL, headers=tokenHeader, json=jsonquery, verify=False)
        if response.ok:
            #print(response.json())
            return [response.status_code, response.json()]
        else:
            return [response.status_code, '']


def get_an_item(AgencyId, Identifier):
        """
        This request retrieves the lastest version of an item based on known identification information.
        https://docs.colectica.com/portal/api/examples/get-item/
        Request Type: GET
        URL: /api/v1/item/agenct/Id
        """
        tokenHeader = g.session_data['tokenHeader']
        URL = "https://"+g.colecticahostname+"/api/v1/item/"+AgencyId+"/"+Identifier
        response = requests.get(URL, headers=tokenHeader, verify=False)
        if response.ok:
            #print(response.json())
            return [response.status_code, response.json()]
        else:
            return [response.status_code, '']
            
def get_an_item_version(AgencyId, Identifier, Version):
        """
            This request an item based on known identification information.
            https://docs.colectica.com/portal/technical/api/v1/#operation/ApiV1ItemByAgencyByIdByVersionGet
            Request Type: GET
            URL: /api/v1/item/{agency}/{id}/{version}
        """
        tokenHeader = g.session_data['tokenHeader']
        URL = "https://"+g.colecticahostname+"/api/v1/item/"+AgencyId+"/"+Identifier+"/"+Version
        response = requests.get(URL, headers=tokenHeader, verify=False)
        if response.ok:
            return [response.status_code, response.json()]
        else:
            return [response.status_code, '']
            
            