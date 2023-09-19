"""
    Provide information for the ExploreData xml functions  
"""

from io import StringIO
import xml.etree.ElementTree as ET
import json
import colecticaapi as c 


########################################################
# Utility functions for xml
########################################################

def get_reference(ddixml, itemxpath):
    """
    ###########################################
    Get get Agency,ID,Version for referenced item, e.g. physicalinstance
    input: ddixml as returned by Colectica API for study
    and xpath for item, e.g. './/StudyUnit/PhysicalInstanceReference'
    ###########################################
    """
    
    #Map the ddi properties to the study properties 
    root = remove_xml_ns(ddixml)
    xml = '{http://www.w3.org/XML/1998/namespace}' #no xml: all namespaces were removed    
    
    ref = {}
    ref['Agency'] = ''
    ref['ID'] = ''
    ref['Version'] = ''
    
    #Get properties 
    ref['Agency'] = getValueFromXPath(root, itemxpath +'/Agency')
    ref['ID'] = getValueFromXPath(root, itemxpath +'/ID')
    ref['Version'] = getValueFromXPath(root, itemxpath +'/Version')
    
                
    return ref

def get_referencelist(ddixml, itemxpath):
    """
    ###########################################
    Get get Agency,ID,Version for a list of referenced items, e.g. RelatedOtherMaterialReference
    input: ddixml as returned by Colectica API for study
    and xpath for item, e.g. './/StudyUnit/RelatedOtherMaterialReference'
    ###########################################
    """
    
    #Map the ddi properties to the study properties 
    root = remove_xml_ns(ddixml)
    xml = '{http://www.w3.org/XML/1998/namespace}' #no xml: all namespaces were removed    
    
    reflist = []
    
    #Get properties lists
    alist = getListFromXPath(root, itemxpath +'/Agency')
    ilist = getListFromXPath(root, itemxpath +'/ID')
    vlist = getListFromXPath(root, itemxpath +'/Version')
    
    #build list items 
    i = 0
    for itm in ilist:
        ref = {}
        ref['Agency'] = alist[i]
        ref['ID'] = itm
        ref['Version'] = vlist[i]
        reflist.append(ref)
        i += 1
                
    return reflist

def get_referenceFromAttributePair(ddixml, itemxpath):
    """
    ###########################################
    Get get Agency,ID,Version for referenced item, e.g. extension:InstrumentReferences
    input: ddixml as returned by Colectica API for study
    and xpath for item, e.g. './/StudyUnit/DataCollection'
    ###########################################
    """
    import ast
    
    #Map the ddi properties to the study properties 
    root = remove_xml_ns(ddixml)
    xml = '{http://www.w3.org/XML/1998/namespace}' #no xml: all namespaces were removed    
    
    ref = {}
    ref['Agency'] = ''
    ref['ID'] = ''
    ref['Version'] = ''
    
    #Get properties 
    urnliststring = getValueFromXPathAttributePair(root, itemxpath+'/UserAttributePair', 'extension:InstrumentReferences')
    if urnliststring  is None: return ref 
    urnlist = ast.literal_eval(urnliststring)
    if urnlist is None: return ref 
    if urnlist[0] is None: return ref 
        
    urnparts = urnlist[0].split(':')
    
    if urnparts[2] is None: return ref 
    if urnparts[3] is None: return ref 
    if urnparts[4] is None: return ref 
    
    urnAgency = urnparts[2]
    urnId = urnparts[3]
    urnVersion = urnparts[4]

    ref['Agency'] = urnAgency
    ref['ID'] = urnId
    ref['Version'] = urnVersion
    
    return ref

                                    

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
    
    #Map the ddi properties to the study properties 
    root = remove_xml_ns(ddixml)
    xml = '{http://www.w3.org/XML/1998/namespace}' #no xml: all namespaces were removed    
    
    ref = {}
    ref['Agency'] = ''
    ref['ID'] = ''
    ref['Version'] = ''
    
    #Get properties 
    ref['Agency'] = getAttributeValueFromXPath(root, itemxpath, 'controlledVocabularyAgencyName')
    ref['ID'] = getAttributeValueFromXPath(root, itemxpath, 'controlledVocabularyID')
    ref['Version'] = getAttributeValueFromXPath(root, itemxpath, 'controlledVocabularyVersionID')    
                
    return ref
    
