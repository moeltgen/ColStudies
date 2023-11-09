"""
    functions to parse ddixml
"""

import util.edxml as ed

############# study object #############


def getnewstudy():
    # Create a new empty study object

    study = {}

    study["ID"] = ""
    study["No"] = ""
    study["DOI"] = ""
    study["Version"] = ""
    study["VersionDate"] = ""
    study["VersionYear"] = ""

    study["AccessClass"] = ""
    study["AccessTextEN"] = ""
    study["AccessTextDE"] = ""

    study["TitleEN"] = ""
    study["TitleDE"] = ""
    study["AlternateTitleEN"] = ""
    study["AlternateTitleDE"] = ""
    study["SubTitleEN"] = ""
    study["SubTitleDE"] = ""

    study["Creators"] = []  # list
    study["Contributors"] = []  # list

    study["Publisher"] = ""
    study["PublicationYear"] = ""
    study["DataURL"] = ""
    study["Availability"] = ""

    study["FurtherRemarksDE"] = ""
    study["FurtherRemarksEN"] = ""
    study["AbstractEN"] = ""
    study["AbstractDE"] = ""
    study["PurposeEN"] = ""
    study["PurposeDE"] = ""

    # List of study groups, in which the study is assigned
    # Attributes are synchronized, so items with same index belong together:
    study["GroupIDs"] = []  # DBK GroupNumbers: GNxxxx
    study["GroupTitlesEN"] = []
    study["GroupTitlesDE"] = []
    study["GroupDescriptionsEN"] = []
    study["GroupDescriptionsDE"] = []
    study["GroupLinksEN"] = []
    study["GroupLinksDE"] = []
    study["GroupLogo"] = []

    # List of study languages
    # Attributes are synchronized, so items with same index belong together:
    study["StudyLanguageIds"] = []  # ISO language codes
    study["StudyLanguageNamesEN"] = []
    study["StudyLanguageNamesDE"] = []
    study["StudyLanguageCountryIds"] = []  # unclear: is ISO, but what is in this list?

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
    study["ModeCollFreeEN"] = ""
    study["ModeCollFreeDE"] = ""
    study["SampProcFreeEN"] = ""
    study["SampProcFreeDE"] = ""
    study["TimeMethFreeEN"] = ""
    study["TimeMethFreeDE"] = ""
    study["AnalysisUnitFreeEN"] = ""
    study["AnalysisUnitFreeDE"] = ""
    study["KindOfDataFreeEN"] = ""
    study["KindOfDataFreeDE"] = ""

    # List of collection dates, may be YYYY or YYYY-MM or YYYY-MM-DD (for StartDate, optional also for EndDate)
    study["CollDatesStart"] = []
    study["CollDatesEnd"] = []

    # List of geographic regions, in which the study is conducted
    # Attributes are synchronized, so items with same index belong together:
    study["GeoIDs"] = []  # ISO nation codes
    study["GeoTitlesEN"] = []
    study["GeoTitlesDE"] = []

    # OtherMaterials: List of downloadable files
    study["OtherMaterials"] = []  # list ob objects

    study["NumberOfUnits"] = ""
    study["AnalysisSystems"] = ""
    study["NumberOfVariables"] = ""

    # Topics
    study["TopicsEN"] = []
    study["TopicsDE"] = []
    study["GroupTopics"] = []  # List of Group topics, unclear????
    study["GroupTopicsDE"] = []  # List of Group topics, unclear????
    study["CESSDATopicsEN"] = []
    study["CESSDATopicsDE"] = []

    study["InstrumentID"] = ""  # Link to Instrument from studyunit

    return study


