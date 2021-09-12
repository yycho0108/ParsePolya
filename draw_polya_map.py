#!/usr/bin/env python3

from typing import Dict, Tuple, List
import networkx as nx


def main():
    G = nx.read_adjlist('/tmp/polya.adjlist', delimiter='\t',
                        create_using=nx.DiGraph)

    # Draw.
    A = nx.drawing.nx_agraph.to_agraph(G)
    A.edge_attr.update(arrowtail='box', color='orange;0.5:purple')
    print(list(A.edge_attr))
    A.layout()
    A.draw('/tmp/polya.svg', prog='dot')


if __name__ == '__main__':
    main()
