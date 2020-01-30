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
_EXTENSIONS_KEY = "all_extensions"

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
        self.arrayExtensions = None
        self.arrayPathExtensions = []
        self.run()

    def run(self):
        isSetDefault = False
        try:
            while(True):
                if self.functions.checkFileExist(_FILE_ACTIVE_PROFILE) == True:
                    print(self.functions.write_read_file(_FILE_ACTIVE_PROFILE, None, False))
                    print("---")

                if isSetDefault == False:
                    self.set_default_values()
                    
                selectedMenu = self.create_menu(isSetDefault)
                isSetDefault = True if isSetDefault == False else isSetDefault

                if selectedMenu < len(self.arrayOfMenu):
                    print('Init operations for: ' + self.arrayOfMenu[selectedMenu] + ' profile...')
                    self.execute_operations(selectedMenu)
                    print('Done. Please Reload Code')
                    input("PRESS ENTER TO CONTINUE!")
                else:
                    break
                print("\n\n\n##############")
        except Exception as e:
            self.functions.set_log('VSCODE PROFILER', str(e.args), True)

    def set_default_values(self):
        # JSON
        self.jsonData = self.functions.read_json_file(_JSON_FILE)

        # Get All Extensions
        self.arrayExtensions = self.jsonData[_EXTENSIONS_KEY] if self.functions.checkKey(self.jsonData, _EXTENSIONS_KEY) else None
        
        # Get Extension path default linux
        self.extensionsPath = self.jsonData[_EXTENSION_PATH_KEY] if self.functions.checkKey(self.jsonData, _EXTENSION_PATH_KEY) else ''
        self.extensionsPath = self.functions.get_home_path() + "/.vscode/extensions" if self.extensionsPath == '' else self.extensionsPath
        self.extensionsPath = self.extensionsPath if self.extensionsPath.endswith('/') else self.extensionsPath + '/'

        # If windows
        if self.functions.is_system_operating(2) == True:
            self.extensionsPath = self.extensionsPath.replace('/', '\\')
        
        if self.functions.checkDirectoryExist(self.extensionsPath) == False:
            raise Exception('\nInvalid extensions path: ' + self.extensionsPath)

        command = "ls " if self.functions.is_system_operating(0) == True else "dir /B " if self.functions.is_system_operating(2) == True else ""
        self.arrayPathExtensions = self.functions.exec_command_get_output(command + "\"" + self.extensionsPath + "\"")
        self.arrayPathExtensions = self.arrayPathExtensions.split("\n")
        if len(self.arrayPathExtensions) == 0:
            raise Exception('No extensions instaled')

    def create_menu(self, isSetDefault: bool):
        data = self.jsonData[_PROFILES_KEY] if self.functions.checkKey(self.jsonData, _PROFILES_KEY) else None
        selected = -1

        if data is None:
            print("No profiles to manage")
        else:
            print("\nVSCode Profile Manager Menu:")

            if isSetDefault == False:
                for key, value in data.items():
                    self.arrayOfMenu.append(key)

            for index, value in enumerate(self.arrayOfMenu):
                print(str(index) + " - " + value)
                if index == 1 or index == 3:
                    print("----")
            
            print("----")
            print(str(len(self.arrayOfMenu)) + " - Exit")
            
            while selected < 0 or selected > len(self.arrayOfMenu):
                selected = self.functions.get_input_keyboard('Enter your profile: ', int)

                if selected < 0 or selected > len(self.arrayOfMenu):
                    print('Please enter only profile inputs!!!')
        return selected

    def get_directory_name_extension(self, extension):
        _command = ""
        _name = ""

        if self.functions.is_system_operating(0) == True:
            _command += "ls \"" + self.extensionsPath + "\" | grep -wi {0}*"
        elif self.functions.is_system_operating(2) == True:
            _command += "dir /B \"" + self.extensionsPath + "\" | findstr {0}*"

        _command = _command.replace("{0}", extension)
        _name = self.functions.exec_command_get_output(_command)
        if len(_name) == 0:
            _command = _command.replace("{0}", extension.lower())
            _name = self.functions.exec_command_get_output(_command)
        _name = _name.split("\n")

        if len(_name) > 1:
            return ''

        _name = _name[0].replace('@', '-')
        if len(_name) == 0:
            return ''

        _dirName = self.extensionsPath + "{0}"
        if self.functions.checkDirectoryExist(_dirName.replace("{0}", _name)) == True:
            return _dirName.replace("{0}", _name)
        elif self.functions.checkDirectoryExist(_dirName.replace("{0}", _name.lower())) == True:
            return _dirName.replace("{0}", _name.lower())
        else:
            return ''

    def enable_disable_extension(self, extension, isEnable = True):
        extensionDirName = self.get_directory_name_extension(extension)

        # No exist extension directory
        if len(extensionDirName) <= 0:
            return False

        filePackage = extensionDirName + "/" + _FILE_PACKAGE_JSON
        if self.functions.is_system_operating(2) == True:
            filePackage = filePackage.replace('/', '\\')
        _fileToCheck = (filePackage + _PACKAGE_JSON_PREFIX) if isEnable == True else (filePackage)

        # No exist package json
        if self.functions.checkFileExist(_fileToCheck) == False:
            return False

        if isEnable == True:
            self.functions.rename_file_dir_name(filePackage + _PACKAGE_JSON_PREFIX, filePackage)
        else:
            self.functions.rename_file_dir_name(filePackage, filePackage + _PACKAGE_JSON_PREFIX)
        return True

    def execute_operations(self, key):
        if key == 0:
            self.install_uninstall_extensions()
        elif key == 1:
            self.install_uninstall_extensions(False)
        elif key == 2 or key > 3:
            self.disable_all()
        elif key == 3:
            self.enable_all()

        if key > 3:
            data = self.jsonData[_PROFILES_KEY][self.arrayOfMenu[key]]
            if len(data) > 0:
                for extension in data:
                    self.enable_disable_extension(extension)

        if key > 1:
            self.save_info_profile(key)

    def install_uninstall_extensions(self, isInstall = True):
        codeReplace = '{0}'
        commandInstall = "code --install-extension {0}"
        commandUninstall = "code --uninstall-extension {0}"
        for key, value in self.arrayExtensions.items():
            if isinstance(value, list):
                print("\nInstall Extensions for: " + key)
                for index, value in enumerate(value):
                    if isInstall == True:
                        self.functions.exec_command(commandInstall.replace(codeReplace, value))
                    else:
                        self.functions.exec_command(commandUninstall.replace(codeReplace, value))    
            else:
                print("\n" + key + " is not array")
                
    def save_info_profile(self, key):
        profile = ''
        if key == 2:
            profile = 'Disabled All'
        elif key == 3:
            profile = 'Enabled All'
        else:
            profile = self.arrayOfMenu[key]
        self.functions.write_read_file("active_profile", "Active Profile: " + profile, True, False)

    def enable_all(self):
        data = self.jsonData[_PROFILES_KEY]
        for key, value in data.items():
            if len(value) > 0:
                for extension in value:
                    self.enable_disable_extension(extension)
    
    def disable_all(self):
        data = self.jsonData[_PROFILES_KEY]
        for key, value in data.items():
            if len(value) > 0:
                for extension in value:
                    self.enable_disable_extension(extension, False)


# Main
if __name__ == "__main__":
    VscodeProfileManager()