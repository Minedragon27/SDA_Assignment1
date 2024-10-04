import time
import keyboard  # Library to capture keyboard input
from GUI import GUI
from Camera import Camera

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


# Create state instances
def custom_on_step():
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

def stepSearchObject():
    shapes=camera.getShapes()
    gui.AddShapes(shapes)
    if gui.GetShapes().count==0:    return
    return User_input

def entryUserInput():
    gui.resetTimer()

search_object= State(
    name="search object",
    step_func=stepSearchObject
)
User_input= State(   # unfinished state
    name="User input",
    entry_func=entryUserInput 
)
# Initialize the state machine with Off state initially
state_machine = StateMachine(initial_state=off_state)
camera=Camera()
gui=GUI()


# Run the state machine in a loop
try:
    print("Press 'o' for human presence, 'n' for no human.")
    state_machine.run()
except KeyboardInterrupt:
    print("State machine stopped.")
