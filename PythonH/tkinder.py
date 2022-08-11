import tkinter


def b1_click():
    print("Precionado boton b1")
def b2_click():
    print("Precionado boton b2")

w = tkinter.Tk()
w.title = "Sin Nombre"
w.geometry("400x400")
fm = tkinter.Frame(w)
fm.grid(row=0,column=0)
b1 = tkinter.Button(fm, text="Boton 1", command=b1_click)
b1.grid(row=1,column=0)
b2 = tkinter.Button(fm, text="Boton 2", command=b2_click)
b2.grid(row=2,column=0)

w.mainloop()