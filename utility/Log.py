import logging
import os
import time

logger = logging.getLogger("DAPP")


# 设置输出等级

def SetLevel(level='DEBUG'):
    true_level = logging.DEBUG
    if level == 'DEBUG':
        true_level = logging.DEBUG
    elif level == 'INFO':
        true_level = logging.INFO
    elif level == 'WARING':
        true_level = logging.WARNING
    elif level == 'ERROR':
        true_level = logging.ERROR
    elif level == 'CRITICAL':
        true_level = logging.CRITICAL
    logger.setLevel(true_level)
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_path = os.path.dirname(os.getcwd()) + '/DAPP/'
    log_name = log_path + rq + '.log'
    logfile = log_name
    ch = logging.StreamHandler()
    ch.setLevel(true_level)
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(true_level)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
