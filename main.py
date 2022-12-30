from tkinter import *
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}

try:
    to_learn_data = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    flashCard_data = pandas.read_csv("data/french_words.csv")
    flashcard_list = flashCard_data.to_dict(orient="records")

else:
    flashcard_list = to_learn_data.to_dict(orient="records")

#--------------------------- FLIP CARDS --------------------------------#

def flip_card():
    english_word = current_card["English"]
    card_canvas.itemconfig(canvas_image, image=back_card_img)
    card_canvas.itemconfig(card_title, text="English", fill="white")
    card_canvas.itemconfig(card_word, text=f"{english_word}", fill="white")
#------------------------- CREATE FLASHCARD -----------------------------#

def next_card():
    global time_to_flip, current_card
    window.after_cancel(time_to_flip)
    current_card = choice(flashcard_list)
    french_word = current_card["French"]
    card_canvas.itemconfig(card_title, text="French", fill="black")
    card_canvas.itemconfig(card_word, text=f"{french_word}", fill="black")
    card_canvas.itemconfig(canvas_image, image=front_card_img)
    time_to_flip = window.after(5000, flip_card)
#----------------------- WORDS NOT LEARNED -----------------------------#

def know():
    flashcard_list.remove(current_card)
    df = pandas.DataFrame(flashcard_list)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()
#----------------------------- UI SETUP --------------------------------#
window = Tk()
window.title("FLASH CARD")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

time_to_flip = window.after(5000, flip_card)

# Creating the canvas and The Images
card_canvas = Canvas(width=800, height=526)
front_card_img = PhotoImage(file="./images/card_front.png")
back_card_img  = PhotoImage(file="./images/card_back.png")
right_img      = PhotoImage(file="./images/right.png")
wrong_img      = PhotoImage(file="./images/wrong.png")

canvas_image = card_canvas.create_image(400, 263, image=front_card_img)
card_title = card_canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
card_word  = card_canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
card_canvas.grid(row=0, column=0, columnspan=2)
card_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

# The Buttons
know_it = Button(image=right_img, highlightthickness=0, command=know)
know_it.grid(row=1, column=1)
unknown = Button(image=wrong_img, highlightthickness=0, command=next_card)
unknown.grid(row=1, column=0)

next_card()

window.mainloop()