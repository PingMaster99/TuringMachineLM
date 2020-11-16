"""
    TuringMachine.py

    Contains the required functions to run a deterministic
    Turing Machine.

    Mathematical Logic test # 5

    Isabel Ortiz        (isaonaranjo)
    Douglas de León     (DouglasDL28)
    Pablo Ruiz 18259    (PingMaster99)

    Version 1.0
    Updated November 16, 2020
"""


class TuringMachine(object):
    """
        This class generates a deterministic Turing Machine
    """
    def __init__(self, input_file):

        # Machine alphabet
        self.accepted_symbols = []

        # Machine states
        self.states = {}
        self.build_machine()

        # Current state and character
        self.current_state = "q0"
        self.current_character = None

        # Accepted symbols and operating characters to calculate
        self.operating_characters = []
        self.generate_operating_characters(input_file)

        # Maximum depth (exits the calculation in case of an infinite loop)
        self.depth_constant = 100
        self.maximum_depth = self.depth_constant
        self.current_depth = 0

        # Pointers to the location of the state and current character in operating_characters
        self.state_location = 0
        self.character_location = 1

    def build_machine(self, input_file="states.txt"):
        self.states = {}
        self.accepted_symbols = []
        start = True
        file = open(input_file)

        for line in file.readlines():
            component_index = 0
            if start:
                self.accepted_symbols = line.strip("\n").split(" ")
                start = False
                continue
            if line[0] == "\n":
                continue

            line = line.strip("\n").split(" ")
            state = line[0]
            self.states[state] = {}
            line.pop(0)
            line.pop(0)
            current_component = ""
            for component in line:
                if(component_index % len(self.accepted_symbols)) == 0:
                    current_component = component
                    self.states[state][component] = []
                    component_index += 1
                    continue
                if component != "":
                    self.states[state][current_component].append(component)
                component_index += 1

    def generate_operating_characters(self, input_file):
        """
        Builds the operating characters of the Turing Machine
        to a form legible by the program from the input string
        :param input_file: file that contains the input string
        """

        # If the machine has calculated another file before, it is reset
        if len(self.operating_characters) > 0:
            self.operating_characters.clear()

            # Current state and character
            self.current_state = "q0"
            self.current_character = None

            # Maximum depth (exits the calculation in case of an infinite loop)
            self.maximum_depth = self.depth_constant
            self.current_depth = 0

            # Pointers to the location of the state and current character in operating_characters
            self.state_location = 0
            self.character_location = 1

        file = open(input_file)
        character_string = file.readlines()[0]

        for character in character_string:
            # Appends known characters to self.operating_characters
            if character in self.accepted_symbols:
                self.operating_characters.append(character)
            # Leaves the list empty if there is an unknown symbol
            elif character != "\n":
                self.operating_characters = []
                break
        if len(self.operating_characters) > 0:
            self.operating_characters.insert(0, self.current_state)
            self.current_character = self.operating_characters[1]

    def calculate(self, output_file="output.txt"):
        output = open(output_file, "w+")
        if self.states is None:
            print("No se proporcionó un archivo de entrada!")
            return False

        # Additional blank spaces at the end of the strip
        remove_blank_space = False

        # Initial state
        current_progress = ""
        print(str(self.current_depth) + ".", current_progress.join(self.operating_characters))

        # The machine will only calculate if it's not in an acceptation state or a rejection state and the maximum
        # recursion depth has not been reached. It won't calculate if the input string has invalid characters.
        while self.current_state != "qaccept" and self.current_state != "qreject" and \
                (self.maximum_depth > self.current_depth) and len(self.operating_characters) > 0:

            operation_list = self.states[self.current_state][self.current_character]
            new_state = operation_list[0]
            new_character = operation_list[1]
            rotation = operation_list[2]

            if rotation == "R":
                if self.state_location == (len(self.operating_characters) - 2) and not remove_blank_space:
                    remove_blank_space = True
                if self.state_location >= len(self.operating_characters) - 2:
                    self.operating_characters.append("_")

                # Rotates to the right
                self.operating_characters[self.state_location], self.operating_characters[self.character_location] = new_character, new_state
                # Updates location indexes
                self.state_location += 1
                self.character_location = self.state_location + 1

            elif rotation == "L":
                if self.state_location == 0:
                    # Leftmost part of input, no rotation is required
                    self.operating_characters[self.state_location], self.operating_characters[self.character_location] = new_state, new_character
                else:
                    # Writes the new character
                    self.operating_characters[self.character_location] = self.current_character
                    # Rotates to the left
                    self.operating_characters[self.state_location - 1], self.operating_characters[self.state_location] = new_state, self.operating_characters[self.state_location - 1]
                    # Updates location indexes
                    self.state_location -= 1
                    self.character_location = self.state_location + 1

            else:
                # No rotation
                self.operating_characters[self.state_location], self.operating_characters[self.character_location] = new_state, new_character

            # Current state update
            self.current_state = self.operating_characters[self.state_location]

            # Current character update
            self.current_character = self.operating_characters[self.character_location]

            # Loop update
            self.current_depth += 1

            # Progress print
            current_progress = ""
            output_progress = str(self.current_depth) + "." + " " + current_progress.join(self.operating_characters)

            if remove_blank_space:
                output_progress = output_progress[0: len(output_progress) - 1]

            print(output_progress)
            output.write(output_progress + "\n")

        if remove_blank_space and self.operating_characters[len(self.operating_characters) - 1] == "_":
            self.operating_characters.pop()

        if self.maximum_depth == self.current_depth:
            self.operating_characters.append("\n(Infinite loop)")
            print("Infinite loop")

        # Generates the output file
        file_output = ""
        output.write("Final state: " + file_output.join(self.operating_characters) + "\n")

