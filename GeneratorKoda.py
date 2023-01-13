import SemantickiAnalizator

f = open("a.frisc", "w")
f.write("    MOVE 40000, R7\n    CALL F_MAIN\n    HALT\n\nF_MAIN MOVE %D 42, R6\n    RET")



f.close()
print("GOTOV")