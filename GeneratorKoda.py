import pisac as PK

pocetak = "    MOVE 40000, R7\n    CALL F_MAIN\n    HALT\n"
PK.upisi(pocetak)

import SemantickiAnalizator
PK.zavrsi()
print("GOTOV")