def ddixml_to_study(ddixml, cvcollection, studyurl):
    """
    ###########################################
    Convert ddixml into a study object
    input: ddixml as returned by Colectica API

    input: cvcollection as cv objects with dicts
    for en/de using codes as key, e.g.:
    CVCollection['Subjects']['ItemsDE'][key]=value
    CVCollection['Subjects']['ItemsEN'][key]=value
    ###########################################
    """

    # Create a new study object: just an empty object or defined study with getnewstudy()
    # study = {}
    study = getnewstudy()

    # Map the ddi properties to the study properties
    root = ed.remove_xml_ns(ddixml)
    xml = (
        "{http://www.w3.org/XML/1998/namespace}"  # no xml: all namespaces were removed
    )

    # IDs
    study["ID"] = ed.getValueFromXPath(root, ".//StudyUnit/ID")
    study["No"] = ed.getValueFromXPath(
        root, './/StudyUnit/UserID[@typeOfUserID="GESIS Study Number"]'
    )

    # do not use DOI at studyunit level, use physicalinstance
    # study['DOI'] = ed.getValueFromXPath(root, './/StudyUnit/UserID[@typeOfUserID="DOI"]')
    # study['Version'] = ed.getAttributeValueFromXPath(root, './/StudyUnit/UserID[@typeOfUserID="DOI"]', 'userIDVersion')

    # these function get the first value, but we need the last (current) DOI/Version:_
    # study['DOI'] = ed.getValueFromXPath(root, './/PhysicalInstance/UserID[@typeOfUserID="DOI"]')
    # study['Version'] = ed.getAttributeValueFromXPath(root, './/PhysicalInstance/UserID[@typeOfUserID="DOI"]', 'userIDVersion')
    # so use the new functions:
    study["DOI"] = ed.getDatasetDOI(ddixml)
    study["Version"] = ed.getDatasetVersion(ddixml)

    pubDate = ed.getValueFromXPath(
        root, ".//PhysicalInstance/Citation/PublicationDate/SimpleDate"
    )
    pubDate = pubDate[0:10]  # only date, no time
    pubYear = pubDate[0:4]  # only year
    study["VersionDate"] = pubDate
    study["VersionYear"] = pubYear

    # AccessClass
    study["AccessClass"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Citation/accessRights", xml + "lang", "de"
    )  # same for both languages
    study["AccessTextEN"] = getAccessClassText(study["AccessClass"], False)
    study["AccessTextDE"] = getAccessClassText(study["AccessClass"], True)

    # Titles
    study["TitleDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Citation/Title/String", xml + "lang", "de"
    )
    study["TitleEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Citation/Title/String", xml + "lang", "en"
    )
    study["AlternateTitleTitleDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Citation/AlternateTitle/String", xml + "lang", "de"
    )
    study["AlternateTitleTitleEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Citation/AlternateTitle/String", xml + "lang", "en"
    )
    study["SubTitleTitleDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Citation/SubTitle/String", xml + "lang", "de"
    )
    study["SubTitleTitleEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Citation/SubTitle/String", xml + "lang", "en"
    )

    # Creators will be filled with Name, FirstName, Affiliation
    study["Creators"] = getCreatorList(
        root,
        ".//StudyUnit/Citation/Creator",
        "CreatorName/String",
        xml + "lang",
        "en",
        "CreatorName",
        "affiliation",
    )

    # Contributors currently not present in ed index, but needed:  // todo: Roles
    study["Contributors"] = getCreatorList(
        root,
        ".//StudyUnit/Citation/Contributor",
        "ContributorName/String",
        xml + "lang",
        "en",
        "ContributorName",
        "affiliation",
    )

    # Publisher
    study[
        "Publisher"
    ] = "GESIS - Leibniz Institute for the Social Sciences"  # fixed value

    # todo: use extra publication year ??
    # study['PublicationYear'] will be filled from PhysicalInstance (fragment must be present in ddixml)
    pubDate = ed.getValueFromXPath(
        root, ".//PhysicalInstance/Citation/PublicationDate/SimpleDate"
    )
    pubDate = pubDate[0:10]  # only date, no time
    pubYear = pubDate[0:4]  # only year
    study["PublicationYear"] = pubYear
    study["PublicationYear"] = pubYear

    # List of collection dates, may be YYYY or YYYY-MM or YYYY-MM-DD (for StartDate, optional also for EndDate)
    study["CollDatesStart"] = getCollDatesList(
        root, ".//StudyUnit/Coverage/TemporalCoverage/ReferenceDate", "StartDate"
    )
    study["CollDatesEnd"] = getCollDatesList(
        root, ".//StudyUnit/Coverage/TemporalCoverage/ReferenceDate", "EndDate"
    )

    # needed for dara and DOI registration:
    # study['DataURL'] = 'https://search.gesis.org/research_data/' + study['No']          #valid and reachable URL needed
    study["DataURL"] = studyurl

    study["Availability"] = "Delivery"  # all studies may be ordered
    if not (
        study["AccessClass"] == "0"
        or study["AccessClass"] == "A"
        or study["AccessClass"] == "B"
        or study["AccessClass"] == "C"
    ):
        study["Availability"] = "NotAvailable"  # not a published study
    if study["AccessClass"] == "0" or study["AccessClass"] == "A":
        study["Availability"] = "Download"  # study data can be downloaded

    # settings required for dara registration: test prefix / DOI / Version / reachable LandingPage
    # study['DOI'] = '10.17889/ZAC0002' # + study['No'] #use test prefix for testing dara registration at https://labs.da-ra.de/dara/study/importXML
    ##Version
    # study['PublicationYear'] = '2023' #start with that one
    # study['DataURL'] = 'https://search.gesis.org/research_data/ZA0002' #valid and reachable URL needed
    # study['Availability'] = 'Unknown' #some setting needed

    # Language dependent content
    study["AbstractDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Abstract/Content", xml + "lang", "de"
    )
    study["AbstractEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Abstract/Content", xml + "lang", "en"
    )

    study["PurposeDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Purpose/Content", xml + "lang", "de"
    )
    study["PurposeEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/Purpose/Content", xml + "lang", "en"
    )

    study["FurtherRemarksDE"] = ed.getValueFromXPathCustomField(
        root, ".//StudyUnit/UserAttributePair", "Weitere Hinweise"
    )
    study["FurtherRemarksEN"] = ed.getValueFromXPathCustomField(
        root, ".//StudyUnit/UserAttributePair", "Further Remarks"
    )

    # extension:InstrumentReferences within DataCollection
    ref = ed.get_referenceFromAttributePair(ddixml, ".//DataCollection")
    if ref is not None:
        study["InstrumentID"] = ref["ID"]

    # More study information from List of CVs
    study["ModeCollsEN"] = getCVTerms(
        root,
        ".//Methodology/DataCollectionMethodology/TypeOfDataCollectionMethodology",
        False,
        cvcollection["TypeOfDataCollectionMethodology"],
    )
    study["ModeCollsDE"] = getCVTerms(
        root,
        ".//Methodology/DataCollectionMethodology/TypeOfDataCollectionMethodology",
        True,
        cvcollection["TypeOfDataCollectionMethodology"],
    )
    study["SampProcsEN"] = getCVTerms(
        root,
        ".//Methodology/SamplingProcedure/TypeOfSamplingProcedure",
        False,
        cvcollection["TypeOfSamplingProcedure"],
    )
    study["SampProcsDE"] = getCVTerms(
        root,
        ".//Methodology/SamplingProcedure/TypeOfSamplingProcedure",
        True,
        cvcollection["TypeOfSamplingProcedure"],
    )
    study["TimeMethsEN"] = getCVTerms(
        root,
        ".//Methodology/TimeMethod/TypeOfTimeMethod",
        False,
        cvcollection["TypeOfTimeMethod"],
    )
    study["TimeMethsDE"] = getCVTerms(
        root,
        ".//Methodology/TimeMethod/TypeOfTimeMethod",
        True,
        cvcollection["TypeOfTimeMethod"],
    )
    study["AnalysisUnitsEN"] = getCVTerms(
        root, ".//StudyUnit/AnalysisUnit", False, cvcollection["AnalysisUnit"]
    )
    study["AnalysisUnitsDE"] = getCVTerms(
        root, ".//StudyUnit/AnalysisUnit", True, cvcollection["AnalysisUnit"]
    )
    study["KindOfDataEN"] = getCVTerms(
        root, ".//StudyUnit/KindOfData", False, cvcollection["KindOfData"]
    )
    study["KindOfDataDE"] = getCVTerms(
        root, ".//StudyUnit/KindOfData", True, cvcollection["KindOfData"]
    )
    # and freetexts
    study["ModeCollFreeEN"] = ed.getValueFromXPathWithAttribute(
        root,
        ".//Methodology/DataCollectionMethodology/Description/Content",
        xml + "lang",
        "en",
    )
    study["ModeCollFreeDE"] = ed.getValueFromXPathWithAttribute(
        root,
        ".//Methodology/DataCollectionMethodology/Description/Content",
        xml + "lang",
        "de",
    )
    study["SampProcFreeEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//Methodology/SamplingProcedure/Description/Content", xml + "lang", "en"
    )
    study["SampProcFreeDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//Methodology/SamplingProcedure/Description/Content", xml + "lang", "de"
    )
    study["TimeMethFreeEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//Methodology/TimeMethod/Description/Content", xml + "lang", "en"
    )
    study["TimeMethFreeDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//Methodology/TimeMethod/Description/Content", xml + "lang", "de"
    )
    study["AnalysisUnitFreeEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/AnalysisUnitsCovered/String", xml + "lang", "en"
    )
    study["AnalysisUnitFreeDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//StudyUnit/AnalysisUnitsCovered/String", xml + "lang", "de"
    )
    study["KindOfDataFreeEN"] = ""  # not supported
    study["KindOfDataFreeDE"] = ""  # not supported

    # ISO nation codes
    study["GeoIDs"] = ed.getListFromXPath(
        root, ".//StudyUnit/Coverage/SpatialCoverage/CountryCode"
    )
    study["GeoTitlesEN"] = getCountryNames(study["GeoIDs"])
    study["GeoTitlesDE"] = []  # todo: is there a library for German country names?

    study["OtherMaterials"] = getOtherMatList(root, ".//OtherMaterial")

    study["NumberOfUnits"] = ed.getValueFromXPath(
        root, ".//PhysicalInstance/GrossFileStructure/CaseQuantity"
    )
    study["AnalysisSystemsEN"] = ed.getValueFromXPathWithAttribute(
        root, ".//PhysicalInstance/Citation/format", xml + "lang", "en"
    )
    study["AnalysisSystemsDE"] = ed.getValueFromXPathWithAttribute(
        root, ".//PhysicalInstance/Citation/format", xml + "lang", "de"
    )

    study["NumberOfVariables"] = str(getCountOfElements(root, ".//Variable"))

    # Topics
    study["TopicsEN"] = ed.getListFromXPath(
        root, ".//StudyUnit/Coverage/TopicalCoverage/Keyword"
    )
    study[
        "TopicsDE"
    ] = []  # todo get German Text from English Text (no CV is used here)

    study["GroupTopics"] = []  # List of Group topics, unclear????
    study["GroupTopicsDE"] = []  # List of Group topics, unclear????

    # study['CESSDATopicsEN'] = getCVTerms(root, './/StudyUnit/Coverage/TopicalCoverage/Subject', False, cvcollection['Subject'])
    # study['CESSDATopicsDE'] = getCVTerms(root, './/StudyUnit/Coverage/TopicalCoverage/Subject', True, cvcollection['Subject'])

    # Groups
    study["GroupIDs"] = ed.getListFromXPath(
        root, './/Group/UserID[@typeOfUserID="GESIS Group Number"]'
    )  # DBK GroupNumbers
    study["GroupTitlesEN"] = ed.getListFromXPathWithAttribute(
        root, ".//Group/Citation/Title", "String", xml + "lang", "en"
    )
    study["GroupTitlesDE"] = ed.getListFromXPathWithAttribute(
        root, ".//Group/Citation/Title", "String", xml + "lang", "de"
    )
    study["GroupDescriptionsEN"] = ed.getListFromXPathWithAttribute(
        root, ".//Group/Abstract", "Content", xml + "lang", "en"
    )
    study["GroupDescriptionsDE"] = ed.getListFromXPathWithAttribute(
        root, ".//Group/Abstract", "Content", xml + "lang", "de"
    )
    study["GroupLinksEN"] = ed.getListFromXPathCustomField(
        root, ".//Group/UserAttributePair", "URL-en"
    )
    study["GroupLinksDE"] = ed.getListFromXPathCustomField(
        root, ".//Group/UserAttributePair", "URL-de"
    )
    # study['GroupLogo'] = ed.getListFromXPathAttributePair(root, './/Group/UserAttributePair', 'extension:ThumbnailImage') #does not work with API, but in Designer xml visible?
    study["GroupLogo"] = ed.getListFromXPathCustomField(
        root, ".//Group/UserAttributePair", "Logo"
    )  # so use custom field instead

    # study language is always in English and German
    LanguageList = []
    LanguageList.append("en")  # if variable documentation in English is available
    LanguageList.append("de")  # if variable documentation in German is available

    study[
        "StudyLanguageIds"
    ] = LanguageList  # ISO language codes 2-letter: in those languages there are questions (associated to variables) available
    study["StudyLanguageNamesEN"] = getLanguageNames(study["StudyLanguageIds"])
    study[
        "StudyLanguageNamesDE"
    ] = []  # todo: is there a library for German country names?
    study[
        "StudyLanguageCountryIds"
    ] = LanguageList  # is ISO language codes, extended by - and a country code for specification (e.g.: de-AT, fr-BE, it-CH)

    return study


