"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g

import colecticaapi as c
import dbkeditapi as d
import starapi as st
import util.edxml as ed
import util.dara as dara
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

    """
    def cell_clicked1(self, msg):
        print("cell_clicked1")
        wp = msg.page
        print("data:", msg.data)
        print("column:", msg.column)
        print("rowIndex:", msg.rowIndex)        
        print("value:", msg.value)        
        print("-")
        
    def row_updated1(self, msg):
        print("row_updated1")
        wp = msg.page
        print("1")
        print(msg.data)
        print("e")
        
        
    def row_selected1(self, msg):
        print("row_selected1")
        wp = msg.page
        if msg.selected:
            wp.selected_rows[msg.rowIndex] = msg.data
        else:
            wp.selected_rows.pop(msg.rowIndex)
        s = f'Selected rows {sorted(list(wp.selected_rows.keys()))}'
        for i in sorted(wp.selected_rows):
            s = f'{s}\n Row {i}  Data: {wp.selected_rows[i]}'
        if wp.selected_rows:
            wp.rows_div.text = s
        else:
            wp.rows_div.text = 'No row selected'
        
    async def select_all_rows(self, msg):
        await self.grid.run_api('selectAll()', msg.page)


    async def deselect_rows(self, msg):
        await self.grid.run_api('deselectAll()', msg.page)
    """

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
            # print('Result: '+ str(result[1]))
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

    # sendform submitted
    def submit_sendform2(self, msg):
        print("Form submitted for sending files to DBKEdit", StudyNo)
        """
        filelist = []
        for row in grid2.options.rowData:
            row['dbk'] = ''
            # File, StudyNo, Size, Type, Publ, DataPubl
            fileinfo = {'File': row['file'], 'StudyNo': row['SN'], 'Size': row['size'], 'Type': row['type'], 'Publ': row['pub'], 'DataPubl': row['datapub']}
            filelist.append(fileinfo)
        
        print(filelist)
        """

        # print(grid2.options.rowData)
        result = d.postFileList(StudyNo, grid2.options.rowData)

        if str(result[0]) == "200":
            print("Result: " + str(result[1]))
            xmlstatus.text = str(result[1])
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

        wp.page.update()

    def reset_sendform2(self, msg):
        xmlstatus.text = ""
        wp.page.update()

    def submit_userform(self, msg):
        print("submit_userform", "set DBKEdit password and/or username")
        myusername = ""
        # parse from data
        for field in msg.form_data:
            if field.type in ["text"]:
                myusername = field.value
                # print('myusername', myusername)
            if field.type in ["password"]:
                mypassword = field.value
                # print('mypassword', mypassword)

        if g.dbkeditusername == "" and not myusername == "":
            g.dbkeditusername = myusername

        if g.dbkeditpassword == "" and not mypassword == "":
            g.dbkeditpassword = mypassword

        # msg.style='display:none;'
        # loginform.classes='hidden'
        msg.page.redirect = "/starinfo/" + agency + "/" + Id

    def reset_userform(self, msg):
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

                studynodir = StudyNo[0:5] + "nn"
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
                    style="height: 320px;width: 1100px;margin: 0.1em;",
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

                # if DBKEdit login information not specified, do it here
                if g.dbkeditusername == "" or g.dbkeditpassword == "":
                    userform = jp.Form(a=buttonsdiv2, classes="border m-1 p-1 w-64")
                    Formtitle = jp.P(text="DBKEdit Login", a=userform)
                    if g.dbkeditusername == "":
                        user_label = jp.Label(
                            text="User",
                            classes="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2",
                            a=userform,
                        )
                        usern = jp.Input(
                            placeholder="User", a=user_label, classes="form-input"
                        )
                        user_label.for_component = usern
                    if g.dbkeditpassword == "":
                        userpw_label = jp.Label(
                            text="Password",
                            classes="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2",
                            a=userform,
                        )
                        userpw = jp.Input(
                            placeholder="Password",
                            a=userpw_label,
                            classes="form-input",
                            type="password",
                        )
                        userpw_label.for_component = userpw
                    submit_button = jp.Input(
                        value="submit", type="submit", a=userform, classes=g.starbutton
                    )
                    userform.on("submit", submit_userform)

            else:
                print("Error get_an_item, status " + str(result[0]))
                wp.add(
                    jp.P(
                        text="Error get_an_item, status " + str(result[0]),
                        classes="m-2",
                    )
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

                row = {
                    "id": FileId,
                    "file": file,
                    "SN": SN,
                    "size": size,
                    "type": typ,
                    "pub": pub,
                    "datapub": datapub,
                    "col": col,
                    "dbk": dbk,
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
            print(result[1])  # parse result[1]
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
                    datapub = linedata[5]
                    pub = linedata[6]
                    # print(file, datapub)
                    fileinfo = {}
                    fileinfo["id"] = FileId
                    fileinfo["file"] = file
                    fileinfo["SN"] = SN
                    fileinfo["size"] = size
                    fileinfo["type"] = typ
                    fileinfo["pub"] = pub
                    fileinfo["datapub"] = datapub

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
                row["size"] = dbkfile[filetocheck]["size"]
                if dbkfile[filetocheck]["pub"] == "J":
                    row["pub"] = True
                else:
                    row["pub"] = False
                if dbkfile[filetocheck]["datapub"] == "J":
                    row["datapub"] = True
                else:
                    row["datapub"] = False

            else:
                # print('not found')
                newValue = "NOTFOUND"
            print("Checking for file ", filetocheck, "result:", newValue)

            # set result
            row["dbk"] = newValue  # like     node.setDataValue(colKey,newValue)

        if result[0] == "205":
            # reset status
            result[0] = "200"

    except Exception as e:
        return ["500", "Error " + str(e)]


def GetGridOptions():
    #'we need: <id> <file> <SN> <size> <type>
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
          {headerName: "File", field: "file"},
          {headerName: "StudyNo", field: "SN"},
          {headerName: "Size", field: "size"},
          {headerName: "Type", field: "type"},
          {headerName: "Publ", field: "pub", cellRenderer: 'checkboxRenderer', editable: true},
          {headerName: "DataPubl", field: "datapub", cellRenderer: 'checkboxRenderer', editable: true},
          
          {headerName: "CheckDBKEdit", field: "dbk", width: 10}
          
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
    return grid_options
