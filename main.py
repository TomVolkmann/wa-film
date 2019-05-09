from app import app, render_template
import database
import re

def confirmInput(form_input):
    if re.match("/[\t\r\n]|(--[^\r\n]*)|(\/\*[\w\W]*?(?=\*)\*\/)/gi", form_input["title"]):
        print("Success")
    else:
        print ("Error! Make sure you only use letters in your name")
    #re.Pattern("/[\t\r\n]|(--[^\r\n]*)|(\/\*[\w\W]*?(?=\*)\*\/)/gi")