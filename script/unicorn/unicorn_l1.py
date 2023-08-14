import os
import math
import struct

from unicorn import *
from unicorn.x86_const import *

filename = "./fibonacci"
file_size = int(math.ceil(os.path.getsize(filename) / 1024) + 1) * 1024

base_adr = 0x400000
stack_adr = 0x0
stack_size = 1024 * 1024

main_start_adr = 0x004004e0
main_end_adr = 0x00400582

instructions_skip_list = [0x004004EF, 0x004004f6, 0x00400502, 0x0040054F]
instructions_IO_putc_list = [0x00400560, 0x00400575]
fibonacci_start = [0x00400670]
fibonacci_end = [0x004006f1, 0x00400709]

ret_instr = 0x004005e9

stack_buf = []
dict_fibonacci_result = {}

def read(name):
    with open(name, "rb") as f:
        return f.read()
        
def u32(data):
    return struct.unpack("I", data)[0]
    
def p32(num):
    return struct.pack("I", num)

def hook_code(mu, address, size, user_data):  
    # print('>>> Tracing instruction at 0x%x, instruction size = 0x%x' %(address, size))

    if address in instructions_skip_list:
        mu.reg_write(UC_X86_REG_RIP, address + size)

    elif address in instructions_IO_putc_list:
        print(chr(mu.reg_read(UC_X86_REG_RDI)), end="")
        mu.reg_write(UC_X86_REG_RIP, address + size)

    elif address in fibonacci_start:
        number, ptrNumber = mu.reg_read(UC_X86_REG_RDI), mu.reg_read(UC_X86_REG_RSI)
        ptrNumber_value = u32(mu.mem_read(ptrNumber, 4))

        args = (number, ptrNumber_value)
        if args in dict_fibonacci_result:
            ret_val, ret_ptrNumber_value = dict_fibonacci_result[args]
            mu.reg_write(UC_X86_REG_RAX, ret_val)
            mu.mem_write(ptrNumber, p32(ret_ptrNumber_value))
            mu.reg_write(UC_X86_REG_RIP, ret_instr)
        else:
            stack_buf.append((number, ptrNumber, ptrNumber_value))

    elif address in fibonacci_end:
        number, ptrNumber, ptrNumber_value = stack_buf.pop()

        ret_val = mu.reg_read(UC_X86_REG_RAX)
        ret_ptrNumber_value = u32(mu.mem_read(ptrNumber, 4))

        args = (number, ptrNumber_value)
        dict_fibonacci_result[args] = (ret_val, ret_ptrNumber_value)

try:
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(base_adr, file_size)
    mu.mem_map(stack_adr, stack_size)

    mu.mem_write(base_adr, read(filename))
    mu.reg_write(UC_X86_REG_RSP, stack_adr + stack_size - 1)
    mu.hook_add(UC_HOOK_CODE, hook_code)

    mu.emu_start(main_start_adr, main_end_adr)
except UcError as e:
    print("ERROR: %s" % e)