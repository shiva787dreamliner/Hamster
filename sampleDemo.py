'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Parking Ticket Machine - an example of FSM

   By:            Qin Chen
   Last Updated:  6/10/16

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import threading
import Queue
import Tkinter as tk

##############################
# A genric state machine
##############################
class StateMachine(object):
	def __init__(self, name, eventQ_handle):
		self.name = name		# machine name
		self.states = []	# list of lists, [[state name, event, transition, next_state],...]
		self.start_state = None
		self.end_states = []	# list of name strings
		self.q = eventQ_handle
		return

	def set_start_state(self, state_name):
		self.start_state = state_name
		return

	def get_start_state(self):
		return self.start_state
		
	def add_end_state(self, state_name):
		self.end_states.append(state_name)
		return
			
	def add_state(self, state, event, callback, next_state):
		self.states.append([state, event, callback, next_state]) # append to list
		return
	
	# you must set start state before calling run()
	def run(self):
		current_state = self.start_state
		#while not self.q.empty(): # for a machine that has end states
		while True:
			#print "current state", current_state
			if current_state in self.end_states:
				break
			if not self.q.empty():
				e = self.q.get()
				for c in self.states:
					if c[0] == current_state and c[1] == e:
						#print('\nAction = %s, Transition = %s to %s' % (c[2], c[0], c[3]))
						print('Transition = %s to %s' % (c[0], c[3]))
						c[2](c[3])	# invoke callback function
						current_state = c[3] 	# next state
						break	# get out of inner for-loop
		return

#######################################################################
# This class has method for drawing state machine map(i.e., current state being highlighted(yellow)
# and all others dehighlighted(green)). It also has method that listens to key pressed.
########################################################################
class GUI(object):
    def __init__(self, root, eventQ_handle):
        self.q = eventQ_handle
        self.root = root
        self.size_x = 40
        self.size_y = 40
        self.msgvar = tk.StringVar()
        self.msgbox = tk.Label(root, bg="orange", textvariable=self.msgvar)
        self.msgbox.pack()
        self.states = {'Unpaid':[100, 150], 'Paid':[200, 150]}
        self.canvas = tk.Canvas(self.root, bg="white", width=300, height=300)
        self.canvas.pack(expand=1, fill='both')

        self.canvas.bind_all("<m>", self.deposit_money)
        self.canvas.bind_all("<t>", self.request_ticket)
        self.canvas.bind_all("<r>", self.request_refund)
        return

    def deposit_money(self, event=None):
        print "\nm pressed"
        self.q.put("deposit_money")
        return

    def request_ticket(self, event=None):
        print "\nt pressed"
        self.q.put("request_ticket")
        return

    def request_refund(self, event=None):
        print "\nr pressed"
        self.q.put("request_refund")
        return

    # high light to_state in yellow and dehigh light from_state in green
    def update_states_map(self, current_state):
    	drawn_states = set() # holds state names that have been drawn
    	for state_name, val in self.states.items():	# step into state machine
    		if state_name not in drawn_states:
    			drawn_states.add(state_name)
    			x = val[0]
        		y = val[1] 
    			if state_name is current_state:
    				self.canvas.create_oval(x-self.size_x, y-self.size_y, x+self.size_x, y+self.size_y, fill="yellow")
    				self.canvas.create_text(x+self.size_x/6, y+self.size_y/6,fill="darkblue",text=state_name)
    			else:
    				self.canvas.create_oval(x-self.size_x, y-self.size_y, x+self.size_x, y+self.size_y, fill="green")
    				self.canvas.create_text(x+self.size_x/6, y+self.size_y/6,fill="darkblue",text=state_name)
    	return

######################################################################
# this class has all the callback functions. They are
# responsible for output(in case of a transducer state machine) and requesting
# for GUI update(i.e., highlight current state and de-highlight other states)
######################################################################
class TicketMachine(object):
	def __init__(self, gui_handle, sm_handle):
		self.gui_handle = gui_handle
		self.sm = sm_handle
		# Populate FSM with ticket machine information in this format:
		# ('state name', 'event/input', 'action/callback', 'new state')
		self.sm.add_state('Unpaid', 'deposit_money', self.taking_money, 'Paid')
		self.sm.add_state('Unpaid', 'request_ticket', self.doing_nothing, 'Unpaid')
		self.sm.add_state('Unpaid', 'request_refund', self.doing_nothing, 'Unpaid')

		self.sm.add_state('Paid', 'deposit_money', self.doing_nothing, 'Paid')
		self.sm.add_state('Paid', 'request_ticket', self.printing_ticket, 'Unpaid')
		self.sm.add_state('Paid', 'request_refund', self.delivering_refund, 'Unpaid')
		
		self.sm.set_start_state('Unpaid')	# this must be done before starting machine
		self.gui_handle.update_states_map("Unpaid")

	def taking_money(self, new_state):
		print "taking money"
		self.gui_handle.update_states_map(new_state)
		self.gui_handle.msgvar.set("taking money")
		return

	def printing_ticket(self, new_state):
		print "printing ticket"
		self.gui_handle.update_states_map(new_state)
		self.gui_handle.msgvar.set("printing ticket")
		return

	def delivering_refund(self, new_state):
		print "delivery refund"
		self.gui_handle.update_states_map(new_state)
		self.gui_handle.msgvar.set("delivery refund")
		return

	def doing_nothing(self, new_state):
		print "doing nothing"
		self.gui_handle.update_states_map(new_state)
		return

def main():
	q = Queue.Queue()	# event queue

	# start user interface session
	# t = threading.Thread(name='User', target=event_producer, args=(q,))
	# t.start()
	m = tk.Tk()
	m.title("Parking Ticket Machine")
	gui_handle = GUI(m, q)

	# Create an instance of FSM
	sm = StateMachine('Parking Ticket FSM', q)

	# Create an instance of ticket machine
	tm = TicketMachine(gui_handle, sm)

	t = threading.Thread(name='FSM', target=sm.run)
	t.daemon = True
	t.start()

	# main thread listening to key presses
	m.mainloop()	

if __name__ == "__main__":
	sys.exit(main())
