import pandas as pd
import chardet    
import numpy as np

def ipc_count(ipc_value):
    if pd.isnull(ipc_value) or ipc_value == '-':
        return 0
    else:
        return len(ipc_value.split(' | '))
