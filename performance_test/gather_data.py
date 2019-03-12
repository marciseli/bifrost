import sys
import os
sys.path.append("/Users/timo/Documents/repos/bc-interop")

from api import store
import string
import random
from blockchain import Blockchain
import csv
import numpy as np
from numpy import genfromtxt


def check_sample_size(blockchain_name):
	my_data = genfromtxt(
		f"/Users/timo/Documents/repos/bc-interop/performance_test/data/{blockchain_name.name}.csv", delimiter=',')
	print(f"Sample size is now: {my_data.size}")

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

def run_test(blockchain_name):
	i = 0
	while i < 25:
		print(f"Number {i} : {store(generate_random_string(10), blockchain_name)}")
		i += 1

# run_test(Blockchain.IOTA)
check_sample_size(Blockchain.IOTA)
