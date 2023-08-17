Ref
- https://skylinelimit.blogspot.com/2018/02/c-4.html
- https://p1kk.github.io/2021/04/14/iot/vivotek%20%E6%91%84%E5%83%8F%E5%A4%B4%E6%A0%88%E6%BA%A2%E5%87%BA%E6%BC%8F%E6%B4%9E%E5%A4%8D%E7%8E%B0/
- https://xz.aliyun.com/t/10214#toc-2

```bash
user@vm-ubuntu20:~/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root$ checksec ./usr/sbin/httpd
[*] Checking for new versions of pwntools
    To disable this functionality, set the contents of /home/user/.cache/.pwntools-cache-3.10/update to 'never' (old way).
    Or add the following lines to ~/.pwn.conf or ~/.config/pwn.conf (or /etc/pwn.conf system-wide):
        [update]
        interval=never
[*] You have the latest version of Pwntools (4.10.0)
[*] '/home/user/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root/usr/sbin/httpd'
    Arch:     arm-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8000)
```

# qemu-arm-static
```bash
user@vm-ubuntu20:~/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted$ find .|grep httpd
./_DC7909.extracted/setup/vadppkg/_genetec-vadp-1-0-2-7.tar.gz.extracted/_0.extracted/script/modify_init_httpd
./_31.extracted/_rootfs.img.extracted/squashfs-root/etc/init.d/httpd
./_31.extracted/_rootfs.img.extracted/squashfs-root/usr/sbin/httpd
./_31.extracted/defconf/_CC8160.tar.bz2.extracted/_0.extracted/etc/rcS.d/S31httpd
user@vm-ubuntu20:~/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted$ file ./_31.extracted/_rootfs.img.extracted/squashfs-root/usr/sbin/httpd
./_31.extracted/_rootfs.img.extracted/squashfs-root/usr/sbin/httpd: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-uClibc.so.0, stripped




user@vm-ubuntu20:~/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root$ sudo chroot . ./qemu-arm-static ./usr/sbin/httpd
sendto() error 20
[debug]add server push uri 3 video3.mjpg
[debug]add server push uri 4 video4.mjpg
[debug] after ini, server_push_uri[0] is /video3.mjpg
[debug] after ini, server_push_uri[1] is /video4.mjpg
AM_ParseConfigFile failed
fopen pid file: Not a directory
[15/Aug/2023:14:39:32 +0000] boa: server version 1.32.1.10(Boa/0.94.14rc21)
[15/Aug/2023:14:39:32 +0000] boa: starting server pid=150530, port 80


user@vm-ubuntu20:~/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root$ sudo ss -ltpn
State         Recv-Q        Send-Q               Local Address:Port                Peer Address:Port       Process                                             
LISTEN        0             128                        0.0.0.0:22                       0.0.0.0:*           users:(("sshd",pid=1097,fd=3))                     
LISTEN        0             128                      127.0.0.1:631                      0.0.0.0:*           users:(("cupsd",pid=141672,fd=7))                  
LISTEN        0             4096                 127.0.0.53%lo:53                       0.0.0.0:*           users:(("systemd-resolve",pid=777,fd=14))          
LISTEN        0             511                      127.0.0.1:42525                    0.0.0.0:*           users:(("node",pid=139173,fd=18))                  
LISTEN        0             244                      127.0.0.1:5432                     0.0.0.0:*           users:(("postgres",pid=1140,fd=5))                 
LISTEN        0             4096                     127.0.0.1:46141                    0.0.0.0:*           users:(("containerd",pid=1076,fd=13))              
LISTEN        0             128                           [::]:22                          [::]:*           users:(("sshd",pid=1097,fd=4))                     
LISTEN        0             250                              *:80                             *:*           users:(("qemu-arm-static",pid=150530,fd=3))        
LISTEN        0             250                              *:8080                           *:*           users:(("qemu-arm-static",pid=150530,fd=4))        
LISTEN        0             128                          [::1]:631                         [::]:*           users:(("cupsd",pid=141672,fd=6))    
```

Because `httpd` will run in background, can't use `sudo chroot . ./qemu-arm-static -g 1234 ./usr/sbin/httpd`

