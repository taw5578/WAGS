import wikipedia
import json
import os
import ast
import random
import AppOpener
import os
import pyttsx3 as tts
import tkinter
import customtkinter

# Parent directory file path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Engine for text to speech output
engine = tts.init()

def open_wiki(instruction, trigger):
    """Opens and displays desired wikipedia page in the 'Wiki' tab section

    Args:
        instruction (string): instruction from the user
        trigger (string): the trigger phrase used to invoke this command
    """
    
    # Open and read current appText json data
    with open(f"{parent_dir}\\assets\\data\\appText.json") as f:
        text_data = f.read()
        
    # Convert to a dictionary
    text_dict = ast.literal_eval(text_data)

    # Remove trigger phrase from instruction and store the topic to be searched
    topic = instruction[(instruction.find(trigger) + len(trigger) + 1):]
    
    try:
        # Generate wiki page from topic
        wiki_page = wikipedia.page(topic)
    
        # 'Wiki' tab with wikipedia page information
        # Include the title, content, and url
        text_dict["wiki"] = f"\n{wiki_page.title}\n\n{wiki_page.content}\n\n\n{wiki_page.url}"
        
        # Write the new dictionary to appText.json
        with open(f"{parent_dir}\\assets\\data\\appText.json", "w") as output:
            json.dump(text_dict, output)
            
        # Verbally inform the user the Wiki tab has been updated
        engine.say(f"I've opened the {topic} Wikipedia page in the Wiki tab. Click the Wiki tab button now to refresh or navigate to the page.")
    
    # Topic is too broad
    except wikipedia.DisambiguationError:
        engine.say(f"The term {topic} is to broad for a search. Please try to be more specific.")
    # Topic does not exist on Wikipedia as a page
    except wikipedia.PageError:
        engine.say(f"The term {topic} returned no matching Wikipedia pages.")
    # Some redirect occurred
    except wikipedia.RedirectError:
        engine.say(f"The term {topic} resulted in an unexpected redirect. Please try another term.")
    # Some other wikipedia error occurred
    except wikipedia.WikipediaException:
        engine.say("I didn't catch that. Please try searching again.")
    
    # Run tts
    engine.runAndWait()


def greeting():
    """
    Gives random generic greeting to the user using text-to-speech
    """
    # Possible responses
    responses = ["Hi, how are you?", "Hello", "Hi there, I'm doing great", "Hello there"]
    # Start tts engine and say a random greeting
    engine.say(random.choice(responses))
    engine.runAndWait()
    
def open_window(instruction, trigger):
    """Opens a specified application in a new window

    Args:
        instruction (string): instruction from the user
        trigger (string): the trigger phrase used to invoke this command
    """
    # List of available apps
    app_list = ["chrome", "google chrome", "microsoft edge", "edge", "firefox", "slack", "steam", "visual studio code", "vscode",
                "spotify", "discord", "snipping tool", "zoom"]
    
    # Partition user's requested app
    app = instruction[(instruction.find(trigger) + len(trigger) + 1):]
    
    # If the app exists within the system
    if app.lower() in app_list:
        # Run and confirm verbally
        engine.say(f"Opening {app}")
        engine.runAndWait()
        AppOpener.open(app, match_closest=True)
    else:
        # Otherwise, app DNE or user didn't use the full name
        engine.say(f"I was unable to open {app}. Please reference the Features page for a list of available apps to open or close.")
        engine.runAndWait()
    
def close_window(instruction, trigger):
    """Closes a specified application in a new window

    Args:
        instruction (string): instruction from the user
        trigger (string): the trigger phrase used to invoke this command
    """
    
    # List of available apps
    app_list = ["chrome", "google chrome", "microsoft edge", "edge", "firefox", "slack", "steam", "visual studio code", "vscode",
                "spotify", "discord", "snipping tool", "zoom"]
    
    # Partition user's requested app
    app = instruction[(instruction.find(trigger) + len(trigger) + 1):]
    
    # If the app exists within the system
    if app.lower().strip() in app_list:
        # Close and confirm verbally
        engine.say(f"Exiting {app}")
        engine.runAndWait()
        AppOpener.close(app, match_closest=True)
    else:
        # Otherwise, app DNE or user didn't use the full name
        engine.say(f"I was unable to close {app}. Please reference the Features page for a list of available apps to open or close.")
        engine.runAndWait()
       
def verify_choice(type):
    """Verifies user choice of logging of or shutting down

    Args:
        type (string): Choice type (shut down or log off)

    Returns:
        _type_: User's decision
    """
    # Inform the user
    engine.say(f"Please confirm your choice to " + type)
    engine.runAndWait()
    # Verify user result
    result = tkinter.messagebox.askyesno(title="Warning", message=f"Confirm your choice to {type}")
    # Return user choice
    return result
        
