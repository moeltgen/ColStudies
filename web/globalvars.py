"""
    colstudies application
"""

import json
import justpy as jp
import settings #api settings and login data stored in file settings.py 
import socket
import menu
    
appname = 'ColStudies'
appversion = '0.2'
session_data = {}
loggedin = False 
status = ''
colecticahosthoststatus = ''

#settings 
colecticahostname = settings.colecticahostname 
colecticausername = settings.colecticausername
colecticapassword = settings.colecticapassword

#classes 
button = 'm-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700 rounded-full ' #flex items-center'

menuul = 'flex;'
menuli = 'mr-3'
menua = 'inline-block border border-blue-500 rounded py-1 px-3 bg-blue-500 text-white'


    
def templatewp():
    
    wp = jp.WebPage()
    wp.title = appname
    wp.favicon = 'favicon.ico'
    wp.css = 'body { font-family: sans-serif; background-color: rgb(219,234,254); margin: 10px; padding: 5px; }'
    
    wp.add(jp.P(text='ColStudies', classes='font-mono  text-3xl')) # p-1 m-2 bg-blue-100
        
    #build menu
    menu.menu(wp)
    
    
    return wp 

def checkhost(hostname):
    #check if host is reachable
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hostname, 80))
    except Exception as e: # work on python 3.x
        colecticahosthoststatus = "Error: Colectica host not reachable on port 80, " + str(e)
    else:
        colecticahosthoststatus = "" #"Colectica host is reachable on port 80" 
    finally:
        return colecticahosthoststatus