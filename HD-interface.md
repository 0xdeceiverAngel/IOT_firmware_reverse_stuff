# 

ref 
- https://ithelp.ithome.com.tw/articles/10241686
- https://wiki.csie.ncku.edu.tw/embedded/PWM
- https://makerpro.cc/2016/07/learning-interfaces-about-uart-i2c-spi/




![](https://www.mbtechworks.com/hardware/imgs/uart-spi-i2c.png)
![](https://img-blog.csdnimg.cn/20181214093903321.png)


# General Purpose Input/Output (GPIO)


>想成開關，GPIO可以是 input、output、analog或其他功能(pwm,timer,USART)，通用型泛用型的輸入、輸出pin(?)

# UART

>嚴格而論UART不是個具體的介面，此介面只提供一個雛形基礎，以此基礎再加搭電路與軟體，才可以實現不同的介面，如RS-232、RS-422、RS-485等。
>不過就Maker運用而言幾乎是用來實現RS-232介面，而RS-232介面只允許兩個裝置直接對接，無法接更多裝置（若為RS-422、RS-485則可接多個裝置）。

# I2C

>I2C與UART/RS-232一樣是兩條線路，最早是PHILIPS（今日的NXP）提出來，在晶片間的聯繫傳輸之用。I2C可以同時連接多個裝置，不似RS-232僅能一對一

# SPI

>與I2C相同是可以接多個裝置的，而且傳輸速度比I2C更快（事實上SD記憶卡的根基就是這個介面），而且與UART/RS-232一樣，發送與接收可同時進行。
>不過SPI也有缺點，一是隨著連接裝置數的增加，線路也是要增加的，每增加一個連接裝置，至少要增加一條，不像I2C可以一直維持只要兩條。而SPI在一對一連接時需要四條，一對二時要五條，一對三時要六條，即N+3的概念。另外SPI比I2C更少纜線化運用，多半是更短距離的連接。在實務上，I2C較常用來連接感測器，而SPI較常用來連接EEPROM記憶體、Flash記憶體（記憶卡），或一些液晶顯示器


# PWM

>Pulse-Width Modulation, 又稱pulse-duration modulation(PDM),是將脈波轉為類比信號的“一種技術”,利用在頻率不變的狀態下, 改變工作週期大小, 使整體平均電壓值上升或下降, 藉此間歇性電壓及功率切換以節省能源及控制等效果

![](https://wiki.csie.ncku.edu.tw/PWM_intr.PNG)


# driver

ref
- https://www.cnblogs.com/-Donge/articles/17668651.html
- https://www.pudn.club/linux/view-peripheral-chip-drivers-from-the-perspective-of-linux-kernel/
- https://zhuanlan.zhihu.com/p/445188798
- https://jyywiki.cn/OS/2023/index.html
- https://www.zhaixue.cc/weixin/weixin-book.html
- https://linmingjie.cn/index.php/archives/313/



- character device
    - stream
- block device
    - array