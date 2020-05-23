import requests
import sys
from config import Config_strings


sys.path.append('../')
from handlers import Handlers
from lib.utility import main_parser, test, epic_exit, simple_exit, order_reader


server_address = ""


def change_store():
    changes = {}
    print(Config_strings.change_store_greetings)
    while True:
        goods = order_reader()
        if goods == Config_strings.exit:
            break
        if goods == Config_strings.cont:
            continue
        changes[goods[0]] = goods[1]
        print(Config_strings.order_looks.format(changes))
    if changes:
        requests.post(server_address + Handlers.change_store, params=changes).text


def change_status():
    while True:
        print(Config_strings.change_status_greetings)
        id_changes = input()
        if id_changes == Config_strings.exit:
            return
        else:
            try:
                id_changes = id_changes.split()
                changes = {Config_strings.id: id_changes[0], Config_strings.value: id_changes[1]}
                requests.post(server_address + Handlers.change_status, params=changes).text
            except IndexError:
                print(Config_strings.bad_input)
                continue
            print(Config_strings.done)
            return


def mail():
    print(Config_strings.mail_greetings)
    while True:
        item_id = input()
        if item_id == Config_strings.exit:
            return
        print(requests.post(server_address + Handlers.mail, params=dict(id=item_id)).text)
        return


def main():
    global server_address
    server_address = main_parser()
    print(server_address)
    try:
        print(test(server_address))
        if test(server_address) == Config_strings.test:
            print(Config_strings.connected)
        else:
            print(Config_strings.connected_to_the_wrong_service)
            exit()
    except:
        epic_exit()
    print(Config_strings.ask_politely)
    while True:
        print(Config_strings.main_greetings)
        try:
            cmd = input(Config_strings.command)
            if cmd == Config_strings.change_store:
                change_store()
            elif cmd == Config_strings.change_status:
                change_status()
            elif cmd == Config_strings.mail:
                mail()
            elif cmd == Config_strings.exit:
                simple_exit()
        except KeyboardInterrupt:
            epic_exit()


if __name__ == "__main__":
    main()
