"""
    CDCStudies application
"""



import os
import sys
import traceback
import json
import globalvars as g
module_dir = os.path.abspath('../ColStudies/web') 
sys.path.append(module_dir)
import colecticaapi as c
import util.edxml as ed
import cdc


def getCVCollection(ddixml, methxml):
    """
    build the CVCollection object to hold all Controlled Vocabularies
    """

    # Limit = 3 #temp for development
    Limit = 9999  # for production

    CVCollection = {}

    try:
        # Subjects
        CV = ed.buildCV(ddixml, ".//StudyUnit/Coverage/TopicalCoverage/Subject", Limit)
        CVCollection["Subject"] = CV

        if not methxml == "":
            # TypeOfDataCollectionMethodology
            CV = ed.buildCV(
                methxml,
                ".//Methodology/DataCollectionMethodology/TypeOfDataCollectionMethodology",
                Limit,
            )
            CVCollection["TypeOfDataCollectionMethodology"] = CV

            # TypeOfSamplingProcedure
            CV = ed.buildCV(
                methxml,
                ".//Methodology/SamplingProcedure/TypeOfSamplingProcedure",
                Limit,
            )
            CVCollection["TypeOfSamplingProcedure"] = CV

            # TypeOfTimeMethod
            CV = ed.buildCV(
                methxml, ".//Methodology/TimeMethod/TypeOfTimeMethod", Limit
            )
            CVCollection["TypeOfTimeMethod"] = CV
        else:
            CVCollection["TypeOfDataCollectionMethodology"] = []
            CVCollection["TypeOfSamplingProcedure"] = []
            CVCollection["TypeOfTimeMethod"] = []

        # AnalysisUnit
        CV = ed.buildCV(ddixml, ".//StudyUnit/AnalysisUnit", Limit)
        CVCollection["AnalysisUnit"] = CV

        # KindOfData
        CV = ed.buildCV(ddixml, ".//StudyUnit/KindOfData", Limit)
        CVCollection["KindOfData"] = CV

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return CVCollection


def get_cdcxml(agency, Id):
    """
    get the cdd xml for a study with metadata from the Colectica API
    """

    try:
        cdcxml = ""

        myddixml = {}
        combined_xml = {}
        
        
        StudyDOI = ""
        StudyNo = ""
        
        result = c.get_an_item(agency, Id)
        if str(result[0]) == "200":
            print("Study found: " + Id)
            Version = result[1]["Version"]
            if result[1]["Item"] is not None:
                myddixml[Id] = result[1]["Item"]

                # build the combined ddi xml, including all referenced items
                combined_xml[Id] = '<ddi:FragmentInstance xmlns:ddi="ddi:instance:3_3" \
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
                xsi:schemaLocation="ddi:instance:3_3 http://www.ddialliance.org/Specification/DDI-Lifecycle/3.3/XMLSchema/instance.xsd">\n'  # start wrapper

                combined_xml[Id] += myddixml[Id]  # add StudyUnit xml

                StudyNo = ed.getStudyNo(myddixml[Id])
                if StudyNo !="":
                    print("StudyNo is ", StudyNo)

                    # get also the referenced items to build CVs used there
                    methxml = ""
                    dcxml = ""

                    ref = ed.get_reference(
                        myddixml[Id], ".//StudyUnit/DataCollectionReference"
                    )
                    itm = c.get_an_item_version(ref["Agency"], ref["ID"], ref["Version"])
                    if itm is not None:
                        if itm[1] is not None:
                            if "Item" in itm[1]:
                                addxml = itm[1]["Item"]
                                dcxml = addxml
                                combined_xml[Id] += "\n" + dcxml
                        if not dcxml == "":
                            # MethodologyReference within DataCollection
                            ref = ed.get_reference(
                                dcxml, ".//DataCollection/MethodologyReference"
                            )
                            itm = c.get_an_item_version(
                                ref["Agency"], ref["ID"], ref["Version"]
                            )
                            if itm is not None:
                                if itm[1] is not None:
                                    if "Item" in itm[1]:
                                        addxml = itm[1]["Item"]
                                        methxml = addxml
                                        combined_xml[Id] += "\n" + methxml
                                        # print('MethodologyReference found')
                    if dcxml == "":
                        print("No DataCollectionReference found")
                    if methxml == "":
                        print("No MethodologyReference found")

                    # get also the referenced dataset to get StudyDOI
                    phyxml = ""
                    ref = ed.get_reference(
                        myddixml[Id], ".//StudyUnit/PhysicalInstanceReference"
                    )
                    itm = c.get_an_item_version(ref["Agency"], ref["ID"], ref["Version"])
                    if itm is not None:
                        if itm[1] is not None:
                            if "Item" in itm[1]:
                                addxml = itm[1]["Item"]
                                phyxml = addxml
                                combined_xml[Id] += "\n" + phyxml

                    if not phyxml == "":
                        ##new functions in ed.:
                        StudyDOI = ed.getDatasetDOI(phyxml)
                        StudyVersion = ed.getDatasetVersion(phyxml)
                        print(StudyDOI, StudyVersion)
                    else:
                        print("No PhysicalInstanceReference found")

                    combined_xml[Id] += "\n</ddi:FragmentInstance>"  # end wrapper

            
            StudyURL = (
                "https://search.gesis.org/research_data/" + StudyNo + "?doi=" + StudyDOI
            )
        
        if StudyNo != "":
            outdir = "CDC" #not "out"
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            xmlfile = str(StudyNo)  + ".xml"  # xml file name #  not + "_" + str(Id) #v0.9.1 do not use cdc_ in the filename 

            # check if CVCollection was saved already
            cvfile = os.path.join(outdir, "CVCollection.json")
            if os.path.exists(cvfile):
                # read the CVCollection file
                f = open(cvfile, "r", encoding="utf-8")
                CVCollection = json.load(f)
                f.close()
                print("CVCollection from local cached file " + cvfile)
            else:
                CVCollection = getCVCollection(myddixml[Id], methxml)
                # write CVCollection to file for later use
                f = open(cvfile, "w", encoding="utf-8")
                json.dump(CVCollection, f, ensure_ascii=False, indent=4)
                f.close()

            # write CDC xml to file (use the combined_xml[Id] here)
            cdc.write_cdcxml_fromddixml(os.path.join(outdir, xmlfile), combined_xml[Id], CVCollection, StudyURL)
            print("createcdc: " + str(xmlfile) + "")

            # read the created file
            f = open(os.path.join(outdir, xmlfile), "r", encoding="utf-8")
            cdcxml = f.read()
            f.close()

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return cdcxml





