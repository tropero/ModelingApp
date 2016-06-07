import math
import random
import os
import networkx as nx
import matplotlib.pyplot as plt
import os


def generate(g_model, g_given_data_dist):
    print(g_model)
    print(type(g_model))
    print(g_given_data_dist)
    print(type(int(g_model)))

    if g_model == "1":
        n = g_given_data_dist['number_of_nodes']
        m = g_given_data_dist['number_of_edges']
        seed = g_given_data_dist['seed']
        print("barabasi_albert_graph n: %s m: %s seed: %s" % (n, m, seed))
        if seed:
            GG = nx.barabasi_albert_graph(n, m, seed)
        else:
            GG = nx.barabasi_albert_graph(n, m)
        print("!!!GG = nx.barabasi_albert_graph(%d, %d)" % (n, m))

    elif g_model == "2":
        # given_data_dict = {'number_of_nodes': '', 'number_of_neighbors': '', 'propability': '', 'seed': ''}
        # watts_strogatz_graph(100, 5, 0.05)
        n = g_given_data_dist['number_of_nodes']
        k = g_given_data_dist['number_of_neighbors']
        p = g_given_data_dist['propability']
        seed = g_given_data_dist['seed']
        # print("watts_strogatz_graph n: %s k: %s p: %s seed: %s" % (n, k, p, seed))
        if seed:
            GG = nx.watts_strogatz_graph(n, k, p, seed)
        else:
            GG = nx.watts_strogatz_graph(n, k, p)
    elif g_model == "3":

        # given_data_dict = {'number_of_nodes': '', 'propability': '', 'seed': ''}

        n = g_given_data_dist['number_of_nodes']
        p = g_given_data_dist['propability']
        seed = g_given_data_dist['seed']
        print("erdos_renyi_graph n: %s p: %s seed: %s" % (n, p, seed))
        if seed:
            GG = nx.nx.erdos_renyi_graph(n, p, seed)
        else:
            GG = nx.nx.erdos_renyi_graph(n, p)
    # else:
    #     GG = nx.scale_free_graph(80, alpha=0.53, beta=0.33, gamma=0.14, delta_in=0, delta_out=0, create_using=None,
    #                        seed=None)
    # GG = nx.erdos_renyi_graph(100, 0.1)
    # GG = nx.scale_free_graph(350, alpha=0.53, beta=0.33, gamma=0.14, delta_in=0, delta_out=0, create_using=None,
    #                        seed=None)
    # GG = nx.watts_strogatz_graph(100, 5, 0.05)
    # GG = nx.barabasi_albert_graph(100, 3)


    G2 = GG.to_undirected()
    print("Is multigraph? : %r " % GG.is_multigraph())

    gg = nx.Graph(G2)  # zamiana z multigrafu na graf usunie parallel edges

    N, K = gg.order(), gg.size()
    avg_deg = float(K) / N
    print("2Nodes: %d Edges: %d Average degree: %f" % (N, K, avg_deg))

    print("Nodes: %d Edges: %d Average degree: %f" % (N, K, avg_deg))

    tup1 = []

    standard_deviation = 0

    list = []

    # print(" stand dev: %f" % standard_deviation)
    for node in gg.nodes():
        # print("Node %d Degree %s" % (node, gg.neighbors(node)))
        current_dev = math.pow((len(gg.neighbors(node)) - avg_deg), 2)
        standard_deviation += current_dev
        if len(gg.neighbors(node)) not in list:
            list.append(len(gg.neighbors(node)))
            # print(" stand dev ++ : %f" % standard_deviation)

    standard_deviation = math.sqrt(standard_deviation / N)
    # print(" stand koniec : %f" % standard_deviation)
    # print("spotkane stopnie: ")
    # print(list)
    listSorted = sorted(list, reverse=True)
    print(listSorted)
    sum_of_list = sum(listSorted)
    length_of_list = len(listSorted)
    avg_of_list = sum_of_list / length_of_list
    print("Sum l: %d Len l: %d Avg: %d" % (sum_of_list, length_of_list, avg_of_list))

    tup1.append(N)
    tup1.append(K)
    tup1.append(round(avg_deg, 2))

    # print(nx.degree_histogram(gg))


    # GG = nx.random_lobster(100, p1=0.6, p2=0.4, seed=None)

    # print(G.nodes())
    #
    # print(G.edges())


    with open("C:\\Users\\Krzychu\\Dropbox\\ModelingApp\\static\\test.json", "w") as fo:
        fo.write("{ \n  \"graph\": [], \n  \"links\": [")
        print("{ \n  \"graph\": [], \n  \"links\": [")
        for edge in gg.edges()[:-1]:
            fo.write("\t\t{\"source\": %d, \"target\": %d}," % (edge[0], edge[1]))
            print("\t\t{\"source\": %d, \"target\": %d}," % (edge[0], edge[1]))
        else:
            fo.write("\t\t{\"source\": %d, \"target\": %d}" % (edge[0], edge[1]))
            print("\t\t{\"source\": %d, \"target\": %d}" % (edge[0], edge[1]))

        fo.write("\t],   \"nodes\": [")
        print("\t],   \"nodes\": [")
        for node in gg.nodes()[:-1]:
            if len(gg.neighbors(node)) > avg_of_list:
                kscore = 0
            else:
                kscore = 1
            fo.write("\t\t{\"size\": %d, \"score\": %d, \"id\": \"%s\",\"type\": \"circle\"}," % (
                ((len(gg.neighbors(node)) / 200) * 200),
                kscore,
                (str(node))))
            print("\t\t{\"size\": %d, \"score\": %d, \"id\": \"%s\",\"type\": \"circle\"}," % (
                ((len(gg.neighbors(node)) / 200) * 200),
                kscore,
                (str(node))))
        else:
            if len(gg.neighbors(node)) > avg_of_list:
                kscore = 0
            else:
                kscore = 1
            fo.write("\t\t{\"size\": %d, \"score\": %d, \"id\": \"%s\",\"type\": \"circle\"}" % (
                ((len(gg.neighbors(node)) / 200) * 200), kscore, (str(node))))
            print("\t\t{\"size\": %d, \"score\": %d, \"id\": \"%s\",\"type\": \"circle\"}" % (
                ((len(gg.neighbors(node)) / 200) * 200), kscore, (str(node))))

        fo.write("\t], \n \"directed\": false, \n \"multigraph\": false \n}")
        print("\t], \n \"directed\": false, \n \"multigraph\": false \n}")
    fo.close()

    print("Is multigraph? : %r " % gg.is_multigraph())

    print("Diameter of this graph: %f " % nx.diameter(gg))

    # diameter = nx.diameter(gg)
    diameter = 5
    tup1.append(round(diameter, 2))

    print("Transivity of this graph: %f " % nx.transitivity(gg))

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

    tup1.append(round(avg_clust, 2))
    tup1.append(round(standard_deviation, 2))

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


    # print("Betweenness centrality %f Closeness centrality %f Eigenvector centrality %f" % (bet_cen, clo_cen, eig_cen))