def getValueFromXPath(node, xpath):
    #get a single (first item) value for given xpath
    userids_all = node.findall(xpath)
    for uid in userids_all:
        return uid.text
    return '' #default empty
    
def getListFromXPath(node, xpath):
    #get a list of items for given xpath, use subpath for value when attribute is given
    #e.g.: (root, './/StudyUnit/Citation/Creator', 'String', xml+'lang', 'en')  
    returnlist = []
    
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        itemtxt = uid.text
        returnlist.append(itemtxt)
        
    return returnlist 

def getAttributeValueFromXPath(node, xpath, attribute):
    #get a single attribute value for given xpath with attribute
    userids_all = node.findall(xpath)
    for uid in userids_all:
        if not uid.attrib[attribute] is None:
            return uid.attrib[attribute]
    return '' #default empty

def getValueFromXPathAttributePair(node, xpath, label):
    #get an AttributeValue for given xpath with UserAttributePair, having label as extension
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        if uid.find('./AttributeKey') != None:
            if uid.find('./AttributeKey').text==label:
                jsonvalue = uid.find('./AttributeValue').text 
                return jsonvalue


def getValueFromXPathWithAttribute(node, xpath, attributename, attributevalue):
    #get a single (first item) value for given xpath when attribute is given 
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        if uid.attrib[attributename]==attributevalue:
            return uid.text
    return '' #default empty            
            
def getListFromXPathWithAttribute(node, xpath, subpath, attributename, attributevalue):
    #get a list of items for given xpath, use subpath for value when attribute is given
    #e.g.: (root, './/StudyUnit/Citation/Creator', 'String', xml+'lang', 'en')  
    returnlist = []
    
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        #print(str(uid))
        for item in uid.findall('./'+subpath):
            if item.attrib[attributename]==attributevalue:
                itemtxt = item.text
                #itemdict = {}
                #itemdict['Name']=itemtxt
                #returnlist.append(itemdict)
                returnlist.append(itemtxt)
        
    return returnlist 

def getValueFromSubPathWithXPathWithAttribute(node, xpath, subpath, attributename, attributevalue):
    #get a single (first item) value for given xpath+subpath, if attribute is given on xpath 
    #e.g.: (questionnode, './/QuestionText', 'LiteralText/Text', 'audienceLanguage', 'en')  
    
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        if uid.attrib[attributename]==attributevalue:
            for item in uid.findall('./'+subpath):
                itemtxt = item.text
                return itemtxt
                
    return '' #default empty

def getValueFromXPathCustomField(node, xpath, label):
    #get an AttributeValue for given xpath with UserAttributePair, using customField
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        if uid.find('./AttributeKey') != None:
            if uid.find('./AttributeKey').text=='extension:CustomField':
                jsonvalue = uid.find('./AttributeValue').text 
                j = json.loads(jsonvalue)
                if j['DisplayLabel']==label:
                    return j['StringValue']
    return '' #default empty 

def getListFromXPathCustomField(node, xpath, label):
    #get a list of AttributeValue for given xpath with UserAttributePair, using customField
    returnlist = []
    
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        if uid.find('./AttributeKey') != None:
            if uid.find('./AttributeKey').text=='extension:CustomField':
                jsonvalue = uid.find('./AttributeValue').text 
                j = json.loads(jsonvalue)
                if j['DisplayLabel']==label:
                    itemtxt = j['StringValue']
                    #itemdict = {}
                    #itemdict['Name']=j['StringValue']
                    returnlist.append(itemtxt)
                
    return returnlist
                    
