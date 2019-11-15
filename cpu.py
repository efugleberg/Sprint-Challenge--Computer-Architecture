"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 7
        self.instructions = {
            1: self.HLT,
            130: self.LDI,
            71: self.PRN,
            69: self.PUSH,
            70: self.POP,
            80: self.CALL,
            17: self.RET,
            160: self.ADD,
            162: self.MUL
        }

    def load(self, path):
        """Load a program into memory."""

        address = 0
        program = []

        # For now, we've just hardcoded a program:
        with open(path) as f:
            for line in f:
                instruction = line.split('#', 1)[0].strip()
                if len(instruction):
                    program.append(int(instruction, 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def HLT(self):
        sys.exit(1)
        self.running = False

    def LDI(self):
        reg_a = self.ram_read(self.pc + 1)
        num = self.ram_read(self.pc + 2)
        self.reg[reg_a] = num
        self.pc +=3

    def PRN(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def PUSH(self):
        reg_a = self.ram[self.pc + 1]
        value = self.reg[reg_a]
        self.reg[self.sp] -= 1 # decrement the pointer address
        self.ram[self.reg[self.sp]] = value
        self.pc += 2

    def POP(self):
        reg_a = self.ram[self.pc + 1]
        value = self.ram[self.reg[self.sp]]
        self.reg[reg_a] = value
        self.reg[self.sp] += 1
        self.pc += 2

    def CALL(self):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        reg_a = self.ram[self.pc + 1]
        self.reg[6] = self.pc + 2
        self.pc = self.reg[reg_a]

    def RET(self):
        # pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc = self.reg[6]
    
    def ADD(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('ADD', reg_a, reg_b)
        self.pc +=3
    
    def MUL(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3

    def run(self):
        """Run the CPU."""

        while True: 
            register = self.ram_read(self.pc)
            self.instructions[register]()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, value, mar):
        self.ram[mar] = value