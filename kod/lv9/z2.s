// shellsort nad nizom charova unsen preko stdin

	.data
tekst: .asciz "_._._._._._._._._._._._._._."
N: .word 28
stdin: .word 0x0
.text
	
.global _start
_start:
	// unesi N u niz
	mov r7, #3
	mov r0, #0
	mov r1, =tekst
	mov r2, #N 
	swi #0

	// sortiraj
	
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
	
	mov r0, =tekst
	add r0, #1
	mov r3, =tekst
	add r3, #N

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
			cmp r1, =tekst
			bge inner_loop
		end_inner:
		strb r2, [r1]

		add r0, #1
		cmp r0, r3 
		blt loop
	end_loop:

	// ispisi niz
	mov r7, #4
	mov r1, =tekst
	mov r0, #1
	mov r2, #N
	swi #0


exit:
	mov r0, #0
	mov r7, #1
	swi
