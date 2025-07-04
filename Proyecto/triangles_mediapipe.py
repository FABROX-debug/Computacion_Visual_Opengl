"""
Genera la lista TRIANGLES (índices de 3 en 3) a partir de MediaPipe.
Así nunca faltan ni sobran enteros.
"""

import mediapipe as mp

# MediaPipe solo expone las aristas (pares) de la teselación.
# Para caras 3D necesitamos transformarlas en triángulos:
_EDGES = mp.solutions.face_mesh.FACEMESH_TESSELATION
#     _EDGES es una lista de 542 pares (a,b)

# ───────────────────────────────
# 1) construimos un grafo de vecindad por vértice
from collections import defaultdict
_adj = defaultdict(set)
for a, b in _EDGES:
    _adj[a].add(b)
    _adj[b].add(a)

# 2) un triángulo existe si (a,b) y (b,c) y (c,a) son aristas
_tri_set = set()
for a in range(468):           # solo los 468 primeros vértices del rostro
    for b in _adj[a]:
        for c in _adj[b]:
            if c in _adj[a] and a < b < c:   # evita duplicados / ordena
                _tri_set.add((a, b, c))

# 3) convertimos a lista plana de int
TRIANGLES = sorted(_tri_set)                 # lista de tuplas (a,b,c)
TRIANGLES_FLAT = [idx for tri in TRIANGLES for idx in tri]

# ───────── debug rápido ─────────
if __name__ == "__main__":
    print(f"{len(TRIANGLES)} triángulos  –  {len(TRIANGLES_FLAT)} índices")
