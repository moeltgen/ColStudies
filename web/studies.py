"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g

import colecticaapi as c 
#import util.edindex as ed
    
def studies():
    wp = g.templatewp()
    
    if g.loggedin:
        wp.add(jp.P(text='Searching for studies!', classes='m-2'))
    
        #get all studies 30ea0200-7121-4f01-8d21-a931a182b86d
        L = c.general_search("30ea0200-7121-4f01-8d21-a931a182b86d", '', 0)
        if L:
            if str(L[0])=='200':
                print('Studies found: '+str(L[1]['TotalResults'])+'') 
                wp.add(jp.P(text='Studies found: '+str(L[1]['TotalResults'])+'', classes='m-2'))
                
                #myddixml = {}
                
                #create table grid for results
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
          {headerName: "Agency", field: "Agency"},
          {headerName: "ID", field: "ID"},
          {headerName: "Version", field: "Version"},
          {headerName: "Title", field: "Title"},
          {headerName: "TitleEN", field: "TitleEN"},
          {headerName: "Details", field: "Details"}
        ],
          rowData: []
    }
    """
                grid = jp.AgGrid(a=wp, options=grid_options, style='height: 350px;width: 1100px;margin: 0.1em;') #style='height: 200px; width: 300px; margin: 0.25em'
                grid.html_columns = [5]
                
                grid.options.columnDefs[3].cellClass = ['w-56'] #width .w-56	width: 14rem;
                grid.options.columnDefs[4].cellClass = ['w-56'] #width 
                #grid.options.columnDefs[5].cellClass = ['hover:bg-blue-500']
                for item in L[1]['Results']:
                    agency = item['AgencyId']
                    Id = item['Identifier'] 
                    Version = item['Version'] 
                    title = ''
                    titleEN = ''
                    titles = item['ItemName'] 
                    for lang in titles:
                        if lang=='de':
                            title = item['ItemName'][lang]
                        if lang=='en':
                            titleEN = item['ItemName'][lang]
                    
                    
                    
                    """
                    #Details info on details page only:
                    StudyNo=''
                    StudyDOI=''
                    StudyVersion=''
                    
                    result = c.get_an_item(agency, Id) #test for getting the complete item, with DDI xml 
                    if str(result[0])=='200':
                        if result[1]['Item'] is not None:
                            myddixml[Id]=result[1]['Item']
                            StudyNo=ed.getStudyNo(myddixml[Id])
                            StudyDOI=ed.getStudyDOI(myddixml[Id])
                            StudyVersion=ed.getStudyVersion(myddixml[Id])
                            Version=ed.getVersion(myddixml[Id])
                            #print(StudyNo, StudyVersion, StudyDOI)
                            
                        else:
                            print('Error get_an_item, no Item, status ' + str(result[0]))
                            wp.add(jp.P(text='Error get_an_item, no Item, status ' + str(result[0]), classes='m-2'))
                    else:
                        print('Error get_an_item, status ' + str(result[0]))
                        wp.add(jp.P(text='Error get_an_item, status ' + str(result[0]), classes='m-2'))
                    """
                    
                    #StudyDOILink = '<a href=' + StudyDOI + '>' + StudyDOI + '</a>'
                    #DetailsLink = '<u><a href=/study/' + agency + '/' + Id + '>Details</a></u>'
                    DetailsLink = ''
                    row = {'Agency': agency, 'ID': Id, 'Version': Version, 'Title': title, 'TitleEN': titleEN, 'Details': DetailsLink}
                    grid.options.rowData.append(row)  

                
            else:
                print('Error, status ' + str(L[0]))
                wp.add(jp.P(text='Error, status ' + str(L[0]), classes='m-2'))
        else:
            wp.add(jp.P(text='Error, no studies found', classes='m-2'))
    
    return wp

