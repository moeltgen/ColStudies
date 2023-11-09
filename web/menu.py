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

    jp.Hr(a=wp)
    # -------------

    jp.Br(a=wp)

    menudiv = jp.Div(text="", a=wp, classes=g.menuul)

    # Button Home
    jp.A(text="Home", href="/", a=menudiv, classes=g.button)

    if not userName == "":
        # Button Studies
        jp.A(text="Studies", href="/studies", a=menudiv, classes=g.button)
        # Button Series
        jp.A(text="Series", href="/series", a=menudiv, classes=g.button)
        # Button Logout
        jp.A(text="Logout", href="/logout", a=menudiv, classes=g.button)

    else:
        # Button Login
        jp.A(text="Login", href="/login", a=menudiv, classes=g.button)

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

    jp.Br(a=wp)
    jp.Strong(text="Welcome to " + g.appname, a=wp)

    jp.Hr(a=wp)
    jp.Br(a=wp)
    # -------------
    return wp
