Ref:
- https://github.com/zodf0055980/QilingLab_Writeup/blob/main/solve.py
- https://paper.seebug.org/2073/

Install

```

python3 -m venv qilingenv 
source qilingenv/bin/activate 
git clone --recurse-submodules https://github.com/qilingframework/qiling.git 
pip3 install .

user@vm-ubuntu18:~$ pip show qiling
Name: qiling
Version: 1.4.4
Summary: Qiling is an advanced binary emulation framework that cross-platform-architecture
Home-page: http://qiling.io
Author: 
Author-email: 
License: GPLv2
Location: /home/user/.local/lib/python3.6/site-packages
Requires: capstone, gevent, keystone-engine, multiprocess, pefile, pyelftools, python-registry, pyyaml, unicorn
Required-by: 
```

Lab binary from https://www.shielder.com/blog/2021/07/qilinglab-release/

# Level1

```c
void challenge1(undefined *param_1)

{
  if (_DAT_00001337 == 0x539) {
    *param_1 = 1;
  }
  return;
}

```






# Level2


```c

void challenge2(undefined *param_1)

{
  int iVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  uint local_1d8;
  uint local_1d4;
  int local_1d0;
  int local_1cc;
  utsname local_1c8;
  undefined8 local_42;
  undefined2 local_3a;
  undefined8 local_38;
  undefined8 local_30;
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  iVar1 = uname(&local_1c8);
  if (iVar1 == 0) {
    local_42 = 0x534f676e696c6951;
    local_3a = 0;
    local_38 = 0x676e656c6c616843;
    local_30 = 0x747261745365;
    local_1d8 = 0;
    local_1d4 = 0;
    for (; sVar2 = strlen((char *)&local_42), (ulong)(long)local_1d0 < sVar2;
        local_1d0 = local_1d0 + 1) {
      if (local_1c8.sysname[local_1d0] == *(char *)((long)&local_42 + (long)local_1d0)) {
        local_1d8 = local_1d8 + 1;
      }
    }
    for (; sVar2 = strlen((char *)&local_38), (ulong)(long)local_1cc < sVar2;
        local_1cc = local_1cc + 1) {
      if (local_1c8.version[local_1cc] == *(char *)((long)&local_38 + (long)local_1cc)) {
        local_1d4 = local_1d4 + 1;
      }
    }
    sVar2 = strlen((char *)&local_42);
    if (((local_1d8 == sVar2) && (sVar2 = strlen((char *)&local_38), local_1d4 == sVar2)) &&
       (5 < local_1d8)) {
      *param_1 = 1;
    }
  }
  else {
    perror("uname");
  }
  if (local_20 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


        00100bdf 48 89 c7        MOV        RDI,RAX
        00100be2 e8 a9 fd        CALL       <EXTERNAL>::uname                                int uname(utsname * __name)
                 ff ff
        00100be7 85 c0           TEST       EAX,EAX
        00100be9 74 11           JZ         LAB_00100bfc
        00100beb 48 8d 3d        LEA        RDI,[s_uname_00101678]                           = "uname"
                 86 0a 00 00



char [] size is 65
           struct utsname {
               char sysname[];    /* Operating system name (e.g., "Linux") */
               char nodename[];   /* Name within communications network
                                     to which the node is attached, if any */
               char release[];    /* Operating system release
                                     (e.g., "2.6.28") */
               char version[];    /* Operating system version */
               char machine[];    /* Hardware type identifier */
           #ifdef _GNU_SOURCE
               char domainname[]; /* NIS or YP domain name */
           #endif
           };
```


# Level3

```c
void challenge3(undefined *param_1)
{
	int __fd;
	long in_FS_OFFSET;
	int local_68;
	int i;
	char readx1;
	char readx20 [32];
	char getrandx20 [40];
	long local_10;
	local_10 = *(long *)(in_FS_OFFSET + 0x28);
	__fd = open("/dev/urandom",0);
	read(__fd,readx20,0x20);
	read(__fd,&readx1,1);
	close(__fd);
	getrandom(getrandx20,0x20,1);
	local_68 = 0;
	for (i = 0; i < 0x20; i = i + 1) 
	{
		if ((readx20[i] == getrandx20[i]) && (readx20[i] != readx1)) 
			{
				local_68 = local_68 + 1;
			}
	}
	if (local_68 == 0x20) {
	*param_1 = 1;
	}
	if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
	/* WARNING: Subroutine does not return */
	__stack_chk_fail();
	}
	return;
}

```

# Level4

