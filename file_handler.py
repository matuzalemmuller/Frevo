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
            terminal, command = saved_command.split(";", 1)
            if terminal == "True":
                terminal_bool = True
            else:
                terminal_bool = False
            return terminal_bool, command
        except IOError as e:
            print(e)
            return None, None
    

    # Saves command
    def save_command(self, terminal, command):
        try:
            if terminal == True:
                preference = "True;" + command
            else:
                preference = "False;" + command
            text_file = open(self._file, 'w+')
            text_file.write(preference)
            text_file.close()
            return True
        except IOError as e:
            print(e)
            return False