#! /usr/bin/env python3

from pydot import Dotter

dotter = Dotter()
dotter.setLink('n1', 'n2', '1To2')
dotter.setLink('n3', 'n2')
dotter.setLink('n1', 'n4')
dotter.setLink('n4', 'n2')
dotter.setLabel('n4', 'NFour')
dotter.setShape('n2', Dotter.SHAPE_TRIANGLE)
dotter.close()
