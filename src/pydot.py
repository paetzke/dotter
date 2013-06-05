'''
@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2013, Friedrich Paetzke
'''

import base64
import subprocess


def escape(s):
    ' Returns the escaped string '
    s = base64.b16encode(bytes(s, encoding='utf-8')).decode(encoding='utf-8')
    for i in range(10):
        s = s.replace(chr(ord('0') + i), chr(ord('a') + i))
    return s


class Dotter:

    GRAPH_DIRECTED = 0
    GRAPH_UNDIRECTED = 1

    SHAPE_BOX = 'box'
    SHAPE_CIRCLE = 'circle'
    SHAPE_FOLDER = 'folder'
    SHAPE_PLAINTEXT = 'plaintext'
    SHAPE_TRIANGLE = 'triangle'

    OUTPUT_BMP = 'bmp'
    OUTPUT_DOT = 'dot'
    OUTPUT_JPG = 'jpg'
    OUTPUT_PDF = 'pdf'
    OUTPUT_PNG = 'png'
    OUTPUT_PS = 'ps'
    OUTPUT_SVG = 'svg'

    def __init__(self,
                 graphType=GRAPH_DIRECTED,
                 outputType=OUTPUT_PDF,
                 outputFilename=None,
                 isStrict=False):
        self._graphType = graphType
        self._isFirstCmd = True
        self._isStrict = isStrict

        args = ['dot']
        args.append('-T' + outputType)
        if outputFilename is None:
            args.append('-O')
        else:
            args.append('-o')
            args.append(outputFilename)

        self.process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            universal_newlines=True)

    def close(self):
        ' Clean up '
        self.execute('}')

    def execute(self, cmd: str):
        ' Executes the command '
        if self._isFirstCmd:
            self._isFirstCmd = False
            if self._isStrict:
                self.execute(' strict ')
            if self._graphType == Dotter.GRAPH_DIRECTED:
                self.execute('digraph')
            else:
                self.execute('graph')
            self.execute(' {')

        cmd += '\n'
        self.process.stdin.write(cmd)

    def setLabel(self, node, label):
        ' Sets the label for node '
        self.execute('{0} [label="{1}"]'.format(escape(node), label))

    def setLink(self, node1, node2, label=None):
        ' Links node1 with node2 '
        if self._graphType == Dotter.GRAPH_DIRECTED:
            fmt = '{0} -> {1}'
        else:
            fmt = '{0} -- {1}'
        if label is not None:
            fmt += ' [label="{0}"]'.format(label)
        self.execute(fmt.format(escape(node1), escape(node2)))

    def setShape(self, node, shape):
        ' Sets the shape for node  '
        self.execute('{0} [shape="{1}"]'.format(escape(node), shape))
