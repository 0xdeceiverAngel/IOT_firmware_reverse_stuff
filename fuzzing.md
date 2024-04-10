# AFL++

ref
- https://www.anquanke.com/post/id/269066
- https://www.ruanx.net/fuzzing-newbie-guide/
- https://www.wangan.com/p/7fy78y1f0efcbba2
- https://tttang.com/archive/1508/
- https://thinkycx.me/2019-01-28-a-simple-AFL-tutorial-for-beginners.html
- https://www.cnblogs.com/WangAoBo/p/8280352.html
- https://blog.attify.com/fuzzing-iot-binaries-with-afl-part-ii/
- https://r888800009.github.io/software/security/fuzzing/
- https://paper.seebug.org/842/
- https://github.com/alex-maleno/Fuzzing-Module
- https://github.com/mykter/afl-training
- https://rk700.github.io/2018/01/04/afl-mutations/
- https://rk700.github.io/2019/11/29/unifuzzer/
- https://ithelp.ithome.com.tw/articles/10287944

>sudo QEMU_LD_PREFIX=./sr20/squashfs-root/ /home/user/fuzz/AFLplusplus/afl-fuzz -Q -i ./bmp-input -o ./bmp-output -- ./sr20/squashfs-root/usr/bin/bmp2tiff @@ /dev/null


Here only test SR20 firmware's binary bmp2tiff

```
┌─ process timing ────────────────────────────────────┬─ overall results ────┐
│        run time : 0 days, 0 hrs, 4 min, 56 sec      │  cycles done : 0     │
│   last new find : 0 days, 0 hrs, 0 min, 19 sec      │ corpus count : 169   │
│last saved crash : 0 days, 0 hrs, 0 min, 38 sec      │saved crashes : 20    │
│ last saved hang : 0 days, 0 hrs, 0 min, 33 sec      │  saved hangs : 25    │
├─ cycle progress ─────────────────────┬─ map coverage┴──────────────────────┤
│  now processing : 152.1 (89.9%)      │    map density : 0.29% / 0.63%      │
│  runs timed out : 0 (0.00%)          │ count coverage : 2.36 bits/tuple    │
├─ stage progress ─────────────────────┼─ findings in depth ─────────────────┤
│  now trying : splice 1               │ favored items : 38 (22.49%)         │
│ stage execs : 41/56 (73.21%)         │  new edges on : 50 (29.59%)         │
│ total execs : 100k                   │ total crashes : 247 (20 saved)      │
│  exec speed : 1983/sec               │  total tmouts : 3035 (0 saved)      │
├─ fuzzing strategy yields ────────────┴─────────────┬─ item geometry ───────┤
│   bit flips : disabled (default, enable with -D)   │    levels : 10        │
│  byte flips : disabled (default, enable with -D)   │   pending : 121       │
│ arithmetics : disabled (default, enable with -D)   │  pend fav : 0         │
│  known ints : disabled (default, enable with -D)   │ own finds : 168       │
│  dictionary : n/a                                  │  imported : 0         │
│havoc/splice : 180/58.5k, 8/35.2k                   │ stability : 100.00%   │
│py/custom/rq : unused, unused, unused, unused       ├───────────────────────┘
│    trim/eff : 99.82%/384, disabled                 │          [cpu000:  6%]
└─ strategy: explore ────────── state: started :-) ──┘
```

```
fuzz/bmp-output/default/crashes# xxd id:000017,sig:11,src:000148,time:240239,execs:71263,op:havoc,rep:1
00000000: 424d 8a4d 0000 04fa 0000 0500 0000 2a00  BM.M..........*.
00000010: 1800 0200 0002 8002 ffff 1a17 0800 0200  ................
```

>./AFLplusplus/afl-clang-fast++ simple_crash.cpp -o target_fast
>./AFLplusplus/afl-fuzz -i testdata -o ./out -- ./test1

# outout folder

```
queue：存放所有具有独特执行路径的测试用例。
crashes：导致目标接收致命signal而崩溃的独特测试用例。
crashes/README.txt：保存了目标执行这些crash文件的命令行参数。
hangs：导致目标超时的独特测试用例。
fuzzer_stats：afl-fuzz的运行状态。
plot_data：用于afl-plot绘图。
```


# GDBFuzz
https://github.com/boschresearch/gdbfuzz

# afl socket
- https://github.com/LyleMi/aflnw
- https://github.com/aflnet/aflnet
- https://gitlab.com/akihe/radamsa
- https://github.com/zyingp/desockmulti

~~或是自己寫扣接上 AFL~~

- Naive fuzzing using Radamsa，寫 py 走網路戳 web
- 讓 socket 從檔案吃
    - patch asm 
    - LD_PRELOAD desockmulti , feed data with stdin
        - patchelf --add-needed ./lib/libpthread.so.0 ./usr/sbin/httpd_patched
    - 重寫daemon，使其返回 0 而無需實際分叉
    - close 改 exit ，讓httpd在退出之前恰好處理 1 個請求


# notes

對無源碼的程式進行fuzz一般有兩種方法:

- 對二進位檔案進行插樁
    - base on afl-qemu
- 使用-n選項進行傳統的fuzz測試
    -  fuzz without instrumentation (non-instrumented mode)

>提到Unicorn，就不得不说起QEMU。QEMU是一款开源的虚拟机，可以模拟运行多种CPU架构的程序或系统。而Unicorn正是基于QEMU，它提取了QEMU中与CPU模拟相关的核心代码，并在外层进行了包装，提供了多种语言的API接口。

>Unicorn最新的release是2017年的1.0.1版本，这是基于QEMU 2的，然而今年QEMU已经发布到QEMU 4了。


>关于QEMU的CPU模拟原理，读者可以在网上搜到一些专门的介绍，例如这篇。大致来说，QEMU是通过引入一层中间语言，TCG，来实现在主机上模拟执行不同架构的代码。例如，如果在x86服务器上模拟MIPS的代码，QEMU会先以基本块（Basic Block）为单位，将MIPS指令经由TCG这一层翻译成x86代码，得到TB(Translation Block)，最终在主机上执行。
>而为了提高模拟运行的效率，QEMU还加入了TB缓存和链接机制。通过缓存翻译完成的TB，减少了下次执行时的翻译开销，这即就是Unicorn所说的JIT。而TB链接机制，则是把原始代码基本块之间的跳转关系，映射到TB之间，从而尽可能地减少了查找缓存的次数和相关的上下文切换。

>Unicorn所提供的hook功能，就是在目标代码翻译成TCG时，插入相关的TCG指令

# mutate

bitflip，按位翻转，1变为0，0变为1
arithmetic，整数加/减算术运算
interest，把一些特殊内容替换到原文件中
dictionary，把自动生成或用户提供的token替换/插入到原文件中
havoc，中文意思是“大破坏”，此阶段会对原文件进行大量变异，具体见下文
splice，中文意思是“绞接”，此阶段会将两个文件拼接起来得到一个新的文件

# TODO
- hardness
- parallel fuzzing
- Various cmd 
- compile env_variables
- Paper
- afl-whatsup
- afl-stat
- PYTHIA
- coverage to source code
- libfuzzer 可以黑箱？
- code trace