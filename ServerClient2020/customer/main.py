import requests
import sys
import ast
from config import Config_strings


sys.path.append('../')
from handlers import Handlers
from lib.utility import main_parser, test, simple_exit, order_reader


server_address = ""


def check_how_much_we_have(item_id):
    return requests.get(server_address + Handlers.check, params=dict(id=item_id)).text


def ask_store():
    store = requests.get(server_address + Handlers.ask_store).text
    print(Config_strings.list_start)
    dont_have = []
    list_to_buy = []
    store = ast.literal_eval(store)
    for i in store:
        if store[i] > 0:
            print("\t\t", i, store[i])
        elif store[i] == 0:
            list_to_buy.append(i)
        else:
            dont_have.append(i)
    print(Config_strings.will_have, *list_to_buy, sep='\n\t\t ')
    print(Config_strings.out_of_these, *dont_have, sep='\n\t\t ')
    print("\n")


def create_order():
    order = {}
    print(Config_strings.create_order_greetings)
    while True:
        goods = order_reader()
        if goods == Config_strings.exit:
            break
        if goods == Config_strings.cont:
            continue
        if int(check_how_much_we_have(str(goods[0]))) < goods[1]:
            print(Config_strings.dont_have)
            continue
        order[goods[0]] = goods[1]
        print(Config_strings.order_looks.format(order))
    if order:
        order_id = requests.post(server_address + Handlers.create_order, params=order).text
        if order_id == Config_strings.too_much:
            print(Config_strings.more_than_possible)
        else:
            print(Config_strings.order_id.format(order_id))
        return


def get_status():
    print(Config_strings.get_status_greetings)
    item_id = input()
    if item_id == Config_strings.exit:
        return
    else:
        ans = requests.get(server_address + Handlers.get_status, params=dict(id=item_id)).text
        print(ans)
        return ans


def main():
    global server_address
    server_address = main_parser()
    try:
        if test(server_address) == Config_strings.works:
            print(Config_strings.online)
        else:
            print(Config_strings.smth_wrong)
            return
    except:
        print(Config_strings.bad_connection)
        return
    while True:
        print(Config_strings.main_greetings)
        try:
            cmd = input(Config_strings.command)
            if cmd == Config_strings.status:
                get_status()
            elif cmd == Config_strings.create:
                create_order()
            elif cmd == Config_strings.store:
                ask_store()
            elif cmd == Config_strings.exit:
                simple_exit()
            else:
                print(Config_strings.bad_input)
        except (KeyboardInterrupt, EOFError):
            simple_exit()


if __name__ == "__main__":
    main()