############# xml helper functions #############


def getCreatorList(
    node, xpath, subpath, attributename, attributevalue, affiliationpath, affiliationatt
):
    # get a list of items for given xpath, use subpath for value when attribute is given
    # e.g.: (root, './/StudyUnit/Citation/Creator', 'String', xml+'lang', 'en')
    # todo: support Role if used for contributors (not found in Colectica xml?)
    returnlist = []

    userids_all = node.findall(xpath)
    for uid in userids_all:
        # print(str(uid))
        affil = ""
        for item in uid.findall("./" + affiliationpath):
            if affiliationatt in item.attrib:  # get affiliation
                affil = item.attrib[affiliationatt]
        for item in uid.findall("./" + subpath):
            if item.attrib[attributename] == attributevalue:  # get Name
                itemtxt = item.text
                itemdict = {}
                itemparts = itemtxt.split(",", 1)  # split into two
                if len(itemparts) == 2:
                    firstname = itemparts[1].strip()
                    lastname = itemparts[0].strip()
                else:
                    firstname = "-"  # no empty content allowed
                    lastname = itemparts[0].strip()
                itemdict["FirstName"] = firstname
                itemdict["Name"] = lastname
                itemdict["Affiliation"] = affil
                returnlist.append(itemdict)

    return returnlist