```c

void challenge4(undefined *param_1)

{
  int local_c;
  
  for (local_c = 0; local_c < 0; local_c = local_c + 1) {
    *param_1 = 1;
  }
  return;
}


                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined challenge4()
             undefined         AL:1           <RETURN>
             undefined4        Stack[-0xc]:4  local_c                                 XREF[3]:     00100e2c(W), 
                                                                                                   00100e3c(RW), 
                                                                                                   00100e43(R)  
             undefined4        Stack[-0x10]:4 local_10                                XREF[2]:     00100e25(W), 
                                                                                                   00100e40(R)  
             undefined8        Stack[-0x20]:8 local_20                                XREF[2]:     00100e21(W), 
                                                                                                   00100e35(R)  
                             challenge4                                      XREF[4]:     Entry Point(*), 
                                                                                          start:00101485(c), 00101ad8, 
                                                                                          00101c34(*)  
        00100e1d 55              PUSH       RBP
        00100e1e 48 89 e5        MOV        RBP,RSP
        00100e21 48 89 7d e8     MOV        qword ptr [RBP + local_20],RDI
        00100e25 c7 45 f8        MOV        dword ptr [RBP + local_10],0x0
                 00 00 00 00
        00100e2c c7 45 fc        MOV        dword ptr [RBP + local_c],0x0
                 00 00 00 00
        00100e33 eb 0b           JMP        LAB_00100e40
                             LAB_00100e35                                    XREF[1]:     00100e46(j)  
        00100e35 48 8b 45 e8     MOV        RAX,qword ptr [RBP + local_20]
        00100e39 c6 00 01        MOV        byte ptr [RAX],0x1
        00100e3c 83 45 fc 01     ADD        dword ptr [RBP + local_c],0x1
                             LAB_00100e40                                    XREF[1]:     00100e33(j)  
        00100e40 8b 45 f8        MOV        EAX,dword ptr [RBP + local_10]
        00100e43 39 45 fc        CMP        dword ptr [RBP + local_c],EAX
        00100e46 7c ed           JL         LAB_00100e35
        00100e48 90              NOP
        00100e49 5d              POP        RBP
        00100e4a c3              RET






```

# Level5
```c
void challenge5(undefined *param_1)

{
  int iVar1;
  time_t tVar2;
  long in_FS_OFFSET;
  int local_50;
  int local_4c;
  int aiStack72 [8];
  int aiStack40 [6];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  tVar2 = time((time_t *)0x0);
  srand((uint)tVar2);
  for (local_50 = 0; local_50 < 5; local_50 = local_50 + 1) {
    aiStack72[local_50] = 0;
    iVar1 = rand();
    aiStack40[local_50] = iVar1;
  }
  local_4c = 0;
  do {
    if (4 < local_4c) {
      *param_1 = 1;
LAB_00100ee0:
      if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
    if (aiStack72[local_4c] != aiStack40[local_4c]) {
      *param_1 = 0;
      goto LAB_00100ee0;
    }
    local_4c = local_4c + 1;
  } while( true );
}

```

# Level6
```c
/* WARNING: Removing unreachable block (ram,0x00100f1a) */

void challenge6(void)

{
  do {
  } while( true );
}

```

```c
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined challenge6()
             undefined         AL:1           <RETURN>
             undefined4        Stack[-0xc]:4  local_c                                 XREF[2]:     00100efe(W), 
                                                                                                   00100f0b(W)  
             undefined1        Stack[-0xd]:1  local_d                                 XREF[2]:     00100f05(W), 
                                                                                                   00100f12(R)  
             undefined8        Stack[-0x20]:8 local_20                                XREF[2]:     00100efa(W), 
                                                                                                   00100f1a(R)  
                             challenge6                                      XREF[4]:     Entry Point(*), 
                                                                                          start:001014cd(c), 00101ae8, 
                                                                                          00101c74(*)  
        00100ef6 55              PUSH       RBP
        00100ef7 48 89 e5        MOV        RBP,RSP
        00100efa 48 89 7d e8     MOV        qword ptr [RBP + local_20],RDI
        00100efe c7 45 fc        MOV        dword ptr [RBP + local_c],0x0
                 00 00 00 00
        00100f05 c6 45 fb 01     MOV        byte ptr [RBP + local_d],0x1
        00100f09 eb 07           JMP        LAB_00100f12
                             LAB_00100f0b                                    XREF[1]:     00100f18(j)  
        00100f0b c7 45 fc        MOV        dword ptr [RBP + local_c],0x1
                 01 00 00 00
                             LAB_00100f12                                    XREF[1]:     00100f09(j)  
        00100f12 0f b6 45 fb     MOVZX      EAX,byte ptr [RBP + local_d]
        00100f16 84 c0           TEST       AL,AL
        00100f18 75 f1           JNZ        LAB_00100f0b
        00100f1a 48 8b 45 e8     MOV        RAX,qword ptr [RBP + local_20]
        00100f1e c6 00 01        MOV        byte ptr [RAX],0x1
        00100f21 90              NOP
        00100f22 5d              POP        RBP
        00100f23 c3              RET

```
# Level7

```c
void challenge7(undefined *param_1)

{
  *param_1 = 1;
  sleep(0xffffffff);
  return;
}

```

