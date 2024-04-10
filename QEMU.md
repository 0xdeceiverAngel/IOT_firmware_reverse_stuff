
Ref
- https://zhuanlan.zhihu.com/p/55685380
- https://blog.csdn.net/weixin_51760563/article/details/119935101
- https://www.cnblogs.com/tangtangworld/p/14157558.html
- https://blog.csdn.net/weixin_43194921/article/details/104702724
- https://www.slideshare.net/ChiaweiWang3/qemu-introduction

# arm
```
user@user-virtual-machine:~$ arm-linux-gnueabi-gcc -static test.c 
user@user-virtual-machine:~$ qemu-arm ./a.out 
```

```
qemu-system-arm -M vexpress-a9 -kernel vmlinuz-3.2.0-4-vexpress -initrd initrd.img-3.2.0-4-vexpress \
-drive if=sd,file=debian_wheezy_armhf_standard.qcow2 \
-append "root=/dev/mmcblk0p2 console=ttyAMA0" \
-net nic -net tap,ifname=tap0,script=no,downscript=no su
```



# mips

install the debian by own

http://ftp.debian.org/debian/dists/Debian10.13/main/installer-mips/current/images/malta/netboot/


```
qemu-system-mips -M malta -m 512 -hda mips.img -kernel vmlinux-4.19.0-21-4kc-malta -initrd initrd.gz -append "console=ttyS0 nokaslr" -nographic
```


```text
https://people.debian.org/~aurel32/qemu/mipsel/

vmlinux-2.6.32-5-4kc-malta
debian_squeeze_mipsel_standard.qcow2

sudo brctl addbr virbr0 
sudo ifconfig virbr0 192.168.122.1/24 up
sudo tunctl -t tap0 
sudo ifconfig tap0 192.168.122.11/24 up 
sudo brctl addif virbr0 tap0

sudo qemu-system-mipsel -M malta -kernel vmlinux-2.6.32-5-4kc-malta -hda debian_squeeze_mipsel_standard.qcow2 -append "root=/dev/sda1 console=tty0" -net nic -net tap,ifname=tap0,script=no,downscript=no -nographic
```


# Another method

Instead use prebuild image, install debian in qemu by self