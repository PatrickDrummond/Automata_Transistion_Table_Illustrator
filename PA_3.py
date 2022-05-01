# Patrick Drummond
# 40185198
# April 14, 2021
# COMP 5361 PA 3

from PySimpleAutomata import automata_IO

########################################
# Part 1: Reading an NFA from a .txt and outputting as a .json to draw
#######################################


# Draw using PySimpleAutomata from input.json file
def draw_json_NFA():
    json_example = automata_IO.nfa_json_importer('/Users/patrickdrummond/Desktop/COMP 5361 Disc Calc/PA3/input1.json')
    automata_IO.nfa_to_dot(json_example, 'output', '/Users/patrickdrummond/Desktop/COMP 5361 Disc Calc/PA3')
    print("NFA JSON Drawn to Output.dot")

def draw_json_DFA():
    json_example = automata_IO.dfa_json_importer('/Users/patrickdrummond/Desktop/COMP 5361 Disc Calc/PA3/input1.json')
    automata_IO.dfa_to_dot(json_example, 'output', '/Users/patrickdrummond/Desktop/COMP 5361 Disc Calc/PA3')
    print("DFA JSON Drawn to Output.dot")


def get_tt():

    # Open your transition table file
    f = open("tt.txt", 'r')

    # array to hold characters for later State object assignment
    # list of relevant characters
    directions = []

    # Skip the top line bc it's only there for readability
    next(f)
    next(f)

    for line in f:
        directions.append([line])

    # print(directions)

    return directions


def process_tt(directions):

    d1 = []
    size = len(directions)

    # put each line in it's own list
    for i in range(0, size):
        d1.append([])

    for i in range(0, size):
        dd = directions[i]
        dummy = ""
        for line in dd:
            for char in line:
                if char != "|":
                    if char != " ":
                        dummy += char
                if char == "|":
                    d1[i].append(dummy)
                    dummy = ""
    return d1


def get_states(ptt):

    states_list = []
    states_size = len(ptt)

    for i in range(0, states_size):
        name = ptt[i][0]
        name = name.replace("*", "").replace(">", "")
        states_list.append(name)

    return states_list


def get_initial_state(ptt):

    initial_state = ""
    states_size = len(ptt)

    for i in range(0, states_size):
        state = ptt[i][0]
        if ">" in state:
            initial_state += state.replace(">", "")

    return initial_state


def get_accepting_states(ptt):

    accepting = []
    states_size = len(ptt)

    for i in range(0, states_size):
        state = ptt[i][0]
        if "*" in state:
            accepting.append(state.replace("*", ""))

    # print("Accepting States")
    # print(accepting)
    return accepting


def get_transitions(ptt, format):

    states = get_states(ptt)
    size = len(ptt)
    transitions = []
    transitions_unformated = []
    transitions_lists = [[],[]]
    transitions_dicts = [{}, {}]


    # Iterate through table adding a and b transitions if not x
    # Start with a
    for i in range(0, size):
        input_state = states[i]
        output_state_a = str(ptt[i][1])
        # print("OUTPUT A " + output_state_a)
        transitions_unformated.append(output_state_a)
        transitions_lists[0].append(output_state_a)
        transitions_dicts[0][input_state] = output_state_a
        if output_state_a != 'x':
            if ',' not in output_state_a:
                transitions.append('["' + input_state + '","a",' + '"' + output_state_a + '"]')
            if ',' in output_state_a:
                # Iterate through transitions adding to list until theres none left
                cc = 1
                for char in output_state_a:
                    if char == ",":
                        cc += 1
                for i in range(0, cc):
                    output = output_state_a[:2] # Get the output state
                    transitions.append('["' + input_state + '","a",' + '"' + output + '"]')
                    output_state_a = output_state_a[3:] # Erase the already written output and the comma

    # Next find the outputs when given a B
    for i in range(0, size):
        input_state = states[i]
        output_state_a = str(ptt[i][2])
        # print("OUTPUT B " + output_state_a)
        transitions_unformated.append(output_state_a)
        transitions_lists[1].append(output_state_a)
        transitions_dicts[1][input_state] = output_state_a
        if output_state_a != 'x':
            if ',' not in output_state_a:
                transitions.append('["' + input_state + '","b",' + '"' + output_state_a + '"]')
            if ',' in output_state_a:
                # Iterate through transitions adding to list until theres none left
                cc = 1
                for char in output_state_a:
                    if char == ",":
                        cc += 1
                for i in range(0, cc):
                    output = output_state_a[:2] # Get the output state
                    transitions.append('["' + input_state + '","b",' + '"' + output + '"]')
                    output_state_a = output_state_a[3:] # Erase the already written output and the comma

    # print(transitions)
    if format == "NFA_PRINT":
        return(transitions)
    if format == "DFA_TABLE":
        return(transitions_unformated)
    if format == "DICTIONARY":
        return(transitions_dicts)


