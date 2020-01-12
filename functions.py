import os
import subprocess
import json
import datetime
from sys import platform

class Functions:
    """
        Init
    """
    def __init__(self, nameFileLog):
        self.logFile = nameFileLog
        self.homePath = None
        #self.set_home_path()

    def set_home_path(self):
        if self.is_system_operating(0) == True:
            self.homePath = os.path.expanduser("~")
        elif self.is_system_operating(2) == True:
            self.jsonFile = "c:\\"

    def get_home_path(self):
        return self.homePath
    
    """
        Only execute command
    """
    def exec_command(self, command):
        os.system(command)

    """
        Execute command and return output
    """
    def exec_command_get_output(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
        return output.decode("utf-8").strip("\n")

    """
        Check if files exists
    """
    def checkFileExist(self, file):
        if isinstance(file, str):
            return os.path.isfile(file)
        else:
            return False

    """
        Check if directories exists
    """
    def checkDirectoryExist(self, directory):
        return os.path.isdir(directory)

    """
        Read JSON File
    """
    def read_json_file(self, json_file):
        json_data = {}
        try:
            stream = open(json_file, 'r')
            json_data = json.load(stream)
            stream.close()
        except Exception as e:
            msg = "\"ERROR on read JSON File\""
            self.set_log('READ JSON', str(e.args))
            json_data = {}
        return json_data

    """
        Check SO by type
    """
    def is_system_operating(self, type):
        is_Platform = False

        if type == 0: # linux
            self.is_Platform = True if (platform == "linux" or platform == "linux2") else False
        elif type == 1: # OS X
            self.is_Platform = True if platform == "darwin" else False
        elif type == 2: # Windows...
            self.is_Platform = True if platform == 'win32' or platform == 'win64' else False
            
        return self.is_Platform

    """
        [Set Log Error]
    """
    def set_log(self, _type, _error_log, print_error = False):
        _type = _type + " " + str(datetime.datetime.now())
        localization_log_file = self.homePath + "/" + self.logFile + ".log"
        _msg = _type + ": " + _error_log
        command = "echo \"" + _msg + "\" | tee -a " + localization_log_file + " > /dev/null"

        if print_error == True:
            print(_msg)

        self.exec_command(command)

    """
        Print Json Data
    Returns:
        [json_data] -- [data of json]
    """
    def print_json_data(self, json_data):
        print(json.dumps(json_data, indent=4, sort_keys=True))

    """[Check if key exist on object]
    Returns:
        [type] -- [description]
    """
    def checkKey(self, object, key):
        if key in object.keys(): 
            return True
        else: 
            return False