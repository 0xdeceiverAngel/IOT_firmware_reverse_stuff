from unicorn import *
from unicorn.x86_const import *

shellcode = b"\xe8\xff\xff\xff\xff\xc0\x5d\x6a\x05\x5b\x29\xdd\x83\xc5\x4e\x89\xe9\x6a\x02\x03\x0c\x24\x5b\x31\xd2\x66\xba\x12\x00\x8b\x39\xc1\xe7\x10\xc1\xef\x10\x81\xe9\xfe\xff\xff\xff\x8b\x45\x00\xc1\xe0\x10\xc1\xe8\x10\x89\xc3\x09\xfb\x21\xf8\xf7\xd0\x21\xd8\x66\x89\x45\x00\x83\xc5\x02\x4a\x85\xd2\x0f\x85\xcf\xff\xff\xff\xec\x37\x75\x5d\x7a\x05\x28\xed\x24\xed\x24\xed\x0b\x88\x7f\xeb\x50\x98\x38\xf9\x5c\x96\x2b\x96\x70\xfe\xc6\xff\xc6\xff\x9f\x32\x1f\x58\x1e\x00\xd3\x80"

base_adr = 0x400000
stack_adr = 0x0
stack_size = 1024 * 1024

dict_system_call = {
    1: "sys_exit",
    15: "sys_chmod", 
}

def hook_code(mu, address, size, user_data):  
    # print('>>> Tracing instruction at 0x%x, instruction size = 0x%x' %(address, size))
    op_code = mu.mem_read(address, size)
    if op_code != b"\x00\x00":
        print((op_code).hex())
    if op_code == b"\xcd\x80":
        call_number = mu.reg_read(UC_X86_REG_EAX)
        param_1 = mu.reg_read(UC_X86_REG_EBX)
        param_2 = mu.reg_read(UC_X86_REG_ECX)
        param_3 = mu.reg_read(UC_X86_REG_EDX)
        param_4 = mu.reg_read(UC_X86_REG_ESI)
        param_5 = mu.reg_read(UC_X86_REG_EDI)
        system_call_name = dict_system_call[call_number]

        print("[*] System call")
        print(f"Call Number: {call_number}({system_call_name})")

        if system_call_name == "sys_chmod":
            file = mu.mem_read(param_1, 64).split(b"\x00")[0]
            print(f"Param 1    : {param_1}({hex(param_1)}) -> {file}")
            print(f"Param 2    : {param_2}({hex(param_2)}) -> {oct(param_2)}")
        else:
            print(f"Param 1    : {param_1}({hex(param_1)})")
        print("")
        mu.reg_write(UC_X86_REG_EIP, address + size)

try:
    mu = Uc(UC_ARCH_X86, UC_MODE_32)
    mu.mem_map(base_adr, 1024 * 1024)
    mu.mem_map(stack_adr, stack_size)

    mu.mem_write(base_adr, shellcode)
    mu.reg_write(UC_X86_REG_ESP, stack_adr + stack_size)
    mu.hook_add(UC_HOOK_CODE, hook_code)

    mu.emu_start(base_adr, base_adr + len(shellcode))
except UcError as e:
    print("ERROR: %s" % e)