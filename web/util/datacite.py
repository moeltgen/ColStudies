"""
    Provide information for the datacite json
"""
import io
import json
import globalvars as g
import traceback
import requests
import util.ddixml as ddi  # moved to util folder

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

def html_encode(s):
    """
    Returns the HTML encoded version of the given ASCII string. 
    """
    htmlCodes = (
            ('&', '&amp;'), #needs to be first 
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;')            
        )
    for code in htmlCodes:
        s = s.replace(code[0], code[1])
    return s


def write_datacitejson_fromddixml(filename, ddixml, cvcoll, studyurl, additionalInfo):
    """
    Builds the DataCite json and writes it into file
    
    """
    try:
        
        
        jsonobject = get_datacite_json_fromddixml(ddixml, cvcoll, studyurl, additionalInfo)
        
               
        f = open(filename, "w", encoding="utf-8")
        json.dump(jsonobject, f, indent=4)
        
        f.close()

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())


def get_datacite_json_fromddixml(ddixml, cvcoll, studyurl, additionalInfo):
    """
    Builds and returns the DataCite json, uses ddi xml as input
    """

    jsonobject = {}

    try:
        jsonstring = ""
        
        data = {}
        
        
        content = {}
        
        
        
        
        
        study = ddi.ddixml_to_study(ddixml, cvcoll, studyurl)
        attributes = dict_study_to_json(study, additionalInfo)
        content['type'] = "dois"
        content['attributes'] = attributes
       
        data['data'] = content

        #print(data)
        
        jsonobject = data #no: json.dumps(data)
        
        
    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return jsonobject





