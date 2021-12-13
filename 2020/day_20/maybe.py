import re
import numpy as np
import itertools
import networkx as nx
from collections import deque
from functools import reduce


def all_regex_matches(pattern, line, pos=0):
    collect = []
    while True:
        if (pos > len(line)):
            break
        m = pattern.search(line[pos:])

        found = False
        if (m):
            start, stop = m.span()
            start += pos
            stop += pos
            count = sum([1 if c == '1' else 0 for c in line[start:stop]])
            collect.append([start, count])
            found = True
            pos = start+1
        if (not found):
            break
    return collect


def find(L, x):
    for (i, s) in enumerate(L):
        if (s == x):
            return i
    return -1


def get_top(T):
    return T[0, :]


def get_bottom(T):
    return T[-1, :]


def get_left(T):
    return T[:, 0]


def get_right(T):
    return T[:, -1]


def to_int(row):
    a = [str(s) for s in list(row)]
    return int("".join(a), 2)


def valid_graph(G, grid):
    for (src, dst) in G.edges():
        src_i = src[0]
        src_j = src[1]
        dst_i = dst[0]
        dst_j = dst[1]
        if (not grid[src_i][src_j] is None) and (not grid[dst_i][dst_j] is None):
            edge_data = G.get_edge_data(src, dst)
            node = grid[src_i][src_j]
            if (edge_data['color'] == 'red'):
                above = grid[dst_i][dst_j]
                x = node[0]
                y = above[2]
                if (x != y):
                    return False
            if (edge_data['color'] == 'blue'):
                l = grid[dst_i][dst_j]
                x = node[3]
                y = l[1]
                if (x != y):
                    return False
    return True


def serialize(cur_soln):
    s = []
    for x in cur_soln:
        s.append({"tile_id": int(x[1]), "tile_rotation": int(x[2])})

    return s


def parse(s, truncate=False):
    tile_no = None
    tile = []
    tiles = dict()
    for line in s:
        if (line.startswith("Tile")):
            tile_no = line[5:len(line)-1]
            tile = []
            continue
        if (line == ""):
            if truncate:
                tile.pop()
                tiles[tile_no] = tile[1:]
            else:
                tiles[tile_no] = tile
            continue
        else:
            row = list(map(lambda x: 1 if x == '#' else 0, list(line)))
            if (len(row) > 2 and truncate):
                row = row[1:len(row)-1]
            tile.append(row)
    if (tile != [] and tile_no != None):
        if (truncate):
            tile.pop()
            tiles[tile_no] = tile[1:]
        else:
            tiles[tile_no] = tile

    return tiles


def all_orientations(tile):
    rotated = []
    v = np.array(tile)
    for rotations in range(3):
        mat = np.rot90(v, k=rotations)
        rotated.append([(rotations, 0), mat])
        for flip in range(1, 3):
            flp = np.flip(mat, flip-1)
            rotated.append([(rotations, flip-1), flp])
    return rotated


def all_sides(tile):
    sides = []
    for rotation in tile:
        matrix = rotation[-1]
        top = to_int(get_top(matrix))
        right = to_int(get_right(matrix))
        bottom = to_int(get_bottom(matrix))
        left = to_int(get_left(matrix))

        sides.append([top, right, bottom, left])
    return sides


def get_match_table(permutation_table):
    match_table = dict()
    for (t1, t2) in itertools.combinations(permutation_table, 2):
        if (t1 == t2):
            continue
        if (t1 not in match_table):
            match_table[t1] = set()

        if (t2 not in match_table):
            match_table[t2] = set()

        t1_sides = map(lambda x: set(x), permutation_table[t1])
        t2_sides = map(lambda x: set(x), permutation_table[t2])

        for (side1, side2) in itertools.product(t1_sides, t2_sides):
            if (len(side1.intersection(side2)) > 0):
                match_table[t2].add(t1)
                match_table[t1].add(t2)
                break
    return match_table


def build_orienttion_table(tiles):
    table = dict()
    for tile in tiles:
        table[tile] = all_orientations(tiles[tile])
    return table


def build_permutation_table(tiles):
    table = dict()
    for tile in tiles:
        table[tile] = all_sides(all_orientations(tiles[tile]))
    return table


