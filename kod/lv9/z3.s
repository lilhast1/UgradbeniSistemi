.data
	tekst: .asciz "____....____"
	N : .word 12
	LOCATION: .word 33
.text
.global _start
_start:
	// uzmi 12 iz stdin
ponovo:
	mov r7, #3
	mov r0, #0
	ldr r1, tekst_addr
	mov r2, #12
	swi #0

	ldr r0, tekst_addr
	ldr r2, tekst_addr
	add r2, #12
	// dok je procitano numericko idi desno
desno:ldrb r1, [r0]
	cmp r1, #48
	blt vrati
	cmp r1, #58
	bge vrati
	add r0, #1
	cmp r0, r2 // izvan opsega izlazi
	ble desno
	// kad nije vrati lijevo
	vrati:
	sub r0, #1
	ldr r1, tekst_addr
	cmp r0, r1
	blt ponovo

	ldr r1, tekst_addr

	mov r2, #0
procesiraj:
	ldrb r3, [r0], #-1
	
	sub r3, #48

	mov r4, r3
	lsl r4, #3
	lsl r3, #1
	add r3, r4 // mnozenje r3 sa 10

	add r2, r3 

	cmp r0, r1
	bge procesiraj

	str r2, loc

exit:
	mov r0, #0
	mov r7, #1
	swi #0

tekst_addr: .word tekst
loc: .word LOCATION
