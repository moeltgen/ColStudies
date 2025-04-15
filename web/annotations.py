"""
    colstudies application
"""

import justpy as jp
import globalvars as g

import colecticaapi as c
import util.edxml as ed


def annotations(request):
    ### form2
    # xml form2 submitted
    def submit_xmlform2(self, msg):
        print("Form submitted to create Annotations in table ", StudyNo)
        xmlstatus.text = ""
        for row in grid.options.rowData:
            row["anno"] = (
                "For Xtabs see https://search.gesis.org/variables/exploredata-"
                + StudyNo
                + "_Var"
                + row["variable"]
            )

        xmlstatus.text = "Set Annotations in table"
        wp.page.update()

    def reset_xmlform2(self, msg):
        xmlstatus.text = ""
        # for row in grid.options.rowData:
        #    row['anno'] = ''
        # xmlstatus.text = 'Reset Annotations in table'
        wp.page.update()

    # sendform submitted
    def submit_sendform2(self, msg):
        print("Form submitted for sending Annotations to Colectica", StudyNo)
        xmlstatus.text = ""
        # print(grid.options.rowData)

        # post to colectica:
        # result = c.addAnnotation(StudyNo, grid.options.rowData)

        # Example Var v10
        print("Get Example Var v10")
        # de.gesis b52f71fe-6a05-42c8-90d8-35efd5c1846c 1
        VarAgency = "de.gesis"
        VarId = "b52f71fe-6a05-42c8-90d8-35efd5c1846c"
        VarVersion = "1"

        result = c.get_an_item_version(VarAgency, VarId, VarVersion)
        if str(result[0]) == "200":
            print("Result: OK")
            # print('Result: '+ str(result[1]))
            # xmlstatus.text = str(result[1])
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

        try:
            jsonitem = result[1]
            if jsonitem["Item"] is not None:
                varxml = jsonitem["Item"]
                # print(varxml)

                # modify the version of the item
                print("current version is", jsonitem["Version"])
                # jsonitem['Version']+=1
                print("new version is", jsonitem["Version"])

                # modify the varxml
                # newxml = ed.AddAnnotation(varxml, './/Variable/UserAttributePair', 'Crosstabs', 'TEST')
                newxml = ed.AddAnnotation(
                    varxml,
                    jsonitem["Version"],
                    ".//{ddi:logicalproduct:3_3}Variable/{ddi:reusable:3_3}UserAttributePair",
                    "Crosstabs",
                    "TEST",
                )

                jsonitem["Item"] = newxml

                items = {
                    "items": [jsonitem],
                    "options": {
                        "versionRationale": {"policy": "overwrite"},
                        "setName": "ColStudies",
                        "namedOptions": ["overwrite"],
                    },
                }

            print("Set Example Var v10")
            result = c.set_an_item_version(items)

            if str(result[0]) == "200":
                print("Result: " + str(result[1]))
                xmlstatus.text = str(result[1])
            else:
                print("Error: " + str(result[0]))
                xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

        except Exception as e:
            print("500", "Error " + str(e))

        wp.page.update()

    def reset_sendform2(self, msg):
        xmlstatus.text = ""
        wp.page.update()

    # start page
    wp = g.templatewp()

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
            text="Annotations",
            href="/annotations/" + agency + "/" + Id,
            a=buttonsdiv,
            classes=g.annotationbutton,
        )

        wp.add(
            jp.P(
                text="Annotations for variables in study with agency "
                + agency
                + " and id "
                + Id,
                classes="m-2",
            )
        )

        # create table grid for variables of study
        grid_options = GetGridOptions()
        grid = jp.AgGrid(
            a=wp,
            options=grid_options,
            style="height: 320px;width:1500px;margin: 0.1em;",
        )  # style='height: 200px; width: 300px; margin: 0.25em'
        # grid.html_columns = [4]

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
                    studyunitxml = result[1]["Item"]

                    # combine all the xml to get variable list
                    combined_xml = {}  # will hold all fragments including referenced ones
                    # build the combined ddi xml, including all referenced items
                    combined_xml[Id] = '<ddi:FragmentInstance xmlns:ddi="ddi:instance:3_3" \
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
                    xsi:schemaLocation="ddi:instance:3_3 http://www.ddialliance.org/Specification/DDI-Lifecycle/3.3/XMLSchema/instance.xsd">\n'  # start wrapper

                    combined_xml[Id] += studyunitxml  # add StudyUnit xml
                    # reset snippets
                    pixml = ""
                    drxml = ""
                    myvarddixml = {}
                    # myvarlist = {}
                    # myvarpos = {}

                    if True:
                        if True:  # get all referenced variables
                            # print('Add fragments which are referenced by studyunit for ' + StudyNo + ': ' + Id + ' - ' + str(Version))
                            ##add fragments which are referenced by studyunit

                            # PhysicalInstanceReference
                            addxml = ""
                            pixml = ""
                            ref = ed.get_reference(
                                studyunitxml, ".//StudyUnit/PhysicalInstanceReference"
                            )

                            itm = c.get_an_item_version(
                                ref["Agency"], ref["ID"], ref["Version"]
                            )
                            if itm is not None:
                                if itm[1]["Item"] is not None:
                                    addxml = itm[1]["Item"]
                                    combined_xml[Id] += "\n" + addxml
                                    pixml = addxml

                            drxml = ""
                            if not pixml == "":
                                # DataRelationshipReference within PhysicalInstance
                                addxml = ""
                                ref = ed.get_reference(
                                    pixml,
                                    ".//PhysicalInstance/DataRelationshipReference",
                                )
                                itm = c.get_an_item_version(
                                    ref["Agency"], ref["ID"], ref["Version"]
                                )
                                if itm is not None:
                                    if itm[1]["Item"] is not None:
                                        addxml = itm[1]["Item"]
                                        combined_xml[Id] += "\n" + addxml
                                        drxml = addxml

                            if not drxml == "":
                                # VariableUsedReference in DataRelationship/LogicalRecord/VariablesInRecord
                                addxml = ""
                                reflist = ed.get_referencelist(
                                    drxml,
                                    ".//DataRelationship/LogicalRecord/VariablesInRecord/VariableUsedReference",
                                )
                                i = 1
                                for ref in reflist:
                                    # print('Variable', ref['Agency'], ref['ID'], ref['Version'])
                                    itm = c.get_an_item_version(
                                        ref["Agency"], ref["ID"], ref["Version"]
                                    )
                                    if itm is not None:
                                        if itm[1]["Item"] is not None:
                                            addxml = itm[1]["Item"]
                                            combined_xml[Id] += "\n" + addxml

                                    # optional process each variable
                                    Limit = 30
                                    if i < Limit:
                                        VarId = ref["ID"]
                                        myvarddixml[VarId] = addxml
                                        # print(addxml)
                                        VarName = ed.getVarName(myvarddixml[VarId])
                                        VarLabel = ed.getVarLabel(myvarddixml[VarId])
                                        # myvarlist[VarId]=VarName
                                        # myvarpos[VarId]=i #save position in dataset
                                        print(
                                            "Variable found: "
                                            + VarName
                                            + " "
                                            + VarLabel
                                        )

                                        VarAgency = ref["Agency"]
                                        VarVersion = ref["Version"]
                                        # print(VarAgency, VarId, VarVersion)

                                        anno = "test"
                                        # look for annotations that contain the Crosstabs link
                                        """
                                        Example annotation
                                        <r:UserAttributePair>
                                            <r:AttributeKey>extension:CustomField</r:AttributeKey>
                                            <r:AttributeValue>{"Title":{"en":"Crosstabs"},"Description":{},"ValueType":0,"HasValue":true,"RelationshipTargetType":"00000000-0000-0000-0000-000000000000","StringValue":"For Crosstabs, see https://search.gesis.org/variables/exploredata-ZA0078_Varv101","MultilingualStringValue":{},"BooleanValue":false,"HasDefinedType":false,"DisplayLabel":"Crosstabs"}</r:AttributeValue>
                                        </r:UserAttributePair>
                                        """
                                        anno = ed.getCustomField(
                                            addxml,
                                            ".//Variable/UserAttributePair",
                                            "Crosstabs",
                                        )

                                        row = {
                                            "study": StudyNo,
                                            "variable": VarName,
                                            "label": VarLabel,
                                            "anno": anno,
                                        }
                                        grid.options.rowData.append(row)
                                    else:
                                        break

                                    i += 1

                # Info
                infodiv = jp.Div(text="", a=wp)
                xmlstatus = jp.Span(
                    text="", a=infodiv, classes="text-red-700 whitespace-pre font-mono"
                )

                buttonsdiv2 = jp.Div(
                    text="", a=wp, classes=g.menuul, style="display: flex;"
                )

                # Form to check
                xmlform2 = jp.Form(a=buttonsdiv2, classes="border m-1 p-1")
                xmlform2submit_button = jp.Input(
                    value="Create Annotations in table",
                    type="submit",
                    a=xmlform2,
                    classes=g.annotationbutton,
                )
                xmlform2.on("submit", submit_xmlform2)
                xmlform2.on("click", reset_xmlform2)

                # Form to send
                sendform2 = jp.Form(a=buttonsdiv2, classes="border m-1 p-1")
                sendform2submit_button = jp.Input(
                    value="Set Annotations in Colectica",
                    type="submit",
                    a=sendform2,
                    classes=g.annotationbutton,
                )
                sendform2.on("submit", submit_sendform2)
                sendform2.on("click", reset_sendform2)

            else:
                print("Error get_an_item, status " + str(result[0]))
                wp.add(
                    jp.P(
                        text="Error get_an_item, status " + str(result[0]),
                        classes="m-2",
                    )
                )

    return wp


def GetGridOptions():
    #'we need: <id> <study> <variable> <label> <anno>
    grid_options = """
    {
        defaultColDef: {
            filter: true,
            sortable: true,
            resizable: true,
            cellStyle: {textAlign: 'left'},
            flex: true,
            headerClass: 'font-bold'
        }, 
          columnDefs: [
          {headerName: "StudyNo", field: "study"},
          {headerName: "Variable", field: "variable"},
          {headerName: "Label", field: "label"},
          {headerName: "Annotation", field: "anno", editable: true} 
        ],
          rowData: []
    }
    """
    return grid_options
