
class Init:

    #read current session data
    @staticmethod
    def read_current():
        pass


    #set config variables
    @staticmethod
    def config():
        pass


    #get new session data from client
    @staticmethod
    def get_new_session_data():
        pass


    #add new session data to database
    @staticmethod
    def add_session():
        pass


    #lunch session tables and lists
    @staticmethod
    def lunch():
        pass


    #--------------------------------APP TABLE DATA--------------------------------#

    AppTableData = """ CREATE TABLE IF NOT EXISTS tasks (
    					id integer PRIMARY KEY,
    					title text NOT NULL,
    					comment text,
    					status integer NOT NULL,
    					created_at text NOT NULL,
    					end_at text,
    					indexed integer NOT NULL
    					); """