def getCollDatesList(node, xpath, subpath):
    # get a list of Dates from TemporalCoverage, StartDate or EndDate

    returnlist = []

    userids_all = node.findall(xpath)
    for uid in userids_all:
        # print(str(uid))
        itemtxt = ""
        for item in uid.findall("./" + subpath):
            itemtxt = item.text
        itemdict = {}
        itemdict["Date"] = itemtxt
        returnlist.append(itemdict)

    return returnlist


def getAccessClassText(accessClass, useGerman):
    # AccessText is fixed, depending on AccessClass
    text = ""
    if accessClass == "0":
        text = "Data and documents are released for everybody."
        if useGerman:
            text = "Daten und Dokumente sind für jedermann freigegeben."
    elif accessClass == "A":
        text = "Data and documents are released for academic research and teaching."
        if useGerman:
            text = "Daten und Dokumente sind für die akademische Forschung und Lehre freigegeben."
    elif accessClass == "B":
        text = "Data and documents are released for academic research and teaching, if the results won’t be published. \
        If any publications or any further work on the results is planned, permission must be obtained by the Data Archive."
        if useGerman:
            text = "Daten und Dokumente sind für die akademische Forschung und Lehre freigegeben, wenn die Ergebnisse nicht veröffentlicht werden. \
        Sollte eine Veröffentlichung oder eine weitergehende Verarbeitung der Ergebnisse geplant sein, ist eine Genehmigung über das Datenarchiv einzuholen."
    elif accessClass == "C":
        text = "Data and documents are only released for academic research and teaching after the data depositor’s written authorization. \
        For this purpose the Data Archive obtains a written permission with specification of the user and the analysis intention."
        if useGerman:
            text = "Daten und Dokumente sind für die akademische Forschung und Lehre nur nach schriftlicher Genehmigung des Datengebers zugänglich. \
        Das Datenarchiv holt dazu schriftlich die Genehmigung unter Angabe des Benutzers und des Auswertungszweckes ein."

    return text


