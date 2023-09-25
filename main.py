from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
SPANISH = "Spanish"
ENGLISH = "English"
TIME = 3000
current_card = {}
to_learn = {}
# ---------------------------- CREATE FLASHCARDS ------------------------------- #

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/spanish.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def flashcard():
    global current_card, timer
    window.after_cancel(timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text=SPANISH, fill="black")
    canvas.itemconfig(card_word, text=f"{current_card[SPANISH]}", fill="black")
    canvas.itemconfig(card_bg, image=card_front_img)
    window.after_cancel(timer)
    timer = window.after(TIME, flip_card)


# ---------------------------- FLIP CARDS WITH TIMER ------------------------------- #

def flip_card():
    canvas.itemconfig(card_title, fill="white", text=ENGLISH)
    canvas.itemconfig(card_word, fill="white", text=current_card[ENGLISH])
    canvas.itemconfig(card_bg, image=card_back_img)


# ---------------------------- UPDATE CSV AND CREATE NEW ------------------------------- #

def remove_word():
    to_learn.remove(current_card)
    new_df = pd.DataFrame(to_learn)
    new_df.to_csv("data/words_to_learn.csv", index=False)

    flashcard()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Test Your Knowledge in Spanish!")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(TIME, flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg= BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 170, text="", font=TITLE_FONT)
card_word = canvas.create_text(400, 275, text="", font=WORD_FONT)


# Buttons
correct_img = PhotoImage(file="images/right.png")
known_button = Button(image=correct_img, highlightthickness=0, command=remove_word)
known_button.config(padx=20, pady=20)
known_button.grid(column=1, row=1)

incorrect_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=incorrect_img, highlightthickness=0, command=flashcard)
unknown_button.grid(column=0, row=1)

flashcard()


window.mainloop()