def log_off():
    """Logs user off after confirming choice
    """
    # Verify user choice
    if verify_choice("log off"):
        engine.say("Logging you off. Goodbye")
        engine.runAndWait()
        # Log off
        os.system("shutdown -l")
    else:
        engine.say("Log off cancelled")
    
    # Inform user of action
    engine.runAndWait()
    
def shut_down():
    """Shuts down computer after confirming choice
    """
    # Verify user choice
    if verify_choice("shut down"):
        engine.say("Shutting down. Goodbye")
        engine.runAndWait()
        # Shut down
        os.system("shutdown -s")
    else:
        engine.say("Shut down cancelled")
        
    # Inform user of action
    engine.runAndWait()
    
def focus_next(event):
    """Advance widget focus to next widget

    Args:
        event (KeyPress): Event sent by pressing Tab key
    """
    event.widget.tk_focusNext().focus()
    return("break")
    
def add_note(title, desc):
    """Open popup to allow for note info entry

    Args:
        title (String): Existing note title
        desc (String): Existing note description
    """
    #Inform user window has opened
    engine.say("Opening note entry window")
    
    # Top level for mutli window GUI
    root = customtkinter.CTkToplevel()
    width = 400
    height = 400
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate x and y cord for window to be placed
    x_coord = int((screen_width/2) - (width/2))
    y_coord = int((screen_height/2) - (height/2))
    
    # Place window
    root.geometry("{}x{}+{}+{}".format(width, height, x_coord, y_coord))
    
    # Frame for note entry
    frame = customtkinter.CTkFrame(root, width=width, height=height)
    frame.pack_propagate(False)
    frame.pack(fill=customtkinter.BOTH, expand=True)
    
    # Force to front
    root.focus_force()
    
    # Set title and size
    root.title("Enter a title and description")
    
    # Create title label and entry
    title_label = customtkinter.CTkLabel(frame, text="Title")
    title_label.pack(pady=10)
    title_entry = customtkinter.CTkTextbox(frame, height=1, width=40)
    title_entry.insert("0.0", title)
    title_entry.pack(padx=20, pady=5, fill=customtkinter.X)
    # Change focus with tab
    title_entry.bind("<Tab>", focus_next)
    
    # Create description label and entry
    desc_label = customtkinter.CTkLabel(frame, text="Description")
    desc_label.pack(pady=10)
    desc_entry = customtkinter.CTkTextbox(frame, wrap=customtkinter.WORD)
    desc_entry.insert("0.0", desc)
    desc_entry.pack(padx=20, pady=5, fill=customtkinter.BOTH, expand=True)
    # Change focus with tab
    desc_entry.bind("<Tab>", focus_next)
    
    # Create save button
    save_button = customtkinter.CTkButton(frame, text="Save", 
                                          command= lambda: save_note(root, 
                                                                     title_entry.get(1.0, customtkinter.END), 
                                                                     desc_entry.get(1.0, customtkinter.END),
                                                                     title))
    save_button.pack(padx=20, pady=10, fill=customtkinter.X)
    
    # Configure grid geometry
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    #Run text to speech
    engine.runAndWait()
    
    
def save_note(root, title, desc, old_title):
    """Saves note to notes directory

    Args:
        root (CTkTopLevel): Note entry window object
        title (String): Name of note file
        desc (String): Contents of note file
        old_title (String): Name of old note file
    """
    # File name length limit is 50 characters
    if len(title) > 50:
        tkinter.messagebox.showwarning("Invalid Note Name",
                                       "Title length too long\n Max length is 50 characters")
        # Exit
        return
    
    # No file name entered
    if not title.strip():
        tkinter.messagebox.showwarning("Invalid Note Name",
                                       "Title of note cannot be blank")
        
        #Exit
        return
    
    # List of illegal file name characters
    illegal_chars = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', '/',
                     '$', '!', '\'', '\"', ':', '@', '+', '`', '|', '=']
    
    # For each character in the title
    for char in title:
        # If the character is illegal
        if char in illegal_chars:
            # Create message
            msg = "Note name cannot contain the following characters:\n"
            for symbol in illegal_chars:
                msg = msg + " " + symbol
            # Warn user, break loop
            tkinter.messagebox.showwarning("Invalid Note Name", msg)
            return
    
    # If there is an old note
    if len(old_title) > 0:
        # Delete it
        os.remove(f"{parent_dir}\\assets\\notes\\{old_title}.txt")
    
    # Create new note file
    with open(f"{parent_dir}\\assets\\notes\\{title.strip()}.txt", "w") as output:
        # Write to note, removing newline
        output.write(desc[:-1])
    
    # Close note entry window
    root.destroy()
    # Inform user note has been saved
    engine.say("Note saved")
    engine.runAndWait()
    
    
