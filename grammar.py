"""
simple starting grammar for work instructions
there are two types of actions:
1) placement actions
2) attachment actions

placement_op := <part 1> <part 2>
parts are sorted in contact order
attachment_op := <fastener> <part 1> ... <part n>
"""

def get_part_str(part, part_counts, attached_part_counts):
	if part_counts[part.part_type] == 1:
		part.instance_count = 1
		attached_part_counts[part.part_type] = 1
		return part.part_type
	
	if part.instance_count is None:
		assert attached_part_counts[part.part_type] < part_counts[part.part_type]
		attached_part_counts[part.part_type] += 1
		part.instance_count = attached_part_counts[part.part_type]

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

	def print(self, part_counts, attached_part_counts):
		if len(self.parts_in_contact) != 0:
			if len(self.parts_in_contact) == 1:
				parts_in_contact_str = f"the {get_part_str(self.parts_in_contact[0], part_counts, attached_part_counts)}"
			else:
				parts_in_contact_str = f"the {', '.join([get_part_str(part, part_counts, attached_part_counts) for part in self.parts_in_contact[:-1]])}"
				parts_in_contact_str = parts_in_contact_str.strip()
				if len(self.parts_in_contact) == 2:
					parts_in_contact_str += f" and the {get_part_str(self.parts_in_contact[-1], part_counts, attached_part_counts)}"
				else:
					parts_in_contact_str += f", and the {get_part_str(self.parts_in_contact[-1], part_counts, attached_part_counts)}"

			print(f"align the {get_part_str(self.part, part_counts, attached_part_counts)} with {parts_in_contact_str}")
		else:
			print(f"position the {self.part.part_type} for assembly")


# parallelized_parts are all placed in the same way 
# relative to parts_in_contact
class ParallelPlacementOp:
	def __init__(self, parallelized_parts, parts_in_contact):
		self.parallelized_parts = parallelized_parts
		self.parts_in_contact = parts_in_contact

	def print(self, part_counts, attached_part_counts):
		parallelized_parts_str = f"the {', '.join([get_part_str(part, part_counts, attached_part_counts) for part in self.parallelized_parts[:-1]])}"

		parallelized_parts_str = parallelized_parts_str.strip()
		parallelized_parts_str += f", and the {get_part_str(self.parallelized_parts[-1], part_counts, attached_part_counts)}"

		if len(self.parts_in_contact) != 0:
			parts_in_contact_str = f"the {', '.join([get_part_str(part, part_counts, attached_part_counts) for part in self.parts_in_contact[:-1]])}"
			parts_in_contact_str = parts_in_contact_str.strip()
			if len(self.parts_in_contact) == 2:
				parts_in_contact_str += f" and the {get_part_str(self.parts_in_contact[-1], part_counts, attached_part_counts)}"
			else:
				parts_in_contact_str += f", and the {get_part_str(self.parts_in_contact[-1], part_counts, attached_part_counts)}"

			print(f"align {parallelized_parts_str} with {parts_in_contact_str}")
		else:
			print(f"position {parallelized_parts_str} for assembly")


class AttachmentOp:
	def __init__(self, fastener, parts):
		self.fastener = fastener
		self.parts = parts

	def print(self, part_counts, attached_part_counts):
		if self.fastener.part_type == "screw":
			action_str = "screw"
		else:
			raise Exception(f"unknown fastener type {self.fastener.part_type}")

		first_part_str = f"the {get_part_str(self.parts[0], part_counts, attached_part_counts)}"

		if len(self.parts[1:]) == 1:
			other_parts_str = f"the {get_part_str(self.parts[1], part_counts, attached_part_counts)}"
		else:
			other_parts_str = f"the {','.join([get_part_str(part, part_counts, attached_part_counts) for part in self.parts[1:-1]])}"
			if len(self.parts[1:]) == 2:
				other_parts_str += f" and the {get_part_str(self.parts[-1], part_counts, attached_part_counts)}"
			elif len(self.parts[1:]) > 2:
				other_parts_str += f", and the {get_part_str(self.parts[-1], part_counts, attached_part_counts)}"

		if len(self.parts[1:]) == 1:
			print(f"{action_str} {first_part_str} to {other_parts_str}")
		else:
			print(f"{action_str} through {other_parts_str}")


