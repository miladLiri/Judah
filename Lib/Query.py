"""
switches:
-c: comment
-i: index

binary switches:
-i -> indices

"""

class Query:

    def __init__(self, query):

        if not isinstance(query, str):
            return

        self.query = str(query)
        self.head = ""
        self.parameters = list()
        self.switches = dict()
        self.binary_switches = dict()

        if not query:
            return

        parts = query.strip().split(" ")
        data = list()

        addToLast = False
        for item in parts:

            if item:
                if addToLast:
                    if item.find("\"") != -1:
                        addToLast = False
                    data[len(data) - 1] += " " + item.replace("\"","")
                else:
                    if item.find("\"") != -1:
                        addToLast = True
                    data.append(item.replace("\"",""))


        self.head = data[0]
        self.parameters = data[1:]

        self.binary_switches.update({
            "comment": self.extract_switch("-c", True),
            "index": self.extract_switch("-i", True)
        })

        self.switches.update({
            "comment" : self.extract_switch("-c"),
            "index" : self.extract_switch("-i")
        })



    def getHead(self):
        return self.head

    def getParameters(self):
        return self.parameters

    def getSwitches(self):
        return self.switches

    def getBinarySwitches(self):
        return self.binary_switches


    #replace head with first parameter
    def popHead(self):

        self.query.replace(self.head, "").strip()
        self.head = self.parameters[0]
        self.parameters.pop(0)

    #return new popHead query
    def rPopHead(self):
        return Query(self.query.replace(self.head, "").strip())


    def extract_switch(self, switch, binary = False):

        params = list()
        for i in self.parameters:
            params.append(i)

        for i in range(len(params)):
            if params[i].find(switch) != -1:
                switchMarkLen = len(params[i])

                if switchMarkLen == 2: #-c ... binary switch
                    if binary:
                        self.parameters.pop(i)
                        return True

                elif switchMarkLen == 3: # -c: comment
                    if binary:
                        return False
                    self.parameters.pop(i)
                    self.parameters.pop(i)
                    return params[i+1]

                else: # -c:comment
                    if binary:
                        return False
                    self.parameters.pop(i)
                    return params[i][3:]

        return False

    #test
    def print(self):
        print("head -> ", self.getHead())
        print("parameters -> ", self.getParameters())
        print("switches -> ", self.getSwitches())
        print("binary switches -> ", self.getBinarySwitches())