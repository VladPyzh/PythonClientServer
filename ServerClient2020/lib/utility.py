import argparse
import requests
from time import sleep


def order_reader():
    goods = input()
    if goods == "exit":
        return "exit"
    try:
        goods = goods.split()
        goods[1] = int(goods[1])
    except IndexError:
        print("Bad input. Try again")
        return "continue"
    if len(goods) != 2 or type(goods[1]) is not int or goods[1] < 1:
        print("\tsomething is wrong, try again")
        return "continue"
    return goods


def simple_exit():
    print("Goodbye!")
    exit()


def epic_exit():
    print("...(some computer sounds) bad connection.")
    sleep(1)
    print("Launch the program of self-destruction")
    for i in range(4):
        print(3 - i)
        sleep(1)
    print("Take me home, country roads")
    exit()


def test(server_address):
    return requests.get(server_address + "/test").text


def main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="8000", type=int)
    args = parser.parse_args()
    server_address = ("http://" + args.host + ":" + str(args.port) + "/")
    return server_address
