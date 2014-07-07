# coding=utf-8
import os, re

def compact(path):
    """Compact .cnf MySQL config, so that file can be line-by-line compared to another similar config."""

    def clean(line):
        line = line.replace('\n', '')
        line = line.replace('\t', ' ')
        line = re.sub(' +', ' ', line)
        comment = line.find('#')
        if comment >= 0:
            line = line[:line.find('#')]
        if line and line[0] == '[':
            return ''
        return line

    with open(os.path.join(path, 'my.cnf'), 'r') as f:
        lines = [clean(line) for line in f.readlines() if clean(line)]
        lines = sorted(set(lines))

    with open(os.path.join(path, 'my_dd.cnf'), 'w') as f:
        f.writelines('\n'.join(lines))