```bash
user@vm-ubuntu20:~/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root$ gdb-multiarch -q ./usr/sbin/httpd
pwndbg: loaded 147 pwndbg commands and 46 shell commands. Type pwndbg [--shell | --all] [filter] for a list.
pwndbg: created $rebase, $ida GDB functions (can be used with print/break)
Reading symbols from ./usr/sbin/httpd...
(No debugging symbols found in ./usr/sbin/httpd)
------- tip of the day (disable with set show-tips off) -------
break-if-taken and break-if-not-taken commands sets breakpoints after a given jump instruction was taken or not
pwndbg> set  architecture arm
The target architecture is set to "arm".
pwndbg> target remote 127.0.0.1:1234
Remote debugging using 127.0.0.1:1234
warning: remote target does not support file transfer, attempting to access files from local filesystem.
Reading symbols from /home/user/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root/lib/ld-uClibc-0.9.33.3-git.so...
(No debugging symbols found in /home/user/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root/lib/ld-uClibc-0.9.33.3-git.so)
0x3fff1e6c in _start () from /home/user/vivotekcc8160/_CC8160-VVTK-0100d.flash.pkg.extracted/_31.extracted/_rootfs.img.extracted/squashfs-root/lib/ld-uClibc-0.9.33.3-git.so
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────
 R0   0x0
 R1   0x408007ee ◂— './usr/sbin/httpd'
 R2   0x0
 R3   0x0
 R4   0x0
 R5   0x0
 R6   0x0
 R7   0x0
 R8   0x0
 R9   0x0
 R10  0x315dc —▸ 0xa894 ◂— push {r3, lr}
 R11  0x0
 R12  0x0
 SP   0x408006c0 ◂— 0x1
 PC   0x3fff1e6c (_start) ◂— mov r0, sp /* '\r' */
──────────────────────────────────────────────────────[ DISASM / arm / set emulate on ]───────────────────────────────────────────────────────
 ► 0x3fff1e6c <_start>       mov    r0, sp
   0x3fff1e70 <_start+4>     bl     #0x3fff64bc                   <0x3fff64bc>
 
   0x3fff1e74 <_start+8>     mov    r6, r0
   0x3fff1e78 <_start+12>    ldr    sl, [pc, #0x30]
   0x3fff1e7c <_start+16>    add    sl, pc, sl
   0x3fff1e80 <_start+20>    ldr    r4, [pc, #0x2c]
   0x3fff1e84 <_start+24>    ldr    r4, [sl, r4]
   0x3fff1e88 <_start+28>    ldr    r1, [sp]
   0x3fff1e8c <_start+32>    sub    r1, r1, r4
   0x3fff1e90 <_start+36>    add    sp, sp, r4, lsl #2
   0x3fff1e94 <_start+40>    add    r2, sp, #4
──────────────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────────────
00:0000│ sp 0x408006c0 ◂— 0x1
01:0004│    0x408006c4 —▸ 0x408007ee ◂— './usr/sbin/httpd'
02:0008│    0x408006c8 ◂— 0x0
03:000c│    0x408006cc —▸ 0x408007ff ◂— 'SUDO_GID=1000'
04:0010│    0x408006d0 —▸ 0x4080080d ◂— 'SUDO_UID=1000'
05:0014│    0x408006d4 —▸ 0x4080081b ◂— 'SUDO_USER=user'
06:0018│    0x408006d8 —▸ 0x4080082a ◂— 'SUDO_COMMAND=/usr/sbin/chroot . ./qemu-arm-static -g 1234 ./usr/sbin/httpd'
07:001c│    0x408006dc —▸ 0x40800875 ◂— 'SHELL=/bin/bash'
────────────────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────────────────
 ► 0 0x3fff1e6c _start
   1      0x0
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> c
Continuing.
[Inferior 1 (process 1) exited normally]
```

# Reverse httpd

```c
char *sub_10AC8()
{
  __uid_t v0; // r0
  const char *v1; // r3
  FILE *v2; // r5
  int v3; // r0
  char *result; // r0
  const char *v5; // r2
  rlim_t rlim_cur; // r3
  int v7; // r3
  struct hostent *v8; // r0
  struct rlimit rlimits; // [sp+4h] [bp-74h] BYREF

  v0 = getuid();
  v1 = (const char *)dword_37E88;
  if ( !dword_37E88 )
  {
    v1 = "/etc/conf.d/boa/boa.conf";
    dword_37E88 = (int)"/etc/conf.d/boa/boa.conf";  // need find /etc/conf.d put back to correct path
  }
  dword_34874 = v0;
  v2 = fopen(v1, "r");
  if ( !v2 )
  {
    fwrite("Could not open boa.conf for reading.\n", 1u, 0x25u, (FILE *)stderr);
    exit(1);
  }
  sub_10834();
  v3 = fclose(v2);
  sub_21D7C(v3);
  if ( !dword_37E94 )
  {
    if ( gethostname((char *)&rlimits, 0x64u) == -1 ) //need set your hostname in firmware's /etc/hosts
    {
      perror("gethostname:");
      exit(1);
    }
    v8 = gethostbyname((const char *)&rlimits);
    if ( !v8 )
    {
      perror("gethostbyname:");
      exit(1);
```



