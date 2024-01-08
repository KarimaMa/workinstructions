from grammar import *


def test_graph0():
	# make all the nodes first with empty fields
	part_names = ["a", "b", "c", "d", "e", "f", "g", "h"]
	fastener_names = ["ab", "hg", "bc", "dc", "ec", "fc", "gc"]
	part_counts = {"block": len(part_names), "screw": len(fastener_names)}

	nodes = {}
	for name in part_names:
		nodes[name] = Node(name, [], [], False, "block", False)
	for name in fastener_names:
		nodes[name] = Node(name, [], [], True, "screw", False)

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
	nodes[part_names[0]] = Node(part_names[0], [], [], False, "spindle block", True)
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[part_names[0]]], True, "screw", False)

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

	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block", True)
	nodes[support_bracket_id] = Node(support_bracket_id, [], [], False, "support bracket", True)

	nodes[spindle_block_id].children = [nodes[support_bracket_id]]
	nodes[support_bracket_id].parents = [nodes[spindle_block_id]]

	for part in range(2,5):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id]], True, "screw", False)

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
	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block", True)

	# screws into spindle block
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[spindle_block_id]], True, "screw", False)

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
	nodes[support_bracket_id] = Node(support_bracket_id, [], [], False, "support bracket", True)

	# screws through support backet and spindle block
	for part in range(5,8):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id]], True, "screw", False)

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
	part_counts = {"spindle block": 1, "left support bracket": 1, "right support bracket": 1, "screws": 9}

	part_names = [next(id_generator) for i in range(num_parts)]

	# graph 1 
	spindle_block_id = part_names[0]
	nodes = {}
	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block", True)

	# screws into spindle block
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[spindle_block_id]], True, "screw", False)

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
	nodes[support_bracket_id1] = Node(support_bracket_id1, [], [], False, "left support bracket", True)

	for part in range(5,8):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id1]], True, "screw", False)

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
	nodes[support_bracket_id2] = Node(support_bracket_id2, [], [], False, "right support bracket", True)

	for part in range(9,12):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id2]], True, "screw", False)

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
				"left support bracket": 1,
				"right support bracket": 1,
				"screws": 11,
				"backing plate": 1}

	part_names = [next(id_generator) for i in range(num_parts)]

	# graph 1 
	spindle_block_id = part_names[0]
	nodes = {}
	nodes[spindle_block_id] = Node(spindle_block_id, [], [], False, "spindle block", True)

	# screws into spindle block
	for part in range(1,4):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[spindle_block_id]], True, "screw", False)

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
	nodes[support_bracket_id1] = Node(support_bracket_id1, [], [], False, "left support bracket", True)

	for part in range(5,8):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id1]], True, "screw", False)

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
	nodes[support_bracket_id2] = Node(support_bracket_id2, [], [], False, "right support bracket", True)

	for part in range(9,12):	
		nodes[part_names[part]] = Node(part_names[part], [], [nodes[support_bracket_id2]], True, "screw", False)

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
	nodes[backing_plate_id] = Node(backing_plate_id, [], [], False, "backing plate", True)
	
	# one screw goes into each support bracket through to the backing plate	
	nodes[part_names[13]] = Node(part_names[13], [], [nodes[support_bracket_id1], nodes[backing_plate_id]], True, "screw", False)
	nodes[part_names[14]] = Node(part_names[14], [], [nodes[support_bracket_id2], nodes[backing_plate_id]], True, "screw", False)
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
	nodes, root, contact_lists, part_counts = test_graph0()
	attached_part_counts = init_attached_part_counts(part_counts)

	# check graph was built correctly 
	for node_name, node in nodes.items():
		for parent in node.parents:
			assert node in parent.children, f"node {node_name} has parent {parent.ID} but {parent.ID} does not have {node_name} as child"
	
		for child in node.children:
			assert node in child.parents, f"node {node_name} has child {child.ID} but {child.ID} does not have {node_name} as parent"

	program = build_program(root, nodes, contact_lists, part_counts)
	program_str = get_program_str(program)
	print(program_str)
	
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
	program_str = get_program_str(program)

	print(f"testing on sample diagram 1 with parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists, part_counts = test_graph1(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	program = build_program(root, nodes, contact_lists, part_counts)
	program_str = get_program_str(program)
	print(program_str)

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
	program_str = get_program_str(program)
	print(program_str)

	print(f"testing on sample diagram 2 with parallelization")
	id_generator = IDGen(0)
	nodes, root, contact_lists, part_counts = test_graph2(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	program = build_program(root, nodes, contact_lists, part_counts)
	program_str = get_program_str(program)
	print(program_str)

	print('#############################')
	print(f"testing graphs 1 and 2 combined:")
	id_generator = IDGen(0)

	nodes, root, contact_lists, part_counts = test_graph1and2(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	program = build_program(root, nodes, contact_lists, part_counts)
	program_str = get_program_str(program)
	print(program_str)

	print('#############################')
	print(f"testing graphs 1, 2, and 3 combined:")
	id_generator = IDGen(0)

	nodes, root, contact_lists, part_counts = test_graph123(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	visited = [root.ID]
	order = [root]
	greedy_order(root, visited, order, fasteners_first)

	program = build_program(root, nodes, contact_lists, part_counts, order)
	program_str = get_program_str(program)
	print(program_str)

	print('#############################')
	print(f"testing graphs 1, 2, 3, and 4 combined:")
	id_generator = IDGen(0)

	nodes, root, contact_lists, part_counts = test_graph1234(id_generator, parallelize=True)
	attached_part_counts = init_attached_part_counts(part_counts)

	visited = [root.ID]
	order = [root]
	greedy_order(root, visited, order, fasteners_first)

	program = build_program(root, nodes, contact_lists, part_counts, order)
	program_str = get_program_str(program)
	print(program_str)

	print('#############################')
	print(f"testing automatic parallelization detection using graphs 1,2,3,4:")
	id_generator = IDGen(0)

	nodes, root, contact_lists, part_counts = test_graph1234(id_generator, parallelize=False)
	parallelize_where_possible(root, contact_lists, nodes, id_generator)
	id2node_map = {}
	get_ID2node_map(root, id2node_map)

	attached_part_counts = init_attached_part_counts(part_counts)

	visited = [root.ID]
	order = [root]
	greedy_order(root, visited, order, fasteners_first)

	program = build_program(root, id2node_map, contact_lists, part_counts, order)
	program_str = get_program_str(program)
	print(program_str)


