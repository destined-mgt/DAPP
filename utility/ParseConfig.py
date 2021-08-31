import configparser


def GetConfig(path):
    cf = configparser.ConfigParser()
    cf.read(path)
    return cf
