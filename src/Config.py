import json

class Config:
    def Get(self, property):
        self.config = json.load(open("config.json"))

        return self.config[property]

