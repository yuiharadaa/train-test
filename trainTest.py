"""
DreamArts 2027 新卒エンジニア採用コーディングテスト
最長片道きっぷの旅（言語: Python 3）

使い方:
  cat input.txt | python solve.py

仕様:
- 入力: "u, v, w"（空白可）を1行1辺として複数行（終端まで）
- 出力: 最長経路のノードIDを1行ずつ（CRLF）で標準出力
注意:
- 一度通ったノードは再訪不可（単純路の最長）
- 有向グラフ想定。孤立頂点・非連結OK
"""
import sys
from typing import Dict, List, Tuple, Set

def parse_edges() -> Tuple[Dict[int, List[Tuple[int, float]]], Set[int]]:
    graph: Dict[int, List[Tuple[int, float]]] = {}
    nodes: Set[int] = set()
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        # 想定フォーマット: "u, v, w"（空白を許容）
        try:
            s, e, d = [x.strip() for x in line.split(",")]
            u, v, w = int(s), int(e), float(d)
        except Exception:
            # 形式がおかしい行は無視（実務的防御）
            continue
        graph.setdefault(u, []).append((v, w))
        nodes.add(u); nodes.add(v)
    # 出次数0でも探索開始点にするため、全ノードをgraphキーとして用意
    for n in nodes:
        graph.setdefault(n, [])
    return graph, nodes

def longest_simple_path(graph: Dict[int, List[Tuple[int, float]]], nodes: Set[int]) -> List[int]:
    best_path: List[int] = []
    best_dist: float = -1.0

    # 反復DFS（スタック）: (現在ノード, 次の辺の走査位置, 現在経路, 訪問集合, 現在距離)
    for start in nodes:
        stack: List[Tuple[int, int, List[int], Set[int], float]] = []
        stack.append((start, 0, [start], {start}, 0.0))

        while stack:
            node, idx, path, visited, dist = stack.pop()

            # ベスト更新
            if dist > best_dist:
                best_dist, best_path = dist, path[:]

            edges = graph.get(node, [])
            # 次の分岐を順に探索
            while idx < len(edges):
                nxt, w = edges[idx]
                idx += 1
                if nxt in visited:
                    continue
                # 現在の状態を戻せるようにプッシュ（分岐継続用）
                stack.append((node, idx, path[:], visited.copy(), dist))
                # 次ノードへ
                new_path = path + [nxt]
                new_visited = visited | {nxt}
                stack.append((nxt, 0, new_path, new_visited, dist + w))
                break  # 直近の分岐を優先して深く潜る（手続き的DFS）
            # すべての辺を試し終えたら自然にバックトラック
    return best_path

def main() -> None:
    graph, nodes = parse_edges()
    if not nodes:
        return
    path = longest_simple_path(graph, nodes)
    # 出力は CRLF（課題の記述に合わせる）
    out = "\r\n".join(str(x) for x in path) + "\r\n"
    sys.stdout.write(out)

if __name__ == "__main__":
    main()
