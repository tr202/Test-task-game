from pprint import pp, pprint
import random
import math


TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()


def get_score(game_stamps, offset):
    # max_offset_condition = game_stamps[len(game_stamps)-1].get("offset")
    max_offset_condition = game_stamps[TIMESTAMPS_COUNT-1]["offset"]
    if offset > max_offset_condition or offset < 0:
        raise IndexError('Out of range')
    k_offset = max_offset_condition / TIMESTAMPS_COUNT  # slope coefficient of a polyline section 

    def get_next_index(game_stamps, offset, k_offset):
        list_index = int(offset / k_offset)
        next_offset = game_stamps[list_index].get("offset")
        delta_offset = offset - next_offset
        delta_sign = -1 if delta_offset < 0 else 1
        if abs(delta_offset) <= OFFSET_MAX_STEP:
            for i in range(list_index, list_index + delta_offset + delta_sign,
                           delta_sign):
                current_offset = game_stamps[i].get('offset')
                if current_offset == offset or (current_offset < offset
                   and game_stamps[i+1].get('offset') > offset):
                    return i
        k_offset = next_offset / list_index
        # print(next_offset, ' ', )  # show recursive iteration
        return get_next_index(game_stamps, offset, k_offset)

    index = get_next_index(game_stamps, offset, k_offset)
    # offset_contain_scores = True if game_stamps[index]["offset"] == offset else False
    return (
        # offset_contain_scores,
        game_stamps[index]["score"]["home"],
        game_stamps[index]["score"]["away"]
        )
    #
    '''
        Takes list of game's stamps and time offset for which returns the scores for the home and away teams.
        Please pay attention to that for some offsets the game_stamps list may not contain scores.
    '''
    # return home, away


print('get_score', get_score(game_stamps, 100000))
