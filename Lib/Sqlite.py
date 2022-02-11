import sqlite3
from sqlite3 import Error
from Lib.Messages import Messages
import config


def connection(sqlite_file):

    if not sqlite_file:
        return

    connect = None

    try:
        connect = sqlite3.connect(sqlite_file)
        return connect

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to make database connection")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def create_table(table, SqliteTableData, db_name = False):

    if not db_name:
        db_name = database_name

    try:
        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(SqliteTableData)
        handle.close()

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to create table")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def create(table, data, db_name = False):

    data = dict(data)

    if not data :
        Messages.push(Messages.Type.ERROR, "failed to create record -> invalid data")
        return False

    query = """ INSERT INTO {tablename} {keys} VALUES {values}""".format(tablename = table, keys = tuple(data), values = tuple(data.values()))

    if not db_name:
        db_name = database_name

    try:
        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        handle.commit()
        handle.close()
        return curs.lastrowid

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to create new record")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def exists(table, key, value, db_name = False):

    query = """SELECT * FROM {tablename} WHERE {key} = '{value}'""".format(tablename=table, key=key, value=value)

    if not db_name:
        db_name = database_name

    try:
        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        row = curs.fetchall()
        handle.close()
        return bool(row)

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to check record existence")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def read(table, key, value, db_name = False):

    query = """SELECT * FROM {tablename} WHERE {key} = '{value}'""".format(tablename = table, key = key, value = value)

    if not db_name:
        db_name = database_name

    try:
        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        row = curs.fetchall()
        handle.close()

        if row :
            return row
        else:
            return False

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to select record")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def read_all(table, db_name = False):

    query = """SELECT * FROM {tablename} """.format(tablename=table)

    if not db_name:
        db_name = database_name

    try:
        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        rows = curs.fetchall()
        handle.close()

        if rows:
            return rows
        else:
            return False

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to select record")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def update(table, key, value, data, db_name = False):

    if not exists(table, key, value):
        Messages.push(Messages.Type.ERROR, "record not exists")
        return False

    data = dict(data)

    if not data :
        Messages.push(Messages.Type.ERROR, "failed to update record -> invalid data!")
        return False

    items = str()
    for k, v in data.items():
        items += " {in_k} = '{in_v}' , ".format(in_k = k, in_v = v)

    query = """UPDATE {tablename} SET {items} WHERE {in_key} = '{in_value}'""".format(tablename=table, items = items[1:len(items)-2], in_key = key, in_value = value)

    if not db_name:
        db_name = database_name

    try:

        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        handle.commit()
        handle.close()

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to update record")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def delete(table, key, value, db_name = False):

    if not exists(table,key,value):
        Messages.push(Messages.Type.ERROR, "record not exists")
        return False

    query = """DELETE  FROM {tablename} WHERE {in_key} = '{in_value}'""".format(tablename=table, in_key=key, in_value=value)

    if not db_name:
        db_name = database_name

    try:

        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        handle.commit()
        handle.close()

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to delete record")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def flush(table, db_name = False):

    query = """DELETE FROM {tablename}""".format(tablename = table)

    if not db_name:
        db_name = database_name

    try:

        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        handle.commit()
        handle.close()

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to flush table")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")


def drop_table(table, db_name = False):

    query ="""DROP TABLE {tablename}""".format(tablename = table)

    if not db_name:
        db_name = database_name

    try:

        handle = connection(db_name)
        curs = handle.cursor()
        curs.execute(query)
        handle.commit()
        handle.close()

    except Error as e:
        Messages.push(Messages.Type.ERROR, "failed to drop table")
        Messages.push(Messages.Type.ERROR, f"SQL: {e}")



# create app tables
def database () :

    create_table("tasks", TasksTableData)
    create_table("lists", ListsTableData)
    create_table("nt_archive", nt_archiveTableData)



#----------------------------Tables Data------------------------------------#

database_name = config.DB_NAME

TasksTableData = """ CREATE TABLE IF NOT EXISTS tasks (
					id integer PRIMARY KEY,
					title text NOT NULL,
					comment text,
					status integer NOT NULL,
					created_at text NOT NULL,
					end_at text,
					indexed integer NOT NULL
					); """

ListsTableData = """ CREATE TABLE IF NOT EXISTS lists (
					id integer PRIMARY KEY,
					title text NOT NULL,
					comment text,
					items text,
					progress text NOT NULL,
					created_at text NOT NULL,
					end_at text,
					indexed integer NOT NULL
					); """

nt_archiveTableData = """ CREATE TABLE IF NOT EXISTS nt_archive (
                        id integer PRIMARY KEY, 
                        start_at text NOT NULL,
                        end_at text,
                        todo text,
                        opt text,
                        progress text
                        ); """