#!/usr/bin/env python3

import argparse
import sys
sys.path.append("..")

from capstone import *
from qiling import *
from qiling.const import *
from unicorn import *
from qiling.os.const import *


MAIN = 0x0402770
HEDWINCGI_MAIN_ADDR = 0x0040bfc0
SESS_GET_UID = 0x004083f0


md = Cs(CS_ARCH_MIPS, CS_MODE_32 + CS_MODE_LITTLE_ENDIAN)

def dump_reg(ql, *args, **kwargs):
    ql.log.info("="*0x10 + " register dump " + "="*0x10)
    for idx, val in ql.arch.regs.save().items():
        if not isinstance(idx, int):
            if 's' in idx or 'ra' in idx:
                ql.log.info(f"{idx}: {hex(val)}")
                
    #breakpoint()

def hook_sess_get_uid(ql):
    ql.hook_code(print_asm)

def malloc_hook(ql):
    print("[x]: hook malloc start")
    params = ql.os.resolve_fcall_params({'size':INT})
    print("[x]: size",hex(params['size']))

def malloc_end(ql):
    print("[x]: hook malloc end")
    v0 = ql.arch.regs.v0
    print("[x]: v0",hex(v0))

def strcpy_end(ql):
    print("[x]: strcpy_end end")
    v0 = ql.arch.regs.v0
    print("[x]: v0",hex(v0))


def strcpy_hook(ql):
    print("[+]: hook strcpy")
    params = ql.os.resolve_fcall_params({'dest':INT ,'src':STRING})
    print("[+]:" , hex(params["dest"]))
    print("[+]:" , len(params["src"]))

    #print("dst: %s" % hex(ql.os.function_arg[0]))
    #print("src: %s" % ql.mem.string(ql.os.function_arg[1]))

    #Not sure why I have to return 2 to continue with the call
    #to the strcpy function. This was taken from example:
    #hello_mips32el_linux_function_hook.py
    return 2

# From https://github.com/qilingframework/qiling/blob/master/examples/hello_x8664_linux_disasm.py
def print_asm(ql, address, size):
    # in sobj_add_string
    if (address > 0x413c90 and address < 0x413D60):
        buf = ql.mem.read(address, size)
        for i in md.disasm(buf, address):
            print(":: 0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))


def read_a3(ql):
    print("[x]: read_a3")
    a3 = ql.arch.regs.a3
    print("[x]: a3",hex(a3))
    buf = ql.mem.read(a3, 1024)    
    print("[x]: a3",buf[:10])
    
def my_sandbox(path, rootfs):
    #buffer = "uid=%s" % (b"A" * 1043 + b"BBBB")
    buffer = "uid=%s" % ("A" * 2000)
    #buffer = "uid=%s" % (b"A" * 5)
    required_env = {
        "REQUEST_METHOD": "POST",
        "HTTP_COOKIE"   : buffer
    }

    ql = Qiling(path, rootfs, env=required_env)
    ql.add_fs_mapper('/tmp', '/var/tmp')                              # Maps hosts /tmp to /var/tmp
    ql.hook_address(lambda ql: print("[+]: At [main] **"), MAIN)
    ql.hook_address(lambda ql: print("[+]: At [hedwingcgi_main] **"), HEDWINCGI_MAIN_ADDR)
    ql.hook_address(lambda ql: print("[+]: At [sess_get_uid] **",hex(SESS_GET_UID) ), SESS_GET_UID)
    ql.hook_address(lambda ql: print("[+]: Ret from sobj_add_string **"), 0x004085c4)
    ql.os.set_api('strcpy', strcpy_hook, QL_INTERCEPT.ENTER)
    ql.os.set_api('strcpy', strcpy_end, QL_INTERCEPT.EXIT)
    ql.os.set_api('malloc', malloc_hook, QL_INTERCEPT.ENTER)
    ql.os.set_api('malloc', malloc_end, QL_INTERCEPT.EXIT)

    #hook_sess_get_uid(ql)
    #ql.hook_address(dump_reg, 0x0040c568)
    #end_of_hedwigcgi_main=0x0040c594
    # ql.hook_address(dump_reg,end_of_hedwigcgi_main )
    ql.hook_address(read_a3, 0x0040c1c0)
    #ql.hook_address(read_a3, 0x0040c1c4)
    #ql.debugger = True
    ql.run()

if __name__ == "__main__":
    my_sandbox(["DIR645A1_FW103RUB08_squashfs-root/htdocs/hedwig.cgi"], "DIR645A1_FW103RUB08_squashfs-root")