def format_for_json(list):

    size = len(list)
    process = []
    for i in range(0, size):
        template = '"' + list[i] + '",'
        if i < size - 1:
            process.append(template)
    process.append('"' + list[i] + '"')

    #print(process)
    return process


def write_to_json(states, initial_states, accepting_states, transitions):

    # Open .dot file
    # Open up the .json file for writing
    f = open("input1.json", "w")
    f.write("{\n")
    f.write('"alphabet" : ["a", "b"],')
    f.write("\n")

    # Write the states
    states = format_for_json(states)
    f.write('"states": [')
    for item in states:
        f.write(item)
        f.write(" ")
    f.write("],")

    # Write the initial state
    f.write("\n")
    f.write('"initial_states": ' + '["' + initial_states + '"],')
    f.write("\n")

    # Write the accepting states
    astates = format_for_json(accepting_states)
    f.write('"accepting_states": [')
    for item in astates:
        f.write(item)
        f.write(" ")
    f.write("],\n")

    # Write the transitions
    tcount = len(transitions)
    f.write('"transitions": [\n')
    for i in range(0, tcount):
        item = transitions[i]
        if i < tcount - 1:
            #print(item)
            f.write(item)
            f.write(",\n")
        else:
            f.write(item)
    f.write("]")
    f.write("}")


def draw_NFA():

    tt = get_tt()
    ptt = process_tt(tt)
    states = get_states(ptt)
    initial_state = get_initial_state(ptt)
    format_for_json(states)
    astates = get_accepting_states(ptt)
    transitions = get_transitions(ptt, "NFA_PRINT")
    write_to_json(states, initial_state, astates, transitions)
    draw_json_NFA()


def grid_format(item):

    if len(item) < 9:
        missing = 9 - len(item)
        for i in range(0, missing):
            item = " " + item
    else:
        i = 1
    return item

def get_trans(title, td, flag):
    temp_a = ""
    temp_b = ""
    if ',' in title:
        #print("TRANS" + title)
        cc = 1
        for char in title:
            if char == ",":
                cc += 1
        for i in range(0, cc):
            temp_trans = title[:2]  # Get the output state
            # TempTrans is now representing state qx
            # Check the transitions dictionary for qx
            ta = ""
            tb = ""
            if temp_trans in td[0]:
                if td[0][temp_trans] != "x":
                    ta = ta + td[0][temp_trans]

            if temp_trans in td[1]:
                if td[1][temp_trans] != "x":
                    tb = tb + td[1][temp_trans]

            if ta not in temp_a:
                temp_a = temp_a + ta + ","
            if tb not in temp_b:
                temp_b = temp_b + tb + ","

            # Remove state that was processed
            title = title[3:]
    temp_a = temp_a[:-1]
    temp_b = temp_b[:-1]
    # Add to your dictionary
    if flag == "a":
        return temp_a
    if flag == "b":
        return temp_b

def convert_to_DFA():

    tt = get_tt()
    ptt = process_tt(tt)
    states = get_states(ptt)
    #print("States: ")
    #print(states)

    transitions = get_transitions(ptt, "DFA_TABLE")
    #print("Transitions DFA Table: ")
    #print(transitions)

    td = get_transitions(ptt, "DICTIONARY")

    #print("States New: ")
    #print(states)
    #print(td)

    i = 0
    while i < len(transitions):
        trans = transitions[i]
        if trans not in states and trans != "x" and trans != "":
            states.append(trans)

            ta = get_trans(trans, td, "a")
            tb = get_trans(trans, td, "b")

            td[0][trans] = ta
            td[1][trans] = tb

            if ta not in transitions:
                transitions.append(ta)
                i = 0
            if tb not in transitions:
                transitions.append(tb)
                i = 0
        i += 1


    #print(td)
    #print(transitions)

    return td

