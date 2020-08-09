import tkinter as tk
from CovidRiskCalc import run
from CovidRiskCalc import get_scale
from CovidRiskCalc import activities

HEIGHT = 300
WIDTH = 750

COLOR = 'light cyan'
STATE_POSITION = 0.05
COUNTY_POSITION = 0.2

def test_function(s, c, l):
    risk_rating['text'] = run(s, c, l)
    print(get_scale(l))

root = tk.Tk()
root.title("COVID-19 Risk Calculator")

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = COLOR)
frame.place(relwidth=1, relheight=1)

button =  tk.Button(frame, text = "Calculate Risk", bg = 'white', font= 20, command=lambda: test_function(state_entry.get(), county_entry.get(), drop['text']))
button.place(relx = 0.45, rely = 0.4, relwidth=0.5, relheight=0.2)

label1 = tk.Label(frame, text="Enter in your state: ", bg=COLOR, font = 40)
label1.place(relx=0, rely=STATE_POSITION)

label2 = tk.Label(frame, text="Enter in your county: ", bg=COLOR, font = 40)
label2.place(relx=0, rely=COUNTY_POSITION)

state_entry = tk.Entry(frame, bg='white')
state_entry.place(relx=0.5, rely=STATE_POSITION, relheight=0.1, relwidth=0.45)

county_entry = tk.Entry(frame, bg = 'white')
county_entry.place(relx=0.5, rely=COUNTY_POSITION, relheight=0.1, relwidth=0.45)

risk_rating = tk.Label(frame, bg = COLOR, font=19)
risk_rating.place(relx=0, rely=0.65,)

clicked = tk.StringVar()
clicked.set("Enter in where you are going")
drop = tk.OptionMenu(root, clicked, *activities)
drop.place(relx=0.005, rely=0.35, relwidth=0.4)



root.mainloop()
