import json
from dafsm import Dafsm


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
        self.set(self,"logic", logic)
        self.set(self,"complete", False)
        self.set(self,"keystate", istate)
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
        self.set(self,"logic", logic)
        self.set(self,"complete", item['complete'])
        istate = manager.getByKey(logic['states'], 'key', item['keystate'])
        self.set(self,"keystate", istate)
        return self


class Wrapper(Dafsm):
    _logics_ = {}

    def __init__(self, name, dictionary, content):
        super().__init__(name)
        if issubclass(content, Content):
            self.bios = dictionary
            self.cntx = content
        else:
            print("Error: Wrong Content inheritance")

    def call(self, fname, cntx):
        if fname in self.bios:
            return self.bios.get(fname)(cntx)
        else:
            print("The function reference key: " + fname + " not exist")
            return None

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
