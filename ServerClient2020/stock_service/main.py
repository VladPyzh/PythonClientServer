import json
import requests
import sys
from time import sleep

sys.path.append('../')
from lib.utility import main_parser, test, epic_exit, simple_exit, order_reader

address = ""


def change_store():
    changes = dict()
    print("    Okay! Enter vendor code and amount (xxxx <amount>) \n As always exit to exit")
    while True:
        goods = order_reader()
        if goods == "exit":
            break
        if goods == "continue":
            continue
        changes[goods[0]] = goods[1]
        print("    Now it looks so: \n {} \n Exit if ready".format(changes))
    if changes:
        requests.post(address + "/change_store", params=changes).text


def change_status():
    while True:
        print("    Type ID and +-value or exit")
        id_changes = input()
        if id_changes == "exit":
            return
        else:
            try:
                id_changes = id_changes.split()
                changes = {"id": id_changes[0], "value": id_changes[1]}
                requests.post(address + "/change_status", params=changes).text
            except IndexError:
                print("Bad input. Try again")
                continue
            except AttributeError:
                print("Done!")
                return


def mail():
    print("    Type ID or exit")
    while True:
        id = input()
        if id == "exit":
            return
        print(requests.post(address + "/mail", params=dict(id=id)).text)
        return


def main():
    global address
    address = main_parser()
    try:
        if test() == "works":
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
        print("    change store -- add or delete goods \n"
              "    change status -- change order status \n"
              "    mail -- write polite letter about the loss of goods \n"
              "    exit")
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
