import SemantickiAnalizator

pocetak = "    MOVE 40000, R7\n    CALL F_MAIN\n    HALT\n"
funkcije = "\nF_MAIN MOVE %D 0, R6\n    RET\n"
globalne_varijable = "\n"


f = open("a.frisc", "w")
f.write(pocetak)
f.write(funkcije)
f.write(globalne_varijable)
f.close()
print("GOTOV")