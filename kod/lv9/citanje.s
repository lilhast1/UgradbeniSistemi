.global _start
.text
_start:
	// ucitaj u buffer
	mov r2, #16
	ldr r1, =buffer
	mov r0, #0
	mov r7, #3
	swi #0

	ldr r1, =buffer
	add r2, r1, r0 // r2 je kraj unesog niza
	mov r3, #0

	mov r0, r1
loop:
	ldrb r4, [r0]
	cmp r4, #48 // '0'=48
	blt end_unos
	cmp r4, #57 // '9'=57
	bgt end_unos

	sub r4, r4, #48

	// mnozi r3 sa 10
	lsl r5, r3, #3
	lsl r6, r3, #1
	add r3, r5, r6

	// dodaj r4
	add r3, r3, r4

	add r0, r0, #1
	cmp r0, r2
	blt loop
end_unos:
	cmp r0, r1
	beq _start

	// upisi r3 u var
	ldr r0, =buffer
	str r3, [r0]

exit:
	mov r0, #0
	mov r7, #1
	swi #0


.data
buffer: .byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
var: .word 0