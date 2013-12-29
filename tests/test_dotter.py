# -*- coding: utf-8 -*-
"""
dotter

Copyright (c) 2013, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
import os
import unittest

from dotter import Dotter, RankType, Shape


def load_data(filename):
    test_data = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    filename = os.path.join(test_data, 'tests/data', filename)
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

    def test_output(self):
        dotter = Dotter(output_to_file=False, output_type='dot')
        for node in ['a', 'b', 'c', 'd']:
            dotter.add_node(node, label=node)
        output = dotter.close()
        output = output.splitlines()
        expected = load_data('test_output.dot')
        self.assertEqual(output, expected)

    def test_nodes_attributes(self):
        dotter = Dotter()
        dotter.nodes_attributes(shape=Shape.Box)
        dotter.nodes_attributes(font='MyFont')
        expected = ['digraph', ' {', 'node [shape="box"]', 'node [fontname="MyFont"]']
        self.assertEqual(dotter.commands, expected)

    def test_output_to_file(self):
        dotter = Dotter(output_filename='test.pdf')
        expected = ['dot', '-Tpdf', '-o', 'test.pdf']
        self.assertEqual(dotter.args, expected)

    def test_strict_graph(self):
        dotter = Dotter(strict=True)
        dotter.add_node('a')
        expected = [' strict ', 'digraph', ' {', 'gb', 'gb [label="a"]']
        self.assertEqual(dotter.commands, expected)

    def test_dotter_str(self):
        dotter = Dotter(strict=True, output_to_file=False, output_type='svg')
        dotter.add_node('a')
        dotter.close()
        expected = ' strict \ndigraph\n {\ngb\ngb [label="a"]\n}'
        self.assertEqual(str(dotter), expected)

    def test_edge_label(self):
        dotter = Dotter(directed=False)
        dotter.add_edge('a', 'b', 'a to b')
        expected = ['graph', ' {', 'gb -- gc [label="a to b"]']
        self.assertEqual(dotter.commands, expected)