def bootstrap(tiles, match_table=None):
    possible_corners = []
    if (not match_table):
        match_table = get_match_table(tiles)

    for tile in match_table.keys():
        if (len(match_table[tile]) == 2):
            possible_corners.append(tile)

    bootstrapped = []
    for tile_id in possible_corners:
        b = all_sides(all_orientations(tiles[tile_id]))
        for i, matrix in enumerate(b):
            bootstrapped.append((matrix, tile_id, i))

    return bootstrapped


def iterative_traversal(G, placement_order, tiles, permutation_table, match_table, bootstrap=None):
    pos = 0
    current_soln = []
    num_rotations = 9
    backtracking = False
    alternative_stack = deque()
    while True:
        if (pos < 0):
            return -1

        if (backtracking):
            if (len(alternative_stack) < 1):
                return -1

            pos -= 1
            current_soln.pop()
            alternatives = alternative_stack.pop()

            if (len(alternatives) < 1):
                continue

            (next_matrix, mat_id, rot_id) = alternatives.pop()
            alternative_stack.append(alternatives)
            y = [next_matrix, mat_id, rot_id]
            current_soln.append(y)
            backtracking = False
            pos += 1

        # If we're not backtracking, immediately check the current soln
        grid = [[None] * len(G.nodes()) for _ in range(len(G.nodes()))]
        for i in range(len(current_soln)):
            p_i, p_j = placement_order[i]
            pnn = current_soln[i][0]
            grid[p_i][p_j] = pnn
            if (not valid_graph(G, grid)):
                backtracking = True
                continue

        # Here, the current solution is good, move forward
        if (not backtracking):
            if (len(current_soln) == len(G.nodes())):
                return serialize(current_soln)
            if (len(current_soln) == 0 and bootstrap):
                (next_matrix, mat_id, rot_id) = bootstrap.pop()
                alternative_stack.append(bootstrap)
                y = [next_matrix, mat_id, rot_id]
                current_soln.append(y)
                pos += 1
                continue

            target_pos = placement_order[pos]
            dependencies = [d[0] for d in G.in_edges(target_pos)]
            dependency_pos = list(map(lambda x: find(placement_order, x), dependencies))
            must_intersect = set(filter(lambda z: z < pos, dependency_pos))
            must_intersect2 = [current_soln[xx][1] for xx in list(must_intersect)]
            alternatives = None
            in_use = set([yyy[1] for yyy in current_soln])
            if (len(must_intersect2) == 0):
                alternatives = set(tiles.keys()) - in_use
            else:
                alternatives = match_table[must_intersect2[0]] - in_use
                for xxx in must_intersect2[1:]:
                    alternatives = alternatives.intersection(match_table[xxx])

            possible = []
            for a in alternatives:
                for j in range(num_rotations):  # enumerate(rotation_labels):
                    matrix = permutation_table[a][j]
                    possible.append((matrix, a, j))

            if (len(possible) < 1):
                backtracking = True
                continue
            else:
                (next_matrix, mat_id, rot_id) = possible.pop()
                alternative_stack.append(possible)
                y = [next_matrix, mat_id, rot_id]
                current_soln.append(y)
                pos += 1
                continue


def q1(tiles, permutation_table, match_table, bootstrap=None):
    side_len = int(len(tiles.keys()) ** .5)
    G = nx.DiGraph()
    for i in range(side_len):
        for j in range(side_len):
            node = (i, j)
            G.add_node(node)
            if i >= 1:
                above = (i-1, j)
                if (above not in G.nodes()):
                    G.add_node(above)
                G.add_edge(node, above, weight='Y', color='red')
            if j >= 1:
                left = (i, j-1)
                if (left not in G.nodes()):
                    G.add_node(left)
                G.add_edge(node, left, weight='X', color='blue')

    placement_order = list(nx.dfs_preorder_nodes(G, source=(side_len - 1, side_len - 1)))
    a = iterative_traversal(G, placement_order, tiles, permutation_table,
                            match_table, bootstrap=bootstrap)
    point_dict = dict()
    point_list = []
    for idx, tilex in enumerate(a):
        d = placement_order[idx]
        coord_i = d[0]
        coord_j = d[1]
        point_dict[(coord_i, coord_j)] = tilex
        point_list.append([coord_i, coord_j, tilex['tile_id'], tilex['tile_rotation']])

    p1 = point_dict[(0, 0)]['tile_id']
    p2 = point_dict[(0, side_len - 1)]['tile_id']
    p3 = point_dict[(side_len - 1, 0)]['tile_id']
    p4 = point_dict[(side_len - 1, side_len - 1)]['tile_id']
    return (int(p1)*int(p2)*int(p3)*int(p4), point_list)


