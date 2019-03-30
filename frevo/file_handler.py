import os
import sys

# Save and read commands from commands file
class ConfigHandler():
    # Creates file if it doesn't exist
    def __init__(self):
        self._file = self.resourcePath("config/commands.txt")
        try:
            os.mkdir(self._file.rsplit('/',1)[0])
            config_file = open(self._file, 'w+')
            config_file.close()
        except:
            pass

    
    # Reads command from commands file
    def read_commands(self):
        try:
            text_file = open(self._file, 'r')
            saved_command = text_file.readlines()
            text_file.close()
            name_list = []
            terminal_list = []
            command_list = []
            for i in saved_command:
                if i == "" or i == "\n":
                    continue
                name, terminal, command = i.split(";",2)
                if terminal == "True":
                    terminal_bool = True
                else:
                    terminal_bool = False
                name_list.append(name)
                terminal_list.append(terminal_bool)
                command_list.append(command[:-1])
            if len(command_list) == 0:
                return None, None, None
            else:
                return name_list, terminal_list, command_list
        except IOError as e:
            print(e)
            return None, None, None
    

    # Saves commands
    def save_commands(self, name_list, terminal_list, command_list):
        try:
            open(self._file, 'w').close()
            if len(command_list) == 0:
                return True
            commands = ""
            for i in range(len(command_list)):
                if terminal_list[i] == True:
                    commands = commands + name_list[i] + ";True;" + command_list[i]
                else:
                    commands = commands + name_list[i] + ";False;" + command_list[i]
            text_file = open(self._file, 'w')
            text_file.write(commands)
            text_file.close()
            return True
        except IOError as e:
            print(e)
            return False
    

    # Handles path when running as a Mac app
    def resourcePath(self,relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)
    

    # Determines whether Frevo is running as code or app based on folder
    # used by Frevo when running as Mac app
    def isApp(self):
        if hasattr(sys, '_MEIPASS'):
            return True
        else:
            return False