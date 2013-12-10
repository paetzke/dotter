"""
dotter

Copyright (c) 2013, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
from base64 import b16encode
from subprocess import PIPE, Popen


class Dotter:

    def __init__(self, directed=True, output_to_file=True, output_filename=None,
                 output_type='pdf', program='dot', strict=False):
        self.directed = directed

        self.args = [program]
        self.args.append('-T%s' % output_type)
        if output_to_file:
            if output_filename:
                self.args.append('-o')
                self.args.append(output_filename)
            else:
                self.args.append('-O')

        self.commands = []
        if strict:
            self.execute(' strict ')
        if self.directed:
            self.execute('digraph')
        else:
            self.execute('graph')
        self.execute(' {')

    def execute(self, command):
        self.commands.append(command)

    def close(self):
        self.execute('}')
        p = Popen(self.args, stdout=PIPE, stdin=PIPE)
        commands = '\n'.join(self.commands)
        commands = commands.encode(encoding='utf-8')
        out, _unused_err = p.communicate(commands)
        out = out.decode(encoding='utf-8')
        return out

    @staticmethod
    def escape(s):
        s = b16encode(bytes(s, encoding='utf-8')).decode(encoding='utf-8')
        for i in range(10):
            s = s.replace(chr(ord('0') + i), chr(ord('a') + i))
        return s

    def add_edge(self, node1, node2, label=None):
        if self.directed:
            fmt = '{0} -> {1}'
        else:
            fmt = '{0} -- {1}'
        if label:
            fmt += ' [label="{0}"]'.format(label)
        self.execute(fmt.format(Dotter.escape(node1), Dotter.escape(node2)))

    def add_node(self, node, font=None, fontsize=None, label=None, shape=None, url=None):
        self.execute('{0}'.format(Dotter.escape(node)))
        self.set_label(node, label if label else node)
        self.node_attributes(node, font, fontsize, shape, url)

    def node_attributes(self, node, font=None, fontsize=None, shape=None, url=None):
        if font:
            cmd = '{0} [fontname="{1}"]'.format(Dotter.escape(node), font)
            self.execute(cmd)
        if fontsize:
            cmd = '{0} [fontsize="{1}"]'.format(Dotter.escape(node), fontsize)
            self.execute(cmd)
        if shape:
            cmd = '{0} [shape="{1}"]'.format(Dotter.escape(node), shape)
            self.execute(cmd)
        if url:
            cmd = '{0} [URL="{1}"]'.format(Dotter.escape(node), url)
            self.execute(cmd)

    def set_label(self, node, label):
        self.execute('{0} [label="{1}"]'.format(Dotter.escape(node), label))

    def nodes_attributes(self, font=None, shape=None):
        if font:
            self.execute('node [fontname="{}"]'.format(font))
        if shape:
            self.execute('node [shape="{}"]'.format(shape))
