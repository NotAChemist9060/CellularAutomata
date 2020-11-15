from tkinter import Frame, Canvas, TOP
from cell_map import CellMap
from typing import List
from logger import Logger
import numpy as np


class CellMapWidget(Frame):

	def __init__(self, master, cell_size: int, step_interval: int, cell_map: CellMap):
		self.cells_count = cell_map.cells_count
		self.cell_size = cell_size
		self.cell_map = cell_map
		self.step_interval = step_interval
		self.simulating = False
		self.logging = False

		self.canvas = Canvas(master, 
			width=(self.cells_count * cell_size),
			height=(self.cells_count * cell_size),
			bg='white')
		self.canvas.pack(side=TOP)
		self.canvas.bind('<Button-1>', self.on_click)

		self.draw()


	def draw(self):
		self.draw_grid()
		self.draw_map()
		

	def on_click(self, event):
		x, y = event.x // self.cell_size, event.y // self.cell_size
		self.cell_map.map[x, y] = (self.cell_map.map[x, y] + 1) % 2

		self.canvas.delete('all')
		self.draw()


	def draw_cell(self, x: int, y: int):
		self.canvas.create_rectangle(self.cell_size * x,
			self.cell_size * y, 
			self.cell_size * (x+1), 
			self.cell_size * (y+1), 
			fill='black')


	def draw_grid(self):
		for i in range(0, self.cells_count * self.cell_size, self.cell_size):
			self.canvas.create_line(0, i, self.cells_count * self.cell_size, i)

		for i in range(0, self.cells_count * self.cell_size, self.cell_size):
			self.canvas.create_line(i, 0, i, self.cells_count * self.cell_size)


	def draw_map(self):
		for i in range(self.cells_count):
			for j in range(self.cells_count):
				if self.cell_map.map[i, j] == 1:
					self.draw_cell(i, j)


	def step(self):
		self.canvas.delete('all')

		self.cell_map.step()

		if self.logging:
			self.logger.log(self.cell_map.map)

		self.draw()


	def simulate_loop(self):
		if self.simulating:
			self.step()
			self.canvas.after(self.step_interval, self.simulate_loop)


	def on_simulate(self, indicator):
		self.simulating = not self.simulating
		self.simulate_loop()

		if indicator:
			if self.simulating:
				indicator.configure(bg='red')
			else:
				indicator.configure(bg='white')


	def on_randomize(self):
		self.canvas.delete('all')

		self.cell_map.randomize()

		if self.logging:
			self.logger.log(self.cell_map.map)

		self.draw()


	def on_clear(self):
		self.canvas.delete('all')

		self.cell_map.clear()

		if self.logging:
			self.logger.log(self.cell_map.map)

		self.draw()


	def on_set_config(self, new_map: np.ndarray):
		self.canvas.delete('all')

		self.cell_map.map = new_map

		if self.logging:
			self.logger.log(self.cell_map.map)

		self.draw()


	def on_start_log(self, session_name: str = 'default'):
		self.logging = True
		self.logger = Logger()
		self.logger.start_session(self.cell_map.map, session_name)


	def on_end_log(self):
		self.logger.end_session()
		self.logging = False


	def on_log(self, indicator, session_name: str = 'default'):
		if not self.logging:
			indicator.configure(bg='red')
			self.on_start_log(session_name)
		else:
			indicator.configure(bg='white')
			self.on_end_log()
