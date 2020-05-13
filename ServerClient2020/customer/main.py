import requests
import sys

sys.path.append('../')
from lib.utility import main_parser, test, simple_exit, order_reader

address = ""


def check_how_much_we_have(id):
    return requests.get(address + "/check", params=dict(id=id)).text


def ask_store():
    store = requests.get(address + "/ask_store").text
    print("     Today we have:")
    dont_have = list()
    list_to_buy = list()
    store = eval(store)
    for i in store:
        if store[i] > 0:
            print("     ", i, store[i])
        elif store[i] == 0:
            list_to_buy.append(i)
        else:
            dont_have.append(i)
    print("     Probaly we will have these soon:")
    for i in list_to_buy:
        print("     ", i)
    print("     Sorry, we are out of these:")
    for i in dont_have:
        print("     ", i)


def create_order():
    order = dict()
    print("     I need vendor code and amount (xxxx <amount>) \n     Type exit if you're ready")
    while True:
        goods = order_reader()
        if goods == "exit":
            break
        if goods == "continue":
            continue
        if int(check_how_much_we_have(str(goods[0]))) < goods[1]:
            print("     We don't have so much or we don't have that at all! Try again or print exit")
            continue
        order[goods[0]] = goods[1]
        print("     Now your order looks so: \n {} \n   Type exit if you're ready".format(order))
    if order:
        order_id = requests.post(address + "/create_order", params=order).text
        try:
            if int(order_id) == -402:
                print("Somehow you decided to buy more than possible :(")
            return
        except ValueError:
            print("     Your order ID is {}".format(order_id))
            return


def get_status():
    print("    Type ID or exit")
    id = input()
    if id == "exit":
        return
    else:
        ans = requests.get(address + "/get_status", params=dict(id=id)).text
        print(ans)
        return ans


def main():
    global address
    address = main_parser()
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
