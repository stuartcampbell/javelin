from time import sleep
from tqdm import tqdm
for i in tqdm(range(1000)):
    sleep(0.01)


try:
    from tqdm import tqdm as tqdm_wrapper
except ImportError:
    def tqdm_wrapper(value):
        return value
