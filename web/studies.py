"""
    colstudies application
"""

import justpy as jp
import globalvars as g
import traceback
import colecticaapi as c
import util.edxml as ed


def studies(request):
    wp = g.templatewp()

    try:
        if g.loggedin:
            SeriesAgency = ""
            SeriesId = ""
            if "agency" in request.path_params:
                SeriesAgency = request.path_params["agency"]
            if "id" in request.path_params:
                SeriesId = request.path_params["id"]

            if not SeriesAgency == "" and not SeriesId == "":
                msg = "Searching for studies of series with id " + SeriesId
                result = c.get_an_item(SeriesAgency, SeriesId)
                if str(result[0]) == "200":
                    if result[1]["Item"] is not None:
                        # print(result[1]['Item'])
                        # print('')
                        SeriesXML = result[1]["Item"]
                        refliststudies = ed.get_referencelist(
                            SeriesXML, ".//Group/StudyUnitReference"
                        )
                        msg += " (found " + str(len(refliststudies)) + " studies)"
                        print("Studies in group: " + str(len(refliststudies)))

            else:
                msg = "Searching for studies"

            wp.add(jp.P(text=msg, classes="m-2"))

            # get all studies 30ea0200-7121-4f01-8d21-a931a182b86d
            L = c.general_search("30ea0200-7121-4f01-8d21-a931a182b86d", "", 0)
            if L:
                if str(L[0]) == "200":
                    print("Studies total: " + str(L[1]["TotalResults"]) + "")
                    wp.add(
                        jp.P(
                            text="Studies total: " + str(L[1]["TotalResults"]) + "",
                            classes="m-2",
                        )
                    )

                    # myddixml = {}

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
                    
                    #counter=0
                    for item in L[1]["Results"]:
                        #print(item)
                        #print('')
                        agency = item["AgencyId"]
                        Id = item["Identifier"]
                        Version = item["Version"]
                        
                        #get StudyNo if available  
                        #counter += 1
                        StudyNo=""
                        #if not counter > 25: # lasts too long for 6000 studies 
                        #    studyresult = c.get_an_item(agency, Id)
                        #    if str(studyresult[0]) == "200":
                        #        if studyresult[1]["Item"] is not None:
                        #            StudyNo = ed.getStudyNo(studyresult[1]["Item"])
                       

                        include = True
                        if not SeriesAgency == "" and not SeriesId == "":
                            # check if study is referenced by selected group/series
                            include = False
                            for ref in refliststudies:
                                if ref["Agency"] == agency and ref["ID"] == Id:
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
                                # "StudyNo": StudyNo,
                            }
                            grid.options.rowData.append(row)

                else:
                    print("Error, status " + str(L[0]))
                    wp.add(jp.P(text="Error, status " + str(L[0]), classes="m-2"))
            else:
                wp.add(jp.P(text="Error, no studies found", classes="m-2"))

        else:
            wp.add(jp.P(text="You are not logged in to Colectica.", classes="m-2"))
    
        #wp.add(
        #    jp.Div(text="StudyNo is displayed only for up to 25 studies")
        #    )
            
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
              {headerName: "Details", field: "Details"}
              
            ],
              rowData: []
        }
        """

    return grid_options
