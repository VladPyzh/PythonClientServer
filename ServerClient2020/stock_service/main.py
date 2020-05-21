import requests
import sys
from time import sleep


sys.path.append('../')
from lib.utility import main_parser, test, epic_exit, simple_exit, order_reader


server_address = ""


def change_store():
    changes = {}
    print("\tOkay! Enter vendor code and amount (xxxx <amount>) \n As always exit to exit")
    while True:
        goods = order_reader()
        if goods == "exit":
            break
        if goods == "continue":
            continue
        changes[goods[0]] = goods[1]
        print("\tNow it looks so: \n {} \n Exit if ready".format(changes))
    if changes:
        requests.post(server_address + "/change_store", params=changes).text


def change_status():
    while True:
        print("\tType ID and +-value or exit")
        id_changes = input()
        if id_changes == "exit":
            return
        else:
            try:
                id_changes = id_changes.split()
                changes = {"id": id_changes[0], "value": id_changes[1]}
                requests.post(server_address + "/change_status", params=changes).text
            except IndexError:
                print("Bad input. Try again")
                continue
            print("Done!")
            return


def mail():
    print("\tType ID or exit")
    while True:
        item_id = input()
        if item_id == "exit":
            return
        print(requests.post(server_address + "/mail", params=dict(id=item_id)).text)
        return


def main():
    global server_address
    server_address = main_parser()
    print(server_address)
    try:
        print(test(server_address))
        if test(server_address) == "works":
            print("Bep-bop...")
            sleep(2)
            print("DEAR LORD WE ARE ONLINE")
        else:
            print("Kinda strange. Don't know where, but we are online")
            exit()
    except:
        epic_exit()
    print("What we gonna do today?")
    while True:
        print("\tchange store -- add or delete goods \n"
              "\tchange status -- change order status \n"
              "\tmail -- write polite letter about the loss of goods \n"
              "\texit")
        try:
            cmd = input("Enter command>")
            if cmd == "change store":
                change_store()
            elif cmd == "change status":
                change_status()
            elif cmd == "mail":
                mail()
            elif cmd == "exit":
                simple_exit()
        except KeyboardInterrupt:
            epic_exit()


if __name__ == "__main__":
    main()
