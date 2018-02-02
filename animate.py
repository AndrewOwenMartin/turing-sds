import tkinter as tk
import random
import json
import itertools
import multi_swarm_solution as turing_sds
from collections import namedtuple

class Swarm:

	def __init__(self,x,y,name):
		self.x = x
		self.y = y
		self.name = name

		self.left=x-(swarm_width/2)
		self.top=y
		self.right=x+(swarm_width/2)
		self.bottom=y+swarm_height

		self.middle_y = y+(swarm_height/2)

		self.agents = []
		for agent_num in range(agent_count):
			self.agents.append(
				Agent(
					x=self.left+(agent_num*agent_dia),
					y=self.top+(0.5*agent_dia),
					hyp=Hyp(random.randint(0,9),random.randint(0,9)),
					active=False,
				)
			)

class Hyp:

	def __init__(self,x,y):
		self.x = x
		self.y = y

class Agent:

	def __init__(self,x,y,hyp,active):
		self.x=x
		self.y=y
		self.hyp=hyp
		self.active=active
		self.left = x
		self.top = y
		self.right = x + agent_dia
		self.bottom = y + agent_dia

class Arrow:

	def __init__(self,coords):
		self.coords=coords

agent_count = 5

swarm_width = 1/3
agent_dia = swarm_width/agent_count
swarm_height = agent_dia*2
v_space = 0.025
my_fill="darkblue"
swarm_label_font="Sans 20"
agent_label_font="Sans 16"
inactive_fill="dark gray"
active_fill="#666600"
quorate_fill="yellow"
swarm_fill="light gray"
background_fill="gray"
linewidth=5
def randcolor():
	return '#' + "".join(
		random.choice('0123456789abcdef')
		for x
		in range(6)
	)

colors = [randcolor() for x in range(2000)]
	#'tomato',#0 redish
	#'SkyBlue1',#1 bluish
	#'olive drab', #2 greenish
	#'MediumPurple1', #3 purplish
	#'DarkOrange1', #4 orange
	#'gold', #5 yellowish
	#'CadetBlue1', #6 light blue
	#'saddle brown', #7 brown
	#'HotPink1', #8 pinky

