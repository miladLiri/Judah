from Lib.Time import Time
from Lib import Sqlite
from Resources.Resource import Resource
from Lib.Messages import Messages

"""
task:
 ->title
 ->comment
 ->status
 ->created_at
 ->end_at
 ->indexed
"""

class Task(Resource):


    table = "tasks"
    key = "title"


    def __init__(self, title, comment = ""):

        self.title = title
        self.comment = comment
        self.status = 0
        self.end_at = 0
        self.created_at = 0
        self.indexed = 0

    def exists(self):

        if not Sqlite.exists(self.table, self.key, self.title):
            return False

        return True

    def get(self):

        if not self.exists():
            Messages.push(Messages.Type.ERROR, f"task {self.title} not found")
            return False

        data = Sqlite.read(self.table, self.key, self.title)[0];

        self.title = data[1]
        self.comment = data[2]
        self.status = data[3]
        self.created_at = data[4]
        self.end_at = data[5]
        self.indexed = data[6]

        return self

    def add(self):

        if self.exists():
            return self.get()

        if self.created_at == 0 :
            self.created_at = Time().get()

        if self.status == 1 :
            self.end_at = Time().get()

        data = self.data()

        Sqlite.create(self.table, data)

        return self

    def done(self):
        self.status = 1
        return self

    def isDone(self):
        return self.status

    def undo(self):
        if self.status == 1:
            self.status = 0

        return self

    def index(self):
        self.indexed = 1
        return self

    def isIndexed(self):
        return self.indexed

    def delete(self):

        if not self.exists():
            Messages.push(Messages.Type.ERROR, f"task {self.title} not found")
            return False

        Sqlite.delete("tasks","title",self.title)
        return self

    def data(self):

        return {
            "title" : self.title,
            "comment" : self.comment,
            "status" : self.status,
            "created_at" : self.created_at,
            "end_at" : self.end_at,
            "indexed" : self.indexed
        }

    def set(self):

        if not self.exists():
            return self.add()

        data = self.data()
        Sqlite.update(self.table, self.key, self.title, data)
        return self


    @staticmethod
    def all():
        data = list()
        tasks = Sqlite.read_all("tasks")

        if not tasks:
            return False

        for task in tasks:
            taskObj = Task(task[1]).get()
            if not taskObj.indexed:
                data.append(taskObj)

        return data


    @staticmethod
    def all_titles():

        data = list()
        tasks = Sqlite.read_all("tasks")

        if not tasks:
            return False

        for task in tasks:
            taskObj = Task(task[1]).get()
            if not taskObj.indexed:
                data.append(task[1])

        return data