Ref
- https://bbs.kanxue.com/thread-277920.htm

Version
- wr740nv1_en_3_12_4_up

Download from
- https://members.driverguide.com/director/get.php/TL-WR740N_v1v2_100910.zip


```bash
user@vm-ubuntu18:~/firmwalker$ ./firmwalker.sh ~/firmware/_wr740nv1_en_3_12_4_up\(100910\).bin.extracted/squashfs-root/|sort|uniq -c|sort -r
      7 /sbin/hostapd
      6 /usr/bin/httpd
```


# Reverse httpd

Call stack
- httpDebugInit
	- CmdRpmHtm
	- DebugResultRpmHtm

```c
int httpDebugInit()
{
  signal(18, doClosePty);
  httpRpmConfAdd(2, "/userRpmNatDebugRpm26525557/start_art.html", &ArtRpmHtm);
  httpRpmConfAdd(2, "/userRpmNatDebugRpm26525557/linux_cmdline.html", &CmdRpmHtm);
  return httpRpmConfAdd(2, "/userRpm/DebugResultRpm.htm", DebugResultRpmHtm);
}
```

```c
int __fastcall CmdRpmHtm(int a1)
{
  int v2; // $v1
  int v3; // $v0
  int v4; // $v0
  int v5; // $t0

  if ( !pty_started )
  {
    pty_started = 1;
    v2 = forkpty(&pty, 0, 0, 0);
    child = v2;
    if ( v2 == -1 )
    {
      pty_started = 0;
      perror("forkpty");
    }
    else
    {
      if ( !v2 )
      {
        execl("/bin/sh", "sh", 0);
        exit(0);
      }
      v3 = fcntl(pty, 3, &fcntl);
      fcntl(pty, 4, v3 | 0x80);
    }
  }
  httpStatusSet(a1, 0);
  httpHeaderGenerate(a1);
  HttpWebV4Head(a1, 0, 0);
  v4 = httpRpmFsA(a1, "/userRpm/HttpDebugRpm.htm");
  v5 = 2;
  if ( v4 != 2 )
    return (__int16)HttpErrorPage(a1, 10, 0, 0);
  return v5;
}
```


```c
int __fastcall DebugResultRpmHtm(int a1)
{
  int v2; // $s4
  int v3; // $s6
  int v4; // $a0
  const char *Env; // $v0
  const char *nn_cmd; // $s0
  const char *v7; // $v0
  const char *v8; // $v0
  size_t v9; // $v0
  char *v10; // $a2
  const char *v11; // $a3
  int v12; // $v0
  int v13; // $v1
  int v14; // $a0
  int v15; // $a1
  int v16; // $v1
  ssize_t v17; // $a1
  char *v18; // $v0
  size_t v19; // $v0
  char *v20; // $v0
  const void *v21; // $s1
  char *v22; // $s0
  int v23; // $v0
  int v24; // $a0
  char v26[3072]; // [sp+18h] [-C10h] BYREF
  char *v27; // [sp+C18h] [-10h]
  int v28; // [sp+C1Ch] [-Ch]
  int v29; // [sp+C20h] [-8h]

  v28 = 256;
  v27 = v26;
  v29 = 0;
  httpStatusSet(a1, 0);
  v2 = 0;
  httpHeaderGenerate(a1);
  v3 = 0;
  if ( !HttpAccessPermit(a1) )
  {
    v4 = HttpDenyPage(a1) << 16;
    return v4 >> 16;
  }
  v26[0] = 0;
  if ( pty_started )
  {
    Env = (const char *)httpGetEnv(a1, "cmd");
    nn_cmd = Env;
    if ( Env )
    {
      if ( strcmp(Env, "exit") )
      {
        if ( !httpGetEnv(a1, "usr")
          || !httpGetEnv(a1, "passwd")
          || (v7 = (const char *)httpGetEnv(a1, "usr"), strcmp(v7, "osteam"))
          || (v8 = (const char *)httpGetEnv(a1, "passwd"), strcmp(v8, "5up")) )  //check username passwd
        {
          v10 = v26;
          v11 = "####User or Password not correct###\\n";
          do
          {
            v12 = *(_DWORD *)v11;
            v13 = *((_DWORD *)v11 + 1);
            v14 = *((_DWORD *)v11 + 2);
            v15 = *((_DWORD *)v11 + 3);
            v11 += 16;
            *(_DWORD *)v10 = v12;
            *((_DWORD *)v10 + 1) = v13;
            *((_DWORD *)v10 + 2) = v14;
            *((_DWORD *)v10 + 3) = v15;
            v10 += 16;
          }
          while ( v11 != "###\\n" );
          v16 = *(_DWORD *)v11;
          *((_WORD *)v10 + 2) = *((_WORD *)v11 + 2);
          *(_DWORD *)v10 = v16;
          goto LABEL_27;
        }
      }
	// if pass authentication 
      v9 = strlen(nn_cmd);
      write(pty, nn_cmd, v9); //execute cmd
      if ( strstr(nn_cmd, "ping") || strstr(nn_cmd, "cat") && !strchr(nn_cmd, 38) )
        write(pty, "&", 1u);
      write(pty, "\n", 1u);
    }
    taskDelay(10);
    while ( 1 )
    {
      v17 = read(pty, &v26[v2], 0x10u);
      ++v3;
      if ( v17 != 16 )
        break;
      v2 += 16;
      if ( v3 == 168 )
      {
        v17 = 0;
        break;
      }
    }
    v18 = &v26[v2];
    if ( (unsigned int)(v17 + 1) >= 2 )
      v18 = &v26[v2 + v17];
    *v18 = 0;
    while ( 1 )
    {
      v20 = strstr(v26, &byte_5249D0);
      v21 = v20 + 2;
      v22 = v20;
      if ( !v20 )
        break;
      v19 = strlen(v20 + 2);
      memmove(v22 + 4, v21, v19 + 1);
      *(_DWORD *)v22 = 1550998638;
    }
  }
LABEL_27:
  httpPrintf(a1, "<SCRIPT language=\"javascript\" type=\"text/javascript\">\nvar %s = new Array(\n", "cmdResult");
  httpPrintf(a1, "\"%s\",\n", v26);
  httpPrintf(a1, "0,0 );\n</SCRIPT>\n");
  HttpWebV4Head(a1, 0, 0);
  v23 = httpRpmFsA(a1, "/userRpm/DebugResult.htm");
  v24 = 2;
  if ( v23 != 2 )
  {
    v4 = HttpErrorPage(a1, 10, 0, 0) << 16;
    return v4 >> 16;
  }
  return v24;
}
```

