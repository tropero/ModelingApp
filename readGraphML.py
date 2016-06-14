import math

import networkx as nx
import untangle


def readGraphML(graph):
    if "graphml" in graph:
        # print("reading graphml")
        # g = nx.read_graphml(graph)
        obj = untangle.parse(graph)
        # wierzcholki = [obj.graphml.graph.node]
        # krawedzie = [obj.graphml.graph.edge]
        #
        # print(wierzcholki)
        # print(krawedzie)
        g = nx.Graph()

        for node in obj.graphml.graph.node:
            if "n" in node['id']:
                nn = node['id']
                newnode = nn.replace("n", "")
                g.add_node(newnode)
            else:
                g.add_node(node['id'])
            print("xxx %s"%node['id'])

        for edge in obj.graphml.graph.edge:
            if "n" in edge['source']:
                es = edge['source']
                newsource = es.replace("n", "")
                if "n" in edge['target']:
                    et = edge['target']
                    newtarget = et.replace("n", "")
                    g.add_edge(newsource, newtarget)
            else:
                g.add_edge(edge['source'], edge['target'])

            print("%s ---> %s" % (edge['source'], edge['target']))

        print("graph nodes mod: ")
        nodesListSorted = sorted(g.nodes())
        print(nodesListSorted)
        print("graph edges mod: ")
        edgeListSorted = sorted(g.edges())

        print(edgeListSorted)


    elif "gml" in graph:
        print("reading gml")
        g = nx.read_gml(graph)

    G2 = g.to_undirected()
    print("Is read graph multigraph? : %r " % g.is_multigraph())

    gg = nx.Graph(G2)

    N, K = gg.order(), gg.size()
    avg_deg = float(K) / N
    print("Nodes: %d Edges: %d Average degree: %f" % (N, K, avg_deg))

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

    listSorted = sorted(list, reverse=True)
    print(listSorted)
    sum_of_list = sum(listSorted)
    length_of_list = len(listSorted)
    avg_of_list = sum_of_list / length_of_list
    print("Sum l: %d Len l: %d Avg: %d" % (sum_of_list, length_of_list, avg_of_list))

    tup1.append(N)
    tup1.append(K)
    tup1.append(round(avg_deg, 2))

    json = ""

    with open("C:\\Users\\Krzychu\\Dropbox\\ModelingApp\\static\\g.json", "w") as fo:
        print("{ \n  \"graph\": [], \n  \"nodes\": [")

        json += "{ \n  \"graph\": [], \n  \"nodes\": ["

        for node in nodesListSorted[:-1]:
            print("list neighbour: %d avg:  %d " % (len(gg.neighbors(node)), avg_of_list))
            print(gg.neighbors(node))

            if len(gg.neighbors(node)) > avg_of_list:
                kscore = 0
            else:
                kscore = 1
            print("\t\t{\"size\": %s, \"score\": %s, \"id\": \"%s\",\"type\": \"circle\"}," % (
                int((len(gg.neighbors(node)) / len(gg.nodes())) * 10 + 1),
                kscore,
                (str(node))))
            json += ("\t\t{\"size\": %s, \"score\": %s, \"id\": \"%s\",\"type\": \"circle\"}," % (
                int((len(gg.neighbors(node)) / len(gg.nodes())) * 10 + 1),
                kscore,
                (str(node))))
        else:
            print("list neigh: %d avg:  %d " % (len(gg.neighbors(node)), avg_of_list))
            print(gg.neighbors(node))
            if len(gg.neighbors(node)) > avg_of_list:
                kscore = 0
            else:
                kscore = 1
 
            print("\t\t{\"size\": %s, \"score\": %s, \"id\": \"%s\",\"type\": \"circle\"}" % (
                int((len(gg.neighbors(node)) / len(gg.nodes())) * 10 + 1), kscore, (str(nodesListSorted[-1]))))
            json += ("\t\t{\"size\": %s, \"score\": %s, \"id\": \"%s\",\"type\": \"circle\"}" % (
                int((len(gg.neighbors(node)) / len(gg.nodes())) * 10 + 1), kscore, (str(nodesListSorted[-1]))))



        print("\t],   \"links\": [")
        json += "\t],   \"links\": ["
        for edge in edgeListSorted[:-1]:
            print("\t\t{\"source\": %s, \"target\": %s, \"weight\": 1}," % (edge[0], edge[1]))
            json += ("\t\t{\"source\": %s, \"target\": %s, \"weight\": 1}," % (edge[0], edge[1]))
        else:
            print("\t\t{\"source\": %s, \"target\": %s, \"weight\": 1}" % (edgeListSorted[-1][0], edgeListSorted[-1][1]))
            json += ("\t\t{\"source\": %s, \"target\": %s, \"weight\": 1}" % (edgeListSorted[-1][0], edgeListSorted[-1][1]))

        print("\t], \n \"directed\": false, \n \"multigraph\": false \n}")
        json += "\t], \n \"directed\": false, \n \"multigraph\": false \n}"
    fo.close()

    print("otrzymany json: ")
    print(json)

    print("Is multigraph? : %r " % gg.is_multigraph())

    # print("Diameter of this graph: %f " % nx.diameter(gg))
    try:
        diameter = nx.diameter(gg)
    except nx.exception.NetworkXError:
        diameter = 9999999

    # diameter = 5
    tup1.append(round(diameter, 2))

    print("Transivity of this graph: %f " % nx.transitivity(gg))

    trans = nx.transitivity(gg)
    tup1.append(round(trans, 2))

    # # Clustering coefficient of node 0
    # print("Clustering coefficient of node 0 %f" % nx.clustering(gg, 0))
    # # Clustering coefficient of all nodes (in a dictionary)
    # clust_coefficients = nx.clustering(gg)

    ccs = nx.clustering(gg)
    avg_clust = sum(ccs.values()) / len(ccs)

    print("Clustering coefficient of all nodes %f" % avg_clust)

    tup1.append(round(avg_clust, 2))
    tup1.append(round(standard_deviation, 2))
    tup1.append(json)

    return tup1
