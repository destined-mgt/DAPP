import threading

from blockchain.contract.elect.listener.event import ElectLoop
from blockchain.contract.price.listener.event import PriceLoop
from blockchain.contract.work.listener.event import WorkLoop
from blockchain.contract.workArg.listener.event import WorkArgLoop

def Switch(status, step):
    new_step = None
    loop = None
    res = False
    if status in (0, 1, 2, 3, 16, 17):
        new_step = "elect"
    if status in (4, 5, 6, 7):
        new_step = "price"
    if status in (8, 9):
        new_step = "workArg"
    if status in (10, 11, 12, 13, 14, 15):
        new_step = "work"
    if step != new_step:
        res = True
        if new_step == "elect":
            loop = threading.Thread(target=ElectLoop, args=(status,))
        if new_step == "price":
            loop = threading.Thread(target=PriceLoop, args=(status,))
        if new_step == "workArg":
            loop = threading.Thread(target=WorkArgLoop, args=(status,))
        if new_step == "work":
            loop = threading.Thread(target=WorkLoop, args=(status,))
    return res, loop
