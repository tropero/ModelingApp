import networkx as nx
import matplotlib.pyplot as plt
import os


def generate():
    #GG = nx.erdos_renyi_graph(100, 0.1)
    GG = nx.scale_free_graph(100, alpha=0.53, beta=0.33, gamma=0.14, delta_in=0, delta_out=0, create_using=None,
                              seed=None)
    #GG = nx.watts_strogatz_graph(100, 5, 0.05)

    N, K = GG.order(), GG.size()
    avg_deg = float(K) / N
    print("Nodes: %d Edges: %d Average degree: %f" % (N, K, avg_deg))

    tup1 = []

    G2 = GG.to_undirected()
    print("Is multigraph? : %r " % GG.is_multigraph())

    gg = nx.Graph(G2)  # zamiana z multigrafu na graf usunie parallel edges
    print("2Nodes: %d Edges: %d Average degree: %f" % (N, K, avg_deg))

    tup1.append(N)
    tup1.append(K)
    tup1.append(avg_deg)


    # GG = nx.random_lobster(100, p1=0.6, p2=0.4, seed=None)

    # print(G.nodes())
    #
    # print(G.edges())

    with open("graph.json", "w") as fo:
        fo.write("{ \n  \"graph\": [], \n  \"links\": [")
        print("{ \n  \"graph\": [], \n  \"links\": [")
        for edge in GG.edges()[:-1]:
            fo.write("\t\t{\"source\": %d, \"target\": %d}," % (edge[0], edge[1]))
            print("\t\t{\"source\": %d, \"target\": %d}," % (edge[0], edge[1]))
        else:
            fo.write("\t\t{\"source\": %d, \"target\": %d}" % (edge[0], edge[1]))
            print("\t\t{\"source\": %d, \"target\": %d}" % (edge[0], edge[1]))

        fo.write("\t],   \"nodes\": [")
        print("\t],   \"nodes\": [")
        for node in GG.nodes()[:-1]:
            fo.write("\t\t{\"size\": %d, \"score\": 1, \"id\": \"%s\",\"type\": \"circle\"}," % (
            ((len(GG.neighbors(node)) / 200) * 200), (str(node))))
            print("\t\t{\"size\": %d, \"score\": 1, \"id\": \"%s\",\"type\": \"circle\"}," % (
            ((len(GG.neighbors(node)) / 200) * 200), (str(node))))
        else:
            fo.write("\t\t{\"size\": %d, \"score\": 1, \"id\": \"%s\",\"type\": \"circle\"}" % (
            ((len(GG.neighbors(node)) / 200) * 200), (str(node))))
            print("\t\t{\"size\": %d, \"score\": 1, \"id\": \"%s\",\"type\": \"circle\"}" % (
            ((len(GG.neighbors(node)) / 200) * 200), (str(node))))

        fo.write("\t], \n \"directed\": false, \n \"multigraph\": false \n}")
        print("\t], \n \"directed\": false, \n \"multigraph\": false \n}")

    print("Is multigraph? : %r "% gg.is_multigraph())

    print("Diameter of this graph: %f "% nx.diameter(gg))

    diameter = nx.diameter(gg)

    tup1.append(round(diameter,2))

    print("Transivity of this graph: %f "% nx.transitivity(gg))

    trans = nx.transitivity(gg)
    tup1.append(round(trans, 2))


    # Clustering coefficient of node 0
    print("Clustering coefficient of node 0 %f" % nx.clustering(gg, 0))
    # Clustering coefficient of all nodes (in a dictionary)
    clust_coefficients = nx.clustering(gg)
    # Average clustering coefficient
    ccs = nx.clustering(gg)
    avg_clust = sum(ccs.values()) / len(ccs)

    print("Clustering coefficient of all nodes %f" % avg_clust)

    tup1.append(round(avg_clust,2))


    return tup1
    # tup1.append(avg_clust)
    #
    # for p in tup1:
    #     print(p)
    #
    # gg = GG.to_undirected()
    #
    # hartford_components = nx.connected_component_subgraphs(gg)
    # hartford_mc = hartford_components[0]
    # # Betweenness centrality
    # bet_cen = nx.betweenness_centrality(hartford_mc)
    # # Closeness centrality
    # clo_cen = nx.closeness_centrality(hartford_mc)
    # # Eigenvector centrality
    # eig_cen = nx.eigenvector_centrality(hartford_mc)


    #print("Betweenness centrality %f Closeness centrality %f Eigenvector centrality %f" % (bet_cen, clo_cen, eig_cen))