"""
    colstudies application
"""

import globalvars as g
import xml.etree.ElementTree as ET
import requests


def get_jwtToken(hostname, username, password):
    """
    First obtain a JWT access token
    documented at https://docs.colectica.com/portal/technical/deployment/local-jwt-provider/#usage
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


def general_search(
    item_type,
    search_term,
    MaxResults=1,
    RankResults=True,
    SearchDepricatedItems=False,
    SearchLatestVersion=True,
):
    """
    Perform a general search: https://docs.colectica.com/portal/api/examples/search/
    Request Type: POST
    URL: /api/v1/_query
    """

    # MaxResults=0 returns all results
    jsonquery = {
        "Cultures": ["en", "de", "en-US", "de-DE"],
        "ItemTypes": [item_type],
        "LanguageSortOrder": ["en-US"],
        "MaxResults": MaxResults,
        "RankResults": RankResults,
        "ResultOffset": 0,
        "ResultOrdering": "None",
        "SearchDepricatedItems": SearchDepricatedItems,
        "SearchTerms": [search_term],
        "SearchLatestVersion": SearchLatestVersion,
    }
    tokenHeader = g.session_data["tokenHeader"]
    URL = "https://" + g.colecticahostname + "/api/v1/_query/"
    
    #print(jsonquery)
    
    response = requests.post(URL, headers=tokenHeader, json=jsonquery, verify=False)
    
    if response.ok:
        #print(response.json())
        return [response.status_code, response.json()]
    else:
        return [response.status_code, ""]


def get_an_item(AgencyId, Identifier):
    """
    This request retrieves the lastest version of an item based on known identification information.
    https://docs.colectica.com/portal/api/examples/get-item/
    Request Type: GET
    URL: /api/v1/item/agenct/Id
    """
    tokenHeader = g.session_data["tokenHeader"]
    URL = (
        "https://" + g.colecticahostname + "/api/v1/item/" + AgencyId + "/" + Identifier
    )
    response = requests.get(URL, headers=tokenHeader, verify=False)
    if response.ok:
        # print(response.json())
        return [response.status_code, response.json()]
    else:
        return [response.status_code, ""]


def get_an_item_version(AgencyId, Identifier, Version):
    """
    This request an item based on known identification information.
    https://docs.colectica.com/portal/technical/api/v1/#operation/ApiV1ItemByAgencyByIdByVersionGet
    Request Type: GET
    URL: /api/v1/item/{agency}/{id}/{version}
    """
    tokenHeader = g.session_data["tokenHeader"]
    URL = (
        "https://"
        + g.colecticahostname
        + "/api/v1/item/"
        + AgencyId
        + "/"
        + Identifier
        + "/"
        + Version
    )
    response = requests.get(URL, headers=tokenHeader, verify=False)
    if response.ok:
        return [response.status_code, response.json()]
    else:
        return [response.status_code, ""]


#
# Methods for updating, using the transaction api
#


def createTransaction():
    """
    This request creates a new transaction

    https://docs.colectica.com/portal/technical/api/v1/#tag/Transaction
    Request Type: POST
    URL: /api/v1/transaction/
    """
    tokenHeader = g.session_data["tokenHeader"]
    URL = "https://" + g.colecticahostname + "/api/v1/transaction/"

    response = requests.post(URL, headers=tokenHeader, verify=False)
    if response.ok:
        print(response.json())

        print(
            getTransactionValue(response.json(), "TransactionId")
        )  # start with capital letters here
        print(getTransactionValue(response.json(), "ItemCount"))
        print(getTransactionValue(response.json(), "PropagatedItemCount"))

        return [response.status_code, response.json()]
    else:
        print(response.json())
        return [response.status_code, ""]

    # transactionId


def getTransactionValue(jsonResponse, itemname):
    """
    This returns the value for item from response, e.g. transactionId
    """
    itemvalue = ""

    try:
        i = 0
        for item in jsonResponse:
            if item == itemname:
                itemvalue = jsonResponse[itemname]
                # print(" - ", i, item, itemvalue)

    except Exception as e:
        print("500", "Error " + str(e))

    return itemvalue


def addToTransaction(transactionId, agencyid, itemid, version, Item):
    """
    This request adds an item to a transaction

    https://docs.colectica.com/api/v1/transaction/_addItemsToTransaction
    Request Type: POST
    URL: /api/v1/transaction/
    """
    try:
        tokenHeader = g.session_data["tokenHeader"]
        URL = (
            "https://"
            + g.colecticahostname
            + "/api/v1/transaction/_addItemsToTransaction/"
        )

        StudyType = "30ea0200-7121-4f01-8d21-a931a182b86d"

        StringItem = ET.tostring(Item, encoding="unicode", method="xml")
        # print(StringItem)

        JSONitem = {
            "itemType": StudyType,
            "agencyId": agencyid,
            "version": version + 1,
            "identifier": itemid,
            "item": StringItem,
        }
        # print(JSONitem)

        jsonquery = {"transactionId": transactionId, "items": [JSONitem]}
        print(jsonquery)

        response = requests.post(URL, headers=tokenHeader, json=jsonquery, verify=False)
        if response.ok:
            print(response.json())
            return [response.status_code, response.json()]
        else:
            print(response.json())
            return [response.status_code, ""]
    except Exception as e:
        print("500", "Error " + str(e))


def commitTransaction(transactionId):
    """
    This request commits items in a transaction to the repository

    https://docs.colectica.com/api/v1/transaction/_commitTransaction
    Request Type: POST
    URL: /api/v1/transaction/_commitTransaction
    """
    tokenHeader = g.session_data["tokenHeader"]
    URL = "https://" + g.colecticahostname + "/api/v1/transaction/_commitTransaction/"

    jsonquery = {}  # todo

    response = requests.post(URL, headers=tokenHeader, json=jsonquery, verify=False)
    if response.ok:
        print(response.json())
        return [response.status_code, response.json()]
    else:
        print(response.json())
        return [response.status_code, ""]


def cancelTransaction(transactionId):
    """
    This request cancels a transaction with transactionId

    https://docs.colectica.com/api/v1/transaction/_cancelTransaction
    Request Type: POST
    URL: /api/v1/transaction/_cancelTransaction
    """
    tokenHeader = g.session_data["tokenHeader"]
    URL = "https://" + g.colecticahostname + "/api/v1/transaction/_cancelTransaction/"

    jsonquery = {"transactionId": transactionId}

    response = requests.post(URL, headers=tokenHeader, json=jsonquery, verify=False)
    if response.ok:
        print(response.json())
        return [response.status_code, response.json()]
    else:
        print(response.json())
        return [response.status_code, ""]


def getTransactionInfo(transactionId):
    """
    This request gets info for a transaction with transactionId

    https://docs.colectica.com/api/v1/transaction/_getTransactions
    Request Type: POST
    URL: /api/v1/transaction/_getTransactions
    """
    tokenHeader = g.session_data["tokenHeader"]
    URL = "https://" + g.colecticahostname + "/api/v1/transaction/_getTransactions/"

    jsonquery = [transactionId]

    response = requests.post(URL, headers=tokenHeader, json=jsonquery, verify=False)
    if response.ok:
        TI = response.json()[0]  # first item of array
        print(TI)
        return [response.status_code, TI]
    else:
        print(response.json())
        return [response.status_code, ""]


#
# Methods for updating, using item api
#

# https://docs.colectica.com/api/v1/item/{agency}/{id}/{version}
#


def set_an_item_version(jsonitem):
    """
    This request updates an item
    https://docs.colectica.com/portal/technical/api/v1/#operation/ApiV1ItemByAgencyByIdByVersionGet
    Request Type: POST
    URL: /api/v1/item

    """

    print("#######################")
    print(jsonitem)
    print("#######################")

    tokenHeader = g.session_data["tokenHeader"]
    URL = "https://" + g.colecticahostname + "/api/v1/item"
    response = requests.post(URL, headers=tokenHeader, json=jsonitem, verify=False)
    if response.ok:
        return [response.status_code, response.json()]
    else:
        return [response.status_code, response.json()]
