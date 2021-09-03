section	.text
    global  _start	
_start:                          	 	; entry point	
	mov ecx, 1                       	; set loop counter

	loop_main:	
	push ecx                         	; save loop counter
	
	xor dx, dx                       	; reset dx
	mov ax, cx
	mov bx, 15
	div bx
	cmp dx, 0		
	jz div_by_3_5                    	; if divisible by 3 and 5
 	
	xor dx, dx                       	; reset dx
	mov ax, cx
	mov bx, 3
	div bx
	cmp dx, 0		
	jz div_by_3                      	; if divisible by 3	
	
	xor dx, dx                       	; reset dx
	mov ax, cx
	mov bx, 5
	div bx
	cmp dx, 0		
	jz div_by_5  				; if divisible by 5	
	
 	; print number
	mov eax, ecx                     	; set print_num arg
	call print_num
	jmp cont
	
	div_by_3_5:                      	; print fizz buzz
	mov eax, 4                       	; syscall number
	mov ebx, 1                       	; stdout
	mov ecx, fizzbuzz                	; ptr to buffer
	mov edx, 11                      	; buffer size
	int 0x80				
	jmp cont
	
	div_by_3:                        	; print fizz
	mov eax, 4                       	; syscall number
	mov ebx, 1  				; stdout 
	mov ecx, fizz                    	; ptr to buffer
	mov edx, 6  				; buffer size
	int 0x80				
	jmp cont
	
	div_by_5:                        	; print buzz
	mov eax, 4                       	; syscall number
	mov ebx, 1  				; stdout 
	mov ecx, buzz                    	; ptr to buffer
	mov edx, 6  				; buffer size
	int 0x80				
	jmp cont
	
	cont:
	pop ecx  				; restore loop counter
	cmp ecx, 100		
	jz exit                          	; end of loop	
	inc ecx                          	; increment loop counter
	jmp loop_main
		
	exit:
	mov eax, 1
	mov ebx, 0                       	; exit(0)
	int 0x80
	
print_num:                       		; arg eax
	push esi                         	; put counter on stack
	mov esi, 0                       	; set counter to 0
	
	loop_div:                        	; keep dividing until eax is 0
	mov edx, 0		
	mov ebx, 10
	div ebx                          	; divide eax by 10, mod in edx
	add edx, 48                      	; ascii char offset
	push edx                         	; put char on stack
	inc esi                          	; increment counter
	cmp eax, 0		
	je print_stack                   	; eax is 0, break
	jmp loop_div
	
	print_stack:                     	; print chars on stack
	cmp esi, 0		
	je done                          	; nothing left to print
	dec esi                          	; decrement counter
	mov eax, 4                       	; syscall number
	mov ebx, 1                       	; stdout
	mov edx, 1                       	; length
	mov ecx, esp                     	; syswrite arg is top of stack
	int 0x80				  
	add esp, 4                       	; update stack ptr
	jmp print_stack
	
	done: 								
 	; print new line
	mov eax, 4                       	; syscall number
	mov ebx, 1                       	; stdout 	
	mov ecx, nl                      	; ptr to buffer
	mov edx, 1                       	; buffer size
	int 0x80				 
	pop esi                          	; restore counter
	ret

section .data
	fizz dw "Fizz", 0Ah, 0Dh
	buzz dw "Buzz", 0Ah, 0Dh
	fizzbuzz dw "Fizz Buzz", 0Ah, 0Dh
	nl dw 0Ah, 0Dh                   	; new line
section .bss