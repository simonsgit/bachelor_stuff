__author__ = 'stamylew'



def assign_path(hostname):
    if hostname == "birdofprey":
        ilp_folder = "/home/stamylew/ilastik_projects/"
        volumes_folder = "/home/stamylew/volumes/"
        ilastik_path = "/home/stamylew/software/ilastik-1.1.6-Linux/run_ilastik.sh"
        autocontext_path = "/home/stamylew/src/autocontext/autocontext.py"
        test_folder = "/home/stamylew/test_folder"

    elif hostname == "fatchicken":
        ilp_folder = "/home/stamyalew/ilastik_projects/"
        volumes_folder = "/home/stamyalew/volumes/"
        ilastik_path = "/home/stamyalew/software/ilastik-1.1.8.post1-Linux/run_ilastik.sh"
        autocontext_path = "//home/stamyalew/src/autocontext/autocontext.py"
        test_folder = "/home/stamyalew/test_folder"

    elif hostname == "sirherny":
        ilp_folder = "/mnt/data/simon/ilastik_projects/"
        volumes_folder = "/mnt/data/simon/volumes/"
        ilastik_path = "/mnt/homes/stamyalew/software/ilastik-1.1.8.post1-Linux/run_ilastik.sh"
        autocontext_path = "/mnt/homes/stamyalew/software/autocontext/autocontext.py"
        test_folder = "/mnt/homes/stamyalew/test_folder"
    else:
        raise Exception("No valid hostname given.")
    return ilp_folder, volumes_folder, ilastik_path, autocontext_path, test_folder
