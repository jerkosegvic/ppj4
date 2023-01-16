import pisac

operatori = '''
F_MOD LOAD R6, (R7+4) ; DESNI
    LOAD R5, (R7+8) ; LIJEVI
    MOVE 0, R4
    CMP R6, R4
    JP_SLE OUT_F_MOD
    CMP R5, R4
    JP_SLT OUT_F_MOD
MOD_F_MOD PUSH R5
    PUSH R6
    CALL F_DIV
    POP R4
    POP R4
    LOAD R6, (R7+4)
    PUSH R6
    PUSH R4
    CALL F_MUL
    POP R4
    POP R4
    LOAD R5, (R7+8)
    SUB R5, R4, R4
    STORE R4, (R7+8)
OUT_F_MOD RET
    
F_DIV LOAD R6, (R7+4) ;DJELITELJ
    MOVE 0, R3 ; R3 GLEDA PREDZNAK
    MOVE 0, R4
    CMP R6, R4; R6 - 0
    JP_EQ ZERO_F_DIV
    JP_SGE L1_F_DIV ; AKO JE R6 POZITIVAN UCITAJ DJELJENIK
    PUSH R6
    CALL F_NEG
    POP R6
    MOVE 1, R4
    ADD R3, R4, R3
    
L1_F_DIV LOAD R5, (R7+8) ;DJELJENIK
    MOVE 0, R4
    CMP R5, R4; R5 - 0
    JP_SGE DIV_F_DIV
    PUSH R5
    CALL F_NEG
    POP R5
    MOVE -1, R4
    ADD R3, R4, R3

DIV_F_DIV MOVE 0, R4
    MOVE 1, R2
LOOP_F_DIV CMP R5, R6
    JP_SLT OUT_F_DIV
    SUB R5, R6, R5
    ADD R2, R4, R4
    JP LOOP_F_DIV

OUT_F_DIV STORE R4, (R7+8)
    MOVE 0, R2
    CMP R3, R2 ; R3 - R2
    JP_EQ EXIT_F_DIV
    PUSH R4 
    CALL F_NEG
    POP R4
    STORE R4, (R7+8)
EXIT_F_DIV RET

ZERO_F_DIV MOVE 0, R3
    STORE R3, (R7+8)
    RET
    
    
F_NEG LOAD R1, (R7+4)
    MOVE -1, R2
    XOR R1, R2, R1
    MOVE 1, R2
    ADD R1, R2, R1
    STORE R1, (R7+4)
    RET
    
F_MUL LOAD R2, (R7+4)
    LOAD R1, (R7+8)
    MOVE 0 ,R3
    CMP R2, R3
    MOVE 0, R6
    JP_SLT NEG1_F_MUL
P1_F_MUL MOVE R1, R3 ;R3 IMA OP1
    MOVE R2, R4 ;R4 IMA OP2
    MOVE 0, R2 ;R2 IMA 0 <- SLUZI KAO AKUMULATOR
    MOVE 0, R1; R1 IMA 0 <- USPOREDBA
    
LOOP_F_MUL CMP R4, R1
    JP_EQ IZLAZ_F_MUL
    ADD R3, R2, R2
    MOVE -1, R5
    ADD R5, R4, R4
    JP LOOP_F_MUL
    
NEG1_F_MUL MOVE -1, R3
    XOR R2, R3, R2
    MOVE 1, R3
    ADD R3, R2, R2
    MOVE 1, R6
    JP P1_F_MUL
IZLAZ_F_MUL
    MOVE 0, R3
    CMP R6, R3
    JP_EQ OUT_F_MUL
    MOVE -1, R3
    XOR R2, R3, R2
    MOVE 1, R3
    ADD R3, R2, R2
OUT_F_MUL STORE R2, (R7+8)
    RET
    
F_INC LOAD R6, (R7+4)
    MOVE 1, R5
    ADD R6, R5, R6
    STORE R6, (R7+4)
    RET
    
F_DEC LOAD R6, (R7+4)
    MOVE 1, R5
    SUB R6, R5, R6
    STORE R6, (R7+4)
    RET'''


def upisi_operatore():
  global operatori 
  pisac.upisi(operatori)