def getListFromXPathAttributePair(node, xpath, label):
    #get a list of AttributeValue for given xpath with UserAttributePair, having label as extension
    returnlist = []
    
    userids_all = node.findall(xpath)  
    for uid in userids_all:
        if uid.find('./AttributeKey') != None:
            if uid.find('./AttributeKey').text==label:
                jsonvalue = uid.find('./AttributeValue').text 
                itemdict = {}
                itemdict['Name']=jsonvalue
                returnlist.append(itemdict)
                
    return returnlist


















                
def getStudyNo(ddixml):
    """
    Get a study number from the DDI xml 
    """
    StudyNo = ''
    
    root = remove_xml_ns(ddixml)
    
    userids_all = root.findall('.//StudyUnit/UserID[@typeOfUserID="GESIS Study Number"]')
    for uid in userids_all:
        StudyNo = uid.text
            
    return StudyNo

def getStudyDOI(ddixml):
    """
    Get a study DOI from the DDI xml 
    """
    StudyDOI = ''
    
    root = remove_xml_ns(ddixml)
    
    userids_all = root.findall('.//StudyUnit/UserID[@typeOfUserID="DOI"]')
    for uid in userids_all:
        StudyDOI = uid.text
            
    return StudyDOI    

def getStudyVersion(ddixml):
    """
    Get a study version to a DOI from the DDI xml 
    """
    StudyVersion = ''
    
    root = remove_xml_ns(ddixml)
    
    userids_all = root.findall('.//StudyUnit/UserID[@typeOfUserID="DOI"]')
    for uid in userids_all:
        if 'userIDVersion' in uid.attrib:
            StudyVersion = uid.attrib['userIDVersion'] #@userIDVersion
            
    return StudyVersion    

def getDatasetDOI(ddixml):
    """
    Get a DOI from the DDI xml of PhysicalInstance 
    """
    DatasetDOI = ''
    
    root = remove_xml_ns(ddixml)
    
    userids_all = root.findall('.//PhysicalInstance/UserID[@typeOfUserID="DOI"]')
    for uid in userids_all:
        DatasetDOI = uid.text
            
    return DatasetDOI    

def getDatasetVersion(ddixml):
    """
    Get a version to a DOI from the DDI xml of PhysicalInstance
    """
    DatasetVersion = ''
    
    root = remove_xml_ns(ddixml)
    
    userids_all = root.findall('.//PhysicalInstance/UserID[@typeOfUserID="DOI"]')
    for uid in userids_all:
        if 'userIDVersion' in uid.attrib:
            DatasetVersion = uid.attrib['userIDVersion'] #@userIDVersion
            
    return DatasetVersion    

def getVersion(ddixml):
    """
    Get a version (DDI) for the study from the xml 
    """
    Version = ''
    
    root = remove_xml_ns(ddixml)
    
    userids_all = root.findall('.//StudyUnit/Version')
    for uid in userids_all:
        Version = uid.text
            
    return Version    


def getStudyTitle(ddixml, lang):
    """
    Get a study title to a DOI from the DDI xml 
    """
    StudyTitle = ''
    
    root = remove_xml_ns(ddixml)
    xml = '{http://www.w3.org/XML/1998/namespace}' #no xml: all namespaces were removed
    
    userids_all = root.findall('.//StudyUnit/Citation/Title/String')
    for uid in userids_all:
        if xml+'lang' in uid.attrib:
            if uid.attrib[xml+'lang']==lang:
                StudyTitle = uid.text
            
    return StudyTitle    


def getAbstract(ddixml, lang):
    """
    Get a study title to a DOI from the DDI xml 
    """
    Abstract = ''
    
    root = remove_xml_ns(ddixml)
    xml = '{http://www.w3.org/XML/1998/namespace}' #no xml: all namespaces were removed
    
    userids_all = root.findall('.//StudyUnit/Abstract/Content')
    for uid in userids_all:
        if xml+'lang' in uid.attrib:
            if uid.attrib[xml+'lang']==lang:
                Abstract = uid.text
            
    return Abstract    


