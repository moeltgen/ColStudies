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



def home():
    #create web page 
    wp = g.templatewp()
    
    if g.loggedin:
        wp.add(jp.P(text='Welcome. Choose a menu item.')) 
    else:
        wp.add(jp.P(text='Welcome. This is where you manage the Colectica studies. After logging in, you can see a list of studies.'))
    
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
jp.Route('/series', series.series)


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

