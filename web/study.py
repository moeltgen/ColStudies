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
import xml.etree.ElementTree as ET
import os


def study(request):
    wp = g.templatewp()

    try:

        def setAccessClass(AgencyId, Identifier, newAccessClass):
            try:
                newxml = ""
                result = c.get_an_item(AgencyId, Identifier)
                if str(result[0]) == "200":
                    myddixml = {}
                    if result[1]["Item"] is not None:
                        myddixml[Id] = result[1]["Item"]

                        Version = result[1]["Version"]

                        AccessClass = ed.getAccessClass(myddixml[Id], "en")
                        if AccessClass == "":
                            AccessClass = ed.getAccessClass(myddixml[Id], "en")
                        print("Old AccessClass: " + AccessClass)
                        print("New AccessClass: " + newAccessClass)

                        newxml = ed.setAccessClass(
                            myddixml[Id], newAccessClass
                        )  # change it in all languages

                # get transactionId
                # creT = c.createTransaction()
                # TransactionId = c.getTransactionValue(creT[1], 'TransactionId')

                TransactionId = 252

                addT = c.addToTransaction(
                    TransactionId, AgencyId, Identifier, Version, newxml
                )

                print(addT)

                if newxml == "":
                    return ["500", "Error " + result[0]]
                else:
                    return ["200", ET.tostring(newxml, encoding="unicode")]
            except Exception as e:
                return ["500", "Error " + str(e)]

        # cancel submitted
        def submit_cancel(self, msg):
            print("Form submitted for cancel")

            transactionId = 250
            result = c.cancelTransaction(transactionId)

            if str(result[0]) == "200":
                print("Result: " + str(result[1]))
                xmlstatus.text = str(result[1])
            else:
                print("Error: " + str(result[0]))
                xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

            wp.page.update()

        # info submitted
        def submit_info(self, msg):
            print("Form submitted for info")

            transactionId = 249
            result = c.getTransactionInfo(transactionId)

            if str(result[0]) == "200":
                # print('Result: '+ str(result[1]))
                xmlstatus.text = str(result[1])

                print(
                    c.getTransactionValue(result[1], "TransactionId"), "TransactionId"
                )
                print(c.getTransactionValue(result[1], "ItemCount"), "ItemCount")
                print(
                    c.getTransactionValue(result[1], "PropagatedItemCount"),
                    "PropagatedItemCount",
                )
                print(c.getTransactionValue(result[1], "Status"), "Status")

            else:
                print("Error: " + str(result[0]))
                xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

            wp.page.update()

        # sendform submitted
        def submit_sendform(self, msg):
            print("Form submitted for test0")
            result = setAccessClass(agency, Id, "0")
            if str(result[0]) == "200":
                # print('Result: '+ str(result[1]))
                xmlstatus.text = str(result[1])
            else:
                print("Error: " + str(result[0]))
                xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

            wp.page.update()

        def reset_sendform(self, msg):
            xmlstatus.text = "Sending..."
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

            wp.add(
                jp.P(
                    text="Searching for study with agency " + agency + " and id " + Id,
                    classes="m-2",
                )
            )

            myddixml = {}

            # create table grid for study
            ###
            grid_options = GetGridOptions()
            grid = jp.AgGrid(
                a=wp,
                options=grid_options,
                style="height: 320px;width: 800px;margin: 0.1em;",
            )  # style='height: 200px; width: 300px; margin: 0.25em'
            grid.html_columns = [1, 2]
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

                    AddGridRows(grid, agency, Id, Version, result)

                    # Buttons
                    buttonsdiv = jp.Div(
                        text="", a=wp, classes=g.menuul, style="display: flex;"
                    )
                    jp.A(
                        text="DOI Info",
                        href="/doiinfo/" + agency + "/" + Id,
                        a=buttonsdiv,
                        classes=g.darabutton,
                    )

                    jp.A(
                        text="STAR Info",
                        href="/starinfo/" + agency + "/" + Id,
                        a=buttonsdiv,
                        classes=g.starbutton,
                    )

                    jp.A(
                        text="File Info",
                        href="/fileinfo/" + agency + "/" + Id,
                        a=buttonsdiv,
                        classes=g.dbkeditbutton,
                    )

                    jp.A(
                        text="Annotations",
                        href="/annotations/" + agency + "/" + Id,
                        a=buttonsdiv,
                        classes=g.annotationbutton,
                    )

                    """
                    #disabled, does not yet work
                    
                    #Form to send  
                    sendform = jp.Form(a=buttonsdiv, classes='border m-1 p-1')
                    sendformsubmit_button = jp.Input(value='Test: set AccessClass to 0', type='submit', a=sendform, classes=g.actionbutton)
                    sendform.on('submit', submit_sendform)
                    sendform.on('click', reset_sendform)
                    
                    #Form to send  
                    cancel = jp.Form(a=buttonsdiv, classes='border m-1 p-1')
                    cancelsubmit_button = jp.Input(value='Test: cancel transaction', type='submit', a=cancel, classes=g.actionbutton)
                    cancel.on('submit', submit_cancel)
                    
                    #Form to send  
                    info = jp.Form(a=buttonsdiv, classes='border m-1 p-1')
                    infosubmit_button = jp.Input(value='Test: info transaction', type='submit', a=info, classes=g.actionbutton)
                    info.on('submit', submit_info)
                    
                    #status 0 = created, 3 = canceled
                    """

                    infodiv = jp.Div(text="", a=wp)
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
            wp.add(jp.P(text="You are not logged in.", classes="m-2"))

    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
        print(traceback.format_exc())

    return wp


