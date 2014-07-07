# coding=utf-8

def format_bracketed(val):
    val = val.strip()
    if val:
        return u" ({0})".format(val)
    else:
        return u""

def with_bracketed(val, rest):
    return val + format_bracketed(rest)

def abbrev(val):
    return u" ".join(u"{}.".format(l[0].upper()) for l in val.split())
