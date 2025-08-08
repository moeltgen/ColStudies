"""
    colstudies application
"""

import justpy as jp
import globalvars as g

import colecticaapi as c
import dbkeditapi as d
import starapi as st
import util.edxml as ed
import os


def starinfo(request):
    def cell_valuechanged1(self, msg):
        # print("cell_valuechanged1")

        if msg.oldValue == True:
            mynewvalue = False
        else:
            mynewvalue = True
        # server side data update:
        grid2.options.rowData[msg.rowIndex] = msg.data


    ### form 1
    # xml form submitted
    def submit_xmlform(self, msg):
        print("Form submitted for checking files at Colectica")
        result = ["000", ""]  # todo #d.postFileList('0017')
        if str(result[0]) == "200":
            print("Result: " + str(result[1]))
            xmlstatus.text = str(result[1])
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

        wp.page.update()

    def reset_xmlform(self, msg):
        xmlstatus.text = "Sending..."
        wp.page.update()

    # sendform submitted
    def submit_sendform(self, msg):
        print("Form submitted for sending files to Colectica")
        result = ["000", ""]  # todo #d.postFileList('0017')
        if str(result[0]) == "200":
            print("Result: " + str(result[1]))
            xmlstatus.text = str(result[1])
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

        wp.page.update()

    def reset_sendform(self, msg):
        xmlstatus.text = "Sending..."
        wp.page.update()

    ###

    ### form2
    # xml form2 submitted
    def submit_xmlform2(self, msg):
        print("Form submitted for checking files at DBKEdit ", StudyNo)

        DBKStudyNo = StudyNo[2:]

        print("DBKStudyNo", DBKStudyNo)

        result = d.getFileList(DBKStudyNo)
        AddGridRows_checkDBK(grid2, agency, Id, Version, result)

        if str(result[0]) == "200":
            #print('Result: '+ str(result[1]))
            xmlstatus.text = "Done"
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])
        wp.page.update()

    def reset_xmlform2(self, msg):
        xmlstatus.text = ""
        for row in grid2.options.rowData:
            row["dbk"] = ""
        wp.page.update()

    # setform submitted
    def submit_setform2(self, msg):
        print("Set DBKType = Type ", StudyNo)
        
        filelist = grid2.options.rowData
        
        for fileinfo in filelist:
            fileinfo["dbktype"] = fileinfo["type"]
        
        #print(filelist)
        if True:
            grid2.options.rowData = filelist 
            xmlstatus.text = str("DBKType = Type")
        
        
        wp.page.update()

    def reset_setform2(self, msg):
        xmlstatus.text = ""
        wp.page.update()

    
    # sendform submitted
    def submit_sendform2(self, msg):
        print("Form submitted for sending files to DBKEdit", StudyNo)

        
        filelist = grid2.options.rowData
        #print(filelist)
        
        result = d.postFileList(StudyNo, filelist)
        
        if str(result[0]) == "200":
            print("Result: " + str(result[1]))
            xmlstatus.text = str(result[1])
        
        elif str(result[0]) == "401":
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + " - Not authorized: You are not logged in to DBKEdit \n" + str(result[1])
        
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

        wp.page.update()

    def reset_sendform2(self, msg):
        xmlstatus.text = ""
        wp.page.update()

    #######################
    #functions for select
    def submit_selform1(self, msg):
        print("Form submitted for select all", StudyNo)
        
        filelist = grid2.options.rowData
        
        for fileinfo in filelist:
            fileinfo["select"] = True 
        
        grid2.options.rowData = filelist 
        xmlstatus.text = str("selected all")
        
        wp.page.update()

    def reset_selform1(self, msg):
        xmlstatus.text = ""
        wp.page.update()
    
    def submit_selform2(self, msg):
        print("Form submitted for select none", StudyNo)
        
        filelist = grid2.options.rowData
        
        for fileinfo in filelist:
            fileinfo["select"] = False
        
        grid2.options.rowData = filelist 
        xmlstatus.text = str("selected none")
        
        wp.page.update()

    def reset_selform2(self, msg):
        xmlstatus.text = ""
        wp.page.update()

        
    def submit_selform3(self, msg):
        print("Form submitted for deleting selected at DBKEdit", StudyNo)
        
        filelist = grid2.options.rowData
        filedelete = []
        for fileinfo in filelist:
            if fileinfo["select"]==True:
                filedelete.append(fileinfo)

        result = d.postFileListDelete(StudyNo, filedelete)
        
        if str(result[0]) == "200":
            print("Result: " + str(result[1]))
            xmlstatus.text = str(result[1])
        
        elif str(result[0]) == "401":
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + " - Not authorized: You are not logged in to DBKEdit \n" + str(result[1])
        
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])
        
        
        wp.page.update()

    def reset_selform3(self, msg):
        xmlstatus.text = ""
        wp.page.update()
    #
    ########################
    
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
            text="STAR Info",
            href="/starinfo/" + agency + "/" + Id,
            a=buttonsdiv,
            classes=g.starbutton,
        )

        wp.add(
            jp.P(
                text="Files for study with agency " + agency + " and id " + Id,
                classes="m-2",
            )
        )
        
        wp.add(
            jp.Div(text="STAR Information", style="background-color: papayawhip; width: 300px;", classes="text-right")
            )
        wp.add(
            jp.Div(text="DBKEdit Information (editable) ", style="background-color: darkseagreen; width: 300px;", classes="text-right")
            )
            
        
        # create table grid for study files
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
                # print('Study found: '+ Id)

                Version = result[1]["Version"]
                if result[1]["Item"] is not None:
                    StudyNo = ed.getStudyNo(result[1]["Item"])
                    studybutton.text = "Study " + StudyNo

                # access star: C:\Users\moeltgen\Documents\python\colstudies_github\STAR_Files\Inventar\ZA100nn\ZA10002\Service
                # parse result: 'we need: <id> <file> <SN> <size> <type> <datapub> <pub>
                result = st.getFileList(StudyNo)
                
                if len(StudyNo)==7:
                    studynodir = StudyNo[0:5] + "nn" #Länge 5 
                elif len(StudyNo)==6:
                    studynodir = StudyNo[0:4] + "nn" #Länge 4
                else:
                    studynodir = StudyNo #nicht vorgesehen
                        
                filepath = os.path.join(
                    g.starpath, studynodir, StudyNo, "Service"
                )  # Service folder for study

                if not str(result[0]) == "200":
                    print("Error getFileList, status " + str(result[0]))
                    wp.add(
                        jp.P(
                            text="Error getFileList, status " + str(result[0]),
                            classes="m-2",
                        )
                    )

                # show result
                # create table grid for STAR info
                wp.add(jp.P(text="STAR files for study ", classes="m-2 text-xl"))
                wp.add(jp.P(text="Folder " + filepath, classes="m-2 text-l"))
                
                
                grid_options = GetGridOptions()
                grid2 = jp.AgGrid(
                    a=wp,
                    options=grid_options,
                    style="height: 600px;width:2100px;margin: 0.1em;",
                )  # style='height: 200px; width: 300px; margin: 0.25em'

                # add the data to grid2
                AddGridRows(grid2, agency, Id, Version, result)

                # add the update methods to grid2
                # grid2.on('rowDataUpdated', row_updated1)
                # grid2.on('cellClicked', cell_clicked1)
                grid2.on("cellValueChanged", cell_valuechanged1)

                # refreshCells
                # cellClicked

                """
                #test 
                wp.selected_rows = {}  # Dictionary holding selected rows
                
                grid2.options.columnDefs[0].checkboxSelection = True
                grid2.on('rowSelected', row_selected1)
                wp.rows_div = jp.Pre(text='Data will go here when you select rows', classes='border text-lg', a=wp)
                btn_deselect = jp.Button(text='Deselect rows', classes=jp.Styles.button_simple+' m-2', a=wp, click=deselect_rows)
                btn_deselect.grid = grid2
                btn_select_all = jp.Button(text='Select all rows', classes=jp.Styles.button_simple+' m-2', a=wp, click=select_all_rows)
                btn_select_all.grid = grid2
                """

                """
                todo Colectica functions:
                
                buttonsdiv = jp.Div(text='', a=wp, classes=g.menuul, style='display: flex;')
                
                #Form to check  
                xmlform = jp.Form(a=buttonsdiv, classes='border m-1 p-1')
                xmlformsubmit_button = jp.Input(value='Check if files are in Colectica', type='submit', a=xmlform, classes=g.starbutton)
                xmlform.on('submit', submit_xmlform)
                xmlform.on('click', reset_xmlform)
                
                #Form to send  
                sendform = jp.Form(a=buttonsdiv, classes='border m-1 p-1')
                sendformsubmit_button = jp.Input(value='Send these files to Colectica', type='submit', a=sendform, classes=g.starbutton)
                sendform.on('submit', submit_sendform)
                sendform.on('click', reset_sendform)
                
                """

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
                    value="Check if files are in DBKEdit",
                    type="submit",
                    a=xmlform2,
                    classes=g.starbutton,
                )
                xmlform2.on("submit", submit_xmlform2)
                xmlform2.on("click", reset_xmlform2)

                # Form to set DBKtype 
                setform2 = jp.Form(a=buttonsdiv2, classes="border m-1 p-1")
                setform2submit_button = jp.Input(
                    value="Set DBKType to value of Type",
                    type="submit",
                    a=setform2,
                    classes=g.starbutton,
                )
                setform2.on("submit", submit_setform2)
                setform2.on("click", reset_setform2)
                
                # Form to send
                sendform2 = jp.Form(a=buttonsdiv2, classes="border m-1 p-1")
                sendform2submit_button = jp.Input(
                    value="Send these files to DBKEdit",
                    type="submit",
                    a=sendform2,
                    classes=g.starbutton,
                )
                sendform2.on("submit", submit_sendform2)
                sendform2.on("click", reset_sendform2)

                ###################
                #new select buttons
                
                buttonsdiv3 = jp.Div(
                    text="", a=wp, classes=g.menuul, style="display: flex;"
                )
                # Select all 
                selform1 = jp.Form(a=buttonsdiv3, classes="border m-1 p-1")
                xmlform2submit_button = jp.Input(
                    value="Select All",
                    type="submit",
                    a=selform1,
                    classes=g.actionbutton,
                )
                selform1.on("submit", submit_selform1)
                selform1.on("click", reset_selform1)
                
                # Select none
                selform2 = jp.Form(a=buttonsdiv3, classes="border m-1 p-1")
                xmlform2submit_button = jp.Input(
                    value="Select None",
                    type="submit",
                    a=selform2,
                    classes=g.actionbutton,
                )
                selform2.on("submit", submit_selform2)
                selform2.on("click", reset_selform2)
                
                # Delete Selected
                selform3 = jp.Form(a=buttonsdiv3, classes="border m-1 p-1")
                xmlform2submit_button = jp.Input(
                    value="Delete selected from DBKEdit",
                    type="submit",
                    a=selform3,
                    classes=g.actionbutton,
                )
                selform3.on("submit", submit_selform3)
                selform3.on("click", reset_selform3)
                
                
                
                #
                ###################


            else:
                print("Error get_an_item, status " + str(result[0]))
                wp.add(
                    jp.P(
                        text="Error get_an_item, status " + str(result[0]),
                        classes="m-2",
                    )
                )
        wp.add(
            jp.Div(text="Document Types")
            )
        
    return wp


