import GenerativnoStablo as GS
import pomocne_funkcije as pomocne
class IDN(GS.Cvor):
    def __init__(self, value, vr, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.ime = vr
        self.tip = None
        self.lizraz = 1 #ovo još rpoc!
    
    def __str__(self):
        return self.dubina*" " + self.value + " -> " + self.ime

class BROJ(GS.Cvor):
    najmanja_vrijednost = - (2 ** 31) 
    najveca_vrijednost = 2 ** 31 - 1
    def __init__(self, value, vr, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.vrijednost = vr

    def izvedi_svojstva(self):
        for c in self.vrijednost:
            if c not in '0123456789':
                pomocne.izlaz(self.parent)
        vr = int(self.vrijednost)
        if vr < self.najmanja_vrijednost or vr > self.najveca_vrijednost:

            pomocne.izlaz(self.parent)

    def __str__(self):
        return self.dubina*" " + self.value + " -> " + str(self.vrijednost)

class ZNAK(GS.Cvor):
    def __init__(self, value, vr, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.vrijednost = vr

    def izvedi_svojstva(self):

        if len(self.vrijednost) == 2:

            drugi_znak = self.vrijednost[1]

            definirani = "tn0'\"\\"

            if drugi_znak not in definirani:
                pomocne.izlaz(self.parent)
        

    def __str__(self):
        return self.dubina*" " + self.value + " -> " + self.vrijednost

class NIZ_ZNAKOVA(GS.Cvor):
    def __init__(self, value, vr, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.vrijednost = vr
        self.tip = "niz(const(char))"
        self.duljina = len(vr)

    def izvedi_svojstva(self):
        niz = self.vrijednost
        definirani = "tn0\'\"\\"
        

        if niz[0] != '"' and niz[-1] != '"':
            pomocne.izlaz(self.parent)
        for i in range(len(niz)-1):
            if niz[i] == '\\':
                if niz[i+1] not in definirani:
                    pomocne.izlaz(self.parent)








    def __str__(self):
        return self.dubina*" " + self.value + " -> " + self.vrijednost

class KR_BREAK(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class KR_CONTINUE(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class KR_RETURN(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class KR_CHAR(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = "char"
    
    def __str__(self):
        return self.dubina*" " + self.value

class KR_CONST(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class KR_INT(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = "int"

    def __str__(self):
        return self.dubina*" " + self.value

class KR_VOID(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = "void"

    def __str__(self):
        return self.dubina*" " + self.value

class KR_IF(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = "if"

    def __str__(self):
        return self.dubina*" " + self.value

class KR_ELSE(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = "else"

    def __str__(self):
        return self.dubina*" " + self.value

class KR_WHILE(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = "while"

    def __str__(self):
        return self.dubina*" " + self.value

class KR_FOR(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = "for"

    def __str__(self):
        return self.dubina*" " + self.value

class PLUS(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_INC(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class MINUS(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_DEC(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_PUTA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_DIJELI(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_MOD(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_PRIDRUZI(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_LT(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_LTE(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_GT(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_GTE(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_EQ(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_NEQ(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_NEG(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value 

class OP_TILDA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_I(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_ILI(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_BIN_I(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_BIN_ILI(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class OP_BIN_XILI(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class ZAREZ(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class TOCKAZAREZ(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class L_ZAGRADA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class D_ZAGRADA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class L_UGL_ZAGRADA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class D_UGL_ZAGRADA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class L_VIT_ZAGRADA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

class D_VIT_ZAGRADA(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def __str__(self):
        return self.dubina*" " + self.value

