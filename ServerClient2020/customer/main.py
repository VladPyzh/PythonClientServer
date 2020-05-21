import requests
import sys


sys.path.append('../')
from lib.utility import main_parser, test, simple_exit, order_reader


server_address = ""


def check_how_much_we_have(item_id):
    return requests.get(server_address + "/check", params=dict(id=item_id)).text


def ask_store():
    store = requests.get(server_address + "/ask_store").text
    print("\tToday we have:")
    dont_have = []
    list_to_buy = []
    store = eval(store)
    for i in store:
        if store[i] > 0:
            print("\t", i, store[i])
        elif store[i] == 0:
            list_to_buy.append(i)
        else:
            dont_have.append(i)
    print("\tProbably we will have these soon:")
    for i in list_to_buy:
        print("\t", i)
    print("\tSorry, we are out of these:")
    for i in dont_have:
        print("\t", i)


def create_order():
    order = {}
    print("\tI need vendor code and amount (xxxx <amount>) \n\tType exit if you're ready")
    while True:
        goods = order_reader()
        if goods == "exit":
            break
        if goods == "continue":
            continue
        if int(check_how_much_we_have(str(goods[0]))) < goods[1]:
            print("\tWe don't have so much or we don't have that at all! Try again or print exit")
            continue
        order[goods[0]] = goods[1]
        print("\tNow your order looks so: \n {} \n\tType exit if you're ready".format(order))
    if order:
        order_id = requests.post(server_address + "/create_order", params=order).text
        if order_id == "too_much_items":
            print("Somehow you decided to buy more than possible :(")
        else:
            print("\tYour order ID is {}".format(order_id))
        return


def get_status():
    print("\tType ID or exit")
    item_id = input()
    if item_id == "exit":
        return
    else:
        ans = requests.get(server_address + "/get_status", params=dict(id=item_id)).text
        print(ans)
        return ans


def main():
    global server_address
    server_address = main_parser()
    try:
        if test() == "works":
            print("We are online! \n")
        else:
            print("Something is wrong with connection \n")
            return
    except:
        print("Connection gone wrong")
        return
    while True:
        print("Type one of these commads: \n"
              "status -- take status of your order \n"
              "create -- create new order \n"
              "store -- ask for what we have in our store \n"
              "exit -- exit")
        try:
            cmd = input("Enter command>")
            if cmd == "status":
                get_status()
            elif cmd == "create":
                create_order()
            elif cmd == "store":
                ask_store()
            elif cmd == "exit":
                simple_exit()
            else:
                print("Input is incorrect, go again")
        except (KeyboardInterrupt, EOFError):
            simple_exit()


if __name__ == "__main__":
    main()
