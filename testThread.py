import threading

class Testthread(threading.Thread):
	def __init__(self):
		super(Testthread, self).__init__()
		self.message = "hello"

	def run(self):
		while (True):
			print self.message


class OtherTestThread(threading.Thread):
	def __init__(self):
		super(OtherTestThread, self).__init__()
		self.message2 = "world"

	def run(self):
		while (True):
			print self.message2

def main():
	example = Testthread()
	exmple2 = OtherTestThread()

	example.start()
	example2.start()


if __name__== "__main__":
    main()
