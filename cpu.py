"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.flag = [0] * 8
        self.sp = 7
        self.instructions = {
            1: self.hlt,
            130: self.ldi,
            71: self.prn,
            69: self.push,
            70: self.pop,
            80: self.call,
            17: self.ret,
            160: self.add,
            162: self.mul,
            167: self.cmp,
            84: self.jmp,
            85: self.jeq,
            86: self.jne
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

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, value, mar):
        self.ram[mar] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        val_one = self.reg[reg_a]
        val_two = self.reg[reg_b]

        if op == "add":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "mul":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "cmp":
            if val_one == val_two:
                self.flag[7] = 1
            if val_one > val_two:
                self.flag[6] = 1
            if val_one < val_two:
                self.flag[5] = 1

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.flag,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def hlt(self):
        sys.exit(1)
        self.running = False

    def ldi(self):
        reg_a = self.ram_read(self.pc + 1)
        num = self.ram_read(self.pc + 2)
        self.reg[reg_a] = num
        self.pc += 3

    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def push(self):
        reg_a = self.ram[self.pc + 1]
        value = self.reg[reg_a]
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = value
        self.pc += 2

    def pop(self):
        reg_a = self.ram[self.pc + 1]
        value = self.ram[self.reg[self.sp]]
        self.reg[reg_a] = value
        self.reg[self.sp] += 1
        self.pc += 2

    def call(self):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        reg_a = self.ram[self.pc + 1]
        self.reg[6] = self.pc + 2
        self.pc = self.reg[reg_a]

    def ret(self):
        self.reg[self.sp] += 1
        self.pc = self.reg[6]

    def add(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('add', reg_a, reg_b)
        self.pc += 3

    def mul(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('mul', reg_a, reg_b)
        self.pc += 3

    def cmp(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('cmp', reg_a, reg_b)
        self.pc += 3

    def jmp(self):
        reg_a = self.ram[self.pc + 1]
        self.pc = self.reg[reg_a]

    def jeq(self):
        if self.flag[7] == 1:
            reg_a = self.ram[self.pc + 1]
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2

    def jne(self):
        if self.flag[7] == 0:
            reg_a = self.ram[self.pc + 1]
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""

        while True:
            register = self.ram_read(self.pc)
            self.instructions[register]()