def select_note(action_type):
    """Allows user to select a note to edit, opening in note entry window
    """
    # List of current notes
    current_notes = os.listdir(f"{parent_dir}\\assets\\notes")
    
    # If there are no notes
    if len(current_notes) == 0:
        # Notify user, exit
        engine.say("Error, you have made no notes")
        engine.runAndWait()
        return
    
    # Inform user
    engine.say("Select which note you want to " + action_type)
    engine.runAndWait()
    
    # Top level for mutli window GUI
    root = customtkinter.CTkToplevel()
    width = 400
    height = 500
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate x and y cord for window to be placed
    x_coord = int((screen_width/2) - (width/2))
    y_coord = int((screen_height/2) - (height/2))
    
    # Place window
    root.geometry("{}x{}+{}+{}".format(width, height, x_coord, y_coord))
        
    # Scrollable frame for note entry
    frame = customtkinter.CTkScrollableFrame(root, width=width, height=height)
    frame.pack(fill=customtkinter.BOTH, expand=True)
    
    # Force to front
    root.focus_force()
    
    # Set title and size
    root.title(f"Select note to {action_type}")
    
    # If read option, button should be close
    if action_type == "read":
        cancel_close_text = "CLOSE"
    # Otherwise, it should be cancel
    else:
        cancel_close_text = "CANCEL"
    
    # Create cancel button
    cancel_button = customtkinter.CTkButton(frame, text=cancel_close_text, fg_color='#B50304', 
                                            hover_color='#850212', command=root.destroy)
    cancel_button.pack(pady=10)
    
    # Dictionary to hold note buttons
    button_dict = {}
    
    # Create button in frame for each note
    for note in current_notes:
        if action_type == "edit":
            # Open function
            def func(root=root, note=note):
                return open_note(root, note)
        elif action_type == "delete":
            # Delete function
            def func(root=root, note=note):
                return delete_note(root, note)
        elif action_type == "read":
            # Read function
            def func(root=root, note=note):
                return read_note(root, note)
        
        # Add button to dict and frame
        button_dict[note] = customtkinter.CTkButton(frame, text=note, command=func)
        button_dict[note].pack(pady=1)
        
    
def open_note(root, note):
    """Opens an existing note in the entry window

    Args:
        root (CTkTopLevel): Note selection window object
        note (String): Name of note file
    """
    # Get note title
    title = os.path.splitext(note)[0]
    desc = ""
    
    try:
        # Open note
        with open(f"{parent_dir}\\assets\\notes\\{note}") as note_f:
            # Read contents
            desc = note_f.read()
        
        # Destroy extra note window
        root.destroy()
        # Open note in add note window
        add_note(title, desc)
        
    except Exception:
        # Inform user of error
        # User likely moved file within system
        root.destroy()
        engine.say("There was an error opening the note file. Please try again")
        engine.runAndWait()
    
    
def delete_note(root, note):
    """Deletes a note in the note directory

    Args:
        root (CTkTopLevel): Note selection window object
        note (String): Name of note file
    """
    try:
        # Remove the file
        os.remove(f"{parent_dir}\\assets\\notes\\{note}")
        
        # Close window and inform muser
        root.destroy()
        engine.say("Note deleted")
        
    except FileNotFoundError:
        # Inform user file not found and close
        root.destroy()
        engine.say("The note file was not found")
        
    except Exception:
        # Some os error occurred, inform user and close
        root.destroy()
        engine.say("There was an error when deleting your note. Please try again.")
        
    # Run tts
    engine.runAndWait()
        
        
def read_note(root, note):
    """Reads a note to the user

    Args:
        root (CTkTopLevel): Note selection window object
        note (String): Name of note file
    """
    try:
        # Open chosen note
        with open(f"{parent_dir}\\assets\\notes\\{note}") as note_f:
            desc = note_f.read()
        
        # Read the note
        engine.say(desc)
        
    except FileNotFoundError:
        # Inform user file not found and close
        root.destroy()
        engine.say("The note file was not found")
        
    except Exception:
        # Some error occurred, inform user and close
        root.destroy()
        engine.say("There was an error when deleting your note. Please try again.")
      
    # Run tts  
    engine.runAndWait()