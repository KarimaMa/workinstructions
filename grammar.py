"""
used to generate unique IDs for new nodes
"""
class IDGen:
	def __init__(self, n):
		self.n = n
	def __iter__(self):
		return self
	def __next__(self):
		result = self.n
		self.n += 1
		return result

"""
Given a traversal order through a graph, assigns
instance counts based on the order the parts' occurrences
"""
def assign_instance_counts(traversal_order):
	attached_part_counts = {}

	for node in traversal_order:
		if node.part_type in attached_part_counts:
			attached_part_counts[node.part_type] += 1
		else:
			attached_part_counts[node.part_type] = 1
		node.instance_count = attached_part_counts[node.part_type]


"""
simple starting grammar for work instructions
there are two types of actions:
1) placement actions
2) attachment actions

placement_op := <part 1> <part 2>
parts are sorted in contact order
attachment_op := <fastener> <part 1> ... <part n>
"""

def get_part_str(part):
	if part.is_unique:
		# part.instance_count = 1
		# attached_part_counts[part.part_type] = 1
		return part.part_type
	
	# if part.instance_count is None:
	# 	assert attached_part_counts[part.part_type] < part_counts[part.part_type]
	# 	attached_part_counts[part.part_type] += 1
	# 	part.instance_count = attached_part_counts[part.part_type]

	if part.instance_count == 1:
		return "first " + part.part_type
	elif part.instance_count == 2:
		return "second " + part.part_type 
	elif part.instance_count == 3:
		return "third " + part.part_type 
	elif part.instance_count == 4:
		return "fourth " + part.part_type 
	elif part.instance_count == 5:
		return "fifth " + part.part_type 
	else:
		return part.part_type + " " + str(part_counts[part.part_type])


class PlacementOp:
	def __init__(self, part, parts_in_contact):
		self.part = part
		self.parts_in_contact = parts_in_contact

	def print(self):
		if len(self.parts_in_contact) != 0:
			if len(self.parts_in_contact) == 1:
				parts_in_contact_str = f"the {get_part_str(self.parts_in_contact[0])}"
			else:
				parts_in_contact_str = f"the {', '.join([get_part_str(part) for part in self.parts_in_contact[:-1]])}"
				parts_in_contact_str = parts_in_contact_str.strip()
				if len(self.parts_in_contact) == 2:
					parts_in_contact_str += f" and the {get_part_str(self.parts_in_contact[-1])}"
				else:
					parts_in_contact_str += f", and the {get_part_str(self.parts_in_contact[-1])}"

			return f"align the {get_part_str(self.part)} with {parts_in_contact_str}\n"
		else:
			return f"position the {self.part.part_type} for assembly\n"


# parallelized_parts are all placed in the same way 
# relative to parts_in_contact
class ParallelPlacementOp:
	def __init__(self, parallelized_parts, parts_in_contact):
		self.parallelized_parts = parallelized_parts
		self.parts_in_contact = parts_in_contact

	def print(self):
		parallelized_parts_str = f"the {', '.join([get_part_str(part) for part in self.parallelized_parts[:-1]])}"

		parallelized_parts_str = parallelized_parts_str.strip()
		parallelized_parts_str += f", and the {get_part_str(self.parallelized_parts[-1])}"

		if len(self.parts_in_contact) != 0:
			parts_in_contact_str = f"the {', '.join([get_part_str(part) for part in self.parts_in_contact[:-1]])}"
			parts_in_contact_str = parts_in_contact_str.strip()
			if len(self.parts_in_contact) == 2:
				parts_in_contact_str += f" and the {get_part_str(self.parts_in_contact[-1])}"
			else:
				parts_in_contact_str += f", and the {get_part_str(self.parts_in_contact[-1])}"

			return f"align {parallelized_parts_str} with {parts_in_contact_str}\n"
		else:
			return f"position {parallelized_parts_str} for assembly\n"