def AddGridRows(grid, agency, Id, Version, result):
    # gridType: FileGrid

    #'we need: <id> <file> <SN> <size> <type>

    if str(result[0]) == "200":
        # parse result[1]
        filedata = result[1]
        filedatarecords = filedata.split("\r\n")
        for line in filedatarecords:
            # print(line)
            if not line == "":
                linedata = line.split(";")
                # for x in linedata:
                #    print(x)
                # print(linedata)
                FileId = linedata[0]
                file = linedata[1]
                SN = linedata[2]
                size = linedata[3]
                typ = linedata[4]
                pub = False
                datapub = False
                col = ""
                dbk = ""
                
                typname=getDocTypeEN(int(typ))
                
                row = {
                    "id": FileId,
                    "file": file,
                    "SN": SN,
                    "size": size,
                    "dbksize": "",              
                    "type": typname,
                    "dbktype": "",              
                    "pub": pub,
                    "datapub": datapub,
                    "col": col,
                    "dbk": dbk,
                    "select": False
                }
                grid.options.rowData.append(row)


def AddGridRows_checkDBK(grid, agency, Id, Version, result):
    # gridType: FileGrid

    #'we need: <id> <file> <SN> <size> <type>

    try:
        # first get the files in DBK, and create dict
        dbkfile = {}
        if str(result[0]) == "200":
            if result[1][:5] == "Error":
                # request.status was ok, but study not found, so no files in DBKEdit: go with empty list
                result[0] = "205"
                dbkfile = {}
        else:
            print("Error DBK getFileList, status " + str(result[0]))
            wp.add(
                jp.P(text="Error getFileList, status " + str(result[0]), classes="m-2")
            )
        if str(result[0]) == "200":
            #print(result[1])  # parse result[1]
            filedata = result[1]
            filedatarecords = filedata.split("\r\n")
            for line in filedatarecords:
                # print(line)
                if not line == "":
                    linedata = line.split(";")

                    # for x in linedata:
                    #    print(x)
                    #print(linedata)
                    l = len(linedata)
                    #print(l)
                    
                    FileId = linedata[0]
                    file = linedata[1]
                    SN = linedata[2]
                    size = linedata[3]
                    typ = linedata[4]
                    datapub = linedata[5]
                    pub = linedata[6]
                    commentde = linedata[7]
                    commenten = linedata[8]
                    
                    if l>9:
                        spssexport = linedata[9]
                    else:
                        spssexport = "N"
                    if l>10:
                        spsslang = linedata[10]
                    else:
                        spsslang = ""
                    
                    commentde = commentde.strip('\"')
                    commenten = commenten.strip('\"')
                    spsslang = spsslang.strip('\"')
                    
                    # print(file, datapub)
                    fileinfo = {}
                    fileinfo["id"] = FileId
                    fileinfo["file"] = file
                    fileinfo["SN"] = SN
                    fileinfo["dbksize"] = size
                    
                    typname = getDocTypeEN(int(typ))
                    fileinfo["dbktype"] = typname 
                    
                    fileinfo["pub"] = pub
                    fileinfo["datapub"] = datapub
                    
                    fileinfo["commentde"] = commentde
                    fileinfo["commenten"] = commenten
                    fileinfo["spssexport"] = spssexport
                    fileinfo["spsslang"] = spsslang

                    dbkfile[file] = fileinfo

        # grid.options.columnDefs[5].editable = True
        # grid.options.columnDefs[5].checkboxSelection = True

        # now check each file
        for row in grid.options.rowData:
            filetocheck = row["file"]
            
            if filetocheck in dbkfile:
                # print('found')
                newValue = "FOUND"
                # set new values
                row["id"] = dbkfile[filetocheck]["id"]
                row["dbksize"] = dbkfile[filetocheck]["dbksize"]
                
                row["dbktype"] = dbkfile[filetocheck]["dbktype"]  #todo:  get label from value 
                
                if dbkfile[filetocheck]["pub"] == "J":
                    row["pub"] = True
                else:
                    row["pub"] = False
                if dbkfile[filetocheck]["datapub"] == "J":
                    row["datapub"] = True
                else:
                    row["datapub"] = False
                row["commentde"] = dbkfile[filetocheck]["commentde"]                                                
                row["commenten"] = dbkfile[filetocheck]["commenten"]                                                
                
                
                if dbkfile[filetocheck]["spssexport"] == "J":
                    row["spssexport"] = True
                else:
                    row["spssexport"] = False
                row["spsslang"] = dbkfile[filetocheck]["spsslang"]                                                
        
            else:
                # print('not found')
                newValue = "NOTFOUND"
            print("Checking for file ", filetocheck, "result:", newValue)

            # set result
            row["dbk"] = newValue  # like     node.setDataValue(colKey,newValue)

        # added in version 0.8
        # now check each file if it is present; add if not present 
        filelist = grid2.options.rowData    #existing files 
        #loop through dbkeditfiles 
        for filename in dbkfile:
            
            found=False 
            for existingfile in filelist:
                if existingfile["file"]==filename:
                    found=True
                    break 
            
            if not found: 
                fileinfo = dbkfile[filename]
                #not used:            
                #typecode = getDocNumEN(fileinfo["dbktype"])
                pub = False 
                datapub = False 
                spssexport= False 
                if fileinfo["pub"] == "J":
                    pub = True 
                if fileinfo["datapub"] == "J":
                    datapub = True 
                if fileinfo["spssexport"] == "J":
                    spssexport = True 
                
                row = {
                        "id": fileinfo["id"],
                        "file": fileinfo["file"],
                        "SN": fileinfo["SN"],
                        "size": "",
                        "dbksize": fileinfo["dbksize"],              
                        "type": "",
                        "dbktype": fileinfo["dbktype"],              
                        "pub": pub,
                        "datapub": datapub,
                        "commentde": fileinfo["commentde"],
                        "commenten": fileinfo["commenten"],
                        "spssexport": spssexport,
                        "spsslang": fileinfo["spsslang"],                    
                        "dbk": "ADDITIONAL",
                        "select": True
                    }
                
                grid.options.rowData.append(row)
                
        
        if result[0] == "205":
            # reset status
            result[0] = "200"

    except Exception as e:
        return ["500", "Error " + str(e)]


