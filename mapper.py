### This file takes two inputs both mentioned at the end of this file:
#### 1. System graph csv file
#### 2. ReBAC policy
### This file returns to the eqOrOpt file two outputs:
#### 1) Low-level authorizations based on given graph and policy
#### 2) Mapping between access requests and relationship patterns

from collections import defaultdict, deque
import csv
import gen_low_level_auths

class LabeledGraphPathFinder(object):
    def __init__(self, csv_file):
        self.graph = defaultdict(list)
        self.source_nodes = set()
        self.target_nodes = set()
        self._load_graph_from_csv(csv_file)
    
    def add_edge(self, source, target, label):
        self.graph[source].append((target, label))
        self.source_nodes.add(source)
        self.target_nodes.add(target)

    def _load_graph_from_csv(self, csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header if exists
            for row in reader:
                source, target, label = row
                self.add_edge(source, target, label)
    
    def find_all_paths(self, max_length=5):
        paths_dict = defaultdict(set)
        
        for start_node in self.source_nodes:
            for end_node in self.target_nodes:
                if start_node == end_node:
                    continue
                
                node_paths = self._bfs_paths(start_node, end_node, max_length)
                if node_paths:
                    for path in node_paths:
                        # Extract only labels from the path
                        label_sequence = [label for (_, _, label) in path]
                        paths_dict[(start_node, end_node)].add(tuple(label_sequence))
        
        return dict(paths_dict)
    
    def _bfs_paths(self, start, end, max_length):
        queue = deque([(start, [], 0)])
        paths = []
        
        while queue:
            current, current_path, path_length = queue.popleft()
            
            if path_length > max_length:
                continue
            
            if current == end and current_path:
                paths.append(current_path)
            
            for neighbor, edge_label in self.graph[current]:
                if path_length < max_length:
                    new_path = current_path + [(current, neighbor, edge_label)]
                    queue.append((neighbor, new_path, path_length + 1))
        
        return paths
    
    def load_policy_from_file(self, txt_file):
        """Read policy TXT file into set of tuples, stripping whitespace."""
        policy = set()
        with open(txt_file, 'r') as f:
            for line in f:
               # Skip empty lines
                if line.strip():
                    policy.add(tuple(item.strip() for item in line.split(',')))
        return policy

def calc_system_metadata(csv_file, txt_file):
    graph = LabeledGraphPathFinder(csv_file)
        
    all_paths = graph.find_all_paths(max_length=5)
    
    policy = graph.load_policy_from_file(txt_file)
    low_level_auths = gen_low_level_auths.find_dict_keys_with_matching_values(all_paths, policy)

    return all_paths, low_level_auths


