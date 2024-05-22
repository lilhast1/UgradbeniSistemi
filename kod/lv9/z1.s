.global _start
_start:
	
	mov r4, #N // N = 48
	mov r0, #0
	mov r1, #1
	mov r2, #1
	mov r5, #FIB_ARR
_fib:
	add r2, r1, r0
	push {r0}
	str r0, [r5], #4
	mov r0, r1
	mov r1, r2
	sub r4, #1
	cmp r4, #0
	bge _fib
	
	
	N: .word 48
	FIB_ARR:	.word 0x8000
	