def q2(tiles, permutation_table, point_list):
    side_len = int(len(tiles.keys()) ** .5)
    point_dict = dict()
    for item in point_list:
        point_dict[(item[0], item[1])] = {'tile_id': item[2], 'tile_rotation': item[3]}

    rows = []
    for i in range(side_len):
        matrix_id = str(point_dict[(i, 0)]['tile_id'])
        rotation = point_dict[(i, 0)]['tile_rotation']
        row = permutation_table[matrix_id][rotation][1]
        for j in range(1, side_len):
            matrix_id = str(point_dict[(i, j)]['tile_id'])
            rotation = point_dict[(i, j)]['tile_rotation']
            mat = permutation_table[matrix_id][rotation][1]
            row = np.concatenate((row, mat), axis=1)
        rows.append(row)
    mat = rows[0]
    for i in range(1, len(rows)):
        r = rows[i]
        mat = np.concatenate((mat, r), axis=0)
    rows, cols = np.shape(mat)

    snake_re1 = r"(..................1.)"
    snake_re2 = r"(1....11....11....111)"
    snake_re3 = r"(.1..1..1..1..1..1...)"

    hashes_1 = sum([1 if c == '1' else 0 for c in snake_re1])
    hashes_2 = sum([1 if c == '1' else 0 for c in snake_re2])
    hashes_3 = sum([1 if c == '1' else 0 for c in snake_re3])

    pattern1 = re.compile(snake_re1)
    pattern2 = re.compile(snake_re2)
    pattern3 = re.compile(snake_re3)

    rotated = []
    for rotations in range(3):
        mx = np.rot90(mat, k=rotations)
        rotated.append(mx)
        for flip in range(1, 3):
            flp = np.flip(mx, flip-1)
            rotated.append(flp)

    hashmarks = 0
    for mx in rotated:
        s = ""
        (rows, cols) = np.shape(mx)
        count_hashes = 0
        for i in range(rows):
            for j in range(cols):
                s += (str(int(mx[i][j])))
                count_hashes += mx[i][j]
            s += "\n"
        hashmarks = count_hashes
        lines = s.split("\n")

        ones = dict()
        twos = dict()
        threes = dict()
        for idx, line in enumerate(lines):
            ones_matches = all_regex_matches(pattern1, line)
            twos_matches = all_regex_matches(pattern2, line)
            threes_matches = all_regex_matches(pattern3, line)
            for m in ones_matches:
                ones[(idx, m[0])] = m[1]
            for m in twos_matches:
                twos[(idx, m[0])] = m[1]
            for m in threes_matches:
                threes[(idx, m[0])] = m[1]

        snakes = 0
        total_hashes_in_matches = 0  # total number of matches in the pattern group
        for k, v in ones.items():
            cur_hashes_in_matches = v
            line_no, pos = k
            if (line_no + 1, pos) in twos:
                cur_hashes_in_matches += twos[(line_no + 1, pos)]
                if (line_no + 2, pos) in threes:
                    cur_hashes_in_matches += twos[(line_no + 1, pos)]
                    snakes += 1
                    total_hashes_in_matches += cur_hashes_in_matches
                    cur_hashes_in_matches = 0
        if (snakes > 0):
            snake_hashes = snakes * (hashes_1 + hashes_2 + hashes_3)
            nonsnake_hashes = hashmarks - snake_hashes
            return nonsnake_hashes


if __name__ == '__main__':
    s = [x.strip() for x in open("input.in").readlines()]
    tiles = parse(s, False)
    table = build_permutation_table(tiles)
    match_table = get_match_table(table)

    b = bootstrap(tiles, match_table=match_table)

    (q1_ans, point_list) = q1(tiles, table, match_table, bootstrap=b)
    print("q1:", q1_ans)
    q2_tiles = parse(s, True)
    rot_table = build_orienttion_table(q2_tiles)
    p = q2(q2_tiles, rot_table, point_list)
    print("q2:", p)
