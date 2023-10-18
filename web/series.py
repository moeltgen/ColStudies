"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g
import traceback
import colecticaapi as c 
    
def series():

    wp = g.templatewp()

    try:
    
        if g.loggedin:
            wp.add(jp.P(text='Searching for series', classes='m-2'))
        
            #get all series 4bd6eef6-99df-40e6-9b11-5b8f64e5cb23
            L = c.general_search("4bd6eef6-99df-40e6-9b11-5b8f64e5cb23", '', 0)
            if L:
                if str(L[0])=='200':
                    print('Series found: '+str(L[1]['TotalResults'])+'') 
                    wp.add(jp.P(text='Series found: '+str(L[1]['TotalResults'])+'', classes='m-2'))
                
                    #create table grid for results
                    grid_options = GetGridOptions()
                    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 350px;width: 1100px;margin: 0.1em;') #style='height: 200px; width: 300px; margin: 0.25em'
                    grid.html_columns = [5] 
                    
                    for item in L[1]['Results']:
                        #print(item)
                        #print('')
                        
                        agency = item['AgencyId']
                        Id = item['Identifier'] 
                        Version = item['Version'] 
                        
                        Name = ''
                        if 'de' in item['ItemName']: Name = item['ItemName']['de'] 
                        NameEN = ''
                        if 'en' in item['ItemName']: NameEN = item['ItemName']['en'] 
                        #Summary = ''
                        #if 'de' in item['Summary']: Summary = item['Summary']['de']
                        #SummaryEN = ''                        
                        #if 'en' in item['Summary']: SummaryEN = item['Summary']['en'] 
                        
                        DetailsLink = '<u><a href=/studies/' + agency + '/' + Id + '>Show studies</a></u>'

                        #row = {'Agency': agency, 'ID': Id, 'Version': Version, 'Name': Name, 'NameEN': NameEN, 'Summary': Summary, 'SummaryEN': SummaryEN, 'Details': DetailsLink}
                        row = {'Agency': agency, 'ID': Id, 'Version': Version, 'Name': Name, 'NameEN': NameEN, 'Details': DetailsLink}
                        grid.options.rowData.append(row)    
                    
                else:
                    print('Error, status ' + str(L[0]))
                    wp.add(jp.P(text='Error, status ' + str(L[0]), classes='m-2'))
                    
            else:
                wp.add(jp.P(text='Error, no series found', classes='m-2'))
        
        else:
            wp.add(jp.P(text='You are not logged in.', classes='m-2'))

    except Exception as e: 
        print('Error in ' + __file__)
        print('Error '+str(e))        
        print(traceback.format_exc())
    
    return wp

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
              {headerName: "Agency", field: "Agency"},
              {headerName: "ID", field: "ID"},
              {headerName: "Version", field: "Version"},
              {headerName: "Name", field: "Name"},
              {headerName: "NameEN", field: "NameEN"},
              {headerName: "Details", field: "Details"}
              
            ],
              rowData: []
        }
        """

#              {headerName: "Summary", field: "Summary"}
#              {headerName: "SummaryEN", field: "SummaryEN"}
        
    return grid_options