# fasteners are all fastened in the same way to the the list of parts
class ParallelAttachmentOp:
	def __init__(self, parallelized_fasteners, parts):
		self.parallelized_fasteners = parallelized_fasteners
		self.parts = parts

	def print(self, part_counts, attached_part_counts):
		fastener_type = self.parallelized_fasteners[0].part_type
		if fastener_type == "screw":
			action_str = "screw"
			fasteners_str = f"{len(self.parallelized_fasteners)} screws"
		else:
			raise Exception(f"unknown fastener type {fastener_type}")

		# first_part_str = f"the {self.parts[0].part_type}"
		first_part_str = f"the {get_part_str(self.parts[0], part_counts, attached_part_counts)}"

		if len(self.parts[1:]) == 1:
			other_parts_str = f"the {get_part_str(self.parts[1], part_counts, attached_part_counts)}"
		else:
			other_parts_str = f"the {','.join([get_part_str(part, part_counts, attached_part_counts) for part in self.parts[1:-1]])}"
			if len(self.parts[1:]) == 2:
				other_parts_str += f" and the {get_part_str(self.parts[-1], part_counts, attached_part_counts)}"
			elif len(self.parts[1:]) > 2 :
				other_parts_str += f", and the {get_part_str(self.parts[-1], part_counts, attached_part_counts)}"

		if len(self.parts) >= 2:
			print(f"use {fasteners_str} to {action_str} {first_part_str} to {other_parts_str}")
		else:
			print(f"attach {fasteners_str} to {first_part_str}")


"""
Expected input:
A disassembly graph
A list mapping each part to all other parts it touches
	- currently needed to know all the parts that a fastener goes through

Each node has all the other parts that block it from being removed 
as children
"""

class Node:
	def __init__(self, ID, children, parents, is_fastener, part_type):
		self.ID = ID
		self.children = children
		self.parents = parents
		self.is_fastener = is_fastener
		self.part_type = part_type
		self.instance_count = None # part type occurence number assigned during traversal

	def __str__(self):
		return f"id {self.ID} {self.part_type}"

class ParallelNode(Node):
	def __init__(self, ID, nodes):
		self.nodes = nodes
		self.ID = ID		
		self.children = [child for child in node.children for node in self.nodes]
		# parallelized nodes must have the same set of parents and be the same part type
		assert all([nodes[0].parents == node.parents for node in self.nodes])
		assert all([nodes[0].part_type == node.part_type for node in self.nodes])

		self.parents = nodes[0].parents
		self.is_fastener = nodes[0].is_fastener
		self.part_type = nodes[0].part_type

	def __str__(self):
		return f"parallel node id {self.ID} {self.part_type}"


def get_ID2node_map(node, ID2node_map):
	for child in node.children:
		if not child in ID2node_map:
			ID2node_map[child.ID] = child
			get_ID2node_map(child, ID2node_map)

