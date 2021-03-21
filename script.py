from fpdf import FPDF
import subprocess
import argparse

def add_to_pdf(pdf, text, give_fill):

    line = ""
    for i in range(0, len(text)):
        if text[i] == '\n':
            pdf.multi_cell(200, 5, txt = line, border = 0, align = 'L', fill = give_fill)
            line = ""
        else:
            line += text[i]    


# Parse arguments
parser = argparse.ArgumentParser(description = "Code file to PDF with output.")
parser.add_argument('path_code_file', metavar = 'p', type = str, help = "Specify path to code file")
parser.add_argument('run_command', metavar = 'r', type = str, help = "Specify the command to run your program/script")
parser.add_argument('output_pdf', metavar = 'o', type = str, help = "Specify name of the generated pdf")
args = parser.parse_args()

# Prompt for description
print("All right! Here is what you gave.")
print("Path to your code file: " + args.path_code_file)
print("Command to run your program/script: " + args.run_command)
print("Name of the generated pdf: " + args.output_pdf)
print("Provide a description (this will be the first thing in your pdf).")
print("Press CTRL + D to stop the input.")

description = ""
while True:
    try:
        line = input()
        line += '\n'
    except EOFError:
        break
    description += line

print("All right! Here is your description.")
print(description)

# Validate or exit
go = int(input("Let's begin? (1/0): "))
if go == 0:
    sys.exit('Bye :( ')

# Get code from the code file
code = "Code\n"
with open(args.path_code_file, "r") as code_file:
    content = code_file.readlines()
    for line in content:
        code += line

# Run the program/script and collect output
output = "\nOutput\n"
subprocess.run("script -q -c \'" + args.run_command + "\' output.txt", shell=True)

with open("output.txt", "r") as output_file:
    content = output_file.readlines()
    for line in content:
        check_one = line.startswith("Script started on")
        check_two = line.startswith("Script done on")
        if (check_one or check_two) == False:
            output += line


# PDF generation starts!
pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", 'B', 12) # description is Arial, bold, font size = 12
add_to_pdf(pdf, description, False)


pdf.set_fill_color(0, 0, 0)
pdf.set_text_color(255,255,255)
pdf.set_font("Courier", 'B', 12) # code is Courier, bold, font size = 12
add_to_pdf(pdf, code, True)

add_to_pdf(pdf, "\n", False) # blank space

pdf.set_font("Courier", size=12) # output is not bold
add_to_pdf(pdf, output, True)

# Generation ends
pdf.output(args.output_pdf)

print("Find the pdf in the current directory.")
print("You are welcome.")
print("Goodbye!")