def getCountryNames(countrylist):
    import pycountry
    # for a list of iso codes, get their names and return the list of names
    # using pycountry.countries (ISO 3166)
    # using pycountry.languages (ISO 639-3)

    returnlist = []

    for country in countrylist:
        if len(country) > 2:
            lang = country[3:]
            country = country[0:2]
        else:
            country = country[0:2]
            lang = ""

        cntryName = pycountry.countries.get(alpha_2=country)
        if cntryName is not None:
            # print(country + '  resolved to ' + cntryName.name) # could also use .official_name
            countrytext = cntryName.name
        else:
            countrytext = ""  # not resolved

        cntryLang = pycountry.languages.get(alpha_2=lang)
        if cntryLang is not None:
            # print(lang + '  resolved to ' + cntryLang.name) # could also use .common_name
            appendtext = cntryLang.name + " in "
        else:
            appendtext = ""

        returnlist.append(appendtext + countrytext)

    return returnlist


def getLanguageNames(languagelist):
    import pycountry
    # for a list of iso codes, get their names and return the list of names
    # using pycountry.countries (ISO 3166)
    # using pycountry.languages (ISO 639-3)

    returnlist = []

    for language in languagelist:
        if len(language) > 2:
            country = language[3:]
            language = language[0:2]
        else:
            language = language[0:2]
            country = ""

        langName = pycountry.languages.get(alpha_2=language)
        if langName is not None:
            # print(language + '  resolved to ' + langName.name) # could also use .common_name
            languagetext = langName.name
        else:
            languagetext = ""  # not resolved

        cntryLang = pycountry.countries.get(alpha_2=country)
        if cntryLang is not None:
            # print(country + '  resolved to ' + cntryLang.name) # could also use .official_name
            appendtext = " in " + cntryLang.name
        else:
            appendtext = ""

        returnlist.append(languagetext + appendtext)

    return returnlist


