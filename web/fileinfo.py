"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g

import colecticaapi as c 
import dbkeditapi as d
import util.edxml as ed
import util.dara as dara 
import os 


def fileinfo(request):
    
    #xml form submitted
    def submit_xmlform(self, msg):
        print('Form submitted for checking files at DBKEdit')
        result = ['000', ''] #todo # working: result = d.getFileList('0017')
        if str(result[0])=='200':
            print('Result: '+ str(result[1])) 
            xmlstatus.text = str(result[1])
        else:
            print('Error: '+ str(result[0]))
            xmlstatus.text = 'Error: '+ str(result[0]) + '\n' + str(result[1])        
        
        wp.page.update()
        
        
    def reset_xmlform(self, msg):
        xmlstatus.text = 'Sending...'
        wp.page.update()
    
    #sendform submitted
    def submit_sendform(self, msg):
        print('Form submitted for sending files to DBKEdit')
        result = ['000', ''] #todo # working: result = d.postFileList('0017')
        if str(result[0])=='200':
            print('Result: '+ str(result[1])) 
            xmlstatus.text = str(result[1])
        else:
            print('Error: '+ str(result[0]))
            xmlstatus.text = 'Error: '+ str(result[0]) + '\n' + str(result[1])        
        
        wp.page.update()
        
        
    def reset_sendform(self, msg):
        xmlstatus.text = 'Sending...'
        wp.page.update()
        
    #start page     
    wp = g.templatewp()
    
    if g.loggedin:
        agency = request.path_params["agency"]
        Id = request.path_params["id"]
        
        #back to study button
        buttonsdiv = jp.Div(text='', a=wp, classes=g.menuul, style='display: flex;')        
        studybutton = jp.A(text='Study', href='/study/' + agency + '/' + Id, a=buttonsdiv, classes=g.button)
        jp.A(text='File Info', href='/fileinfo/' + agency + '/' + Id, a=buttonsdiv, classes=g.dbkeditbutton)
                
                
        wp.add(jp.P(text='Files for study with agency ' + agency + ' and id ' + Id, classes='m-2'))
        
        
        #create table grid for study files 
        if True:
            #agency = item['AgencyId']
            #Id = item['Identifier'] 
            Title = ''
            TitleEN = ''
            StudyNo=''
            StudyDOI=''
            StudyVersion=''
            Version=''
            
            result = c.get_an_item(agency, Id) #test for getting the complete item, with DDI xml 
            if str(result[0])=='200':
                print('Study found: '+ Id) 
                
                
                Version=result[1]['Version']
                if result[1]['Item'] is not None:
                    StudyNo=ed.getStudyNo(result[1]['Item'])
                    studybutton.text = "Study " + StudyNo
                
                
                # access dbkedit: getFileList.asp?study=0017
                # parse result: 'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>
                
                #working: 
                #result = d.getFileList('0017') #todo: use real study number
                
                
                if str(result[0])=='200':
                    print('Filelist found: '+ Id)
                else:
                    print('Error getFileList, status ' + str(result[0]))
                    wp.add(jp.P(text='Error getFileList, status ' + str(result[0]), classes='m-2'))
                    
                #show result                             
                #create table grid for File info
                wp.add(jp.P(text='Colectica files for study ', classes='m-2 text-xl'))
                grid_options = GetGridOptions()
                grid2 = jp.AgGrid(a=wp, options=grid_options, style='height: 320px;width: 800px;margin: 0.1em;' ) #style='height: 200px; width: 300px; margin: 0.25em'
                
                #AddGridRows(grid2, agency, Id, Version, result)
                
                buttonsdiv = jp.Div(text='', a=wp, classes=g.menuul, style='display: flex;')
                
                #Form to check  
                xmlform = jp.Form(a=buttonsdiv, classes='border m-1 p-1')
                xmlformsubmit_button = jp.Input(value='Check if files are in DBKEdit', type='submit', a=xmlform, classes=g.dbkeditbutton)
                xmlform.on('submit', submit_xmlform)
                xmlform.on('click', reset_xmlform)
                
                #Form to send  
                sendform = jp.Form(a=buttonsdiv, classes='border m-1 p-1')
                sendformsubmit_button = jp.Input(value='Send these files to DBKEdit', type='submit', a=sendform, classes=g.dbkeditbutton)
                sendform.on('submit', submit_sendform)
                sendform.on('click', reset_sendform)
                
                infodiv = jp.Div(text='', a=wp)
                xmlstatus = jp.Span(text='', a=infodiv, classes='text-red-700 whitespace-pre font-mono') 
                
            else:
                print('Error get_an_item, status ' + str(result[0]))
                wp.add(jp.P(text='Error get_an_item, status ' + str(result[0]), classes='m-2'))       
    
        
    return wp
    
def AddGridRows(grid, agency, Id, Version, result):
    #gridType: FileGrid
    
    #'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>
    
    if str(result[0])=='200':
        #parse result[1]
        filedata = result[1]
        filedatarecords = filedata.split('\r\n')
        for line in filedatarecords:
            #print(line)
            if not line=='':
                linedata = line.split(';')
                #for x in linedata:
                #    print(x)
                #print(linedata)
                FileId=linedata[0]
                file=linedata[1]
                SN=linedata[2]
                size=linedata[3]
                typ=linedata[4]
                datapubl=linedata[5]
                publ=linedata[6]
                
                row = {'id': FileId, 'file': file, 'SN': SN, 'size': size, 'type': typ, 'datapubl': datapubl, 'publ': publ}
                grid.options.rowData.append(row)  
        
    

def GetGridOptions():
    
    
    #'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>
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
          {headerName: "DataPubl", field: "datapubl"},
          {headerName: "Publ", field: "publ"}
        ],
          rowData: []
    }
    """
        
    return grid_options
    

