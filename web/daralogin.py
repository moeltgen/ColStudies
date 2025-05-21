"""
    colstudies application
"""

import justpy as jp
import globalvars as g

import util.dara as d


def login(request):
    # login form submitted, check if dara accepts and return token
    def submit_form(self, msg):
        #print(msg.form_data)
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
                
        result =  d.logintest_dara(g.daraapi, myusername, mypassword)
        
        if result[0] == "0":
            g.session_data["darausername"] = ""
            g.daraloggedin = False
            txtmsg = "Your login to dara has failed."
            g.darastatus == "failedLogin"
            print(txtmsg)
            loginstatus.text = txtmsg
            wp.page.update()

        else:
            g.session_data["darausername"] = myusername
            g.darausername=myusername
            g.darapassword=mypassword
            g.daraloggedin = True
            txtmsg = "You have successfully logged in to dara."
            g.darastatus == "successLogin"
            print(txtmsg)
            loginstatus.text = txtmsg
            loginform.classes = "hidden"
            msg.page.redirect = "/daralogin"
        
        
    # reset loginstatus message
    def reset_formmessage(self, msg):
        loginstatus.text = txtmsg
        wp.page.update()

    txtmsg = ""

    # create page
    wp = g.templatewp()
    
    
    
    if not g.daraloggedin:
        if g.darastatus == "failedLogin":
            Message = jp.P(
                text="Login not successful",
                a=wp,
                classes="block uppercase tracking-wide text-red-700 text-xs font-bold mb-2",
            )

        elif g.darastatus == "":
            loginform = jp.Form(a=wp, classes="border m-1 p-1 w-64")
            Formtitle = jp.P(text="Login with your dara account", a=loginform)

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
                value="DaraLogin", type="submit", a=loginform, classes=g.button
            )

            loginform.on("submit", submit_form)

            loginform.on("click", reset_formmessage)

            if not g.darausername == "" and not g.darapassword == "":
                usern.value = g.darausername
                passw.value = g.darapassword
                # user still needs to click on submit button
                submit_form

        elif g.darastatus == "successLogin":
            Message = jp.P(
                text="Login successful",
                a=wp,
                classes="block uppercase tracking-wide text-red-700 text-xs font-bold mb-2",
            )

    else:
        if g.darastatus == "successLogin":
            wp.add(jp.P(text="You have successfully logged in to dara."))

        else:
            # if already logged in before
            wp.add(jp.P(text="You are logged in to dara."))

    loginstatus = jp.Span(text="", a=wp, classes="text-red-700")

    return wp


def logout(request):
    # delete token from session
    g.session_data["darausername"] = ""
    g.daraloggedin = False
    
    g.darausername=""
    g.darapassword=""
    # create page
    wp = g.templatewp()
    wp.add(jp.P(text="You have been logged out from dara"))

    return wp
