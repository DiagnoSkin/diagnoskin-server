import json

class Config:
    def __init__(self, configPath):
        with open(configPath) as configFile:
            configFileContent = json.load(configFile)
        self.imageHeight = configFileContent['imageHeight']
        self.imageWidth = configFileContent['imageWidth']