def getOtherMatList(node, xpath):
    # get a list of items for OtherMaterial, using Types:
    # PublishedDocumentationFile
    # UnpublishedDocumentationFile
    # FreeDataFile
    # PublishedDataFile
    # UnpublishedDataFile

    # Example
    # OtherMaterial = {}
    # OtherMaterial["title-en"] = "ZA3440_Notes.pdf (Remarks)"
    # OtherMaterial["id"] = "ZA3440_OthMat13122"
    # OtherMaterial["type"] = "Remarks"
    # OtherMaterial["title-de"] = "ZA3440_Notes.pdf (Anmerkungen)"
    # OtherMaterial["external-url"] = "https://dbk.gesis.org/dbksearch/download.asp?id=13122"
    # study['OtherMaterials'].append(OtherMaterial)

    xml = (
        "{http://www.w3.org/XML/1998/namespace}"  # no xml: all namespaces were removed
    )

    returnlist = []

    userids_all = node.findall(xpath)
    for uid in userids_all:
        omtype = ""
        for item in uid.findall("./TypeOfMaterial"):
            omtype = item.text

        if (
            omtype == "PublishedDocumentationFile"
            or omtype == "PublishedDataFile"
            or omtype == "FreeDataFile"
        ):
            titlede = ""
            titleen = ""
            for item in uid.findall("./Citation/Title/String"):
                if item.attrib[xml + "lang"] == "de":
                    titlede = item.text
                if item.attrib[xml + "lang"] == "en":
                    titleen = item.text
            itemdict = {}
            itemdict["title-en"] = titleen
            itemdict["id"] = uid.find("./ID").text
            itemdict["type"] = uid.find("./MIMEType").text
            itemdict["title-de"] = titlede
            itemdict["external-url"] = uid.find("./ExternalURLReference").text
            returnlist.append(itemdict)

    return returnlist


