# Fetch / set config values.
# Seperate from Cache.py however
# the two may be merged into a single
# file at some point thanks to classes
import json

class Config:
    def __init__(self):
        with open('config.json') as config:    
            self.config = json.load(config)

    def Get(self, property):
        if(property == "*"):
            return self.config
        else:
            return self.config[property]
    def Set(self, property, newvalue):
        self.config[property] = newvalue

        with open('config.json', 'w') as config:
            json.dump(self.config, config, indent=4)

        return True