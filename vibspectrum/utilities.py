import numpy as np
import pandas as pd

def load_txt_file(path):
    sig = np.loadtxt(path)
    return sig