class AttachmentOp:
	def __init__(self, fastener, parts):
		self.fastener = fastener
		self.parts = parts

	def print(self):
		if self.fastener.part_type == "screw":
			action_str = "screw"
		else:
			raise Exception(f"unknown fastener type {self.fastener.part_type}")

		if len(self.parts) == 1: # just fastening the fastener into one object
			return f"{action_str} into the {get_part_str(self.parts[0])}\n"
		elif len(self.parts) == 2: # fastening two objects together
			first_part_str = get_part_str(self.parts[0])
			second_part_str = get_part_str(self.parts[1])
			return f"{action_str} the {first_part_str} to the {second_part_str}\n"
		else: # fastening more than 2 objects together
			parts_str = f"{','.join([get_part_str(part) for part in self.parts[:-1]])}"
			parts_str += f", and the {get_part_str(self.parts[-1])}"
			return f"{action_str} through the {parts_str}\n"


# fasteners are all fastened in the same way to the the list of parts
class ParallelAttachmentOp:
	def __init__(self, parallelized_fasteners, parts):
		self.parallelized_fasteners = parallelized_fasteners
		self.parts = parts

	def print(self):
		fastener_type = self.parallelized_fasteners[0].part_type
		if fastener_type == "screw":
			action_str = "screw"
			fasteners_str = f"{len(self.parallelized_fasteners)} screws"
		else:
			raise Exception(f"unknown fastener type {fastener_type}")

		# first_part_str = f"the {self.parts[0].part_type}"
		first_part_str = f"the {get_part_str(self.parts[0])}"

		if len(self.parts[1:]) == 1:
			other_parts_str = f"the {get_part_str(self.parts[1])}"
		else:
			other_parts_str = f"the {','.join([get_part_str(part) for part in self.parts[1:-1]])}"
			if len(self.parts[1:]) == 2:
				other_parts_str += f" and the {get_part_str(self.parts[-1])}"
			elif len(self.parts[1:]) > 2 :
				other_parts_str += f", and the {get_part_str(self.parts[-1])}"

		if len(self.parts) >= 2:
			return f"use {fasteners_str} to {action_str} {first_part_str} to {other_parts_str}\n"
		else:
			return f"attach {fasteners_str} to {first_part_str}\n"


"""
Expected input:
A disassembly graph
A list mapping each part to all other parts it touches
	- currently needed to know all the parts that a fastener goes through

Each node has all the other parts that block it from being removed 
as children
"""

class Node:
	def __init__(self, ID, children, parents, is_fastener, part_type, is_unqiue):
		self.ID = ID
		self.children = children
		self.parents = parents
		self.is_fastener = is_fastener
		self.part_type = part_type
		self.instance_count = None # part type occurence number assigned during traversal
		self.is_unqiue = is_unqiue

	def __str__(self):
		return f"id {self.ID} {self.part_type}"

class ParallelNode(Node):
	def __init__(self, ID, nodes):
		self.nodes = nodes
		self.ID = ID		
		self.children = [child for node in self.nodes for child in node.children]
		# parallelized nodes must have the same set of parents and be the same part type
		assert all([nodes[0].parents == node.parents for node in self.nodes])
		assert all([nodes[0].part_type == node.part_type for node in self.nodes])

		self.parents = nodes[0].parents
		self.is_fastener = nodes[0].is_fastener
		self.part_type = nodes[0].part_type
		self.is_unique = None

	def __str__(self):
		return f"parallel node id {self.ID} {self.part_type}"


def get_ID2node_map(node, ID2node_map):
	if not node.ID in ID2node_map:
		ID2node_map[node.ID] = node
	for child in node.children:
		if not child.ID in ID2node_map:
			get_ID2node_map(child, ID2node_map)

"""
When a node has a set of children beloning to the same part type and 
the same operation between itself and each child in the set, we can
parallelize that operation across the children.
This function will modify the DAG to merge all the children into one node
ID is the ID to assign the new parallelized node
contact lists contains for each fastener, all the parts it perforates in
perforation order
"""
def parallelize_op(parent_node, children_nodes, ID, contact_lists):
	# print(f"parallelizing {parent_node.ID} {parent_node.part_type} with children {[node.ID for node in children_nodes]}")
	# print(contact_lists)
	assert(all([contact_lists[children_nodes[0].ID] == contact_lists[node.ID] for node in children_nodes]))
	assert all([children_nodes[0].parents == node.parents for node in children_nodes])
	# for now assert that the nodes being parallelized only have one parent
	assert all([children_nodes[0].part_type == node.part_type for node in children_nodes])

	contact_lists[ID] = contact_lists[children_nodes[0].ID]

	new_node = ParallelNode(ID, children_nodes)
	# remove children from parent node that have been  
	# parallelized and encapsulated into the parallel node
	parent_node_children = []
	for child in parent_node.children:
		if not child in children_nodes:
			parent_node_children += [child]

	parent_node_children += [new_node]
	parent_node.children = parent_node_children

	return new_node


