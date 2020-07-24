"""CPU functionality."""

import sys

# Instructions
PRN = 0b01000111    # Print
HLT = 0b00000001    # Halt
LDI = 0b10000010
ADD = 0b10100000
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.running = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def hlt(self):
        self.running = False
        self.pc += 1

    def ldi(self, reg_num, val):
        self.reg[reg_num] = val
        self.pc += 3

    def prn(self, reg_num):
        print(self.reg[reg_num])
        self.pc += 2

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:
        #
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        file_name = sys.argv[1]
        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split = line.split('#')[0]
                    command = split.strip()

                    if command == '':
                        continue

                instruction = int(command,2)
                self.ram[address] = instruction
                address += 1
        except:
            print(f'{sys.argv[0]}: {sys.argv[1]} file not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.load()
        while self.running:
            instruction_reg = self.ram[self.pc]
            reg_a = self.ram[self.pc+1]
            reg_b = self.ram[self.pc+2]

            if instruction_reg == HLT:
                self.hlt()

            elif instruction_reg == LDI:
                self.ldi(reg_a, reg_b)

            elif instruction_reg == PRN:
                self.prn(reg_a)

            elif instruction_reg == ADD:
                self.alu("ADD", reg_a, reg_b)
                self.pc += 3

            elif instruction_reg == MUL:
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3

            elif instruction_reg == PUSH:
                # Decrement pointer
                self.reg[7] -= 1
                value = self.reg[reg_a]

                # Put val on stack pointer address
                sp = self.reg[7]
                self.ram[sp] = value
                self.pc += 2


            elif instruction_reg == POP:
                # Get Stack Pointer
                sp = self.reg[7]

                value = self.ram[sp]
                # Put value at given counter
                self.reg[reg_a] = value
                # Increment Stack Pointer
                self.reg[7] += 1
                self.pc += 2


            elif instruction_reg == CALL:

                address = self.reg[reg_a]
                return_address = self.pc + 2
                self.reg[7] -= 1
                sp = self.reg[7]
                self.ram[sp] = return_address
                self.pc = address


            elif instruction_reg == RET:
                sp = self.reg[7]
                return_address = self.ram[sp]
                self.reg[7] += 1
                self.pc = return_address


            else:
                print(f'Instruction at counter {self.pc} unrecognized.')
                self.pc += 1

            self.trace()