def buildCV(ddixml, xpath, Limit):
    """
    build a CV dictionary from the ddixml for the given xpath
     Limit as max items for debugging
     (not using C as ColecticaObject)
    """
    
    CV = {}
    
    ##get CV e.g. used in Subject (from first item)
    ##using attributes, e.g. controlledVocabularyID                            
    #controlledVocabularyID="13e2670a-e28a-455b-a6fb-c6cca95e6dc8" 
    #controlledVocabularyAgencyName="de.gesis" 
    #controlledVocabularyVersionID="1"
    ref = get_cvinfo(ddixml, xpath)
    #print(ref)
    CV['Agency']=ref['Agency']
    CV['ID']=ref['ID']
    CV['Version']=ref['Version']
    cvxml=''
    addxml=''
    itm = c.get_an_item_version(ref['Agency'], ref['ID'], ref['Version'])
    if itm is not None:
        if 'Item' in itm[1]:
            addxml=itm[1]['Item']
            #do not add here: combined_xml[Id] += '\n' + addxml
            cvxml = addxml
            #print('CV found for '+xpath)
    
    CVItems = {} #dict for items 
    CVItemsEN = {} #dict for English
    CVItemsDE = {} #dict for German

    if not cvxml=='':
        root = remove_xml_ns(cvxml)
        codes = root.findall('.//Code') #allow any level here, do not use './/CodeList/Code'
        for code in codes:
            value = code.find('./Value').text
            catref = code.find('./CategoryReference/ID').text
            CVItem = {}
            CVItem['Value'] = value
            CVItem['Catref'] = catref
            CVItems[catref] = value 
    
    
        ##CategoryReferences within CodeList, ALL LEVELS 
        addxml=''
        reflist = get_referencelist(cvxml, './/Code/CategoryReference')
        i = 1 
        for ref in reflist:
            #print(ref['Agency'], ref['ID'], ref['Version'])
            CVItem = {}
            if i >= Limit: #to avoid key error later 
                key = ref['ID']
                value = CVItems[key] #get value from previous dict 
                CVItemsEN[value] = '' 
                CVItemsDE[value] = '' 
            else:
                itm = c.get_an_item_version(ref['Agency'], ref['ID'], ref['Version'])
                if itm is not None:
                    if 'Item' in itm[1]:
                        addxml=itm[1]['Item']
                        #do not add here: combined_xml[Id] += '\n' + addxml
                        cvlevel1xml = addxml
                #for each category
                if cvlevel1xml is not None:
                    root = remove_xml_ns(cvlevel1xml)
                    xml = '{http://www.w3.org/XML/1998/namespace}' #no xml: all namespaces were removed
                    key = ref['ID']
                    value = CVItems[key] #get value from previous dict 
                    #print(cvlevel1xml)
                    texten = root.find('.//Category/Label/Content[@'+xml+'lang="en"]').text 
                    textde = root.find('.//Category/Label/Content[@'+xml+'lang="de"]').text 
                    CVItemsEN[value] = texten 
                    CVItemsDE[value] = textde 
                    #print(value, textde)
            if i == Limit:
                print('Limited to '+str(Limit)+' CV codes for testing: CV for '+xpath)
                #break
            i += 1    
    
    #finally add the dicts to the CV, and the CV to the CVCollection
    CV['Items']=CVItems
    CV['ItemsDE']=CVItemsDE
    CV['ItemsEN']=CVItemsEN    
    
    return CV 
    
    
def remove_xml_ns(xml):
    """
    Read xml from string, remove namespaces, return root
    """
    it = ET.iterparse(StringIO(xml))
    for _, el in it:
        prefix, has_namespace, postfix = el.tag.partition('}')
        if has_namespace:
            el.tag = postfix  # strip all namespaces
    root = it.root
    return root

