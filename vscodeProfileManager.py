from functions import Functions
import os

# App Directory
_EXTENSION_KEY = "extensionPath"
_PROFILES_KEY = "profiles"
_LOG_FILE = ".vscodeProfileManager"
_JSON_FILE = ".vscodeProfile.json"

class VscodeProfileManager:
    """
        Init
    """
    def __init__(self):
        # Init functions class
        self.functions = Functions(_LOG_FILE)

        self.homePath = None
        self.extensionsPath = None
        self.jsonFile = None
        self.json_data = None
        self.run()
        

    def run(self):
        try:
            self.set_default_values()
            self.functions.print_json_data(self.jsonData)
        except Exception as e:
            self.set_log('VSCODE PROFILER', str(e.args), True)
        

    def set_default_values(self):
        # Home Path
        self.homePath = self.functions.get_home_path()

        # JSON
        self.jsonFile = self.homePath + "/" + _JSON_FILE
        self.jsonData = self.functions.read_json_file(self.jsonFile)
        
        # Get Extension path
        self.extensionsPath = self.jsonData[_EXTENSION_KEY] if self.functions.checkKey(self.jsonData, _EXTENSION_KEY) else None

# Main
if __name__ == "__main__":
    VscodeProfileManager()