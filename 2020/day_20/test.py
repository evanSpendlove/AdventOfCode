from collections import defaultdict
from functools import reduce

import numpy as np
import re

NESSIE = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''.splitlines()

NESSIE_OFFSETS = [(i, j) for i in range(len(NESSIE)) for j in range(len(NESSIE[0])) if NESSIE[i][j] == '#']

class Tile:
    def __init__(self, raw_tile):
        parsed = parse_tile(raw_tile)
        self.id = parsed[0]
        self.shape = parsed[1]
        self.frozen = False
        self.top, self.bottom, self.left, self.right = self._calc_borders()

        self.t, self.b, self.l, self.r = self._calc_borders()
        self.all_possible_borders = {self.t, self.b, self.l, self.r}
        self.rot_left(2)
        self.t, self.b, self.l, self.r = self._calc_borders()
        self.all_possible_borders.update((self.t, self.b, self.l, self.r))
        self.rot_left(2)

    def __str__(self):
        state = f"Tile ID: {self.id}."
        state += f'\n\n {self.shape}'
        return state

    def __repr__(self):
        return str(self.id)

    def _calc_borders(self):
        top = '0b' + ''.join(map(str, self.shape[0]))
        bottom = '0b' + ''.join(map(str, self.shape[-1]))
        left = '0b' + ''.join(map(str, self.shape[:,0]))
        right = '0b' + ''.join(map(str, self.shape[:,-1]))
        borders = (int(border, 2) for border in (top, bottom, left, right))
        return borders

    def rot_left(self, n=1):
        self.shape = np.rot90(self.shape, n)
        self.top, self.bottom, self.left, self.right = self._calc_borders()

    def flip(self):
        self.shape = np.flipud(self.shape)
        self.top, self.bottom, self.left, self.right = self._calc_borders()


def parse_tile(tile):
    lines = tile.splitlines()
    tile_id = int(re.findall(r'\d+', lines[0])[0])
    arr = []
    for line in lines[1:]:
        int_line = []
        for c in line:
            if c == '.':
                int_line.append(0)
            else:
                int_line.append(1)
        arr.append(int_line)
    shape = np.array(arr)

    return tile_id, shape


def make_tiles(inp):
    raw_tiles = inp.split('\n\n')
    parsed_tiles = []
    for t in raw_tiles:
        parsed_tiles.append(Tile(t))
    return parsed_tiles


def check_connection(A, B, side):
    if side == 'R' and A.right == B.left:
        return True
    elif side == 'L' and A.left == B.right:
        return True
    elif side == 'T' and A.top == B.bottom:
        return True
    elif side == 'B' and A.bottom == B.top:
        return True


def count_adj(check, tiles, side, edgecount):
    for tile in tiles:
        if check != tile:
            if check_connection(check, tile, side):
                edgecount[check.id] += 1
                return
            for _ in range(3):
                tile.rot_left()
                if check_connection(check, tile, side):
                    edgecount[check.id] += 1
                    return
            tile.flip()
            if check_connection(check, tile, side):
                edgecount[check.id] += 1
                return
            else:
                for _ in range(3):
                    tile.rot_left()
                    if check_connection(check, tile, side):
                        edgecount[check.id] += 1
                        return


def find_adj(check, tiles, side):
    for tile in tiles:
        if check != tile:
            if check_connection(check, tile, side):
                tile.frozen = True
                return tile
            elif not tile.frozen:
                for _ in range(3):
                    tile.rot_left()
                    if check_connection(check, tile, side):
                        tile.frozen = True
                        return tile
                tile.flip()
                if check_connection(check, tile, side):
                    tile.frozen = True
                    return tile
                else:
                    for _ in range(3):
                        tile.rot_left()
                        if check_connection(check, tile, side):
                            tile.frozen = True
                            return tile


