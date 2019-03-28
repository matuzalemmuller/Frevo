import os
import sys

# Save and read commands from commands file
class ConfigHandler():
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
            if saved_command == "":
                return None, None, None
            for i in saved_command:
                name, terminal, command = i.split(";",2)
                if terminal == "True":
                    terminal_bool = True
                else:
                    terminal_bool = False
                name_list.append(name)
                terminal_list.append(terminal_bool)
                command_list.append(command)
            return name_list, terminal_list, command_list
        except IOError as e:
            print(e)
            return None, None, None
    

    # Saves command
    def save_commands(self, name_list, terminal_list, command_list):
        try:
            if len(command_list) == 0:
                return True
            for i in range(len(command_list)):
                if terminal_list[i] == True:
                    command = name_list[i] + ";True;" + command_list[i] + "\n"
                else:
                    command = name_list[i] + ";False;" + command_list[i] + "\n"
                text_file = open(self._file, 'a+')
                text_file.write(command)
                text_file.close()
            return True
        except IOError as e:
            print(e)
            return False
    

    # Handles path when running as an .app
    def resourcePath(self,relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)
    

    # Determines whether frevo is running as code or app
    def isApp(self):
        if hasattr(sys, '_MEIPASS'):
            return True
        else:
            return False