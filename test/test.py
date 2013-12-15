#! /usr/bin/env python3
"""
dotter

Copyright (c) 2013, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
import sys
import os
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)

from dotter import Dotter, RankType


def load_data(filename):
    filename = os.path.join(BASE_DIR, 'test/data', filename)
    with open(filename, 'r') as f:
        return f.read().splitlines()


class TestDotter(unittest.TestCase):

    def test_undirected_graph(self):
        dotter = Dotter(directed=False)
        dotter.add_edge('a', 'b')
        expected = ['graph', ' {', 'gb -- gc']
        self.assertEqual(expected, dotter.commands)

    def test_directed_graph(self):
        dotter = Dotter(directed=True)
        dotter.add_edge('a', 'b')
        expected = ['digraph', ' {', 'gb -> gc']
        self.assertEqual(expected, dotter.commands)

    def test_strict(self):
        dotter = Dotter(strict=False)
        dotter.add_edge('a', 'b')
        dotter.add_edge('a', 'b')
        expected = ['digraph', ' {', 'gb -> gc', 'gb -> gc']
        self.assertEqual(expected, dotter.commands)

    def test_addnode_label(self):
        dotter = Dotter()
        dotter.add_node('a', label='b')
        expected = ['digraph', ' {', 'gb', 'gb [label="b"]']
        self.assertEqual(expected, dotter.commands)

    def test_rank(self):
        dotter = Dotter()
        for node in ['a', 'b', 'c', 'd']:
            dotter.add_node(node, label=node)
        dotter.add_edge('a', 'b')
        dotter.add_edge('a', 'c')
        dotter.add_edge('a', 'd')

        dotter.rank(['a', 'b'], RankType.Min)
        dotter.rank(['c'], RankType.Same)
        dotter.rank(['d'], RankType.Max)

        expected = load_data('test_rank.dot')
        self.assertEqual(expected, dotter.commands)


if __name__ == '__main__':
    unittest.main()
