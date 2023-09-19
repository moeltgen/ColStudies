"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g

import colecticaapi as c 
    
def series():
    wp = g.templatewp()
    
    if g.loggedin:
        wp.add(jp.P(text='Searching for series!', classes='m-2'))
    
        #get all series 4bd6eef6-99df-40e6-9b11-5b8f64e5cb23
        L = c.general_search("4bd6eef6-99df-40e6-9b11-5b8f64e5cb23", '', 0)
        if L:
            if str(L[0])=='200':
                print('Series found: '+str(L[1]['TotalResults'])+'') 
                wp.add(jp.P(text='Series found: '+str(L[1]['TotalResults'])+'', classes='m-2'))
            
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
          {headerName: "Title", field: "Title"}
        ],
          rowData: []
    }
    """
                grid = jp.AgGrid(a=wp, options=grid_options) #style='height: 200px; width: 300px; margin: 0.25em'
                for item in L[1]['Results']:
                    agency = item['AgencyId']
                    Id = item['Identifier'] 
                    title = ''
                    row = {'Agency': agency, 'ID': Id, 'Title': title}
                    grid.options.rowData.append(row)    
                
            else:
                print('Error, status ' + str(L[0]))
                wp.add(jp.P(text='Error, status ' + str(L[0]), classes='m-2'))
                
        else:
            wp.add(jp.P(text='Error, no series found', classes='m-2'))
    
    return wp

