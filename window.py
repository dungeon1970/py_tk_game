import tkinter as tk

from PIL import Image,ImageTk
import time
import imageio
class Gui():

    def __init__(self,current_location, locations, puzzles):
        # create window
        self.root = tk.Tk()
        self.root.configure(bg='green')
        self.root.title("Our game")

        # variables
        self.current_location = current_location
        self.locations = locations
        self.puzzles = puzzles
        self.header_text = tk.StringVar()
        self.scene_text = tk.StringVar()
        self.popup_text = tk.StringVar()

        self.draw_window()
        self.change_location(self.current_location)
        self.root.mainloop()

    # method which draws window and components
    def draw_window(self):
        # Gets both half the screen width/height and window width/height, places window
        windowWidth = int(self.root.winfo_screenwidth()/4*2.5)
        windowHeight = int(self.root.winfo_screenheight()/4*2.5)
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2-50)
        self.root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
        self.root.resizable('FALSE','FALSE')
        # main dialogue frame box
        self.scene_canvas = tk.Canvas(self.root, bg="black", highlightthickness=.5)
        self.scene_canvas.place(relx=0.02, rely=0.04, relwidth=0.56, relheight=0.7)
        # main dialogue location frame
        self.location_frame = tk.Frame(self.scene_canvas, bg = "black")
        self.location_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.15)
        # horizontal line between location and story
        self.scene_divider = tk.Frame(self.scene_canvas, bg = "#069C89").place(relx=0.05, rely=0.2, relwidth=0.9)
        # main dialogue location story frame
        self.scene_frame = tk.Frame(self.scene_canvas, bg = "black")
        self.scene_frame.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.7)
        # picture box
        self.animation_frame = tk.Frame(self.root)
        self.animation_frame.place(relx=0.6, rely=0.04, relwidth=0.38, relheight=0.7)
        self.animation_picture = tk.Label(self.animation_frame)
        self.animation_picture.pack()
        # main options box
        self.scene_options = tk.Canvas(self.root, bg="black", highlightthickness=.5)
        self.scene_options.place(relx=0.02, rely=0.77, relwidth=0.96, relheight=0.2)

        self.root.update()
        story_width = self.scene_frame.winfo_width() - 15
        # location dialogue label
        self.location = tk.Label(self.location_frame, fg = "#069C89", bg="black", textvariable = self.header_text, font=('Gabriola 26 underline')).place(relwidth=1, relheight=1)
        # loccation story label
        self.scene = tk.Label(self.scene_frame, bg="black", fg = "white", padx=15, justify=tk.LEFT, textvariable = self.scene_text, wraplength = story_width, font=('"segoe print" 12'), anchor = "nw").place(relwidth=1)

    # method which shows current location animation
    def animation(self):
        animation_width = self.animation_frame.winfo_width()
        animation_height = self.animation_frame.winfo_height()
        try:
            animation_video = self.video.get_next_data()
            animation_image = Image.fromarray(animation_video)
            animation_image=ImageTk.PhotoImage(animation_image.resize((animation_width, animation_height), Image.ANTIALIAS))
            self.animation_picture.config(image=animation_image)
            self.animation_picture.image = animation_image
            self.animation_picture.after(self.delay, lambda: self.animation())
        except:
            self.video.close()
            return 

    # method which shows current location header text
    def show_header_text(self):
        header = self.locations[self.current_location].title
        text =""
        for letter in header:
            text += letter
            time.sleep(.01)
            self.header_text.set(text)
            self.root.update()

    # method which shows current location scene story
    def show_scene_story(self, text, label):
        scene_story = text
        text =""
        for letter in scene_story:
            text += letter
            time.sleep(.01)
            label.set(text)
            self.root.update()

    # method called to display options for location
    def show_option_buttons(self):
        text = tk.StringVar()
        tk.Label(self.scene_options, bg = "black", height="1", font=('Gabriola 12'), fg="white", text = "What do you do? ").pack(side=tk.TOP, anchor="w", padx=15, pady=2)
        if len(self.puzzles[self.current_location].options.items()) == 0:
            text.set("  Leave by")
        else:
            text.set("Or leave by")
        for option, values in self.puzzles[self.current_location].options.items():
            if values["option"][1] == "Active":
                tk.Button(self.scene_options, font= ('"Arial Black" 10'), bg="green", padx=2, pady=2, fg="white", text=values["option"][0], command=lambda x=option: self.show_pop_up(x)).pack(side=tk.LEFT, padx=15, anchor="nw")
        tk.Label(self.scene_options, bg = "black", font= ('Helvetica 10 bold'), fg="white", textvariable=text).pack(side=tk.LEFT, padx=5, pady=5, anchor="n")
        for exit in self.locations[self.current_location].exits:
            tk.Button(self.scene_options, font= ('"Arial Black" 10'), padx=2, pady=2, bg="cyan", text=exit[0], command=lambda x=exit: self.change_location(x[1])).pack(side=tk.LEFT, anchor="nw", padx=15)

    # function called when event is triggered or location changes
    def change_location(self, location):
        self.scene_text.set("")
        self.clear_scene_options_frame()
        self.current_location = location
        video_name = f"images/{self.locations[self.current_location].picture}.mp4" 
        self.video = imageio.get_reader(video_name)
        self.delay = int(1000 / self.video.get_meta_data()['fps'])
        self.animation()
        self.show_header_text()
        self.show_scene_story(self.puzzles[self.current_location].get_option_stories(), self.scene_text)
        self.show_option_buttons()

    # method to show popup when option button is pressed
    def show_pop_up(self, option):
        self.clear_scene_options_frame()
        self.popup = tk.Canvas(self.root, bg="#163e1b")
        self.popup.place(relx=0.2, rely=0.2, relheight=0.6, relwidth=0.6)
        self.root.update()
        popup_width = self.popup.winfo_width()-32
        tk.Label(self.popup, wraplength=popup_width, bg="#163e1b", fg="white", font=('"segoe print" 20 bold'), textvariable = self.popup_text, anchor = "nw", justify=tk.LEFT).pack(side=tk.TOP, padx=15, pady=15)
        self.show_scene_story(self.puzzles[self.current_location].options[option]["response"], self.popup_text)
        time.sleep(0.7)
        tk.Button(self.popup, text="OK", command=lambda x = option, y = self.popup: self.remove_popup(x,y)).pack(side=tk.BOTTOM, pady=10)

    # function called to remove popup story and update scene
    def remove_popup(self, option, popup):
        popup.destroy()
        self.puzzles[self.current_location].update_option(option)
        self.show_scene_story(self.puzzles[self.current_location].get_option_stories(), self.scene_text)
        self.show_option_buttons()

    def clear_scene_options_frame(self):
        for child in self.scene_options.winfo_children():
            if str(type(child)) == "<class 'tkinter.Button'>" or str(type(child)) == "<class 'tkinter.Label'>":
                child.destroy()

    # function called to load game
    def load_game(self):
        pass

    # function called to save game progress
    def save_game(self):
        pass