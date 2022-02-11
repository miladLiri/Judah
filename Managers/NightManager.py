from Managers.Manager import Manager
from Resources.nt_archive import nt_archive
from Lib.Time import Time
from Resources.Tasks import Task
from Lib.Query import Query
from Presentation.Styles import NightStyle
from Lib.Messages import Messages
import config


class NightManager(Manager):

    start_handle = False


    #process query for starting night mode
    @staticmethod
    def process(query):

        if not isinstance(query, Query):
            return

        NightManager.start_handle = NightManager.set_previous_start_handle()
        head = query.getHead()

        if head == "":
            NightManager.start_handle = NightManager.start()
            if not NightManager.start_handle:
                return False

        return NightManager.micro_process(query)


    #dispatch night mode query
    @staticmethod
    def micro_process(query, internal_head = False):

        if not NightManager.start_handle:
            Messages.push(Messages.Type.NOTICE, "you should start night mode to use nt commands")
            return False

        head = ""
        if internal_head:
            head = internal_head
        else:
            head = query.getHead()

        if head == "end":
            return NightManager.end()

        elif head == "status":
            return NightStyle.status( NightManager.status() )

        elif head == "add":
            return NightManager.add(query.getParameters()[0], query.getParameters()[1:], query.getBinarySwitches()["index"])

        elif head == "unset":
            return NightManager.unset(query.getParameters(), query.getBinarySwitches()["index"])

        elif head == "del":
            return NightManager.delete(query.getParameters(), query.getBinarySwitches()["index"])

        else:
            Messages.push(Messages.Type.ERROR, "invalid command")
            return False


    #start night mode
    @staticmethod
    def start():

        #check night duration
        if not NightManager.check_nt_duration():
            Messages.push(Messages.Type.NOTICE, f"night mode can be started {config.NT_DURATION} hours after last night mode")
            return False

        #check previous start
        if not NightManager.check_previous_start():
            Messages.push(Messages.Type.NOTICE, "night mode is already started")
            return False

        #confirm message
        confirm_message = "if night mode starts: \n" \
                          "all changes in todo and optional list will be saved  \n" \
                          "lists will be empty for next day \n" \
                          "new resources can't be added \n" \
                          "confirm start night mode (y/n) :"

        confirm = input(NightStyle.confirm_message(confirm_message))
        if confirm != "y" and confirm != "Y":
            Messages.push(Messages.Type.NOTICE, "night mode canceled")
            return False

        #save to do and optional list of day
        Manager.tdl.set()
        Manager.opt.set()

        # make new archive record with now time for start
        nt_archive.start()

        #empty especial lists
        Manager.tdl.clear().set()
        Manager.opt.clear().set()

        #return start handle
        start_handle = nt_archive.last_start()
        if start_handle:
            Messages.push(Messages.Type.SUCCESS, "night mode started !!")
        else:
            Messages.push(Messages.Type.NOTICE, "night mode canceled")


    #end night mode
    @staticmethod
    def end():

        confirm_message = "confirm end night mode (y/n) ?"
        confirm = input(NightStyle.confirm_message(confirm_message))
        if confirm != "y" and confirm != "Y":
            return False
        nt_archive.end(NightManager.start_handle)
        start_handle = NightManager.set_previous_start_handle()
        Messages.push(Messages.Type.SUCCESS, "day begins !!")

    #show all remaining tasks and tdl/opt
    @staticmethod
    def status():

        data = dict({
            "tdl": Manager.tdl_present_data(),
            "opt": Manager.opt_present_data(),
            "tasks" : Manager.all_tasks_present_data()
        })

        return data


    #add task to opt/tdl
    @staticmethod
    def add(target_list, tasks, indices = False):

        items = Manager.select_from_all_tasks(tasks, indices)
        if not items:
            return False

        if target_list == "tdl":

            for item in items:
                if Manager.opt.has(item):
                    Messages.push(Messages.Type.NOTICE, f"Optional list already has task {item}")
                    items.remove(item)

            Manager.tdl.append(items).set()

        elif target_list == "opt":

            for item in items:
                if Manager.tdl.has(item):
                    Messages.push(Messages.Type.NOTICE, f"ToDo list already has task {item}")
                    items.remove(item)

            Manager.opt.append(items).set()

        else:
            Messages.push(Messages.Type.ERROR, "invalid target list")

        return NightManager.micro_process(False,"status")


    #remove item from opt/tdl
    @staticmethod
    def unset(tasks, indices = False):

        items = Manager.select_from_special_list(tasks, indices)
        if not items:
            return False

        for item in items:

            if Manager.tdl.has(item):
                Manager.tdl.get().remove(item).set()
            elif Manager.opt.has(item):
                Manager.opt.get().remove(item).set()

        return NightManager.micro_process(False,"status")


    #delete task
    @staticmethod
    def delete(tasks, indices = False):

        items = Manager.select_from_all_tasks(tasks, indices)
        if not items:
            return False

        for item in items:
            if Manager.tdl.has(item):
                Manager.tdl.remove(item).set()
            elif Manager.opt.has(item):
                Manager.opt.remove(item).set()

            Task(item).get().delete()

        return NightManager.micro_process(False,"status")



    #helper functions


    @staticmethod
    def check_nt_duration():

        last_end = nt_archive.last_end()

        if not last_end:
            return True
        else:
            then = Time().translate(last_end,True)

        duration = round( Time.duration( Time(), then ) / (3600) ) -1

        if duration > config.NT_DURATION :
            return True
        else:
            return False


    @staticmethod
    def check_previous_start():

        start = nt_archive.last_start()
        end = nt_archive.last_end()

        if start and not end :
            return False

        return True


    @staticmethod
    def set_previous_start_handle():

        start = nt_archive.last_start()
        end = nt_archive.last_end()

        if end :
            return False

        elif not end and start:
            return start

        else:
            return False




