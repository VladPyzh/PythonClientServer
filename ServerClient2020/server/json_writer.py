import json


def writter():
    file = open("storage.txt", "w")
    storage = {"car": 1,
               "byke": 100,
               "engine": 0,
               "toilet_paper": -1
               }
    file.write(json.dumps(storage))
    file.close()

    file = open("statuses.txt", "w")
    statuses = {"id0": 2,
                "id1": 1,
                "id2": 1,
                "id3": 1,
                "Test": 0
                }
    file.write(json.dumps(statuses))
    file.close()

    file = open("mail.txt", "w")
    mail = {
        "123": "Sorry, we lost your order. \u00af\\_(\u30c4)_/\u00af",
        "id0": "Sorry, we lost your order. \u00af\\_(\u30c4)_/\u00af"
    }
    file.write(json.dumps(mail))
    file.close()

    file = open("orders-list.txt", "w")
    orders = {
        "id0": {"byke": "1"},
        "id1": {"byke": "1"},
        "id2": {"byke": "1"},
        "id3": {"byke": "1"}
    }
    file.write(json.dumps(orders))
    file.close()

