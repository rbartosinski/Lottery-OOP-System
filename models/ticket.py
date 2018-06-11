from models.dbconnection import DBconnection


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
            cnx.commit()
            self.__id = cursor.lastrowid
            return True
        else:
            sql = """UPDATE Tickets SET first_name='{}', last_name='{}', selected_numbers='{}' WHERE id={}"""
            cursor.execute(sql.format(self.first_name, self.last_name, self.selected_numbers, self.__id))
            cnx.commit()
            return True

    @staticmethod
    def load_ticket_by_name(cursor, first_name, last_name):
        sql = 'SELECT id, first_name, last_name, selected_numbers FROM Tickets WHERE first_name="{}" and last_name="{}"'
        cursor.execute(sql.format(first_name, last_name))
        data = cursor.fetchone()
        if data is not None:
            loaded_ticket = Ticket()
            loaded_ticket.__id = data[0]
            loaded_ticket.first_name = data[1]
            loaded_ticket.last_name = data[2]
            loaded_ticket.selected_numbers = data[3]
            return loaded_ticket
        else:
            return None

    @staticmethod
    def load_ticket_by_id(cursor, id):
        sql = 'SELECT id, first_name, last_name, selected_numbers FROM Tickets WHERE id="{}"'
        ret = []
        cursor.execute(sql.format(id))
        data = cursor.fetchone()
        if data is not None:
            loaded_ticket = Ticket()
            loaded_ticket.__id = data[0]
            loaded_ticket.first_name = data[1]
            loaded_ticket.last_name = data[2]
            loaded_ticket.selected_numbers = data[3]
            return loaded_ticket
        else:
            return None

    @staticmethod
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

    @staticmethod
    def load_table_of_winners(cursor):
        sql = """SELECT first_name, last_name, lottery_numbers, date_of_selection, points_of_user FROM Tickets JOIN Lotteries ON Tickets.id=Lotteries.ticket_id;"""
        cursor.execute(sql)
        results = []
        for record in cursor:
            results.append(record)
        return results


def new_ticket():
    person_1 = Ticket()
    person_1.first_name = input("Imię: ")
    person_1.last_name = input("Nazwisko: ")
    while True:
        try:
            numbers_quantity = int(input("Ile liczb będziesz zgadywać: "))
        except ValueError:
            print("Wpisz poprawną liczbę.")
        else:
            break
    selected_numbers = []
    for number in range(1, numbers_quantity+1):
        selected_number = int(input("Podaj " + str(number) + " cyfrę: "))
        selected_numbers.append(selected_number)
    selected_numbers_to_db = str(selected_numbers)
    person_1.selected_numbers = selected_numbers_to_db
    person_1.save_to_db(cursor)
    print("Kupon został dodany")


def change_numbers():
    first_name = input("Imię: ")
    last_name = input("Nazwisko: ")
    person_1 = Ticket.load_ticket_by_name(cursor, first_name, last_name)
    print("Liczby wybrane wcześniej: ", person_1.selected_numbers)
    while True:
        try:
            numbers_quantity = int(input("Ile liczb będziesz zgadywać: "))
        except ValueError:
            print("Wpisz poprawną liczbę.")
        else:
            break
    selected_numbers = []
    for number in range(1, numbers_quantity + 1):
        selected_number = int(input("Podaj " + str(number) + " cyfrę: "))
        selected_numbers.append(selected_number)
    selected_numbers_to_db = str(selected_numbers)
    person_1.selected_numbers = selected_numbers_to_db
    person_1.save_to_db(cursor)
    print("Kupon został zmieniony")


def table_of_winners():
    table = Ticket.load_table_of_winners(cursor)
    for record in table:
        print("Imię i nazwisko: ", record[0], record[1])
        print("Trafione losowania: ", record[2], record[3], "Liczba punktów: ", record[4])