import time
import keyboard  # Library to capture keyboard input
from GUI import GUI
from Camera import Camera
import pygame
from pygame.locals import *
import sys
import DoBotArm as dbt
from serial.tools import list_ports
import threading

class State:
    """Base class for all states in the state machine."""
    def __init__(self, name, entry_func=None, step_func=None, leave_func=None):
        self.name = name
        self.entry_func = entry_func if entry_func else self.default_entry
        self.step_func = step_func if step_func else self.default_step
        self.leave_func = leave_func if leave_func else self.default_leave

    def entry(self):
        """Executes the entry function (custom or default)."""
        self.entry_func()

    def step(self):
        """Executes the step function (custom or default)."""
        return self.step_func()

    def leave(self):
        """Executes the leave function (custom or default)."""
        self.leave_func()

    def default_entry(self):
        print(f"Entering {self.name} state")

    def default_step(self):
        print(f"Running {self.name} state")
        return None  # Return None by default, indicating no state change

    def default_leave(self):
        print(f"Leaving {self.name} state")


class StateMachine:
    """State machine to manage states and transitions."""
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.entry()

    def step(self):
        """Execute one step of the state machine."""
        next_state = self.current_state.step()

        if next_state:
            self.transition_to(next_state)

    def transition_to(self, next_state):
        """Handle the transition to the next state."""
        if isinstance(next_state, State):
            self.current_state.leave()
            self.current_state = next_state
            self.current_state.entry()
        else:
            print(f"State '{next_state}' not recognized!")

    def run(self):
        """Run the state machine in a loop."""
        while True:
            self.step()
            time.sleep(0.5)  # Simulate a time delay in each iteration


# example states and functions

def custom_off_step():
    print("Human detected, lights ON.")
    # Keep checking for input to turn off
    if keyboard.is_pressed('n'):  # Simulate no human detected
        return off_state
    return None  # Stay in the On state

off_state = State(
    name="Off",
    entry_func=lambda: print("Lights are already OFF"),
    step_func=custom_off_step
)

#state functions

def stepSearchObject():
    shapes=camera.getShapes()
    gui.addShapes(shapes)
    if gui.getShapes().count==0:  return
    return userInputState

def entryUserInput():
    gui.resetTimer()

def stepUserInput():
    for event in pygame.event.get():
        if event.type==shapeSelectedType:
            gui.selectShape(event.shape)
            return moveArmToObjectState
    if gui.checkTimer(100): return searchObjectState        

def stepMoveArmToObject():
    if dobot.getPosition()==gui.getSelectedShape().getCenter():
        return placeOnConveyorState
    
def entryPlaceOnConveyor():
    gui.dobot.toggleSuction()
    x,y=gui.getSelectedShape().getCenter()
    dobot.moveArmXYZ(x,y,gui.getSelectedShape().getDepth())
#States

searchObjectState= State(
    name="search object",
    step_func=stepSearchObject
)
userInputState= State(   
    name="User input",
    entry_func=entryUserInput ,
    step_func=stepUserInput
)
moveArmToObjectState= State(
    name="move arm to object",
    step_func=stepMoveArmToObject
)
placeOnConveyorState= State(
    name="place on conveyor",
    entry_func=entryPlaceOnConveyor
)

# Initialize the objects and pygame
pygame.init()
state_machine = StateMachine(initial_state=searchObjectState)
camera=Camera()

homeX, homeY, homeZ = 170, 0, 0
dobot = dbt.DoBotArm("COM3", homeX, homeY, homeZ, home= False)

gui=GUI(pygame.display.set_mode((0, 0), pygame.FULLSCREEN))

shapeSelectedType=USEREVENT+1


def main():

    end=False
    # Run the state machine in a loop
    while True:

        try:
            events=pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    end=True
                if event.type==MOUSEBUTTONDOWN:
                    for shape in gui.getShapes():
                        if shape.clickedOn():
                            shapeSelected=pygame.event.Event(shapeSelectedType,shape=shape) # creates event and attaches the shape that was clicked on
                            pygame.event.post(shapeSelected) # posts the event
                            break # break so it doesnt go to multiple shapes if they overlap
            
            if end==True: #User has quit
                pygame.quit()
                sys.exit()
                break
            state_machine.step()

        except KeyboardInterrupt:
            break


main()