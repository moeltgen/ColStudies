"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g


#modules for routes
import login
import series
import studies
import study
import doiinfo 
import fileinfo
import starinfo
import annotations



def home():
    #create web page 
    wp = g.templatewp()
    
    jp.Br(a=wp) 
    wp.add(jp.P(text='Welcome. This is where you manage the Colectica studies. '))
    jp.Br(a=wp) 
    wp.add(jp.P(text='- Studies will show all studies of the Colectica Repository. You can then select a study to perform actions.')) 
    wp.add(jp.P(text='- Series will show all series of the Colectica Repository. You can then show all studies within a series.')) 
    wp.add(jp.P(text='- Actions include registration of DOIs with da|ra and managing file download permissions with DBKEdit.')) 
    jp.Br(a=wp)
    wp.add(jp.P(text='Settings can  be modified in settings.py (restart needed).')) 
    jp.Br(a=wp)
    
    if g.loggedin:
        wp.add(jp.P(text='Choose a menu item.')) 
        
    else:
        wp.add(jp.P(text='After logging in, you can see a list of studies.'))
    
    jp.Br(a=wp)
    
        
    return wp

#start application server
print('')
print('Start Application ' + g.appname)
print('Version ' + g.appversion)
print('')




#add routes 
jp.Route('/login', login.login)
jp.Route('/logout', login.logout)
jp.Route('/studies', studies.studies)
jp.Route('/studies/{agency}/{id}', studies.studies) 
jp.Route('/series', series.series)

jp.Route('/study/{agency}/{id}', study.study)
jp.Route('/doiinfo/{agency}/{id}', doiinfo.doiinfo)
jp.Route('/fileinfo/{agency}/{id}', fileinfo.fileinfo)
jp.Route('/starinfo/{agency}/{id}', starinfo.starinfo)
jp.Route('/annotations/{agency}/{id}', annotations.annotations)

print("Warning: urllib3.disable_warnings() is set - communication is not encrypted!")

#start application server with home page 
#set host and port in justpy.env
#jp.justpy(home, host='127.0.0.1', port='1278') 


print('')
print('Config vars from settings.py')
if not g.colecticahostname=='': 
    print('  - colecticahostname: ' + g.colecticahostname)
    g.colecticahosthoststatus = g.checkhost(g.colecticahostname)
    if not g.colecticahosthoststatus=='': 
        print('  - ' + g.colecticahosthoststatus)
    else:
        print('  - Colectica host is reachable on port 80')
else:
    print('  - colecticahostname not configured!')
if not g.colecticausername=='': print('  - colecticausername is set')
if not g.colecticapassword=='': print('  - colecticapassword is set')




print('')


jp.justpy(home) 

