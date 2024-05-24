.data
array: .word 0:20
tekst: .asciz "____....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....________....____"
N: .word 20
LOCATION: .word 33
.text
	
.global _start
_start:
	// uzmi i napuni N
	mov r7, #3
	mov r0, #0
	ldr r1, tekst_addr
	mov r2, #30
	swi #0

	ldr r5, tekst_addr
	ldr r6, =N
	ldr r7, =N

	push {lr}
	bl readint
	pop {lr}

	cmp r5, r7
	beq _start

	ldr r5, tekst_addr
	ldr r6, =array
	ldr r7, =N
	ldr r10, =N
	mov r9, #0
parse:
	push {lr}
	bl readint
	pop {lr}
	
	push {lr}
	cmp r7, r5
	beq load_buffer
	pop {lr}

	mov r5, r7
	add r5, #1
	add r6, #4
	add r9, #1
	cmp r9, r10
	blt parse

	ldr r6, =array
	ldr r7, =N
	push {lr}
	bl sort
	pop{lr}

medminmax:
	// min je r6
	ldr r0, [r6]
	// max je r6 + N - 1
	mov r8, r7
	sub r8, #1
	lsl r8, #2
	ldr r1, [r6, r8]
	lsr r8, #3
	lsl r8, #2
	ldr r2, [r6, r8]
printing:
	push {r0, r1, r2}
	ldr r0, format
	bl printf
exit:
	mov r0, #0
	mov r7, #1
	swi #0


sort:
	// sortiraj niz u r6, N u r7
	
	// for (char* j = arr + 1; j < arr + N; j++) {
	// 	char k = *j;
	// 	for (char* i = j - 1; i >= arr; i--) {
	// 		if (k >= *i) {
	// 			i = i + 1;
	// 			break;
	// 		}
	// 		*(i + 1) = *i
	// 	}
	// 	*i = k;
	// } 
	
	ldr r0, [r6]
	add r0, #4
	ldr r3, [r6]
	add r3, r7

	loop:

		ldr r2, [r0]
		mov r1, r0
		sub r1, #4  

		inner_loop:
			ldr r4, [r1]
			cmp r2, r4 
			blt end_if 
			if: add r1, #4
				b end_inner
			end_if: strb r4, [r1, #4]

			sub r1, #4
			cmp r1, r6
			bge inner_loop
		end_inner:
		strb r2, [r1]

		add r0, #4
		cmp r0, r3 
		blt loop
	end_loop:
exit_sort:
	bx lr 

readint:
	// uzmi iz [r5], stavi u [r6], procitano do stavi u r7, r8 je error reg
	mov r8, #1

	ldr r0, [r5]
	ldr r2, [r5]
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
	ldr r1, [r5]
	cmp r0, r1
	blt ponovo

	ldr r1, [r5]
	mov r7, r0 // procitano do!
	mov r2, #0
procesiraj:
	ldrb r3, [r1], #1
	
	sub r3, #48

	mov r4, r2
	lsl r4, #3
	lsl r2, #1
	add r2, r4 // mnozenje r2 sa 10

	add r2, r3 

	cmp r0, r1
	bge procesiraj
	str r2, [r6]

	bx lr



ponovo:
	mov r7, r0
	mov r8, #1
	bx lr


load_buffer:
	mov r7, #3
	mov r0, #0
	ldr r1, tekst_addr
	mov r2, #12
	swi #0
	bx lr

tekst_addr: .word tekst
loc: .word LOCATION
arr_addr: .word array
N: .word 11
stdin: .word 0
