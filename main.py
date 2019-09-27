import time
from mngeng import *


def ev_envComplete(cntx):
    print(time.time(), ": Run ev_envComplete:")
    return True


def fn_reqPrepare(cntx):
    print(time.time(), ": Run fn_reqPrepare:")


def ev_reqComplete(cntx):
    print(time.time(), ": Run ev_reqComplete:")
    return True


def fn_resPrepare(cntx):
    print(time.time(), ": Run fn_resPrepare:")


def fn_initResponse(cntx):
    return print(time.time(), ": Run fn_initResponse:")


def fn_sendResponse(cntx):
    return print(time.time(), ": Run fn_sendResponse:")


def ev_resComplete(cntx):
    print(time.time(), ": Run ev_resComplete:")
    return True


def fn_updateSession(cntx):
    print(time.time(), ": Run fn_updateSession:")


def fnLetsgo(cntx):
    print(time.time(), ": Run fnLetsgo:")


def evComplete(cntx):
    time.sleep(1)
    print(time.time(), ": Run evComplete:")
    return True


def fnGoto(cntx):
    print(time.time(), ": Run fnGoto:")


def fnGoodbye(cntx):
    print(time.time(), ": Run fnGoodbye:")


dict = {
    # main loop action
    "ev_envComplete": lambda cntx: ev_envComplete(cntx),
    "fn_reqPrepare": lambda cntx: fn_reqPrepare(cntx),
    "ev_reqComplete": lambda cntx: ev_reqComplete(cntx),
    "fn_resPrepare": lambda cntx: fn_resPrepare(cntx),
    "fn_initResponse": lambda cntx: fn_initResponse(cntx),
    "fn_sendResponse": lambda cntx: fn_sendResponse(cntx),
    "ev_resComplete": lambda cntx: ev_resComplete(cntx),
    "fn_updateSession": lambda cntx: fn_updateSession(cntx),
    # super state action
    "fnLetsgo": lambda cntx: fnLetsgo(cntx),
    "evComplete": lambda cntx: evComplete(cntx),
    "fnGoto": lambda cntx: fnGoto(cntx),
    "fnGoodbye": lambda cntx: fnGoodbye(cntx)
}

# ----------------------------------
import json

with open('mainloop.json') as f:
    fsm = json.load(f)


class myContent(Content):
    __counter__ = 0

    # Constructor
    def __init__(self, name):
        super().__init__(name)

    def bios(self):
        return {
            # main loop action
            "ev_envComplete": lambda cntx: self.ev_envComplete(cntx),
            "fn_reqPrepare": lambda cntx: self.fn_reqPrepare(cntx),
            "ev_reqComplete": lambda cntx: self.ev_reqComplete(cntx),
            "fn_resPrepare": lambda cntx: self.fn_resPrepare(cntx),
            "fn_initResponse": lambda cntx: self.fn_initResponse(cntx),
            "fn_sendResponse": lambda cntx: self.fn_sendResponse(cntx),
            "ev_resComplete": lambda cntx: self.ev_resComplete(cntx),
            "fn_updateSession": lambda cntx: self.fn_updateSession(cntx),
            # super state action
            "fnLetsgo": lambda cntx: self.fnLetsgo(cntx),
            "evComplete": lambda cntx: self.evComplete(cntx),
            "fnGoto": lambda cntx: self.fnGoto(cntx),
            "fnGoodbye": lambda cntx: self.fnGoodbye(cntx)
        }

    def ev_envComplete(self):
        print(time.time(), ": Run ev_envComplete:",self.__counter__)
        self.__counter__ += 1
        return True

    def fn_reqPrepare(self):
        print(time.time(), ": Run fn_reqPrepare:",self.__counter__)
        self.__counter__ += 1

    def ev_reqComplete(self):
        print(time.time(), ": Run ev_reqComplete:",self.__counter__)
        self.__counter__ += 1
        return True

    def fn_resPrepare(self):
        print(time.time(), ": Run fn_resPrepare:",self.__counter__)
        self.__counter__ += 1

    def fn_initResponse(self):
        print(time.time(), ": Run fn_initResponse:",self.__counter__)
        self.__counter__ += 1

    def fn_sendResponse(self):
        print(time.time(), ": Run fn_sendResponse:",self.__counter__)
        self.__counter__ += 1

    def ev_resComplete(self):
        print(time.time(), ": Run ev_resComplete:",self.__counter__)
        self.__counter__ += 1
        return True

    def fn_updateSession(self):
        print(time.time(), ": Run fn_updateSession:",self.__counter__)
        self.__counter__ += 1

    def fnLetsgo(self):
        print(time.time(), ": Run fnLetsgo:",self.__counter__)
        self.__counter__ += 1

    def evComplete(self):
        time.sleep(1)
        print(time.time(), ": Run evComplete:",self.__counter__)
        self.__counter__ += 1
        return True

    def fnGoto(self):
        print(time.time(), ": Run fnGoto:",self.__counter__)
        self.__counter__ += 1

    def fnGoodbye(self):
        print(time.time(), ": Run fnGoodbye:",self.__counter__)
        self.__counter__ += 1


class asyncWrapper(Wrapper):
    # Constructor
    def __init__(self, name, content):
        super().__init__(name, content.bios(content), content)


engine = asyncWrapper('test', myContent)
data = engine.init(engine.load(fsm))

while data.get(data)["complete"] is not True:
    data = engine.event(data)

# data = engine.event(data)
# print("State: ",data.get(data)["keystate"])
# print("Complete: ",data.get(data)["complete"])
