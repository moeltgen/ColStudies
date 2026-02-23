"""
    Provide information for the CESSDA CDC DDI xml
"""
import io
import xml.etree.ElementTree as ET
import globalvars as g
import traceback
import requests
import util.ddixml as ddi  # moved to util folder


def getCVItem(ElementName, xmllang, strTerm, VocabName, strVocabURI, CVColl, CVName):
        #Returns the XML Content string for the CV item
        #in language en or de
        #with element ElementName
        #
        #looks up the strTerm in the CV with Name CVName from CVColl in the selected language xmllang 

        strHTML = ""
        
        if not ElementName == "": 
            
            #get code from CVColl
            code = ""
            ElementLang="ItemsDE"
            if xmllang=="en":
                ElementLang="ItemsEN"
            for att, val in CVColl[CVName][ElementLang].items():
                if val == strTerm:
                    code=att
                    break 
            
            strHTML += "<" + ElementName
            if xmllang != "":
                strHTML += ' xml:lang="' + xmllang + '"'
            strHTML += ">\n" 

            strHTML += strTerm + '\n'

            strHTML += "<concept"
            if VocabName != "":
                strHTML += ' vocab="' + VocabName + '"'
            if strVocabURI != "":
                strHTML += ' vocabURI="' + strVocabURI + '"'
            strHTML += ">"
            strHTML += code
            strHTML += "</concept>\n" 

            strHTML += "</" + ElementName + ">\n" 
    

        return strHTML

def getVocabInfo(cvsname):

        vocab = []
    
        url_de=""
        url_en=""
        cvname=""
        if cvsname=="kinddata":
                url_de = "https://vocabularies.cessda.eu/v2/vocabularies/GeneralDataFormat/2.0?languageVersion=de-2.0.1"
                url_en = "https://vocabularies.cessda.eu/v2/vocabularies/GeneralDataFormat/2.0?languageVersion=en-2.0"
                cvname = "GeneralDataFormat"
        elif cvsname=="samplingprocedure":
                url_de = "https://vocabularies.cessda.eu/v2/vocabularies/SamplingProcedure/1.1?languageVersion=de-1.1.1"
                url_en = "https://vocabularies.cessda.eu/v2/vocabularies/SamplingProcedure/1.1?languageVersion=en-1.1"
                cvname = "SamplingProcedure"
        elif cvsname=="unittype":
                url_de = "https://vocabularies.cessda.eu/v2/vocabularies/AnalysisUnit/1.0?languageVersion=de-1.0.1"
                url_en = "https://vocabularies.cessda.eu/v2/vocabularies/AnalysisUnit/1.0?languageVersion=en-1.0"
                cvname = "AnalysisUnit"
        elif cvsname=="unittype_v2.1": #wegen neuer Version!!
                url_de = "https://vocabularies.cessda.eu/v2/vocabularies/AnalysisUnit/2.1?languageVersion=de-2.1.1"
                url_en = "https://vocabularies.cessda.eu/v2/vocabularies/AnalysisUnit/2.1?languageVersion=en-2.1"
                cvname = "AnalysisUnit"
        elif cvsname=="modecollection":
                url_de = "https://vocabularies.cessda.eu/v2/vocabularies/ModeOfCollection/4.0?languageVersion=de-4.0.1" #war EN!!
                url_en = "https://vocabularies.cessda.eu/v2/vocabularies/ModeOfCollection/4.0?languageVersion=en-4.0"
                cvname = "ModeOfCollection"
        elif cvsname=="timemethod":
                url_de = "https://vocabularies.cessda.eu/v2/vocabularies/TimeMethod/1.2?languageVersion=de-1.2.1" #war EN!!
                url_en = "https://vocabularies.cessda.eu/v2/vocabularies/TimeMethod/1.2?languageVersion=en-1.2"
                cvname = "TimeMethod"
        elif cvsname=="topicclass":
                url_de = "https://vocabularies.cessda.eu/v2/vocabularies/TopicClassification/4.1?languageVersion=de-4.1.1"
                url_en = "https://vocabularies.cessda.eu/v2/vocabularies/TopicClassification/4.1?languageVersion=en-4.1"
                cvname = "TopicClassification"
        
        vocab = [cvname, url_de, url_en ]
        
        return vocab 

    






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




