import os
import re
import sys

from flask.ext.script import Command, Option


class ExportCommand(Command):

    LINE_PATTERN = re.compile('(\S+?)\s*?=\s*?(\S+?)$')

    def get_options(self):
        return [
            Option('-i', '--in', dest='in_path', default='./.env'),
            Option('-o', '--out', dest='out_path', default='./profile'),
        ]

    def export(self, in_path, out_path):
        out_lines = list()
        with open(in_path, 'r') as in_file:
            for line in in_file.readlines():
                matched = self.LINE_PATTERN.findall(line)
                if matched and len(matched[0]) == 2:
                    name, value = matched[0]
                    out_lines.append('export %s=%s' % (name, value))

        with open(out_path, 'w') as out_file:
            out_file.write('\n'.join(out_lines))

    def run(self, in_path, out_path):
        self.export(in_path, out_path)
        print 'Export from: %s to %s' % (in_path, out_path)
