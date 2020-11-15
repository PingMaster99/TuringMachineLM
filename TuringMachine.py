class TuringMachine(object):
    """
        This class generates a deterministic Turing Machine
    """
    def __init__(self, input_file):
        #self.states = ["q0", "q1", "q2", "q3", "q4", "qaccept", "qreject"]

        # Machine states
        self.states = {
            "q0": {"a": ["a", "q0", "R"], "b": [], "c": [], "_": ["_", "qaccept", "R"]},
            "q1": {"a": [], "b": [], "c": []}
        }

        # Current state and character
        self.current_state = "q0"
        self.current_character = None

        # Accepted symbols and operating characters to calculate
        self.accepted_symbols = ["a", "b", "3", "4", "5"]
        self.operating_characters = []
        self.generate_operating_characters(input_file)

        # Maximum depth (exits the calculation in case of an infinite loop)
        self.maximum_depth = 100
        self.current_depth = 0

        # Pointers to the location of the state and current character in operating_characters
        self.state_location = 0
        self.character_location = 1

    def generate_operating_characters(self, input_file):
        """
        Builds the operating characters of the Turing Machine
        to a form legible by the program from the input string
        :param input_file: file that contains the input string
        """
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

    def calculate(self):

        # The machine will only calculate if it's not in an acceptation state or a rejection state and the maximum
        # recursion depth has not been reached. It won't calculate if the input string has invalid characters.
        remove_blank_space = False
        while self.current_state != "qaccept" and self.current_state != "qreject" and \
                (self.maximum_depth >= self.current_depth) and len(self.operating_characters) > 0:

            operation_list = self.states[self.current_state][self.current_character]
            new_character = operation_list[0]
            new_state = operation_list[1]
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

        if remove_blank_space and self.operating_characters[len(self.operating_characters) - 1] == "_":
            self.operating_characters.pop()

        if self.maximum_depth == self.current_depth:
            self.operating_characters = ["Infinite loop"]

        # Generates the output file
        file_output = ""
        output = open("output.txt", "w+")
        output.write(file_output.join(self.operating_characters))

