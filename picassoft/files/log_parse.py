# coding=utf-8
import sys
import re
import decimal
from collections import namedtuple, Counter
from picassoft.utils.iso8601 import parse_datetime


DEF_PATTERN =\
    r'([\d\-:+T]+) \| ([\d]+) \| ([\d]+) b \| ([\d\.]+) s \| "([\w\.]*)" "(\w*) ([^"]*)" \[([\d.]*)\] "([^"]*)" "([^"]*)"'
LogEntry = namedtuple('Request', 'datetime status bytes seconds host command url address referer agent')


def parse(file_name, regexp, parser):
    with open(file_name, 'r') as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                items = match.groups()
                yield parser(*items)


def nginx_parser(timestamp, status, bytes_sent, seconds, host, command, url, address, referer, agent):
    return LogEntry(parse_datetime(timestamp),
                    int(status), int(bytes_sent), decimal.Decimal(seconds),
                    host, command, url, address, referer, agent)


def print_items(*args):
    for items in parse(*args):
        print items


def calc_stats(*args):
    cnt = 0
    total_time = decimal.Decimal()
    min_time = decimal.Decimal()
    max_time = decimal.Decimal()
    agents = Counter()
    hosts = Counter()
    for items in parse(*args):
        cnt += 1
        total_time += items.seconds
        min_time = min(min_time, items.seconds)
        max_time = max(max_time, items.seconds)
        agents[items.agent] += 1
        hosts[items.host] += 1
    print "Count, Total time, Min time, Avg time, Max time"
    print cnt, total_time, min_time, total_time / cnt if cnt > 0 else 0, max_time
    print "Agents: name, count"
    for i, (agent, count) in enumerate(agents.most_common(10)):
        print("{:2}) {:4} {}".format(i + 1, count, agent))
    print "Hosts: name, count"
    for i, (host, count) in enumerate(hosts.most_common(100)):
        print("{:2}) {:4} {}".format(i + 1, count, host))


def main():
    import sys
    file_name = sys.argv[1]
    regexp = re.compile(sys.argv[2] if len(sys.argv) > 2 else DEF_PATTERN)
    parser = nginx_parser
    calc_stats(file_name, regexp, parser)


if __name__ == "__main__":
    main()
    sys.stdin.read(1)
