# coding=utf-8
'''
CREATE TABLE Tickets (
    id INT(11) AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    selected_numbers VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);
'''
from dbconnection import DBconnection


db = DBconnection(user='root', password='coderslab', database='LotteryDB')
cnx = db.cnx
cursor = db.cursor


class Ticket():
    __id = None
    first_name = None
    last_name = None
    selected_numbers = None

    def __init__(self):
        self.__id = -1
        self.first_name = ""
        self.last_name = ""
        self.selected_numbers = ""

    def __str__(self):
        return "{} {} Wybrane liczby: {}".format(self.first_name, self.last_name, self.selected_numbers)

    @property
    def id(self):
        return self.__id

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO Tickets(first_name, last_name, selected_numbers) VALUES ('{}', '{}', '{}')"""
            cursor.execute(sql.format(self.first_name, self.last_name, self.selected_numbers))
            print(self.first_name, self.last_name, self.selected_numbers)
            cnx.commit()
            print(cursor.lastrowid)
            self.__id = cursor.lastrowid
            return True
        else:
            sql = """UPDATE Tickets SET first_name='{}', last_name='{}', selected_numbers='{}' WHERE id={}"""
            cursor.execute(sql.format(self.first_name, self.last_name, self.selected_numbers, self.__id))
            cnx.commit()
            return True

    @staticmethod#potrzebna do weryfikacji użytkowników
    def load_ticket_by_name(cursor, first_name, last_name):
        sql = 'SELECT id, first_name, last_name, selected_numbers FROM Tickets WHERE first_name="{}", last_name="{}"'
        cursor.execute(sql.format(first_name, last_name))
        data = cursor.fetchone()
        if data is not None:
            loaded_ticket = Ticket()
            loaded_ticket.__id = row[0]
            loaded_ticket.first_name = row[1]
            loaded_ticket.last_name = row[2]
            loaded_ticket.selected_numbers = row[3]
            return loaded_ticket
        else:
            return None

    @staticmethod#potrzebna do sprawdzenia kto wygrał - metofa chyba lepsz
    def load_ticket_by_number(cursor, selected_numbers):
        sql = 'SELECT id, first_name, last_name, selected_numbers FROM Tickets WHERE selected_numbers="{}"'
        ret = []
        cursor.execute(sql.format(selected_numbers))
        result = cursor.fetchall()
        for row in result:
            loaded_ticket = Ticket()
            loaded_ticket.__id = row[0]
            loaded_ticket.first_name = row[1]
            loaded_ticket.last_name = row[2]
            loaded_ticket.selected_numbers = row[3]
            ret.append(loaded_ticket)
            return ret
        else:
            return None

    @staticmethod#potrzebna do sprawdzenia kto wygrał
    def load_all_tickets(cursor):
        sql = 'SELECT id, first_name, last_name, selected_numbers FROM Tickets'
        ret = []
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            loaded_ticket = Ticket()
            loaded_ticket.__id = row[0]
            loaded_ticket.first_name = row[1]
            loaded_ticket.last_name = row[2]
            loaded_ticket.selected_numbers = row[3]
            ret.append(loaded_ticket)
        return ret


def new_ticket():

    person_1 = Ticket()
    person_1.first_name = input("Imię: ")
    person_1.last_name = input("Nazwisko: ")
    numbers_quantity = int(input("Ile liczb będziesz zgadywać: "))
    selected_numbers = []
    for number in range(1, numbers_quantity+1):
        selected_number = int(input("Podaj " + str(number) + " cyfrę: "))
        selected_numbers.append(selected_number)
    selected_numbers_to_db = str(selected_numbers)
    person_1.selected_numbers = selected_numbers_to_db
    person_1.save_to_db(cursor)
    print("Kupon został dodany")


# new_ticket()
cnx.close()