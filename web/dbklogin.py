"""
    colstudies application
"""

import justpy as jp
import globalvars as g

import dbkeditapi as d


def login(request):
    # login form submitted, check if DBKEdit accepts and return token
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
        
        #print('myusername', myusername)
        #print('mypassword', mypassword)
        
        result =  d.LoginTest(myusername, mypassword)
        
        if result[0] == "0":
            g.session_data["DBKUserName"] = ""
            g.dbkloggedin = False
            txtmsg = "Your login to DBKEdit has failed."
            g.dbkstatus == "failedLogin"
            print(txtmsg)
            loginstatus.text = txtmsg
            wp.page.update()

        else:
            g.session_data["DBKUserName"] = myusername
            g.dbkeditusername=myusername
            g.dbkeditpassword=mypassword
            g.dbkloggedin = True
            txtmsg = "You have successfully logged in to DBKEdit."
            g.dbkstatus == "successLogin"
            print(txtmsg)
            loginstatus.text = txtmsg
            loginform.classes = "hidden"
            msg.page.redirect = "/dbklogin"
        
        
    # reset loginstatus message
    def reset_formmessage(self, msg):
        loginstatus.text = txtmsg
        wp.page.update()

    txtmsg = ""

    # create page
    wp = g.templatewp()
    
    
    
    if not g.dbkloggedin:
        if g.dbkstatus == "failedLogin":
            Message = jp.P(
                text="Login not successful",
                a=wp,
                classes="block uppercase tracking-wide text-red-700 text-xs font-bold mb-2",
            )

        elif g.dbkstatus == "":
            loginform = jp.Form(a=wp, classes="border m-1 p-1 w-64")
            Formtitle = jp.P(text="Login with your DBKEdit account", a=loginform)

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
                value="DBKLogin", type="submit", a=loginform, classes=g.button
            )

            loginform.on("submit", submit_form)

            loginform.on("click", reset_formmessage)

            if not g.dbkeditusername == "" and not g.dbkeditpassword == "":
                usern.value = g.dbkeditusername
                passw.value = g.dbkeditpassword
                # user still needs to click on submit button
                submit_form

        elif g.dbkstatus == "successLogin":
            Message = jp.P(
                text="Login successful",
                a=wp,
                classes="block uppercase tracking-wide text-red-700 text-xs font-bold mb-2",
            )

    else:
        if g.dbkstatus == "successLogin":
            wp.add(jp.P(text="You have successfully logged in to DBKEdit."))

        else:
            # if already logged in before
            wp.add(jp.P(text="You are logged in to DBKEdit."))

    loginstatus = jp.Span(text="", a=wp, classes="text-red-700")

    return wp


def logout(request):
    # delete token from session
    g.session_data["DBKUserName"] = ""
    g.dbkloggedin = False
    
    g.dbkeditusername=""
    g.dbkeditpassword=""
    # create page
    wp = g.templatewp()
    wp.add(jp.P(text="You have been logged out from DBKEdit"))

    return wp
