from datetime import datetime
from random import randint
from models.ticket import Ticket
from models.dbconnection import DBconnection
import json


db = DBconnection(user='root', password='coderslab', database='LotteryDB')
cnx = db.cnx
cursor = db.cursor


class Lottery():
    __id = None
    lottery_numbers = None
    date_of_selection = None
    ticket_id = None
    points_of_user = None

    def __init__(self):
        self.__id = -1
        self.lottery_numbers = ""
        self.date_of_selection = ""
        self.ticket_id = ""
        self.points_of_user = ""

    @property
    def id(self):
        return self.__id

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO Lotteries(lottery_numbers, date_of_selection, ticket_id, points_of_user) VALUES ('{}', '{}', '{}', '{}')"""
            cursor.execute(sql.format(self.lottery_numbers, self.date_of_selection, self.ticket_id, self.points_of_user))
            cnx.commit()
            self.__id = cursor.lastrowid
            return True


def lottery_engine(numbers_quantity, numbers_range_min, numbers_range_max):
    won_numbs = []
    for i in range(0, numbers_quantity):
        numb = randint(numbers_range_min, numbers_range_max)
        if numb in won_numbs:
            while not numb not in won_numbs:
                numb = randint(numbers_range_min, numbers_range_max)
        won_numbs.append(numb)
    sorted_won_numbs = sorted(won_numbs)
    print("Zakończone losowanie. Zwycięskie cyfry: ", sorted_won_numbs)
    return sorted_won_numbs


def compare_winners():
    with open('models/zadanie.json') as js:
        data = json.load(js)

    numbers_quantity = data["numbers-quantity"]
    numbers_range = data["numbers-range"]
    numbers_range_min = numbers_range["min"]
    numbers_range_max = numbers_range["max"]

    global lottery_results
    lottery_results = lottery_engine(numbers_quantity, numbers_range_min, numbers_range_max)

    ticket = Ticket()
    all_tickets = ticket.load_all_tickets(cursor)
    winners = []
    winners_list = []
    ticket_list = []

    for ticket in all_tickets:
        tickets_from_db = ticket.selected_numbers[1:-1].split(", ")
        tickets_to_load = (list(tickets_from_db))
        player_dict = {}
        for numb in tickets_to_load:
            if int(numb) in lottery_results:
                winners.append(ticket)
                player_dict[ticket.id] = 1
                dict_to_add = player_dict
                if dict_to_add in ticket_list:
                    ticket_list.remove(dict_to_add)
                    player_dict[ticket.id] += 1
                    dict_to_change = player_dict
                    ticket_list.append(dict_to_change)
                else:
                    ticket_list.append(dict_to_add)
        if winners is not None:
            for person in winners:
                if person.id not in winners_list:
                    winners_list.append(person.id)

        return ticket_list


def new_lottery(ticket_list):
    if ticket_list == []:
        return print("Nie było zwycięzców")
    else:
        for ticket in ticket_list:
            lottery_1 = Lottery()
            lottery_1.lottery_numbers = str(lottery_results)
            lottery_1.date_of_selection = datetime.today()
            all_keys = ticket.keys()
            for key in all_keys:
                lottery_1.ticket_id = key
                lottery_1.points_of_user = ticket[key]
            lottery_1.save_to_db(cursor)
        return lottery_1.ticket_id