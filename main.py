import random
import threading
from tkinter import *

with open("words.txt") as file:
    list_of_words_x = (file.read()).split(",")
    list_of_words = [word.replace('"', '') for word in list_of_words_x]

with open("high_score.txt") as file:
    high_score = int(file.read())

window = Tk()
window.title("Typing Speed Test")
window.minsize(width=200, height=200)
window.config(padx=5, pady=5)

typed_words_list = []


# Funcs
def count_down(seconds):
    count = seconds
    count_min = f"0{count // 60}"
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        # timer
        window.after(1000, count_down, count - 1)
    else:
        score = len(typed_words_list)
        score_txt = f"Your typing speed:\n {score} words per min"
        score_label.configure(text=score_txt)
        typed_words_txt.delete('1.0', END)
        start_button['state'] = 'normal'
        typed_words_txt['state'] = 'disabled'
        word_label.configure(text=" ")
        if int(high_score) < score:
            with open("high_score.txt", "w") as hs_file:
                hs_file.write(str(score))
            high_score_label.configure(text=f"High score:\n {score} words per min")


def clear_list():
    global typed_words_list
    typed_words_list = []


def start_test():
    clear_list()
    typed_words_txt['state'] = 'normal'
    start_button['state'] = 'disabled'
    typed_words_txt.focus_set()
    count_down(10)
    score_label.config(text="\n")
    show_new_word()
    check()


def show_new_word():
    new_word = random.choice(list_of_words)
    list_of_words.remove(new_word)
    word_label.configure(text=new_word)


def check():
    word = word_label.cget("text")
    if word == (typed_words_txt.get("1.0", 'end-1c')).strip():
        if word not in typed_words_list:  # <-prevents duplication of words (?)
            typed_words_list.append(word)
        typed_words_txt.delete('1.0', 'end-1c')
        show_new_word()
    threading.Timer(0.1, check).start()  # thread of constant checking


# Labels
high_score_label = Label(text=f"High score:\n {high_score} words per min", font=("Arial", 12, "bold"))
high_score_label.grid(column=0, row=0)
high_score_label.config(padx=5, pady=5)

word_label = Label(text="", font=("Arial", 12, "bold"))
word_label.grid(column=0, row=2)
word_label.config(padx=5, pady=5)

score_label = Label(text="\n", font=("Arial", 12, "bold"))
score_label.grid(column=0, row=5)
score_label.config(padx=5, pady=5)

# Buttons
start_button = Button(text="Start", command=start_test)
start_button.grid(column=0, row=3)

# Text
typed_words_txt = Text(width=20, height=1)
typed_words_txt.grid(column=0, row=4)
typed_words_txt.config()
typed_words_txt['state'] = 'disabled'

# Canvas
canvas = Canvas(width=200, height=200, highlightthicknes=0)
timer_img = PhotoImage(file="timer.png")
canvas.create_image(100, 100, image=timer_img)
timer_text = canvas.create_text(100, 100, text="01:00", fill="black", font=("Arial", 20, "bold"))
canvas.grid(column=0, row=1)


window.mainloop()
