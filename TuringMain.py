"""
    TuringMain.py

    Runs a Turing Machine based off the input of 3 files
    It produces 3 output files with an acceptation result, a
    rejection result, and an infinite loop result.

    Isabel Ortiz        (isaonaranjo)
    Douglas de León     (DouglasDL28)
    Pablo Ruiz 18259    (PingMaster99)

    Version 1.0
    Updated November 16, 2020
"""
from TuringMachine import *

# Accepted input
print("\n************************\n     Accepted input \n************************")
t = TuringMachine("./Inputs/accepted_input.txt")
t.calculate(output_file="./Outputs/accepted_output.txt")

# Rejected input
print("\n************************\n     Rejected input \n************************")
t.generate_operating_characters("./Inputs/rejected_input.txt")
t.calculate(output_file="./Outputs/rejected_output.txt")

# Infinite loop input
print("\n************************\n  Infinite loop input \n************************")
t.generate_operating_characters("./Inputs/loop_input.txt")
t.calculate(output_file="./Outputs/loop_output.txt")