def getCountOfElements(node, xpath):
    # count the number of items for given xpath

    userids_all = node.findall(xpath)
    count = 0
    if userids_all is not None:
        count = len(userids_all)

    return count


def get_cvinfo(ddixml, itemxpath):
    """
    ###########################################
    Get get Agency,ID,Version for referenced item, e.g. physicalinstance
    input: ddixml as returned by Colectica API for study
    and xpath for item, e.g. './/StudyUnit/Coverage/TopicalCoverage/Subject'

    controlledVocabularyID="13e2670a-e28a-455b-a6fb-c6cca95e6dc8"
    controlledVocabularyAgencyName="de.gesis"
    controlledVocabularyVersionID="1"

    ###########################################
    """

    # Map the ddi properties to the study properties
    root = ed.remove_xml_ns(ddixml)
    xml = (
        "{http://www.w3.org/XML/1998/namespace}"  # no xml: all namespaces were removed
    )

    ref = {}
    ref["Agency"] = ""
    ref["ID"] = ""
    ref["Version"] = ""

    # Get properties
    ref["Agency"] = ed.getAttributeValueFromXPath(
        root, itemxpath, "controlledVocabularyAgencyName"
    )
    ref["ID"] = ed.getAttributeValueFromXPath(root, itemxpath, "controlledVocabularyID")
    ref["Version"] = ed.getAttributeValueFromXPath(
        root, itemxpath, "controlledVocabularyVersionID"
    )

    return ref


def getCVTerms(node, xpath, useGerman, cvcollitem):
    # get a list of used CV codes and their text
    # e.g. a list of CESSDA Topics and look up the German or English text for the given code
    # e.g.: './/StudyUnit/Coverage/TopicalCoverage/Subject'
    # cvcollitem contains used CV: e.g. cvcollection['Subject']

    returnlist = []

    # get list of codes
    topiclist = ed.getListFromXPath(node, xpath)

    for topic in topiclist:
        # for each code, get language specific term
        if useGerman:
            itemtxt = cvcollitem["ItemsDE"][topic]
        else:
            itemtxt = cvcollitem["ItemsEN"][topic]
        # print(topic, itemtxt)
        returnlist.append(itemtxt)

    return returnlist


