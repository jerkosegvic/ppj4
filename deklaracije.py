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
    def __init__(self, identifikator, tip, duljina, values = [], ADR = None):
        deklaracija.__init__(self, identifikator, tip)
        self.duljina = duljina
        self.values = values
        self.adresa = ADR
        if ADR == None:
            PK.upisi_niz(identifikator, duljina, values)

    def zadnja_adresa(self):
        return self.adresa + (self.duljina - 1) * 4

class funkcija(deklaracija):
    def __init__(self, identifikator, tip, definirana, parametri = None):
        deklaracija.__init__(self, identifikator, tip)
        self.parametri = parametri
        self.definirana = definirana
        