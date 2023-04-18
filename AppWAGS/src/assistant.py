import speech_recognition as sr
import os
import ast
import commands
import pyttsx3 as tts

# Parent directory path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Engine for text to speech output
engine = tts.init()

def get_instruction(recognizer, mic):
    """Continually listens to mic and returns instruction with trigger statement removed

    Args:
        recognizer (sr.Recognizer): speech recognition object
        mic (sr.Microphone): microphone object

    Returns:
        string: instruction detected by the recognizer through the user's microphone
    """
    try:
        # Set mic as source and listen
        with mic as src:
            # Try to listen for 3 seconds, max of 5
            audio = recognizer.listen(source=src, timeout=3.0, phrase_time_limit=5.0)
        
        # Try to recognize
        try:
            instruction = " "
            instruction = recognizer.recognize_google(audio)
            
        # Speech not recognized
        except sr.UnknownValueError:
            return None
        # Google Speech API error
        except sr.RequestError:
            return "ERROR: Exception Thrown"
            
        # Return instruction, if it contains 'wags'
        if "wags" in instruction.lower():
            return instruction[(instruction.lower().find("wags") + 5):]
        else:
            return None
        
    # No speech recognized in the time allotted
    except sr.WaitTimeoutError:
        return None
    # Input/Output error occurred
    except IOError:
        engine.say("No default microphone selected. Refer to the Microphone Setup section in the Tips tab to learn how to select one")
        engine.runAndWait()
        return None


def get_command(instruction):
    """Returns command type based on set triggers in \assets\features.json

    Args:
        instruction (string): raw instruction from microphone input

    Returns:
        tuple (string, string): tuple containing (command type, trigger phrase)
    """
    
    # Open features.json
    with open(f"{parent_dir}\\assets\\data\\features.json") as f:
        # Read data
        feature_data = f.read()
    # Convert to dictionary
    feature_dict = ast.literal_eval(feature_data)
    
    # For each dictionary in the features section
    for option in feature_dict["features"]:
        # For each trigger statement
        for trigger in option["triggers"]:
            # If the trigger is within the instruction
            if trigger in instruction:
                # Return the current command type
                return (option["type"], trigger)
        
    # No triggers matched
    return ("NULL", "NULL")


def run_command(command_info, instruction):
    """Runs respective assistant feature

    Args:
        command_info (String): Type of command triggered
        instruction (String): Actual instruction given by the user
    """
    if (command_info[0] == "search"):
        commands.open_wiki(instruction, trigger=command_info[1])
    elif (command_info[0] == "greeting"):
        commands.greeting()
    elif (command_info[0] == "open"):
        commands.open_window(instruction, trigger=command_info[1])
    elif (command_info[0] == "close"):
        commands.close_window(instruction, trigger=command_info[1])
    elif (command_info[0] == "logoff"):
        commands.log_off()
    elif (command_info[0] == "shutdown"):
        commands.shut_down()
    elif(command_info[0] == "add note"):
        commands.add_note("", "")
    elif(command_info[0] == "edit note"):
        commands.select_note("edit")
    elif(command_info[0] == "delete note"):
        commands.select_note("delete")
    elif(command_info[0] == "read note"):
        commands.select_note("read")
    


def run_assistant(recognizer, mic):
    """Runs virtual assistant by listening for trigger statements from user
    
    Args:
        recognizer (sr.Recognizer): Speech recognizer
        mic (sr.Microphone): Microphone for speech recognition
        
    Returns:
        String: The actual instruction given by the user
    """
    
    # Gather raw voice instruction from the user
    raw_instruction = get_instruction(recognizer, mic)
    
    # If no instruction was given
    if raw_instruction == None:
        return None
    # If an exception was thrown
    elif raw_instruction == "ERROR: Exception Thrown":
        return "An error occurred, please try again"
    # Otherwise, valid command
    else:
        # Parse command information
        command_info = get_command(raw_instruction)
        
        # Run respective command
        run_command(command_info, raw_instruction)
        
        # Return heard command
        return raw_instruction