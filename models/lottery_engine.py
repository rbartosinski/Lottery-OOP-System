from random import randint
from ticket import Ticket
from dbconnection import DBconnection


db = DBconnection(user='root', password='coderslab', database='LotteryDB')
cnx = db.cnx
cursor = db.cursor


def lottery_engine():
    won_numbs = []
    for i in range(0, 5):
        numb = randint(221, 227)
        if numb in won_numbs:
            while not numb not in won_numbs:
                numb = randint(221, 227)
        won_numbs.append(numb)
    return won_numbs


lottery_results = lottery_engine()
print("Zakończone losowanie. Zwycięskie cyfry: ", lottery_results)


def compare_winners():
    pool = 10000
    ticket = Ticket()
    all_tickets = ticket.load_all_tickets(cursor)
    winners = []
    winners_list = []
    points_list = []
    keys_list = []
    for ticket in all_tickets:
        tickets_from_db = ticket.selected_numbers[1:-1].split(", ")
        tickets_to_load = (list(tickets_from_db))
        for numb in tickets_to_load:
            if int(numb) in lottery_results:
                winners.append(ticket)
        if winners is not None:
            for person in winners:
                winners_list.append(person.id)
                if person.id not in keys_list:
                    keys_list.append(person.id)
        points = {}
        for winner in winners_list:
            counted = winners_list.count(winner)
            points[person.id] = counted
            if points not in points_list:
                points_list.append(points)
    list_of_players = []
    list_of_scores = []
    for index, pointed_one in enumerate(points_list):
        player = keys_list[index]
        total_score = pointed_one[keys_list[index]]
        list_of_players.append(player)
        list_of_scores.append(total_score)
    max_value = max(list_of_scores)
    max_index = list_of_scores.index(max_value)
    st_winner = list_of_players[max_index]
    print(st_winner)
    return points_list


test = compare_winners()
print(test)


# ilość zwyciezcow
# kwota do podzielenia
# json
# zapis wynikow do bazy