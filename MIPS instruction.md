Ref
- https://isite.tw/2015/03/17/13075
- https://uweb.engr.arizona.edu/~ece369/Resources/spim/MIPSReference.pdf
- http://twins.ee.nctu.edu.tw/courses/ca_20/co_08_fall/lecture/Lecture%2002B-MIPS%20instructions.pdf

```
Name Register number Usage 

$zero 0 the constant value 0 
$v0-$v1 2-3 values for results and expression evaluation 
$a0-$a3 4-7 arguments 
$t0-$t7 8-15 temporaries 
$s0-$s7 16-23 saved 
$t8-$t9 24-25 more temporaries 
$gp 28 global pointer 
$sp 29 stack pointer 
$fp 30 frame pointer 
$ra 31 return address


0xF
	fp
		stack
	sp
0x0
```


Sample 1
```c
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[])
{
	puts("test");
	return 0;

}
```
Asm
```
$LC0:
	.ascii "test\000"
main:
	addiu $sp,$sp,-32  // sp=sp-32
	sw $31,28($sp)     // mem[$sp+28]=$31
	sw $fp,24($sp)    // mem[$sp+24]=$fp
	move $fp,$sp      // $fp = $sp
	
	sw $4,32($fp)     // mem[$sp+32]=$4
	sw $5,36($fp)     // mem[$sp+36]=$5
	lui $2,%hi($LC0)   // $2= $LC0 * 2^16
	addiu $4,$2,%lo($LC0)    // $4 =$2 + $LC0
	jal puts            // $ra=PC+4; go to address puts
	nop
	move $2,$0
	
	move $sp,$fp
	lw $31,28($sp)
	lw $fp,24($sp)
	addiu $sp,$sp,32
	jr $31

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
	int b=2;
	f(1,b,3,4,5);
	return 0;
}

```
Asm
```
f(int, int, int, int, int):
	addiu $sp,$sp,-8 #sp-=8
	sw $fp,4($sp) #mem sp+4 =fp
	move $fp,$sp  #fp= sp
	
	sw $4,8($fp)  #mem fp+8 =$4
	sw $5,12($fp) #mem fp+5 =$5
	sw $6,16($fp) #mem fp+6 =$6
	sw $7,20($fp) #mem fp+7 =$7
	
	lw $3,8($fp)
	lw $2,12($fp)
	nop
	addu $3,$3,$2
	
	lw $2,16($fp)
	nop
	addu $3,$3,$2
	
	lw $2,20($fp)
	nop
	addu $3,$3,$2
	
	lw $2,24($fp) #mem $2= fp+24 
	nop
	addu $2,$3,$2  #return $2
	
	move $sp,$fp
	lw $fp,4($sp)
	addiu $sp,$sp,8
	jr $31
	nop

  

main:
	addiu $sp,$sp,-48
	sw $31,44($sp)
	sw $fp,40($sp)
	move $fp,$sp
	
	sw $4,48($fp)
	sw $5,52($fp)
	
	li $2,2            #$2 0x2     
	sw $2,32($fp)      #mem fp+32 = $2
	
	li $2,5            #$2 0x5    
	sw $2,16($sp)      #mem fp+16 = $2
	
	li $7,4            #$7 0x4     
	li $6,3            #$6 0x3    
	lw $5,32($fp)      #$5 = mem fp+32(0x2)
	li $4,1            #$4 0x1    
	jal f(int, int, int, int, int)
	
	nop
	move $2,$0
	move $sp,$fp
	lw $31,44($sp)
	lw $fp,40($sp)
	addiu $sp,$sp,48
	jr $31
	nop
