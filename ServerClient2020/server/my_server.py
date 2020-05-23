import flask
import json
import sys
from collections import defaultdict
from config import Config_strings, status_dict


sys.path.append('../')
from handlers import Handlers


app = flask.Flask(Config_strings.name)



def read_json(file_name):
    f = open(file_name, "r")
    obj = json.loads(f.read())
    f.close()
    return obj


def write_json(file_name, obj):
    f = open(file_name, "w")
    f.write(json.dumps(obj))
    f.close()


def change_status(item_id, changes=1):
    try:
        changes = int(changes)
    except ValueError:
        return False
    try:
        statuses = read_json("statuses.txt")
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        statuses = {}

    statuses = defaultdict(int, statuses)
    statuses[item_id] += changes

    write_json("statuses.txt", statuses)

    return True


def storage_reader():
    with open("storage.txt", "r") as f:
        storage = json.loads(f.read())
        f.close()
        return storage


def read_mails(order_id):
    try:
        mails = read_json("mail.txt")
        try:
            ans = mails[order_id]
            del mails[order_id]
            write_json("mail.txt", mails)
            return ans
        except (IndexError, KeyError):
            return Config_strings.nothing
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return Config_strings.nothing


@app.route(Handlers.test, methods=["GET"])
def test():
    return Config_strings.test_answer


@app.route(Handlers.check, methods=["GET"])
def check():
    storage = storage_reader()
    vender_code = str(flask.request.args["id"])
    try:
        return str(storage[vender_code])
    except KeyError:
        return "-1"


@app.route(Handlers.ask_store, methods=["GET"])
def ask_store():
    storage = storage_reader()
    return str(storage)


@app.route(Handlers.create_order, methods=["POST"])
def create_order():
    order = {
        item: flask.request.args[item]
        for item in flask.request.args
    }
    storage = storage_reader()
    for i in order:
        if storage[i] < int(order[i]):
            return Config_strings.too_much_items
        storage[i] -= int(order[i])

    write_json("storage.txt", storage)

    try:
        orders_list = read_json("orders-list.txt")
        order_id = "id" + str(len(orders_list))
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        orders_list = {}
        order_id = "id0"

    orders_list[order_id] = order
    write_json("orders-list.txt", orders_list)
    change_status(order_id)
    return order_id


@app.route(Handlers.get_status, methods=["GET"])
def get_status():
    item_id = str(flask.request.args["id"])
    mail = read_mails(item_id)
    if mail != Config_strings.nothing:
        return mail
    try:
        statuses = read_json("statuses.txt")
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return Config_strings.dont_have_order

    try:
        status = str(statuses[item_id])
        try:
            return status_dict[status]
        except KeyError:
            return Config_strings.better_call
    except KeyError:
        return Config_strings.dont_have_order


###stock service part###


@app.route(Handlers.change_store, methods=["POST"])
def change_store():
    changes = {
        item: flask.request.args[item]
        for item in flask.request.args
    }
    storage = storage_reader()
    storage = defaultdict(int, storage)
    for i in changes:
        storage[i] += int(changes[i])

    write_json("storage.txt", storage)
    return Config_strings.changed


@app.route(Handlers.change_status, methods=["POST"])
def adm_change_status():
    item_id = flask.request.args["id"]
    value = flask.request.args["value"]
    value = int(value)
    if change_status(item_id, value):
        return Config_strings.changed
    else:
        return ""


@app.route(Handlers.mail, methods=["POST"])
def add_mail():
    item_id = str(flask.request.args["id"])
    try:
        mails = read_json("mail.txt")
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        mails = {}

    mails[item_id] = Config_strings.polite_mail
    write_json("mail.txt", mails)
    return Config_strings.sent


def main():
    port = int(input())
    app.run("::", port=port, debug=True)


if __name__ == "__main__":
    main()