def ddixml_to_var(ddixml, Limit, vagency="", vid="", vversion=""):
    # import edindex as ed

    """
    ###########################################
    Convert ddixml into a var object  
    input: ddixml for complete study as returned by Colectica API
    input optional: filter for variable varid, varagency, varversion
    ###########################################
    """

    # create a list of variables
    varlist = []

    #
    # Map the ddi properties to the variable properties
    #

    root = ed.remove_xml_ns(ddixml)  # complete study xml
    xml = (
        "{http://www.w3.org/XML/1998/namespace}"  # no xml: all namespaces were removed
    )

    # get a list of referenced variables
    reflist = ed.get_referencelist(
        ddixml,
        ".//DataRelationship/LogicalRecord/VariablesInRecord/VariableUsedReference",
    )
    i = 1
    for ref in reflist:
        processVariable = False
        if not (vagency == "" or vid == "" or vversion == ""):
            if (
                vagency == ref["Agency"]
                and vid == ref["ID"]
                and vversion == ref["Version"]
            ):
                processVariable = True
        else:
            processVariable = True

        if processVariable:
            varAgency = ref["Agency"]
            varID = ref["ID"]
            varVersion = ref["Version"]

            # Select this variable
            URNCondition = (
                '[URN="urn:ddi:' + varAgency + ":" + varID + ":" + varVersion + '"]'
            )
            xpath = ".//Variable" + URNCondition
            variablenode = root.find(xpath)
            if variablenode is not None:
                # Create a new variable object: just an empty object or defined variable with getnewvariable()
                variable = {}
                # variable = getnewvariable()

                # added WZM
                # variable['Agency'] = ref['Agency']
                # variable['ID'] = ref['ID']
                # variable['Version'] = ref['Version']

                # IDs
                # varName = getValueFromXPath(root, './/Variable/VariableName/String')
                varName = getValueFromXPath(variablenode, ".//VariableName/String")
                variable["ID"] = varName
                variable["Name"] = varName
                variable["LabelEN"] = getValueFromXPathWithAttribute(
                    variablenode, ".//Label/Content", xml + "lang", "en"
                )
                variable["LabelDE"] = getValueFromXPathWithAttribute(
                    variablenode, ".//Label/Content", xml + "lang", "de"
                )

                # already set:
                # varAgency = getValueFromXPath(variablenode, './/Agency')
                # varID = getValueFromXPath(variablenode, './/ID')
                # varVersion = getValueFromXPath(variablenode, './/Version')

                # var['Position']        #sequence in dataset is set on study level when processing all referenced variables
                variable["Position"] = i

                # Notes
                variable["NoteTextEN"] = getValueFromXPathWithAttribute(
                    variablenode, ".//Description/Content", xml + "lang", "en"
                )  # ArchiveNote en
                variable["RemarkTextEN"] = getValueFromXPathCustomField(
                    variablenode, ".//UserAttributePair", "Remark"
                )  # RemarkText en
                variable["DerivationTextEN"] = getValueFromXPathCustomField(
                    variablenode, ".//UserAttributePair", "Derivation"
                )  # Derivation en
                variable["NoteTextDE"] = getValueFromXPathWithAttribute(
                    variablenode, ".//Description/Content", xml + "lang", "de"
                )  # ArchiveNote de
                variable["RemarkTextDE"] = getValueFromXPathCustomField(
                    variablenode, ".//UserAttributePair", "Anmerkung"
                )  # RemarkText de
                variable["DerivationTextDE"] = getValueFromXPathCustomField(
                    variablenode, ".//UserAttributePair", "Ableitung"
                )  # Derivation de

                # Question: QuestionGrid or QuestionItem
                # not here: variable['Question']= question

                # Values + Labels
                # CodeValues and CategoryLabels
                variable["Values"] = []  # start with empty list
                xpath = (
                    ".//Variable"
                    + URNCondition
                    + "/VariableRepresentation/CodeRepresentation/CodeListReference"
                )
                ref = ed.get_reference(ddixml, xpath)
                if ref is not None:
                    # Select this CodeListReference
                    variable["Values"] = getVarValuesList(
                        ddixml, ref["Agency"], ref["ID"], ref["Version"]
                    )
                    variable["CodeListID"] = ref["ID"]

                # variable complete
                varlist.append(variable)

            if i == Limit:
                print("Limited to " + str(Limit) + " variables for testing")
                break
            i += 1
    return varlist
