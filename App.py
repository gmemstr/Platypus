from multiprocessing import Process
from src.Webserver import Webserver
from src.Slackbot import Bot
from src.Config import Config
from src.Statuses import Scanning
    
config = Config()
ws  = Webserver()
scn = Scanning()
sb = Bot()

if __name__ == "__main__":
    # This code determines which frontend to start up
    # It's a bit messy but it's the best method I could
    # think of to handle this. Hopefully I'll be able to
    # slim it down significantly.

    if config.Get("enable_webserver") is True and config.Get("enable_slackbot") is True:
        print("Webserver starting up")
        print("Slackbot enabled.")

        # The order in which the processes are started
        # is important, since the flask process effectively
        # blocks the rest of the code from running (wtfkwbtihiw)
        sbp = Process(target=sb.Loop()).start()
        scnp = Process(target=scn.Loop()).start()
        wsp = Process(target=ws.Run()).start()

    elif config.Get("enable_webserver") is True:
        print("Webserver starting up")
        # scnp = Process(target=scn.Loop()).start()
        wsp = Process(target=ws.Run()).start()


    elif config.Get("enable_slackbot") is True:
        print("Slackbot enabled")
        scnp = Process(target=scn.Loop()).start()
        sbp = Process(target=sb.Loop()).start()


    else: 
        print("No frontends enabed. Scanning to cache only.")
        scn.Loop()

