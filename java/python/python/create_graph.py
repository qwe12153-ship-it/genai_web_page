import json
import networkx as nx
from pyvis.network import Network

# --- 1. 讀取新的多層結構 JSON 檔案 ---
JSON_FILE_NAME = "computer_intro.json" 

try:
    with open(JSON_FILE_NAME, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"錯誤：找不到 '{JSON_FILE_NAME}' 檔案。")
    print("請確認您已下載檔案，並將其與此 Python 程式放在同一個資料夾底下。")
    exit()

# --- 2. 使用 NetworkX 建立一個有向圖物件 ---
G = nx.DiGraph()

# --- 3. 將 JSON 中的節點和邊加入到圖形物件中 ---
# 加入節點 (Nodes)
for node in data['nodes']:
    # 根據節點層級設定不同的大小
    if node['level'] == 1:
        node_size = 40
    elif node['level'] == 2:
        node_size = 25
    elif node['level'] == 3:
        node_size = 15
    elif node['level'] == 4:
        node_size = 10
    else: # Level 5 and beyond
        node_size = 8

    G.add_node(
        node['id'], 
        label=node['label'], 
        level=node['level'],
        group=node['group'],
        size=node_size,
        title=f"層級: {node['level']}\n群組: {node['group']}\nID: {node['id']}"
    )

# 加入邊 (Edges)
for edge in data['edges']:
    if edge['source'] in G and edge['target'] in G:
        G.add_edge(
            edge['source'], 
            edge['target'], 
            title=edge['label'],
            label=edge['label']
        )

# --- 4. 使用 Pyvis 進行互動式視覺化 ---
net = Network(
    height="900px", 
    width="100%", 
    bgcolor="#222222", 
    font_color="white", 
    notebook=False, 
    cdn_resources='remote', 
    directed=True
)

net.from_nx(G)

# --- 5. 設定視覺化選項，優化圖形佈局 ---
net.force_atlas_2based(
    gravity=-80,
    central_gravity=0.01,
    spring_length=220,
    spring_strength=0.08,
    damping=0.4,
    overlap=0
)

net.show_buttons(filter_=['physics'])

# --- 6. 產生最終的 HTML 檔案 ---
try:
    output_filename = "knowledge_graph_L4_plus.html"
    net.save_graph(output_filename)
    print(f"多層級知識圖譜已成功儲存為 '{output_filename}'")
    print("請用您的網頁瀏覽器開啟此檔案以進行互動式瀏覽。")
except Exception as e:
    print(f"儲存檔案時發生錯誤: {e}")