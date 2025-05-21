"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g
import traceback
import colecticaapi as c
import util.edxml as ed
import util.dara as dara
import os


def doiinfo(request):
    wp = g.templatewp()

    try:
        # register form submitted
        def submit_form(self, msg):
            if g.darausername == "" or g.darapassword == "":
                resulttext = "Not logged in to da|ra! \n"
                print(resulttext)
                registerstatus.text = resulttext
            else:
                print("Form submitted for registration of DOI")
                resulttext = dararegister(agency, Id)
                registerstatus.text = resulttext

            wp.page.update()

        # xml form submitted
        def submit_xmlform(self, msg):
            print("Form submitted for showing dara xml")
            daraxml = get_daraxml(agency, Id)
            xmlstatus.text = daraxml

            wp.page.update()

        # start page
        if g.loggedin:
            agency = request.path_params["agency"]
            Id = request.path_params["id"]

            # back to study button
            buttonsdiv = jp.Div(text="", a=wp, classes=g.menuul, style="display: flex;")
            studybutton = jp.A(
                text="Study",
                href="/study/" + agency + "/" + Id,
                a=buttonsdiv,
                classes=g.button,
            )
            jp.A(
                text="DOI Info",
                href="/doiinfo/" + agency + "/" + Id,
                a=buttonsdiv,
                classes=g.darabutton,
            )

            wp.add(
                jp.P(
                    text="Searching for study with agency " + agency + " and id " + Id,
                    classes="m-2",
                )
            )

            myddixml = {}

            if True:
                # agency = item['AgencyId']
                # Id = item['Identifier']
                Title = ""
                TitleEN = ""
                StudyNo = ""
                StudyDOI = ""
                StudyVersion = ""
                Version = ""

                result = c.get_an_item(
                    agency, Id
                )  # test for getting the complete item, with DDI xml
                if str(result[0]) == "200":
                    print("Study found: " + Id)

                    Version = result[1]["Version"]
                    if result[1]["Item"] is not None:
                        StudyNo = ed.getStudyNo(result[1]["Item"])
                        studybutton.text = "Study " + StudyNo

                    # create table grid for DOI info
                    wp.add(jp.P(text="DOI Info ", classes="m-2 text-xl"))
                    grid_options = GetGridOptions()
                    grid2 = jp.AgGrid(
                        a=wp,
                        options=grid_options,
                        style="height: 150px;width:1500px;margin: 0.1em;",
                    )  # style='height: 200px; width: 300px; margin: 0.25em'
                    grid2.html_columns = [1, 2]
                    AddGridRows(grid2, agency, Id, Version, result)

                    if not g.daradoiprefix == "":
                        warndiv = jp.Div(
                            text="DOI prefix is replaced by "
                            + g.daradoiprefix
                            + " (settings.py)",
                            a=wp,
                            classes="text-red-700 whitespace-pre font-mono",
                        )

                    buttonsdiv = jp.Div(
                        text="", a=wp, classes=g.menuul, style="display: flex;"
                    )
                    # Form to show xml
                    xmlform = jp.Form(a=buttonsdiv, classes="border m-1 p-1")
                    submit_button = jp.Input(
                        value="show dara xml",
                        type="submit",
                        a=xmlform,
                        classes=g.darabutton,
                    )
                    xmlform.on("submit", submit_xmlform)

                    # Form to register
                    registerform = jp.Form(a=buttonsdiv, classes="border m-1 p-1")
                    submit_button = jp.Input(
                        value="register/update DOI",
                        type="submit",
                        a=registerform,
                        classes=g.darabutton,
                    )
                    registerform.on("submit", submit_form)

                    infodiv = jp.Div(text="", a=wp)
                    registerstatus = jp.Span(
                        text="",
                        a=infodiv,
                        classes="text-red-700 whitespace-pre font-mono",
                    )
                    xmlstatus = jp.Span(
                        text="",
                        a=infodiv,
                        classes="text-red-700 whitespace-pre font-mono",
                    )

                else:
                    print("Error get_an_item, status " + str(result[0]))
                    wp.add(
                        jp.P(
                            text="Error get_an_item, status " + str(result[0]),
                            classes="m-2",
                        )
                    )
        else:
            wp.add(jp.P(text="You are not logged in to Colectica.", classes="m-2"))

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return wp