def studies():
    
    studylist = []
    try:
            # get all studies 30ea0200-7121-4f01-8d21-a931a182b86d
            L = c.general_search("30ea0200-7121-4f01-8d21-a931a182b86d", "", 0)
            if L:
                counter=0
                if str(L[0]) == "200":
                    print("Studies total: " + str(L[1]["TotalResults"]) + "")
                    
                    
                    for item in L[1]["Results"]:
                        #print(item)
                        #print('')
                        agency = item["AgencyId"]
                        Id = item["Identifier"]
                        Version = item["Version"]
                        
                        
                        
                        #get StudyNo if available  
                        include = False
                        
                        StudyNo="-"
                        if not counter > 25: # lasts too long for 6000 studies 
                        #if False:
                            #include = True
                            studyresult = c.get_an_item(agency, Id)
                            if str(studyresult[0]) == "200":
                                if studyresult[1]["Item"] is not None:
                                    StudyNo = ed.getStudyNo(studyresult[1]["Item"])
                                    counter += 1

                        studyitem = [StudyNo, agency, Id, Version]
                        studylist.append(studyitem)

                        if include:
                            title = ""
                            titleEN = ""
                            titles = item["ItemName"]
                            for lang in titles:
                                if lang == "de":
                                    title = item["ItemName"][lang]
                                if lang == "en":
                                    titleEN = item["ItemName"][lang]


                            displaytitle = title
                            if displaytitle=='': displaytitle=titleEN
                            print("------------")
                            print(StudyNo)
                            print(title)
                            print(titleEN)
                            
                #print("Studies with StudyNo: " + str(counter) + "")                
                    
    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())
    
    return studylist
    
                    
def login():
        tokenHeader = c.get_jwtToken(g.colecticahostname, g.colecticausername, g.colecticapassword)
        
        if tokenHeader == "":
            g.session_data["tokenHeader"] = ""
            g.session_data["userName"] = ""
            g.loggedin = False
            txtmsg = "Your login to Colectica has failed."
            g.status == "failedLogin"
            print(txtmsg)

        else:
            g.session_data["tokenHeader"] = tokenHeader
            g.session_data["userName"] = g.colecticausername
            g.loggedin = True
            txtmsg = "You have successfully logged in to Colectica."
            g.status == "successLogin"
            print(txtmsg)
    
    

def logout():
    # delete token from session
    g.session_data["tokenHeader"] = ""
    g.session_data["userName"] = ""
    g.loggedin = False
                    
                    
                    
# start application
print("")
print("Start Application " + g.appname)
print("Version " + g.appversion)
print("")


def colecticacheck():
    # Run the CDC Studies Check
    print("")
    print("Login to ", g.colecticahostname)
    login()
    
    if g.loggedin:
        print("")
        print("Get number of studies")
        studylist = studies()
        
        studycount = 0
        success = 0 
        for study in studylist:
            studycount+=1
            if studycount>0:
                print("")
                StudyNo = study[0]
                agency = study[1]
                Id = study[2]
                Version = study[3]                        
                
                #print(StudyNo)
                
                #combine the CDC DDI2.5 metadata from Colectica DDI DDI 3.3 here 
                cdcxml = get_cdcxml(agency, Id) 
                
                #print(cdcxml)
                if cdcxml != "":
                    success +=1
                    print("Success")
                #else:
                #    print("Error")
                            
    print("")
    print("")
    print("Success for ", success, " studies")

# Check Colectica Host Server 
print("")
print("Config vars from settings.py")
if g.colecticahostname == "":
    print("  - colecticahostname not configured!")
else:
    print("  - colecticahostname: " + g.colecticahostname)
    g.colecticahosthoststatus = g.checkhost(g.colecticahostname)
    if not g.colecticahosthoststatus == "":
        print("  - " + g.colecticahosthoststatus)
    else:
        print("  - Colectica host is reachable on port 80")
        
        if g.colecticausername == "":
            print("  - colecticausername is not set")
        else:
            if g.colecticapassword == "":
                print("  - colecticapassword is not set")
            else:
                #really run the check
                colecticacheck()


    print("")
    print("Finished.")
    print("")


