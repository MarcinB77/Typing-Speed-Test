import random
import threading
from _tkinter import TclError
from tkinter import messagebox, Label, Button, Text, Canvas, PhotoImage, Tk
import requests
from requests.exceptions import ConnectionError, RequestException
from json.decoder import JSONDecodeError

SECONDS = 15

MAIN_FONT = ("Arial", 12, "bold")
TIMER_FONT = ("Arial", 20, "bold")

URL = "https://random-word-api.herokuapp.com/word?number=150"
ERRORS = (IndexError, ValueError, ConnectionError, JSONDecodeError, RequestException)

list_of_words = []
typed_words_list = []


class WordListGenerator:
    def __init__(self, url):
        self.response = requests.get(url)
        self.words = self.response.json()


def generate_words():
    global list_of_words
    try:
        generator = WordListGenerator(URL)

    except ERRORS:
        try:
            with open("words.txt") as words:
                temp_list = words.read().split(",")
        except (FileNotFoundError, IndexError):
            messagebox.showerror(title='Error', message="Sorry, no words to show. Try again later.")
        else:
            list_of_words = [word.replace('"', '') for word in temp_list]
    else:
        list_of_words = [word.replace('"', '') for word in generator.words]


def clear_list():
    global typed_words_list


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing speed test")
        self.minsize(200, 200)

        # Labels
        self.typed_words_list = []
        self.high_score_label = Label(text=f"High score:\n {self.high_score} words per min", font=MAIN_FONT)
        self.high_score_label.grid(column=0, row=0)
        self.high_score_label.config(padx=5, pady=5)

        self.word_label = Label(text="", font=MAIN_FONT)
        self.word_label.grid(column=0, row=2)
        self.word_label.config(padx=5, pady=5)

        self.score_label = Label(text="\n", font=MAIN_FONT)
        self.score_label.grid(column=0, row=5)
        self.score_label.config(padx=5, pady=5)

        # Buttons
        self.start_button = Button(text="Start", command=self.start_test)
        self.start_button.grid(column=0, row=3)

        # Text
        self.typed_words_txt = Text(width=20, height=1)
        self.typed_words_txt.grid(column=0, row=4)
        self.typed_words_txt['state'] = 'disabled'

        # Canvas
        self.canvas = Canvas(width=200, height=200)
        try:
            self.timer_img = PhotoImage(file="timer.png")
            self.canvas.create_image(100, 100, image=self.timer_img)
        except TclError:
            pass
        self.timer_text = self.canvas.create_text(100, 100, text="01:00", fill="black", font=TIMER_FONT)
        self.canvas.grid(column=0, row=1)

    with open("high_score.txt") as file:
        high_score = int(file.read())

    # Funcs
    def count_down(self, seconds):
        count = seconds
        count_min = f"0{count // 60}"
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            # timer
            self.after(1000, self.count_down, count - 1)
        else:
            score = len(typed_words_list)
            score_txt = f"Your typing speed:\n {score} words per min"
            self.score_label.configure(text=score_txt)
            self.typed_words_txt.delete('1.0', 'end')
            self.start_button['state'] = 'normal'
            self.typed_words_txt['state'] = 'disabled'
            self.word_label.configure(text=" ")
            if int(self.high_score) < score:
                self.new_high_score(score)

    def new_high_score(self, score):
        with open("high_score.txt", "w") as hs_file:
            hs_file.write(str(score))
        self.high_score_label.configure(text=f"High score:\n {score} words per min")
        messagebox.showinfo(title="Result", message=f"New high score! {score} words per min")

    def start_test(self):
        clear_list()
        generate_words()
        self.typed_words_txt['state'] = 'normal'
        self.start_button['state'] = 'disabled'
        self.typed_words_txt.focus_set()
        self.count_down(SECONDS)
        self.score_label.config(text="\n")
        self.show_new_word()
        self.check()

    def show_new_word(self):
        self.typed_words_txt.config(fg='black')
        new_word = random.choice(list_of_words)
        list_of_words.remove(new_word)
        self.word_label.configure(text=new_word)

    def check(self):
        word = self.word_label.cget("text")
        typed_word = (self.typed_words_txt.get("1.0", 'end-1c')).strip()
        if len(word) <= len(typed_word) and word != typed_word:
            self.typed_words_txt.config(fg='red')
        else:
            self.typed_words_txt.config(fg='black')
        if word == typed_word:
            if word not in typed_words_list:  # prevents duplication of words
                typed_words_list.append(word)
            self.typed_words_txt.delete('1.0', 'end-1c')
            self.show_new_word()
        threading.Timer(0.1, self.check).start()  # thread of constant checking


if __name__ == "__main__":
    app = App()
    app.mainloop()
