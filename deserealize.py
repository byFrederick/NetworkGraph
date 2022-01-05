import json 

class importJson:
    def __init__(self, pathJson):
        self.jsonFile = open(pathJson)
        self.jsonData = json.loads(self.jsonFile.read())
    def getUsers(self):
        return self.jsonData["users"]
    def getRelations(self):
        return self.jsonData["relations"]
        
