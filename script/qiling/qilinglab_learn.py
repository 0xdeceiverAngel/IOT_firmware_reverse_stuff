from qiling import *
from qiling.const import *
from qiling.os.mapper import QlFsMappedObject

import os
import struct

class hookurandom(QlFsMappedObject):  

    def read(self, size: int) :  
        if size == 1:
            return b"\x66" 
        else:
            return b"\x41" * size

    def close(self) :
        return 0

def hookgetrandom(ql, buf, buflen, flags):
    if buflen == 32:
        data = b'\x41' * buflen  
        ql.mem.write(buf, data)
        ql.os.set_syscall_return(buflen)
    else:
        ql.os.set_syscall_return(-1)

def hook_uname(ql, write_buf, *args, **kw):
    rdi = ql.arch.regs.rdi
    print(f"utsname address: {hex(rdi)}") 
    ql.mem.write(rdi, b'QilingOS\x00')
    ql.mem.write(rdi + 65 * 3, b'ChallengeStart\x00') 

def hook_eax(ql):
    ql.arch.regs.eax = 1
    return

def hook_rand(ql):
    ql.arch.regs.rax = 0 

def hook_rax(ql):
    ql.arch.regs.rax = 0

def hook_sleep(ql):
    return 0

def challenge8_hook(ql):

    MAGIC = 0x3DFCD6EA00000539

    magic_addrs = ql.mem.search(ql.pack64(MAGIC)) 

    for magic_addr in magic_addrs: 

        # Dump and unpack the candidate structure
        candidate_heap_struct_addr = magic_addr - 8 
        candidate_heap_struct = ql.mem.read(candidate_heap_struct_addr, 24) 
        print(candidate_heap_struct)

        string_addr, _ , check_addr = struct.unpack('QQQ', candidate_heap_struct) 

        if ql.mem.string(string_addr) == "Random data":
            
            ql.mem.write(check_addr, b"\x01")
            break

def hook_tolower(ql):
    return 1

class Fake_cmdline(QlFsMappedObject):
    def read(self, expected_len):
        return b'qilinglab' 

    def close(self):
        return 0

def hook_cpuid(ql, address, size):

    if ql.mem.read(address, size) == b'\x0F\xA2': # CPUID 0F A2
        regs = ql.arch.regs
        regs.ebx = 0x696C6951
        regs.ecx = 0x614C676E
        regs.edx = 0x20202062
        regs.rip += 2 


if __name__ == '__main__':
    path = ["qilinglab-x86_64"]
    rootfs = "qiling/examples/rootfs/x8664_linux"
    ql = Qiling(path, rootfs)

    #level1
    ql.mem.map(0x1000, 0x1000, info='[challenge1]')
    #           start   size    info
    #           size must be n*sizeof(page), page size default in qiling is 4096 bytes
    ql.mem.write(0x1337, ql.pack16(1337))

    #level2
    ql.os.set_syscall("uname",hook_uname, QL_INTERCEPT.EXIT)

    #level3
    ql.add_fs_mapper(r'/dev/urandom', hookurandom())
    ql.os.set_syscall("getrandom", hookgetrandom)

    #level4

    base = ql.mem.get_lib_base(os.path.split(ql.path)[-1]) 
    ql.hook_address(hook_eax, base + 0xE43)

    #level5
    ql.os.set_api('rand', hook_rand)

    #level6

    base = ql.mem.get_lib_base(os.path.split(ql.path)[-1])
    hook_addr = base + 0xF16
    ql.hook_address(hook_rax, hook_addr)

    #level7


    ql.os.set_api('sleep', hook_sleep)

    #level8
    base_addr = ql.mem.get_lib_base(os.path.split(ql.path)[-1])
    addr = base_addr + 0xFB5    

    ql.hook_address(challenge8_hook, addr)

    #level9
    ql.os.set_api('tolower', hook_tolower)

    #level10
    ql.add_fs_mapper('/proc/self/cmdline', Fake_cmdline())


    #level11


    ql.hook_code(hook_cpuid)


    ql.run()
    