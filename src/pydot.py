'''
@author: Friedrich Paetzke <f.paetzke@gmail.com>
@copyright: Copyright (c) 2013 Friedrich Paetzke
@license: GPL
'''

import subprocess


def _esc(s):
    '''
    @type s: str
    '''
    if s is None:
        return ''
    s = s.replace(' ', 'SPACE')
    s = s.replace('-', 'HYPHEN')
    s = s.replace('.', 'DOT')
    s = s.replace('/', 'SLASH')
    s = s.replace('ä', 'ae')
    s = s.replace('ö', 'oe')
    s = s.replace('ü', 'ue')
    return s


class Dotter:

    '''
    '''
    GRAPH_DIRECTED = 0
    GRAPH_UNDIRECTED = 1

    '''
    '''
    SHAPE_BOX = 'box'
    SHAPE_CIRCLE = 'circle'
    SHAPE_FOLDER = 'folder'
    SHAPE_PLAINTEXT = 'plaintext'
    SHAPE_TRIANGLE = 'triangle'

    '''
    '''
    OUTPUT_BMP = 'bmp'
    OUTPUT_DOT = 'dot'
    OUTPUT_JPG = 'jpg'
    OUTPUT_PDF = 'pdf'
    OUTPUT_PNG = 'png'
    OUTPUT_PS = 'ps'
    OUTPUT_SVG = 'svg'


    def __init__(self, graphType=GRAPH_DIRECTED, outputType=OUTPUT_PDF,
                 outputFilename=None, isStrict=False):
        '''
        @type graphType:
        @type outputType:
        @type outputFilename: str
        @type isStrict: bool
        '''
        self._graphType = graphType
        self._isFirstCmd = True
        self._isStrict = isStrict

        args = ['dot']
        args.append('-T%s' % outputType)
        if outputFilename is None:
            args.append('-O')
        else:
            args.append('-o')
            args.append(outputFilename)

        self.process = subprocess.Popen(args,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        universal_newlines=True)


    def close(self):
        ''' Clean Up. '''
        self.execute('}')


    def execute(self, cmd):
        '''
        @type cmd: str
        '''
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
        '''
        @type node: str
        @type label: str
        '''
        self.execute('%s [label="%s"]' % (_esc(node), label))


    def setLink(self, node1, node2, label=None):
        '''
        @type node1: str
        @type node2: str
        @type label: str
        '''
        if self._graphType == Dotter.GRAPH_DIRECTED:
            fmt = '%s -> %s'
        else:
            fmt = '%s -- %s'

        if label is not None:
            fmt += ' [label="%s"]' % label
        self.execute(fmt % (_esc(node1), _esc(node2)))


    def setShape(self, node, shape):
        '''
        @type node: str
        @type shape:
        '''
        self.execute('%s [shape="%s"]' % (_esc(node), shape))