def dict_study_to_json(study, additionalInfo):
    """
    ##########################################################################
    Convert a study to the DataCite JSON
    input: study object
    ##########################################################################
    """

    xmlstring = ""
    
    content = {}

    try:
                
        # requiredFields = Array("titles", "creators", "publisher", "publicationYear", "types")
        
        
        #geoLocations, geoLocationPlace (nur Ländernamen, English)
        #study["GeoIDs"] = []  # ISO nation codes
        #study["GeoTitlesEN"] = []
        #study["GeoTitlesDE"] = []
        locations = []
        if additionalInfo:
            for geo in study["GeoTitlesEN"]:
                if not geo=="":        
                    location = {"geoLocationPlace": geo}
                    locations.append(location)
        #add all locations     
        content['geoLocations'] = locations  
        ##############################################
        
        types = {"resourceTypeGeneral": "Dataset"}
        content['types'] = types
        
        version = study["Version"].strip()
        content['version'] = version
        
        ten = html_encode(study["TitleEN"].strip())
        tde = html_encode(study["TitleDE"].strip())
        titleen = {"lang": "en", "title": ten}
        titlede = {"lang": "de", "title": tde}
        titles = [titlede, titleen]         #todo: subtitles
        content['titles'] = titles
        
        creators = []
        for itm in study["Creators"]:
            #print(itm)
            if itm["FirstName"]=="" and itm["Name"]=="":
                if not itm["Affiliation"]=="":
                    cr = {"name": itm["Affiliation"].strip(), "nameType": "Organizational", "affiliation": [], "nameIdentifiers":[]}
                    
                    creators.append(cr)
                    
            else:
                crname = itm["Name"].strip()
                if not itm["FirstName"]=="":
                    crname += ", " + itm["FirstName"].strip()
                    if not itm["Affiliation"]=="":
                        cr = {"name": crname, "nameType": "Personal", "givenName": itm["FirstName"].strip(), "familyName": itm["Name"].strip(), "affiliation": [{"name": itm["Affiliation"]}], "nameIdentifiers":[]}
                    else:
                        cr = {"name": crname, "nameType": "Personal", "affiliation": [], "nameIdentifiers":[]}
                else:
                    cr = {"name": crname, "nameType": "Personal"}
                creators.append(cr)
        
        content['creators'] = creators
        
        doi=study["DOI"]
        DOIparts = doi.split("/")
        prefix = DOIparts[0].strip()
        suffix = DOIparts[1].strip()
        #content['prefix'] = prefix
        #content['suffix'] = suffix
        
        
        
        url = study["DataURL"].strip()
        content['url'] = url
        
        publicationYear = study["PublicationYear"].strip()
        content['publicationYear'] = publicationYear
        
        ##################
        #dates, collected
        dates = []
        count=0
        if additionalInfo:
            for itm in study["CollDatesStart"]:
                
                item = itm["Date"].strip()
                item2 = study["CollDatesEnd"][count]["Date"].strip()
                text=item 
                if not item2=="":
                    text+="/"+item2
                date = {"date": text, "dateType": "Collected"}
                dates.append(date) 
                count+=1
        
        #dates, issued (new: use VersionDate for this)
        item = study["VersionDate"].strip()
        if not additionalInfo:
            #use only the year of the version date 
            if len(item)>4:
                item=item[0:4]
        if True: #not item=="":
            date = {"date": item, "dateType": "Issued"}
            dates.append(date) 

        content['dates'] = dates
        ##################
        
                    
        
        #publisher        
        #print("Publisher: ", study["Publisher"])
        #override the long name from study object 
        publisherName = {"name": "GESIS Data Archive"}
        content['publisher'] = publisherName
        
        if additionalInfo:
            rightsList = [
                    {
                        "lang": "de",
                        "rights": "Alle im GESIS DBK veröffentlichten Metadaten sind frei verfügbar unter den Creative Commons CC0 1.0 Universal Public Domain Dedication. GESIS bittet jedoch darum, dass Sie alle Metadatenquellen anerkennen und sie nennen, etwa die Datengeber oder jeglichen Aggregator, inklusive GESIS selbst. Für weitere Informationen siehe https://search.gesis.org/faq"
                    },
                    {
                        "lang": "en",
                        "rights": "All metadata from GESIS DBK are available free of restriction under the Creative Commons CC0 1.0 Universal Public Domain Dedication. However, GESIS requests that you actively acknowledge and give attribution to all metadata sources, such as the data providers and any data aggregators, including GESIS. For further information see https://search.gesis.org/faq"
                    }
                ]
        else:
            rightsList = []
        content['rightsList'] = rightsList
        
        #todo? "language": "en" (fixed?)
        
        identifiers = []
        #no FDZ 
        if additionalInfo:
            ident = study["No"].strip() 
            identifier = {"identifier": ident, "identifierType": "ZA-No."}
            identifiers.append(identifier)            
        content['identifiers'] = identifiers            
        
        
        #could not find
        # - study["Availability"]
        
        ##############################################
        # subjects
        # Topics: No ZA topics anymore
        #study["TopicsEN"] = []
        #study["TopicsDE"] = []
        # Topics: CESSDA Topic Classification
        subjects = []
        for topic in study["CESSDATopicsDE"]:
            if not topic=="":        
                subject = {"lang": "de", "subject": topic, "subjectScheme": "CESSDA Topic Classification"}
                subjects.append(subject)
        for topic in study["CESSDATopicsEN"]:
            if not topic=="":        
                subject = {"lang": "en", "subject": topic, "subjectScheme": "CESSDA Topic Classification"}
                subjects.append(subject)
        
        #add all subjects     
        content['subjects'] = subjects  
        ##############################################
        
        ##############################################
        # contributors: Contributors
        
        #todo: Role currently not available. , "contributorType": itm["Role"].strip()           TODO 
        
        contributors = []
        if additionalInfo:
            for itm in study["Contributors"]:
                #print(itm)
                if itm["FirstName"]=="" and itm["Name"]=="":
                    if not itm["Affiliation"]=="":
                        cr = {"name": itm["Affiliation"].strip(), "nameType": "Organizational"}
                        contributors.append(cr)
                        
                else:
                    crname = itm["Name"].strip()
                    if not itm["FirstName"]=="":
                        crname += ", " + itm["FirstName"].strip()
                    cr = {"name": crname, "nameType": "Personal", "givenName": itm["FirstName"].strip(), "familyName": itm["Name"].strip()}
                    contributors.append(cr)
        
        content['contributors'] = contributors
        ##############################################
        
        # relatedIdentifiers: not available in study object
        
        ##############################################
        #descriptions - several: abstract, methods....
        descriptions = []
        #abstract 
        desc = study["AbstractDE"].strip() 
        if not desc=="":        
            description = {"lang": "de", "description": desc, "descriptionType": "Abstract"}
            descriptions.append(description)
        desc = study["AbstractEN"].strip() 
        if not desc=="":        
            description = {"lang": "en", "description": desc, "descriptionType": "Abstract"}
            descriptions.append(description)
        #scheinen bisher nicht exportiert worden zu sein:
        #study["FurtherRemarksDE"]
        #study["FurtherRemarksEN"]
        
        
        #summary 
        #desc = study["PurposeDE"].strip() 
        #if not desc=="":        
        #    description = {"lang": "de", "description": desc, "descriptionType": "TableOfContents"}
        #    descriptions.append(description)
        #desc = study["PurposeEN"].strip() 
        #if not desc=="":        
        #    description = {"lang": "en", "description": desc, "descriptionType": "TableOfContents"}
        #    descriptions.append(description)
        
        #seems to be missing as well:
        """
        # More study information from List of CVs
        study["ModeCollsEN"] = []
        study["ModeCollsDE"] = []
        study["SampProcsEN"] = []
        study["SampProcsDE"] = []
        study["TimeMethsEN"] = []
        study["TimeMethsDE"] = []
        study["AnalysisUnitsEN"] = []
        study["AnalysisUnitsDE"] = []
        study["KindOfDataEN"] = []
        study["KindOfDataDE"] = []
        # and freetexts
        study["ModeCollFreeEN"] = ""        #done
        study["ModeCollFreeDE"] = ""        #done
        study["SampProcFreeEN"] = ""        #done
        study["SampProcFreeDE"] = ""        #done
        study["TimeMethFreeEN"] = ""
        study["TimeMethFreeDE"] = ""
        study["AnalysisUnitFreeEN"] = ""        #done
        study["AnalysisUnitFreeDE"] = ""        #done
        study["KindOfDataFreeEN"] = ""
        study["KindOfDataFreeDE"] = ""
        """
        
        #Method: Universe // Grundgesamtheit
        desc = study["AnalysisUnitFreeDE"].strip() 
        if not desc=="":        
            description = {"lang": "de", "description": desc, "descriptionType": "Methods"}
            descriptions.append(description)
        desc = study["AnalysisUnitFreeEN"].strip()
        if not desc=="":        
            description = {"lang": "en", "description": desc, "descriptionType": "Methods"}
            descriptions.append(description)
        #Method: // Auswahlverfahren
        desc = study["SampProcFreeDE"].strip() 
        if not desc=="":        
            description = {"lang": "de", "description": desc, "descriptionType": "Methods"}
            descriptions.append(description)
        desc = study["SampProcFreeEN"].strip()
        if not desc=="":        
            description = {"lang": "en", "description": desc, "descriptionType": "Methods"}
            descriptions.append(description)
        #Method: // Erhebungsmodus
        desc = study["ModeCollFreeDE"].strip() 
        if not desc=="":        
            description = {"lang": "de", "description": desc, "descriptionType": "Methods"}
            descriptions.append(description)
        desc = study["ModeCollFreeEN"].strip()
        if not desc=="":        
            description = {"lang": "en", "description": desc, "descriptionType": "Methods"}
            descriptions.append(description)    
        
        #add all descriptions     
        content['descriptions'] = descriptions  
        ##############################################
        
        
        #DOI 
        content['doi'] = doi.strip()
        
        #no event
        

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return content



def logintest_datacite(dataciteapi, username, password):
    """
    test if login is possible
    """
    returnmsg = ""
    
    import urllib3

    urllib3.disable_warnings()
    
    try:
        
        dataciteheaders = {"Content-Type": "application/json",
                            "accept": "application/vnd.api+json"}
        
        #empty metadata
        payload = { "data": { "type": "dois" } }
        

        # try to update a random doi with empty metadata: DOI needs to be in repo
        
        randomDOI = "10.4232/1.11636test"
        url = dataciteapi + "/" + randomDOI
        
        
        response = requests.put( url,
            json=payload,
            headers=dataciteheaders,
            auth=(username, password),
            verify=False,
        )
        
        

        if response.status_code==422:
            #param is missing or the value is empty: attributes
            #this means that authentication was successful
            #print("SUCCESS")
            #print(response.text)
            return ["1","SUCCESS"]
        elif response.status_code==404:
            #DOI not found
            # this means that authentication cannot be checked
            print("Authentication cannot be checked because DOI does not exist!", randomDOI )
            return ["0","FAILED"]
        else:
            #e.g. 401 Bad credentials
            #print("FAILED")   
            #print(response.text)
            return ["0","FAILED"]
        
     

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return returnmsg
