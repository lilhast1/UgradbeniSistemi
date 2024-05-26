.global _start
.text
_start:
	// ucitaj u buffer
	mov r2, #120
	ldr r1, =buffer
	mov r0, #0
	mov r7, #3
	swi #0

	// obradi buffer i spasi u N
	// r0 - duzina niza, r1 - lokacija niza, r2-buffer
	// r0 - dokle je buffer procitan
	push {r0} // broj karaktera u bufferu spsavam
	ldr r1, =N
	ldr r2, =buffer
	bl readint

	mov r2, r0
	ldr r1, =N

	ldr r3, [r1]
	cmp r3, #10
	bgt _start // maksimalna velicina niza prepucana

	mov r4, #0
	ldr r1, =arr
fill_arr:
	push {r3, r4}

	bl readint
	mov r2, r0
	add r1, #4

	pop {r3, r4}
	cmp r4, r3
	
	blt fill_arr
	
	// sortiraj arr
	mov r0, r3
	push {r3}

	ldr r1, =arr
	bl sort


	// nadji medianu - r1, max - r2 i opseg - r3
	pop {r0} // r0 je N
	ldr r4, =arr
	ldr r3, [r4] // r3 je min

	sub r0, #1 // indeks zadnjeg
	lsl r5, r0, #2
	ldr r2, [r4, r5] // uzmi zadnji on je max

	lsr r5, r5, #3  // r5 je sada N/2
	lsl r5, r5, #2  // r5 je sada 2N
	ldr r1, [r4, r5] // mediana

	sub r3, r2, r3 // opseg sada

	// printf zovi
	ldr r0, =format
	bl printf
exit:
	mov r0, #0
	mov r7, #1
	swi #0


// funkcija koja pretvara ASCII u int
// r0 - duzina niza, r1 - lokacija, r2 - buffer
// r0 - dokle je buffer procitan
readint:
	ldrb r3, [r2], #1
	cmp r3, #48 // 48 = '0'
	blt second_chance
	cmp r3, #57 // 57 = '9'
	bgt second_chance

	mov r4, #0
parse:
	sub r3, r3, #48

	add r4, r3, r4

	ldrb r3, [r2], #1
	cmp r3, #48 // 48 = '0'
	blt end_read
	cmp r3, #57 // 57 = '9'
	bgt end_read

	lsl r5, r4, #3
	lsl r6, r4, #1
	add r4, r5, r6

	b parse

end_read:
	mov r0, r2
	str r4, [r1]
	bx lr
second_chance:
	cmp r3, #0x20 // space
	beq readint
	cmp r3, #13 // newline
	beq readint
	cmp r3, #9
	beq readint // tab
	b end_read

// r0 - duzina, r1 - niz
sort:
	mov r4, r1
	add r5, r4, r0
	add r0, r4, #1
	
	L1:
	ldrb r2, [r0]
	mov r1, r0
	loop:
	cmp r1, r4
	ble end_loop
		sub r6, r1, #4
		ldrb r3, [r6]
		cmp r3, r2
		ble end_loop
		strb r3, [r1]
		sub r1, #4
		b loop
	end_loop:
	strb r2, [r1]
	add r0, #4
	cmp r0, r5
	blt L1
	bx lr


.data
buffer: .byte 0,0,0,0,0,0,0,0,0,0,0,0,0
arr: .word 0,0,0,0,0,0,0,0,0,0,0,0,0,0
N: .word 0
format: .asciz "\n %d %d %d \n"