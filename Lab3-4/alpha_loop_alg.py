import pandas as pd


class AlphaAlgorithm_loop:
    def __init__(self, thresh_direct_followers=0.1, thresh_parallel=0.3, thresh_oneloop=0.1):
        self.log = None
        self.all_events_set = None
        self.event_to_index = None
        self.index_to_event = None
        self.prob_matrix = None
        self.parallel_matrix = None
        self.oneloop_vector = None

        self.direct_followers_set = None
        self.causalities_dict = None
        self.inv_causalities_dict = None
        self.parallel_tasks_set = None
        self.oneloop_set = None

        self.direct_followers_threshold = thresh_direct_followers
        self.parallel_threshold = thresh_parallel
        self.oneloop_threshold = thresh_oneloop

    def read_log_file(self, filepath):
        self.log = set()

        if isinstance(filepath, str):
            # XES file
            if filepath.endswith('.xes'):
                xes_log = xes_import.apply(filepath)
                for trace in xes_log:
                    event_s = [x['concept:name'] for x in trace]
                    self.log.add(tuple(event_s))
            # CSV
            elif filepath.endswith('.csv'):
                df = pd.read_csv(filepath,
                                 names=['case_id', 'activity', 'stamp'],
                                 header=1)

                case_number = df["case_id"].iloc[-1]

                for i in range(1, case_number + 1):
                    case_df = df.loc[df['case_id'] == i]
                    self.log.add(tuple(case_df['activity'].tolist()))

            self.all_events_set = set()
            for sequence in self.log:
                for event in sequence:
                    self.all_events_set.add(event)

            self.event_to_index = {event: ind for ind, event in enumerate(self.all_events_set)}
            self.index_to_event = {ind: event for ind, event in enumerate(self.all_events_set)}

        # Python List
        else:
            self.log = filepath

    def build_model(self):
        if self.log is None:
            print("ERROR: Read log file before building model.")
            return
        self._construct_matrices()
        self._construct_direct_followers_set()
        self._construct_causalities_dict()
        self._construct_inv_causalities_dict()
        self._construct_parallel_tasks_set()
        self._construct_TI_set()
        self._construct_TO_set()
        self._construct_oneloop_set()

    def create_graph(self, filename='graph', show=False):
        if self.log is None:
            print("ERROR: Read log file and build model before creating graph.")
            return
        causality = self.causalities_dict
        parallel_events = self.parallel_tasks_set
        inv_causality = self.inv_causalities_dict

        # prepare in/out matrix
        inout_df = pd.DataFrame(index=list(self.all_events_set), columns=['IN', 'OUT'])
        for col in inout_df.columns:
            for row in inout_df.index:
                inout_df[col][row] = row

        '''
        Code below is copied from this site: https://ai.ia.agh.edu.pl/pl:dydaktyka:dss:lab03
        However some modifications were made.
        '''

        G = MyGraph()

        # adding 1loops to graph
        for event in self.oneloop_set:
            G.add_one_loop(event, inout_df)

            # adding split gateways based on causality
        for event in causality.keys():
            if len(causality[event]) > 1:
                if tuple(causality[event]) in parallel_events:
                    G.add_and_split_gateway(inout_df['OUT'][event], [inout_df['IN'][elem] for elem in causality[event]])
                else:
                    G.add_xor_split_gateway(inout_df['OUT'][event], [inout_df['IN'][elem] for elem in causality[event]])

        # adding merge gateways based on inverted causality
        for event in inv_causality.keys():
            if len(inv_causality[event]) > 1:
                if tuple(inv_causality[event]) in parallel_events:
                    G.add_and_merge_gateway([inout_df['OUT'][elem] for elem in inv_causality[event]],
                                            inout_df['IN'][event])
                else:
                    G.add_xor_merge_gateway([inout_df['OUT'][elem] for elem in inv_causality[event]],
                                            inout_df['IN'][event])
            elif len(inv_causality[event]) == 1:
                source = list(inv_causality[event])[0]
                G.edge(inout_df['OUT'][source], inout_df['IN'][event])

        # adding start event
        G.add_event__("start")
        if len(self.TI_set) > 1:
            if tuple(self.TI_set) in parallel_events:
                G.add_and_split_gateway("start", [inout_df['IN'][event] for event in self.TI_set])
            else:
                G.add_xor_split_gateway("start", [inout_df['IN'][event] for event in self.TI_set])
        else:
            G.edge("start", inout_df['IN'][list(self.TI_set)[0]])

        # adding end event
        G.add_event__("end")
        if len(self.TO_set) > 1:
            if tuple(self.TO_set) in parallel_events:
                G.add_and_merge_gateway([inout_df['OUT'][event] for event in self.TO_set], "end")
            else:
                G.add_xor_merge_gateway([inout_df['OUT'][event] for event in self.TO_set], "end")
        else:
            G.edge(inout_df['OUT'][list(self.TO_set)[0]], "end")

        # G.format = 'svg'
        G.render('graph_folder/' + filename, format='jpg', view=True)

        if show == True:
            cv2_imshow(imread('graph_folder/graph1-zad1.jpg'))

    def _construct_matrices(self):
        freq_matrix = [[0 for _ in range(len(self.all_events_set))] for _ in range(len(self.all_events_set))]
        for sequence in self.log:
            for task_a, task_b in zip(sequence, sequence[1:]):
                freq_matrix[self.event_to_index[task_a]][self.event_to_index[task_b]] += 1

        self.prob_matrix = [[0 for _ in range(len(self.all_events_set))] for _ in range(len(self.all_events_set))]
        for row_index, row in enumerate(self.prob_matrix):
            for col_index, elem in enumerate(row):
                task_1_2 = freq_matrix[row_index][col_index]
                task_2_1 = freq_matrix[col_index][row_index]
                self.prob_matrix[row_index][col_index] = (abs(task_1_2) - abs(task_2_1)) / (
                            abs(task_1_2) + abs(task_2_1) + 1)

        self.parallel_matrix = [[0 for _ in range(len(self.all_events_set))] for _ in range(len(self.all_events_set))]
        for row_index, row in enumerate(self.parallel_matrix):
            for col_index, elem in enumerate(row):
                task_1_2 = freq_matrix[row_index][col_index]
                task_2_1 = freq_matrix[col_index][row_index]
                if task_1_2 > 0 and task_2_1 > 0:
                    self.parallel_matrix[row_index][col_index] = 1 - abs(task_1_2 - task_2_1) / max(task_1_2, task_2_1)

        self.oneloop_vector = [0 for _ in range(len(self.all_events_set))]
        for index in range(len(self.all_events_set)):
            self.oneloop_vector[index] = freq_matrix[index][index] / (freq_matrix[index][index] + 1)

    def _construct_direct_followers_set(self):
        self.direct_followers_set = set()
        for row_index, row in enumerate(self.prob_matrix):
            for col_index, elem in enumerate(row):
                if elem > self.direct_followers_threshold:
                    self.direct_followers_set.add((self.index_to_event[row_index], self.index_to_event[col_index]))

    def _construct_causalities_dict(self):
        self.causalities_dict = {}
        for task_pair in self.direct_followers_set:
            if task_pair[0] in self.causalities_dict.keys():
                self.causalities_dict[task_pair[0]].append(task_pair[1])
            else:
                self.causalities_dict[task_pair[0]] = [task_pair[1]]

    def _construct_inv_causalities_dict(self):
        self.inv_causalities_dict = {}
        for key, values in self.causalities_dict.items():
            if len(values) == 1:
                if values[0] in self.inv_causalities_dict.keys():
                    self.inv_causalities_dict[values[0]].append(key)
                else:
                    self.inv_causalities_dict[values[0]] = [key]

    def _construct_parallel_tasks_set(self):
        self.parallel_tasks_set = set()
        for row_index, row in enumerate(self.parallel_matrix):
            for col_index, elem in enumerate(row):
                if row_index == col_index:
                    continue
                if elem > self.parallel_threshold:
                    task_pair = (self.index_to_event[row_index], self.index_to_event[col_index])
                    self.parallel_tasks_set.add(task_pair)

    def _construct_TI_set(self):
        self.TI_set = set()
        next_events = [task_pair[1] for task_pair in self.direct_followers_set]
        for event in self.all_events_set:
            if event not in next_events:
                self.TI_set.add(event)

    def _construct_TO_set(self):
        self.TO_set = set()
        first_events = [task_pair[0] for task_pair in self.direct_followers_set]
        for event in self.all_events_set:
            if event not in first_events:
                self.TO_set.add(event)

    def _construct_oneloop_set(self):
        self.oneloop_set = set()
        for index, prob in enumerate(self.oneloop_vector):
            if prob > self.oneloop_threshold:
                self.oneloop_set.add(self.index_to_event[index])
