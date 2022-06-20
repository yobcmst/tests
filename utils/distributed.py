import os


def is_rank_zero():
    return get_rank() == 0


def print_once(s):
    if is_rank_zero():
        print(s)


def get_rank():
    return int(os.environ.get('LOCAL_RANK', 0))