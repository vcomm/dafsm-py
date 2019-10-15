class Dafsm(object):

    # Constructor
    def __init__(self, name):
        self.name = name

    def trigger(self, fname, cntx):
        raise NotImplementedError()

    def call(self, fname, cntx):
        raise NotImplementedError()

    def queuecall(self, cntx):
        raise NotImplementedError()

    def switch(self, cntx, sstate):
        raise NotImplementedError()

    def unswitch(self, cntx):
        raise NotImplementedError()

    def getByKey(self, obj, key, value):
        item = None
        if type(obj) is list:
            for x in obj:
                if x[key] == value:
                    item = x
        elif type(obj) is dict:
            item = obj[value]
        return item

    def eventListener(self, cntx):
        # fsm = cntx.get(cntx)["logic"]
        # state = self.getByKey(fsm.get("states"), "key", cntx.get(cntx)["keystate"])
        state = cntx.get(cntx)["keystate"]
        if state is None:
            return None
        transitions = state.get("transitions")
        if transitions is not None:
            for trans in transitions:
                triggers = trans.get("triggers")
                if triggers is not None:
                    for trig in triggers:
                        res = self.trigger(trig.get("name"), cntx)
                        if res:
                            return trans
        return None

    def gotoNextstate(self, trans, fsm):
        return self.getByKey(fsm.get("states"), "key", trans.get("nextstatename"))

    def exitAction(self, cntx):
        # fsm = cntx.get(cntx)["logic"]
        # state = self.getByKey(fsm.get("states"), "key", cntx.get(cntx)["keystate"])
        state = cntx.get(cntx)["keystate"]
        if state is None:
            return None
        exits = state.get("exits")
        if exits is not None:
            for action in exits:
                self.call(action.get("name"), cntx)
        return

    def entryAction(self, cntx):
        # fsm = cntx.get(cntx)["logic"]
        # state = self.getByKey(fsm.get("states"), "key", cntx.get(cntx)["keystate"])
        state = cntx.get(cntx)["keystate"]
        if state is None:
            return None
        entries = state.get("entries")
        if entries is not None:
            for action in entries:
                self.call(action.get("name"), cntx)
        return

    def stayAction(self, cntx):
        # fsm = cntx.get(cntx)["logic"]
        # state = self.getByKey(fsm.get("states"), "key", cntx.get(cntx)["keystate"])
        state = cntx.get(cntx)["keystate"]
        if state is None:
            return None
        stays = state.get("stays")
        if stays is not None:
            for action in stays:
                self.call(action.get("name"), cntx)
        return

    def effectAction(self, trans, cntx):
        effects = trans.get("effects")
        if effects is not None:
            for eff in effects:
                self.call(eff.get("name"), cntx)
        return

    def event(self, cntx):
        try:
            keystate = cntx.get(cntx)["keystate"]
            if keystate is not None:
                #print(cntx.get(cntx)['logic']['id'],"[",keystate['key'],"]")
                trans = self.eventListener(cntx)
                if trans is not None:
                    nextstate = self.gotoNextstate(trans, cntx.get(cntx)["logic"])
                    if nextstate is not None:
                        self.exitAction(cntx)
                        self.effectAction(trans, cntx)
                        cntx.set(cntx, "keystate", nextstate)
                        self.entryAction(cntx)
                        superstate = nextstate.get("superstate")
                        if superstate is not None:
                            self.switch(cntx, superstate, nextstate.get("name"))
                        self.queuecall(cntx)
                        #print(cntx.get(cntx)['logic']['id'], "[", cntx.get(cntx)["keystate"]['key'], "]")
                    else:
                        print("FSM error: next state missing")
                else:
                    self.stayAction(cntx)
                    self.queuecall(cntx)
        except BaseException as err:
            print(err)
        finally:
            state = cntx.get(cntx)["keystate"]
            if state and state.get("transitions") is None:
                cntx.set(cntx, "complete", True)
                self.unswitch(cntx)
            return cntx
