import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
 
#  Red de ciudades, rutas y posiciones
CIUDADES = [
    "CDMX", "Puebla", "Querétaro", "Morelia",
    "León", "San Luis", "Guadalajara",
    "Aguascalientes", "Zacatecas", "Torreón",
    "Saltillo", "Monterrey",
]
 
RUTAS = [
    ("CDMX",        "Puebla",          135),
    ("CDMX",        "Querétaro",       215),
    ("CDMX",        "Morelia",         302),
    ("Querétaro",   "León",             90),
    ("Querétaro",   "San Luis",        195),
    ("Querétaro",   "Guadalajara",     360),
    ("León",        "Guadalajara",     155),
    ("León",        "Aguascalientes",  103),
    ("León",        "Morelia",         170),
    ("San Luis",    "Zacatecas",       190),
    ("San Luis",    "Monterrey",       500),
    ("San Luis",    "Saltillo",        460),
    ("Guadalajara", "Aguascalientes",  147),
    ("Guadalajara", "Zacatecas",       290),
    ("Aguascalientes","Zacatecas",     120),
    ("Zacatecas",   "Torreón",         280),
    ("Zacatecas",   "Saltillo",        330),
    ("Torreón",     "Monterrey",       330),
    ("Saltillo",    "Monterrey",        86),
]
 
# Posiciones 
POS = {
    "CDMX":           (-99.1,  19.4),
    "Puebla":         (-98.2,  19.0),
    "Querétaro":      (-100.4, 20.6),
    "Morelia":        (-101.2, 19.7),
    "León":           (-101.7, 21.1),
    "San Luis":       (-100.9, 22.1),
    "Guadalajara":    (-103.3, 20.7),
    "Aguascalientes": (-102.3, 21.9),
    "Zacatecas":      (-102.6, 22.8),
    "Torreón":        (-103.4, 25.5),
    "Saltillo":       (-101.0, 25.4),
    "Monterrey":      (-100.3, 25.7),
}

INF = float('inf')

#  Construir grafo NetworkX
def build_graph():
    G = nx.Graph()
    G.add_nodes_from(CIUDADES)
    for u, v, w in RUTAS:
        G.add_edge(u, v, weight=w)
    return G
 
#  Dijkstra paso a paso
def dijkstra_steps(graph_adj, start):
    dist  = {n: INF for n in CIUDADES}
    prev  = {n: None for n in CIUDADES}
    settled = set()
    pq    = [(0, start)]
    dist[start] = 0
    steps = []  # lista de snapshots
 
    # snapshot inicial
    steps.append({
        "dist":     dict(dist),
        "prev":     dict(prev),
        "settled":  set(settled),
        "current":  None,
        "relaxing": None,
        "log":      f"Inicio: dist[{start}] = 0, resto = ∞",
    })
 
    while pq:
        du, u = heapq.heappop(pq)
        if u in settled:
            continue
        settled.add(u)
        steps.append({
            "dist":     dict(dist),
            "prev":     dict(prev),
            "settled":  set(settled),
            "current":  u,
            "relaxing": None,
            "log":      f"Extraer '{u}' (dist={du} km) → marcado como RESUELTO",
        })
 
        for v, w in graph_adj[u]:
            if v in settled:
                continue
            nd = dist[u] + w
            improved = nd < dist[v]
            if improved:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
            steps.append({
                "dist":     dict(dist),
                "prev":     dict(prev),
                "settled":  set(settled),
                "current":  u,
                "relaxing": (u, v),
                "log":      (f"Relajar {u}→{v} (peso {w} km): dist[{v}] = {nd} km  ✓ mejora"
                             if improved else
                             f"Relajar {u}→{v} (peso {w} km): dist[{v}] = {dist[v]} km  — sin cambio"),
            })
 
    steps.append({
        "dist":     dict(dist),
        "prev":     dict(prev),
        "settled":  set(settled),
        "current":  None,
        "relaxing": None,
        "log":      "¡Algoritmo completado! Todas las distancias mínimas calculadas.",
    })
    return steps, dist, prev
 
 
