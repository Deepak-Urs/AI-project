import time
import copy
import heapq as heap  # For queueing

#Main function for taking inputs regarding mode of puzzle
def main():
	print('Choose an option: \n')
	print('1 - Create your own custom puzzle or 2 - Default puzzle -- !\n')

	choice = input()

	if (choice == '1'):
		mode_customized()
	elif (choice == '2'):
		mode_default()
	else:
		print('Choose a valid option!\n')
		main()

def search_function_choice(begin_state, end_state):

	print('Please select the search method you like to utilize :\n')

	print('1 - Uniform Cost Search\n')
	print('2 - A* (Manhattan Distance heuristic)\n')
	print('3 - A* (Misplaced Tile Heuristic)\n')

	class_search = input()

	if (class_search > str(0) and class_search < str(4)):
		# Referred: https://docs.python.org/3/library/time.html#module-time
		start = time.process_time()
		calculate_main_search_algo(begin_state, end_state, class_search)
		res = time.process_time() - start
		print('Computationally: ', time.process_time() - start, 'ms utilized!\n')
		if round(res, 3) == 0.000:
			print('Logically, we have less than 0 ms utilized!\n')
		else:
			print('Logically, we have', round(res, 3), 'ms utilized!\n')

	else:
		print('Enter a valid choice!\n')
		print('To return to the main menu, enter 1.\n Press 2 to go back to the default mode menu.\n Press any other key to restart the search method menu.\n')

		incorrect_input_2 = input()

		if (incorrect_input_2 == '1'):
			main()
		elif (incorrect_input_2 == '2'):
			mode_default()
		else:
			search_function_choice(begin_state, end_state)

def calculate_main_search_algo(begin_state, end_state, class_search):

	# Making a root node from the starting state
	priority_queue = []
	first_parent = Node(curr_state=begin_state)
	
	# Add the first node to our heap
	heap.heappush(priority_queue, first_parent)

	#As we have already included the root in the priority_queue.
	queues_max_nodes = 1
	# As no node has been expanded thus far.
	nodes_expanded_count = 0

	states_visited = []

	while (priority_queue):

		if queues_max_nodes < len(priority_queue):
			queues_max_nodes = len(priority_queue)

		present_node = heap.heappop(priority_queue)

		print('The optimal state to expand with a cost function of g(n) = ', str(
			int(present_node.g)), 'and h(n) = ', str(int(present_node.g)), 'is : \n')

		present_node_state = present_node.curr_state
		for value in present_node_state:
			print('[', *value, ']')

		# Assuming this is our desired end state.
		if (equal_state(present_node_state, end_state)):
			print('A solution detected! The nodes and their expansion order is as follows: \n')
			present_node.print_nodes_traced()
			print('The maximum number of elements in the priority_queue: ', queues_max_nodes,
			      'with the number of nodes expanded: ', nodes_expanded_count, '\n')
			return nodes_expanded_count, queues_max_nodes

		else:
			# Add the current state to the list of states we have already checked
			states_visited.append(present_node)
			collection_child = present_node.tile_operators()

			# Remove null values from this list (if any) and if there are no other values in list, continue
			# Referred https://www.geeksforgeeks.org/python-remove-none-values-from-list/
			updated_collection_child = [value for value in collection_child if value]

			if (updated_collection_child == []):
				continue

			for stateofnewchild in updated_collection_child:
				child_new = Node(curr_state=stateofnewchild, g=0, h=0)

				# we can simply proceed without performing any additional calculations for this node, If this new child node already exists in our priority_queue or has already been visited.
				# Clipping the Repeated states
				if (priority_queue and child_new in priority_queue):
					continue
				elif (states_visited and child_new in states_visited):
					continue
				else:
					# Case: 1 Uniform Cost Search
					if (class_search == str(1)):
						child_new.h = 0  
					# Case 2: Manhattan Distance heuristic with A*
					elif (class_search == str(2)):
						child_new.h = distance_manhattan(child_new.curr_state, end_state)
					else:
						# Case 3: Misplaced Tile heuristic with A*
						child_new.h = count_misplaced_tiles(child_new.curr_state, end_state)  

				present_node.append_child_node_pseudo(node=child_new)

				heap.heappush(priority_queue, child_new)

			nodes_expanded_count += 1

	print('No available solutions.\n')
	return False

def equal_state(state1, state2):
    # Flatten the list of lists for easy comparison
    result_list1 = [value for val in state1 for value in val]
    result_list2 = [value for val in state2 for value in val]

    return result_list1 == result_list2

