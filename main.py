import asyncio
import sys
import threading
from tkinter import *
from pygame import mixer


class main(Tk):
    def __init__(self):
        Tk.__init__(self)
        mixer.init()
        self.title('ALTERA MUSIC')
        self.geometry('300x125')
        self.geometry('+%d+%d' % (5, 5))
        self.config(bg='#2e2d2d')
        self.attributes('-alpha', 0)
        self.attributes('-topmost', 1)
        self.overrideredirect(True)

        self.bgcolor = '#2e2d2d'
        Label(self, text='ALTERA MUSIC', bg=self.bgcolor, fg='white').place(x=1, y=1)
        self.play_button = Button(self, text="play", width=13, command=lambda: asyncio.run(self.start()), bg=self.bgcolor, fg='white')
        self.playlist_button = Button(self)
        self.exit_button = Button(self, text='x', width=3, height=1,
                                  command=lambda: asyncio.run(self.app_exit())).place(x=270, y=0)
        self.minimise_button = Button(self, text='-', width=3, height=1,
                                      command=lambda: asyncio.run(self.minimize())).place(x=240, y=0)

        self.volume_slider = Scale(self, label='Volume', from_=0, to=1, digits=3, resolution=0.01, orient=HORIZONTAL,
                                   command=lambda event: asyncio.run(self.set_volume()), bg=self.bgcolor, fg='white')
        self.volume_slider.set(1)
        self.icon = Toplevel(self)
        self.icon.attributes('-alpha', 0)

        # start app
        threading.Thread(target=lambda: asyncio.run(self.main()), daemon=True).start()
        self.icon.bind("<Map>", lambda event: asyncio.run(self.unminimize()))
        self.mainloop()

    async def minimize(self):
        await self.disappear()
        self.icon.state('iconic')

    async def unminimize(self):
        await self.reappear()
        self.icon.state('normal')

    async def app_exit(self):
        sys.exit()

    async def main(self):
        self.play_button.place(x=1, y=32)
        self.volume_slider.place(x=1, y=60)
        await self.load_song("")
        await self.reappear()

    async def load_song(self, url_or_fp):
        mixer.music.load("cool.mp3")

    async def set_volume(self):
        mixer.music.set_volume(self.volume_slider.get())


    async def check(self):
        while mixer.music.get_busy():
            pass
        self.play_button.config(text="start", command=lambda: asyncio.run(self.start()))
        await self.load_song("")
        await self.reappear()

    async def start(self):
        self.play_button.config(text="pause", command=lambda: asyncio.run(self.pause()))
        mixer.music.play()
        threading.Thread(target=lambda: asyncio.run(self.check()), daemon=True).start()

    async def pause(self):
        self.play_button.config(text="unpause", command=lambda: asyncio.run(self.unpause()))
        mixer.music.pause()

    async def unpause(self):
        self.play_button.config(text="pause", command=lambda: asyncio.run(self.pause()))
        mixer.music.unpause()

    async def stop(self):
        self.play_button.config(text="play", command=lambda: asyncio.run(self.play()))
        mixer.music.pause()

    async def disappear(self):
        opacity = 0.9
        while opacity >= 0:
            await asyncio.sleep(0.005)
            opacity -= 0.025
            self.attributes('-alpha', opacity)

    async def reappear(self):
        opacity = 0
        while not opacity >= 0.9:
            await asyncio.sleep(0.005)
            opacity += 0.025
            self.attributes('-alpha', opacity)


if __name__ == '__main__':
    app = main()