def build_adj(G):
    adj = {n: [] for n in CIUDADES}
    for u, v, d in G.edges(data='weight'):
        adj[u].append((v, d))
        adj[v].append((u, d))
    return adj
 
 
def reconstruct_path(prev, start, end):
    path, cur = [], end
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == start else []
 
 
# ─────────────────────────────────────────
#  Colores por estado
# ─────────────────────────────────────────
C_DEFAULT  = "#d0d8e8"
C_SETTLED  = "#4caf7d"
C_CURRENT  = "#7c4dff"
C_RELAXING = "#ff9800"
C_START    = "#e53935"
C_PATH     = "#1565c0"
 
E_DEFAULT  = "#b0bec5"
E_RELAXING = "#ff9800"
E_PATH     = "#1565c0"
E_SETTLED  = "#4caf7d"
 

#  Render de un snapshot
def render_step(ax_graph, ax_table, G, step, start, step_idx, total_steps):
    ax_graph.clear()
    ax_table.clear()
 
    dist     = step["dist"]
    prev     = step["prev"]
    settled  = step["settled"]
    current  = step["current"]
    relaxing = step["relaxing"]
    log      = step["log"]
 
    # Colores de nodos 
    node_colors = []
    node_sizes  = []
    for n in G.nodes():
        if n == start:
            node_colors.append(C_START)
            node_sizes.append(900)
        elif n == current:
            node_colors.append(C_CURRENT)
            node_sizes.append(900)
        elif relaxing and n == relaxing[1]:
            node_colors.append(C_RELAXING)
            node_sizes.append(800)
        elif n in settled:
            node_colors.append(C_SETTLED)
            node_sizes.append(750)
        else:
            node_colors.append(C_DEFAULT)
            node_sizes.append(650)
 
    # Colores de aristas 
    edge_colors = []
    edge_widths = []
    path_edges  = set()
    for n in CIUDADES:
        if prev[n]:
            path_edges.add((prev[n], n))
            path_edges.add((n, prev[n]))
 
    for u, v in G.edges():
        if relaxing and ((u == relaxing[0] and v == relaxing[1]) or
                         (v == relaxing[0] and u == relaxing[1])):
            edge_colors.append(E_RELAXING)
            edge_widths.append(3.5)
        elif (u, v) in path_edges or (v, u) in path_edges:
            edge_colors.append(E_PATH)
            edge_widths.append(2.5)
        else:
            edge_colors.append(E_DEFAULT)
            edge_widths.append(1.2)
 
    # Dibujar grafo
    nx.draw_networkx_nodes(G, POS, ax=ax_graph,
                           node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_labels(G, POS, ax=ax_graph,
                            font_size=7, font_weight='bold')
    nx.draw_networkx_edges(G, POS, ax=ax_graph,
                           edge_color=edge_colors, width=edge_widths, alpha=0.85)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, POS, edge_labels=edge_labels,
                                 ax=ax_graph, font_size=6, alpha=0.75,
                                 bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.6))
 
    ax_graph.set_title(f"Paso {step_idx}/{total_steps-1}:  {log}",
                       fontsize=8, pad=8, wrap=True)
    ax_graph.axis('off')
 
    # Leyenda 
    legend = [
        mpatches.Patch(color=C_START,    label="Origen"),
        mpatches.Patch(color=C_CURRENT,  label="Procesando"),
        mpatches.Patch(color=C_RELAXING, label="Relajando"),
        mpatches.Patch(color=C_SETTLED,  label="Resuelto"),
        mpatches.Patch(color=C_DEFAULT,  label="Pendiente"),
    ]
    ax_graph.legend(handles=legend, loc='lower left', fontsize=6.5,
                    framealpha=0.85, edgecolor='#ccc')
 
    #  Tabla de distancias 
    ax_table.axis('off')
    col_labels = ["Ciudad", "Dist (km)", "Vía", "Estado"]
    rows = []
    cell_colors = []
    for n in CIUDADES:
        d = dist[n]
        d_str = str(d) if d != INF else "∞"
        p_str = prev[n] if prev[n] else "—"
        if n in settled:
            estado = "✓ resuelto"
            row_color = ["#c8f0d8", "#c8f0d8", "#c8f0d8", "#c8f0d8"]
        elif n == current:
            estado = "◀ actual"
            row_color = ["#e8d8ff", "#e8d8ff", "#e8d8ff", "#e8d8ff"]
        elif relaxing and n == relaxing[1]:
            estado = "~ relajando"
            row_color = ["#ffe8b0", "#ffe8b0", "#ffe8b0", "#ffe8b0"]
        else:
            estado = "pendiente"
            row_color = ["#f5f5f5", "#f5f5f5", "#f5f5f5", "#f5f5f5"]
        rows.append([n, d_str, p_str, estado])
        cell_colors.append(row_color)
 
    tbl = ax_table.table(
        cellText=rows,
        colLabels=col_labels,
        cellLoc='center',
        loc='center',
        cellColours=cell_colors,
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7.5)
    tbl.scale(1, 1.35)
    ax_table.set_title("Tabla de distancias", fontsize=9, pad=6)
 
 
