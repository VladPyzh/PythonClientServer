import flask
import json

app = flask.Flask("buy_and_deliver")
status_dict = {1: "In stock", 2: "On road", 3: "It's ready!"}


def change_status(id, changes=1):
    try:
        changes = int(changes)
    except ValueError:
        return False
    try:
        f = open("statuses.txt", "r")
        statuses = json.loads(f.read())
        f.close()
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        statuses = dict()

    f = open("statuses.txt", "w")

    try:
        statuses[id] += changes
    except KeyError:
        statuses[id] = changes

    f.write(json.dumps(statuses))
    f.close()

    return True


def storage_reader():
    with open("storage.txt", "r") as f:
        storage = json.loads(f.read())
        f.close()
        return storage
    return {}


def read_mails(id):
    try:
        f = open("mail.txt", "r")
        mails = json.loads(f.read())
        f.close()
        try:
            ans = mails[id]
            f = open("mail.txt", "w")
            del mails[id]
            f.write(json.dumps(mails))
            f.close()
            return ans
        except (IndexError, KeyError):
            return "nothing"
    except (json.decoder.JSONDecodeError, FileNotFoundError, IndexError):
        return "nothing"


@app.route("/test", methods=["GET"])
def test():
    return "works"


@app.route("/check", methods=["GET"])
def check():
    storage = storage_reader()
    vender_code = str(flask.request.args["id"])
    try:
        return str(storage[vender_code])
    except KeyError:
        return "-401"


@app.route("/ask_store", methods=["GET"])
def ask_store():
    storage = storage_reader()
    return str(storage)


@app.route("/create_order", methods=["POST"])
def create_order():
    order = {
        item: flask.request.args[item]
        for item in flask.request.args
    }
    storage = storage_reader()
    for i in order:
        if storage[i] < int(order[i]):
            return "-402"
        storage[i] -= int(order[i])

    f = open("storage.txt", "w")
    f.write(json.dumps(storage))
    f.close()

    try:
        f = open("orders-list.txt", "r")
        orders_list = json.loads(f.read())
        order_id = "id" + str(len(orders_list))
        f.close()
    except TypeError:
        orders_list = dict()
        order_id = "id0"

    orders_list[order_id] = order
    f = open("orders-list.txt", "w")
    f.write(json.dumps(orders_list))

    change_status(order_id)
    return order_id


@app.route("/get_status", methods=["GET"])
def get_status():
    id = str(flask.request.args["id"])
    mail = read_mails(id)
    if mail != "nothing":
        return mail
    f = open("statuses.txt", "r")
    try:
        statuses = json.loads(f.read())
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return "We don't have orders with that id. :( \n"
    try:
        status = statuses[id]
        try:
            return status_dict[status]
        except KeyError:
            return "There is something wrong with your order \n" \
                   "Calls us!"
    except KeyError:
        return "We don't have orders with that id. :("


###stock service part###


@app.route("/change_store", methods=["POST"])
def change_store():
    changes = {
        item: flask.request.args[item]
        for item in flask.request.args
    }
    storage = storage_reader()
    for i in changes:
        try:
            storage[i] += int(changes[i])
        except KeyError:
            storage[i] = int(changes[i])

    f = open("storage.txt", "w")
    f.write(json.dumps(storage))
    f.close()
    return "changed!"


@app.route("/change_status", methods=["POST"])
def adm_change_status():
    id = flask.request.args["id"]
    value = flask.request.args["value"]
    value = int(value)
    if change_status(id, value):
        return "changed!"
    else:
        return ""


@app.route("/mail", methods=["POST"])
def add_mail():
    id = str(flask.request.args["id"])
    try:
        f = open("mail.txt", "r")
        mails = json.loads(f.read())
        f.close()
    except (json.decoder.JSONDecodeError, FileNotFoundError, TypeError):
        mails = dict()

    mails[id] = "Sorry, we lost your order. ¯\_(ツ)_/¯"
    f = open("mail.txt", "w")
    f.write(json.dumps(mails))
    f.close()
    return "The letter was sent"


def main():
    app.run("::", port=8888, debug=True)


if __name__ == "__main__":
    main()

# Mystakes code:
#
# -401 Asking for bad vender code
# -402 Trying to buy more than possible
#
