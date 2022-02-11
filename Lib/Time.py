from datetime import datetime
from persiantools.jdatetime import JalaliDateTime
import config


calendar = config.CALENDAR

class Time:

    def __init__(self):
        self.time = datetime.now()

    def get(self):

        if calendar == "normal" :
            return self.time.strftime("%A %Y/%d/%B %H:%M")

        elif calendar == "persian":
            return JalaliDateTime(self.time).strftime("%A %Y/%B/%d %H:%M")

    def translate(self,date_str, normal = False):

        if calendar == "normal" or normal:
            self.time = datetime.strptime(date_str,"%A %Y/%d/%B %H:%M")

        elif calendar == "persian":
            self.time = JalaliDateTime.strptime(date_str, "%A %Y/%B/%d %H:%M")

        return self


    @staticmethod
    def now(normal=False):
        if calendar == "normal" or normal:
            return datetime.now().strftime("%A %Y/%d/%B %H:%M")

        elif calendar == "persian":
            return JalaliDateTime(datetime.now()).strftime("%A %Y/%B/%d %H:%M")


    @staticmethod
    def duration(t1, t2):

        if not isinstance(t1, Time):
            return False

        if not isinstance(t2, Time):
            return False

        return (t1.time - t2.time).total_seconds()