class Node:

	def __init__(self, curr_state=0, parent=None, h=0, g=0):
		# In this context, where 'h' represents the cost to reach the goal, 'g' represents the cost from the start, and 'curr_state' signifies the current state of the puzzle.
		self.h = h
		self.g = g

		# The puzzle's current state undergoes modifications after each operation.
		self.curr_state = curr_state
		self.parent = parent 
		self.children = []

	# In this case, the cost of 1 refers to the cost associated with expanding this particular node.
	def append_child_node_pseudo(self, node, cost=1):
        # Increase the child's cost from the starting point.
		node.g = self.g + cost
		self.children.append(node)
		node.parent = self

	# display and calculate the number of nodes traversed until the result is reached. This is achieved by utilizing the parent node of each selected child.
	def print_nodes_traced(self):
		x = self
		trace = 0

		while (x):
			print(x.curr_state)
			trace += 1
			x = x.parent

		print('The count of nodes traced. : ', trace, '\n')

	#Referred https://stackoverflow.com/questions/7803121/in-python-heapq-heapify-doesnt-take-cmp-or-key-functions-as-arguments-like-sor/7803240#7803240
	#Function to compare costs of two nodes, used to sort nodes in the heap by cost
	def __lt__(self, other):
		return other.g + other.h > self.g + self.h

	#Function to calculate the total f value as h+g
	def f_calculator(self):
		return (self.g + self.f)

	#Like lt function, this is used to compare equality of nodes in the heap
	def __eq__(self, other):
		return self.curr_state == other.curr_state

	#Function to define movements of the 0 tile
	def tile_operators(self):
		correct_states = []
		puzzle = self.curr_state

		#Variables to depict coordinates of 0 in the puzzle - initialised as 0,0
		p = 0
		q = 0

		#Find the coordinates of 0 in the 2D array

		for i in range(0, len(puzzle)):
			for j in range(0, len(puzzle)):
				if (puzzle[i][j] == 0):
					p = i
					q = j
					break

		# left operation move
		if (q != 0):
			newstate = copy.deepcopy(puzzle)
			newstate[p][q] = newstate[p][q-1]
			newstate[p][q-1] = 0

        	#Check if this state is same as it's parent, parent is not null and add only if false
			if (self.parent and equal_state(newstate, self.parent.curr_state)):
				correct_states.append(None)
			else:
				correct_states.append(newstate)

        # up operation move
		if (p != 0):
			newstate = copy.deepcopy(puzzle)
			newstate[p][q] = newstate[p-1][q]
			newstate[p-1][q] = 0

			if (self.parent and equal_state(newstate, self.parent.curr_state)):
				correct_states.append(None)
			else:
				correct_states.append(newstate)

        # Right operation move
		if (q != (len(puzzle)-1)):
			newstate = copy.deepcopy(puzzle)
			newstate[p][q] = newstate[p][q+1]
			newstate[p][q+1] = 0
			if (self.parent and equal_state(newstate, self.parent.curr_state)):
				correct_states.append(None)
			else:
				correct_states.append(newstate)

        # Down operation move
		if (p != (len(puzzle)-1)):
			newstate = copy.deepcopy(puzzle)
			newstate[p][q] = newstate[p+1][q]
			newstate[p+1][q] = 0

			if (self.parent and equal_state(newstate, self.parent.curr_state)):
				correct_states.append(None)
			else:
				correct_states.append(newstate)

		return correct_states

def distance_manhattan(begin_state, end_state):
	heuristic = 0

	# Employing three iterations: The initial iteration encompasses traversing all the elements within the 2D array, while the subsequent two iterations serve the purpose of extracting the positions of each element.
	for i in range(1, len(begin_state)*len(begin_state[0])):
		for j in range(0, len(begin_state)):
			for k in range(0, len(begin_state)):
				if (i == begin_state[j][k]):
					start_row = j
					start_col = k
				if (i == end_state[j][k]):
					final_row = j
					final_col = k

		heuristic += (abs(final_row - start_row) + abs(final_col - start_col))

	return heuristic


def count_misplaced_tiles(begin_state, end_state):
	heuristic = 0
	for i in range(0, len(begin_state)):
		for j in range(0, len(begin_state)):
			if (begin_state[i][j] != 0 and begin_state[i][j] != end_state[i][j]):
				heuristic += 1

	return heuristic

def mode_customized():
	print('For the puzzle, Input the puzzle_size (rows size = columns size) :\n')

	puzzle_size = int(input())

	custom_input = []

	# Generating and setting up the custom end state by utilizing these links:
	# https://stackoverflow.com/questions/20114349/incrementing-values-in-2d-array/20114599#20114599
	end_state = [[(j + 1) + (puzzle_size * i) for j in range(puzzle_size)]
                for i in range(puzzle_size)]
	end_state[puzzle_size-1][puzzle_size-1] = 0

	print('Goal state (Customized) for puzzle (',  puzzle_size, 'x', puzzle_size, ' ) is: \n')
	for st in end_state:
		print('[', *st, ']')

	if (puzzle_size > 0):
		print('**** INPUT INDIVIDUAL NUMBERS WITH A SPACE ****')
		for value in range(1, puzzle_size+1):
			print('Input row value: ', str(value))
			val = input()
			val = [int(i) for i in val.split()]
			custom_input.append(val)

		search_function_choice(custom_input, end_state)

	else:
		print('Input valid value!')
		mode_customized()

#Function for choosing a puzzle from the pre-defined ones 
def mode_default():

	#For the default mode, goal state is 3x3 and can be pre-defined
	end_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

	trivial = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
	easy = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
	medium = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
	challenging = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
	hard = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
	difficult = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]

	print('Default options available :\n')
	print('1 - trivial : ')
	for value in trivial:
		print('[', *value, ']')

	print('\n2 - easy : ')
	for value in easy:
		print('[', *value, ']')

	print('\n3 - medium : ')
	for value in medium:
		print('[', *value, ']')

	print('\n4 - challenging : ')
	for value in challenging:
		print('[', *value, ']')

	print('\n5 - hard : ')
	for value in hard:
		print('[', *value, ']')

	print('\n6 - difficult : ')
	for value in difficult:
		print('[', *value, ']')

	mode_default = input()

	if (mode_default == '1'):
		#Storing the value of user chosen list in an empty list called 'begin_state'
		begin_state = trivial
	elif (mode_default == '2'):
		begin_state = easy
	elif (mode_default == '3'):
		begin_state = medium
	elif (mode_default == '4'):
		begin_state = challenging
	elif (mode_default == '5'):
		begin_state = hard
	elif (mode_default == '6'):
		begin_state = difficult
	else:
		print('Enter a valid input!! \n Enter 1 -> For Main Menu \n (Any other key -> To restart the default mode menu!)')
		incorrect_input = input()

		if (incorrect_input == '1'):
			main()
		else:
			mode_default()

	search_function_choice(begin_state, end_state)


main()