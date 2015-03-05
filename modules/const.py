import os
import ConfigParser
import time


class Const:
    def __init__(self):
        # Define the dir splitter for the current OS
        if os.name == "nt":
            self.DIR_SPLITTER = '\\'
        else:
            self.DIR_SPLITTER = '/'

        # config file parse
        self.ROOT, self.PORT, self.default_page, self.max_threads = self.config2vars("config.ini")
        # Socket configuration
        self.ADDRESS = ('', self.PORT)

        self.FORBIDDEN_FILES = ["password.txt"]
        self.MOVED_FILES = {"a.txt": "b.txt", "": self.default_page}

        self.BUFFER_SIZE = 8192

    def config2vars(self, configfile):
        """
        Check if the config file exists
        if not exists create one and add the Default settings


        Default settings
        ================

        [settings]
        port = 8080
        root = # Empty by default
        default_page = "index.html"
        max_threads = 10

        ================

        Parse the config file to variables by reading the config file
        and saving

        checking if the ROOT dir exists if not
        Checking if @CWD@/root/ exists if not creates
        changing the CWD to root

        :rtype : object
        :param configfile:
        """
        # Create the config if not exists
        if not os.path.isfile(os.getcwd() + self.DIR_SPLITTER + "config.ini"):
            config = ConfigParser.RawConfigParser()
            config.add_section('settings')
            config.set('settings', 'port', '8080')
            config.set('settings', 'root', '# Empty by default')
            config.set('settings', 'default_page', 'index.html')
            config.set('settings', 'max_threads', '10')

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        # Read from the file
        config = ConfigParser.ConfigParser()
        config.read(configfile)
        ROOT = config.get("settings", "root")
        PORT = config.getint("settings", "port")
        default_page = config.get("settings", "default_page")
        max_threads = config.getint("settings", "max_threads")

        if not os.path.exists(ROOT):
            # Check if the directory not exists and change to CWD + root
            ROOT = os.getcwd() + self.DIR_SPLITTER + "root"
            if not os.path.exists(ROOT):
                # If new path not exists create him
                os.makedirs(ROOT)

        return ROOT, PORT, default_page, max_threads

    def cls(self):
        """
        Clear the console screen
        (works on most of the systems)
        """
        os.system(['clear', 'cls'][os.name == 'nt'])

    def time_stamp(self):
        return time.strftime("[%H:%M:%S]")