def AddGridRows(grid, agency, Id, Version, result):
    # gridType: StudyGrid

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

            AccessClass = ed.getAccessClass(myddixml[Id], "en")
            if AccessClass == "":
                AccessClass = ed.getAccessClass(myddixml[Id], "en")

        else:
            print("Error get_an_item, no Item, status " + str(result[0]))
            wp.add(
                jp.P(
                    text="Error get_an_item, no Item, status " + str(result[0]),
                    classes="m-2",
                )
            )

        StudyDOI = "https://doi.org/" + StudyDOI

        if not StudyDOI == "":
            StudyDOILink = "<a href=" + StudyDOI + ">" + StudyDOI + "</a>"
        if not StudyURL == "":
            StudyURLLink = "<a href=" + StudyURL + ">" + StudyURL + "</a>"

        DetailsLink = ""

        # add fields
        row = {"Field": "Agency", "Value": agency, "Details": DetailsLink}
        grid.options.rowData.append(row)
        row = {"Field": "ID", "Value": Id, "Details": DetailsLink}
        grid.options.rowData.append(row)
        row = {"Field": "Version", "Value": Version, "Details": DetailsLink}
        grid.options.rowData.append(row)

        row = {"Field": "Title", "Value": Title, "Details": DetailsLink}
        grid.options.rowData.append(row)
        row = {"Field": "TitleEN", "Value": TitleEN, "Details": DetailsLink}
        grid.options.rowData.append(row)

        row = {"Field": "StudyNo", "Value": StudyNo, "Details": DetailsLink}
        grid.options.rowData.append(row)
        row = {"Field": "StudyVersion", "Value": StudyVersion, "Details": DetailsLink}
        grid.options.rowData.append(row)

        row = {"Field": "AccessClass", "Value": AccessClass, "Details": DetailsLink}
        grid.options.rowData.append(row)

        row = {"Field": "StudyDOI", "Value": StudyDOILink, "Details": DetailsLink}
        grid.options.rowData.append(row)

        row = {"Field": "Abstract", "Value": Abstract, "Details": DetailsLink}
        grid.options.rowData.append(row)
        row = {"Field": "AbstractEN", "Value": AbstractEN, "Details": DetailsLink}
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
