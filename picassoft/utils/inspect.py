def print_vars(object):
    import pprint
    pprint.pprint(vars(object))

def interrogate(item):
    """Print useful information about item."""
    if hasattr(item, '__name__'):
        print("NAME:    ", item.__name__)
    if hasattr(item, '__class__'):
        print("CLASS:   ", item.__class__.__name__)
    print("ID:      ", id(item))
    print("TYPE:    ", type(item))
    print("VALUE:   ", repr(item))
    print("CALLABLE:", "Yes" if callable(item) else "No")
    if hasattr(item, '__doc__'):
        firstline = getattr(item, '__doc__').strip().split('\n')[0]
        print("DOC:     ", firstline)
