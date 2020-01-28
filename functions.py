import os
import subprocess
import json
import datetime
from sys import platform
from typing import TypeVar, Generic

T = TypeVar('T')

class Functions:
    """
        Init
    """
    def __init__(self, nameFileLog):
        self.logFile = nameFileLog
        self.homePath = ''
        self.set_home_path()

    def set_home_path(self):
        if self.is_system_operating(0) == True:
            self.homePath = os.path.expanduser("~")
        elif self.is_system_operating(2) == True:
            self.homePath = os.path.expanduser("~")

    def get_home_path(self) -> str:
        return self.homePath

    def exec_command(self, command):
        """Only execute command
        
        Arguments:
            command {str} -- command to execute
        """
        os.system(command)
    
    def exec_command_get_output(self, command):
        """Execute command and return output
        
        Arguments:
            command {str} -- command to execute
        
        Returns:
            str -- output command
        """
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
        return output.decode("utf-8").strip("\n")
    

    def checkFileExist(self, file):
        """Check if files exists
        
        Arguments:
            file {str} -- name of full path with name
        
        Returns:
            bool -- True if exist
        """
        if isinstance(file, str):
            return os.path.isfile(file)
        else:
            return False
    
    
    def checkDirectoryExist(self, directory):
        """Check if directories exists
        
        Arguments:
            directory {str} -- name of directory
        
        Returns:
            bool -- True if exist
        """
        return os.path.isdir(directory)

    
    def rename_file_dir_name(self, oldName, newName):
        """Rename file or directory
        
        Arguments:
            oldName {str} -- Old name of file/directory
            newName {str} -- New name of file/directory
        """
        os.rename(oldName, newName)

    
    def read_json_file(self, json_file):
        """Read JSON File
        
        Arguments:
            json_file {str} -- name of full path with name of file
        
        Returns:
            object -- json data
        """  
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

    
    def is_system_operating(self, type):
        """Check SO by type
        
        Arguments:
            type {int} -- [description]
        
        Returns:
            bool -- True if system operatin
        """
        is_Platform = False

        if type == 0: # linux
            self.is_Platform = True if (platform == "linux" or platform == "linux2") else False
        elif type == 1: # OS X
            self.is_Platform = True if platform == "darwin" else False
        elif type == 2: # Windows...
            self.is_Platform = True if platform == 'win32' or platform == 'win64' else False
        return self.is_Platform

    def write_read_file(self, nameFile: str, data, isWrite: bool):
        if len(nameFile) > 0:
            _type = "a" if isWrite == True else "r"
            _content = None
            _file = open(nameFile, _type)

            if isWrite == True:
                _file.write(data)
                
            _content = _file.read()
            f.close()
            return _content


    

    def set_log(self, _type, _error_log, print_error = False):
        """Set Log Error
        
        Arguments:
            _type {str} -- [description]
            _error_log {str} -- [description]
        
        Keyword Arguments:
            print_error {bool} -- [description] (default: {False})
        """
        _type = _type + " " + str(datetime.datetime.now())
        _log_file = self.logFile + ".log"
        _msg = _type + ": " + _error_log
        self.write_read_file(_log_file, _msg, True)

        if print_error == True:
            print(_msg)
        self.exec_command(command)
    

    def print_json_data(self, json_data):
        """Print Json Data
        
        Arguments:
            json_data {object} -- [description]
        """
        print(json.dumps(json_data, indent=4, sort_keys=True))

    
    def checkKey(self, object, key):
        """Check if key exist on object
        
        Arguments:
            object {object} -- object to check
            key {str} -- key to check
        
        Returns:
            [bool] -- True if exist, False if not
        """
        if key in object.keys(): 
            return True
        else: 
            return False

    
    def get_input_keyboard(self, message, typeInput: Generic[T]) -> T:
        """Read data from keyboard
        
        Arguments:
            message {str} -- Message to print on read input
            typeInput {Generic[T]} -- Type of data to get from input
        
        Returns:
            T -- data inserted
        """
        while True:
            try:
                x = typeInput(input(message))
                return x
            except ValueError:
                print("Oops!  That was no valid.  Try again...")