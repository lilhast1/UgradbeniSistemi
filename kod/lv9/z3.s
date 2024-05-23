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
	mov r1, =tekst
	mov r2, #N 
	swi #0

	mov r0, =tekst
	mov r2, =tekst
	add r2, #N
	// dok je procitano numericko idi desno
desno:ldrb r1, [r0]
	cmp r1, #48
	bl vrati
	cmp r1, #58
	bge vrati
	add r0, #1
	cmp r0, r2 // izvan opsega izlazi
	ble desno:
	// kad nije vrati lijevo
	vrati:
	sub r0, #1

	cmp r0, =tekst
	bl ponovo

	mov r1, =tekst

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

	str r2, LOCATION

exit:
	mov r0, #0
	mov r7, #1
	swi
