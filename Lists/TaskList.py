from Resources.Tasks import Task
import json
from Lib.Time import Time
from Lib import Sqlite
from Lib.Messages import Messages

# id integer PRIMARY KEY,
# title text NOT NULL,
# comment text,
# items text,
# progress text NOT NULL,
# created_at text NOT NULL,
# end_at text,
# indexed integer NOT NULL


class TaskList:


    table = "lists"
    key = "title"



    def __init__(self, title, items = "", comment = ""):

        self.title = title
        self.comment = comment
        self.created_at = 0
        self.end_at = 0
        self.progress = 0
        self.indexed = 0
        self.items = dict()

        if items != "":
            for item, comm in items.items():
                if not self.has(item):
                    self.items.update({ item : Task(item, comm) })


    def exists(self):

        if not Sqlite.exists(self.table, self.key, self.title):
            return False

        return True


    def calculate_progress(self):

        items = self.data()["items"]

        if not items:
            return 0

        all = len(items)
        done = 0

        for item in items:
            if Task(item).get().isDone():
                done += 1

        return round((done / all)*100)


    def get(self):

        if not self.exists():
            Messages.push(Messages.Type.ERROR, f"list {self.title} not found")
            return False

        data = Sqlite.read(self.table, self.key, self.title)[0];

        self.title = data[1]
        self.comment = data[2]

        self.items = dict()
        items = list(json.loads(data[3]))
        for item in items:
            self.items.update({item: Task(item).get()})

        self.progress = self.calculate_progress()
        self.created_at = data[5]
        self.end_at = data[6]
        self.indexed = data[7]

        return self


    #contains task objects
    def tasks(self):
        return list(self.items.values())


    #contains task titles
    def data(self):

        return {
            "title": self.title,
            "comment": self.comment,
            "items": list(self.items.keys()),
            "progress": self.progress,
            "created_at": self.created_at,
            "end_at": self.end_at,
            "indexed": self.indexed
        }


    def add(self):

        if self.exists():
            return self.get()

        if not self.items :
            Messages.push(Messages.Type.ERROR, f"failed to add list {self.title} -> empty task list")
            return

        if self.created_at == 0:
            self.created_at = Time().get()

        if self.progress == 100:
            self.end_at = Time().get()

        data = self.data()
        data["items"] = json.dumps(data["items"])
        Sqlite.create(self.table, data)

        tasks = self.tasks()
        for task in tasks:

            if task.exists() :
                tempComment = task.comment
                task.get()
                task.comment = tempComment
                task.index().set()
            else:
                task.index().add()

        return self


    def isDone(self):
        return int(self.progress) == 100


    def index(self):
        self.indexed = 1
        return self


    def isIndexed(self):
        return self.indexed


    def destroy(self):

        if not self.exists():
            Messages.push(Messages.Type.ERROR, f"list {self.title} not found")
            return False

        tasks = self.get().tasks()

        for task in tasks:
            task.delete()

        Sqlite.delete(self.table, self.key, self.title)


    def set(self):

        if not self.exists():
            return self.add()

        tasks = self.tasks()
        for task in tasks:

            if task.exists():
                tempComment = task.comment
                task.get()
                if tempComment != task.comment:
                    task.comment = tempComment

                task.index().set()
            else:
                task.index().add()

        self.progress = self.calculate_progress()

        data = self.data()
        data["items"] = json.dumps(data["items"])
        Sqlite.update(self.table, self.key, self.title, data)
        return self


    def clear(self):
        self.items = dict()
        return self


    def append(self, items):

        if items != "":
            for item, comm in items.items():
                if not self.has(item):
                    self.items.update({item: Task(item, comm)})

        return self


    def has(self, title):

        tasks = self.data()["items"]

        for task in tasks:
            if task == title:
                return True

        return False


    def remove(self, title):
        self.items.pop(title)
        return self




#built-in task lists
class SpecialList(TaskList):


    def __init__(self,title):
        super().__init__(title)


    def append(self, items):

        if items != "":
            for item in items:
                task = Task(item)
                if task.exists():
                    if not self.has(item):
                        self.items.update({ item : task.get() })
                    else:
                        Messages.push(Messages.Type.NOTICE, f"list already has task {item}")
        return self


    def add(self):

        if self.exists():
            return self.get()


        if self.created_at == 0:
            self.created_at = Time().get()

        data = self.data()
        data["items"] = json.dumps(data["items"])
        Sqlite.create(self.table, data)

        return self


    def set(self):

        if not self.exists():
            return self.add()

        self.progress = self.calculate_progress()

        tasks = self.tasks()
        for task in tasks:
            if task.exists():
                tempComment = task.comment
                task.get()
                if tempComment != task.comment:
                    task.comment = tempComment
                    task.set()


        data = self.data()
        data["items"] = json.dumps(data["items"])
        Sqlite.update(self.table, self.key, self.title, data)
        return self







#implement built-in special lists
def lists():
    SpecialList("ToDoList").add()
    SpecialList("OptionalList").add()