"""
Given a list of nodes, group ones that perform the same
operation together. Two nodes perform the same operation 
if they have the same part type and they share the same
parent parts.
"""
def group_by_operation(nodes):
	op_types = set()
	for node in nodes:
		op_type = (node.is_fastener, node.part_type, '-'.join([str(p.ID) for p in node.parents]))
		op_types.add(op_type)
	groups = {}
	for op_type in op_types:
		groups[op_type] = []
	for node in nodes:
		op_type = (node.is_fastener, node.part_type, '-'.join([str(p.ID) for p in node.parents]))
		groups[op_type] += [node]
	return groups


"""
Returns whether a node is the immediate parent of all
the given children based on the contact lists which
orders all parts in contact in topological order from 
closest to furthest
"""
def is_immediate_parent(node, children, contact_lists):
	for child in children:
		if not node == contact_lists[child.ID][0]:
			return False
	return True


"""
Finds where parallelization of operations over parts
can occur in a graph and mutates it to be parallelized 
root: root node of DAG
contact_lists: dict mapping each fastener to the parts it perforates in perforation order
id_generator: generator to yield new unique IDs to assign to new nodes
"""
def parallelize_where_possible(root, contact_lists, ID2node_map, id_generator):
	node_levels = {}
	levels_dict = {}
	topological_sort(root, node_levels, levels_dict)

	max_level = max(levels_dict.keys())
	for level in range(max_level,-1,-1):		
		level_nodes = levels_dict[level]
		for nodeID in level_nodes:
			node = ID2node_map[nodeID]
			if len(node.children) > 1:
				op_groups = group_by_operation(node.children)
				for op_type, op_group in op_groups.items():
					# for now only parallelize over fasteners 
					# for fasteners that go through multiple parts (i.e. multiple parents), 
					# the parallelization should happen at their immediate parent 
					if len(op_group) > 1 and op_type[0] and is_immediate_parent(node, op_group, contact_lists):
						parallel_node_ID = next(id_generator)
						# print(f"parallelizing {op_type} for parent node {node.ID}")
						parallelize_op(node, op_group, parallel_node_ID, contact_lists)


"""
returns number of nodes in the graph
"""
def count_nodes(root):
	if len(root.children) == 0:
		return 1
	else:
		return 1 + sum([count_nodes(child) for child in self.children])


def topological_sort(node, node_levels, levels_dict):
	if len(node.children) == 0:
		level = 0
		node_levels[node.ID] = level
		if level in levels_dict:
			if not (node.ID in levels_dict[level]):
				levels_dict[level] += [node.ID]
		else:
			levels_dict[level] = [node.ID]
	else:
		for child in node.children:
			topological_sort(child, node_levels, levels_dict) 

		level = max([node_levels[child.ID] for child in node.children]) + 1
		node_levels[node.ID] = level
		if level in levels_dict:
			if not (node.ID in levels_dict[level]):
				levels_dict[level] += [node.ID]
		else:
			levels_dict[level] = [node.ID]



"""
returns the node list with fasteners placed first
"""
def fasteners_first(nodes):
	fasteners = []
	non_fasteners = []
	for n in nodes:
		if n.is_fastener:
			fasteners += [n]
		else:
			non_fasteners += [n]
	return fasteners + non_fasteners

"""
given the topologically sorted node levels and levels dict,
returns a traversal that, from each level, visits as far
down the levels as possible before returning back up as few 
levels as possible to be able to assemble more parts, and 
continuing greedily back down the levels from there

Also takes a priority rule for sorting children
"""
def greedy_order(last_visited_node, visited, order, priority_rule=None):
	if priority_rule is None:
		sorted_children = last_visited_node.children
	else:
		sorted_children = priority_rule(last_visited_node.children)
	for child in sorted_children:
		if can_visit(child, visited) and not child.ID in visited:
			visited += [child.ID]
			order += [child]
			greedy_order(child, visited, order, priority_rule)


