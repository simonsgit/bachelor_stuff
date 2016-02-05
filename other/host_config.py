__author__ = 'stamylew'

from os.path import expanduser

def assign_path(hostname):
    if hostname == "birdofprey":
        home =              "/home/stamylew/"
        ilp_folder =        home + "ilastik_projects/"
        volumes_folder =    home + "volumes/"
        ilastik_path =      home + "software/ilastik-1.1.6-Linux/run_ilastik.sh"
        autocontext_path =  home + "src/autocontext/autocontext.py"
        test_folder =       home + "test_folder"

    elif hostname == "fatchicken":
        home =              "/home/stamyalew/"
        ilp_folder =        home + "ilastik_projects/"
        volumes_folder =    home + "volumes/"
        ilastik_path =      home + "software/ilastik-1.1.8.post1-Linux/run_ilastik.sh"
        autocontext_path =  home + "src/autocontext/autocontext.py"
        test_folder =       home + "test_folder"

    elif hostname == "sirherny":
        home =              "/mnt/homes/stamyalew/"
        ilp_folder =        "/mnt/data/simon/ilastik_projects/"
        volumes_folder =    "/mnt/data/simon/volumes/"
        ilastik_path =      home + "software/ilastik-1.1.8.post1-Linux/run_ilastik.sh"
        autocontext_path =  home + "software/autocontext/autocontext.py"
        test_folder =       home + "test_folder"
    else:
        raise Exception("No valid hostname given.")
    return home, ilp_folder, volumes_folder, ilastik_path, autocontext_path, test_folder

class host:
    def __init__(self, hostname):
        self.hostname = hostname

    @property
    def hostname(self):
        """Returns hostname
        """
        return self.hostname

    @property
    def home_dir(self):
        """Returns home directory path
        """
        home = expanduser("~")
        return home

    def get_ilp_folder(self, hostname, home_dir):
        """Return ilp folder path
        """
        if hostname == "birdofprey" or "fatchicken":
            ilp_folder = home_dir + "ilastik_projects/"
        elif hostname == "sirherny":
            ilp_folder = "/mnt/data/simon/ilastik_projects/"
        return ilp_folder

    def get_volumes_folder(self, hostname, home_dir):
        """Return volumes folder path
        """
        if hostname == "birdofprey" or "fatchicken":
            volumes_folder = home_dir + "volumes/"
        elif hostname == "sirherny":
            volumes_folder = "/mnt/data/simon/volumes/"
        return volumes_folder

    def get_ilastik_path(self, hostname, home_dir):
        """Return ilastik path
        """
        if hostname == "birdofprey":
            ilastik_path = home_dir + "software/ilastik-1.1.6-Linux/run_ilastik.sh"
        elif hostname == "fatchicken" or "sirherny":
            ilastik_path = home_dir + "software/ilastik-1.1.8.post1-Linux/run_ilastik.sh"
        return ilastik_path

    def get_autocontext_path(self, hostname, home_dir):
        """Return autocontext path
        """
        if hostname == "birdofprey" or "fatchicken":
            autocontext_path = home_dir + "src/autocontext/autocontext.py"#
        elif hostname == "sirherny":
            autocontext_path = home_dir + "software/autocontext/autocontext.py"
        return autocontext_path

    def get_test_folder_path(self, home_dir):
        """Return test folder path
        """
        test_folder_path = home_dir + "test_folder"
        return test_folder_path