with open("cmd_config", "r") as fo:
    lines = fo.readlines()

sections = {}
current_section = None

# Parse the file and store sections in a dictionary
for line in lines:
    if line.startswith("CONFIG "):
        current_section = line.strip()
        sections[current_section] = []
    elif current_section:
        sections[current_section].append(line)

# Output sections and handle user input
while True:
    x = input("****** Select what you want ('q' to quit): ")

    if x == 'q':
        break

    found_section = None

    for section, content in sections.items():
        if x in section:
            found_section = section
            break

    if found_section:
        print("\n********** CONTENT OF SECTION ************\n")
        for line in sections[found_section]:
            print(line, end="")
    else:
        print("Section not found. Please try again.")
