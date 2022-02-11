from Resources.Resource import Resource
import Lib.Sqlite

class List:

    table = "lists"
    key = "title"

    def __init__(self, title, sample_resource, items):

        self.title = title
        self.sample = sample_resource
        self.items = list()

        for item,comment in items.items():

            sample = Resource()
            sample = sample_resource
            sample.title = item

            if sample.exists():
                sample.get()
                sample.comment = comment
                sample.index().set()
            else:
                sample.comment = comment
                sample.index().add()

            self.items.append(item)


    def add(self):
        pass

    