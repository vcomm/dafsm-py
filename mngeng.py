import json
from dafsm import Dafsm

class Content:
  __arg__ = {
    "logic": None,
    "keystate": None,
    "complete": True
  }
  _status_ = []

  def get(self):
    return self.__arg__
  def set(self, name, value):
    self.__arg__[name] = value
    return self.__arg__

class Wrapper(Dafsm):
  _logics_ = {}

  def __init__(self, dictionary, name):
      super().__init__(name)
      self.bios = dictionary
      self.cntx = Content

  def call(self, fname, cntx):
      if fname in self.bios:
        return self.bios.get(fname)(cntx)
      else:
        print("The function reference key: "+fname+" not exist")
        return None

  def load(self, jsonstr):
    logic = json.loads(jsonstr)
    lname = logic["prj"]+logic["id"]
    self._logics_.update({lname: logic})
    return lname

  def init(self, lname):
    logic = self._logics_.get(lname)
    iState = super().getByKey(logic['states'],'key','init')
    if iState != None:
      self.cntx._status_.append({'logic': lname, 'keystate': iState['key'], 'complete': False})
    return self.cntx._status_

  def loadLogic(self, jsonlogic):
      self.cntx.set(self.cntx,"logic",json.loads(jsonlogic))
      states = self.cntx.get(self.cntx)['logic']['states']
      iState = super().getByKey(states,"key","init")
      if iState != None:
        self.cntx.set(self.cntx,"complete",False)
        self.cntx.set(self.cntx,"keystate",iState)
        print("Initialization completed")
        return self.cntx
      else:
        print("Error: cannot find init state")
      return None
