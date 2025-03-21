#include <iostream>
#include <vector>
#include <queue>

using namespace std;

class Graph {
private:
    int V;
    vector<vector<int>> adj;

public:
    Graph(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    void bfs(int source) {
        vector<int> distance(V, -1);
        queue<int> q;

        distance[source] = 0;
        q.push(source);

        while (!q.empty()) {
            int node = q.front();
            q.pop();

            for (int neighbor : adj[node]) {
                if (distance[neighbor] == -1) {
                    distance[neighbor] = distance[node] + 1;
                    q.push(neighbor);
                }
            }
        }

        cout << "Shortest distances from node " << source << ":\n";
        for (int i = 0; i < V; i++) {
            cout << "To node " << i << ": " << distance[i] << "\n";
        }
    }
};

int main() {
    int vertices = 6;
    Graph g(vertices);

    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 4);
    g.addEdge(3, 5);
    g.addEdge(4, 5);

    g.bfs(0);

    return 0;
}
