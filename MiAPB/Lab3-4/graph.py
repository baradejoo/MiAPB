'''
Kod poniżej to kod skopiowany z tej strony: https://ai.ia.agh.edu.pl/pl:dydaktyka:dss:lab03
Ostatnia funkcja stanowi rozwiązanie zadania 5.
'''

import graphviz


class MyGraph(graphviz.Digraph):

    def __init__(self):
        graphviz.Digraph.__init__(self)
        self.graph_attr['rankdir'] = 'LR'
        self.node_attr['shape'] = 'Mrecord'
        self.graph_attr['splines'] = 'ortho'
        self.graph_attr['nodesep'] = '0.8'
        self.edge_attr.update(penwidth='2')

    def add_event__(self, name):
        super(MyGraph, self).node(name, shape="circle", label="")

    def add_and_gateway(self, *args):
        super(MyGraph, self).node(*args, shape="diamond",
                                  width=".6", height=".6",
                                  fixedsize="true",
                                  fontsize="40", label="+")

    def add_xor_gateway(self, *args, **kwargs):
        super(MyGraph, self).node(*args, shape="diamond",
                                  width=".6", height=".6",
                                  fixedsize="true",
                                  fontsize="35", label="×")

    def add_and_split_gateway(self, source, targets, *args):
        gateway = 'ANDs ' + str(source) + '->' + str(targets)
        self.add_and_gateway(gateway, *args)
        super(MyGraph, self).edge(source, gateway)
        for target in targets:
            super(MyGraph, self).edge(gateway, target)

    def add_xor_split_gateway(self, source, targets, *args):
        gateway = 'XORs ' + str(source) + '->' + str(targets)
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).edge(source, gateway)
        for target in targets:
            super(MyGraph, self).edge(gateway, target)

    def add_and_merge_gateway(self, sources, target, *args):
        gateway = 'ANDm ' + str(sources) + '->' + str(target)
        self.add_and_gateway(gateway, *args)
        super(MyGraph, self).edge(gateway, target)
        for source in sources:
            super(MyGraph, self).edge(source, gateway)

    def add_xor_merge_gateway(self, sources, target, *args):
        gateway = 'XORm ' + str(sources) + '->' + str(target)
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).edge(gateway, target)
        for source in sources:
            super(MyGraph, self).edge(source, gateway)

    def add_one_loop(self, event, mat, *args):
        in_add = False
        out_add = False
        outname = "one-loop " + str(event) + " out"
        inname = "one-loop " + str(event) + " in"

        if mat['IN'][event] == event:
            self.add_xor_gateway(inname, *args)
            mat['IN'][event] = inname
            in_add = True
        if mat['OUT'][event] == event:
            self.add_xor_gateway(outname, *args)
            mat['OUT'][event] = outname
            out_add = True

        super(MyGraph, self).edge(mat['OUT'][event], mat['IN'][event])

        if in_add == True:
            super(MyGraph, self).edge(mat['IN'][event], event)
        if out_add == True:
            super(MyGraph, self).edge(event, mat['OUT'][event])
