#!/usr/bin/env python3

from typing import Dict, Tuple, List
from fuzzysearch import find_near_matches, find_near_matches_in_file
import itertools
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt


def threes(iterator):
    """s -> (s0,s1,s2), (s1,s2,s3), (s2, s3,4), ..."""
    a, b, c = itertools.tee(iterator, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


def determine_location(
        loc_map: Dict[str, List[Tuple[int, int]]],
        heuristics: List[str],
        start, end):

    # Make a copy
    # print(type(loc_map[list(loc_map.keys())[0]][0][0]))
    loc_map = loc_map.copy()
    loc_map = {
        k: [e for e in v if(start <= e[0] and e[1] < end)]
        for(k, v) in loc_map.items()}

    n = len(heuristics)
    changed = True
    while changed:
        changed = False

        # Process upper bound of first element
        b, c = heuristics[0], heuristics[1]
        upper_bound = max(cc[0] for cc in loc_map[c])
        n0 = len(loc_map[b])
        loc_map[b] = [
            (bb, ee) for (
                bb, ee) in loc_map[b] if (ee < upper_bound)]
        n1 = len(loc_map[b])
        if n1 < n0:
            changed = True

        for a, b, c in threes(heuristics):
            n0 = len(loc_map[b])

            lower_bound = min(aa[1] for aa in loc_map[a])
            upper_bound = max(cc[0] for cc in loc_map[c])

            prv = loc_map[b]
            loc_map[b] = [
                (bb, ee) for (
                    bb, ee) in loc_map[b] if (
                    lower_bound <= bb and ee < upper_bound)]

            # If prev known:: easy
            if len(loc_map[a]) == 1 and len(loc_map[b]) > 0:
                loc_map[b] = [loc_map[b][0]]

            n1 = len(loc_map[b])
            if n1 == 0:
                print('b', b)
                print('prev:lmb', prv)
                print(F'{lower_bound} ~ {upper_bound}')
                raise IndexError('n1==0')

            if n1 < n0:
                # print(F'changed: {loc_map[b]}')
                changed = True

        # Process lower bound of last element
        a, b = heuristics[-2], heuristics[-1]
        lower_bound = min(aa[1] for aa in loc_map[a])
        n0 = len(loc_map[b])
        loc_map[b] = [
            (bb, ee) for (
                bb, ee) in loc_map[b] if (
                lower_bound <= bb)]
        if len(loc_map[a]) == 1 and len(loc_map[b]) > 0:
            loc_map[b] = [loc_map[b][0]]
        n1 = len(loc_map[b])
        if n1 < n0:
            changed = True

    return loc_map


def get_max_l_dist(w):
    if len(w) > 9:
        return 1
    else:
        return 0


def main():

    # NOTE(ycho): `upper()` required since find_near_matches
    # doesn't appear to have an option to toggle case sensitivity.
    with open('heuristics.txt') as f:
        heuristics = [s.strip().upper() for s in f.readlines()]

    with open('polya.txt') as f:
        text = f.read().upper()

    # with open('/tmp/polya.txt') as f:
    h0 = 'PART III. SHORT DICTIONARY OF HEURISTIC'
    m = find_near_matches(h0, text, max_l_dist=get_max_l_dist(h0))
    print(m[1])
    start = m[1].end

    h1 = 'PART IV. PROBLEMS, HINTS, SOLUTIONS'
    m = find_near_matches(h1, text, max_l_dist=get_max_l_dist(h1))
    end = m[1].start
    print(start, end)

    loc_map = {}
    # with open('/tmp/polya.txt') as f:
    for h in heuristics:
        ms = find_near_matches(h, text, max_l_dist=get_max_l_dist(h))
        loc_map[h] = [(m.start, m.end) for m in ms]

    #for h in heuristics:
    #    print(loc_map[h])

    # print(loc_map)

    # Find orderings in which these heuristics were introduced

    bounds_map = determine_location(loc_map, heuristics, start, end)

    corrections = {
        'ANALOGY': [(81118, 81125)],
        'AUXILIARY ELEMENTS': [(96250, 96268)],
        'AUXILIARY PROBLEM': [(102202, 102219)]
    }
    bounds_map.update(corrections)

    print('heuristics ...')
    for h in heuristics:
        print(h, bounds_map[h])
    print('analogy', bounds_map['ANALOGY'])

    for h, b in bounds_map.items():
        if len(b) != 1:
            raise ValueError(F'N[{h}] != 1')

    bounds = [bounds_map[h][0] for h in heuristics]

    # NOTE(ycho): For manual correction ...
    #for h in heuristics:
    #    print(h, loc_map[h])
    #    if len(loc_map[h]) != 1:
    #        # raise ValueError(h, type(h))
    #        for a, b in zip(loc_map[h], loc_map[h][1:]):
    #            print(F'[{h}] for a = {a}')
    #            print(text[a[1]:b[0]])

    G = nx.DiGraph()
    n = len(heuristics)

    for i0, i1 in zip(range(n), range(1, n + 1)):
        h = heuristics[i0]

        flag = False
        if 'WHAT IS THE UNKNOWN' in h:
            flag = True

        # Determine bounds
        b0 = bounds[i0][1]

        if i1 >= n:
            b1 = end
        else:
            b1 = bounds[i1][0]

        if flag:
            print(text[b0:b1])

        #if 'draw a' in h.lower():
        #    print('drawa')
        #    print('bound...', b0, b1)
        #    print(text[b0:b1])
        #    print(loc_map[h])
        #    for (b0,b1) in loc_map[h]:
        #        print(text[b0:b1])

        for h_in, locs in loc_map.items():
            if h == h_in:
                continue

            #if 'draw a' in h.lower() and 'figures' in h_in.lower():
            #    print(h_in)
            #    print('figures...')
            #    print(locs)

            for l in locs:
                if b0 <= l[0] and l[1] < b1:
                    if flag and (h_in not in text[b0:b1]):
                        raise ValueError(
                            F'h_in={h_in} not in text of {h}\n text={text[b0:b1]}')
                    #if 'draw a' in h.lower():
                    #    print(F'{h} connects to {h_in}')
                    G.add_edge(h, h_in)

    # Save graph ...
    nx.write_adjlist(G, '/tmp/polya.adjlist', delimiter='\t')
    print(nx.read_adjlist('/tmp/polya.adjlist', delimiter='\t').nodes())

    seed = [
        'WHAT IS THE UNKNOWN?',
        'IS IT POSSIBLE TO SATISFY THE CONDITION?',
        'DRAW A FIGURE',
        'SEPARATE THE VARIOUS PARTS OF THE CONDITION']

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

    # Draw ...
    A = nx.drawing.nx_agraph.to_agraph(G)
    A.edge_attr.update(arrowtail='box', color='orange;0.5:purple')
    print(list(A.edge_attr))
    A.layout()
    A.draw('/tmp/polya.pdf', prog='dot')

    # [Deprecated & Ugly] Draw ...
    # nx.draw_networkx(G)
    #nx.draw_networkx_nodes(G, G
    #        node_size=[len(v) * 1 for v in G.nodes()],
    #        node_color="w")
    # print(G)
    # plt.show()

    #for h_src, locs in loc_map.items():
    #    for l in locs:
    #        for i, b in enumerate(bounds):
    #            if l[0] > b[1]:
    #                h_dst = heuristics[i]
    #                print(F'{h_dst} connects to {h_src}.')
    #                break


if __name__ == '__main__':
    main()
