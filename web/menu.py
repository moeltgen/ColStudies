"""
    colstudies application
"""

import justpy as jp
import globalvars as g


def menu(wp):
    # login status
    if "userName" in g.session_data:
        userName = g.session_data["userName"]
    else:
        userName = ""
        
    # DBK login status
    if "DBKUserName" in g.session_data:
        DBKUserName = g.session_data["DBKUserName"]
    else:
        DBKUserName = ""
        

    jp.Hr(a=wp)
    # -------------

    jp.Br(a=wp)

    menudiv = jp.Div(text="", a=wp, classes=g.menuul)

    # Button Home
    jp.A(text="Home", href="/", a=menudiv, classes=g.button)
    
    #div = jp.Div(text="", a=menudiv)
    #p = jp.P(text=" ", a=menudiv)
    
    if not userName == "":
        # Button Studies
        jp.A(text="Studies", href="/studies", a=menudiv, classes=g.button)
        # Button Series
        jp.A(text="Series", href="/series", a=menudiv, classes=g.button)
        # Button Search
        jp.A(text="Search", href="/search", a=menudiv, classes=g.button)
        
        #div = jp.Div(text="", a=menudiv)
        #p = jp.P(text=" ", a=menudiv)
        
        # Button Logout
        jp.A(text="ColecticaLogout", href="/logout", a=menudiv, classes=g.button)

    else:
        # Button Login
        jp.A(text="ColecticaLogin", href="/login", a=menudiv, classes=g.button)


    if not DBKUserName == "":
        # Button Logout
        jp.A(text="DBKLogout", href="/dbklogout", a=menudiv, classes=g.button)

    else:
        # DBK Button Login
        jp.A(text="DBKLogin", href="/dbklogin", a=menudiv, classes=g.button)

    # jp.Br(a=wp)

    # show login status
    if not userName == "":
        jp.Div(text=str(g.colecticahostname), a=wp, classes="text-right")
        jp.Div(text="logged in as " + str(userName), a=wp, classes="text-right")
        jp.Br(a=wp)
    else:
        jp.Div(text=str(g.colecticahostname), a=wp, classes="text-right")
        jp.Div(text="not logged in", a=wp, classes="text-right")
        jp.Br(a=wp)

    if not g.colecticahosthoststatus == "":
        jp.Div(text=g.colecticahosthoststatus, a=wp, classes="text-right")

    jp.Hr(a=wp)
    # -------------

    # show DBK login status
    if not DBKUserName == "":
        jp.Div(text=str("DBKEdit"), a=wp, classes="text-right")
        jp.Div(text="logged in as " + str(DBKUserName), a=wp, classes="text-right")
        jp.Br(a=wp)
    else:
        jp.Div(text=str("DBKEdit"), a=wp, classes="text-right")
        jp.Div(text="not logged in", a=wp, classes="text-right")
        jp.Br(a=wp)

    jp.Hr(a=wp)
    # -------------

    jp.Br(a=wp)
    jp.Strong(text="Welcome to " + g.appname + " " + g.appversion, a=wp)

    jp.Hr(a=wp)
    jp.Br(a=wp)
    # -------------
    return wp
