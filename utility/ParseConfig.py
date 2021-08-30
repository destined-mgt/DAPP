import configparser


def GetConfig(path, items):
    cf = configparser.ConfigParser()
    cf.read(path)
    cfg = cf.items(items)
    return cfg
