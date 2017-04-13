import sys, time

class State():
	def __init__(self, lhs, rhs, states = []):
		self.lhs = lhs
		self.rhs = rhs
		self.states = states

	def is_initial(self):
		return self.lhs['C'] == 0 and self.lhs['M'] == 0 and self.lhs['B'] == 0

	def is_valid(self):
		return self.lhs['C'] >= 0 and self.rhs['C'] >= 0 and \
			   self.lhs['M'] >= 0 and self.rhs['M'] >= 0 and \
			   (self.lhs['M'] >= self.lhs['C'] or self.lhs['M'] == 0) and \
			   (self.rhs['M'] >= self.rhs['C'] or self.rhs['M'] == 0)

	def is_goal(self, goal):
		return self.rhs['C'] == goal.fetch_rhs()['C'] and \
			   self.rhs['B'] == goal.fetch_rhs()['B'] and \
			   self.rhs['M'] == goal.fetch_rhs()['M']

	def on_left(self):
		return self.lhs['B'] == 1 and self.rhs['B'] == 0
		
	def on_right(self):
		return self.lhs['B'] == 0 and self.rhs['B'] == 1
		
	def store_states(self, states):
		self.states = states

	def load_states(self):
		return self.states

	def fetch_lhs(self):
		return self.lhs

	def fetch_rhs(self):
		return self.rhs

def func_read_file(name):
	fp = open(name, 'r');
	lines = fp.readlines();
	fp.close();
	lhs = lines[0].rstrip().split(',')
	rhs = lines[1].rstrip().split(',')
	return {'M': int(lhs[0]), 'C': int(lhs[1]), 'B': int(lhs[2])}, {'M': int(rhs[0]), 'C': int(rhs[1]), 'B': int(rhs[2])}

def func_write_file(name, result):
	fp = open(name, 'w+')
	fp.write('\n'.join(result))
	fp.close()

def func_move_one(lhs, rhs, which, count, flag):
	if flag:
		lhs[which] += count
		lhs['B'] = 1
		rhs[which] -= count
		rhs['B'] = 0
		return State(lhs, rhs)
	else:
		lhs[which] -= count
		lhs['B'] = 0
		rhs[which] += count
		rhs['B'] = 1
		return State(lhs, rhs)

def func_move_two(lhs, rhs, flag):
	if flag:
		lhs['C'] += 1
		lhs['B'] = 1
		lhs['M'] += 1
		rhs['C'] -= 1
		rhs['B'] = 0
		rhs['M'] -= 1
		return State(lhs, rhs)
	else:
		lhs['C'] -= 1
		lhs['B'] = 0
		lhs['M'] -= 1
		rhs['C'] += 1
		rhs['B'] = 1
		rhs['M'] += 1
		return State(lhs, rhs)

def func_build_successor(state):
	states, flag = [], state.on_right()

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'C', 2, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'C', 1, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_two(lhs, rhs, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'M', 1, flag)
	if new_state.is_valid():
		states.append(new_state)

	lhs, rhs = state.fetch_lhs().copy(), state.fetch_rhs().copy()
	new_state = func_move_one(lhs, rhs, 'M', 2, flag)
	if new_state.is_valid():
		states.append(new_state)

	return states

def func_dfs_search(state, goal):
	state_stack, state_explore = [], []	
	state_stack.append(state)
	
	while state_stack:
		tmp_state = state_stack.pop()
		if tmp_state.is_goal(goal):
			return tmp_state
		successor = func_build_successor(tmp_state)
		tmp_state.store_states(successor)
		if tmp_state not in state_explore:
			state_explore.append(tmp_state)
			for item in successor:
				if (item not in state_explore) and (not item.is_initial()):
					state_stack.append(item)

	return None

def func_bfs_search(state, goal):
	state_stack, state_explore = [], []	
	state_stack.append(state)
	
	while state_stack:
		tmp_state = state_stack.pop(0)
		if tmp_state.is_goal(goal):
			return tmp_state
		successor = func_build_successor(tmp_state)
		tmp_state.store_states(successor)
		if tmp_state not in state_explore:
			state_explore.append(tmp_state)
			for item in successor:
				if (item not in state_explore) and (not item.is_initial()):
					state_stack.append(item)
		
	return None
	
def func_print_state(state):
	print 'LHS:', state.fetch_lhs(), '<--->', 'RHS:', state.fetch_rhs()
	for item in state.load_states():
		print 'LHS:', item.fetch_lhs(), '<--->', 'RHS:', item.fetch_rhs()
	print

def func_print_string(tree, result = []):
	lhs = '(' + ','.join([str(value) for value in tree.fetch_lhs().values()]) + ')'
	rhs = '(' + ','.join([str(value) for value in tree.fetch_rhs().values()]) + ')'
	result.append(lhs + ' <---> ' + rhs)
	for state in tree.load_states():
		func_print_tree(state, result)
	
def func_print_tree(tree, level = 0):
	lhs = '(' + ','.join([str(value) for value in tree.fetch_lhs().values()]) + ')'
	rhs = '(' + ','.join([str(value) for value in tree.fetch_rhs().values()]) + ')'
	print '+' * level + lhs, '<--->', rhs
	level += 1
	for state in tree.load_states():
		func_print_tree(state, level)

if __name__ == '__main__':
	params = sys.argv
	start_file = params[1]
	goal_file = params[2]
	mode = params[3]
	output = params[4]
	start_lhs, start_rhs = func_read_file(start_file)
	goal_lhs, goal_rhs = func_read_file(goal_file)

	goal_state = State(goal_lhs, goal_rhs)
	init_state = State(start_lhs, start_rhs)
	# func_dfs_search(init_state, goal_state)
	func_bfs_search(init_state, goal_state)
	# func_print_tree(init_state)
	result = []
	func_print_string(init_state, result)
	print result
	# func_write_file(output, ['(3,3,left,0,0)', '(2,3,left,1,0)', '(0,3,right,3,0)', '(1,3,left,2,0)', '(1,1,right,2,2)', '(2,2,left,1,1)', '(2,0,right,1,3)', '(3,0,left,0,3)', '(1,0,right,2,3)', '(1,1,left,2,2)', '(0,0,right,3,3)', '(1,3,right,2,0)'])
