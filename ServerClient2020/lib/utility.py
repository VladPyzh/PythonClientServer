import argparse
import requests
import sys
from time import sleep
from lib.config import Config_strings


sys.path.append('../')
from handlers import Handlers


def order_reader():
    goods = input()
    if goods == Config_strings.exit:
        return Config_strings.exit
    try:
        goods = goods.split()
        goods[1] = int(goods[1])
    except IndexError:
        print(Config_strings.bad_input)
        return Config_strings.cont
    if len(goods) != 2 or type(goods[1]) is not int or goods[1] < 1:
        print(Config_strings.smth_wrong)
        return Config_strings.cont
    return goods


def simple_exit():
    print(Config_strings.goodbye)
    exit()


def epic_exit():
    print(Config_strings.bad_connection)
    sleep(1)
    print(Config_strings.launch)
    for i in range(4):
        print(3 - i)
        sleep(1)
    print(Config_strings.press_f)
    exit()


def test(server_address):
    return requests.get(server_address + Handlers.test).text


def main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    args = parser.parse_args()
    server_address = ("http://" + args.host + ":" + str(args.port) + "/")
    return server_address
