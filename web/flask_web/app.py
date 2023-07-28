# This file is part of https://github.com/jainamoswal/Flask-Example.
# Usage covered in <IDC lICENSE>
# Jainam Oswal. <jainam.me> 


# Import Libraries 
from flask import Flask
from flask import Flask, render_template
# Define app.
app = app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            #template_folder='web/templates'
            )

# Import the __init__.py from modules which had imported all files from the folder.
import modules
