#!/usr/bin/evn python
import os
import re
import sys


line_re = re.compile('(\S+?)\s*?=\s*?(\S+?)$')


def env2profile(env_path, out_path):
    out_lines = list()
    with open(env_path, 'r') as env_file:
        for line in env_file.readlines():
            matched = line_re.findall(line)
            if matched and len(matched[0]) == 2:
                name, value = matched[0]
                out_lines.append('export %s=%s' % (name, value))
    with open(out_path, 'w') as out_file:
        out_file.write('\n'.join(out_lines))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        _, env_path, out_path = sys.argv
        env2profile(env_path, out_path)
    else:
        print 'Wrong numbers of args'
