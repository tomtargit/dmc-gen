from dmc.dmc import DmcSheet

class Project:

    def __init__(self, arg_name):
        self.name = arg_name
        self.location = ''
        self.sheets = []


    def AddSheet(self, arg_name):
        self.sheets.append(arg_name)


    


if __name__ == '__main__':
    pass