def write_cdcxml_fromddixml(filename, ddixml, cvcoll, studyurl):
    """
    Builds the CDC xml as tree and writes it into file
    pro: error if not well-formed
    con: no comments
    """
    
    from lxml.etree import tostring # update to lxml to include comments as well 
    import lxml.etree as LET
    
    
    try:
        xmlstring = get_cdcxml_string_fromddixml(ddixml, cvcoll, studyurl)
        
        root = LET.fromstring(xmlstring)
        tree = LET.ElementTree(root)
        
        f = open(filename, "w", encoding="utf-8")
        f.write(tostring(tree, 
                            encoding="unicode",
                            xml_declaration=False, ###encoding with unicode does not allow for declaration
                            pretty_print=True,
                            with_comments=True
                            )
                )
        ### tree.write(
            ### f,
            ### encoding="utf-8",   ###unicode
            ### xml_declaration=True,
            ### default_namespace="ddi:codebook:2_5",        
        ###)
        f.close()

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())
        f = open(filename+".err.xml", "w", encoding="utf-8")
        f.write(xmlstring)
        f.close()


def get_cdcxml_string_fromddixml(ddixml, cvcoll, studyurl):
    """
    Builds and returns the CDC xml as string, uses ddi xml as input
    """
    
    xmlstring = ""
    
    try:
    
        xmlstring += header("", "")  # todo: info object has no English Title

        study = ddi.ddixml_to_study(ddixml, cvcoll, studyurl)
        xmlstring += dict_study_to_root(study, cvcoll)

        
        xmlstring += footer()
        
        #debug
        #print("")
        #print(xmlstring)
        #print("")
        

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return xmlstring


def header(title_en, title_de):
    """
    Returns the CDC xml header
    """
    xmlstring = ""
    #declaration
    # not supported by lxml when using unicode 
    #xmlstring += "<?xml version='1.0' encoding='ISO-8859-1'?>\n" 
    #comments    
    xmlstring += "<!-- Selection of DDI 2.5 Elements and Attributes used by DBK for DDI2.5 Export for CESSDA CDC -->\n"
    xmlstring += "<!-- The original DDI 2.5 Schema can be found at http://www.ddialliance.org/Specification/DDI-Codebook/2.5/ -->\n"
    xmlstring += "<!-- A copy of the DDI 2.5 Schema can be found at http://dbkapps.gesis.org/DDI/2_5 -->\n"
    xmlstring += "<!--                                         -->\n"
    xmlstring += "<!-- created by W. Zenk-Möltgen, 2025-10-17  -->\n"
    xmlstring += "<!-- from Python CDCStudies.py               -->\n"
    xmlstring += "<!-- DDI-Codebook Export Format 2.5          -->\n"
    xmlstring += "<!-- Version 3.1.0                           -->\n"
    xmlstring += "<!--                                         -->\n"
    xmlstring += "<!--                                         -->\n"

    #root node
    xmlstring += '<codeBook xmlns="ddi:codebook:2_5" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    xmlstring += 'xsi:schemaLocation="ddi:codebook:2_5 https://ddialliance.org/Specification/DDI-Codebook/2.5/XMLSchema/codebook.xsd"\n'
    xmlstring += 'version="2.5" >\n'
    
    
    return xmlstring


def footer():
    """
    Returns the CDC xml footer
    """
    
    xmlstring = "</codeBook>\n"
    return xmlstring

