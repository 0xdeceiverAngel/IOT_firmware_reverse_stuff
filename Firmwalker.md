Ref
- https://www.ol4three.com/2021/03/10/IOT/D-Link-DIR-882%E5%9B%BA%E4%BB%B6%E8%A7%A3%E5%AF%86%E5%AE%9E%E9%AA%8C/


Extract from unencrypted firmware , find decrypt tool in transition period firmware
```
Archive:  DIR-882_REVA_FIRMWARE_v1.10B02.zip
  inflating: DIR-882_REVA_RELEASE_NOTES_v1.10B02_EN.pdf  
  inflating: DIR-882_REVA_TRANSITION_INSTRUCTIONS_v1.04B02_EN.pdf  
 extracting: DIR882A1_FW104B02_Middle_FW_Unencrypt.bin  
 extracting: DIR882A1_FW110B02.bin   


user@vm-ubuntu18:~/Practice-Note/D-Link DIR-882固件解密实验$ binwalk DIR882A1_FW104B02_Middle_FW_Unencrypt.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             uImage header, header size: 64 bytes, header CRC: 0x50982AB1, created: 2018-03-11 13:18:48, image size: 13265102 bytes, Data Address: 0x81001000, Entry Point: 0x816118E0, data CRC: 0x3A2AC829, OS: Linux, CPU: MIPS, image type: OS Kernel Image, compression type: lzma, image name: "Linux Kernel Image"
160           0xA0            LZMA compressed data, properties: 0x5D, dictionary size: 33554432 bytes, uncompressed size: 18684352 bytes

user@vm-ubuntu18:~/Practice-Note/D-Link DIR-882固件解密实验$ binwalk DIR882A1_FW110B02.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
1391843       0x153CE3        QNX4 Boot Block

user@vm-ubuntu18:~/Practice-Note/D-Link DIR-882固件解密实验$ binwalk DIR_882_FW120B06.BIN

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------


user@vm-ubuntu18:~/Practice-Note/D-Link DIR-882固件解密实验/_DIR882A1_FW104B02_Middle_FW_Unencrypt.bin.extracted$ binwalk -e A0

user@vm-ubuntu18:~/Practice-Note/D-Link DIR-882固件解密实验/_DIR882A1_FW104B02_Middle_FW_Unencrypt.bin.extracted/_A0.extracted$ binwalk -e 8AB758

```

Decrypt firmware
```
sudo chroot . qemu-mipsel-static ./bin/sh

# ./bin/imgdecrypt DIR_882_FW120B06.BIN
key:C05FBF1936C99429CE2A0781F08D6AD8


user@vm-ubuntu18:~/Practice-Note/D-Link DIR-882固件解密实验/_DIR882A1_FW104B02__FW_Unencrypt.bin.extracted/_A0.extracted/_8AB758.extracted/cpio-root$ su
do binwalk DIR_882_FW120B06.BIN 
[sudo] password for user: 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             uImage header, header size: 64 bytes, header CRC: 0x7CC28308, created: 2019-05-16 05:10:52, image size: 13752582 bytes, Data Address: 0x81001000, Entry Point: 0x815FF440, data CRC: 0x32B9B72C, OS: Linux, CPU: MIPS, image type: OS Kernel Image, compression type: lzma, image name: "Linux Kernel Image"
160           0xA0            LZMA compressed data, properties: 0x5D, dictionary size: 33554432 bytes, uncompressed size: 19102144 bytes
11080822      0xA91476        gzip compressed data, ASCII, has header CRC, has 20713 bytes of extra data, has comment, last modified: 1995-11-13 08:03:50


```


Using firmwaler
```bash
user@vm-ubuntu18:~/firmwalker$ ./firmwalker.sh ~/Practice-Note/DIR-882/_DIR_882_FW120B06.BIN.extracted/_A0.extracted/_8957DC.extracted/
***Firmware Directory***
/home/user/Practice-Note/DIR-882/_DIR_882_FW120B06.BIN.extracted/_A0.extracted/_8957DC.extracted/
***Search for password files***
##################################### passwd

##################################### shadow

##################################### *.psk

***Search for Unix-MD5 hashes***


***Search for SSL related files***
##################################### *.crt

##################################### *.pem
/cpio-root/etc_ro/cacert.pem
/cpio-root/etc_ro/public.pem
Shodan cli not found.
unable to load certificate
139630492807616:error:0909006C:PEM routines:get_name:no start line:../crypto/pem/pem_lib.c:745:Expecting: TRUSTED CERTIFICATE
Incorrect File Content:Continuing
Shodan cli not found.

##################################### *.cer

##################################### *.p7b

##################################### *.p12

##################################### *.key


***Search for SSH related files***
##################################### authorized_keys

##################################### *authorized_keys*

##################################### host_key

##################################### *host_key*

##################################### id_rsa

##################################### *id_rsa*

##################################### id_dsa

##################################### *id_dsa*

##################################### *.pub


***Search for files***
##################################### *.conf
/cpio-root/etc_ro/lighttpd/lighttpd.conf
/cpio-root/etc_ro/lighttpd/lighttpd_webdav.conf
/cpio-root/etc_ro/lld2d.conf
/cpio-root/etc/jcpd.conf

##################################### *.cfg

##################################### *.ini


***Search for database related files***
##################################### *.db

##################################### *.sqlite

##################################### *.sqlite3


***Search for shell scripts***
##################################### shell scripts
/firmwalker.sh
/cpio-root/etc_ro/onetouch/scripts/rss_xml.sh
/cpio-root/etc_ro/onetouch/scripts/rss_checker.sh
/cpio-root/etc_ro/rept_dbdc_test.sh
/cpio-root/etc_ro/apcli_connect_trial.sh
/cpio-root/etc_ro/rept_test.sh
/cpio-root/sbin/cpubusy.sh
/cpio-root/sbin/nand_test_reboot.sh

...
```