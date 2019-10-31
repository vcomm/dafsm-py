import time
import asyncio
from mngeng import *


class Cntn(Content):
    __counter__ = 0

    # Constructor
    def __init__(self, name):
        super().__init__(name)

    def bios(self):
        return {
            # main loop action
            "ev_envComplete": self.ev_envComplete,
            "fn_reqPrepare": self.fn_reqPrepare,
            "ev_reqComplete": self.ev_reqComplete,
            "fn_resPrepare": self.fn_resPrepare,
            "fn_initResponse": self.fn_initResponse,
            "fn_sendResponse": self.fn_sendResponse,
            "ev_resComplete": self.ev_resComplete,
            "fn_updateSession": self.fn_updateSession,
            # super state action
            "fnLetsgo": self.fnLetsgo,
            "evComplete": self.evComplete,
            "fnGoto": self.fnGoto,
            "fnGoodbye": self.fnGoodbye,
            "fnCount": self.fnCount,
            "evCounFinish": self.evCounFinish,
            "evContinue": self.evContinue,

        }

    def evContinue(self):
        if self.__counter__ < 1000:
            return True
        else:
            return False

    def evCounFinish(self):
        if self.__counter__ > 1000:
            return True
        else:
            return False

    def fnCount(self):
        print(time.time(), ": Run fnCount:", self.__counter__)
        self.__counter__ += 100

    def ev_envComplete(self):
        print(time.time(), ": Run ev_envComplete:", self.__counter__)
        self.__counter__ += 1
        return True

    async def fn_reqPrepare(self):
        await asyncio.sleep(1)
        print(time.time(), ": Run fn_reqPrepare:", self.__counter__)
        self.__counter__ += 1

    def ev_reqComplete(self):
        print(time.time(), ": Run ev_reqComplete:", self.__counter__)
        self.__counter__ += 1
        return True

    async def fn_resPrepare(self):
        await asyncio.sleep(1)
        print(time.time(), ": Run fn_resPrepare:", self.__counter__)
        self.__counter__ += 1

    async def fn_initResponse(self):
        await asyncio.sleep(1)
        print(time.time(), ": Run fn_initResponse:", self.__counter__)
        self.__counter__ += 1

    async def fn_sendResponse(self):
        await asyncio.sleep(1)
        print(time.time(), ": Run fn_sendResponse:", self.__counter__)
        self.__counter__ += 1

    def ev_resComplete(self):
        print(time.time(), ": Run ev_resComplete:", self.__counter__)
        self.__counter__ += 1
        return True

    async def fn_updateSession(self):
        await asyncio.sleep(1)
        print(time.time(), ": Run fn_updateSession:", self.__counter__)
        self.__counter__ += 1

    def fnLetsgo(self):
        # await asyncio.sleep(1)
        print(time.time(), ": Run fnLetsgo:", self.__counter__)
        self.__counter__ += 1

    def evComplete(self):
        print(time.time(), ": Run evComplete:", self.__counter__)
        self.__counter__ += 1
        return True

    def fnGoto(self):
        # await asyncio.sleep(1)
        print(time.time(), ": Run fnGoto:", self.__counter__)
        self.__counter__ += 1

    def fnGoodbye(self):
        # await asyncio.sleep(1)
        print(time.time(), ": Run fnGoodbye:", self.__counter__)
        self.__counter__ += 1


engine = AsyncWrapper('engine')
data = engine.init(engine.load(engine.read('mainloop.json')), Cntn('mydata'))
data.engine(engine)

print('Validate: ', engine.validate('mainloop', data))

while data.get()["complete"] is not True:
    #data = engine.event(data)
    data = data.emit()
    #time.sleep(1)


# data = engine.event(data)
# print("State: ",data.get(data)["keystate"])
# print("Complete: ",data.get(data)["complete"])

def null():
    return


async def one():
    await asyncio.sleep(5)
    print("Complete One")


async def two():
    await asyncio.sleep(1)
    print("Complete Two")


async def three():
    await asyncio.sleep(3)
    print("Complete Three")


async def seqcall(aws):
    for f in aws:
        earliest_result = await f


print('Async function: ', asyncio.iscoroutinefunction(two))

asyncio.run(seqcall([one(), two(), three()]))