def find_corners(tiles, debug=False):
    edgecount = defaultdict(int)
    corners = []

    for check in tiles:
        if debug:
            print(f"Checking {check.id}")

        for d in ("TBLR"):
            count_adj(check, tiles, d, edgecount)

        if edgecount[check.id] == 2:
            corners.append(check)

        if len(corners) == 4:
            return corners

def find_corners_2(tiles):
    edgecount = defaultdict(int)
    for tile in tiles:
        for other in tiles:
            if tile != other and tile.all_possible_borders & other.all_possible_borders:
                edgecount[tile.id] += 1
    
    corners = [tile for tile in tiles if edgecount[tile.id] == 2]
    return corners


def initiate_row(corners):
    for corner in corners:
        if find_adj(corner, tiles, 'R') and (len(corners) == 1 or find_adj(corner, tiles, 'B')):
            current_leftmost = corner
            next_row = find_adj(corner, tiles, 'B')
            break
    return current_leftmost, next_row


def make_row(init_tile, tiles, row):
    while True:
        next_right = find_adj(init_tile, tiles, 'R')
        if not next_right:
            break
        else:

            next_in_row = np.copy(next_right.shape[1:9, 1:9])
            row = np.concatenate((row, next_in_row), axis=1)
            init_tile = next_right
    return row


def generate_map(tiles, corners):
    rows = []

    while True:
        current_leftmost, next_row = initiate_row(corners)
        row_init = np.copy(current_leftmost.shape[1:9, 1:9])
        row = make_row(current_leftmost, tiles, row_init)
        corners = [next_row]
        rows.append(row)
        if not next_row:
            break

    full_map = rows[0]
    for row in rows[1:]:
        full_map = np.concatenate((full_map, row), axis=0)

    return full_map


def find_monsters(map_monsters):
    monster_count = 0
    for i in range(len(map_monsters)-2):
        j = 0
        while j+20 <= len(map_monsters):
            monster_window = map_monsters[i:i+3, j:j+20]
            is_monster = True
            for coord in NESSIE_OFFSETS:
                x, y = coord
                if monster_window[x][y] != 1:
                    is_monster = False
                    break
            if is_monster:
                print("AAAAAAAAAAH! IT'S A MONSTEEEEEERRRR!")
                monster_count += 1

            j += 1

    return monster_count


def count_monsters(map_monsters):
    count = find_monsters(map_monsters)

    if count == 0:
        for _ in range(3):
            map_monsters = np.rot90(map_monsters, 1)
            count = find_monsters(map_monsters)
            if count != 0:
                return count
        map_monsters = np.flipud(map_monsters)
        count = find_monsters(map_monsters)
        if count != 0:
            return count
        else:
            for _ in range(3):
                map_monsters = np.rot90(map_monsters, 1)
                count = find_monsters(map_monsters)
                if count != 0:
                    return count
    return count


def calculate_roughness(map_monsters, monster_count):
    s = 0
    for row in map_monsters:
        s += np.sum(row)
    return s - (15 * monster_count)


test = '''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###
Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..
Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...
Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.
Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..
Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.
Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#
Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.
Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...'''


print("Tests...")
tiles = make_tiles(test)
corners = find_corners(tiles)
corners = find_corners_2(tiles)
map_monsters = generate_map(tiles, find_corners_2(tiles))
count = count_monsters(map_monsters)
print("Corner product:", reduce(lambda a, b: a * b, [corner.id for corner in corners]) == 20899048083289)
print("Water roughness:", calculate_roughness(map_monsters, count) == 273)
print('---------------------')


with open('input.in', mode='r') as inp:
    print('Solution...')
    tiles = make_tiles(inp.read())
    corners = find_corners_2(tiles)
    map_monsters = generate_map(tiles, corners)
    count = count_monsters(map_monsters)
    print("Corner product:", reduce(lambda a, b: a * b, [corner.id for corner in corners]))
    print("Water roughness:", calculate_roughness(map_monsters, count))
