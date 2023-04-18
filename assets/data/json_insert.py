import json
import os

dict = {
    "welcome": """
    Welcome to the Windows Automated General Servitor (WAGS)

    To run the application, hit the “Run” button located below. 
    If you wish to stop the application, simply hit the “Stop” button that 
    replaces the “Run” button.""",

    "features": """
    Features page:

    Say “Something” - does “action1”
    Say “Something” - does “action2”
    Say “Something” - does “action3”
    Say “Something” - does “action4”
    Say “Something” - does “action5”""",

    "settings": """
    Settings page""",

    "github": """
    Github page"""
    
    }

json_obj = json.dumps(dict, indent=4)

parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

with open(f"{parent_dir}\\data\\appText.json", "w") as f:
    f.write(json_obj)