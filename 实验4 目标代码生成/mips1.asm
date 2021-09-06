li $k1,1
li $a0,0
li $a1,1
li $a2,2
li $a3,3
loop1:
slt $a0,$s3,$zero
slt $a1,$zero,$s3
nor $t0,$a0,$a1
loop2:
beq $t0,$zero,loop5
loop3:
add $t1,$s1,$s2
loop4:
add $s4,$t1,$zero
loop5:
slt $a0,$s3,$k1
slt $a1,$k1,$s3
nor $t2,$a0,$a1
loop6:
beq $t2,$zero,loop9
loop7:
sub $t3,$s1,$s2
loop8:
add $s4,$t3,$zero
loop9:
slt $a0,$s3,$a2
slt $a1,$a2,$s3
nor $t4,$a0,$a1
loop10:
beq $t4,$zero,loop13
loop11:
and $t5,$s2,$s1
loop12:
add $s4,$t5,$zero
loop13:
slt $a0,$s3,$a3
slt $a1,$a3,$s3
nor $t6,$a0,$a1
loop14:
beq $t6,$zero,loop17
loop15:
or $t7,$s2,$s1
loop16:
add $s4,$t7,$zero
loop17:
syscall