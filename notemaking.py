#!/usr/bin/python3.6

import os
import sqlite3
import datetime
import sys
from termcolor import colored


home = os.environ.get('HOME')
subfoldername = 'Notedatabase'
filepath = os.path.join(home, subfoldername)

os.makedirs(filepath, exist_ok=True)

targetpath = os.path.join(filepath, 'mydb.db')


class Mynotes():
    Default_status = "N"
    Workdone_status = "_Done_"
    currnet_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def __init__(self):
        self.Create_conn()

    def Create_conn(self):
        self.conn = sqlite3.connect(f'{targetpath}')
        self.conn2 = sqlite3.connect(f'{targetpath}')
        self.cus = self.conn.cursor()
        self.cus_2 = self.conn2.cursor()
        self.cus.execute(
            'CREATE TABLE IF NOT EXISTS Todo_database(ID INTEGER PRIMARY KEY AUTOINCREMENT, Created_on timestamp, Mynotes TEXT, Status TEXT )  ')

        self.cus_2.execute(
            'CREATE TABLE IF NOT EXISTS Work_done_database(ID, Created_on timestamp, Mynotes TEXT, Status TEXT )  ')

    def data_entry(self):

        try:

            noteinpt = str(input("Eneter your todo : "))

            self.cus.execute(
                " INSERT INTO Todo_database (Created_on, Mynotes, status) VALUES (?, ?, ?) ", (self.currnet_date, noteinpt, self.Default_status))
            self.conn.commit()

        except KeyboardInterrupt as e:
            print("\n Exiting...")

    def Read_database(self):
        print("\t\t-----My Todos-----")
        print()
        data = self.cus.execute(
            """SELECT * FROM Todo_database ORDER BY -ID """)

        records = data.fetchall()
        total = len(records)
        for data in records:

            ID = data[0]
            Date = data[1]
            Notes = data[2]

            print(
                f" \t\t| {Date} | [ {ID:02} ] | {colored(Notes,'green')}")

        print(f"\n\t\t\t\t\t\t\tTotal tasks {colored(total,'cyan')} ")

    def update_and_delete(self):
        try:
            ID_VALUE = int(input("Update task, Enter ID number : "))

            self.cus.execute(
                f"SELECT * FROM Todo_database WHERE ID ={ID_VALUE}")
            d_v = self.cus.fetchone()
            self.conn.commit()
            self.cus.execute(
                f"DELETE from Todo_database where ID = {ID_VALUE} ")
            # print(d_v)
            self.conn.commit()

            self.cus_2.execute(
                " INSERT INTO Work_done_database (ID,Created_on, Mynotes, status) VALUES (?,?, ?, ?) ", d_v)

            self.cus_2.execute(
                f" UPDATE Work_done_database SET status= '{self.Workdone_status}' WHERE ID={ID_VALUE}")

            self.conn2.commit()

            self.wdone()

        except Exception as e:
            pass
        except KeyboardInterrupt as e:
            print("\nExiting...")
            sys.exit()

    def wdone(self):
        print("\n\t\t-----WORK DONE-----\n")
        data = self.cus.execute(
            """SELECT * FROM Work_done_database ORDER BY -ID """)

        records = data.fetchall()

        total = len(records)
        for data in records:

            ID = data[0]
            Date = data[1]
            Notes = data[2]

            print(
                f" \t\t| {Date} | [ {ID:02} ]  |  {colored(Notes,'green')}")

        print(f"\n\t\t\t\t\t\t\tTask completed {colored(total,'cyan')} ")

    def Connection_Close(self):
        self.conn.close()
        self.conn2.close()


def main():

    me = Mynotes()

    print("""
        \n\t Enter 'ls '  To list all tasks...
        \n\t Enter 'ii '  To add the task...
        \n\t Enter 'lsw'  To list all completed tasks...
        \n\t Enter 'dd'   To mark task as Done...
        \n\t Enter 'q or Ctrl+c ' To Exit...
          """)

    while True:
        try:
            choice = input("Enter ur choice >> ")

            if choice == "ls":
                print()
                me.Read_database()
                print()

            elif choice == "ii":
                print()
                me.Read_database()
                me.data_entry()

                print()

            elif choice == "dd":
                print()
                print(
                    "Enter ID number to update the Task...You can see completed tsk by entering 'lsw' ")
                me.Read_database()
                me.update_and_delete()
                print()

            elif choice == 'lsw':
                print()
                me.wdone()
                print()

            elif choice == 'q':

                me.Connection_Close()
                sys.exit()

        except KeyboardInterrupt as e:
            print("\nExiting...")
            sys.exit()


if __name__ == '__main__':
    main()