"""
When a node has a set of children beloning to the same part type and 
the same operation between itself and each child in the set, we can
parallelize that operation across the children.
This function will modify the DAG to merge all the children into one node
"""
def parallelize_op(parent_node, children_nodes, ID, contact_lists):
	assert(all([contact_lists[children_nodes[0].ID] == contact_lists[node.ID] for node in children_nodes]))
	assert all([children_nodes[0].parents == node.parents for node in children_nodes])
	# for now assert that the nodes being parallelized only have one parent
	assert len(children_nodes[0].parents) == 1 and children_nodes[0].parents[0] == parent_node
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
returns number of nodes in the graph
"""
def count_nodes(root):
	if len(root.children) == 0:
		return 1
	else:
		return 1 + sum([count_nodes(child) for child in self.children])


def topological_sort(node, node_levels, levels_dict):
	print(str(node))
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

"""
Program is just an ordered list of statements
since it doesn't seem to need more complicated 
structure like an AST for now
"""
def build_program(DA_dag, ID2node_map, contact_lists, part_counts, traversal_order=None):
	program = []
	node_levels = {}
	levels_dict = {}
	topological_sort(DA_dag, node_levels, levels_dict)
	for level in levels_dict:
		print(f"{level}: {[ID2node_map[p].part_type for p in levels_dict[level]]}")

	if traversal_order is None:
		node_levels = {}
		levels_dict = {}
		topological_sort(DA_dag, node_levels, levels_dict)

		max_level = max(levels_dict.keys())

		for level in range(max_level,-1,-1):
			levelIDs = levels_dict[level]
			if level == max_level:
				top_node = ID2node_map[levelIDs[0]]
				assert len(levelIDs) == 1 and len(top_node.parents) == 0
				statement = PlacementOp(top_node, [])
				program += [statement]
				print(f"level {level} nodeID {levelIDs[0]} {top_node.part_type}")

			else:
				for nodeID in levelIDs:
					node = ID2node_map[nodeID]
					print(f"level {level} {str(node)} parents {[str(p) for p in node.parents]}")
					if node.is_fastener:
						parts_touching = contact_lists[nodeID]
						print(f"touching parts {[str(p) for p in parts_touching]}")
						if isinstance(node, ParallelNode):
							statement = ParallelAttachmentOp(node.nodes, parts_touching)
						else:
							statement = AttachmentOp(node, parts_touching)
						program += [statement]
					else:
						# part is not a fastener but is blocking and thus 
						# touching all of its parents. We must align this
						# part with all of its parents to prepare it for
						# subsequent fastening steps. We ignore parents that
						# are fasteners because parent fasteners do not have 
						# notable interations with their children
						non_fastener_parents = list(filter(lambda x: not x.is_fastener, node.parents))
						if isinstance(node, ParallelNode):
							statement = ParallelPlacementOp(node.nodes, non_fastener_parents)
						else:
							statement = PlacementOp(node, non_fastener_parents)
						program += [statement]
	else:
		top_node = traversal_order[0]
		assert len(top_node.parents) == 0
		statement = PlacementOp(top_node, [])
		program += [statement]
		print(f"first node {top_node.part_type}")

		for i, node in enumerate(traversal_order[1:]):
			print(f"{i}th visited: {str(node)} parents {[str(p) for p in node.parents]}")
			if node.is_fastener:
				parts_touching = contact_lists[node.ID]
				print(f"touching parts {[str(p) for p in parts_touching]}")
				if isinstance(node, ParallelNode):
					statement = ParallelAttachmentOp(node.nodes, parts_touching)
				else:
					statement = AttachmentOp(node, parts_touching)
				program += [statement]
			else:
				non_fastener_parents = list(filter(lambda x: not x.is_fastener, node.parents))
				if isinstance(node, ParallelNode):
					statement = ParallelPlacementOp(node.nodes, non_fastener_parents)
				else:
					statement = PlacementOp(node, non_fastener_parents)
				program += [statement]

	return program


def print_program(program, part_counts, attached_part_counts):
	for statement in program:
		statement.print(part_counts, attached_part_counts)


"""
For now, to differentiate between sets of identical parts that have 
the same assembly steps, we keep track of how many of each part type
there are and how many have been attached so far. Each part thus gets
an ordinal number by which it is referred to: i.e. screw on the THIRD plate.
"""
def init_attached_part_counts(part_counts):
	attached_part_counts = {}
	for key in part_counts:
		print(f"key {key}")
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
	print(f"in graph walker max level: {max_level}")
	for level in range(max_level,-1,-1):
		levelIDs = levels_dict[level]
		print(f"level {level} levelids {levelIDs}")
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
	print(f"in merge graphs graph 2 starting ID: {graph2_starting_id}")

	def increment_id(node):
		node.ID += graph2_starting_id

	graph_walker(graph2root, graph2nodes, increment_id)

	for key, value in graph2contact_lists.items():
		print(f"node id {key} touches {[str(p) for p in value]}")
		graph1contact_lists[key+graph2_starting_id] = value

	for key, value in graph2nodes.items():
		graph1nodes[key+graph2_starting_id] = value

	return graph1nodes, graph1root, graph1contact_lists


def test_graph0():
	# make all the nodes first with empty fields
	part_names = ["a", "b", "c", "d", "e", "f", "g", "h"]
	fastener_names = ["ab", "hg", "bc", "dc", "ec", "fc", "gc"]
	part_counts = {"block": len(part_names), "screw": len(fastener_names)}

	nodes = {}
	for name in part_names:
		nodes[name] = Node(name, [], [], False, "block")
	for name in fastener_names:
		nodes[name] = Node(name, [], [], True, "screw")

	nodes["ab"].children = []
	nodes["ab"].parents = [nodes["a"]]

	nodes["hg"].children = []
	nodes["hg"].parents = [nodes["h"]]

	nodes["a"].children = [nodes["ab"]]
	nodes["a"].parents = [nodes["b"], nodes["bc"]]

	nodes["h"].children = [nodes["hg"]]
	nodes["h"].parents = [nodes["g"], nodes["gc"]]

	nodes["b"].children = [nodes["a"], nodes["bc"]]
	nodes["b"].parents = [nodes["c"], nodes["d"], nodes["dc"]]

	nodes["g"].children = [nodes["h"], nodes["gc"]]
	nodes["g"].parents = [nodes["c"], nodes["f"], nodes["fc"]]

	nodes["d"].children = [nodes["b"], nodes["e"], nodes["dc"]]
	nodes["d"].parents = [nodes["c"]]

	nodes["f"].children = [nodes["g"], nodes["e"], nodes["fc"]]
	nodes["f"].parents = [nodes["c"]]

	nodes["bc"].children = [nodes["a"]]
	nodes["bc"].parents = [nodes["b"]]

	nodes["gc"].children = [nodes["h"]]
	nodes["gc"].parents = [nodes["g"]]
	
	nodes["dc"].children = [nodes["b"], nodes["e"]]
	nodes["dc"].parents = [nodes["d"]]

	nodes["fc"].children = [nodes["g"], nodes["e"]]
	nodes["fc"].parents = [nodes["f"]]
	
	nodes["e"].children = [nodes["ec"]]
	nodes["e"].parents = [nodes["d"], nodes["c"], nodes["f"], \
								nodes["dc"], nodes["fc"]]

	nodes["ec"].children = []
	nodes["ec"].parents = [nodes["e"]]

	nodes["c"].children = [nodes["b"], nodes["d"], nodes["e"],\
							 	nodes["f"], nodes["g"]]

	root = nodes["c"]

	contact_lists = {}
	contact_lists["ab"] = [nodes["a"], nodes["b"]]
	contact_lists["hg"] = [nodes["h"], nodes["g"]]
	contact_lists["bc"] = [nodes["b"], nodes["c"]]
	contact_lists["gc"] = [nodes["g"], nodes["c"]]
	contact_lists["dc"] = [nodes["d"], nodes["c"]]
	contact_lists["fc"] = [nodes["f"], nodes["c"]]
	contact_lists["ec"] = [nodes["e"], nodes["c"]]

	return nodes, root, contact_lists, part_counts


def test_graph1(id_generator, parallelize=False):
	num_parts = 4
	part_counts = {'spindle block': 1, 'screws': 3}
	part_names = [next(id_generator) for i in range(num_parts)]
	# first part is spindle block
	nodes = {}
	nodes[part_names[0]] = Node(part_names[0], [], [], False, "spindle block")
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[part_names[0]]], True, "screw")

	nodes[part_names[0]].children = [nodes[part_names[i]] for i in range(1,4)]
	nodes[part_names[0]].parents = []

	root = nodes[part_names[0]]

	contact_lists = {}
	for i in range(1,4):
		contact_lists[part_names[i]] = [root]

	if parallelize:
		# parallelize the screwing
		screws = [nodes[i] for i in range(1,4)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(root, screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	return nodes, root, contact_lists, part_counts


def test_graph2(id_generator, parallelize=False):
	num_parts = 5
	part_counts = {"spindle block": 1, "support bracket": 1, "screws": 3}
	part_names = [next(id_generator) for i in range(num_parts)]
	# first part is spindle block
	nodes = {}
	spindle_block_id = part_names[0]
	support_bracket_id = part_names[1]

	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block")
	nodes[support_bracket_id] = Node(support_bracket_id, [], [], False, "support bracket")

	nodes[spindle_block_id].children = [nodes[support_bracket_id]]
	nodes[support_bracket_id].parents = [nodes[spindle_block_id]]

	for part in range(2,5):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id]], True, "screw")

	nodes[support_bracket_id].children = [nodes[part_names[i]] for i in range(2,5)]

	root = nodes[spindle_block_id]

	contact_lists = {}
	for i in range(2,5):
		contact_lists[part_names[i]] = [nodes[spindle_block_id], nodes[support_bracket_id]]

	if parallelize:
		# parallelize the screwing 
		screws = [nodes[i] for i in range(2,5)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(nodes[support_bracket_id], screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	return nodes, root, contact_lists, part_counts


"""
same as graph2 but without root node, used
for insertion into graph 1
"""
def test_graph1and2(id_generator, parallelize=False):
	num_parts = 8
	part_counts = {'spindle block': 1, 'support bracket': 1, 'screws': 6}
	part_names = [next(id_generator) for i in range(num_parts)]
	spindle_block_id = part_names[0]
	nodes = {}
	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block")

	# screws into spindle block
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[spindle_block_id]], True, "screw")

	nodes[spindle_block_id].children = [nodes[part_names[i]] for i in range(1,4)]
	nodes[spindle_block_id].parents = []

	root = nodes[spindle_block_id]

	contact_lists = {}
	for i in range(1,4):
		contact_lists[part_names[i]] = [nodes[spindle_block_id]]

	if parallelize:
		# parallelize the screwing
		screws = [nodes[i] for i in range(1,4)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(root, screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	support_bracket_id = part_names[4]
	nodes[support_bracket_id] = Node(support_bracket_id, [], [], False, "support bracket")

	# screws through support backet and spindle block
	for part in range(5,8):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id]], True, "screw")

	nodes[support_bracket_id].children = [nodes[part_names[i]] for i in range(5,8)]
	nodes[support_bracket_id].parents = [nodes[spindle_block_id]]
	nodes[spindle_block_id].children += [nodes[support_bracket_id]]

	for i in range(5,8):
		contact_lists[part_names[i]] = [nodes[spindle_block_id], nodes[support_bracket_id]]

	if parallelize:
		# parallelize the screwing 
		screws = [nodes[i] for i in range(5,8)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(nodes[support_bracket_id], screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	return nodes, root, contact_lists, part_counts



"""
same as graph2 but without root node, used
for insertion into graph 1
"""
def test_graph123(id_generator, parallelize=False):
	num_parts = 12
	# how many of each part type there is
	part_counts = {"spindle block": 1, "support bracket": 2, "screws": 9}

	part_names = [next(id_generator) for i in range(num_parts)]

	# graph 1 
	spindle_block_id = part_names[0]
	nodes = {}
	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block")

	# screws into spindle block
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[spindle_block_id]], True, "screw")

	nodes[spindle_block_id].children = [nodes[part_names[i]] for i in range(1,4)]
	nodes[spindle_block_id].parents = []

	root = nodes[spindle_block_id]

	contact_lists = {}
	for i in range(1,4):
		contact_lists[part_names[i]] = [nodes[spindle_block_id]]

	if parallelize:
		# parallelize the screwing
		screws = [nodes[i] for i in range(1,4)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(root, screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	# graph 2 - screws through support backet and spindle block
	support_bracket_id1 = part_names[4]
	nodes[support_bracket_id1] = Node(support_bracket_id1, [], [], False, "support bracket")

	for part in range(5,8):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id1]], True, "screw")

	nodes[support_bracket_id1].children = [nodes[part_names[i]] for i in range(5,8)]
	nodes[support_bracket_id1].parents = [nodes[spindle_block_id]]
	nodes[spindle_block_id].children += [nodes[support_bracket_id1]]

	for i in range(5,8):
		contact_lists[part_names[i]] = [nodes[support_bracket_id1], nodes[spindle_block_id]]

	if parallelize:
		# parallelize the screwing 
		screws = [nodes[i] for i in range(5,8)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(nodes[support_bracket_id1], screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	# graph 3 - other support bracket
	support_bracket_id2 = part_names[8]
	nodes[support_bracket_id2] = Node(support_bracket_id2, [], [], False, "support bracket")

	for part in range(9,12):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id2]], True, "screw")

	nodes[support_bracket_id2].children = [nodes[part_names[i]] for i in range(9,12)]
	nodes[support_bracket_id2].parents = [nodes[spindle_block_id]]
	nodes[spindle_block_id].children += [nodes[support_bracket_id2]]

	for i in range(9,12):
		contact_lists[part_names[i]] = [nodes[support_bracket_id2], nodes[spindle_block_id]]

	if parallelize:
		# parallelize the screwing 
		screws = [nodes[i] for i in range(9,12)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(nodes[support_bracket_id2], screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	return nodes, root, contact_lists, part_counts


	
"""
Full assembly steps 1,2,3, and 4
"""
def test_graph1234(id_generator, parallelize=False):
	num_parts = 15
	# how many of each part type there is
	part_counts = {
				"spindle block": 1, 
				"support bracket": 2,
				"screws": 11,
				"backing plate": 1}

	part_names = [next(id_generator) for i in range(num_parts)]

	# graph 1 
	spindle_block_id = part_names[0]
	nodes = {}
	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block")

	# screws into spindle block
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[spindle_block_id]], True, "screw")

	nodes[spindle_block_id].children = [nodes[part_names[i]] for i in range(1,4)]
	nodes[spindle_block_id].parents = []

	root = nodes[spindle_block_id]

	contact_lists = {}
	for i in range(1,4):
		contact_lists[part_names[i]] = [nodes[spindle_block_id]]

	if parallelize:
		# parallelize the screwing
		screws = [nodes[i] for i in range(1,4)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(root, screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	# graph 2 - screws through support backet and spindle block
	support_bracket_id1 = part_names[4]
	nodes[support_bracket_id1] = Node(support_bracket_id1, [], [], False, "support bracket")

	for part in range(5,8):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id1]], True, "screw")

	nodes[support_bracket_id1].children = [nodes[part_names[i]] for i in range(5,8)]
	nodes[support_bracket_id1].parents = [nodes[spindle_block_id]]
	nodes[spindle_block_id].children += [nodes[support_bracket_id1]]

	for i in range(5,8):
		contact_lists[part_names[i]] = [nodes[support_bracket_id1], nodes[spindle_block_id]]

	if parallelize:
		# parallelize the screwing 
		screws = [nodes[i] for i in range(5,8)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(nodes[support_bracket_id1], screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node

	# graph 3 - other support bracket
	support_bracket_id2 = part_names[8]
	nodes[support_bracket_id2] = Node(support_bracket_id2, [], [], False, "support bracket")

	for part in range(9,12):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id2]], True, "screw")

	nodes[support_bracket_id2].children = [nodes[part_names[i]] for i in range(9,12)]
	nodes[support_bracket_id2].parents = [nodes[spindle_block_id]]
	nodes[spindle_block_id].children += [nodes[support_bracket_id2]]

	for i in range(9,12):
		contact_lists[part_names[i]] = [nodes[support_bracket_id2], nodes[spindle_block_id]]

	if parallelize:
		# parallelize the screwing 
		screws = [nodes[i] for i in range(9,12)]
		parallel_screws_id = next(id_generator)
		parallelized_screws_node = parallelize_op(nodes[support_bracket_id2], screws, parallel_screws_id, contact_lists)
		for screw in screws:
			del nodes[screw.ID]
		nodes[parallel_screws_id] = parallelized_screws_node


	# graph 4 - backing plate
	backing_plate_id = part_names[12]
	nodes[backing_plate_id] = Node(backing_plate_id, [], [], False, "backing plate")
	
	# one screw goes into each support bracket through to the backing plate	
	nodes[part_names[13]] = Node(part_names[13], [], [nodes[support_bracket_id1], nodes[backing_plate_id]], True, "screw")
	nodes[part_names[14]] = Node(part_names[14], [], [nodes[support_bracket_id2], nodes[backing_plate_id]], True, "screw")
	nodes[backing_plate_id].children = [nodes[part_names[13]], nodes[part_names[14]]]

	nodes[support_bracket_id1].children += [nodes[part_names[13]]]
	nodes[support_bracket_id2].children += [nodes[part_names[14]]]

	# backing plate touches spindle block and both support brackets
	nodes[backing_plate_id].parents = [nodes[spindle_block_id], nodes[support_bracket_id1], nodes[support_bracket_id2]]

	nodes[spindle_block_id].children += [nodes[backing_plate_id]]
	nodes[support_bracket_id1].children += [nodes[backing_plate_id]]
	nodes[support_bracket_id2].children += [nodes[backing_plate_id]]

	# screw goes through support bracket to backing plate
	contact_lists[part_names[13]] = [nodes[support_bracket_id1], nodes[backing_plate_id]]
	contact_lists[part_names[14]] = [nodes[support_bracket_id2], nodes[backing_plate_id]]

	return nodes, root, contact_lists, part_counts



if __name__ == "__main__":

	class IDGen:
		def __init__(self, n):
			self.n = n
		def __iter__(self):
			return self
		def __next__(self):
			result = self.n
			self.n += 1
			return result

	nodes, root, contact_lists, part_counts = test_graph0()
	attached_part_counts = init_attached_part_counts(part_counts)

	# check graph was built correctly 
	for node_name, node in nodes.items():
		for parent in node.parents:
			assert node in parent.children, f"node {node_name} has parent {parent.ID} but {parent.ID} does not have {node_name} as child"
	
		for child in node.children:
			assert node in child.parents, f"node {node_name} has child {child.ID} but {child.ID} does not have {node_name} as parent"

	program = build_program(root, nodes, contact_lists, part_counts)
	print_program(program, part_counts, attached_part_counts)
	
	print('#############################')
	print(f"testing on sample diagram 1 without parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists, part_counts = test_graph1(id_generator, parallelize=False)
	attached_part_counts = init_attached_part_counts(part_counts)

	for node_name, node in nodes.items():
		for parent in node.parents:
			assert node in parent.children, f"node {node_name} has parent {parent.ID} but {parent.ID} does not have {node_name} as child"
	
		for child in node.children:
			assert node in child.parents, f"node {node_name} has child {child.ID} but {child.ID} does not have {node_name} as parent"

	program = build_program(root, nodes, contact_lists, part_counts)
	print_program(program, part_counts, attached_part_counts)

	print(f"testing on sample diagram 1 with parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists, part_counts = test_graph1(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	program = build_program(root, nodes, contact_lists, part_counts)
	print_program(program, part_counts, attached_part_counts)

	print('#############################')
	print(f"testing on sample diagram 2 without parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists, part_counts = test_graph2(id_generator, parallelize=False)
	attached_part_counts = init_attached_part_counts(part_counts)

	for node_name, node in nodes.items():
		for parent in node.parents:
			assert node in parent.children, f"node {node_name} has parent {parent.ID} but {parent.ID} does not have {node_name} as child"
	
		for child in node.children:
			assert node in child.parents, f"node {node_name} has child {child.ID} but {child.ID} does not have {node_name} as parent"

	program = build_program(root, nodes, contact_lists, part_counts)
	print_program(program, part_counts, attached_part_counts)

	print(f"testing on sample diagram 2 with parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists, part_counts = test_graph2(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	program = build_program(root, nodes, contact_lists, part_counts)
	print_program(program, part_counts, attached_part_counts)

	print('#############################')
	print(f"testing graphs 1 and 2 combined:")
	id_generator = IDGen(0)

	nodes, root, contact_lists, part_counts = test_graph1and2(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	program = build_program(root, nodes, contact_lists, part_counts)
	print_program(program, part_counts, attached_part_counts)

	print('#############################')
	print(f"testing graphs 1, 2, and 3 combined:")
	id_generator = IDGen(0)

	nodes, root, contact_lists, part_counts = test_graph123(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	visited = [root.ID]
	order = [root]
	greedy_order(root, visited, order, fasteners_first)

	program = build_program(root, nodes, contact_lists, part_counts, order)
	print_program(program, part_counts, attached_part_counts)


	print('#############################')
	print(f"testing graphs 1, 2, 3, and 4 combined:")
	id_generator = IDGen(0)

	nodes, root, contact_lists, part_counts = test_graph1234(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	visited = [root.ID]
	order = [root]
	greedy_order(root, visited, order, fasteners_first)

	program = build_program(root, nodes, contact_lists, part_counts, order)
	print_program(program, part_counts, attached_part_counts)


