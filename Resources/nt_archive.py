from Lib import Sqlite
from Lib.Time import Time
from Managers.Manager import Manager
from Lib.Messages import Messages
import json
from datetime import datetime

class nt_archive:

    table = "nt_archive"
    key = "start_at"

    #last night mode data
    @staticmethod
    def last():

        record = Sqlite.read_all(nt_archive.table)

        if not record:
            return False
        else:
            record = record[-1]

        data = {
            "start_at" : record[1],
            "end_at": record[2],
            "todo": record[3],
            "opt": record[4],
            "progress": record[5],
        }

        return data;

    #last night mode end_at
    @staticmethod
    def last_end():

        data = nt_archive.last()

        if not data:
            return False
        else:
            return data["end_at"]

    # last night mode start_at
    @staticmethod
    def last_start():

        data = nt_archive.last()

        if not data:
            return False
        else:
            return data["start_at"]

    # create new archive record when night mode starts
    @staticmethod
    def start():

        data = {
            "start_at": Time.now(True),
            "end_at": "",
            "todo": json.dumps(Manager.tdl.data()["items"]),
            "opt": json.dumps(Manager.opt.data()["items"]),
            "progress": Manager.tdl.progress
        }

        Sqlite.create(nt_archive.table,data)

    # add end_at time to archive record
    @staticmethod
    def end(start_handle):

        data = { "end_at": Time.now(True) }

        if not Sqlite.exists(nt_archive.table, nt_archive.key, start_handle,):
            Messages.push(Messages.Type.ERROR, f"archive record that starts at {start_handle} not found")
            return False;

        Sqlite.update(nt_archive.table, nt_archive.key, start_handle, data)