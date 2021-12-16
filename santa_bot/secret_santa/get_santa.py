import random


def get_santas(id_users):
    pars = {}
    random.shuffle(id_users)
    for index in range(len(id_users) - 1):
        pars[id_users[index]] = id_users[index + 1]

    pars[id_users[-1]] = id_users[0]
    return pars