class Application(tk.Frame):

	def __init__(self, master, width, height, modern, from_file,quorum_threshold, draw_hypotheses):

		tk.Frame.__init__(self, master)

		self.pack()

		self.master = master

		self.width = width

		self.height = height

		self.modern = modern

		self.halt = False

		self.quorum_threshold = quorum_threshold

		self.draw_hypotheses = draw_hypotheses

		if self.modern:
			self.input_file_name = 'multi-swarm-animation.json'
		else:
			self.input_file_name = 'json_animation.json'

		if from_file:

			with open(self.input_file_name,'r') as file:
				print('attempting to load',self.input_file_name)
				if self.modern:
					data = []
					for line in file.readlines():
						data.append(json.loads(line))
				else:
					data = json.load(file)
				repeat_num, repeat = random.choice(data)
				print('randomly chose repeat',repeat_num)
				if self.modern:
					iterations = [
						x
						for x
						in repeat
					]
				else:
					iterations = [
						x[2]
						for x
						in random.choice(data)[2]]
		else:

			animation = turing_sds.get_anim(x=100,y=100,quorum_threshold=quorum_threshold,max_iterations=None)
			iterations = (x for x in animation)

			print("Iteration count",len(animation))

		self.iteration_generator = enumerate(x for x in iterations)


		self.swarms = [
			Swarm( 0.5,  0+(v_space*1),'Init'),   #0 -> 0
			Swarm(0.75,0.2+(v_space*2),'x>0'),    #2 -> 1
			Swarm(0.75,0.4+(v_space*3),'Dec(x)'), #3 -> 2
			Swarm(0.75,0.6+(v_space*4),'Inc(y)'), #4 -> 3
			Swarm(0.25,0.2+(v_space*2),'x=0'),    #1 -> 4
			Swarm(0.25,0.4+(v_space*3),'Halt'),   #5 -> 5
		]

		bottom_of_init = (
			self.swarms[0].x,
			self.swarms[0].bottom,)

		top_of_xeq0 = (
			self.swarms[4].x,
			self.swarms[4].top,)

		top_of_xgt0 = (
			self.swarms[1].x,
			self.swarms[1].top,)

		bottom_of_xeq0 = (
			self.swarms[4].x,
			self.swarms[4].bottom,)

		top_of_halt = (
			self.swarms[5].x,
			self.swarms[5].top)

		bottom_of_xgt0 = (
			self.swarms[1].x,
			self.swarms[1].bottom,)

		top_of_decx = (
			self.swarms[2].x,
			self.swarms[2].top)

		bottom_of_decx = (
			self.swarms[2].x,
			self.swarms[2].bottom,)

		top_of_incy = (
			self.swarms[3].x,
			self.swarms[3].top)

		left_of_xgt0 = (
			self.swarms[1].left,
			self.swarms[1].middle_y,
		)

		bit_left_of_xgt0 = (
			self.swarms[1].left-(1/24),
			self.swarms[1].middle_y,
		)

		right_of_xeq0 = (
			self.swarms[4].right,
			self.swarms[4].middle_y,
		)

		bit_right_of_xeq0 = (
			self.swarms[4].right+(1/24),
			self.swarms[4].middle_y,
		)

		left_of_incy_upper = (
			self.swarms[3].left,
			self.swarms[3].top+(swarm_height/4)
		)

		bit_left_of_incy_upper = (
			self.swarms[3].left-(1/24),
			self.swarms[3].top+(swarm_height/4)
		)

		left_of_incy_lower = (
			self.swarms[3].left,
			self.swarms[3].top+(3*(swarm_height/4))
		)

		bit_left_of_incy_lower = (
			self.swarms[3].left-(3/24),
			self.swarms[3].top+(3*(swarm_height/4))
		)

		self.arrows = [
			Arrow([top_of_xeq0, bottom_of_init]),
			Arrow([top_of_xgt0, bottom_of_init]),
			Arrow([top_of_halt, bottom_of_xeq0]),
			Arrow([top_of_decx, bottom_of_xgt0]),
			Arrow([top_of_incy, bottom_of_decx]),
			#Arrow([bit_left_of_xgt0, top_of_incy]),
			Arrow([bit_left_of_incy_upper,left_of_incy_upper]),
			Arrow([bit_left_of_incy_lower,left_of_incy_lower]),
		]

		self.lines = [
			Arrow([left_of_xgt0, bit_left_of_xgt0]),
			Arrow([right_of_xeq0, bit_right_of_xeq0]),
			Arrow([left_of_xgt0, bit_left_of_xgt0]),
	Arrow([bit_right_of_xeq0, bit_left_of_incy_lower]),
			Arrow([bit_left_of_xgt0, bit_left_of_incy_upper]),
		]

		self.createWidgets()

	def createWidgets(self):

		self.canvas = tk.Canvas(self, width=self.width, height=self.height)

		self.canvas['bg'] = background_fill

		self.canvas.pack(expand=True)

		root.bind('q', self.quit)

		self.draw()

	def update_network(self,modern=True):

		try:
			iteration_num, iteration = next(self.iteration_generator)
		except StopIteration:
			self.halt = True
			print('No more iterations. Halting')
			return

		print(iteration_num)

		if modern:

			for display_swarm, (name, hypotheses) in zip(self.swarms,iteration):
				for agent, (x,y,c) in zip(display_swarm.agents,hypotheses):
					if x < 0:
						x = 0
					if y < 0:
						y = 0
					agent.hyp.x = x
					agent.hyp.y = y
					agent.active = c

		else:

			for display_swarm, data_swarm in zip(self.swarms,iteration):
				name = data_swarm['swarm name']
				hypotheses = data_swarm['hypotheses']
				num = data_swarm['num']
				for agent, (activity,hyp) in zip(display_swarm.agents,hypotheses):
					if hyp:
						x,y = hyp
					else:
						x,y = '-','-'

					agent.hyp.x =x
					agent.hyp.y =y
					agent.active = activity


	def draw(self):

		try:
			self.framecount += 1
		except AttributeError:
			self.framecount = 1

		self.update_network()

		self.draw_network(self.framecount, self.quorum_threshold)

		self.frames_per_second = 60

		delay = int(1000/self.frames_per_second)

		if not self.halt:

			self.after(delay, self.draw)

			#print('drawing again after ',delay)

		#self.canvas.postscript(file="frames/file_name_{fc:03}.ps".format(fc=self.framecount), colormode='color')

	def draw_network(self, framecount, quorum_threshold):

		try:
			self.canvas.delete(self.frame_text)
		except AttributeError:
			pass

		self.frame_text = self.canvas.create_text(
			100,
			20,
			fill="#000000",
			font=agent_label_font,
			justify="right",
			text="{i:1d}".format(i=framecount)
		)

		for swarm in self.swarms:

			self.draw_swarm(swarm, quorum_threshold)

		for arrow in self.arrows:
			self.draw_arrow(arrow)

		for line in self.lines:
			self.draw_arrow(line,arrow_end=None)

	def draw_arrow(self, arrow, arrow_end=tk.LAST, head=(30,30,10)):
		# list of xys
		try:
			arrow.line
		except AttributeError:
			arrow.line = self.canvas.create_line(
				arrow.coords[0][0]*self.width,
				arrow.coords[0][1]*self.height,
				arrow.coords[1][0]*self.width,
				arrow.coords[1][1]*self.height,
				arrow=arrow_end,
				arrowshape=head,
				width=linewidth,
			)

	def draw_swarm(self, swarm, quorum_threshold):

		self.draw_swarm_box(swarm)
		self.draw_swarm_label(swarm)
		for agent in swarm.agents:
			self.draw_agent(agent, quorum_threshold)

	def draw_agent(self, agent, quorum_threshold):

		try:
			self.canvas.delete(agent.left_arc)
		except AttributeError:
			pass

		try:
			self.canvas.delete(agent.right_arc)
		except AttributeError:
			pass

		try:
			self.canvas.delete(agent.activity_oval)
		except AttributeError:
			pass

		if agent.active:
			l_fill = colors[agent.hyp.x]
			r_fill = colors[agent.hyp.y]
			if agent.active < quorum_threshold:
				stipple = "gray50"
			else:
				stipple = None
			activity_fill = active_fill

		else:
			l_fill = inactive_fill
			r_fill = inactive_fill
			stipple = None
			activity_fill = inactive_fill

		if agent.active == 1:

			activity_fill = quorate_fill

			agent.activity_oval = self.canvas.create_oval(
				agent.left*self.width,
				agent.top*self.height,
				agent.right*self.width,
				agent.bottom*self.height,
				fill=activity_fill,)

		else:

			agent.left_arc = self.canvas.create_arc(
				agent.left*self.width,
				agent.top*self.height,
				agent.right*self.width,
				agent.bottom*self.height,
				stipple=stipple,
				fill=l_fill,
				start=90,
				extent=180,
				outline='')

			agent.right_arc = self.canvas.create_arc(
				agent.left*self.width,
				agent.top*self.height,
				agent.right*self.width,
				agent.bottom*self.height,
				stipple=stipple,
				fill=r_fill,
				start=-90,
				extent=180,
				outline='')

		try:
			self.canvas.delete(agent.label)
		except AttributeError:
			pass

		agent.label = self.canvas.create_text(
			(agent.left+(agent_dia/2))*self.width,
			(agent.top+(agent_dia/2))*self.height,
			#anchor="nw",
			fill=my_fill,
			font=agent_label_font,
			justify="center",
			text="({x},{y})".format(
				x=agent.hyp.x,
				y=agent.hyp.y,)
		)



	def draw_swarm_box(self, swarm):

		try:

			swarm.box

		except AttributeError:

			swarm.box = self.canvas.create_rectangle(
				swarm.left*self.width,
				swarm.top*self.height,
				swarm.right*self.width,
				swarm.bottom*self.height,
				fill=swarm_fill)
				#(swarm.x-(swarm_width/2))*self.width,
				#swarm.y*self.height,
				#(swarm.x+(swarm_width/2))*self.width,
				#(swarm.y+swarm_height)*self.height,)

	def draw_swarm_label(self, swarm):

		try:

			swarm.label

		except AttributeError:

			swarm.label = self.canvas.create_text(
				swarm.left*self.width,
				swarm.top*self.height,
				anchor="nw",
				fill="darkblue",
				font=swarm_label_font,
				justify="right",
				text=swarm.name)

	def quit(self, event):

		print('keyboard quit')

		root.destroy()

root = tk.Tk()

app = Application(
	master=root,
	width=1080,
	height=1080,
	modern=True,
	from_file=False,
	quorum_threshold=2,
	draw_hypotheses=False)

root.mainloop()
