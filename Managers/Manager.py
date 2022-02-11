from Lists import TaskList
from Resources.Tasks import Task
from Lib.Messages import Messages


class Manager:

    tdl = TaskList.SpecialList("ToDoList").get()
    opt = TaskList.SpecialList("OptionalList").get()


    # process query
    @staticmethod
    def process(query, internal_head = False):
        pass

    #preparing tdl data for show in terminal
    @staticmethod
    def tdl_present_data():

        tdlTasks = Manager.tdl.tasks()
        data = list()

        index = 0
        for item in tdlTasks:
            data.append(dict({
                "index": index,
                "title": item.title,
                "comment": item.comment,
                "status": item.status,
            }))
            index += 1

        return data


    # preparing tdl data for show in terminal
    @staticmethod
    def opt_present_data():

        optTasks = Manager.opt.tasks()
        data = list()

        index = len(Manager.tdl.data()["items"])
        for item in optTasks:
            data.append(dict({
                "index": index,
                "title": item.title,
                "comment": item.comment,
                "status": item.status,
            }))
            index += 1

        return data


    # preparing un indexed tasks data for present in terminal
    @staticmethod
    def all_tasks_present_data():

        tasks = Task.all()
        data = list()
        if not tasks:
            return data

        index = 0
        for item in tasks:

            if item.isDone():
                continue

            data.append(dict({
                "index": index,
                "title": item.title,
                "comment": item.comment,
                "status": item.status,
            }))
            index += 1

        return data


    # selecting data from all tasks
    @staticmethod
    def select_from_all_tasks(tasks, indices=False):

        all_tasks = Manager.all_tasks_present_data()
        items = list()

        if indices:
            for index in tasks:
                index = int(index)

                # check index validation
                if not index >= 0 or not index < len(all_tasks):
                    Messages.push(Messages.Type.ERROR, f"invalid task index {index}")
                    continue

                items.append(all_tasks[index]["title"])

        elif tasks and not indices:
            for task_title in tasks:

                # check title validation
                flag = True
                for task_data in all_tasks:
                    if task_data["title"] == task_title:
                        flag = False
                if flag:
                    Messages.push(Messages.Type.ERROR, f"invalid task {task_title}")
                    continue

                items.append(task_title)

        return items


    #selecting data from tdl/opt list
    @staticmethod
    def select_from_special_list(tasks, indices = False):

        items = list()

        if indices:
            for index in tasks:
                index = int(index)

                # check index validation
                if index >= 0 and index < len(Manager.tdl.tasks()):
                    items.append(Manager.tdl.data()["items"][index])

                elif index >= len(Manager.tdl.tasks()) and index < len(Manager.tdl.tasks()) + len(Manager.opt.tasks()):
                    items.append(Manager.opt.data()["items"][index - len(Manager.tdl.tasks())])

                else:
                    Messages.push(Messages.Type.ERROR, f"invalid task index {index}")


        elif tasks and not indices:
            for task_title in tasks:

                # check title validation
                if Manager.tdl.has(task_title):
                    items.append(task_title)

                elif Manager.opt.has(task_title):
                    items.append(task_title)

                else:
                    Messages.push(Messages.Type.ERROR, f"invalid task {task_title}")

        return items

