def getCitation(study):
    """
    ##########################################################################
    Convert a study to the CDC DDI 2.5 xml - Citation 
    input: study object
    ##########################################################################
    """

    xmlstring = ""

    try:
        
        #special for Colectica studies: check if StudyNo is in title (first with blank, second without blank)
        titleEN = study["TitleEN"].replace(study["No"]+" ","")
        titleDE = study["TitleDE"].replace(study["No"]+" ","")
        titleEN = titleEN.replace(study["No"],"")
        titleDE = titleDE.replace(study["No"],"")        
        
        xmlstring += "\n"
        
        if True:
            xmlstring += '<citation>\n'

            xmlstring += '<titlStmt>\n'
            xmlstring += '<titl xml:lang="en">' + html_encode(titleEN) + '</titl>\n'                #Titel
            xmlstring += '<parTitl xml:lang="de">' + html_encode(titleDE) + '</parTitl>\n'          #Deutscher Titel als parTitl

            #new add IDNo for both languages: 'new include version number for local id in case of DBK

            xmlstring += '<IDNo xml:lang="en" agency="GESIS">' + study["No"]                                             #Studiennummer (und Versionsnummer)
            if study["Version"] != '': xmlstring +=  ', Version ' + study["Version"]
            xmlstring += '</IDNo>\n'
            xmlstring += '<IDNo xml:lang="de" agency="GESIS">' + study["No"]                                             #Studiennummer (und Versionsnummer)
            if study["Version"] != '': xmlstring +=  ', Version ' + study["Version"]
            xmlstring += '</IDNo>\n'

            xmlstring += '<IDNo xml:lang="en" agency="DOI">' + study["DOI"] + '</IDNo>\n'
            xmlstring += '<IDNo xml:lang="de" agency="DOI">' + study["DOI"] + '</IDNo>\n'

            xmlstring += '</titlStmt>\n'

            xmlstring += '<rspStmt>\n'
            
            
            #xmlstring += getPR(Study)                          #Primärforscher
            strPR = ""
            for itm in study["Creators"]:
                if itm["FirstName"]=='-': #new: no firstname
                    AuthE = html_encode(itm["Name"])
                else:
                    AuthE = html_encode(itm["Name"] + ", " + itm["FirstName"])
                Affi = html_encode(itm["Affiliation"])

                if AuthE != '' and Affi != '':
                    strPR += '<AuthEnty xml:lang="en" affiliation="' + Affi + '">' + AuthE + '</AuthEnty>\n' 
                    strPR += '<AuthEnty xml:lang="de" affiliation="' + Affi + '">' + AuthE + '</AuthEnty>\n' 
                else:
                    if Affi != '':
                        strPR += '<AuthEnty xml:lang="en">' + Affi + '</AuthEnty>\n'
                        strPR += '<AuthEnty xml:lang="de">' + Affi + '</AuthEnty>\n'
                    
                    if AuthE != '':
                        strPR += '<AuthEnty xml:lang="en">' + AuthE + '</AuthEnty>\n'
                        strPR += '<AuthEnty xml:lang="de">' + AuthE + '</AuthEnty>\n'
            
            xmlstring += strPR
            
            #new contributors
            #<othId role='editor' affiliation='INRA'>Jane Smith</othId>
            #xmlstring += getContributors(Study)                          #Contributors
            strPR = ""
            for itm in study["Contributors"]:
                if itm["FirstName"]=='-': #new: no firstname
                    AuthE = html_encode(itm["Name"])
                else:
                    AuthE = html_encode(itm["Name"] + ", " + itm["FirstName"])
                Affi = html_encode(itm["Affiliation"])
                
                roleAtt=''
                #roleAtt = 'role="' + html_encode(itm["Role"]) + '"' 
                #todo Colectica currently does not support the Role? study object does not have it 
                if AuthE != '' and Affi != '':
                    strPR += '<othId xml:lang="en" '+roleAtt+' affiliation="' + Affi + '">' + AuthE + '</othId>\n' 
                    strPR += '<othId xml:lang="de" '+roleAtt+' affiliation="' + Affi + '">' + AuthE + '</othId>\n' 
                else:
                    if Affi != '':
                        strPR += '<othId xml:lang="en" '+roleAtt+' >' + Affi + '</othId>\n'
                        strPR += '<othId xml:lang="de" '+roleAtt+' >' + Affi + '</othId>\n'
                    
                    if AuthE != '':
                        strPR += '<othId xml:lang="en" '+roleAtt+' >' + AuthE + '</othId>\n'
                        strPR += '<othId xml:lang="de" '+roleAtt+' >' + AuthE + '</othId>\n'
            
            xmlstring += strPR

            xmlstring += '</rspStmt>\n'

            #fundAg only for SDN
                    #xmlstring += '<prodStmt>\n'
                    #xmlstring += '<fundAg>' & Study.fundingAgency & '</fundAg>\n' 'new .fundingAgency
                    #xmlstring += '</prodStmt>\n'


            xmlstring += '<distStmt>\n'
            xmlstring += '<distrbtr xml:lang="en" abbr="GESIS" affiliation="GESIS - Leibniz Institute for the Social Sciences" URI="http://www.gesis.org/">GESIS Data Archive for the Social Sciences</distrbtr>\n'
            xmlstring += '<distrbtr xml:lang="de" abbr="GESIS" affiliation="GESIS - Leibniz Institut für Sozialwissenschaften" URI="http://www.gesis.org/">GESIS Datenarchiv für Sozialwissenschaften</distrbtr>\n'
            xmlstring += '<distDate date="' + study["PublicationYear"] + '" xml:lang="en"/>\n'            #PublicationDate
            xmlstring += '<distDate date="' + study["PublicationYear"] + '" xml:lang="de"/>\n'            #PublicationDate
            xmlstring += '</distStmt>\n'

            

            #xmlstring += getVersion(Study)                                                               #Version/Publikationsdatum/DOI/Name
            xmlstring += '<verStmt>\n'
            vTextEN = '' #todo Colectica currently does not support Version Text 
            vTextDE = '' #todo Colectica currently does not support Version Text 
            strVersion = '' 
            strVersion += '	<version xml:lang="en" date="' + study["PublicationYear"] + '" type="GESIS Data Archive Version">Version ' + study["Version"] + ' (' + study["VersionDate"] + '), ' + vTextEN + ', doi:' + study["DOI"] + '</version>\n'
            strVersion += '	<version xml:lang="de" date="' + study["PublicationYear"] + '" type="GESIS Data Archive Version">Version ' + study["Version"] + ' (' + study["VersionDate"] + '), ' + vTextDE + ', doi:' + study["DOI"] + '</version>\n'
            xmlstring += strVersion 
            xmlstring += '</verStmt>\n'

            #URL to study description'new 2021-02-11 '2.9.3 not only in docDscr also in stdyDscr
            xmlstring += '<holdings xml:lang="en" URI="https://search.gesis.org/research_data/' + study["No"] + '?lang=en"/>\n' #v0.9.1 remove duplicate ZA
            xmlstring += '<holdings xml:lang="de" URI="https://search.gesis.org/research_data/' + study["No"] + '?lang=de"/>\n' #v0.9.1 remove duplicate ZA       

            xmlstring += "</citation>\n"
        
    
    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return xmlstring

