from tkinter import *
import pandas as pd
import random


BACKGROUND_COLOR = "#B1DDC6"
COUNT = 1

# ---------------------------------READING DATA--------------------------------------------------
try:
    data = pd.read_csv("data/words_to_learn.csv")
    data_to_learn = data.to_dict(orient="records")
    word = {}
except FileNotFoundError:
    data = pd.read_csv("data/en_words.csv")
    data_to_learn = data.to_dict(orient="records")
    word = {}


# -----------------------------------Flip cards-----------------------------------------------------
def flip():
    canvas_2.itemconfig(front, image=card_back_img)
    canvas_2.itemconfig(flashcard_title, text="Ukrainian", fill="white")
    canvas_2.itemconfig(flashcard_word, text=word["translate"], fill="white")


# ----------------------------------Generate words-------------------------------------------------

def next_card():
    global flip_timer, word, data_to_learn, data, COUNT
    word = random.choice(data_to_learn)
    window.after_cancel(flip_timer)
    canvas_2.itemconfig(front, image=card_front_img)
    canvas_2.itemconfig(flashcard_title, text="English", fill="black")
    canvas_2.itemconfig(flashcard_word, text=word["word"], fill="black")
    flip_timer = window.after(5000, flip)


def is_known():
    data_to_learn.remove(word)
    update_data = pd.DataFrame.from_dict(data_to_learn)
    update_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ----------------------------------Screen Setup--------------------------------------------------
window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(4000, flip)

# ----------------------------------------GUI----------------------------------------------------
# card back
canvas_1 = Canvas(width=900, height=600, highlightthickness=0, bg=BACKGROUND_COLOR)
card_back_img = PhotoImage(file="images/card_back.png")
back = canvas_1.create_image(450, 300, image=card_back_img)
canvas_1.grid(row=0, column=0, columnspan=2)

# card front
canvas_2 = Canvas(width=900, height=600, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="images/card_front.png")
front = canvas_2.create_image(450, 300, image=card_front_img)
canvas_2.grid(row=0, column=0, columnspan=2)
flashcard_title = canvas_2.create_text(445, 150, text="English", fill="black", font=("Ariel", 40, "italic"))
flashcard_word = canvas_2.create_text(445, 300, text=f"", font=("Ariel", 60, "bold"))

# buttons
cancel_image = PhotoImage(file="images/wrong.png")
done_image = PhotoImage(file="images/done.png")
cancel_button = Button(image=cancel_image, highlightthickness=0, command=next_card)
cancel_button.grid(row=1, column=0, padx=50, pady=0)
done_button = Button(image=done_image, highlightthickness=0, command=is_known)
done_button.grid(row=1, column=1, padx=50, pady=0)
next_card()

window.mainloop()
