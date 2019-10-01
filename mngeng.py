import json
import asyncio
from dafsm import Dafsm


class ValidateException(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        super()
        self.value = value


class Content:
    _arg_ = {
        "logic": None,
        "keystate": None,
        "complete": True
    }
    _status_ = []

    # Constructor
    def __init__(self, name):
        self.name = name

    def bios(sel):
        raise NotImplementedError()

    def get(self):
        return self._arg_

    def set(self, name, value):
        self._arg_[name] = value
        return self._arg_

    def shift(self, logic, istate):
        if (logic or istate) is None:
            return None
        # Update status list
        item = self._status_[-1]
        item['keystate'] = self._arg_['keystate']['key']
        item['complete'] = self._arg_['complete']
        # -------------------
        self.set(self, "logic", logic)
        self.set(self, "complete", False)
        self.set(self, "keystate", istate)
        self._status_.append({'logic': logic["id"], 'keystate': istate['key'], 'complete': False})
        return self

    def unshift(self, manager):
        # remove insulated child logic
        item = self._status_[-1]
        self._status_.remove(item)
        # restore parent logic
        item = self._status_[-1]
        lname = item['logic']
        logic = manager._logics_[lname]
        self.set(self, "logic", logic)
        self.set(self, "complete", item['complete'])
        istate = manager.getByKey(logic['states'], 'key', item['keystate'])
        self.set(self, "keystate", istate)
        return self


class Wrapper(Dafsm):
    _logics_ = {}
    _seqfuncs_ = []

    def __init__(self, name, content):
        super().__init__(name)
        if issubclass(content, Content):
            self.bios = content.bios(content)
            self.cntx = content
        else:
            print("Error: Wrong Content inheritance")

    def trigger(self, fname, cntx):
        if fname in self.bios:
            return self.bios.get(fname)(cntx)
        else:
            print("The function reference key: " + fname + " not exist")
            return None

    def call(self, fname, cntx):
        self._seqfuncs_.append(self.bios.get(fname))
        print('Accelerate functions seq')

    def queuecall(self, cntx):
        for func in self._seqfuncs_:
            result = func(cntx)
        self._seqfuncs_.clear()
        print('Execute Queue calls')

    def switch(self, cntx, sstate, name):
        if name != '*':
            logic = self._logics_.get(name)
            if logic is None:
                logic = self.load(self.read(sstate.get("link")))
            self.cntx.shift(self.cntx, logic, super().getByKey(logic['states'], 'key', 'init'))
        else:
            logic = self.load(self.read(sstate.get("link")))
            self.cntx.shift(self.cntx, logic, super().getByKey(logic['states'], 'key', 'init'))
        return super().event(cntx)

    def unswitch(self, cntx):
        self.cntx.unshift(self.cntx, self)
        return super().event(cntx)

    def read(self, link):
        with open(link) as f:
            fsm = json.load(f)
        return fsm

    def load(self, json):
        if type(json) is str:
            logic = json.loads(json)
        else:
            logic = json
        lname = logic["id"]
        self._logics_.update({lname: logic})
        return logic

    def validate(self, lname):
        status = True
        try:
            logic = self._logics_.get(lname)
            states = logic['states']
            if type(states) is list:
                for state in states:
                    exits = state.get("exits")
                    if exits is not None:
                        for ext in exits:
                            fnc_name = ext.get("name")
                            if self.bios.get(fnc_name) is None:
                                raise ValidateException('Wrong Exit function: ' + fnc_name)

                    stays = state.get("stays")
                    if stays is not None:
                        for stay in stays:
                            fnc_name = stay.get("name")
                            if self.bios.get(fnc_name) is None:
                                raise ValidateException('Wrong Stay function: ' + fnc_name)

                    entries = state.get("entries")
                    if entries is not None:
                        for ent in entries:
                            fnc_name = ent.get("name")
                            if self.bios.get(fnc_name) is None:
                                raise ValidateException('Wrong Entry function: ' + fnc_name)

                    transitions = state.get("transitions")
                    if transitions is not None:
                        for trans in transitions:
                            triggers = trans.get("triggers")
                            if triggers is not None:
                                for trig in triggers:
                                    fnc_name = trig.get("name")
                                    if self.bios.get(fnc_name) is None:
                                        raise ValidateException('Wrong Trigger function: ' + fnc_name)
                            effects = trans.get("effects")
                            if effects is not None:
                                for eff in effects:
                                    fnc_name = eff.get("name")
                                    if self.bios.get(fnc_name) is None:
                                        raise ValidateException('Wrong Effect function: ' + fnc_name)
            elif type(states) is dict:
                raise ValidateException('State List is dictionary')
        except ValidateException as err:
            print('Validate Exception Error: ', err.value)
            status = False
        except BaseException as err:
            print('Logic Exception Error: ', err)
            status = False
        finally:
            return status

    def init(self, logic):
        iState = super().getByKey(logic['states'], 'key', 'init')
        if iState != None:
            self.cntx.set(self.cntx, "logic", logic)
            self.cntx.set(self.cntx, "complete", False)
            self.cntx.set(self.cntx, "keystate", iState)
            self.cntx._status_.append({'logic': logic["id"], 'keystate': iState['key'], 'complete': False})
            print("Initialization completed:", logic["prj"] + logic["id"])
            return self.cntx
        else:
            print("Error: cannot find init state")
        return None

    def loadLogic(self, jsonlogic):
        self.cntx.set(self.cntx, "logic", json.loads(jsonlogic))
        states = self.cntx.get(self.cntx)['logic']['states']
        iState = super().getByKey(states, "key", "init")
        if iState != None:
            self.cntx.set(self.cntx, "complete", False)
            self.cntx.set(self.cntx, "keystate", iState)
            print("Initialization completed")
            return self.cntx
        else:
            print("Error: cannot find init state")
        return None


class AsyncWrapper(Wrapper):
    # Constructor
    def __init__(self, name, content):
        super().__init__(name, content)

    async def seqcall(self, cntx):
        for func in self._seqfuncs_:
            if asyncio.iscoroutinefunction(func) is True:
                await func(cntx)
            else:
                func(cntx)

    def call(self, fname, cntx):
        self._seqfuncs_.append(self.bios.get(fname))
        print('Accelerate functions seq')

    def queuecall(self, cntx):
        asyncio.run(self.seqcall(cntx))
        self._seqfuncs_.clear()
        print('Execute Queue calls')
