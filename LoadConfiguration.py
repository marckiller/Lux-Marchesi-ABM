import json

class Configuration:

    def __init__(self, path_to_json = 'configuration.json'):
        f = open(path_to_json)
        self.__data = json.load(f)
        f.close()
    
    def get_variables(self):
        return self.__data
    
    #but one can also load the data via staticmethod
    @staticmethod
    def get_variables(path_to_json = 'configuration.json'):
        f = open(path_to_json)
        data = json.load(f)
        f.close()
        return data
