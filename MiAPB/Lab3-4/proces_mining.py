import pandas as pd
from itertools import chain
from more_itertools import pairwise
from collections import Counter
import pygraphviz as pgv
from IPython.display import Image, display
from io import BytesIO
import pydot


def adv_modify_w_net(edge_filt, event_filt, w_net, ev_counter):
    # easy filtration
    new_dict = {k: v for k, v in w_net.items() if ev_counter[k] >= event_filt}
    new_dict_2 = {}
    for event, succesors in new_dict.items():
        new_dict3 = {k: v for k, v in succesors.items() if v >= edge_filt}
        new_dict_2[event] = new_dict3

    # advanced filtration with deleting unused nodes
    new_dict_adv = {k: v for k, v in new_dict_2.items() if v != {}}
    used_nodes = [k for k, v in new_dict_adv.items()]
    used_nodes.append('End')

    new_dict_adv2 = {}
    for ev, succ in new_dict_adv.items():
        for succesor, cnt in succ.items():
            if succesor in used_nodes:
                new_dict_adv2.update({ev: {}})

    for ev, succ in new_dict_adv.items():
        for succesor, cnt in succ.items():
            if succesor in used_nodes:
                new_dict_adv2[ev].update({succesor: cnt})

    return new_dict_adv2, used_nodes


def plot_adv_graph(net, sort, ev_start_set, ev_end_set, ev_counter,  trace_max, trace_min):
    G = pgv.AGraph(strict=False, directed=True)
    G.graph_attr['rankdir'] = 'LR'
    G.node_attr['shape'] = 'Mrecord'

    G.add_node("start", shape="circle", label="")
    for ev_start in ev_start_set:
        G.add_edge("start", ev_start)

    # get values from sorted sort
    time_value = sort['diff'].values.tolist()
    val_value = sort['Activity'].values.tolist()

    for event, succesors in net.items():
        value = ev_counter[event]
        ind = val_value.index(event)
        value = time_value[ind]
        color = int(float(time_value[0] - value) / float(time_value[0] - time_value[-1]) * 100.00)
        my_color = "#ff9933" + str(hex(color))[2:]
        G.add_node(event, style="rounded,filled", fillcolor=my_color)
        for succesor, cnt in succesors.items():
            G.add_edge(event, succesor, penwidth=4 * cnt / (trace_max - trace_min) + 0.1, label=cnt)
    G.add_node("end", shape="circle", label="", penwidth='3')
    for ev_end in ev_end_set:
        G.add_edge(ev_end, "end")

    # G.draw('simple_heuristic_net_with_events.png', prog='dot')
    # G = Image('simple_heuristic_net_with_events.png')
    graph_, = pydot.graph_from_dot_data(G.string())
    png_str = graph_.create_png(prog='dot')

    return png_str


def adv_modify_w_net_task_dur(edge_filt, event_filt, csv):
    df = pd.read_csv(csv.name)
    #
    df['start'] = pd.to_datetime(df['Start Timestamp'])
    df['end'] = pd.to_datetime(df['Complete Timestamp'])
    df['diff'] = df['end'] - df['start']
    #
    dfs = df[['Case ID', 'Activity', 'start', 'end', 'diff']]
    diff_df = dfs.groupby('Activity', as_index=False)['diff'].mean()
    ev_counter = dfs.Activity.value_counts()
    dfs = (dfs
           .sort_values(by=['Case ID', 'start'])
           .groupby(['Case ID'])
           .agg({'Activity': ';'.join})
           )

    dfs['count'] = 0
    dfs = (
        dfs.groupby('Activity', as_index=False).count()
            .sort_values(['count'], ascending=False)
            .reset_index(drop=True)
    )
    dfs['trace'] = [trace.split(';') for trace in dfs['Activity']]
    w_net = dict()
    ev_start_set = set()
    ev_end_set = set()
    for index, row in dfs[['trace', 'count']].iterrows():
        if row['trace'][0] not in ev_start_set:
            ev_start_set.add(row['trace'][0])
        if row['trace'][-1] not in ev_end_set:
            ev_end_set.add(row['trace'][-1])
        for ev_i, ev_j in pairwise(row['trace']):
            if ev_i not in w_net.keys():
                w_net[ev_i] = Counter()
            w_net[ev_i][ev_j] += row['count']

    modified_graph, used_nodes = adv_modify_w_net(edge_filt, event_filt, w_net, ev_counter)

    # del elem in diff_df with unused nodes, deleted in adv_modify_w_net function
    diff_mod = diff_df
    dp = diff_mod.loc[diff_mod['Activity'].isin(used_nodes)]

    # sort by time and get intensity of color
    sort = dp.sort_values('diff')
    sort = sort[sort.Activity != 'End']

    trace_counts = sorted(chain(*[c.values() for c in w_net.values()]))
    trace_min = trace_counts[0]
    trace_max = trace_counts[-1]
    color_min = ev_counter.min()
    color_max = ev_counter.max()

    G = plot_adv_graph(modified_graph, sort, ev_start_set, ev_end_set, ev_counter, trace_max, trace_min)

    return G
