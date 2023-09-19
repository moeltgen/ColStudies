"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g

import colecticaapi as c 
import util.edxml as ed
import util.dara as dara 
import os 
    
def study(request):
    
    
    #register form submitted
    def submit_form(self, msg):
        if g.darausername=='' or g.darapassword=='':
            resulttext = "No username or password for da|ra supplied in settings.py"
            print(resulttext)
            registerstatus.text = resulttext
        else:
            print('Form submitted for registration of DOI')
            resulttext = dararegister(agency, Id)
            registerstatus.text = resulttext
        
        wp.page.update()
        
    #start page     
    wp = g.templatewp()
    
    if g.loggedin:
        agency = request.path_params["agency"]
        Id = request.path_params["id"]
        
        wp.add(jp.P(text='Searching for study with agency ' + agency + ' and id ' + Id, classes='m-2'))
        
                
        myddixml = {}
        
        #create table grid for study 
        ###
        grid_options = GetGridOptions("StudyGrid")
        grid = jp.AgGrid(a=wp, options=grid_options, style='height: 320px;width: 800px;margin: 0.1em;' ) #style='height: 200px; width: 300px; margin: 0.25em'
        grid.html_columns = [1,2]
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
                AddGridRows(grid, agency, Id, Version, result, "StudyGrid")

                #create table grid for DOI info
                wp.add(jp.P(text='DOI Info ', classes='m-2'))
                grid_options = GetGridOptions("DOIGrid")
                grid2 = jp.AgGrid(a=wp, options=grid_options, style='height: 150px;width: 800px;margin: 0.1em;' ) #style='height: 200px; width: 300px; margin: 0.25em'
                grid2.html_columns = [1,2]
                AddGridRows(grid2, agency, Id, Version, result, "DOIGrid")
                
                
                #Form to register
                registerform = jp.Form(a=wp, classes='border m-1 p-1')
                registerstatus = jp.Span(text='', a=registerform, classes='text-red-700 whitespace-pre font-mono') 
                submit_button = jp.Input(value='register/update DOI', type='submit', a=registerform, classes=g.button)
                registerform.on('submit', submit_form)
                
                
                
            else:
                print('Error get_an_item, status ' + str(result[0]))
                wp.add(jp.P(text='Error get_an_item, status ' + str(result[0]), classes='m-2'))
    
        
    return wp
    