def getStdyInfo(study, cvcoll):
    """
    ##########################################################################
    Convert a study to the CDC DDI 2.5 xml - Study Info  
    input: study object
    ##########################################################################
    """

    xmlstring = ""

    try:
        
        xmlstring += "<stdyInfo>\n"
        
        xmlstring += "<subject>\n"
        #new: do not use TheSoz anymore 
        
        #GetCAb(Study)                                                                     'neu 2.4 Cessda Topic Classification
        vocab = "CESSDA Topic Classification"
        vocabURI = "https://vocabularies.cessda.eu/v2/vocabularies/TopicClassification/4.0?languageVersion=en-4.0" #new 2.9.5
        vocabURIde = "https://vocabularies.cessda.eu/v2/vocabularies/TopicClassification/4.0?languageVersion=de-4.0.1" #new 2.9.5
        strCAb = ''
        for itm in study["CESSDATopicsEN"]:
            strCAb += '  <topcClas xml:lang="en" vocab="' + vocab + '" vocabURI="' + vocabURI + '">' + itm + '</topcClas>\n'
        
        for itm in study["CESSDATopicsDE"]:
            strCAb += '  <topcClas xml:lang="de" vocab="' + vocab + '" vocabURI="' + vocabURIde + '">' + itm + '</topcClas>\n'
        xmlstring += strCAb
        
        xmlstring += "</subject>\n"


        #abstract and summary
        if study["PurposeEN"] != '':
            xmlstring += '<abstract xml:lang="en" contentType="abstract">' + html_encode(study["PurposeEN"]) + '</abstract>\n'
            if study["AbstractEN"] != '':
                xmlstring += '<abstract xml:lang="en" contentType="mixed">' + html_encode(study["AbstractEN"]) + '</abstract>\n'
        else:
            if study["AbstractEN"] != '':
                xmlstring += '<abstract xml:lang="en" contentType="abstract">' + html_encode(study["AbstractEN"]) + '</abstract>\n'
        if study["PurposeDE"] != '':
            xmlstring += '<abstract xml:lang="de" contentType="abstract">' + html_encode(study["PurposeDE"]) + '</abstract>\n'
            if study["AbstractDE"] != '':
                xmlstring += '<abstract xml:lang="de" contentType="mixed">' + html_encode(study["AbstractDE"]) + '</abstract>\n'
        else:
            if study["AbstractDE"] != '':
                xmlstring += '<abstract xml:lang="de" contentType="abstract">' + html_encode(study["AbstractDE"]) + '</abstract>\n'
                
        
        xmlstring += "<sumDscr>\n"
        
        #strXMLFILE = strXMLFILE & getCollDates(Study)
        #done in ddixml.py : needs update to ColStudies: it uses now COLLECTION EVENTS, not the old COVERAGE
        #find out summary: earliest start and latest end 
        startlist = []
        for itm in study["CollDatesStart"]:
            startdate = itm["Date"]
            startlist.append(startdate)
        endlist = []        
        for itm in study["CollDatesEnd"]:
            enddate = itm["Date"]
            endlist.append(enddate)
        if startlist:
            sumStart = min(startlist)
        else:
            sumStart = ""
        if endlist:
            sumEnd = max(endlist)
        else:
            sumEnd = ""
        
        if sumStart != "":  #prevent empty date attributes
            if sumStart == sumEnd:
                xmlstring +=  '<collDate date="' + str(sumStart) + '" event="single" />\n'
            else:
                xmlstring +=  '<collDate date="' + str(sumStart) + '" event="start" />\n'
                xmlstring +=  '<collDate date="' + str(sumEnd) + '" event="end" />\n'
        

        #strXMLFILE = strXMLFILE & getGeogCovers(Study)                                                               'Geographic Coverages/Nations  
        #If Len(IsoCode) = 2 Then 'for CDC use only 2-letter country items               'todo: no Freetext???
        sNation = ''
        count = 0
        for itm in study["GeoIDs"]:
            if len(itm)==2:
                #add geo 
                #print(itm, study["GeoTitlesEN"][count])
                sNation += '<nation xml:lang="en" abbr="' + itm + '">' + study["GeoTitlesEN"][count] + '</nation>\n'
            count+=1
        xmlstring += sNation 
        

        
        #new CV anlyUnit Unit Type 
        vocab = getVocabInfo("unittype_v2.1") #neue Version von AnalysisUnit
        vocabname = vocab[0]
        vocaburide = vocab[1]
        vocaburien = vocab[2]
        CVName="AnalysisUnit"
        for itm in study["AnalysisUnitsEN"]:
            xmlstring += getCVItem("anlyUnit", "en", itm, vocabname, vocaburien, cvcoll, CVName)
        for itm in study["AnalysisUnitsDE"]:
            xmlstring += getCVItem("anlyUnit", "de", itm, vocabname, vocaburide, cvcoll, CVName)
            
        #'Unit Type Kommentar  
        strKe = html_encode(study["AnalysisUnitFreeEN"] )
        strKd = html_encode(study["AnalysisUnitFreeDE"] )
        if strKe != "": 
            xmlstring += '<anlyUnit xml:lang="en">' + strKe + '</anlyUnit>\n'
        if strKd != "": 
            xmlstring += '<anlyUnit xml:lang="de">' + strKd + '</anlyUnit>\n' 
                
        
        #universe only for SDN
                
        
        #'new CV kindData Kind of Data
        vocab = getVocabInfo("kinddata") 
        vocabname = vocab[0]
        vocaburide = vocab[1]
        vocaburien = vocab[2]
        CVName="KindOfData"
        for itm in study["KindOfDataEN"]:
            xmlstring += getCVItem("dataKind", "en", itm, vocabname, vocaburien, cvcoll, CVName)
        for itm in study["KindOfDataDE"]:
            xmlstring += getCVItem("dataKind", "de", itm, vocabname, vocaburide, cvcoll, CVName)        
        
        #'Kind of Data Kommentar
        strKe = html_encode(study["KindOfDataFreeEN"] )
        strKd = html_encode(study["KindOfDataFreeDE"] )
        if strKe != "": 
            xmlstring += '<dataKind xml:lang="en">' + strKe + '</dataKind>\n'
        if strKd != "": 
            xmlstring += '<dataKind xml:lang="de">' + strKd + '</dataKind>\n' 
        
        
        
        
        
        xmlstring += "</sumDscr>\n"
        xmlstring += "</stdyInfo>\n"
        
        
        
    
    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return xmlstring

