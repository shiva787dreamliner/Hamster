import Tkinter as tk

def main ():
	print main
	master = tk.Tk()

	canvas1 = tk.Canvas(master, bg = "blue", width = 300, height = 300)
	canvas1.pack

	master.mainloop()


if __name__=="__main__":
	main()