def AddGridRows(grid, agency, Id, Version, result, gridType):
    #gridType: StudyGrid, DOIGrid or DOIProposalGrid
    
    myddixml = {}
    if result[1]['Item'] is not None:
        myddixml[Id]=result[1]['Item']
        #print(myddixml[Id]) #contains Fragment with StudyUnit
        
        StudyNo=ed.getStudyNo(myddixml[Id])
        #use Dataset: StudyDOI=ed.getStudyDOI(myddixml[Id])
        #use Dataset: StudyVersion=ed.getStudyVersion(myddixml[Id])
        Version=ed.getVersion(myddixml[Id])
        #print(StudyNo, StudyVersion, StudyDOI)
        
        #Get the PhysicalInstanceReference
        addxml=''
        pixml=''
        ref = ed.get_reference(myddixml[Id], './/StudyUnit/PhysicalInstanceReference')
        itm = c.get_an_item_version(ref['Agency'], ref['ID'], ref['Version'])
        if itm is not None:
            if 'Item' in itm[1]:
                addxml=itm[1]['Item']
        if not addxml=='':
            ##new functions in ed.: 
            StudyDOI = ed.getDatasetDOI(addxml)
            StudyVersion = ed.getDatasetVersion(addxml)
            #print(StudyDOI, StudyVersion)
        else:
            print('No PhysicalInstanceReference found!')
        
        #default URL https://search.gesis.org/research_data/ZA3811?doi=10.4232/1.3811
        #
        #set default URL here - is not editable in Colectica Designer at the moment
        #
        #        
        StudyURL = 'https://search.gesis.org/research_data/' + StudyNo + '?doi=' + StudyDOI
        

        
        ##new functions in ed.: 
        Title = ed.getStudyTitle(myddixml[Id], 'de') 
        TitleEN = ed.getStudyTitle(myddixml[Id], 'en')
        Abstract = ed.getAbstract(myddixml[Id], 'de') 
        AbstractEN = ed.getAbstract(myddixml[Id], 'en')
                
        
    else:
        print('Error get_an_item, no Item, status ' + str(result[0]))
        wp.add(jp.P(text='Error get_an_item, no Item, status ' + str(result[0]), classes='m-2'))
    
    if gridType=='DOIProposalGrid':
        #create a proposal with default values
        prefix = "10.17889"                     #dara test prefix 
        StudyVersion = "1.0.0"                  #start with 1.0.0 
        StudyDOI = "https://doi.org/" +prefix + "/" + StudyNo + "." + StudyVersion        
        StudyURL = 'https://search.gesis.org/research_data/' + StudyNo + '?doi=' + StudyDOI
    else:
        StudyDOI = "https://doi.org/" + StudyDOI    
    
    if not StudyDOI=='':
        StudyDOILink = '<a href=' + StudyDOI + '>' + StudyDOI + '</a>'
    if not StudyURL=='':
        StudyURLLink = '<a href=' + StudyURL + '>' + StudyURL + '</a>'
        
    DetailsLink = ''
                        
    #add fields                   
    if gridType=='StudyGrid':
        row = {'Field': 'Agency', 'Value': agency, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        row = {'Field': 'ID', 'Value': Id, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        row = {'Field': 'Version', 'Value': Version, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        
        row = {'Field': 'Title', 'Value': Title, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        row = {'Field': 'TitleEN', 'Value': TitleEN, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        
        
        row = {'Field': 'StudyNo', 'Value': StudyNo, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        row = {'Field': 'StudyVersion', 'Value': StudyVersion, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        row = {'Field': 'StudyDOI', 'Value': StudyDOILink, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        
        row = {'Field': 'Abstract', 'Value': Abstract, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        row = {'Field': 'AbstractEN', 'Value': AbstractEN, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
    elif gridType=='DOIGrid' or gridType=='DOIProposalGrid':
        
        # in case of DOIGrid: show link to view dara xml 
        showdaraxmllink = ''
        if gridType=='DOIGrid': 
            showdaraxmllink = '/study/daraxml/' + agency + '/' + Id
            showdaraxmllink = '<a href=' + showdaraxmllink + '>Show da|ra xml</a>'
    
        row = {'Field': 'StudyNo', 'Value': StudyNo, 'Details': showdaraxmllink}
        grid.options.rowData.append(row)  
        row = {'Field': 'StudyVersion', 'Value': StudyVersion, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        row = {'Field': 'StudyDOI', 'Value': StudyDOILink, 'Details': DetailsLink}
        grid.options.rowData.append(row)  
        
        # in case of DOIGrid: show note for URL 
        showurlnote = ''
        if gridType=='DOIGrid': 
            showurlnote = '(not from DDI)'
    
        row = {'Field': 'StudyURL', 'Value': StudyURLLink, 'Details': showurlnote}
        grid.options.rowData.append(row)  
    

def GetGridOptions(GridType):
    
    if GridType=="StudyGrid" or GridType=="DOIGrid":
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
    else:
        grid_options = ""
        
    return grid_options
    

    
#route: /study/daraxml/{agency}/{id}
def daraxml(request):
    """
    show page to load the dara xml and show it 
    """

    wp = g.templatewp()
    
    
    if g.loggedin:
        agency = request.path_params["agency"]
        Id = request.path_params["id"]
        
                
        jp.Br(a=wp)
        jp.Br(a=wp)
        wp.add(jp.P(text='Show da|ra XML for study with agency ' + agency + ' and id ' + Id, classes='m-2 font-bold'))
        jp.Br(a=wp)
        jp.Br(a=wp)
        
        
        xmltext = jp.Div(text='dara xml', classes='whitespace-pre font-mono', a=wp) #xml will go here 
                 
        daraxml  = get_daraxml(agency, Id)
        xmltext.text = daraxml 
        jp.run_task(wp.update()) 
        
    return wp



    
 
def dararegister(agency, Id):
    """
    post the daraxml to the dara API to register the DOI
    """
    
    xmltext = ''
    
    if g.loggedin:
        xmltext = 'dara xml \n'
                 
        daraxml  = get_daraxml(agency, Id)
        xmltext += ' - built successfully \n'
        print('daraxml built successfully ')
        
        
        outdir = 'out'
        xmlfile = 'dara_'+str(Id)+'.xml' # xml file name
        
        xmltext += ' - call register_dara(create or update) at ' + g.daraapi + ' \n'
        print('call register_dara(create or update) at ' + g.daraapi)
        
        #todo: IS currently DRAFT at da|ra!
        
        regresult = dara.register_dara(os.path.join(outdir, xmlfile), g.daraapi, g.darausername, g.darapassword) #call the registration api #get settings from globalvars.py 
        xmltext += ' - Result: ' + regresult + ' \n'
        print(regresult)
                        
    else:
        xmltext = 'not logged in'
                
    return xmltext



def getCVCollection(ddixml, methxml):
    """
    build the CVCollection object to hold all Controlled Vocabularies 
    """

                            
    Limit = 3 #temp for development
    #Limit = 9999 #for production
    
    
    CVCollection = {}
    
    #Subjects 
    CV = ed.buildCV(ddixml, './/StudyUnit/Coverage/TopicalCoverage/Subject', Limit)
    CVCollection['Subject'] = CV
    
    if not methxml=='':
        #TypeOfDataCollectionMethodology                            
        CV = ed.buildCV(methxml, './/Methodology/DataCollectionMethodology/TypeOfDataCollectionMethodology', Limit)
        CVCollection['TypeOfDataCollectionMethodology'] = CV
        
        #TypeOfSamplingProcedure                            
        CV = ed.buildCV(methxml, './/Methodology/SamplingProcedure/TypeOfSamplingProcedure', Limit)
        CVCollection['TypeOfSamplingProcedure'] = CV
        
        #TypeOfTimeMethod                            
        CV = ed.buildCV(methxml, './/Methodology/TimeMethod/TypeOfTimeMethod', Limit)
        CVCollection['TypeOfTimeMethod'] = CV
    else:
        CVCollection['TypeOfDataCollectionMethodology'] = []
        CVCollection['TypeOfSamplingProcedure'] = []
        CVCollection['TypeOfTimeMethod'] = []
    
    #AnalysisUnit                            
    CV = ed.buildCV(ddixml, './/StudyUnit/AnalysisUnit', Limit)
    CVCollection['AnalysisUnit'] = CV
    
    #KindOfData                            
    CV = ed.buildCV(ddixml, './/StudyUnit/KindOfData', Limit)
    CVCollection['KindOfData'] = CV
                               
    
    return CVCollection


def get_daraxml(agency, Id): 
    """
    get the dara xml for a study with metadata from the Colectica API 
    """
    
    daraxml =''
    
    myddixml = {}
    combined_xml = {}
    result = c.get_an_item(agency, Id)  
    if str(result[0])=='200':
        print('Study found: '+ Id)                                     
        Version=result[1]['Version']
        if result[1]['Item'] is not None:
            myddixml[Id]=result[1]['Item']
            
            
            #build the combined ddi xml, including all referenced items 
            combined_xml[Id] = '<ddi:FragmentInstance xmlns:ddi="ddi:instance:3_3" \
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
            xsi:schemaLocation="ddi:instance:3_3 http://www.ddialliance.org/Specification/DDI-Lifecycle/3.3/XMLSchema/instance.xsd">\n' #start wrapper
            
            combined_xml[Id] += myddixml[Id] #add StudyUnit xml 
            
            
            StudyNo=ed.getStudyNo(myddixml[Id])
            
            # get also the referenced items to build CVs used there 
            methxml='' 
            dcxml=''
            
            ref = ed.get_reference(myddixml[Id], './/StudyUnit/DataCollectionReference')
            itm = c.get_an_item_version(ref['Agency'], ref['ID'], ref['Version'])
            if itm is not None:
                if itm[1] is not None:
                    if 'Item' in itm[1]:
                        addxml=itm[1]['Item']
                        dcxml = addxml
                        combined_xml[Id] += '\n' + dcxml
                if not dcxml=='':
                    #MethodologyReference within DataCollection
                    ref = ed.get_reference(dcxml, './/DataCollection/MethodologyReference')
                    itm = c.get_an_item_version(ref['Agency'], ref['ID'], ref['Version'])
                    if itm is not None:
                        if itm[1] is not None:
                            if 'Item' in itm[1]:
                                addxml=itm[1]['Item']
                                methxml = addxml
                                combined_xml[Id] += '\n' + methxml
                                #print('MethodologyReference found')    
            if dcxml=='':
                print('No DataCollectionReference found')    
            if methxml=='':
                print('No MethodologyReference found')    

            # get also the referenced dataset to get StudyDOI 
            phyxml=''
            ref = ed.get_reference(myddixml[Id], './/StudyUnit/PhysicalInstanceReference')
            itm = c.get_an_item_version(ref['Agency'], ref['ID'], ref['Version'])
            if itm is not None:
                if itm[1] is not None:
                    if 'Item' in itm[1]:
                        addxml=itm[1]['Item']
                        phyxml = addxml
                        combined_xml[Id] += '\n' + phyxml
                
            if not phyxml=='':
                ##new functions in ed.: 
                StudyDOI = ed.getDatasetDOI(phyxml)
                StudyVersion = ed.getDatasetVersion(phyxml)
                print(StudyDOI, StudyVersion)
            else:
                print('No PhysicalInstanceReference found')    
            
            combined_xml[Id] += '\n</ddi:FragmentInstance>' #end wrapper
            
    StudyURL = 'https://search.gesis.org/research_data/' + StudyNo + '?doi=' + StudyDOI
            
            

    if True:
        outdir = 'out'
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        xmlfile = 'dara_'+str(Id)+'.xml' # xml file name
        
        CVCollection = getCVCollection(myddixml[Id], methxml)
        
        
        #write dara xml to file (use the combined_xml[Id] here; StudyURL needs to be injected - is not in DDIxml )
        dara.write_daraxml_fromddixml(os.path.join(outdir, xmlfile), combined_xml[Id], CVCollection, StudyURL) 
        print('createdara: ' + Id + ' '+str(xmlfile)+'')
        
        #read the created file
        f = open(os.path.join(outdir, xmlfile), 'r', encoding='utf-8')
        daraxml = f.read()
        f.close()
    
    return daraxml
