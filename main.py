import networkx as nx
import random
import igraph as ig
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

# Sort colors by hue, saturation, value and name.
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
sorted_names = [name for hsv, name in by_hsv]
print(sorted_names)
light_color = ['whitesmoke', 'w', 'white', 'snow', 'ivory', 'beige', 'lightyellow', 'antiquewhite', 'tan',
               'navajowhite', 'ghostwhite',
               'black', 'k', 'midnightblue', 'navy', 'darkblue', 'mediumblue', 'b', ]
for lc in light_color:
    sorted_names.remove(lc)
n = len(sorted_names)
print(n)


# 基于GN算法的社团检测
def GN_comm(Gi):
    h1 = Gi.community_edge_betweenness(clusters=None,
                                       directed=False, weights=None)  # GN算法社团检测
    comm_list = list(h1.as_clustering())  # 按照Q最大的原则对系统树图进行切割，
    return comm_list


# 基于fast greedy算法的社团检测
def fastgreedy_comm(Gi):
    h1 = Gi.community_fastgreedy(weights=None)  # fastgreedy算法社团检测
    community_list = list(h1.as_clustering())  # 按照默认Q值最大的原则，对系统树图进行切割
    return community_list


# 基于标签传播label propagation的社团检测
def label_pro_comm(Gi):
    comm_list_G = Gi.community_label_propagation()
    comm_list = []
    for item in comm_list_G:
        comm_list.append(item)
    return comm_list


# 对Graph的社区发现结果染色，不同的社区染成不同的颜色
def color_community(Gi, community_list, method=""):
    # plt.figure(figsize=(16, 16))
    pos = nx.spring_layout(Gi)  # positions for all nodes
    nx.draw_networkx_edges(Gi, pos)
    color_random = random.sample(sorted_names, n)
    color_index = 0
    for comm in community_list:
        nx.draw_networkx_nodes(Gi, pos, nodelist=comm, node_color=color_random[color_index])
        color_index += 1
        plt.axis("off")

    nx.draw_networkx_labels(Gi, pos)
    plt.show()
    # plt.savefig("figs/"+filename.split('.')[0]+"_"+method+".png")


if __name__ == "__main__":
    # Graph 文件名
    filename = "footu.txt"  # "adun_int.txt"  或者  "du.txt"  或者  "footu.txt"
    G = ig.Graph.Read_Edgelist(filename, directed=False)
    Gx = nx.read_edgelist(filename, nodetype=int)

    comm_list = GN_comm(G)
    print(comm_list)
    print(len(comm_list))
    color_community(Gx, comm_list,"gn")

    comm_list = fastgreedy_comm(G)
    print(comm_list)
    print(len(comm_list))
    color_community(Gx, comm_list, "fg")

    comm_list = label_pro_comm(G)
    print(comm_list)
    print(len(comm_list))
    color_community(Gx, comm_list,"lp")
