"""
    colstudies application
"""

import justpy as jp
import globalvars as g
import traceback
import colecticaapi as c
import util.edxml as ed


def search(request):
    wp = g.templatewp()


    #searchform submitted
    def submit_searchform(self, msg):
        for field in msg.form_data:
            if field.type in ["text"]:
                searchterm = field.value
            if field.type in ["checkbox"]:
                display = field.checked

        print("Searching in Colectica for", searchterm)
        
        #search for studies 
        result = c.general_search("30ea0200-7121-4f01-8d21-a931a182b86d", searchterm, 0) #use 10 to return max 10 results (0 for all)

        if str(result[0]) == "200":
            
            numResults = result[1]['TotalResults']
            
            print("Found: " + str(numResults))
            xmlstatus.text = "Updating... " + str(numResults)
            
            
            counter=0
            grid.options.rowData = []
            
            for item in result[1]["Results"]:
                #print(item)
                #print('')
                agency = item["AgencyId"]
                Id = item["Identifier"]
                Version = item["Version"]
                
                #print(agency, Id, Version)
                
                #get StudyNo if available  
                counter += 1
                StudyNo=""
                if display:
                    if not counter > 50: # lasts too long for 6000 studies 
                        studyresult = c.get_an_item(agency, Id)
                        if str(studyresult[0]) == "200":
                            if studyresult[1]["Item"] is not None:
                                StudyNo = ed.getStudyNo(studyresult[1]["Item"])
               

                include = True
                
                if include:
                    title = ""
                    titleEN = ""
                    titles = item["ItemName"]
                    for lang in titles:
                        if lang == "de":
                            title = item["ItemName"][lang]
                        if lang == "en":
                            titleEN = item["ItemName"][lang]
                    
                    
                    DetailsLink = (
                        "<u><a href=/study/"
                        + agency
                        + "/"
                        + Id
                        + ">Details</a></u>"
                    )

                    row = {
                        "Agency": agency,
                        "ID": Id,
                        "Version": Version,
                        "Title": title,
                        "TitleEN": titleEN,
                        "Details": DetailsLink,
                        "StudyNo": StudyNo,
                    }
                    grid.options.rowData.append(row)
                
            xmlstatus.text = "Found: " + str(numResults)
            
        else:
            print("Error: " + str(result[0]))
            xmlstatus.text = "Error: " + str(result[0]) + "\n" + str(result[1])

        wp.page.update()
    
    def reset_searchform(self, msg):
        xmlstatus.text = "Reset"
        wp.page.update()


    try:
        if g.loggedin:
            msg = "Searching for studies"

            wp.add(jp.P(text=msg, classes="m-2"))
            
            input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-blue-500"

            #Form to search
            searchform = jp.Form(a=wp, classes='border m-1 p-1')
            term = jp.Input(type='text', a=searchform, classes=input_classes, placeholder='Enter term')
            
            label = jp.Label(a=searchform, classes='m-2 p-2 inline-block')
            check = jp.Input(type='checkbox', a=searchform, classes='m-2 p-2 inline-block')
            
            caption = jp.Span(text='Display StudyNo in results (may take longer)', a=label)
    
            searchformsubmit_button = jp.Input(value='Search in Colectica', type='submit', a=searchform, classes=g.starbutton)
            searchform.on('submit', submit_searchform)
            searchform.on("click", reset_searchform)
            
                
            # get all studies 30ea0200-7121-4f01-8d21-a931a182b86d
            # or use a search term 
            
            #L = c.general_search("30ea0200-7121-4f01-8d21-a931a182b86d", "Stefan", 0)
            if True:
                if True:
                #if str(L[0]) == "200":
                    #print("Studies total: " + str(L[1]["TotalResults"]) + "")
                    

                    # create table grid for results
                    grid_options = GetGridOptions()
                    grid = jp.AgGrid(
                        a=wp,
                        options=grid_options,
                        style="height: 350px;width:1500px;margin: 0.1em;",
                    )  # style='height: 200px; width: 300px; margin: 0.25em'
                    grid.html_columns = [5]
                    
                    # see https://v2.tailwindcss.com/docs/width
                    grid.options.columnDefs[3].cellClass = ["w-80"]  # width .w-56	width: 14rem;
                    grid.options.columnDefs[4].cellClass = ["w-80"]  # width
                    # grid.options.columnDefs[5].cellClass = ['hover:bg-blue-500']
                    
                
                    xmlstatus = jp.Span(
                        text="",
                        a=searchform,
                        classes="text-red-700 whitespace-pre font-mono",
                    )


                #else:
                #    print("Error, status " + str(L[0]))
                #    wp.add(jp.P(text="Error, status " + str(L[0]), classes="m-2"))
            else:
                wp.add(jp.P(text="Error, no studies found", classes="m-2"))

        else:
            wp.add(jp.P(text="You are not logged in to Colectica.", classes="m-2"))
    
        wp.add(
            jp.Div(text="StudyNo is displayed only for up to 50 studies only")
            )
            
    except Exception as e:
        print("Error in " + __file__)
        print("Error " + str(e))
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
              {headerName: "Title", field: "Title"},
              {headerName: "TitleEN", field: "TitleEN"},
              {headerName: "Details", field: "Details"},
              {headerName: "StudyNo", field: "StudyNo"}
              
            ],
              rowData: []
        }
        """

    return grid_options
