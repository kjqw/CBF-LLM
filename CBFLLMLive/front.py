# %% Imports
from typing import Callable
import tkinter
from tkinter import Tk, Canvas, PhotoImage
from tkinter.ttk import Label, Frame, Entry, Button
from PIL import Image, ImageTk
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from threading import Thread
import time

# %% SentimentalTextGenerationSystem


@dataclass
class StreamInfo:
    additional_text: str
    is_eos: bool
    positiveness: float


class SentimenatalTextGenerationSystem(ABC):
    @abstractmethod
    def start(self, initial_text: str, stream_listener: Callable[[StreamInfo], None]):
        pass

    @abstractmethod
    def stop():
        pass


class DummySentimentalTextGenerationSystem(SentimenatalTextGenerationSystem):
    def start(self, initial_text, stream_listener):
        baka = [
            StreamInfo("本当", False, 0.3),
            StreamInfo("に", False, 0.2),
            StreamInfo("馬", False, 0.0),
            StreamInfo("鹿", False, -0.2),
            StreamInfo("なん", False, -0.5),
            StreamInfo("だな", False, -0.6),
            StreamInfo("！", True, -0.5),
        ]

        def work():
            for si in baka:
                time.sleep(max(0, random.gauss(1, 0.2)))
                stream_listener(si)

        Thread(target=work).start()

    def stop():
        pass


# %% Front Class

pi_handles = []

POSITIVE_TSUKUYOMI_FNAMES = """02 喜び・称賛/02-02b ほんわか-手を組む-口開け.png
02 喜び・称賛/02-04b 喜び・称賛-口開け.png
03 ご案内/03-03a ご案内-右手-口閉じ.png
03 ご案内/03-01b ご案内-左手-口開け.png""".splitlines()
MEDIUM_TSUKUYOMI_FNAMES = """06 きょとん・驚き・赤面/06-01a きょとん-口閉じ.png
07 トラブル・謝罪/07-03b 残念です……-口開け.png
08 悲しみ・涙/08-01c 憂い-目閉じ.png""".splitlines()
NONPOSITIVE_TSUKUYOMI_FNAMES = """07 トラブル・謝罪/07-01b 大変です！-口開け.png
07 トラブル・謝罪/07-01b 大変です！-口開け.png""".splitlines()


def get_random_tsukuyomi_fname_by_positiveness(positiveness: float) -> str:
    if positiveness > 0.3:
        return random.choice(POSITIVE_TSUKUYOMI_FNAMES)
    if positiveness >= 0:
        return random.choice(MEDIUM_TSUKUYOMI_FNAMES)
    return random.choice(NONPOSITIVE_TSUKUYOMI_FNAMES)


def get_random_tsukuyomi_pi_by_positiveness(positiveness: float) -> ImageTk.PhotoImage:
    fname = get_random_tsukuyomi_fname_by_positiveness(positiveness)
    img = Image.open(
        f"./つくよみちゃん万能立ち絵素材（花兎＊様）/02 いろんなポーズのPNG/{fname}"
    )
    w, h = img.size
    h_ref = 500
    w_ref = int(w * h_ref / h)
    resized_img = img.resize((w_ref, h_ref))
    pi = ImageTk.PhotoImage(resized_img)
    pi_handles.append(pi)
    return pi


class SentimenatalTextGenerationFrame(Frame):
    def __init__(self, master=None, model: SentimenatalTextGenerationSystem = None):
        super().__init__(master)
        # モデル
        self.model = model

        # コントロールパネル
        p1 = Frame(self)
        p1.grid(column=0, row=0)
        ## テキスト入力・表示
        self.text_entry = Entry(p1, font=("Meiryo UI", 36))
        self.text_entry.pack(fill="x", expand=True)
        ## 開始ボタン
        def start_button_command():
            self.on_start_button_press()

        start_button = Button(p1, text="開始", command=start_button_command)
        start_button.pack()
        ## 停止ボタン
        stop_button = Button(p1, text="停止")
        stop_button.pack()

        # つくよみちゃん表情
        self.tsukuyomi_label = Label(
            self, image=get_random_tsukuyomi_pi_by_positiveness(1.0)
        )
        self.tsukuyomi_label.grid(column=1, row=0)

    def on_start_button_press(self):
        def stream_listener(si: StreamInfo):
            self.text_entry.insert(tkinter.END, si.additional_text)
            self.text_entry.configure(
                foreground="black" if si.positiveness >= 0 else "red"
            )
            self.tsukuyomi_label.configure(
                image=get_random_tsukuyomi_pi_by_positiveness(si.positiveness)
            )

        self.model.start(self.text_entry.get(), stream_listener)


class Front(Tk):
    def __init__(self):
        super().__init__()
        SentimenatalTextGenerationFrame(
            self, DummySentimentalTextGenerationSystem()
        ).pack(expand=True, fill="both")
        self.mainloop()


# %%
if __name__ == "__main__":
    Front()