def can_visit(node, visited):
	return len(node.parents) == 0 or all([parent.ID in visited for parent in node.parents])


def sort_parts_by_ordinal_number(parts):
	part_dict = {}
	for p in parts:
		if p.part_type in part_dict:
			part_dict[p.part_type] += [p]
		else:
			part_dict[p.part_type] = [p]

	sorted_parts = []
	for p,v in part_dict.items():
		sorted_parts += sorted(v, key=lambda x: x.instance_count)

	return sorted_parts


"""
Program is just an ordered list of statements
since it doesn't seem to need more complicated 
structure like an AST for now
"""
def build_program(DA_dag, ID2node_map, contact_lists, part_counts, traversal_order=None):
	program = []
	node_levels = {}
	levels_dict = {}

	if traversal_order is None:
		node_levels = {}
		levels_dict = {}
		topological_sort(DA_dag, node_levels, levels_dict)
		max_level = max(levels_dict.keys())
		traversal_order = [ID2node_map[nodeID] for level in range(max_level, -1, -1) for nodeID in levels_dict[level]]

	assign_instance_counts(traversal_order)

	top_node = traversal_order[0]
	assert len(top_node.parents) == 0
	statement = PlacementOp(top_node, [])
	program += [statement]

	for i, node in enumerate(traversal_order[1:]):
		if node.is_fastener:
			parts_touching = contact_lists[node.ID]
			if isinstance(node, ParallelNode):
				statement = ParallelAttachmentOp(node.nodes, parts_touching)
			else:
				statement = AttachmentOp(node, parts_touching)
			program += [statement]
		else:
			non_fastener_parents = list(filter(lambda x: not x.is_fastener, node.parents))
			# sort the parts that need to be aligned with this part by their assigned ordinal number
			non_fastener_parents = sort_parts_by_ordinal_number(non_fastener_parents) 
			if isinstance(node, ParallelNode):
				statement = ParallelPlacementOp(node.nodes, non_fastener_parents)
			else:
				statement = PlacementOp(node, non_fastener_parents)
			program += [statement]

	return program


def get_program_str(program):
	program_str = ""
	for statement in program:
		program_str += statement.print()
	return program_str.strip()

"""
For now, to differentiate between sets of identical parts that have 
the same assembly steps, we keep track of how many of each part type
there are and how many have been attached so far. Each part thus gets
an ordinal number by which it is referred to: i.e. screw on the THIRD plate.
"""
def init_attached_part_counts(part_counts):
	attached_part_counts = {}
	for key in part_counts:
		attached_part_counts[key] = 0
	return attached_part_counts

"""
Applies the func to every node in the graph in 
topological order
"""
def graph_walker(DA_dag, ID2node_map, func):
	node_levels = {}
	levels_dict = {}
	topological_sort(DA_dag, node_levels, levels_dict)
	max_level = max(levels_dict.keys())
	for level in range(max_level,-1,-1):
		levelIDs = levels_dict[level]
		for nodeID in levelIDs:
			node = ID2node_map[nodeID]
			func(node)

"""
Make graph2 the child of the given parent node from graph1
"""
def merge_graphs(graph1info, graph2info, parent_node):
	
	graph1nodes, graph1root, graph1contact_lists = graph1info
	graph2nodes, graph2root, graph2contact_lists = graph2info

	parent_node.children += [graph2root]
	assert len(graph2root.parents) == 0
	graph2root.parents = [parent_node]

	graph2_starting_id = max(graph1nodes.keys()) + 1

	def increment_id(node):
		node.ID += graph2_starting_id

	graph_walker(graph2root, graph2nodes, increment_id)

	for key, value in graph2contact_lists.items():
		print(f"node id {key} touches {[str(p) for p in value]}")
		graph1contact_lists[key+graph2_starting_id] = value

	for key, value in graph2nodes.items():
		graph1nodes[key+graph2_starting_id] = value

	return graph1nodes, graph1root, graph1contact_lists

