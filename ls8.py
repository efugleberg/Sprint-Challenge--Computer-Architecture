"""Main."""

import sys
from cpu import *

args = sys.argv

if len(args) < 2:
    sys.exit("You must pass the path of a file to load")

program_path = args[1]

cpu = CPU()

cpu.load(program_path)
cpu.run()