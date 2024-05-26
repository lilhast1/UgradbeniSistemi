.global _start
.text
_start:
// ucitaj u buffer
	mov r2, #16
	ldr r1, =buffer
	mov r0, #0
	mov r7, #3
	swi #0

	cmp r0, #16
	bgt _start

// r4 - niz, r5 - kraj, r0 - prva petlja, r1 - druga petlja
	ldr r4, =buffer
	add r5, r4, r0
	add r0, r4, #1
	
	L1:
	ldrb r2, [r0]
	mov r1, r0
	loop:
	cmp r1, r4
	ble end_loop
		sub r6, r1, #1
		ldrb r3, [r6]
		cmp r3, r2
		ble end_loop
		strb r3, [r1]
		sub r1, #1
		b loop
	end_loop:
	strb r2, [r1]
	add r0, #1
	cmp r0, r5
	blt L1

	mov r2, #16
	ldr r1, =buffer
	mov r0, #1
	mov r7, #4
	swi #0

exit:
	mov r0, #0
	mov r7, #1
	swi #0

.data
buffer: .byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
