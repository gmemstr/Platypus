import bcrypt
from functools import wraps
from flask import g, request, redirect, url_for

from src.Config import Config

config = Config()

class LoginManager:
    def Login(self, username, password):
        self.name = config.Get("admin_username")
        self.password = config.Get("admin_password").encode("utf8")

        if username == self.name:
            password = password.encode('utf8')
            if bcrypt.hashpw(password, self.password) == self.password:
                return str(bcrypt.gensalt())
            else:
                return False

class User:

    def __init__(self):
        self.id = ""

    def UserID(self, uid):
        if self.id == "" and uid != None:
            print("set uid")
            self.id = uid
        elif self.id == uid:
            print("valid uid")
            return True
        else:
            print("invalid uid")
            return False


# Password generation script
# Manual right now because... I'm lazy?
if __name__ == "__main__":
    print("Generate new Admin password")
    newpass = input("New password: ")
    confpass = input("Confirm password: ")

    if newpass == confpass:
        newpass = newpass.encode("utf8")
        hashed = bcrypt.hashpw(newpass, bcrypt.gensalt())
        print("Set \"admin_password\" in config.json to " + str(hashed))
    else:
        print("Passwords did not match!")

    # LoginManager().Login("admin", confpass)
