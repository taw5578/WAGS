import tkinter
import customtkinter
from PIL import Image
import assistant
import os
import sys
import ast
import json
import speech_recognition as sr
import threading



class AppWAGS(customtkinter.CTk):
    # Directory of project
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    
    isRunning = False                      # State of assistant
    assistant_thread = threading.Thread()  # Thread for running the voice assistant
    recognizer = sr.Recognizer()           # Speech recognizer
    mic = sr.Microphone()                  # Microphone for speech recognition
    
    # Open and read json containing app text
    with open(f"{parent_dir}\\assets\\data\\appText.json") as f:
        text_data = f.read()
        
    # Convert str to dict
    text_dict = ast.literal_eval(text_data)
    
    # Dimensions
    width = 700
    height = 350
    
    # Fonts
    sidebar_font = 15
    
    # Colors
    background_color = "#070705"
    font_color = "#e1e1e1"
    active_tab_color = "#242726"
    sidebar_color = "#161716"
    hover_color="#353a3a"
    
    # Justify text center tag
    justify_center = 1


    # Default constructor
    def __init__(self):
        # Call parent constructor
        super().__init__()
        
        # Set background color
        self.configure(fg_color=self.background_color)

        # Set window title and size
        self.title("WAGS Application")
        self.geometry(f"{self.width}x{self.height}")
        
        # Disable ability to resize window
        self.resizable(False, False)
        
        

        # 5x5 grid layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure((1, 2, 3), weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure((1, 2, 3), weight=1)
        


        # Create sidebar frame
        self.sidebar_f = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.sidebar_color)
        # Place in (1, 0) and span down 4 rows
        self.sidebar_f.grid(row=1, column=0, rowspan=4, sticky="nsew")
        self.sidebar_f.grid_rowconfigure(4, weight=1)

        # Opening logo img in "..\assets\images"
        self.logo = customtkinter.CTkImage(Image.open(f"{self.parent_dir}\\assets\\images\\WAGS_logo.png"),
                                           size=(140, 40))
        
        # Opening run button img in "..\assets\images"
        self.run_button_img = customtkinter.CTkImage(Image.open(f"{self.parent_dir}\\assets\\images\\run_button.png"), 
                                                     size=(40, 40))
        
        # Opening stop button img in "..\assets\images"
        self.stop_button_img = customtkinter.CTkImage(Image.open(f"{self.parent_dir}\\assets\\images\\stop_button.png"),
                                                      size=(40, 40))

        # Creating label for logo, filling with blue background
        # Place in (0,0) grid coordinate
        self.logo_l = customtkinter.CTkLabel(self, fg_color=self.sidebar_color, corner_radius=0, text="", image=self.logo, height=50)
        self.logo_l.grid(row=0, column=0, sticky="nsew")
        
        # Creating main display page framework
        self.mainpage_f = customtkinter.CTkFrame(self, width=400, height=600)
        self.mainpage_f.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew", padx=5)

        # Main text field in mainpage_f
        self.main_text = customtkinter.CTkTextbox(self.mainpage_f, fg_color=self.background_color, corner_radius=0, text_color=self.font_color, 
                                                  font=("Arial", 14), cursor="arrow", activate_scrollbars=True, height=600, wrap="word")

        # Button height
        height_b = 75
        
        # Creating sidebar buttons #
        self.welcome_b = customtkinter.CTkButton(self.sidebar_f, corner_radius=0, height=height_b, border_spacing=10, text="Welcome", 
                                                 command=lambda : self.change_page("welcome"), font=customtkinter.CTkFont(size=self.sidebar_font, weight="bold"),
                                                 fg_color=self.active_tab_color, hover_color=self.hover_color, anchor="w", text_color=self.font_color)
        self.welcome_b.grid(row=0, column=0, sticky="ew")

        self.features_b = customtkinter.CTkButton(self.sidebar_f, corner_radius=0, height=height_b, border_spacing=10, text="Features", 
                                                 command=lambda : self.change_page("features"), font=customtkinter.CTkFont(size=self.sidebar_font, weight="bold"),
                                                 fg_color="transparent", hover_color=self.hover_color, anchor="w", text_color=self.font_color)
        self.features_b.grid(row=1, column=0, sticky="ew")

        self.wiki_b = customtkinter.CTkButton(self.sidebar_f, corner_radius=0, height=height_b, border_spacing=10, text="Wiki", 
                                                 command=lambda : self.change_page("wiki"), font=customtkinter.CTkFont(size=self.sidebar_font, weight="bold"),
                                                 fg_color="transparent", hover_color=self.hover_color, anchor="w", text_color=self.font_color)
        self.wiki_b.grid(row=2, column=0, sticky="ew")
        
        self.tips_b = customtkinter.CTkButton(self.sidebar_f, corner_radius=0, height=height_b, border_spacing=10, text="Tips", 
                                                 command=lambda : self.change_page("tips"), font=customtkinter.CTkFont(size=self.sidebar_font, weight="bold"),
                                                 fg_color="transparent", hover_color=self.hover_color, anchor="w", text_color=self.font_color)
        self.tips_b.grid(row=3, column=0, sticky="ew")

        # Use text box to fill all of mainpage_f
        self.main_text.pack(expand=True, fill="both")
        # Insert welcome text
        self.main_text.insert("0.0", self.text_dict.get("welcome"))
        # Add tag to align text to center
        self.main_text.tag_add(self.justify_center, "0.0", "end")
        self.main_text.tag_config(self.justify_center, justify=customtkinter.CENTER)
        # Disable editing of the text box
        self.main_text.configure(state="disabled")
        
        # Variable to track what text is currently being displayed
        self.current_page = self.text_dict.get("welcome")
        
        
        
        # Bottom bar frame
        self.bottom_f = customtkinter.CTkFrame(self, fg_color=self.background_color, corner_radius=5, height=50, width=560)
        self.bottom_f.grid(row=4, column=1, sticky="nsew", padx=5, pady=7, columnspan=3)
        # Configure bottom frame to be 3x1
        self.bottom_f.columnconfigure((1, 2, 3), weight=1)
        
        
        # Left bottom frame
        self.left_bottom_f = customtkinter.CTkFrame(self.bottom_f, fg_color=self.background_color, corner_radius=5, width=220, height=50)
        self.left_bottom_f.grid(row=1, column=1, columnspan=1)
        
        # Bottom-left frame text box, displays most recent command executed
        self.last_comm_text = customtkinter.CTkTextbox(self.left_bottom_f, fg_color=self.sidebar_color, corner_radius=5, width=220, height=50,
                                                       cursor="arrow", font=customtkinter.CTkFont(size=13), text_color=self.font_color,
                                                       wrap="word", activate_scrollbars=True)
        self.last_comm_text.pack(fill="x")
        
        # Insert default text
        self.last_comm_text.insert("0.0", "Last Command:\n")
        # Disable editing of the text box
        self.last_comm_text.configure(state="disabled")
        
                
        # Right bottom frame
        self.right_bottom_f = customtkinter.CTkFrame(self.bottom_f, fg_color=self.sidebar_color, corner_radius=5)
        self.right_bottom_f.grid(row=1, column=2, columnspan=2, sticky="nsew")
        
        
        # Creating label for run_button image
        self.run_button = customtkinter.CTkButton(self.right_bottom_f, cursor="hand2", fg_color="transparent", corner_radius=5, text="", image=self.run_button_img, 
                                                  command=lambda : self.change_button(), hover=False, height=40, width=50)
        self.run_button.pack(side="left", padx=(1/2))
        
        # Status indicator text box
        self.status_text = customtkinter.CTkTextbox(self.right_bottom_f, fg_color=self.sidebar_color, height=40, width=260,
                                                    font=customtkinter.CTkFont(size=25), text_color=self.font_color, cursor="arrow", 
                                                    padx=2, pady=2, activate_scrollbars=False)
        self.status_text.pack(side="left")
        
        # Insert default text
        self.status_text.insert("0.0", "Click Button To Run")
        # Disable editing of the text box
        self.status_text.configure(state="disabled")


    # Change the text displayed on mainpage_f
    def change_page(self, page):
        # If the current page has not been selected (wiki page will refresh no matter what)
        if self.text_dict.get(page) != self.current_page or page == "wiki":            
            # Set active tab's color, reset previously active tab to transparent
            if page == "welcome": self.welcome_b.configure(fg_color=self.active_tab_color)
            else: self.welcome_b.configure(fg_color="transparent")
            
            if page == "features": self.features_b.configure(fg_color=self.active_tab_color)
            else: self.features_b.configure(fg_color="transparent")
            
            # If wiki page
            if page == "wiki": 
                self.wiki_b.configure(fg_color=self.active_tab_color)
                # Open appText json and get wiki page text
                with open(f"{self.parent_dir}\\assets\\data\\appText.json") as f:
                    data = f.read()
                    self.text_dict = ast.literal_eval(data)
            else: self.wiki_b.configure(fg_color="transparent")
            
            if page == "tips": self.tips_b.configure(fg_color=self.active_tab_color)
            else: self.tips_b.configure(fg_color="transparent")

            # Configure text to editable
            self.main_text.configure(state="normal")
            # Delete previous text
            self.main_text.delete("0.0", "end")
            # Insert new text
            self.main_text.insert("0.0", self.text_dict.get(page))
            # Add tag to align text to center
            self.main_text.tag_add(self.justify_center, "0.0", "end")
            self.main_text.tag_config(self.justify_center, justify=customtkinter.CENTER)
            # Reconfigure back to non-editable
            self.main_text.configure(state="disabled")
            # Set current text to updated text
            self.current_page = self.text_dict.get(page)
        
    def change_button(self):
        """Changes run/stop button depending on current running status
        """       
        # if not running
        if not self.isRunning:
            # if the assistant is not still running
            if self.ensure_assistant_stop():
                # Disable button while changing settings
                self.run_button.configure(state="disabled")
                
                # change current status and button
                self.isRunning = True
                self.run_button.configure(image=self.stop_button_img)
                
                # Change status text
                self.status_text.configure(state="normal")
                self.status_text.delete("0.0", "end")
                self.status_text.insert("0.0", "Click Button to Stop")
                self.status_text.configure(state="disabled")

                # Create new thread to execute run_app()
                self.assistant_thread = threading.Thread(target=self.run_app)
                self.assistant_thread.daemon = True
                # Run assistant on new thread
                self.assistant_thread.start()
                
                # Allow 3 second buffer for assistant to start properly
                self.after(3000, lambda: self.run_button.configure(state="normal"))

        
        # else, it is running
        else:
            # Disable button while changing settings
            self.run_button.configure(state="disabled")
            # change current status and button
            self.isRunning = False
            
            self.status_text.configure(state="normal")
            self.status_text.delete("0.0", "end")
            self.status_text.insert("0.0", "Click Button to Run")
            self.status_text.configure(state="disabled")
            
            # Change state and image
            self.run_button.configure(state="normal", image=self.run_button_img)
            
        
            
    def ensure_assistant_stop(self):
        """Ensures that the previous thread dedicated to the assistant has ended terminated

        Returns:
            boolean: False if still running, True if it has ended
        """
        # If the previous thread is still running
        if self.assistant_thread.is_alive(): 
            # Display warning message       
            tkinter.messagebox.showwarning(title="Warning", message="The previous assistant is still shutting down.\nPlease wait a few seconds and try running again.")

            # Return false to indicate that a new thread should not be created
            return False
        
        else:
            # The assistant has stopped
            return True
        
    
    def run_app(self):
        """Runs assistant on a new daemon thread
        """
        # While the system is running
        while self.isRunning:
            # Trigger assistant listener
            result = assistant.run_assistant(self.recognizer, self.mic)
            
            # Update last command box
            if result != None:
                # Configure text to editable
                self.last_comm_text.configure(state="normal")
                # Delete previous text
                self.last_comm_text.delete("0.0", "end")
                # Insert new text
                self.last_comm_text.insert("0.0", "Last Command:\n" + result)
                # Reconfigure back to non-editable
                self.last_comm_text.configure(state="disabled")
        # Exit thread
        sys.exit()
                
    
    def on_close(self):
        """
        Destructor for the application
        Resets wiki page text to default value
        """
        # Set wiki text to default
        self.text_dict["wiki"] = "\n\n\n\n\nAsk WAGS to look something up and it will be displayed here! \n\nTry saying: \"Hey WAGS, what is Truman State University?\"\n\nIf you're expecting something to be displayed here that isn't,\npress the 'Wiki' tab button on the left to refresh"

        # Restore in file
        with open(f"{self.parent_dir}\\assets\\data\\appText.json", "w") as output:
            json.dump(self.text_dict, output)

        # Close app
        self.destroy()


        

# For running application
if __name__ == "__main__":
    app = AppWAGS()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.eval('tk::PlaceWindow . center')
    app.mainloop()