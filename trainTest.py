#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使い方
    Get-Content input.txt | python trainTest.py

入力形式:
    1 行につき 1 本の路線を表す。
        u, v, w
    u: 始点の駅 ID（整数）
    v: 終点の駅 ID（整数）
    w: 距離（浮動小数点数）
    ※ カンマの前後には任意のスペースを許容する。

出力:
    最長経路を構成する駅 ID を、通過順に 1 行ずつ出力する。
    行末の改行は CRLF (\r\n) とする。

制約:
    - 同じ駅を 2 回以上通る経路は無効（単純路のみを対象）。
    - グラフは有向グラフとして扱う。
    - 孤立頂点や非連結グラフも入力として許容する。
"""

import sys
from typing import Dict, List, Tuple, Set, TextIO


Graph = Dict[int, List[Tuple[int, float]]]


def parse_edges(stream: TextIO) -> Tuple[Graph, Set[int]]:

    graph: Graph = {}
    nodes: Set[int] = set()

    for raw in stream:
        line = raw.strip()
        if not line:
            # 空行は無視
            continue

        try:
            # "u, v, w" をカンマで分割し、空白を取り除く
            s, e, d = (part.strip() for part in line.split(","))
            u = int(s)
            v = int(e)
            w = float(d)
        except Exception:
            # 形式が異なる行はスキップ（防御的プログラミング）
            continue

        graph.setdefault(u, []).append((v, w))
        nodes.add(u)
        nodes.add(v)

    # 出次数 0 の駅も探索開始点にできるよう、キーを補完しておく
    for n in nodes:
        graph.setdefault(n, [])

    return graph, nodes


def dfs_longest_from(
    start: int,
    graph: Graph,
) -> Tuple[float, List[int]]:
    best_dist = 0.0
    best_path: List[int] = [start]

    # (現在の駅, 現在までの距離, 現在の経路, 訪問済み駅集合)
    stack: List[Tuple[int, float, List[int], Set[int]]] = [
        (start, 0.0, [start], {start})
    ]

    while stack:
        node, dist, path, visited = stack.pop()

        # 現時点の経路が最長なら更新
        if dist > best_dist:
            best_dist = dist
            best_path = path

        # 次の駅へ進めるだけ進める
        for nxt, w in graph.get(node, []):
            if nxt in visited:
                # 一度通った駅には戻らない
                continue

            new_dist = dist + w
            new_path = path + [nxt]
            new_visited = visited | {nxt}
            stack.append((nxt, new_dist, new_path, new_visited))

    return best_dist, best_path


def solve_from_stream(stream: TextIO) -> List[int]:
    
    graph, nodes = parse_edges(stream)
    if not nodes:
        return []

    overall_best_dist = -1.0
    overall_best_path: List[int] = []

    # すべての駅を出発点候補として最長経路を探索
    for start in sorted(nodes):
        dist, path = dfs_longest_from(start, graph)
        if dist > overall_best_dist:
            overall_best_dist = dist
            overall_best_path = path

    return overall_best_path


def main() -> None:
    path = solve_from_stream(sys.stdin)

    # 規定通り、駅 ID を 1 行ずつ CRLF で出力する
    if not path:
        return

    out = "\r\n".join(str(x) for x in path) + "\r\n"
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
