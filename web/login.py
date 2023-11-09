"""
    colstudies application
"""

import json
import justpy as jp
import globalvars as g

import colecticaapi as c


def login(request):
    # login form submitted, check if Colectica accepts and return token
    def submit_form(self, msg):
        # print(msg.form_data)
        # msg.page.redirect = '/form_submitted'
        # session_data[msg.session_id] = msg.form_data

        myusername = ""
        mypassword = ""
        # parse from data
        for field in msg.form_data:
            if field.type in ["text"]:
                myusername = field.value
            if field.type in ["password"]:
                mypassword = field.value

        tokenHeader = c.get_jwtToken(g.colecticahostname, myusername, mypassword)
        if tokenHeader == "":
            g.session_data["tokenHeader"] = ""
            g.session_data["userName"] = ""
            g.loggedin = False
            txtmsg = "Your login has failed."
            g.status == "failedLogin"
            print(txtmsg)
            loginstatus.text = txtmsg
            wp.page.update()

        else:
            g.session_data["tokenHeader"] = tokenHeader
            g.session_data["userName"] = myusername
            g.loggedin = True
            txtmsg = "You have successfully logged in."
            g.status == "successLogin"
            print(txtmsg)
            loginstatus.text = txtmsg
            loginform.classes = "hidden"
            msg.page.redirect = "/studies"

    # reset loginstatus message
    def reset_formmessage(self, msg):
        loginstatus.text = txtmsg
        wp.page.update()

    txtmsg = ""

    # create page
    wp = g.templatewp()

    if not g.loggedin:
        if g.status == "failedLogin":
            Message = jp.P(
                text="Login not successful",
                a=wp,
                classes="block uppercase tracking-wide text-red-700 text-xs font-bold mb-2",
            )

        elif g.status == "":
            loginform = jp.Form(a=wp, classes="border m-1 p-1 w-64")
            Formtitle = jp.P(text="Login with your Colectica account", a=loginform)

            user_label = jp.Label(
                text="User Name",
                classes="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2",
                a=loginform,
            )
            usern = jp.Input(placeholder="User Name", a=loginform, classes="form-input")
            user_label.for_component = usern

            password_label = jp.Label(
                classes="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 mt-2",
                a=loginform,
            )
            jp.Div(
                text="Password",
                classes="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2",
                a=password_label,
            )
            passw = jp.Input(
                placeholder="Password",
                a=password_label,
                classes="form-input",
                type="password",
            )

            # check_label = jp.Label(classes='text-sm block', a=loginform)
            # jp.Input(type='checkbox', a=check_label, classes='form-checkbox text-blue-500')
            # jp.Span(text='Send me stuff', a=check_label, classes= 'ml-2')

            submit_button = jp.Input(
                value="Login", type="submit", a=loginform, classes=g.button
            )

            loginform.on("submit", submit_form)

            loginform.on("click", reset_formmessage)

            if not g.colecticausername == "" and not g.colecticapassword == "":
                usern.value = g.colecticausername
                passw.value = g.colecticapassword
                # user still needs to click on submit button
                submit_form

        elif g.status == "successLogin":
            Message = jp.P(
                text="Login successful",
                a=wp,
                classes="block uppercase tracking-wide text-red-700 text-xs font-bold mb-2",
            )

    else:
        if g.status == "successLogin":
            wp.add(jp.P(text="You have successfully logged in."))

        else:
            # if already logged in before
            wp.add(jp.P(text="You are logged in."))

    loginstatus = jp.Span(text="", a=wp, classes="text-red-700")

    return wp


def logout(request):
    # delete token from session
    g.session_data["tokenHeader"] = ""
    g.session_data["userName"] = ""
    g.loggedin = False

    # create page
    wp = g.templatewp()
    wp.add(jp.P(text="You have been logged out"))

    return wp