```c
int __fastcall sub_17F80(int a1)
{
  char *v2; // r0
  int v3; // r3
  const char *v4; // r5
  char *v5; // r9
  const char *v6; // r8
  const char *v7; // r3
  int v8; // r6
  int v9; // t1
  _BOOL4 v10; // r10
  int v12; // r2
  const char *v13; // r0
  bool v14; // zf
  int v15; // r2
  int v16; // t1
  bool v17; // zf
  int v18; // r0
  int v19; // r2
  int v20; // r1
  ssize_t v21; // r5
  int v22; // r2
  char *v23; // r0
  const char *v24; // r6
  char *v25; // r0
  int result; // r0
  int v27; // r6
  FILE *v28; // r0
  int v29; // r6
  FILE *v30; // r0
  int v31; // r2
  int v32; // r3
  char *kk_ptr; // r7
  char *kk_ptr_newline; // r6
  char *kk_ptr_colon; // r0
  int v36; // r7
  int v37; // r0
  int v38; // r2
  unsigned int v39; // r3
  char *haystack; // [sp+Ch] [bp-44h]
  const char *v41; // [sp+14h] [bp-3Ch]
  char dest[4]; // [sp+18h] [bp-38h] BYREF
  int v43; // [sp+1Ch] [bp-34h]
  int v44; // [sp+20h] [bp-30h]
  int v45; // [sp+24h] [bp-2Ch]

  haystack = (char *)(a1 + 13690);
  v2 = strncpy((char *)(a1 + 21882), (const char *)(a1 + 13690), 0x1FFFu);
  v3 = *(_DWORD *)(a1 + 6516);
  v4 = (const char *)(a1 + *(_DWORD *)(a1 + 72) + 13632 + 58);
  v5 = &haystack[v3];
  if ( (dword_34864 & 0x10) != 0 && v4 < v5 )
  {
    haystack[v3] = 0;
    sub_16534(v2);
    fprintf((FILE *)stderr, "%s:%d - Parsing headers (\"%s\")\n", "src/read.c", 57, v4);
  }
  v6 = v4 - 1;
  v7 = v4;
  if ( v4 >= v5 )
  {
LABEL_24:
    if ( *(_DWORD *)a1 > 3u )
      return 1;
    v20 = *(_DWORD *)(a1 + 6516);
    if ( (unsigned int)(0x1FFF - v20) >= 0x2000 )
    {
      sub_1627C(a1);
      fwrite("No space left in client stream buffer, closing\n", 1u, 0x2Fu, (FILE *)stderr);
      result = 0;
      *(_DWORD *)(a1 + 16) = 400;
      *(_DWORD *)a1 = 12;
      return result;
    }
    v21 = read(*(_DWORD *)(a1 + 4448), &haystack[v20], 0x2000 - v20);
    if ( !strncmp(haystack, "POST", 4u) || (v25 = (char *)strncmp(haystack, "PUT", 3u)) == 0 )
    {
      v22 = *(unsigned __int8 *)(a1 + 13690);
      *(_DWORD *)dest = 0;
      v43 = 0;
      v44 = 0;
      v45 = 0;
      if ( v22 )
      {
        kk_ptr = strstr(haystack, "Content-Length");
        kk_ptr_newline = strchr(kk_ptr, '\n');
        kk_ptr_colon = strchr(kk_ptr, ':');
        strncpy(dest, kk_ptr_colon + 1, kk_ptr_newline - (kk_ptr_colon + 1)); // cause overflow
      }
```



# Exploit

ROP chain
- padding
- pop {r1, pc}
- cmd_addr // r1
- mov r0, r1 ; pop {r4, r5, pc}  //r0 =r1 
- aaaa
- bbbb
- sys_addr
- cmd  // cmd string

DOS
- `"Content-Length": f"{payload}"`
- `payload = "A"*100`
# Run on arm 

```bash
[23-08-16  8:50AM :22] ┌──(user㉿kali)-[~/Downloads/squashfs-root]
└─$ sudo chroot . /bin/sh 
chroot: failed to run command ‘/bin/sh’: Exec format error

[23-08-16  8:59AM :08] ┌──(user㉿kali)-[~/Downloads/squashfs-root]
└─$ uname -a
Linux kali 6.0.0-kali3-arm64 #1 SMP Debian 6.0.7-1kali1 (2022-11-07) aarch64 GNU/Linux

```