import json


def writter():
    f = open("storage.txt", "w")
    storage = {"car": 1,
               "byke": 100,
               "engine": 0,
               "toilet_paper": -1
               }
    f.write(json.dumps(storage))
    f.close()

    f = open("statuses.txt", "w")
    statuses = {"id0": 2,
                "id1": 1,
                "id2": 1,
                "id3": 1,
                "Test": 0
                }
    f.write(json.dumps(statuses))
    f.close()

    f = open("mail.txt", "w")
    mail = {
        "123": "Sorry, we lost your order. \u00af\\_(\u30c4)_/\u00af",
        "id0": "Sorry, we lost your order. \u00af\\_(\u30c4)_/\u00af"
    }
    f.write(json.dumps(mail))
    f.close()

    f = open("orders-list.txt", "w")
    orders = {
        "id0": {"byke": "1"},
        "id1": {"byke": "1"},
        "id2": {"byke": "1"},
        "id3": {"byke": "1"}
    }
    f.write(json.dumps(orders))
    f.close()

