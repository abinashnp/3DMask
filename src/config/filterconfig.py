import os


def get_config(filter_name):
    switcher = {
        "hat": get_hat_config(),
        "horn": get_hat_config(),
        "pirate": get_pirate_config(),
        "viking": get_viking_config()
    }
    return switcher.get(filter_name, get_hat_config())


def get_hat_config():
    modelName = os.getcwd() + "/models/cowboy/cowboy.obj"
    albedoName = os.getcwd() + "/models/cowboy/Hat1_albedo.jpeg"
    scale_factor = 2.2
    x_deflection = 0
    y_deflection = -0.12
    hor_s = 1.2
    ver_s = 1
    idA = 151
    idB = 10
    lat_s = -0.05
    camera_eye = [0, 0.09, 1]
    return modelName, albedoName, scale_factor, x_deflection, y_deflection, idA, idB, camera_eye, hor_s, ver_s, lat_s


def get_pirate_config():
    modelName = os.getcwd() + "/models/pirate/pirate.obj"
    albedoName = os.getcwd() + "/models/pirate/pirate.png"
    scale_factor = 2.8
    x_deflection = 0
    y_deflection = -0.10
    hor_s = 1
    ver_s = 1
    idA = 151
    idB = 10
    lat_s = 0.15
    camera_eye = [0, 0, 1]
    return modelName, albedoName, scale_factor, x_deflection, y_deflection, idA, idB, camera_eye, hor_s, ver_s, lat_s


def get_viking_config():
    modelName = os.getcwd() + "/models/viking/viking.obj"
    albedoName = os.getcwd() + "/models/viking/helmet_color.png"
    scale_factor = 3.1
    x_deflection = 0
    y_deflection = -0.014
    hor_s = 1.4
    ver_s = 1
    idA = 151
    idB = 10
    lat_s = 0.1
    camera_eye = [0, 0.2, 1]
    return modelName, albedoName, scale_factor, x_deflection, y_deflection, idA, idB, camera_eye, hor_s, ver_s, lat_s
