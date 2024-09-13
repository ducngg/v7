import time
from typing import Callable, TypeVar

R = TypeVar('R')

UTILS_START_TIME = time.time()

def set_time():
    global UTILS_START_TIME
    UTILS_START_TIME = time.time()
    
def finish_log(task_name: str):
    global UTILS_START_TIME
    print(f"\tFinished `{task_name}` in {time.time() - UTILS_START_TIME:.5f} seconds")

def exec(task_name: str, func: Callable[..., R], *args, verbose: int = 1, **kwargs) -> R:
    """
    Use this function to log the executing time of `func`.
    """
    set_time()
    result = func(*args, **kwargs)
    
    if verbose > 0:
        finish_log(task_name)
        
    return result

