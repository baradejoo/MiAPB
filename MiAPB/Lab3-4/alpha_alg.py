import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_import
from graph import MyGraph

class AlphaAlgorithm:
    def __init__(self):
        self.log = None
        self.TL_set = None
        self.TI_set = None
        self.TO_set = None
        self.direct_followers_set = None
        self.causalities_dict = None
        self.inv_causalities_dict = None
        self.parallel_tasks_set = None

    def read_log_file(self, filepath):
        self.log = set()

        # if isinstance(filepath, str): // cannot be isinstance used because of streamlit UploadedFile object is not a str
        if True:
            # XES file
            if filepath.name.endswith('.xes'):
                xes_log = xes_import.apply(filepath)
                for trace in xes_log:
                    event_s = [x['concept:name'] for x in trace]
                    self.log.add(tuple(event_s))
            # CSV
            elif filepath.name.endswith('.csv'):
                df = pd.read_csv(filepath,
                                 names=['case_id', 'activity', 'stamp'],
                                 header=1)

                case_number = df["case_id"].iloc[-1]

                for i in range(1, case_number + 1):
                    case_df = df.loc[df['case_id'] == i]
                    self.log.add(tuple(case_df['activity'].tolist()))

        # Python List
        else:
            self.log = filepath

    def build_model(self):
        if self.log is None:
            print("ERROR: Read log file before building model.")
            return
        self.construct_TL_set()
        self.construct_TI_set()
        self.construct_TO_set()
        self.construct_direct_followers_set()
        self.construct_causalities_dict()
        self.construct_inv_causalities_dict()
        self.construct_parallel_tasks_set()

    def create_graph(self, filename=None, show=False):
        if self.log is None:
            print("ERROR: Read log file and build model before creating graph.")
            return
        elif self.TL_set is None:
            print("ERROR: Build model before creating graph.")
            return
        causality = self.causalities_dict
        parallel_event_s = self.parallel_tasks_set
        inv_causality = self.inv_causalities_dict

        '''
        Code below is copied from this site: https://ai.ia.agh.edu.pl/pl:dydaktyka:dss:lab03
        However some modifications were made.
        '''

        G = MyGraph()

        # adding split gateways based on causality
        for event_ in causality.keys():
            if len(causality[event_]) > 1:
                if tuple(causality[event_]) in parallel_event_s:
                    G.add_and_split_gateway(event_, causality[event_])
                else:
                    G.add_xor_split_gateway(event_, causality[event_])

        # adding merge gateways based on inverted causality
        for event_ in inv_causality.keys():
            if len(inv_causality[event_]) > 1:
                if tuple(inv_causality[event_]) in parallel_event_s:
                    G.add_and_merge_gateway(inv_causality[event_], event_)
                else:
                    G.add_xor_merge_gateway(inv_causality[event_], event_)
            elif len(inv_causality[event_]) == 1:
                source = list(inv_causality[event_])[0]
                G.edge(source, event_)

        # adding start event_
        G.add_event__("start")
        if len(self.TI_set) > 1:
            if tuple(self.TI_set) in parallel_event_s:
                G.add_and_split_gateway("start", self.TI_set)
            else:
                G.add_xor_split_gateway("start", self.TI_set)
        else:
            G.edge("start", list(self.TI_set)[0])

        # adding end event_
        G.add_event__("end")
        if len(self.TO_set) > 1:
            if tuple(self.TO_set) in parallel_event_s:
                G.add_and_merge_gateway(self.TO_set, "end")
            else:
                G.add_xor_merge_gateway(self.TO_set, "end")
        else:
            G.edge(list(self.TO_set)[0], "end")

        # G.format = 'svg' - 'graph_folder/' is in content folder always
        if filename is not None:
            G.render('graph_folder/' + filename, format='jpg', view=False)

        return G

    def construct_TL_set(self):
        self.TL_set = set()
        for sequence in self.log:
            for task in sequence:
                self.TL_set.add(task)

    def construct_TI_set(self):
        self.TI_set = set()
        for sequence in self.log:
            self.TI_set.add(sequence[0])

    def construct_TO_set(self):
        self.TO_set = set()
        for sequence in self.log:
            self.TO_set.add(sequence[-1])

    def construct_direct_followers_set(self):
        self.direct_followers_set = set()
        for sequence in self.log:
            for task_a, task_b in zip(sequence, sequence[1:]):
                self.direct_followers_set.add((task_a, task_b))

    def construct_causalities_dict(self):
        self.causalities_dict = {}
        for pair_in_task in self.direct_followers_set:
            if tuple(reversed(pair_in_task)) not in self.direct_followers_set:
                if pair_in_task[0] in self.causalities_dict.keys():
                    self.causalities_dict[pair_in_task[0]].append(pair_in_task[1])
                else:
                    self.causalities_dict[pair_in_task[0]] = [pair_in_task[1]]

    def construct_inv_causalities_dict(self):
        self.inv_causalities_dict = {}
        for key, values in self.causalities_dict.items():
            if len(values) == 1:
                if values[0] in self.inv_causalities_dict.keys():
                    self.inv_causalities_dict[values[0]].append(key)
                else:
                    self.inv_causalities_dict[values[0]] = [key]

    def construct_parallel_tasks_set(self):
        self.parallel_tasks_set = set()
        for pair_in_task in self.direct_followers_set:
            if tuple(reversed(pair_in_task)) in self.direct_followers_set:
                self.parallel_tasks_set.add(pair_in_task)