def AddGridRows(grid, agency, Id, Version, result):
    # gridType: DOIGrid or DOIProposalGrid

    try:
        myddixml = {}

        if result[1]["Item"] is not None:
            myddixml[Id] = result[1]["Item"]
            # print(myddixml[Id]) #contains Fragment with StudyUnit

            StudyNo = ed.getStudyNo(myddixml[Id])
            # use Dataset: StudyDOI=ed.getStudyDOI(myddixml[Id])
            # use Dataset: StudyVersion=ed.getStudyVersion(myddixml[Id])
            Version = ed.getVersion(myddixml[Id])
            # print(StudyNo, StudyVersion, StudyDOI)

            # Get the PhysicalInstanceReference
            addxml = ""
            pixml = ""
            ref = ed.get_reference(
                myddixml[Id], ".//StudyUnit/PhysicalInstanceReference"
            )
            itm = c.get_an_item_version(ref["Agency"], ref["ID"], ref["Version"])
            if itm is not None:
                if "Item" in itm[1]:
                    addxml = itm[1]["Item"]
            if not addxml == "":
                ##new functions in ed.:
                StudyDOI = ed.getDatasetDOI(addxml)
                StudyVersion = ed.getDatasetVersion(addxml)
                # print(StudyDOI, StudyVersion)
            else:
                print("No PhysicalInstanceReference found!")

            # if the settings indicate to override DDI XML DOI, e.g. for using the test prefix
            if not g.daradoiprefix == "":
                StudyDOIparts = StudyDOI.split("/")
                StudyDOI = g.daradoiprefix + "/" + StudyDOIparts[1]

            # default URL https://search.gesis.org/research_data/ZA3811?doi=10.4232/1.3811
            #
            # set default URL here - is not editable in Colectica Designer at the moment
            #
            #
            StudyURL = (
                "https://search.gesis.org/research_data/" + StudyNo + "?doi=" + StudyDOI
            )

            ##new functions in ed.:
            Title = ed.getStudyTitle(myddixml[Id], "de")
            TitleEN = ed.getStudyTitle(myddixml[Id], "en")
            Abstract = ed.getAbstract(myddixml[Id], "de")
            AbstractEN = ed.getAbstract(myddixml[Id], "en")

        else:
            print("Error get_an_item, no Item, status " + str(result[0]))
            wp.add(
                jp.P(
                    text="Error get_an_item, no Item, status " + str(result[0]),
                    classes="m-2",
                )
            )

        if False:
            # create a proposal with default values
            prefix = "10.17889"  # dara test prefix
            StudyVersion = "1.0.0"  # start with 1.0.0
            StudyDOI = "https://doi.org/" + prefix + "/" + StudyNo + "." + StudyVersion
            StudyURL = (
                "https://search.gesis.org/research_data/" + StudyNo + "?doi=" + StudyDOI
            )
        else:
            StudyDOI = "https://doi.org/" + StudyDOI

        if not StudyDOI == "":
            StudyDOILink = "<a href=" + StudyDOI + ">" + StudyDOI + "</a>"
        if not StudyURL == "":
            StudyURLLink = "<a href=" + StudyURL + ">" + StudyURL + "</a>"

        DetailsLink = ""

        # add fields

        # in case of DOIGrid: show link to view dara xml
        showdaraxmllink = ""
        # showdaraxmllink = '/study/daraxml/' + agency + '/' + Id
        # showdaraxmllink = '<a href=' + showdaraxmllink + '>Show da|ra xml</a>'

        row = {"Field": "StudyNo", "Value": StudyNo, "Details": showdaraxmllink}
        grid.options.rowData.append(row)
        row = {"Field": "StudyVersion", "Value": StudyVersion, "Details": DetailsLink}
        grid.options.rowData.append(row)
        row = {"Field": "StudyDOI", "Value": StudyDOILink, "Details": DetailsLink}
        grid.options.rowData.append(row)

        # in case of DOIGrid: show note for URL
        showurlnote = ""
        showurlnote = "(not from DDI)"

        row = {"Field": "StudyURL", "Value": StudyURLLink, "Details": showurlnote}
        grid.options.rowData.append(row)

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())


def GetGridOptions():
    grid_options = """
    {
        defaultColDef: {
            filter: true,
            sortable: true,
            resizable: true,
            cellStyle: {textAlign: 'left'},
            headerClass: 'font-bold'
        }, 
          columnDefs: [
          {headerName: "Field", field: "Field"},
          {headerName: "Value", field: "Value"},
          {headerName: "Details", field: "Details"}
        ],
          rowData: []
    }
    """

    return grid_options


def dararegister(agency, Id):
    """
    post the daraxml to the dara API to register the DOI
    """

    xmltext = ""

    try:
        if g.loggedin:
            xmltext = "dara xml \n"

            daraxml = get_daraxml(agency, Id)
            xmltext += " - built successfully \n"
            print("daraxml built successfully ")

            outdir = "out"
            xmlfile = "dara_" + str(Id) + ".xml"  # xml file name

            xmltext += " - call register_dara(create or update) at " + g.daraapi + " \n"
            print("call register_dara(create or update) at " + g.daraapi)

            # todo: IS currently DRAFT at da|ra!

            regresult = dara.register_dara(
                os.path.join(outdir, xmlfile), g.daraapi, g.darausername, g.darapassword
            )  # call the registration api #get settings from globalvars.py
            xmltext += " - Result: " + regresult + " \n"
            print(regresult)

        else:
            xmltext = "not logged in"

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return xmltext


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


def get_daraxml(agency, Id):
    """
    get the dara xml for a study with metadata from the Colectica API
    """

    try:
        daraxml = ""

        myddixml = {}
        combined_xml = {}
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

        # if DOI should be replaced by DOI in settings
        if not g.daradoiprefix == "":
            StudyDOIparts = StudyDOI.split("/")
            StudyDOI = g.daradoiprefix + "/" + StudyDOIparts[1]

        StudyURL = (
            "https://search.gesis.org/research_data/" + StudyNo + "?doi=" + StudyDOI
        )

        if True:
            outdir = "out"
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            xmlfile = "dara_" + str(Id) + ".xml"  # xml file name

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

            # write dara xml to file (use the combined_xml[Id] here; StudyURL needs to be injected - is not in DDIxml )
            dara.write_daraxml_fromddixml(
                os.path.join(outdir, xmlfile), combined_xml[Id], CVCollection, StudyURL
            )
            print("createdara: " + Id + " " + str(xmlfile) + "")

            # read the created file
            f = open(os.path.join(outdir, xmlfile), "r", encoding="utf-8")
            daraxml = f.read()
            f.close()

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return daraxml
