from mngeng import Wrapper

json_string = """
{
    "id": "loop",
    "type": "FSM",
    "prj": "main_",
    "complete": false,
    "start": {"name": "fnStart"},
    "stop": {"name": "fnStop"},
    "countstates": 3,
    "states": [
        {
          "key": "init",
          "name": "InitialState",
          "exits": [{"name": "fnLetsgo"}],
          "transitions": [
            {
              "nextstatename": "final",
              "triggers": [{"name": "evComplete"}],
              "effects": [{"name": "fnGoto"}]
            }
          ]
        },{
          "key": "final",
          "name": "FinalState",
          "entries": [{"name": "fnWelcome"}]
        }
    ]
}
"""


def fnStart(cntx):
    return print("Run fnStart:")


def fnStop(cntx):
    return print("Run fnStop:")


def fnLetsgo(cntx):
    return print("Run fnLetsgo:")


def evComplete(cntx):
    print("Run evComplete:")
    return True


def fnGoto(cntx):
    return print("Run fnGoto:")


def fnWelcome(cntx):
    return print("Run fnWelcome:")


dict = {
    "fnLetsgo": lambda cntx: fnLetsgo(cntx),
    "evComplete": lambda cntx: evComplete(cntx),
    "fnGoto": lambda cntx: fnGoto(cntx),
    "fnWelcome": lambda cntx: fnWelcome(cntx)
}

engine = Wrapper(dict,'test')
#print(engine.init(engine.load(json_string)))

data = engine.loadLogic(json_string)
data = engine.event(data)
print("State: ",data.get(data)["keystate"])
print("Complete: ",data.get(data)["complete"])

# engine.test()
# data = json.loads(json_string)
# print(data["prj"]+data["id"])
# print(engine.getByKey(data.get("logic")["states"],"key","init"))


# final = engine.getByKey(data.get(data)["logic"]["states"],"key","final")
# if "transitions" in final:
#  print("Yes, 'transitions' is one of the keys in the thisdict dictionary")
# else:
#  print(final.get("transitions"))
