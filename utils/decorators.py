def singleton(cls):
    """
    A decorator function that ensures a class has only one instance and provides a global point of access to it.
    """

    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
