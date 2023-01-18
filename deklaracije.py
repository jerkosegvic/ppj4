import pisac as PK
class deklaracija:
    def __init__(self, identifikator, tip):
        self.identifikator = identifikator
        self.tip = tip

    def __str__(self):
        return self.identifikator + "  tip: " + str(self.tip)

class varijabla(deklaracija):
    def __init__(self, identifikator, tip, value = None, ADR = None):
        deklaracija.__init__(self, identifikator, tip)
        self.value = value
        self.adresa = ADR
        if identifikator.startswith('1id$$n'):
            return 
        
        if ADR == None:
            #print("a ja sam retardiran i upisujem tu")
            #ADR +=4
            PK.upisi_varijablu(identifikator, value)
            PK.upisi("    POP R1")
            PK.upisi("    PUSH R1")
            PK.upisi("    STORE R1, (VAR_" + identifikator + ")")
        else:
            PK.upisi("    POP R1")
            PK.upisi("    PUSH R1")
            if ADR < 0:
                PK.upisi("    STORE R1, (R0-0" + str(format(-ADR, 'X')) + ')')
            else:
                #PK.upisi("    STORE R1, (R0+0" + str(format(ADR, 'X')) + ')')
                return 

class niz(deklaracija):
    def __init__(self, identifikator, tip, duljina, values = [], ADR = None, init = False):
        deklaracija.__init__(self, identifikator, tip)
        self.duljina = duljina
        self.values = values
        self.adresa = ADR
        if ADR == None:
            PK.upisi_niz(identifikator, duljina, values)
            PK.upisi("    MOVE VAR_" + identifikator + ", R2")
            for i in reversed(list(range(duljina))):
                PK.upisi("    POP R1")
                PK.upisi("    STORE R1, (R2+0" + str(format(i*4, 'X')) + ")")
        
        elif init:
            a = -ADR 
            for i in range(duljina):
                PK.upisi("    POP R1")
                PK.upisi("    STORE R1, (R0-0" + str(format(a, 'X')) + ")")
                a += 4

        if ADR != None:
            ADR -= (self.duljina - 1) * 4
            self.adresa = ADR
    def zadnja_adresa(self):
        return self.adresa + (self.duljina - 1) * 4

class funkcija(deklaracija):
    def __init__(self, identifikator, tip, definirana, parametri = None):
        deklaracija.__init__(self, identifikator, tip)
        self.parametri = parametri
        self.definirana = definirana

class pointer(deklaracija):
    def __init__(self, identifikator, pointer, ADR = None, tip = None):
        deklaracija.__init__(self, identifikator, None)
        self.pointer = pointer
        self.adresa = ADR
        self.tip = tip
        if ADR == None:
            PK.upisi_varijablu(identifikator, None)
