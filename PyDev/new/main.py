import numpy as np
import pandas as pd
import os
from datetime import date as dt

import seaborn as sns

import matplotlib.pyplot as plt

import string
import hashlib

import csv
import codecs

from WarekiClass import WarekiClass
from ReceiptyClass import ReceiptyClass

def main():

    receptyCls = ReceiptyClass()

    #df_recepty = receptyCls.readReceipty()

    receptyCls.receiptyFlatten()

if __name__ == "__main__":

    main()
