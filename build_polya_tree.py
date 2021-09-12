#!/usr/bin/env python3

from typing import Dict, Tuple, List
import networkx as nx
from matplotlib import pyplot as plt


def main():
    G = nx.read_adjlist('/tmp/polya.adjlist', delimiter='\t',
                        create_using=nx.DiGraph)

    seed = [
        'WHAT IS THE UNKNOWN?',
        'IS IT POSSIBLE TO SATISFY THE CONDITION?',
        'DRAW A FIGURE',
        'SEPARATE THE VARIOUS PARTS OF THE CONDITION']

    G2 = nx.Graph()

    # Follow recursively through references
    visited = set()
    while seed:
        # Filter incoming seeds, just in case.
        seed = [s for s in seed if s not in visited]

        next_seed = []
        for s in seed:
            if s in visited:
                continue
            visited.add(s)

        for s in seed:
            for src, nxt in G.out_edges(s):
                if nxt in visited:
                    continue
                G2.add_edge(src, nxt)
                print(F'{src}->{nxt}')
                next_seed.append(nxt)

        seed = next_seed
    print(visited)
    print(len(visited))

    A = nx.drawing.nx_agraph.to_agraph(G2)
    # A.edge_attr.update(arrowtail='box', color='orange;0.5:purple')
    A.draw('/tmp/polya_tree.svg', prog='dot')



if __name__ == '__main__':
    main()