#  Simulador interactivo
def run_simulator():
    print("\n  Ciudades disponibles:")
    for i, c in enumerate(CIUDADES, 1):
        print(f"  {i:>2}. {c}")
    start = input("\n  Ciudad de origen (Enter = CDMX): ").strip() or "CDMX"
    if start not in CIUDADES:
        print(f"  '{start}' no encontrada. Usando CDMX.")
        start = "CDMX"
 
    G   = build_graph()
    adj = build_adj(G)
    steps, dist_final, prev_final = dijkstra_steps(adj, start)
    total = len(steps)
 
    fig, (ax_graph, ax_table) = plt.subplots(
        1, 2, figsize=(16, 7),
        gridspec_kw={'width_ratios': [2, 1]}
    )
    fig.suptitle("🚚  Logística y Transporte — Dijkstra paso a paso",
                 fontsize=12, fontweight='bold')
    fig.patch.set_facecolor('#f0f2f5')
 
    state = {"idx": 0}
 
    def draw():
        render_step(ax_graph, ax_table, G, steps[state["idx"]],
                    start, state["idx"], total)
        # Mostrar ruta final si está en el último paso
        if state["idx"] == total - 1:
            destino = input_destino.strip()
            if destino and destino in CIUDADES and destino != start:
                path = reconstruct_path(prev_final, start, destino)
                if path:
                    path_edges = list(zip(path[:-1], path[1:]))
                    nx.draw_networkx_edges(G, POS, edgelist=path_edges,
                                           ax=ax_graph, edge_color=C_PATH,
                                           width=4, alpha=1.0)
        fig.canvas.draw_idle()
 
    def on_next(event):
        if state["idx"] < total - 1:
            state["idx"] += 1
            draw()
 
    def on_prev(event):
        if state["idx"] > 0:
            state["idx"] -= 1
            draw()
 
    def on_auto(event):
        for i in range(state["idx"], total):
            state["idx"] = i
            draw()
            plt.pause(0.55)
 
    # Pedir destino para resaltar ruta final
    input_destino = input(f"  Ciudad destino para resaltar ruta final (Enter = Monterrey): ").strip() or "Monterrey"
 
    # Botones
    ax_prev = plt.axes([0.25, 0.02, 0.12, 0.045])
    ax_next = plt.axes([0.44, 0.02, 0.12, 0.045])
    ax_auto = plt.axes([0.63, 0.02, 0.12, 0.045])
 
    from matplotlib.widgets import Button
    btn_prev = Button(ax_prev, '◀ Anterior', color='#dde3f0', hovercolor='#b0bcd8')
    btn_next = Button(ax_next, 'Siguiente ▶', color='#dde3f0', hovercolor='#b0bcd8')
    btn_auto = Button(ax_auto, '▶▶ Auto',    color='#c8f0d8', hovercolor='#80d4a8')
 
    btn_prev.on_clicked(on_prev)
    btn_next.on_clicked(on_next)
    btn_auto.on_clicked(on_auto)
 
    draw()
    plt.tight_layout(rect=[0, 0.07, 1, 0.96])
    plt.show()
 
 
if __name__ == "__main__":
    run_simulator()
 