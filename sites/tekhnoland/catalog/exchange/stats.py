# coding=utf-8
from datetime import timedelta
from collections import defaultdict


class Stats(object):

    def __init__(self, name):
        self.name = name
        self.stats = defaultdict(int)

    def __getitem__(self, stat_name):
        return self.stats[stat_name]

    def __setitem__(self, stat_name, amount=1):
        self.stats[stat_name] = amount

    def __unicode__(self):
        stats = u", ".join(u"{} {}".format(name, value) for name, value in self.stats.iteritems())
        return u"{} {}".format(stats, self.name)

    def __repr__(self):
        return u"Load result: {}".format(self)

    def format_with_time(self, elapsed):
        loaded = self['loaded']
        speed = loaded / elapsed if elapsed > 1 else loaded
        yield u"Loaded {} {} in {} ({:.2f} {}/s)".format(loaded, self.name, timedelta(seconds=elapsed), speed, self.name)
        yield u"   {}".format(self)
