# -*- coding: utf-8 -*-
"""
dotter

Copyright (c) 2013-2014, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
import os

from dotter import Dotter, RankType, Shape


def load_data(filename):
    test_data = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    filename = os.path.join(test_data, 'tests/data', filename)
    with open(filename, 'r') as f:
        return f.read().splitlines()


def test_undirected_graph():
    dotter = Dotter(directed=False)
    dotter.add_edge('a', 'b')
    expected = ['graph', ' {', 'gb -- gc']
    assert expected == dotter.commands


def test_directed_graph():
    dotter = Dotter(directed=True)
    dotter.add_edge('a', 'b')
    expected = ['digraph', ' {', 'gb -> gc']
    assert expected == dotter.commands


def test_strict():
    dotter = Dotter(strict=False)
    dotter.add_edge('a', 'b')
    dotter.add_edge('a', 'b')
    expected = ['digraph', ' {', 'gb -> gc', 'gb -> gc']
    assert expected == dotter.commands


def test_addnode_label():
    dotter = Dotter()
    dotter.add_node('a', label='b')
    expected = ['digraph', ' {', 'gb', 'gb [label="b"]']
    assert expected == dotter.commands


def test_rank():
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
    assert expected == dotter.commands


def test_output():
    dotter = Dotter(output_to_file=False, output_type='dot')
    for node in ['a', 'b', 'c', 'd']:
        dotter.add_node(node, label=node)
    output = dotter.close()
    output = output.splitlines()
    expected = load_data('test_output.dot')
    assert output == expected


def test_nodes_attributes():
    dotter = Dotter()
    dotter.nodes_attributes(shape=Shape.Box)
    dotter.nodes_attributes(font='MyFont')
    expected = ['digraph', ' {', 'node [shape="box"]',
                'node [fontname="MyFont"]']
    assert dotter.commands == expected


def test_output_to_file():
    dotter = Dotter(output_filename='test.pdf')
    expected = ['dot', '-Tpdf', '-o', 'test.pdf']
    assert dotter.args == expected


def test_strict_graph():
    dotter = Dotter(strict=True)
    dotter.add_node('a')
    expected = [' strict ', 'digraph', ' {', 'gb', 'gb [label="a"]']
    assert dotter.commands == expected


def test_dotter_str():
    dotter = Dotter(strict=True, output_to_file=False, output_type='svg')
    dotter.add_node('a')
    dotter.close()
    expected = ' strict \ndigraph\n {\ngb\ngb [label="a"]\n}'
    assert str(dotter) == expected


def test_edge_label():
    dotter = Dotter(directed=False)
    dotter.add_edge('a', 'b', 'a to b')
    expected = ['graph', ' {', 'gb -- gc [label="a to b"]']
    assert dotter.commands == expected
