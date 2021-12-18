import random
from secret_santa.models import SantaGame, Participant


def get_santas(id_users):
    pars = {}
    random.shuffle(id_users)
    for index in range(len(id_users) - 1):
        pars[id_users[index]] = id_users[index + 1]

    pars[id_users[-1]] = id_users[0]
    return pars


def get_random_wishlist(tg_id):
    participant = Participant.objects.get(tg_id=tg_id)
    game = participant.game
    participants = Participant.objects.filter(game=game).exclude(tg_id=tg_id)
    random_participant = random.choice(participants)
    return random_participant.wish_list
