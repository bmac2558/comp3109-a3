.text
.global simple
.type mymin, @function
.p2align 4,,15

simple:
    pushq   %rbp
    movq    %rsp, %rsp
    pushq   %rbx
#assigning memory for local variables
    movq    %rdi, %rax
    imulq   $4, %rax, %rax
    addq    $16, %rax, %rax
    imulq   $0, %rax, %rax
    subq    %rax, %rsp
    andq    $-16, %rsp
#creating space for temporaries
    movq    %rdi, %rax
    imulq   $6, %rax
    subq    %rax, %rsp
    movq    %rsi, %rax
#move %r10 to first unused temp variable
    addq    %rdi, %r10
    imulq   $4, %r10, %r10
    addq    $16, %r10
    imulq   $1, %r10, %r10
    subq    %rbp, %r10
    negq    %r10
    andq    $-16, %r10
    movq    $rdi, $rdx
    shrl    $2, %rdx
    jz      .loop_end<var>
    leaq    .const<1>, %rax
#move %r10 to first available temp
    addq    %rdi, %r10
    imulq   $4, %r10, %r10
    addq    $16, %r10
    imulq   $2, %r10, %r10
    subq    %rbp, %r10
    negq    %r10
    andq    $-16, %r10
    movq    $rdi, $rdx
    shrl    $2, %rbx
    jz      .loop_end<const>
#move %rax to local_var
    addq    %rdi, %rax
    imulq   $4, %rax, %rax
    addq    $16, %rax
    imulq   $3, %rax, %rax
    subq    %rbp, %rax
    negq    %rax
    andq    $-16, %rax
#move %r10 to first available temp
    addq    %rdi, %r10
    imulq   $4, %r10, %r10
    addq    $16, %r10
    imulq   $2, %r10, %r10
    subq    %rbp, %r10
    negq    %r10
    andq    $-16, %r10
    movq    $rdi, $rdx
    shrl    $2, %rbx
    jz      .loop_end<const>
#move %rax to last used temp
    addq    %rdi, %rax
    imulq   $4, %rax, %rax
    addq    $16, %rax
    imulq   $3, %rax, %rax
    subq    %rbp, %rax
    negq    %rax
    andq    $-16, %rax
#move %r10 to second last used temp
    addq    %rdi, %r10
    imulq   $4, %r10, %r10
    addq    $16, %r10
    imulq   $2, %r10, %r10
    subq    %rbp, %r10
    negq    %r10
    andq    $-16, %r10
    movq    %r10, %r11
    movq    %rdi, %rdx
    shrl    $2, %rbx
    jz      .loop_end<add>
#move %r10 to point to parameter
    movq    %rdi, %r10
#move %rax to last used temp vaiable
    addq    %rax, %rax
    imulq   $4, %rax, %rax
    addq    $16, %rax
    imulq   $1, %rax, %rax
    subq    %rbp, %rax
    negq    %rax
    andq    %-16, %rax
    movq    %rdi, %rdx
    shrl    $2, %rdx
    jz      .loop_end<var>
    popq    %rbx
    leave
    ret

.data
.align
.const<1>:
    .float<1>
    .float<1>
    .float<1>
    .float<1>

.loop_begin<const>:

    movaps  (%rax), %xmm0
    movaps  %xmm0, (%r10)
    addq    $16, %r10
    decq    %rbx
    jnz     .loop_begin

.loop_end<const>

.loop_begin<var>:

    movaps  (%rax), %xmm0
    movaps  %xmm0, (%r10)
    addq    $16, %rax
    addq    $16, %r10
    decq    %rbx
    jnz     .loop_begin

.loop_end<var>

.loop_begin<add>:

    movaps  (%rax), %xmm0
    movaps  (%r10), %xmm1
    addps   %xmm0, %xmm1
    movaps  %xmm1, (%r11)
    addq    $16, %rax
    addq    $16, %r10
    addq    $16, %r11
    decq    %rbx
    jnz     .loop_begin<add>

.loop_end<add>

.loop_begin<sub>:

    movaps  (%rax), %xmm0
    movaps  (%r10), %xmm1
    subps   %xmm0, %xmm1
    movaps  %xmm1, (%r11)
    addq    $16, %rax
    addq    $16, %r10
    addq    $16, %r11
    decq    %rbx
    jnz     .loop_begin<add>

.loop_end<sub>

.loop_begin<div>:

    movaps  (%rax), %xmm0
    movaps  (%r10), %xmm1
    divps   %xmm0, %xmm1
    movaps  %xmm1, (%r11)
    addq    $16, %rax
    addq    $16, %r10
    addq    $16, %r11
    decq    %rbx
    jnz     .loop_begin<add>

.loop_end<div>

.loop_begin<mul>:

    movaps  (%rax), %xmm0
    movaps  (%r10), %xmm1
    mulps   %xmm0, %xmm1
    movaps  %xmm1, (%r11)
    addq    $16, %rax
    addq    $16, %r10
    addq    $16, %r11
    decq    %rbx
    jnz     .loop_begin<add>

.loop_end<mul>

.loop_begin<min>:

    movaps  (%rax), %xmm0
    movaps  (%r10), %xmm1
    minps   %xmm0, %xmm1
    movaps  %xmm1, (%r11)
    addq    $16, %rax
    addq    $16, %r10
    addq    $16, %r11
    decq    %rbx
    jnz     .loop_begin<add>

.loop_end<min>