# Emulate 

```bash
user@vm-ubuntu18:/tmp/FirmAE$ sudo ./run.sh -c dlink /home/user/firmware/DIR830LA1_FW100B07.bin
[*] /home/user/firmware/DIR830LA1_FW100B07.bin emulation start!!!
[*] extract done!!!
[*] get architecture done!!!
mke2fs 1.44.1 (24-Mar-2018)
cp: cannot stat '/tmp/FirmAE/binaries//console.mipseb': No such file or directory
```

Need download https://github.com/pr0v3rbs/FirmAE/releases put in binaries folder




```bash
user@vm-ubuntu18:/tmp/FirmAE$ sudo ./run.sh -d dlink /home/user/firmware/wr740nv1_en_3_12_4_up.bin 
[*] /home/user/firmware/wr740nv1_en_3_12_4_up.bin emulation start!!!
[*] extract done!!!
[*] get architecture done!!!
[*] /home/user/firmware/wr740nv1_en_3_12_4_up.bin already succeed emulation!!!

[IID] 3
[MODE] debug
[+] Network reachable on 192.168.0.1!
[+] Web service on 192.168.0.1
[+] Run debug!
Creating TAP device tap3_0...
Set 'tap3_0' persistent and owned by uid 0
Bringing up TAP device...
Starting emulation of firmware... /tmp/FirmAE/binaries//vmlinux.mipseb.4: No such file or directory
qemu-system-mips: qemu: could not load kernel '/tmp/FirmAE/binaries//vmlinux.mipseb.4': Failed to load ELF
Bringing down TAP device...
Deleting TAP device tap3_0...
Set 'tap3_0' nonpersistent
Done!
192.168.0.1 true true .031711885 .031711885
[*] firmware - wr740nv1_en_3_12_4_up
[*] IP - 192.168.0.1
[*] connecting to netcat (192.168.0.1:31337)
[-] failed to connect netcat
------------------------------
|       FirmAE Debugger      |
------------------------------
1. connect to socat
2. connect to shell
3. tcpdump
4. run gdbserver
5. file transfer
6. exit
> 
```


Try access `userRpmNatDebugRpm26525557/linux_cmdline.html`, return 404 

```
user@vm-ubuntu18:~$ curl http://192.168.0.1/userRpm/DebugResultRpm.htm
<title>404 Not Found</title>
<h1>404 Not Found</h1>
The resource requested could not be found on this server.
user@vm-ubuntu18:~$ curl http://192.168.0.1/userRpmNatDebugRpm26525557/linux_cmdline.html
<title>404 Not Found</title>
<h1>404 Not Found</h1>
The resource requested could not be found on this server.
```

Found `DebugResult.htm` ,but `linux_cmdline.html` is missing

```
user@vm-ubuntu18:~/firmware/_wr740nv1_en_3_12_4_up(100910).bin.extracted/squashfs-root$ find . -name *.htm|grep DebugResult
./web/userRpm/DebugResult.htm
```