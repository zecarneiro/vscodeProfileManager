#!/usr/bin/env python3
from functions import Functions
import os

# App Directory
_EXTENSION_PATH_KEY = "extensionPath"
_PROFILES_KEY = "profiles"
_LOG_FILE = "vscodeProfileManager"
_JSON_FILE = "vscodeProfile.json"
_PACKAGE_JSON_PREFIX = "VSCODE_PROFILE"
_FILE_PACKAGE_JSON = "package.json"
_FILE_ACTIVE_PROFILE = "active_profile"
_COMMENT_JSON_KEY = "comment_vsprofile"

class VscodeProfileManager:
    """
        Init
    """
    def __init__(self):
        # Init functions class
        self.functions = Functions(_LOG_FILE)
        self.extensionsPath = ''
        self.json_data = None
        self.arrayOfMenu = ['Install', 'Uninstall', 'Disable All','Enable All']
        self.arrayPathExtensions = []
        self.arrayPathWithoutIgnoredExtensions = []
        self.run()

    def run(self):
        try:
            if self.functions.checkFileExist(_FILE_ACTIVE_PROFILE) == True:
                self.functions.exec_command("cat " + _FILE_ACTIVE_PROFILE)
                print("---")

            self.set_default_values()
            selectedMenu = self.create_menu()
            if selectedMenu < len(self.arrayOfMenu):
                print('Init operations for: ' + self.arrayOfMenu[selectedMenu] + ' profile...')
                self.execute_operations(selectedMenu)
                print('Done. Please Reload Code')
                input("PRESS ENTER TO EXIT!")
        except Exception as e:
            self.functions.set_log('VSCODE PROFILER', str(e.args), True)

    def set_default_values(self):
        # JSON
        self.jsonData = self.functions.read_json_file(_JSON_FILE)
        
        # Get Extension path
        self.extensionsPath = self.jsonData[_EXTENSION_PATH_KEY] if self.functions.checkKey(self.jsonData, _EXTENSION_PATH_KEY) else None
        print(self.functions.get_home_path())
        if self.extensionsPath == None:
            if self.functions.is_system_operating(0) == True:
                self.extensionsPath = self.functions.get_home_path() + "/.vscode/extensions"
            elif self.functions.is_system_operating(2) == True:
                self.extensionsPath = self.functions.get_home_path() + "/.vscode/extensions"

        self.extensionsPath = self.extensionsPath if self.extensionsPath.endswith('/') else self.extensionsPath + '/'
        if self.functions.checkDirectoryExist(self.extensionsPath) == False:
            raise Exception('\nInvalid extensions path: ' + self.extensionsPath)

        command = "ls " if self.functions.is_system_operating(0) == True else "dir " if self.functions.is_system_operating(2) == True else ""
        self.arrayPathExtensions = self.functions.exec_command_get_output(command + self.extensionsPath)
        self.arrayPathExtensions = self.arrayPathExtensions.split("\n")
        if len(self.arrayPathExtensions) == 0:
            raise Exception('No extensions instaled')

    def create_menu(self):
        data = self.jsonData[_PROFILES_KEY] if self.functions.checkKey(self.jsonData, _PROFILES_KEY) else None
        selected = -1

        if data is None:
            print("No profiles to manage")
        else:
            for key, value in data.items():
                if _COMMENT_JSON_KEY not in key:
                    self.arrayOfMenu.append(key)

            for index, value in enumerate(self.arrayOfMenu):
                print(str(index) + " - " + value)
            
            print("----")
            print(str(len(self.arrayOfMenu)) + " - Exit")
            
            while selected < 0 or selected > len(self.arrayOfMenu):
                selected = self.functions.get_input_keyboard('Enter your profile: ', int)

                if selected < 0 or selected > len(self.arrayOfMenu):
                    print('Please enter only profile inputs!!!')
            
        return selected

    def get_command_to_extension(self, extension, isCheck):
        if isCheck == True:
            return "ls " + self.extensionsPath + " | grep -cwi " + extension + "*"
        else:
            return "ls " + self.extensionsPath + " | grep -wi " + extension + "*"

    def enable_extension(self, extension):
        filePackage = ''
        count = int(self.functions.exec_command_get_output(self.get_command_to_extension(extension, True)))
        if count == 1:
            extensionName = self.functions.exec_command_get_output(self.get_command_to_extension(extension, False))
            filePackage = self.extensionsPath + extensionName + "/" + _FILE_PACKAGE_JSON

        if self.functions.checkFileExist(filePackage + _PACKAGE_JSON_PREFIX) == True:
            self.functions.rename_file_dir_name(filePackage + _PACKAGE_JSON_PREFIX, filePackage)

    def disable_extension(self, extension):
        filePackage = ''
        count = int(self.functions.exec_command_get_output(self.get_command_to_extension(extension, True)))
        if count == 1:
            extensionName = self.functions.exec_command_get_output(self.get_command_to_extension(extension, False))
            filePackage = self.extensionsPath + extensionName + "/" + _FILE_PACKAGE_JSON
            
        if self.functions.checkFileExist(filePackage) == True:
            self.functions.rename_file_dir_name(filePackage, filePackage + _PACKAGE_JSON_PREFIX)

    def execute_operations(self, key):
        if key == 0 or key > 1:
            self.disable_all()
        elif key == 1:
            self.enable_all()

        if key > 1:
            data = self.jsonData[_PROFILES_KEY][self.arrayOfMenu[key]]
            if len(data) > 0:
                for extension in data:
                    self.enable_extension(extension)
        self.save_info_profile(key)
                
    def save_info_profile(self, key):
        profile = ''
        if key == 0:
            profile = 'Disabled All'
        elif key == 1:
            profile = 'Enabled All'
        else:
            profile = self.arrayOfMenu[key]
        command = "echo 'Active Profile: " + profile + "' > active_profile"
        self.functions.exec_command(command)

    def enable_all(self):
        data = self.jsonData[_PROFILES_KEY]
        for key, value in data.items():
            if len(value) > 0:
                for extension in value:
                    self.enable_extension(extension)
    
    def disable_all(self):
        data = self.jsonData[_PROFILES_KEY]
        for key, value in data.items():
            if len(value) > 0:
                for extension in value:
                    self.disable_extension(extension)


# Main
if __name__ == "__main__":
    VscodeProfileManager()