def getMethod(study, cvcoll):
    """
    ##########################################################################
    Convert a study to the CDC DDI 2.5 xml - Method 
    input: study object
    ##########################################################################
    """

    xmlstring = ""
    
    
    try:
        xmlstring += "<method>\n"
        xmlstring += "<dataColl>\n"
        
        
        #todo 
        
        
        #'new CV timeMeth Erhebungsdesign 
        vocab = getVocabInfo("timemethod") 
        vocabname = vocab[0]
        vocaburide = vocab[1]
        vocaburien = vocab[2]
        CVName="TypeOfTimeMethod"
        for itm in study["TimeMethsEN"]:
            xmlstring += getCVItem("timeMeth", "en", itm, vocabname, vocaburien, cvcoll, CVName)
        for itm in study["TimeMethsDE"]:
            xmlstring += getCVItem("timeMeth", "de", itm, vocabname, vocaburide, cvcoll, CVName)        
        
        #'Erhebungsdesign Kommentar
        strKe = html_encode(study["TimeMethFreeEN"] )
        strKd = html_encode(study["TimeMethFreeDE"] )
        if strKe != "": 
            xmlstring += '<timeMeth xml:lang="en">' + strKe + '</timeMeth>\n'
        if strKd != "": 
            xmlstring += '<timeMeth xml:lang="de">' + strKd + '</timeMeth>\n' 
        
        
        #new CV sampProc Sampling Procedure 
        vocab = getVocabInfo("samplingprocedure") 
        vocabname = vocab[0]
        vocaburide = vocab[1]
        vocaburien = vocab[2]
        CVName="TypeOfSamplingProcedure"
        for itm in study["SampProcsEN"]:
            xmlstring += getCVItem("sampProc", "en", itm, vocabname, vocaburien, cvcoll, CVName)
        for itm in study["SampProcsDE"]:
            xmlstring += getCVItem("sampProc", "de", itm, vocabname, vocaburide, cvcoll, CVName)        
        
        #'Sampling Procedure Kommentar
        strKe = html_encode(study["SampProcFreeEN"] )
        strKd = html_encode(study["SampProcFreeDE"] )
        if strKe != "": 
            xmlstring += '<sampProc xml:lang="en">' + strKe + '</sampProc>\n'
        if strKd != "": 
            xmlstring += '<sampProc xml:lang="de">' + strKd + '</sampProc>\n' 
        
        #todo
        
        #modeofcoll
        #'new CV collMode Mode Of Collection 
        vocab = getVocabInfo("modecollection") 
        vocabname = vocab[0]
        vocaburide = vocab[1]
        vocaburien = vocab[2]
        CVName="TypeOfDataCollectionMethodology"
        for itm in study["ModeCollsEN"]:
            xmlstring += getCVItem("collMode", "en", itm, vocabname, vocaburien, cvcoll, CVName)
        for itm in study["ModeCollsDE"]:
            xmlstring += getCVItem("collMode", "de", itm, vocabname, vocaburide, cvcoll, CVName)        
        
        #'Mode Of Collection Kommentar
        strKe = html_encode(study["ModeCollFreeEN"] )
        strKd = html_encode(study["ModeCollFreeDE"] )
        if strKe != "": 
            xmlstring += '<collMode xml:lang="en">' + strKe + '</collMode>\n'
        if strKd != "": 
            xmlstring += '<collMode xml:lang="de">' + strKd + '</collMode>\n' 
        
        
        
        
        xmlstring += "</dataColl>\n"
        xmlstring += "</method>\n"
        
    
    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return xmlstring

