
Ref
- https://www.iotsec-zone.com/article?id=358
- https://www.iotsec-zone.com/article?id=375


# Universal Asynchronous Receiver/Transmitter (UART)

Pin
- GND -
- VCC +
- TXD
- RXD

配合三用電錶蜂鳴器，找出GND\\VCC，TX\\RX 用uart轉usb，交叉測試

設定bitrate，沒有分析儀就用猜的，連上shell

利用ROM讀取的工具直接dump出來，丟binwalk

# Joint Test Action Group (JTAG)

邊界掃描:向晶片發送資料，將確認輸出與輸入，從而驗證是否正常執行

功能
- 燒錄
- debug 對晶片和周邊設備
- 針腳debug

有不同PIN腳數量，對應到不同的腳位功能

Jtagulator 硬體可以用來辨識腳位等