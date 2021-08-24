import time

class Grid:

	def __init__(self):
		self.recursions = 0

	# TESTED OK
	def read_csv(self, file):
		grid = [[" " for j in range(1, 10)] for i in range(1, 10)]
		with open(file, 'r') as csv_file:
			line_num = 0
			for line in csv_file:
				nums = line.strip().split(',')
				assert len(nums) == 9
				int_nums = []
				for num in nums:
					try:
						num = int(num)
					except:
						num = " "
					int_nums.append(num)
				grid[line_num] = int_nums
				line_num += 1
		return grid

	# TESTED OK
	def print_grid(self, grid):
		print("\n")
		horizontal_sep = '+'+ ('-' * (18+9+2)) + '+'
		sub_grid_div = "+".join(['-' * (9) for i in range(3)])
		print(horizontal_sep)
		a = 0
		for line in grid:
			line = [str(x) for x in line]
			print_me = "|"
			idx = 0
			for num in line:
				print_me += " "+num+" "
				if idx == 2 or idx == 5:
					print_me += "|"
				idx += 1
			print_me += "|"
			print(print_me)
			if a == 2 or a == 5:
				print("|"+sub_grid_div+"|")
			a += 1
		print(horizontal_sep)
		print("\n")

	# TESTED OK
	def get_rows(self, grid):
		return grid

	# TESTED OK
	def get_cols(self, grid):
		cols = []
		for x in range(9):
			col = []
			for y in range(9):
				col.append(grid[y][x])
			cols.append(col)
		return cols

	# TESTED OK
	def get_sub_grids(self, grid):
		sub_grids = []
		for x in range(0, 9, 3):
			for y in range(0, 9, 3):
				sub_rows = grid[x:x+3]
				sub_grid = []
				for sub_row in sub_rows:
					sub_grid.extend(sub_row[y:y+3])
				sub_grids.append(sub_grid)
		return sub_grids

	# TESTED OK
	def num_valid(self, num):
		return num in range(1, 10)

	# TESTED OK
	def nums_valid(self, nums):
		nums_seen = []
		if len(nums) != 9:
			return False
		for x in nums:
			if not self.num_valid(x):
				return False
			if x in nums_seen:
				return False
			nums_seen.append(x)
		return True

	def valid(self, grid):
		for row in self.get_rows(grid):
			if not self.nums_valid(row):
				return False 
		for col in self.get_cols(grid):
			if not self.nums_valid(col):
				return False 
		for grid in self.get_sub_grids(grid):
			if not self.nums_valid(grid):
				return False 
		return True

	# TESTED OK
	def incr_pos(self, x, y):
		if x < 8:
			x += 1
		else:
			x = 0
			y += 1
		if y == 9:
			raise Exception("Reached end")
		return x, y

	# TESTED OK
	def decr_pos(self, x, y):
		if x > 0:
			x -= 1
			return x, y
		else:
			x = 8
			y -= 1
			return x, y

	def find_next_empty(self, grid, x, y):
		while self.num_valid(grid[x][y]):
			x, y = self.incr_pos(x, y)
			if x > 8 or y > 8:
				raise Exception
		return x, y

	def copy(self, grid):
		new_grid = [[" " for j in range(1, 10)] for i in range(1, 10)]
		for x in range(9):
			for y in range(9):
				new_grid[x][y] = grid[x][y]
		return new_grid

	def recurse(self, old_grid, x, y, level):
		self.recursions += 1
		grid = self.copy(old_grid)
		level += 1
		self.print_grid(grid)

		# grid is valid - stop recursion
		if self.valid(grid):
			print("FOUND VALID GRID")
			return True

		# find next empty spot
		try:
			new_x, new_y = self.find_next_empty(grid, x, y)
			# set a number and recurse 
			row = grid[new_x]
			col = [r[new_y] for r in grid]
			sub_grid_x = 3*(new_x // 3)
			sub_grid_y = 3*(new_y // 3)
			sub_grid = []
			for ree in grid[sub_grid_x:sub_grid_x+3]:
				sub_grid.extend(ree[sub_grid_y:sub_grid_y+3])
			for num in range(1, 10):
				time.sleep(0.001)
				if not ((num in row) or (num in col) or (num in sub_grid)):
					grid[new_x][new_y] = num
					solved = self.recurse(grid, new_x, new_y, level)
					if solved:
						return True
		except Exception as ex:
			print(ex)
			# no next empty, backtrack
		return False


if __name__ == "__main__":
	g = Grid()
	grid = g.read_csv('./grid1.csv')
	g.print_grid(grid)
	g.recurse(grid, 0, 0, 0)
	print(g.recursions)

