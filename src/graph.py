from collections import defaultdict
from quick_union import QuickUnion


def bucket_to_graph(buckets):
    graph = defaultdict(set)

    for ib, buc in enumerate(buckets):
        print(ib, len(buc))
        for i in buc:
            for j in buc:
                if i != j:
                    graph[i].add(j)
                    graph[j].add(i)

    return dict(graph)


def graph_to_edges(graph):
    pass


def prim_path(graph):
    pass


def kruskal_path(image_pairs, nodes):
    '''
    Kruskal like algorithm for creating path

    Args:
      image_pairs: list of (image1, image2, score)
    '''

    edges = defaultdict(list)
    stop = len(nodes) - 1

    # prevents self loops
    qu = QuickUnion(len(nodes))
    qu_idx = {v: i for i, v in enumerate(nodes)}

    sorted_image_pairs = sorted(image_pairs,
                                key=lambda x: x[2], reverse=True)

    print('\t- Calculating minimum spanning path...')

    for i, j, score in sorted_image_pairs:
        # number of node constrained with two
        if len(edges[i]) < 2 and len(edges[j]) < 2 \
           and (not qu.is_connected(qu_idx[i], qu_idx[j])):
            edges[i].append(j)
            edges[j].append(i)
            qu.connect(qu_idx[i], qu_idx[j])

            # Early stop we have N-1 edge after all
            stop -= 1
            if stop == 0:
                break

    return list(reconstruct_path(edges))


def reconstruct_path(edges):
    visited = set()
    start_nodes = (k for k, v in edges.items() if len(v) == 1)

    for start in start_nodes:
        if start not in visited:
            yield from (_reconstruct_path_step(edges, start, visited))


def _reconstruct_path_step(edges, start, visited):
    curr = start
    while True:
        yield curr
        visited.add(curr)

        if len(edges[curr]) == 0:
            break

        for nn in edges[curr]:
            edges[nn].remove(curr)
        curr = nn