# Level8

```c
void challenge8(void *param_1)

{
  undefined8 *puVar1;
  void **ppvVar2;
  void *pvVar3;
  
  ppvVar2 = (void **)malloc(0x18); //struct
  pvVar3 = malloc(0x1e);           //ptr
  *ppvVar2 = pvVar3;               
  *(undefined4 *)(ppvVar2 + 1) = 0x539;  //1337
  *(undefined4 *)((long)ppvVar2 + 0xc) = 0x3dfcd6ea;  //1039980266
  puVar1 = (undefined8 *)*ppvVar2;
  *puVar1 = 0x64206d6f646e6152;  //ptr value
  *(undefined4 *)(puVar1 + 1) = 0x617461;  //6386785
  ppvVar2[2] = param_1;
  return;
}


_DWORD *__fastcall challenge8(__int64 a1)
{
  _DWORD *result; // rax
  _DWORD *v2; // [rsp+18h] [rbp-8h]

  v2 = malloc(0x18uLL);
  *(_QWORD *)v2 = malloc(0x1EuLL);
  v2[2] = 1337;
  v2[3] = 1039980266;
  strcpy(*(char **)v2, "Random data");
  result = v2;
  *((_QWORD *)v2 + 2) = a1;
  return result;
}

/*

Here needs to review the assembly

struct unknown{  //0x18
 0x0  
	 ptr -> malloc (0x1e) 
 0x8  
	 0x539 1337
 0xc
	 0x3dfcd6ea 1039980266

 0x10
	 param_1 
}  

*/

```

# Level9

```c
unsigned __int64 __fastcall challenge9(bool *a1)
{
  char *i; // [rsp+18h] [rbp-58h]
  char dest[32]; // [rsp+20h] [rbp-50h] BYREF
  char src[40]; // [rsp+40h] [rbp-30h] BYREF
  unsigned __int64 v5; // [rsp+68h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  strcpy(src, "aBcdeFghiJKlMnopqRstuVWxYz");
  src[27] = 0;
  strcpy(dest, src);
  for ( i = dest; *i; ++i )
    *i = tolower(*i);
  *a1 = strcmp(src, dest) == 0;
  return __readfsqword(0x28u) ^ v5;
}
```

# Level10

```c
unsigned __int64 __fastcall challenge10(_BYTE *a1)
{
  int i; // [rsp+10h] [rbp-60h]
  int fd; // [rsp+14h] [rbp-5Ch]
  ssize_t v4; // [rsp+18h] [rbp-58h]
  char buf[72]; // [rsp+20h] [rbp-50h] BYREF
  unsigned __int64 v6; // [rsp+68h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  fd = open("/proc/self/cmdline", 0);
  if ( fd != -1 )
  {
    v4 = read(fd, buf, 0x3FuLL);
    if ( v4 > 0 )
    {
      close(fd);
      for ( i = 0; v4 > i; ++i )
      {
        if ( !buf[i] )
          buf[i] = 32;
      }
      buf[v4] = 0;
      if ( !strcmp(buf, "qilinglab") )
        *a1 = 1;
    }
  }
  return __readfsqword(0x28u) ^ v6;
}
```

# Level11

```c
unsigned __int64 __fastcall challenge11(_BYTE *a1)
{
  int v7; // [rsp+1Ch] [rbp-34h]
  int v8; // [rsp+24h] [rbp-2Ch]
  char s[4]; // [rsp+2Bh] [rbp-25h] BYREF
  char v10[4]; // [rsp+2Fh] [rbp-21h] BYREF
  char v11[4]; // [rsp+33h] [rbp-1Dh] BYREF
  unsigned __int64 v12; // [rsp+38h] [rbp-18h]

  v12 = __readfsqword(0x28u);
  _RAX = 0x40000000LL;
  __asm { cpuid }
  v7 = _RCX;
  v8 = _RDX;
  if ( __PAIR64__(_RBX, _RCX) == 0x696C6951614C676ELL && (_DWORD)_RDX == 538976354 )
    *a1 = 1;
  sprintf(
    s,
    "%c%c%c%c",
    (unsigned int)_RBX,
    (unsigned int)((int)_RBX >> 8),
    (unsigned int)((int)_RBX >> 16),
    (unsigned int)((int)_RBX >> 24));
  sprintf(
    v10,
    "%c%c%c%c",
    (unsigned int)v7,
    (unsigned int)(v7 >> 8),
    (unsigned int)(v7 >> 16),
    (unsigned int)(v7 >> 24));
  sprintf(
    v11,
    "%c%c%c%c",
    (unsigned int)v8,
    (unsigned int)(v8 >> 8),
    (unsigned int)(v8 >> 16),
    (unsigned int)(v8 >> 24));
  return __readfsqword(0x28u) ^ v12;
}
```