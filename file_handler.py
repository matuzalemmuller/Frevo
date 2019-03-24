class FileHandler():
    def __init__(self):
        self.file = "commands.txt"

    
    def read_commands(self):
        try:
            text_file = open(self.file, 'r')
            command = text_file.readline()
            text_file.close()
            return command
        except IOError as e:
            print(e)
            return None
    

    def save_command(self, command):
        try:
            text_file = open("commands.txt", 'w+')
            text_file.write(command)
            text_file.close()
            return True
        except IOError as e:
            print(e)
            return False