# Save and read commands from commands file
class FileHandler():
    def __init__(self):
        self._file = "commands.txt"

    
    # Reads command from commands file
    def read_commands(self):
        try:
            text_file = open(self._file, 'r')
            saved_command = text_file.readline()
            text_file.close()
            if saved_command == "":
                return None, None, None
            name, terminal, command = saved_command.split(";",2)
            if terminal == "True":
                terminal_bool = True
            else:
                terminal_bool = False
            return name, terminal_bool, command
        except IOError as e:
            print(e)
            return None, None, None
    

    # Saves command
    def save_command(self, name, terminal, command):
        try:
            if terminal == True:
                preference = name + ";True;" + command
            else:
                preference = name + ";False;" + command
            text_file = open(self._file, 'w+')
            text_file.write(preference)
            text_file.close()
            return True
        except IOError as e:
            print(e)
            return False