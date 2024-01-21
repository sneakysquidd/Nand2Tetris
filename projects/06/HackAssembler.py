file_path = 'rect/Rect.asm'
symbol_table = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
                'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576}

with open(file_path, 'r') as file:
    instruction = 0
    instructions = []
    for line in file:
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        if len(line) == 0:
            continue
        if line[0] == '/':
            continue



        if line[0] == '(':
            symbol_table[line[1:-1]] = instruction
            continue
        instructions.append(line.split("//")[0])
        instruction += 1


with open("rect.hack", 'w') as file:
    next_avail = 16
    for i in range(len(instructions)):
        curr_instruction = instructions[i]

        if curr_instruction[0] == '@':  # IF 'A' INSTRUCTION
            symbol = curr_instruction[1:]
            if not symbol.isnumeric():
                if symbol not in symbol_table:
                    symbol_table[symbol] = next_avail
                    next_avail += 1
                symbol = symbol_table[symbol]
            file.write(bin(int(symbol))[2:].zfill(16)+'\n')
        else: # IF 'C' INSTRUCTION
            binary = "111"
            if "=" in curr_instruction:
                dest, process = curr_instruction.split("=")
            else:
                dest = ""
                process = curr_instruction

            if ";" in process:
                comp, jump = process.split(";")
            else:
                jump = ""
                comp = process
            a = "0"
            if 'M' in comp:
                a = "1"
            c_dict = {"0": "101010", "1": "111111", "-1": "111010", "D": "001100", "A": "110000", "M": "110000", "!D": "001101", "!A": "110001", "!M": "110001", "-D": "001111", "-A": "110011", "-M": "110011", "D+1": "011111", "A+1": "110111", "M+1": "110111", "D-1": "001110", "A-1": "110010", "M-1": "110010", "D+A": "000010", "D+M": "000010", "D-A": "010011", "D-M": "010011", "A-D": "000111", "M-D": "000111", "D&A": "000000", "D&M": "000000", "D|A": "010101", "D|M": "010101"}
            c = c_dict[comp]

            d0 = ("A" in dest) * 1
            d1 = ("D" in dest) * 1
            d2 = ("M" in dest) * 1
            d = f'{d0}{d1}{d2}'

            j_dict = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
            j = j_dict[jump]

            file.write("111"+a+c+d+j+'\n')



