import heapq

class Graph:
    """Клас для представлення зваженого графа."""
    def __init__(self):
        self.vertices = {}

    def add_edge(self, u, v, weight):
        """Додає ребро (u → v) із заданою вагою."""
        if u not in self.vertices:
            self.vertices[u] = []
        if v not in self.vertices:
            self.vertices[v] = []
        self.vertices[u].append((v, weight))
        self.vertices[v].append((u, weight))  # робимо граф неорієнтованим

    def dijkstra(self, start):
        """Знаходить найкоротші шляхи від вершини start до всіх інших."""
        # Відстані до всіх вершин спочатку нескінченні
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start] = 0

        # Бінарна купа для вибору вершини з мінімальною вагою
        heap = [(0, start)]  # (вага, вершина)
        visited = set()

        while heap:
            current_distance, current_vertex = heapq.heappop(heap)

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            # Оновлюємо відстані до сусідів
            for neighbor, weight in self.vertices[current_vertex]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))

        return distances


# ТЕСТОВИЙ ГРАФ

if __name__ == "__main__":
    g = Graph()

    # Додаємо ребра (граф як приклад транспортної мережі)
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)
    g.add_edge("C", "E", 10)
    g.add_edge("D", "E", 2)
    g.add_edge("D", "Z", 6)
    g.add_edge("E", "Z", 3)

    start_node = "A"
    shortest_paths = g.dijkstra(start_node)

    print(f"Найкоротші шляхи від вершини {start_node}:")
    for vertex, distance in shortest_paths.items():
        print(f"{start_node} → {vertex}: {distance}")
