"""
    Provide information for the dara xml
"""
import io
import xml.etree.ElementTree as ET
import json
import globalvars as g
import traceback 
import requests
import util.ddixml as ddi #moved to util folder 


def write_daraxml_fromddixml(filename, ddixml, cvcoll, studyurl):
    """
    Builds the dara xml as tree and writes it into file 
    pro: error if not well-formed
    con: no comments
    """
    try:
        tree = get_daraxml_tree_fromddixml(ddixml, cvcoll, studyurl)
        f = open(filename, "w", encoding="utf-8")
        tree.write(f, encoding='unicode', xml_declaration=True, default_namespace='http://da-ra.de/schema/kernel-4')
        f.close()
    
    except Exception as e: 
        print('Error in ' + __file__)
        print('Error '+str(e))        
        print(traceback.format_exc())


def get_daraxml_tree_fromddixml(ddixml, cvcoll, studyurl):
    """
    Builds and returns the dara xml as tree, uses ddi xml as input  
    """
    
    tree = ET.ElementTree()
    
    try:
        xmlstring = ''
        xmlstring += header('', '')  #todo: info object has no English Title
        study = ddi.ddixml_to_study(ddixml, cvcoll, studyurl)
        
        #if DOI should be replaced by DOI in settings
        if not g.daradoiprefix=='':
            StudyDOI = study['DOI']
            StudyDOIparts = StudyDOI.split('/')
            StudyDOI = g.daradoiprefix + '/' + StudyDOIparts[1]
            study['DOI'] = StudyDOI
            
        xmlstring += dict_study_to_root(study)
        xmlstring += footer()  
        
        tree = ET.ElementTree(ET.fromstring(xmlstring)) 
        
    except Exception as e: 
        print('Error in ' + __file__)
        print('Error '+str(e))        
        print(traceback.format_exc())

    return tree

def header(title_en, title_de):
    """
    Returns the dara xml header 
    """
        
    xmlstring = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
    xmlstring += '<!-- erstellt von W. Zenk-Moeltgen, 01.12.2017 -->\n'
    xmlstring += '<!-- aus DBKEdit am 16.02.2023           -->\n'
    xmlstring += '<resource xmlns="http://da-ra.de/schema/kernel-4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.da-ra.de/dara/schemadefinitions/dara.xsd">\n'
    xmlstring += '<!--\n'
    xmlstring += 'da|ra 4.0 Documentation for Study \''+ title_en + '\'\n'
    xmlstring += '-->\n'
    xmlstring += '<!--\n'
    xmlstring += 'da|ra 4.0 Dokumentation für Studie \''+ title_de + '\'\n'
    xmlstring += '-->\n'
    xmlstring += ''    
    return xmlstring

def footer():
    """
    Returns the dara xml footer 
    """
    xmlstring = '</resource>\n'
    return xmlstring
    


