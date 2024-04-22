#

Arduino uno

Get compiled file 

```
Blink.ino.eep:                 ASCII text, with CRLF line terminators
Blink.ino.elf:                 ELF 32-bit LSB executable, Atmel AVR 8-bit, version 1 (SYSV), statically linked, with debug_info, not stripped
Blink.ino.hex:                 ASCII text, with CRLF line terminators
Blink.ino.with_bootloader.bin: data
Blink.ino.with_bootloader.hex: ASCII text
```

arduino_due_
```
/tmp/aa/build/arduino.sam.arduino_due_x  file *
Blink.ino.bin: data
Blink.ino.elf: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, with debug_info, not stripped
Blink.ino.map: ASCII text, with CRLF line terminators
```


In ida
```c=
void init()
{
  int v0; // r0
  uint32_t v1; // r4
  uint32_t v2; // r0

  v0 = SystemInit();
  MEMORY[0xE000E014] = SystemCoreClock / 0x3E8u - 1;
  v1 = 0;
  MEMORY[0xE000ED23] = -16;
  MEMORY[0xE000E018] = 0;
  MEMORY[0xE000E010] = 7;
  _libc_init_array(v0);
  do
  {
    v2 = v1++;
    digitalWrite(v2, 0);
  }
  while ( v1 != 79 );
  MEMORY[0x400E0EA0] = -1;
  MEMORY[0x400E10A0] = -1;
  MEMORY[0x400E12A0] = -1;
  MEMORY[0x400E14A0] = -1;
  PIO_Configure(1074662912, 1, 768, 0);
  digitalWrite(0, 1u);
  PIO_Configure(1074662912, 1, 3072, 0);
  PIO_Configure(1074662912, 1, 12288, 0);
  PIO_Configure(1074664448, 2, 48, 0);
  PIO_Configure(1074663424, 1, 3072, 0);
  PIO_Configure(1074662912, 1, 3, 0);
  PIO_Configure(1074663424, 1, 49152, 0);
  pmc_enable_periph_clk(37);
  adc_init(1074528256, SystemCoreClock, 20000000, 12);
  adc_configure_timing(1074528256, 0, 3145728, 1);
  adc_configure_trigger(1074528256, 0, 0);
  adc_disable_interrupt(1074528256, -1);
  adc_disable_all_channel(1074528256);
  analogOutputInit();
}


void loop()
{
  digitalWrite(0xDu, 1u);
  delay(0x3E8u);
  digitalWrite(0xDu, 0);
  delay(0x3E8u);
}
```