# prints DFA table from NFA tt.txt file
def print_DFA_table():

    sa = get_accepting_states(process_tt(get_tt()))

    td = convert_to_DFA()
    da = td[0]
    db = td[1]
    dal = list(da.values())
    dbl = list(db.values())
    states = list(da.keys())


    for i in range(0, len(sa)):
        for j in range(0, len(states)):
            if sa[i] in states[j] and "*" not in states[j]:
                states[j] = "*" + states[j]

    # Print top of table
    # Print Header
    print("\nDFA:")
    print("|     δ    |      a   |    b     |")
    print("|--------------------------------|")
    print("|         x|         x|         x|")
    for i in range(0, len(states)):
        state = states[i]
        tranA = dal[i]
        tranB = dbl[i]
        if tranA == "":
            tranA = "x"
        if tranB == "":
            tranB = "x"

        print("| " + grid_format(state), end="")
        print("| " + grid_format(tranA), end="")
        print("| " + grid_format(tranB) + "|")

    print("|--------------------------------|")

def write_DFA():

    td = convert_to_DFA()
    da = td[0]
    db = td[1]

    # Add trash state to your output menus
    da["G"] = "G"
    db["G"] = "G"
    da["x"] = "x"
    db["x"] = "x"

    # print(td)

    dfa_state = []
    dfa_transitions = []
    dfa_intial = []
    dfa_accepting = []

    ss = get_initial_state(process_tt(get_tt()))
    dfa_intial.append(ss)
    dfa_state.append(ss)

    sa = get_accepting_states(process_tt(get_tt()))

    i = 0
    while i < len(dfa_state):
        # Go through items in the states.
        # Look in the output menu and write output to transitions list
        # if the output isn't in the states, add it and run again (i = 0)
        for item in dfa_state:
            state = item
            # print("STATE: " + state)
            output_a = da[state]
            output_b = db[state]
            if output_a == "":
                output_a = "x"
            if output_b == "":
                output_b = "x"
            dfa_transitions.append('["' + state + '","a",' + '"' + output_a + '"]')
            dfa_transitions.append('["' + state + '","b",' + '"' + output_b + '"]')
            if output_a not in dfa_state:
                dfa_state.append(output_a)
                i = 0
            if output_b not in dfa_state:
                dfa_state.append(output_b)
                i = 0
        i += 1

    dfa_transitions = list(dict.fromkeys(dfa_transitions)) # Delete Duplicates

    # Populate accepting states list
    for i in range(0, len(sa)):
        for j in range(0, len(dfa_state)):
            if sa[i] in dfa_state[j]:
                dfa_accepting.append(dfa_state[j])

    #dfa_state.append("G")
    # print("DFA States:")
    # print(dfa_state)
    # print("Initial State")
    # print(dfa_intial)
    # print("DFA Accepting: ")
    # print(dfa_accepting)
    # print("Gotta get this one...")
    # print("DFA Transitions: ")
    # print(dfa_transitions)

    # Open .dot file
    # Open up the .json file for writing
    f = open("input1.json", "w")
    f.write("{\n")
    f.write('"alphabet" : ["a", "b"],')
    f.write("\n")

    # Write the states
    states = format_for_json(dfa_state)
    f.write('"states": [')
    for item in states:
        f.write(item)
        f.write(" ")
    f.write("],")

    # Write the initial state
    f.write("\n")
    f.write('"initial_state": ' + '"' + dfa_intial[0] + '",')
    f.write("\n")

    # Write the accepting states
    f.write('"accepting_states": [')
    dfa_accepting = format_for_json(dfa_accepting)
    for item in dfa_accepting:
        f.write(item)
        f.write(" ")
    f.write("],\n")

    # Write the transitions
    tcount = len(dfa_transitions)
    f.write('"transitions": [\n')
    for i in range(0, tcount):
        item = dfa_transitions[i]
        if i < tcount - 1:
            #print(item)
            f.write(item)
            f.write(",\n")
        else:
            f.write(item)
    f.write("]")
    f.write("}")

    #draw_json_DFA()



#convert_to_DFA()
#draw_NFA()
#print_DFA_table()
#write_DFA()
#draw_json_DFA()

def operate():

    c = input("Input 1 to draw NFA to output.dot\nInput 2 to draw DFA TT and output.dot\n"
              "Input 9 to exit. > ")

    while c != "9":

        if c == "1":
            draw_NFA()
            c = input("Next > ")
        if c == "2":
            print_DFA_table()
            write_DFA()
            draw_json_DFA()
            c = input("Next > ")

    if c == "9":
        print("Exit.")

operate()

