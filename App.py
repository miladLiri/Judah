from Lib.Query import Query
from Managers.DayManager import DayManager
from Managers.NightManager import NightManager
from Lib.Messages import Messages
from Presentation.Styles import MessageStyle

class App:

    @staticmethod
    def Request_Dispatch(request):

        request = Query(request)
        head = request.getHead()
        Response = False

        if head == "nt":
            Response = NightManager.process(request.rPopHead())
        else:
            Response = DayManager.process(request)

        if Response:
            print(Response)



    @staticmethod
    def Show_Messages():

        messages = Messages.flush()
        if not messages:
            return

        for message in messages:
            print( MessageStyle.show_message( message.get_string(), message.get_color() ) )