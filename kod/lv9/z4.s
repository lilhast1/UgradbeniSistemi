.data
	tekst: .asciz "____....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....____"
	N : .word 20
	N_MAX: .word 20
	format: .asciz "\n%d %d %d\n"
	arr: 
	.word   0x0000F000
    .word   0x0000F001
    .word   0x0000F002
    .word   0x0000F000
    .word   0x0000F001
    .word   0x0000F002
    .word   0x0000F000
    .word   0x0000F001
    .word   0x0000F002
    .word   0x0000F000
    .word   0x0000F001
    .word   0x0000F002
    .word   0x0000F000
    .word   0x0000F001
    .word   0x0000F002
    .word   0x0000F000
    .word   0x0000F001
    .word   0x0000F002
    .word   0x0000F000
    .word   0x0000F001
.text

.global _start
_start:
	// unesi N
	mov r7, #3
	mov r0, #0
	mov r1, =tekst
	mov r2, #2 
	swi #0	

	mov r6, =N
	push {lr}
	bl readint // parsiraj 
	pop {lr}
	cmp r7, 0xFFFFFFFF // nema inta
	bne _start
	cmp r7, #N_MAX // previse brojeva
	bgt _start

	// unesi niz
	mov r7, #3
	mov r0, #0
	mov r1, =tekst
	mov r3, #N
	mov r2, [r3] // *N 
	swi #0	


	mov r6, =arr
parse:
	push {lr}
	bl readint
	pop {lr}
	cmp r7, 0xFFFFFFFF
	beq procitano
	add r6, #4
	b parse
procitano:
	mov r0, =arr
	push{lr}
	bl sort
	pop{lr}  

// nadji medijanu, max i opseg
	mov r0, =arr // r0 ptr
	ldr r1, [r0] // r1 - min
	ldr r3, #N // r3 - N
	sub r3, #4 // r3 = N - 1
	lsl r3, #2
	ldr r2, [r0, r3] // r2 - max
	lsr r3, #3  // r3 - N / 2
	lsl r3, #2  // r3 = 4 * floor(N/2)  
	add r0, r3
	ldr r3, [r0]
	push {r1, r2, r3}
	ldr r0, =format
	bl printf



exit:
	mov r0, #0
	mov r7, #1
	swi #0












// citaj int sa std in na lokaciju data u r6 a u r7 stavlja lokaciju buffera koju nije mogao
readint:
	push {r11}
	mov r0, =tekst
	mov r2, =tekst
	add r2, #N
	// dok je procitano numericko idi desno
desno:ldrb r1, [r0]
	cmp r1, #48
	blt vrati
	cmp r1, #57
	bgt vrati
	add r0, #1
	cmp r0, r2 // izvan opsega izlazi
	ble desno:
	// kad nije vrati lijevo
	vrati:
	sub r0, #1
	mov r7, r0

	cmp r0, =tekst
	blt NO_INT

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

	str r2, [r6]

end_read_int:	bx lr
NO_INT: mov r7, 0xFFFFFFFF
		bx lr

// sortiraj niz intova iz [r0]
sort:
	mov r5, r0
	loop:

		ldrb r2, [r0]
		mov r1, r0
		sub r1, #1  

		inner_loop:
			ldrb r4, [r1]
			cmp r2, r4 
			blt end_if 
			if: add r1, #1
				b end_inner
			end_if: strb r4, [r1, 1]

			sub r1, #1
			cmp r1, r5
			bge inner_loop
		end_inner:
		strb r2, [r1]

		add r0, #1
		cmp r0, r3 
		blt loop
	end_loop:
end_sort:	bx lr