def GetGridOptions():
    #'we need: <id> <file> <SN> <size> <type>
    
    typelist = ""
    typelist += "'" + getDocTypeEN(1) + "',"
    typelist += "'" + getDocTypeEN(2) + "',"
    typelist += "'" + getDocTypeEN(3) + "',"
    typelist += "'" + getDocTypeEN(4) + "',"
    typelist += "'" + getDocTypeEN(5) + "',"
    typelist += "'" + getDocTypeEN(6) + "',"
    typelist += "'" + getDocTypeEN(7) + "',"
    typelist += "'" + getDocTypeEN(8) + "',"
    typelist += "'" + getDocTypeEN(9) + "',"
    typelist += "'" + getDocTypeEN(10) + "',"
    typelist += "'" + getDocTypeEN(11) + "',"
    typelist += "'" + getDocTypeEN(12) + "',"
    typelist += "'" + getDocTypeEN(13) + "',"
    typelist += "'" + getDocTypeEN(14) + "',"
    typelist += "'" + getDocTypeEN(15) + "',"
    typelist += "'" + getDocTypeEN(16) + "',"
    typelist += "'" + getDocTypeEN(17) + "'"
    
    
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
          {headerName: "ID", field: "id"},
          {headerName: "File", field: "file", cellStyle: {'background-color': 'papayawhip'}},
          {headerName: "StudyNo", field: "SN", cellStyle: {'background-color': 'papayawhip'}},
          {headerName: "Size", field: "size", cellStyle: {'background-color': 'papayawhip'}},
          {headerName: "DBKSize", field: "dbksize"},
          {headerName: "Type", field: "type", cellStyle: {'background-color': 'papayawhip'}},
          {headerName: "DBKType", field: "dbktype", 
                cellStyle: {'background-color': 'darkseagreen'}, 
                cellEditor: 'agSelectCellEditor', cellEditorParams: {
                    values: ["""+typelist+"""]
                    }, editable: true},          
          {headerName: "Publ", field: "pub", cellRenderer: 'checkboxRenderer', editable: true, cellStyle: {'background-color': 'darkseagreen'}},
          {headerName: "DataPubl", field: "datapub", cellRenderer: 'checkboxRenderer', editable: true, cellStyle: {'background-color': 'darkseagreen'}},
          {headerName: "CommentDE", field: "commentde", editable: true, cellStyle: {'background-color': 'darkseagreen'}},
          {headerName: "CommentEN", field: "commenten", editable: true, cellStyle: {'background-color': 'darkseagreen'}},
          {headerName: "SPSS Export", field: "spssexport", cellRenderer: 'checkboxRenderer', editable: true, cellStyle: {'background-color': 'darkseagreen'}},
          {headerName: "SPSS Language", field: "spsslang", editable: true, cellStyle: {'background-color': 'darkseagreen'}},
          {headerName: "CheckDBKEdit", field: "dbk", width: 10},
          {headerName: "Select", field: "select", cellRenderer: 'checkboxRenderer', editable: true, cellStyle: {'background-color': 'bittersweet'}}
                    
        ],
          rowData: []
    }
    """
    ## todo later:
    ## {headerName: "CheckColectica", field: "col", width: 10},
    ##

    # , cellRenderer: 'checkboxRenderer', editable: false
    # , cellRenderer: 'agCheckboxCellRenderer', editable: true
    # , cellRenderer: 'agCheckboxCellRenderer', editable: true, cellEditor: 'agCheckboxCellEditor'
    #
    
    
    """
    Liste der Material-Typen:

    1	Fragebogen	Questionnaire
    2	Methodenbericht	Method Report
    3	Codebuch	Codebook
    4	sonstiges	Other Document
    5	Datensatz	Dataset
    6	Datengeber-Bericht	Data Depositor Report
    7	Code-/Spaltenplan	Codeplan
    8	Anmerkungen	Remarks
    9	Studienbeschreibung	Study Description
    10	Tabelle	Table
    11	Methodenfragebogen	Method Questionnaire
    12	Bericht	Report
    13	Kartenspiel/Listenheft	Cards/Lists
    14	Variablenreport	Variable Report
    15	Leitfaden	Guidelines
    16	Nutzungsvertrag	User Contract
    17	DDI-C Codebuch	DDI-C Codebook
    """
    return grid_options

def getDocTypeDE(docnum):
    
    docType = ""
    
    if docnum==1:
        docType = "Fragebogen"
    elif docnum==2:
        docType = "Methodenbericht"
    elif docnum==3:
        docType = "Codebuch"
    elif docnum==4:
        docType = "sonstiges"
    elif docnum==5:
        docType = "Datensatz"
    elif docnum==6:
        docType = "Datengeber-Bericht"
    elif docnum==7:
        docType = "Code-/Spaltenplan"
    elif docnum==8:
        docType = "Anmerkungen"
    elif docnum==9:
        docType = "Studienbeschreibung"
    elif docnum==10:
        docType = "Tabelle"
    elif docnum==11:
        docType = "Methodenfragebogen"
    elif docnum==12:
        docType = "Bericht"
    elif docnum==13:
        docType = "Kartenspiel/Listenheft"
    elif docnum==14:
        docType = "Variablenreport"
    elif docnum==15:
        docType = "Leitfaden"
    elif docnum==16:
        docType = "Nutzungsvertrag"
    elif docnum==17:
        docType = "DDI-C Codebuch"    
        
    return docType

def getDocTypeEN(docnum):
    
    docType = ""
    
    if docnum==1:
        docType = "Questionnaire"
    elif docnum==2:
        docType = "Method Report"
    elif docnum==3:
        docType = "Codebook"
    elif docnum==4:
        docType = "Other Document"
    elif docnum==5:
        docType = "Dataset"
    elif docnum==6:
        docType = "Data Depositor Report"
    elif docnum==7:
        docType = "Codeplan"
    elif docnum==8:
        docType = "Remarks"
    elif docnum==9:
        docType = "Study Description"
    elif docnum==10:
        docType = "Table"
    elif docnum==11:
        docType = "Method Questionnaire"
    elif docnum==12:
        docType = "Report"
    elif docnum==13:
        docType = "Cards/Lists"
    elif docnum==14:
        docType = "Variable Report"
    elif docnum==15:
        docType = "Guidelines"
    elif docnum==16:
        docType = "User Contract"
    elif docnum==17:
        docType = "DDI-C Codebook"
            
    return docType
    
def getDocNumEN(docType):
    
    docnum = 0
    
    if docType == "Questionnaire":
        docnum=1
    elif docType == "Method Report":
        docnum=2
    elif docType == "Codebook":
        docnum=3        
    elif docType == "Other Document":
        docnum=4
    elif docType == "Dataset":
        docnum=5
    elif docType == "Data Depositor Report":
        docnum=6
    elif docType == "Codeplan":
        docnum=7
    elif docType == "Remarks":
        docnum=8
    elif docType == "Study Description":
        docnum=9
    elif docType == "Table":
        docnum=10
    elif docType == "Method Questionnaire":
        docnum=11
    elif docType == "Report":
        docnum=12
    elif docType == "Cards/Lists":
        docnum=13
    elif docType == "Variable Report":
        docnum=14
    elif docType == "Guidelines":
        docnum=15
    elif docType == "User Contract":
        docnum=16
    elif docType == "DDI-C Codebook":
        docnum=17
            
    return docnum
    
    
    
        
