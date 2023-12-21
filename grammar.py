"""
simple starting grammar for work instructions
there are two types of actions:
1) placement actions
2) attachment actions

placement_op := <part 1> <part 2>
parts are sorted in contact order
attachment_op := <fastener> <part 1> ... <part n>
"""

class PlacementOp:
	def __init__(self, part, parts_in_contact):
		self.part = part
		self.parts_in_contact = parts_in_contact

	def print(self):
		if len(self.parts_in_contact) != 0:
			parts_in_contact_str = ", ".join([str(part.part_type) + ' ' + str(part.ID) for part in self.parts_in_contact])
			print(f"align {self.part.part_type} {self.part.ID} with {parts_in_contact_str}")
		else:
			print(f"position {self.part.part_type} {self.part.ID} for assembly")

# parallelized_parts are all placed in the same way 
# relative to parts_in_contact
class ParallelPlacementOp:
	def __init__(self, parallelized_parts, parts_in_contact):
		self.parallelized_parts = parallelized_parts
		self.parts_in_contact = parts_in_contact

	def print(self):
		if len(self.parts_in_contact) != 0:
			parts_in_contact_str = ", ".join([str(part.part_type) + ' ' + str(part.ID) for part in self.parts_in_contact])
			parallelized_parts_str = ', '.join([str(part.part_type) + ' ' + str(part.ID) for part in self.parallelized_parts])
			print(f"align {parallelized_parts_str} with {parts_in_contact_str}")
		else:
			print(f"position {parallelized_parts_str} for assembly")


class AttachmentOp:
	def __init__(self, fastener, parts):
		self.fastener = fastener
		self.parts = parts

	def print(self):
		if self.fastener.part_type == "screw":
			action_str = "screw"
		else:
			raise Exception(f"unknown fastener type {self.fastener.part_type}")

		first_part_str = f"{self.parts[0].part_type} {self.parts[0].ID}"
		other_parts_str = ",".join([str(part.part_type) + ' ' + str(part.ID) for part in self.parts[1:]])
		if len(self.parts[1:]) == 1:
			print(f"{action_str} {first_part_str} to {other_parts_str}")
		else:
			print(f"{action_str} through {','.join([str(part.part_type)+''+str(part.ID) for part in self.parts])}")

# fasteners are all fastened in the same way to the the list of parts
class ParallelAttachmentOp:
	def __init__(self, parallelized_fasteners, parts):
		self.parallelized_fasteners = parallelized_fasteners
		self.parts = parts

	def print(self):
		fastener_type = self.parallelized_fasteners[0].part_type
		if fastener_type == "screw":
			action_str = "screw"
			fasteners_str = ', '.join([str(part.part_type) + ' ' + str(part.ID) for part in self.parallelized_fasteners])
		else:
			raise Exception(f"unknown fastener type {fastener_type}")

		first_part_str = f"{self.parts[0].part_type} {self.parts[0].ID}"
		other_parts_str = ",".join([str(part.part_type) + ' ' + str(part.ID) for part in self.parts[1:]])

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


def get_node2ID_map(node, node2ID_map):
	for child in node.children:
		if not child in node2ID_map:
			node2ID_map[child.ID] = child
			get_node2ID_map(child, node2ID_map)

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
Program is just an ordered list of statements
since it doesn't seem to need more complicated 
structure like an AST for now
"""
def build_program(DA_dag, node2ID_map, contact_lists):
	node_levels = {}
	levels_dict = {}
	topological_sort(DA_dag, node_levels, levels_dict)
	max_level = max(levels_dict.keys())

	program = []

	for level in range(max_level,-1,-1):
		levelIDs = levels_dict[level]
		if level == max_level:
			top_node = node2ID_map[levelIDs[0]]
			assert len(levelIDs) == 1 and len(top_node.parents) == 0
			statement = PlacementOp(top_node, [])
			program += [statement]
		else:
			for nodeID in levelIDs:
				node = node2ID_map[nodeID]

				if node.is_fastener:
					parts_touching = contact_lists[nodeID]
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



	return program


def print_program(program):
	for statement in program:
		statement.print()



def test_graph0():
	# make all the nodes first with empty fields
	part_names = ["a", "b", "c", "d", "e", "f", "g", "h"]
	fastener_names = ["ab", "hg", "bc", "dc", "ec", "fc", "gc"]

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

	return nodes, root, contact_lists


def test_graph1(id_generator, parallelize=False):
	num_parts = 4
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

	return nodes, root, contact_lists


def test_graph2(id_generator, parallelize=False):
	num_parts = 5
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

	return nodes, root, contact_lists


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

	nodes, root, contact_lists = test_graph0()
	# check graph was built correctly 
	for node_name, node in nodes.items():
		for parent in node.parents:
			assert node in parent.children, f"node {node_name} has parent {parent.ID} but {parent.ID} does not have {node_name} as child"
	
		for child in node.children:
			assert node in child.parents, f"node {node_name} has child {child.ID} but {child.ID} does not have {node_name} as parent"

	program = build_program(root, nodes, contact_lists)
	print_program(program)
	
	print('#############################')
	print(f"testing on sample diagram 1 without parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists = test_graph1(id_generator, parallelize=False)
	for node_name, node in nodes.items():
		for parent in node.parents:
			assert node in parent.children, f"node {node_name} has parent {parent.ID} but {parent.ID} does not have {node_name} as child"
	
		for child in node.children:
			assert node in child.parents, f"node {node_name} has child {child.ID} but {child.ID} does not have {node_name} as parent"

	program = build_program(root, nodes, contact_lists)
	print_program(program)

	print(f"testing on sample diagram 1 with parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists = test_graph1(id_generator, parallelize=True)
	program = build_program(root, nodes, contact_lists)
	print_program(program)

	print('#############################')
	print(f"testing on sample diagram 2 without parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists = test_graph2(id_generator, parallelize=False)
	for node_name, node in nodes.items():
		for parent in node.parents:
			assert node in parent.children, f"node {node_name} has parent {parent.ID} but {parent.ID} does not have {node_name} as child"
	
		for child in node.children:
			assert node in child.parents, f"node {node_name} has child {child.ID} but {child.ID} does not have {node_name} as parent"

	program = build_program(root, nodes, contact_lists)
	print_program(program)

	print(f"testing on sample diagram 2 with parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists = test_graph2(id_generator, parallelize=True)
	program = build_program(root, nodes, contact_lists)
	print_program(program)



