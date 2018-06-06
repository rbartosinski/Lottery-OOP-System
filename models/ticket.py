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


new_ticket()
cnx.close()
