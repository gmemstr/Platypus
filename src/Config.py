# Fetch / set config values.
# Seperate from Cache.py however
# the two may be merged into a single
# file at some point thanks to classes
import json

class Config:
    def Get(self, property):
        self.config = json.load(open("config.json"))

        if(property == "*"):
            return self.config
        else:
            return self.config[property]
    def Set(self, property, newvalue):
        self.config = json.load(open("config.json"))

        self.config[property] = newvalue

        json.dump(open("config.json"), config, indent=4)

        return true
