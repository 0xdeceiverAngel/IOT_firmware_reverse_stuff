Ref
- http://sp1.wikidot.com/arm
- https://xta0.me/2013/06/15/ARM-Assembly.html
- https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff807?token=

```

r7 (FP)  : frame pointer
r13 (SP) : stack pointer 
r14 (LR) : link register 
r15 (PC) : program counter


0xf
		lr
		old r7(fp)
	R7
		saved registers
		local storage
	SP
0x0

``` 



Sample 1
```c
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[])
{
	puts("hello");
	return 0;
}
```

asm
```asm
# Push {r1,lr} 
# 0x4 lr val
# 0x0 r1 val


.LC0:
	.ascii "hello\000"
main:
	push {r3, lr}
	movw r0, #:lower16:.LC0
	movt r0, #:upper16:.LC0
	bl puts
	movs r0, #0
	pop {r3, pc}
```

Sample 2
```c
#include <stdio.h>
#include <string.h>
int f(int a,int b,int c,int d,int e)
{
	return a+b+c+d+e;
}
int main(int argc, char *argv[])
{
	int b=0;
	scanf("%d",&b);
	int k=f(6,b,7,8,9);
	printf("%d",k);
	return 0;
}
```

Asm
```
f(int, int, int, int, int):
	push {r7}         # 4
	sub sp, sp, #20   # sp=sp-20
	add r7, sp, #0
	
	str r0, [r7, #12]
	str r1, [r7, #8]
	str r2, [r7, #4]
	str r3, [r7]
	
	ldr r2, [r7, #12]
	ldr r3, [r7, #8]
	add r2, r2, r3
	
	ldr r3, [r7, #4]
	add r2, r2, r3
	
	ldr r3, [r7]
	add r2, r2, r3
	
	ldr r3, [r7, #24] # get last arg ,(4+20)
	add r3, r3, r2
	
	mov r0, r3   # return 
	
	adds r7, r7, #20
	mov sp, r7
	ldr r7, [sp], #4
	bx lr
.LC0:
	.ascii "%d\000"
main:
	push {r7, lr}
	sub sp, sp, #24
	add r7, sp, #8
	str r0, [r7, #4]
	str r1, [r7]
	
	movs r3, #0      # r3=0 , b=0
	str r3, [r7, #8] # [r7+8]=r3
	add r3, r7, #8   #  r3=r7+8 
	mov r1, r3       #  r1=r3
	
	movw r0, #:lower16:.LC0
	movt r0, #:upper16:.LC0
	bl __isoc99_scanf
	
	ldr r1, [r7, #8] # r1=[r7+8] 
	movs r3, #9
	str r3, [sp] # [sp]=r3
	movs r3, #8
	movs r2, #7
	movs r0, #6
	bl f(int, int, int, int, int)
	
	str r0, [r7, #12]  # [r7+12]=r0
	ldr r1, [r7, #12]  # r1=[r7+12]
	movw r0, #:lower16:.LC0
	movt r0, #:upper16:.LC0
	bl printf

	movs r3, #0
	mov r0, r3
	adds r7, r7, #16
	mov sp, r7
	pop {r7, pc}
	```