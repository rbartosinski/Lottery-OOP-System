from models.lottery_engine import new_lottery, compare_winners
from models.ticket import new_ticket, change_numbers, Ticket, table_of_winners
from models.dbconnection import DBconnection


db = DBconnection(user='root', password='coderslab', database='LotteryDB')
cnx = db.cnx
cursor = db.cursor


def run_app():
    print("""
    Witaj w systemie losowania!
    Co chcesz zrobić?
    1 - Dodaj nowego gracza
    2 - Zmień liczby gracza
    3 - Losuj / nowa gra
    4 - Tabela zwycięzców
    5 - Zamknij program
    """)
    while True:
        choice = input()
        if choice == "1":
            new_ticket()
        elif choice == "2":
            change_numbers()
        elif choice == "3":
            comp_w = compare_winners()
            result = new_lottery(comp_w)
            if result:
                winner = Ticket.load_ticket_by_id(cursor, result)
                print("Zwycięzcą jest: ", winner.first_name, winner.last_name)
        elif choice == "4":
            table_of_winners()
        elif choice == "5":
            break
        else:
            print("Co dalej? Wprowadź poprawną operację.")


run_app()