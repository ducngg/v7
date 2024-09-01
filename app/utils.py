import argparse

def str_to_bool(value: str) -> bool:
    if value.lower() in ('true', 'yes', 'y', '1'):
        return True
    elif value.lower() in ('false', 'no', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
