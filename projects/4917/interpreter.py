import sys


def ascii(state, highlight):
    center = []
    for (i, s) in enumerate(state):
        if i-4 in highlight:
            s = "_"+str(s)+"_"
        center.append(str(s).center(4))

    print("""
    ┌────────┐ ┌────────┐
    │IP: {0}│ │IS: {1}│
    └────────┘ └────────┘
    ┌────────┐ ┌────────┐
    │R0: {2}│ │R1: {3}│
    └────────┘ └────────┘

    ┌────┬────┬────┬────┐
  0 │{4}│{5}│{6}│{7}│ 3
    ├────┼────┼────┼────┤
  4 │{8}│{9}│{10}│{11}│ 7
    ├────┼────┼────┼────┤
  8 │{12}│{13}│{14}│{15}│ 11
    ├────┼────┼────┼────┤
 12 │{16}│{17}│{18}│{19}│ 15
    └────┴────┴────┴────┘  

""".format(*center))


def cpu(IP, IS, R0, R1, memory):
    """
                          │ IP: instruction pointer
    ┌──────┐ ┌──────┐     │ IS: instruction store, current instruction
    │IP: 0 │ │IS: 0 │     │ R0: register 0
    └──────┘ └──────┘     │ R1: register 1
    ┌──────┐ ┌──────┐     ├───────────────────────────────────────────
    │R0: 0 │ │R1: 0 │     │    0 halt
    └──────┘ └──────┘     │    1 add R0 = R0 + R1
      0   1   2   3       │    2 subtract R0 = R0 - R1
    ┌───┬───┬───┬───┐     │    3 increment R0 R0 = R0 + 1
    │ 0 │ 0 │ 0 │ 0 │     │    4 increment R1 R1 = R1 + 1
    ├───┼───┼───┼───┤     │    5 decrement R0 R0 = R0 - 1
    │ 0 │ 0 │ 0 │ 0 │     │    6 decrement R1 R1 = R1 - 1
    ├───┼───┼───┼───┤     │    7 ring bell
    │ 0 │ 0 │ 0 │ 0 │     │  8 X print data X
    ├───┼───┼───┼───┤     │  9 X load value of address X into R0
    │ 0 │ 0 │ 0 │ 0 │     │ 10 X load value of address X into R1
    └───┴───┴───┴───┘     │ 11 X store R0 into address X
     12  13  14  15       │ 12 X store R1 into address X
                          │ 13 X jump to address X
                          │ 14 X jump to address X if R0 == 0
                          │ 15 X jump to address X if R0 != 0
    """

    while True:
        IS = memory[IP]
        highlight = [IP]
        if (IS >= 8):
            highlight = [IP, IP+1]

        ascii([IP, IS, R0, R1, *memory], highlight)

        if IS == 0:
            break
        elif IS == 1:
            R0 = R0 + R1
            IP += 1
        elif IS == 2:
            R0 = R0 - R1
            IP += 1
        elif IS == 3:
            R0 += 1
            IP += 1
        elif IS == 4:
            R1 += 1
            IP += 1
        elif IS == 5:
            R0 -= 1
            IP += 1
        elif IS == 6:
            R1 -= 1
            IP += 1
        elif IS == 7:
            print("*** BEEP ***")
            IP += 1
        elif IS == 8:
            print("*** ", memory[IP+1], "***")
            IP += 2
        elif IS == 9:
            R0 = memory[memory[IP+1]]
            IP += 2
        elif IS == 10:
            R1 = memory[memory[IP+1]]
            IP += 2
        elif IS == 11:
            memory[memory[IP+1]] = R0
            IP += 2
        elif IS == 12:
            memory[memory[IP+1]] = R1
            IP += 2
        elif IS == 13:
            IP = memory[IP + 1]
        elif IS == 14:
            if R0 == 0:
                IP = memory[IP + 1]
            else:
                IP += 2
        elif IS == 15:
            if R0 != 0:
                IP = memory[IP + 1]
            else:
                IP += 2

        input()


if len(sys.argv) == 1 or ".prg" not in sys.argv[1]:
    print("usage: python3 ", sys.argv[0] + " file.prg")
    sys.exit(1)

f = open(sys.argv[1])
state = []
for line in f.readlines():
    if '#' in line:
        continue
    line = line.replace("│", " ")
    line = line.replace("_", " ")
    row = []
    for s in line.split():
        if s.isdigit():
            row.append(int(s))
    # remove first and last element in case its pasted from our output
    if len(row) == 6:
        row.pop(5)
        row.pop(0)
    if len(row) > 0:
        state += row
f.close()

instruction_pointer, instruction_store, r0, r1, *memory = state
cpu(instruction_pointer, instruction_store, r0, r1, memory)