def dict_study_to_root(study):
    """
    ##########################################################################
    Convert a study to the dara ressource xml 
    input: study object
    ##########################################################################
    """
    
    xmlstring = ''
    
    try:
        xmlstring += ' <resourceType>Dataset</resourceType>\n'      #fixed value 
        
        xmlstring += ' <resourceIdentifier>\n'
        xmlstring += '  <identifier>' + study['No'] + '</identifier>\n' #new use StudyNo here 
        xmlstring += '  <currentVersion>' + study['Version'] + '</currentVersion>\n'    
        xmlstring += ' </resourceIdentifier>\n'
        
        xmlstring += ' <titles>\n'
        xmlstring += '  <title>\n'
        xmlstring += '   <language>de</language>\n'
        xmlstring += '   <titleName>' + study['TitleDE'] + '</titleName>\n'
        xmlstring += '  </title>\n'
        xmlstring += '  <title>\n'
        xmlstring += '   <language>en</language>\n'
        xmlstring += '   <titleName>' + study['TitleEN'] + '</titleName>\n'
        xmlstring += '  </title>\n'
        xmlstring += ' </titles>\n'
        
        
        
        #creator = info['Citation']['creator']            #todo: info object has no First, Middle, LastName 
        #creator = info['Citation']['creator']            #todo: institution
        
        xmlstring += ' <creators>\n'
        for itm in study['Creators']:
            xmlstring += '  <creator>\n'
            xmlstring += '   <person>\n'
            xmlstring += '    <firstName>' + itm['FirstName'] + '</firstName>\n'
            xmlstring += '    <middleName></middleName>\n'
            xmlstring += '    <lastName>' + itm['Name'] + '</lastName>\n'
            if itm['Affiliation']!='':
                xmlstring += '     <affiliation>\n'
                xmlstring += '      <affiliationName>' + itm['Affiliation'] + '</affiliationName>\n'
                xmlstring += '     </affiliation>\n'
            xmlstring += '   </person>\n'
            xmlstring += ' </creator>\n'
            #xmlstring += '  <creator>\n'
            #xmlstring += '   <institution>\n'
            #xmlstring += '    <institutionName>' + institution + '\n'
            #xmlstring += ' </institutionName>\n'
            #xmlstring += '   </institution>\n'
            #xmlstring += ' </creator>\n'
        
        xmlstring += ' </creators>\n'

        #settings required for dara registration 
        xmlstring += ' <dataURLs>\n'
        xmlstring += '  <dataURL>' + study['DataURL'] + '</dataURL>\n'
        xmlstring += ' </dataURLs>\n'
        xmlstring += ' <doiProposal>' + study['DOI'] + '</doiProposal>\n'
        xmlstring += ' <publicationDate>\n'
        xmlstring += '  <year>' + study['PublicationYear'] + '</year>\n'
        xmlstring += ' </publicationDate>\n'
        xmlstring += ' <availability>\n'
        xmlstring += '  <availabilityType>' + study['Availability'] + '</availabilityType>\n'
        xmlstring += ' </availability>\n'
        
        
        
        
        

        xmlstring += ' <descriptions>\n'
        xmlstring += '  <description>\n'
        xmlstring += '   <language>de</language>\n'
        xmlstring += '   <freetext>' + study['AbstractDE'] + '</freetext>\n'
        xmlstring += '   <descriptionType>Abstract</descriptionType>\n' # fixed value 
        xmlstring += '  </description>\n'
        xmlstring += '  <description>\n'
        xmlstring += '   <language>en</language>\n'
        xmlstring += '   <freetext>' + study['AbstractEN'] + '</freetext>\n'
        xmlstring += '   <descriptionType>Abstract</descriptionType>\n' # fixed value 
        xmlstring += '  </description>\n'
        xmlstring += ' </descriptions>\n'
        
        xmlstring += ' <notes>\n'
        xmlstring += '  <note>\n'
        xmlstring += '   <language>de</language>\n'
        xmlstring += '   <text>' + study['FurtherRemarksDE'] + '</text>\n'
        xmlstring += '  </note>\n'
        xmlstring += '  <note>\n'
        xmlstring += '   <language>en</language>\n'
        xmlstring += '   <text>' + study['FurtherRemarksEN'] + '</text>\n'
        xmlstring += '  </note>\n'
        xmlstring += ' </notes>\n'
    
    except Exception as e: 
        print('Error in ' + __file__)
        print('Error '+str(e))        
        print(traceback.format_exc())
    
    return xmlstring
    

def register_dara(daraxmlfile, daraapi, username, password):
    """
    register the DOI/Version of the given xml at dara
    """
    returnmsg = ''
    
    try:

        daraheaders = {"Content-Type": "application/xml;charset=UTF-8"}
        
        #get dara xml from file 
        with io.open(daraxmlfile,'r',encoding='utf8') as f:
            daraxml = f.read()

        #do a POST request 
        response = requests.post(daraapi, data=daraxml.encode('utf8'), headers=daraheaders, auth=(username, password), verify=False)
        
        if response.status_code==200 or response.status_code==201:
            #print('OK or Created: ' + str(response.status_code) )
            returnmsg += ('OK or Created: ' + str(response.status_code) +'\n')
        else:
            #print('Error Status: ' + str(response.status_code) )
            returnmsg += ('Error Status: ' + str(response.status_code) +'\n')
                
        #try to parse json response 
        try:
            isError=False
            jsonResponse = response.json()
            for item in jsonResponse:
                if item=='errors':
                    isError=True
            if isError:
                print('Result: ERROR!')
            else:
                print('Result: Success')
            #print(str(jsonResponse))
            returnmsg += (str(jsonResponse)+'\n')
                    
        except ValueError:
            # no JSON returned
            #print('no JSON returned')
            returnmsg += ('no JSON returned'+'\n')

    except Exception as e: 
        print('Error in ' + __file__)
        print('Error '+str(e))        
        print(traceback.format_exc())

    return returnmsg 

