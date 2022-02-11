from Lib import Sqlite
from App import App
from Lists import TaskList


Sqlite.database()
TaskList.lists()



while True:

    App().Show_Messages()
    App().Request_Dispatch(input())

