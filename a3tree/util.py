"""
By default, assignments will take %rax to hold the address of the
destination vector, %r10 the address of the source or first operand vector,
and %r11 the sencond operand vector, if applicable.

"""
MOVQ_RAX = """
    movq    %rax, {dst}
"""
MOVQ_RAX_R10 = MOVQ_RAX.format(dst='%r10')
MOVQ_RAX_R11 = MOVQ_RAX.format(dst='%r11')

ASSIGN = """
    # copy vector from {from_} to {to}
    movq    %rdi, %rbx      # load vector length into counter %rbx
    shrq    $2, %rbx        # divide counter reg by 4
                            # (per loop iteration 4 floats)
    jz      .loop_end_assig_{idx} # check whether number is equal to zero

    .loop_begin_assig_{idx}:

        movaps  ({from_}), %xmm0   # load source into %xmm0
        movaps  %xmm0, ({to})   # store %xmm0
{from_incr}
        addq    $16, {to}       # increment destination pointer by (4 x float)

        decq    %rbx            # decrement counter
        jnz     .loop_begin_assig_{idx} # jump to loop header if counter is not zero

    .loop_end_assig_{idx}:
"""

ASSIGN_OP = """
    # perform ({op1}) {operation} ({op2}) and store result at ({to})
    movq    %rdi, %rbx      # load vector length into counter %rbx
    shrq    $2, %rbx        # divide counter reg by 4
                            # (per loop iteration 4 floats)
    jz      .loop_end_assig_{idx} # check whether number is equal to zero

    .loop_begin_assig_{idx}:

        movaps  ({op2}), %xmm0   # load first operand into %xmm0
        movaps  ({op1}), %xmm1   # load second operand into %xmm1

        # perform operation
        {operation}   %xmm0, %xmm1

        movaps  %xmm1, ({to})   # store result

        # increment pointers (by 4 x float)
{op1_incr}{op2_incr}
        addq    $16, {to}

        decq    %rbx            # decrement counter
        jnz     .loop_begin_assig_{idx} # jump to loop header if counter is not zero

    .loop_end_assig_{idx}:

"""

CTR_INCR = """
        addq    $16, {ctr}       # increment source pointer by (4 x float)
"""

OPERATOR_INSTRUCTION = {
        '+': 'addps',
        '-': 'subps',
        '*': 'mulps',
        '/': 'divps',
        'MIN': 'minps',
        }

# beware: horrible, horrible module global variable
curr_idx = 0

def assign(from_='%r10', to='%rax', from_const=False):
    """Copy the vector pointed to by `from_` to the one pointed to by `to`."""

    from_incr = '' if from_const else CTR_INCR.format(ctr=from_)

    global curr_idx
    curr_idx += 1

    return ASSIGN.format(
            idx=curr_idx,
            from_=from_,
            to=to,
            from_incr=from_incr)


def assign_op(operation, operand1='%r10', operand2='%r11', to='%rax',
        operand1_const=False, operand2_const=False):
    """
    Perform the named or symbolic `operation` upon the vectors pointed to by
    the registers `operand1` and `operand2`, storing the result in the vector
    pointed to by `to`.
    
    i.e. assign_op('/', x, y) => (%rax) = (x) / (y)

    """
    operation = OPERATOR_INSTRUCTION.get(operation, operation)
    op1_incr = '' if operand1_const else CTR_INCR.format(ctr=operand1)
    op2_incr = '' if operand2_const else CTR_INCR.format(ctr=operand2)

    global curr_idx
    curr_idx += 1

    # this will be "oprps %<op2> %<op1>" , which means (OPR op1 op2)
    return ASSIGN_OP.format(
            idx=curr_idx,
            operation=operation,
            op1=operand1,
            op2=operand2,
            to=to,
            op1_incr=op1_incr,
            op2_incr=op2_incr)
