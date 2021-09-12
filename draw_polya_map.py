#!/usr/bin/env python3

from typing import Dict, Tuple, List
import networkx as nx


def main():
    G = nx.read_adjlist('/tmp/polya.adjlist', delimiter='\t',
                        create_using=nx.DiGraph)

    seed = [
        'WHAT IS THE UNKNOWN?',
        'IS IT POSSIBLE TO SATISFY THE CONDITION?',
        'DRAW A FIGURE',
        'SEPARATE THE VARIOUS PARTS OF THE CONDITION']

    # Follow recursively through references
    visited = set()
    while seed:
        seed = [s for s in seed if s not in visited]
        for s in seed:
            if s in visited:
                continue

            visited.add(s)
            for src, nxt in G.out_edges(s):
                if nxt in visited:
                    continue
                print(F'{src}->{nxt}')
                seed.append(nxt)
    print(visited)
    print(len(visited))

    # Draw.
    A = nx.drawing.nx_agraph.to_agraph(G)
    A.edge_attr.update(arrowtail='box', color='orange;0.5:purple')
    print(list(A.edge_attr))
    A.layout()
    A.draw('/tmp/polya.svg', prog='dot')


if __name__ == '__main__':
    main()
