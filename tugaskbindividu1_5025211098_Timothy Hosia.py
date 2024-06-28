graph = {
    'A': {'B': 5, 'C': 10, 'D': 8},
    'B': {'E': 12, 'F': 15},
    'C': {'G': 7},
    'D': {'H': 9},
    'E': {'I': 5},
    'F': {'J': 8},
    'G': {'K': 6},
    'H': {'L': 11},
    'I': {'M': 6},
    'J': {'M': 4},
    'K': {'M': 9},
    'L': {'M': 7},
    'M': {}
}

SLD = {
    'A': 13,
    'B': 8,
    'C': 14,
    'D': 15,
    'E': 4,
    'F': 12,
    'G': 10,
    'H': 10,
    'I': 1,
    'J': 4,
    'K': 9,
    'L': 7,
    'M': 0
}

def a_star_search(graph, start, goal, SLD):
    frontier = [(start, 0)]
    explored = set()
    parent = {start: None}
    g = {start: 0}

    while frontier:
        node, cost = frontier.pop(0)
        explored.add(node)

        if node == goal:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return list(reversed(path)), cost

        for neighbor, neighbor_cost in graph[node].items():
            if neighbor not in explored:
                new_cost = g[node] + neighbor_cost
                if neighbor not in [n[0] for n in frontier]:
                    frontier.append((neighbor, new_cost + SLD[neighbor]))
                elif new_cost < g[neighbor]:
                    frontier.remove((neighbor, g[neighbor] + SLD[neighbor]))
                    frontier.append((neighbor, new_cost + SLD[neighbor]))

                parent[neighbor] = node
                g[neighbor] = new_cost

    return None

# Panggil fungsi A* search dengan parameter yang sesuai
path, cost = a_star_search(graph, 'A', 'M', SLD)

# Cetak jalur terpendek dan biayanya
if path:
    print('Jalur terpendek:', ' -> '.join(path))
    print('Biaya:', cost)
else:
    print('Tidak ditemukan jalur dari', start, 'ke', goal)
