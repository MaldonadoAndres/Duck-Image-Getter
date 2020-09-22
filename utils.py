import numpy as np
import os
import tensorflow as tf


def getDirName(text):
    return text.split(" ")[0].title()


def get_girl_name(index: int):
    if index == 0:
        return "Irene"
    elif index == 1:
        return "Joy"
    elif index == 2:
        return "Seulgi"
    elif index == 3:
        return "Wendy"
    elif index == 4:
        return "Yeri"
    else:
        return "Not Red Velvet Member"
