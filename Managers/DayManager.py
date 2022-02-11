from Managers.Manager import Manager
from Lib.Query import Query
from Resources.Tasks import Task
from Managers.NightManager import NightManager
from Presentation.Styles import DayStyle
from Lib.Messages import Messages

class DayManager(Manager):


    #dispatch query
    @staticmethod
    def process(query, internal_head = False):

        if NightManager.set_previous_start_handle():
            Messages.push(Messages.Type.NOTICE, "you are still in night mode. you must close the night mode first")
            return False

        head = str()
        if internal_head:
            head = internal_head
        else:
            head = query.getHead()


        if head == "" or head == "show":
           return DayStyle.show( DayManager.show() )


        elif head == "done":
           return  DayManager.done(query.getParameters(), query.getBinarySwitches()["index"])


        elif head == "undo":
           return DayManager.undo(query.getParameters(), query.getBinarySwitches()["index"])


        elif head == "del":
            return DayManager.delete(query.getParameters(), query.getBinarySwitches()["index"])


        elif head == "new":
            return DayManager.new(query.rPopHead())

        else:
            Messages.push(Messages.Type.ERROR, "invalid command")
            return False


    #show todolist and optional list data
    @staticmethod
    def show():

        data = dict({
            "tdl" : Manager.tdl_present_data(),
            "tdlProgress" : str(Manager.tdl.calculate_progress()) + "%",
            "opt" : Manager.opt_present_data(),
            "optProgress" : str(Manager.opt.calculate_progress()) + "%",
        })

        return data


    #change task status to done
    @staticmethod
    def done(tasks, indices = False):

        items = Manager.select_from_special_list(tasks, indices)
        if not items:
            return False

        for item in items:
            Task(item).get().done().set()

        Manager.tdl.set()
        Manager.opt.set()

        return DayManager.process(False,"show")


    #change task status to not done
    @staticmethod
    def undo(tasks, indices = False):

        items = Manager.select_from_special_list(tasks,indices)
        if not items:
            return False

        for item in items:
            Task(item).get().undo().set()

        Manager.tdl.set()
        Manager.opt.set()

        return DayManager.process(False,"show")


    #remove task from todolist and optional list
    @staticmethod
    def delete(tasks, indices = False):

        items = Manager.select_from_special_list(tasks, indices)
        if not items:
            return False

        for item in items:
            if Manager.tdl.has(item):
                Manager.tdl.remove(item).set()
            elif Manager.opt.has(item):
                Manager.opt.remove(item).set()

        return DayManager.process(False,"show")


    #create new resource
    @staticmethod
    def new(query):

        if not isinstance(query, Query):
            return False

        head = query.getHead()

        if head == "task":
            Task(query.parameters[0],query.getSwitches()["comment"]).add()

        else:
            Messages.push(Messages.Type.ERROR, "invalid Resource type")
            return False

        Messages.push(Messages.Type.SUCCESS, "new Resource added")