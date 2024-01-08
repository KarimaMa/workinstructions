"""
injests json dissassembly info and converts to graph
"""
import json
from grammar import *


def infer_part_type_from_name(name):
	name = name.split("_")[0]
	# our VERY naive inference rule is that if the part name 
	# starts with a number then it is a screw - this will 
	# obviously break in the future
	if name[0].isdigit():
		return "screw"
	else:
		return name

def json2graph(json_file):
	with open(json_file, "r") as f:
		data = json.load(f)

	id2node_map = {}
	for node_info in data:
		nodeID = node_info["id"]
		# most often for now, the part type will be missing because
		# we don't have classifiers yet - instead try to infer the 
		# part type from the part name
		part_type = infer_part_type_from_name(node_info["name"])
		is_fastener = node_info["is_fastener"]
		new_node = Node(nodeID, [], [], is_fastener, part_type, None)
		id2node_map[nodeID] = new_node

	root = None
	contact_lists = {}
	part_counts = {}

	for node_info in data:
		nodeID = node_info["id"]
		node = id2node_map[nodeID]
		node.children = [id2node_map[c] for c in node_info["children"]]
		node.parents = [id2node_map[p] for p in node_info["parents"]]

		if len(node.parents) == 0:
			root = node

		if node.is_fastener:
			contact_lists[nodeID] = [id2node_map[part] for part in node_info["fastened_parts"]]
			for i, part in enumerate(contact_lists[nodeID][:-1]):
				assert all([other_part not in part.children for other_part in contact_lists[nodeID][i+1:]])

		if node.part_type in part_counts:
			part_counts[node.part_type] += 1
		else:
			part_counts[node.part_type] = 1

	for nodeID, node in id2node_map.items():
		node.is_unique = (part_counts[node.part_type] == 1)

	return root, id2node_map, contact_lists, part_counts


if __name__ == "__main__":
	root, id2node_map, contact_lists, part_counts = json2graph("assembly_info.json")
	id_generator = IDGen(len(id2node_map))

	parallelize_where_possible(root, contact_lists, id2node_map, id_generator)
	# make a new id2node map after parallelization to remove nodes merged 
	# via parallelization and add new parallel node
	id2node_map = {} 
	get_ID2node_map(root, id2node_map)


	visited = [root.ID]
	order = [root]
	greedy_order(root, visited, order, fasteners_first)

	program = build_program(root, id2node_map, contact_lists, part_counts, order)
	program_str = get_program_str(program)
	print(program_str)