def getDataAccs(study):
    """
    ##########################################################################
    Convert a study to the CDC DDI 2.5 xml - Data Access 
    input: study object
    ##########################################################################
    """

    xmlstring = ""

    try:
        
        xmlstring += "  <dataAccs>\n"
        xmlstring += "   <useStmt>\n"
        xmlstring += '    <restrctn xml:lang="en">' + study["AccessClass"] + " - " + study["AccessTextEN"] + "</restrctn>\n"        #access class and description
        xmlstring += '    <restrctn xml:lang="de">' + study["AccessClass"] + " - " + study["AccessTextDE"] + "</restrctn>\n"        #Zugangsklasse und Beschreibung
        xmlstring += "   </useStmt>\n"
        xmlstring += "  </dataAccs>\n"
        
    
    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return xmlstring


def dict_study_to_root(study, cvcoll):
    """
    ##########################################################################
    Convert a study to the CDC DDI 2.5 xml
    input: study object
    ##########################################################################
    """

    xmlstring = ""

    try:
    
        #study["No"]
        #study["TitleDE"]
        #study["TitleEN"]
        
        #test html entities
        #study["TitleEN"] += "<testelement/> ze & iufhsdjfbk "
        
        
        #special for Colectica studies: check if StudyNo is in title (first with blank, second without blank)
        titleEN = study["TitleEN"].replace(study["No"]+" ","")
        titleDE = study["TitleDE"].replace(study["No"]+" ","")
        titleEN = titleEN.replace(study["No"],"")
        titleDE = titleDE.replace(study["No"],"") 
    
        #getXMLdocDscr()
        xmlstring += "<docDscr>\n"
        xmlstring += "<citation>\n"
        xmlstring += "<titlStmt>\n"
        xmlstring += '<titl xml:lang="en">DDI study level documentation for study ' + study["No"] + ' '
        xmlstring += html_encode(titleEN) 
        xmlstring += "</titl>\n"                    #only one titl possible here
        xmlstring += "</titlStmt>\n"

        xmlstring += "<rspStmt>\n"
        xmlstring += '<AuthEnty xml:lang="en" affiliation="GESIS">GESIS - Leibniz Institute for the Social Sciences</AuthEnty>\n'
        xmlstring += '<AuthEnty xml:lang="de" affiliation="GESIS">GESIS - Leibniz Institut für Sozialwissenschaften</AuthEnty>\n'
        xmlstring += "</rspStmt>\n"
        
        xmlstring += '<holdings xml:lang="en" URI="https://search.gesis.org/research_data/' + study["No"] + '?lang=en"/>\n' #v0.9.1 remove duplicate ZA
        xmlstring += '<holdings xml:lang="de" URI="https://search.gesis.org/research_data/' + study["No"] + '?lang=de"/>\n' #v0.9.1 remove duplicate ZA       
        
        xmlstring += "</citation>\n"
        xmlstring += "</docDscr>\n"

        
        
        
        #getXMLstdyDscr()
            
        xmlstring += " <stdyDscr>\n"
        
        xmlstring += getCitation(study)
        xmlstring += getStdyInfo(study, cvcoll)
        xmlstring += getMethod(study, cvcoll)
        xmlstring += getDataAccs(study)
        
        xmlstring += " </stdyDscr>\n"
        

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return xmlstring


