import GenerativnoStablo as GS
import zavrsni_klase as ZK
import pomocne_funkcije as pomocne
import ProgramskoStablo as PS
import copy

#IZRAZI
class primarni_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None
    
    def izvedi_svojstva(self):
        self.oblik = None
        if len(self.children) == 1:
            child = self.children[0]

            if isinstance(child, ZK.IDN):
                self.tip = pomocne.tip_idn(self, child.ime)
                self.lizraz = child.lizraz
                uvjet = pomocne.provjeri_idn(child)
                if not uvjet:
                    pomocne.izlaz(self)

            elif isinstance(child, ZK.BROJ):
                self.tip = 'int'
                self.lizraz = 0
                child.izvedi_svojstva()

            elif isinstance(child, ZK.ZNAK):
                #child.izvedi_svojstva()
                self.tip = 'char'
                self.lizraz = 0
            
            elif isinstance(child, ZK.NIZ_ZNAKOVA):
                child.izvedi_svojstva()
                self.tip = 'niz(const(char))'
                self.lizraz = 0
            
            else:
                pomocne.izlaz(self)     

        elif len(self.children) == 3:
            c1 = self.children[0]        
            c2 = self.children[1]        
            c3 = self.children[2]     

            if isinstance(c1, ZK.L_ZAGRADA) and isinstance(c2, izraz) and isinstance(c3, ZK.D_ZAGRADA):
                c2.izvedi_svojstva() # trebamo još vidjet što znači provjeri, pretpostavljam da to osigurava da svojstva postoje

                self.oblik = c2.oblik
                self.tip = c2.tip
                self.lizraz = c2.lizraz
            else:
                pomocne.izlaz(self)
        
        else:
            pomocne.izlaz(self)

        
class postfiks_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None
        

    def dohvati_idn2(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, primarni_izraz):

                if isinstance(c1.children[0], ZK.IDN):
                    return c1.children[0]
        
        return None

    def dohvati_idn(self):
        #print("dohvacam idn za postfiks izraz ", str(self))
        trenutni = self
        q = [self]
        while (not isinstance(trenutni, ZK.IDN)) and (len(q) > 0):
            trenutni = q.pop(0)
            for child in trenutni.children:
                q.append(child)
            #print("trenutni mi je ", trenutni)
        if not isinstance(trenutni, ZK.IDN):
            return None
        return trenutni


    def izvedi_svojstva(self):
        if len(self.children) == 1:
            child = self.children[0]

            if isinstance(child, primarni_izraz):
                child.izvedi_svojstva()
                self.tip = child.tip
                self.lizraz = child.lizraz
            else:
                pomocne.izlaz(self)
            if child.oblik == None:
                dhv = self.dohvati_idn()
                if dhv is not None:
                    #print("za cvor ", self, "dohvacen idn ", dhv.ime)
                    self.oblik = pomocne.nadi_oblik(self, dhv)
                    
                    

        elif len(self.children) == 4: 
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]

            if isinstance(c1, postfiks_izraz) and isinstance(c2, ZK.L_UGL_ZAGRADA) and isinstance(c3, izraz) and isinstance(c4, ZK.D_UGL_ZAGRADA):

                #ovo je indeksiranje, oblik tipa a[2]
                c1.izvedi_svojstva()

                if c1.oblik != 'niz':
                    pomocne.izlaz(self)

                if c1.tip.startswith('niz'): #trebamo se jos dogovorit kako tip odredit, ugl ovo mora provjeravat je li c1 dopušteni niz
                    # niz tipa niz(niz(int)) nije dopušten!
                    tip = c1.tip[4:len(c1.tip)-1]
                    self.tip = tip
                    self.oblik = 'indeksirani_niz'
                    # osiguraj samo jedan niz
                    if tip.startswith('const'):
                        self.lizraz = 0
                    else:
                        self.lizraz = 1

                    c3.izvedi_svojstva()

                    if c3.tip != 'int':
                        pomocne.izlaz(self)
            
            elif isinstance(c1, postfiks_izraz) and isinstance(c2, ZK.L_ZAGRADA) and isinstance(c3, lista_argumenata) and isinstance(c4, ZK.D_ZAGRADA):
                #ovo je za poziv funckije s argumentima!

                c1.izvedi_svojstva()
                if c1.oblik != 'funkcija':
                    dhv = c1.dohvati_idn()
                    if not pomocne.provjeri_egzistenciju(self, dhv.ime):
                        pomocne.izlaz(self)

                c3.izvedi_svojstva()

                #parametri = c1.parm_tip
                argumetni = c3.tipovi

                valjano = pomocne.provjeri_valjanost_argumenata_postfiks(c1,argumetni)

                if not valjano:         
                    pomocne.izlaz(self)

                self.tip = c1.tip
                self.oblik = 'pozvana_funkcija'
                self.lizraz = 0
            else:
                pomocne.izlaz(self)
        
        elif len(self.children) == 3:
            #poziv f-je bez argumenata
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1,postfiks_izraz) and isinstance(c2, ZK.L_ZAGRADA) and isinstance(c3, ZK.D_ZAGRADA):

                c1.izvedi_svojstva()
                if c1.oblik != 'funkcija':
                    dhv = c1.dohvati_idn()
                    if not pomocne.provjeri_egzistenciju(self, dhv.ime):
                        pomocne.izlaz(self)

                    pomocne.izlaz(self)

                self.tip = c1.tip
                self.oblik = 'pozvana_funkcija'
                uvjet = pomocne.provjeri_valjanost_argumenata_postfiks(c1, None)

                if not uvjet:
                    pomocne.izlaz(self)
            else:
                pomocne.izlaz(self)
        
        elif len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if isinstance(c1, postfiks_izraz) and (isinstance(c2,ZK.OP_INC) or isinstance(c2,ZK.OP_DEC)):
                c1.izvedi_svojstva()
                if c1.oblik == 'funkcija':
                    pomocne.izlaz(self)

                if c1.lizraz == 0 or c1.tip != 'int':
                    pomocne.izlaz(self)

                self.tip = c1.tip
                self.lizraz = 0
        
        else:
            pomocne.izlaz(self)


                    


class lista_argumenata(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tipovi = []

    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, izraz_pridruzivanja):
                c1.izvedi_svojstva()
                self.tipovi.append(c1.tip)
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, lista_argumenata) and isinstance(c2, ZK.ZAREZ) and isinstance(c3, izraz_pridruzivanja):

                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                self.tipovi = copy.deepcopy(c1.tipovi)
                self.tipovi.append(c3.tip)
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None

            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)


class unarni_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]
            if isinstance(c1,postfiks_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)
        
        elif len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if (isinstance(c1, ZK.OP_INC) or isinstance(c1, ZK.OP_DEC)) and isinstance(c2, unarni_izraz):
                c2.izvedi_svojstva()

                if c2.lizraz == 0 or c2.tip != 'int':
                    pomocne.izlaz(self) #moramo se dogovorit oko errora, najbolje da tu odma izhendlamo kraj

                self.tip = 'int' #moze i c2.tip
                self.oblik = c2.oblik
                self.lizraz = 0

            elif isinstance(c1, unarni_operator) and isinstance(c2, cast_izraz):
                c2.izvedi_svojstva()

                if c2.tip != 'int':
                    pomocne.izlaz(self)

                self.tip = 'int'
                self.oblik = c2.oblik
                self.lizraz = 0
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)


class unarni_operator(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

class cast_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None
    def nadi_postfiks(self):
        trenutni = self
        q = [self]
        while not isinstance(trenutni, postfiks_izraz):
            trenutni = q.pop(0)
            for child in trenutni.children:
                q.append(child)
        return trenutni

    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, unarni_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 4:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]

            if isinstance(c1, ZK.L_ZAGRADA) and isinstance(c2, ime_tipa) and isinstance(c3, ZK.D_ZAGRADA) and isinstance(c4, cast_izraz):
                c2.izvedi_svojstva()
                c4.izvedi_svojstva()
                idn = c4.nadi_postfiks().dohvati_idn()
                #print(self, " => ", idn)
            
                uvjet =  pomocne.provjeri_cast(c2.tip, c4.tip)
                "pomocne.varijabla_je(self, idn) and"
                if not uvjet or c4.oblik == 'niz' or c4.oblik == 'funkcija':
                    pomocne.izlaz(self)
                
                self.tip = c2.tip
                self.oblik = c4.oblik
                self.lizraz = 0
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)
            

class ime_tipa(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1,specifikator_tipa):
                c1.izvedi_svojstva()
                self.tip = c1.tip
            else:
                pomocne.izlaz(self)
        elif len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if isinstance(c1, ZK.KR_CONST) and isinstance(c2,specifikator_tipa):
                c2.izvedi_svojstva()

                if c2.tip == 'void':
                    pomocne.izlaz(self)

                self.tip = 'const(' + c2.tip + ')'
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class specifikator_tipa(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None

    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, ZK.KR_VOID):
                self.tip = 'void'
            elif isinstance(c1, ZK.KR_CHAR):
                self.tip = 'char'
            elif isinstance(c1, ZK.KR_INT):
                self.tip = 'int'
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)


class multiplikativni_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, cast_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, multiplikativni_izraz) and (isinstance(c2,ZK.OP_PUTA) or isinstance(c2,ZK.OP_DIJELI) or isinstance(c2,ZK.OP_MOD)) and isinstance(c3, cast_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c3.tip != 'int':
                    pomocne.izlaz(self)
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class aditivni_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None
    
    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, multiplikativni_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, aditivni_izraz) and (isinstance(c2,ZK.PLUS) or isinstance(c2,ZK.MINUS)) and isinstance(c3, multiplikativni_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c3.tip != 'int':
                    #pomocne.izlaz(self)
                    'pass'
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class odnosni_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, aditivni_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, odnosni_izraz) and (isinstance(c2,ZK.OP_LT) or isinstance(c2,ZK.OP_LTE) or isinstance(c2,ZK.OP_GT) or isinstance(c2,ZK.OP_GTE)) and isinstance(c3, aditivni_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c3.tip != 'int':
                    pomocne.izlaz(self)
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class jednakosni_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, odnosni_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, jednakosni_izraz) and (isinstance(c2,ZK.OP_EQ) or isinstance(c2,ZK.NEQ)) and isinstance(c3, odnosni_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c2.tip != 'int':
                    pomocne.izlaz(self)
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class bin_i_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, jednakosni_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, bin_i_izraz) and isinstance(c2, ZK.OP_BIN_I) and isinstance(c3, jednakosni_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c2.tip != 'int':
                    pomocne.izlaz(self)
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class bin_xili_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, bin_i_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, bin_xili_izraz) and isinstance(c2, ZK.OP_BIN_XILI) and isinstance(c3, bin_i_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c2.tip != 'int':
                    pomocne.izlaz(self)
                
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)

                self.tip = 'int'
                self.lizraz = 0
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class bin_ili_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None     

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, bin_xili_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, bin_ili_izraz) and isinstance(c2, ZK.OP_BIN_ILI) and isinstance(c3, bin_xili_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c2.tip != 'int':
                    pomocne.izlaz(self)
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)                                

class log_i_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, bin_ili_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, log_i_izraz) and isinstance(c2, ZK.OP_I) and isinstance(c3, bin_ili_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c2.tip != 'int':
                    pomocne.izlaz(self)
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class log_ili_izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, log_i_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, log_ili_izraz) and isinstance(c2, ZK.OP_ILI) and isinstance(c3, log_i_izraz):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != 'int' and c2.tip != 'int':
                    pomocne.izlaz(self)
                
                self.tip = 'int'
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class izraz_pridruzivanja(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None
        self.duljina = 10

    def postaje_niz_znakova(self):
        return self.tip == 'char' and self.oblik == 'niz'

    def dohvati_NIZ_ZNAKOVA(self):
        #print("dohvacam idn za postfiks izraz ", str(self))
        trenutni = self
        q = [self]
        while (not isinstance(trenutni, ZK.NIZ_ZNAKOVA)) and (len(q) > 0):
            trenutni = q.pop(0)
            for child in trenutni.children:
                q.append(child)
            #print("trenutni mi je ", trenutni)
        if not isinstance(trenutni, ZK.NIZ_ZNAKOVA):
            return None
        return trenutni

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, log_ili_izraz):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, postfiks_izraz) and isinstance(c2, ZK.OP_PRIDRUZI) and isinstance(c3, izraz_pridruzivanja):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c1.tip != c3.tip:
                    pomocne.izlaz(self)

                if c1.lizraz == 0:
                    pomocne.izlaz(self)
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)

                self.oblik = None
                self.tip = c1.tip
        
                self.lizraz = 0
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class izraz(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.lizraz = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, izraz_pridruzivanja):
                c1.izvedi_svojstva()
                self.tip = c1.tip
                self.lizraz = c1.lizraz
                self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, izraz) and isinstance(c2, ZK.ZAREZ) and isinstance(c3, izraz_pridruzivanja):
                c1.izvedi_svojstva()
                c3.izvedi_svojstva()
                
                self.tip = c3.tip
                self.lizraz = 0
                if c3.oblik == 'niz' or c3.oblik == 'funkcija' or  c1.oblik == 'niz' or c1.oblik == 'funkcija':
                    pomocne.izlaz(self)
                self.oblik = None
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

#NAREDBE
class slozena_naredba(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        self.oblik = None
        pomocne.updateaj_blok(self)
        if len(self.children) == 3:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, ZK.L_VIT_ZAGRADA) and isinstance(c2, lista_naredbi) and isinstance(c3, ZK.D_VIT_ZAGRADA):

                c2.izvedi_svojstva()
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 4:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]

            if isinstance(c1,ZK.L_VIT_ZAGRADA) and isinstance(c2,lista_deklaracija) \
                and isinstance(c3, lista_naredbi) and isinstance(c4,ZK.D_VIT_ZAGRADA):
                c2.izvedi_svojstva()
                c3.izvedi_svojstva()

            else:
                pomocne.izlaz(self)
    
        else:
            pomocne.izlaz(self)


class lista_naredbi(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        self.oblik = None
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, naredba):
                c1.izvedi_svojstva()
            else:
                pomocne.izlaz(self)
        elif len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if isinstance(c1, lista_naredbi) and isinstance(c2, naredba):
                c1.izvedi_svojstva()
                c2.izvedi_svojstva()

            else: 
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)


class naredba(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        self.oblik = None
        if len(self.children) == 1:
            c1 = self.children[0]
            if isinstance(c1, slozena_naredba):
                c1.izvedi_svojstva()

            elif isinstance(c1, izraz_naredba):
                c1.izvedi_svojstva()
                self.oblik = c1.oblik

            elif isinstance(c1, naredba_grananja):
                c1.izvedi_svojstva()
            
            elif isinstance(c1, naredba_petlje):
                c1.izvedi_svojstva()

            elif isinstance(c1, naredba_skoka):
                c1.izvedi_svojstva()

            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class izraz_naredba(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, ZK.TOCKAZAREZ):
                self.tip = 'int'
            else:
                pomocne.izlaz(self)
        elif len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if isinstance(c1, izraz) and isinstance(c2, ZK.TOCKAZAREZ):
                c1.izvedi_svojstva()
                self.oblik = c1.oblik
                self.tip = c1.tip
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class naredba_grananja(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        if len(self.children) == 5:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]
            c5 = self.children[4]

            if isinstance(c1, ZK.KR_IF) and isinstance(c2, ZK.L_ZAGRADA) and isinstance(c3, izraz) \
                and isinstance(c4, ZK.D_ZAGRADA) and isinstance(c5, naredba):

                c3.izvedi_svojstva()

                if c3.tip != 'int' or c3.oblik == 'funkcija' or c3.oblik == 'niz':
                    pomocne.izlaz(self)

                c5.izvedi_svojstva()
            
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 7:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]
            c5 = self.children[4]
            c6 = self.children[5]
            c7 = self.children[6]
            
            
           
            if isinstance(c1, ZK.KR_IF) and isinstance(c2, ZK.L_ZAGRADA) and isinstance(c3, izraz) \
                and isinstance(c4, ZK.D_ZAGRADA) and isinstance(c5, naredba) and isinstance(c6, ZK.KR_ELSE) and isinstance(c7, naredba):
                c3.izvedi_svojstva()
                #print(c3.oblik)
                #tu je greska sta main shvati ko varijablu, nema oblik
                if c3.tip != 'int' or c3.oblik == 'funkcija' or c3.oblik == 'niz':
                    pomocne.izlaz(self)

                c5.izvedi_svojstva()
                c7.izvedi_svojstva()

            else:
                pomocne.izlaz(self)

        else:
            pomocne.izlaz(self)
            




class naredba_petlje(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):

        if len(self.children) == 5:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]
            c5 = self.children[4]

            if isinstance(c1, ZK.KR_WHILE) and isinstance(c2, ZK.L_ZAGRADA) and isinstance(c3, izraz) \
                and isinstance(c4, ZK.D_ZAGRADA) and isinstance(c5, naredba):

                c3.izvedi_svojstva()

                if c3.tip != 'int' or c3.oblik == 'funkcija' or c3.oblik == 'niz':
                    pomocne.izlaz(self)

                c5.izvedi_svojstva()
            
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 6:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]
            c5 = self.children[4]
            c6 = self.children[5]

            if isinstance(c1, ZK.KR_FOR) and isinstance(c2, ZK.L_ZAGRADA) and isinstance(c3, izraz_naredba) \
               and isinstance(c4, izraz_naredba) and isinstance(c5, ZK.D_ZAGRADA) and isinstance(c6, naredba):

               c3.izvedi_svojstva()
               c4.izvedi_svojstva()

               if c4.tip != 'int' or c4.oblik == 'funkcija' or c4.oblik == 'niz' or c3.oblik == 'funkcija' or c3.oblik == 'niz':
                    pomocne.izlaz(self)

               c6.izvedi_svojstva()
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 7:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]
            c5 = self.children[4]
            c6 = self.children[5]
            c7 = self.children[6]

            if isinstance(c1, ZK.KR_FOR) and isinstance(c2, ZK.L_ZAGRADA) and isinstance(c3, izraz_naredba) \
               and isinstance(c4, izraz_naredba) and isinstance(c5, izraz) and isinstance(c6, ZK.D_ZAGRADA) and isinstance(c7, naredba):

               c3.izvedi_svojstva()
               c4.izvedi_svojstva()
               #print(c4.tip)
               #ovdje je greska sto gleda funkcije i varijable jednako
               #oblik se ne propagira do ovdje pa to treba pogledat


               if c4.tip != 'int' or c4.oblik == 'funkcija' or c4.oblik == 'niz' or c3.oblik == 'funkcija' or c3.oblik == 'niz':
                #OVO TREBA PROVJERITI JOŠ JEDNOM 
                #or c5.oblik == 'funkcija' or c5.oblik == 'niz':
                    pomocne.izlaz(self)
               
               c5.izvedi_svojstva()
               c7.izvedi_svojstva()
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)



class naredba_skoka(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        if len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if (isinstance(c1, ZK.KR_BREAK) or isinstance(c1, ZK.KR_CONTINUE)) and isinstance(c2, ZK.TOCKAZAREZ):

                uvjet = pomocne.u_petlji(self)

                if not uvjet:
                    pomocne.izlaz(self)

            elif isinstance(c1, ZK.KR_RETURN) and isinstance(c2, ZK.TOCKAZAREZ):

                uvjet = pomocne.u_void_funkciji(self)

                if not uvjet:
                    pomocne.izlaz(self)

            else:
                pomocne.izlaz(self)
        elif len(self.children) == 3:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, ZK.KR_RETURN) and isinstance(c2, izraz) and isinstance(c3, ZK.TOCKAZAREZ):
                c2.izvedi_svojstva()
                pov = pomocne.tip_funkcije(self, c2.tip) 
                #print(c2.children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].tip)

                if not pov or c2.oblik == 'funkcija' or c2.oblik == 'niz':
                    pomocne.izlaz(self)

            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class prijevodna_jedinica(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        
        if len(self.children) == 1:
            c1 = self.children[0] 

            if isinstance(c1, vanjska_deklaracija):
                c1.izvedi_svojstva()
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if isinstance(c1, prijevodna_jedinica) and isinstance(c2, vanjska_deklaracija):

                c1.izvedi_svojstva()
                c2.izvedi_svojstva()
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class vanjska_deklaracija(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)      

    def izvedi_svojstva(self):
        if len(self.children) == 1:

            c1 = self.children[0]

            if isinstance(c1, deklaracija):
                c1.izvedi_svojstva()  
            
            elif isinstance(c1, definicija_funkcije):
                c1.izvedi_svojstva()
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

#DEKLARACIJE I DEFINICIJE
class definicija_funkcije(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.ime = None
        self.tip = None
        self.parametri = []
        self.broj_parametara = 0

    #ime funkcije ce mu pridodati IDN, a tip <ime tipa>
    def izvedi_svojstva(self):
        if len(self.children) == 6:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]
            c5 = self.children[4]
            c6 = self.children[5]

            if isinstance(c1, ime_tipa) and isinstance(c2, ZK.IDN) and isinstance(c3, ZK.L_ZAGRADA) \
                and isinstance(c4, ZK.KR_VOID) and isinstance(c5, ZK.D_ZAGRADA) and isinstance(c6, slozena_naredba):

                c1.izvedi_svojstva()

                if c1.tip.startswith('const'):
                    pomocne.izlaz(self)
                
                uvjet = pomocne.provjeri_definiciju(self, c2.ime)
                
                if uvjet:
                    pomocne.izlaz(self)

                #4. provjerit postoji li deklaracije funkcije
                postoji_deklaracija = pomocne.provjeri_egzistenciju(self, c2.ime)
                if postoji_deklaracija:
                    uvjet2 = pomocne.provjeri_valjanost_argumenata(self, None) and \
                        pomocne.tip_funkcije(self, c1.tip)

                    if not uvjet2:
                        pomocne.izlaz(self)
                   
                    #zabiljezit deklaraciju
                else:
                    pomocne.dodaj_lokalnu_funkciju_void(self, c2.ime, c1.tip, True)
                
                c6.izvedi_svojstva()
                self.oblik = 'definirana_funkcija'

            elif isinstance(c1, ime_tipa) and isinstance(c2, ZK.IDN) and isinstance(c3, ZK.L_ZAGRADA) \
                and isinstance(c4, lista_parametara) and isinstance(c5, ZK.D_ZAGRADA) and isinstance(c6, slozena_naredba):

                c1.izvedi_svojstva()

                if c1.tip.startswith('const'):
                    pomocne.izlaz(self)

                uvjet = pomocne.provjeri_definiciju(self, c2.ime)

                if uvjet:
                    pomocne.izlaz(self)

                c4.izvedi_svojstva()

                postoji_deklaracija = pomocne.provjeri_egzistenciju(self, c2.ime)
                if postoji_deklaracija:
                    uvjet2 = pomocne.provjeri_valjanost_argumenata(self, c4.tipovi) and \
                        pomocne.tip_funkcije(self, c1.tip)

                else:
                    tipovi_tuplovi = list(zip(c4.tipovi, c4.imena))
                    pomocne.dodaj_lokalnu_funkciju(self, c2.ime, c1.tip, True, tipovi_tuplovi)
                    #print(tipovi_tuplovi)
                    pomocne.dodaj_argumente(c6, tipovi_tuplovi)

                c6.izvedi_svojstva()
                self.oblik = 'definirana_funkcija'

            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)




class lista_parametara(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tipovi = []
        self.imena = []

    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, deklaracija_parametra):

                c1.izvedi_svojstva()
                
                self.tipovi = [c1.tip]
                self.imena = [c1.ime]
            else:
                pomocne.izlaz(self)
        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, lista_parametara) and isinstance(c2, ZK.ZAREZ) and isinstance(c3, deklaracija_parametra):

                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                if c3.ime in c1.imena:
                    pomocne.izlaz(self)

                self.tipovi = copy.deepcopy(c1.tipovi)
                self.tipovi.append(c3.tip)
                self.imena = copy.deepcopy(c1.imena)
                self.imena.append(c3.ime)
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class deklaracija_parametra(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tip = None
        self.ime = None

    def izvedi_svojstva(self):
        if len(self.children) == 2:
            c1 = self.children[0]
            c2 = self.children[1]

            if isinstance(c1, ime_tipa) and isinstance(c2, ZK.IDN):

                c1.izvedi_svojstva()

                if c1.tip == 'void':
                    pomocne.izlaz(self)

                self.tip = c1.tip
                self.ime = c2.ime
                self.oblik = 'var'
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 4:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]

            if isinstance(c1, ime_tipa) and isinstance(c2, ZK.IDN) \
                and isinstance(c3, ZK.L_UGL_ZAGRADA) and isinstance(c4, ZK.D_UGL_ZAGRADA):

                c1.izvedi_svojstva()
                if c1.tip == 'void':
                    pomocne.izlaz(self)

                self.tip = 'niz(' + c1.tip + ')'
                self.ime = c2.ime
                self.oblik = 'niz'
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)



class lista_deklaracija(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]
            
            if isinstance(c1, deklaracija):

                c1.izvedi_svojstva()
            
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 2:

            c1 = self.children[0]
            c2 = self.children[1]

            if isinstance(c1, lista_deklaracija) and isinstance(c2, deklaracija):

                c1.izvedi_svojstva()
                c2.izvedi_svojstva()

            else:
                pomocne.izlaz(self)

        else:
            pomocne.izlaz(self)

       
class deklaracija(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)

    def izvedi_svojstva(self):

        if len(self.children) == 3:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, ime_tipa) and isinstance(c2, lista_init_deklaratora) and isinstance(c3, ZK.TOCKAZAREZ):
                
                c1.izvedi_svojstva()
                
                c2.ntip = c1.tip
                c2.izvedi_svojstva()
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)

class lista_init_deklaratora(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.ntip = None
    
    def izvedi_svojstva(self):
        if len(self.children) == 1:
            c1 = self.children[0]

            if isinstance(c1, init_deklarator):

                c1.ntip = self.ntip
                c1.izvedi_svojstva()
            else:
                pomocne.izlaz(self)

        elif len(self.children) == 3:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, lista_init_deklaratora) and isinstance (c2, ZK.ZAREZ) and isinstance(c3, init_deklarator):

                c1.ntip = self.ntip
                c1.izvedi_svojstva()

                c3.ntip = self.ntip
                c3.izvedi_svojstva()

            else:
                pomocne.izlaz(self)

        else:
            pomocne.izlaz(self)


class init_deklarator(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.ntip = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:

            c1 = self.children[0]

            if isinstance(c1, izravni_deklarator):

                c1.ntip = self.ntip
                c1.izvedi_svojstva()
                self.oblik = c1.oblik
                
                if c1.tip.startswith('const') or c1.tip.startswith('niz(const'):
                    pomocne.izlaz(self)
            else:
                pomocne.izlaz(self)
    
        elif len(self.children) == 3:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, izravni_deklarator) and isinstance(c2, ZK.OP_PRIDRUZI) and isinstance(c3, inicijalizator):

                c1.ntip = self.ntip
                c1.izvedi_svojstva()

                c3.izvedi_svojstva()

                #nemam snage za provjerit 3 jbg
                tip = c1.tip
                if tip in ['char', 'int', 'const(int)', 'const(char)']:
                    if tip.startswith('const'):
                        tip = tip[6 : len(tip) - 1]
                    
                    if c3.tip != tip and tip != 'char':
                        pomocne.izlaz(self)

                    
                    if tip == 'char' and c3.tip == 'int':
                        pomocne.izlaz(self)


                elif tip.startswith('niz'):

                    tip = tip[4 : len(tip) - 1]

                    if tip.startswith('const'):
                        tip = tip[6 : len(tip) - 1]

                    if c3.broj_elemenata > c1.broj_elemenata:
                        pomocne.izlaz(self)

                    for t in c3.tipovi:
                        if t != tip:
                            pomocne.izlaz(self)
                #print(c3.oblik)
                if c3.oblik == 'funkcija':
                    pomocne.izlaz(self)
            else:
                pomocne.izlaz(self)
        else:
            pomocne.izlaz(self)


class izravni_deklarator(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.ime = None
        self.tip = None
        self.je_funkcija = None
        self.parametri = None
        self.pov = None
        self.ntip = None
        self.broj_elemenata = None

    def izvedi_svojstva(self):
        if len(self.children) == 1:

            c1 = self.children[0]

            if isinstance(c1, ZK.IDN):

                self.tip = self.ntip
                
                if self.ntip == 'void':
                    pomocne.izlaz(self)

                uvjet = pomocne.provjeri_identifikator_lokalno(self, c1.ime)
                c1.tip = self.ntip
                if uvjet:
                    pomocne.izlaz(self)

                pomocne.dodaj_argumente(self, [(c1.tip, c1.ime)])
                self.oblik = 'var'
                #provjeri ime bla bla bla
            else:
                pomocne.izlaz(self)
            
        elif len(self.children) == 4:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]
            c4 = self.children[3]

            if isinstance(c1, ZK.IDN) and isinstance(c2, ZK.L_UGL_ZAGRADA) and \
                isinstance(c3, ZK.BROJ) and isinstance(c4, ZK.D_UGL_ZAGRADA):

                if self.ntip == 'void':
                    pomocne.izlaz(self)

                self.tip = 'niz(' + self.ntip + ')'

                uvjet = pomocne.provjeri_identifikator_lokalno(self, c1.ime)

                if uvjet:
                    pomocne.izlaz(self)
                if int(c3.vrijednost) <= 0 or int(c3.vrijednost) > 1024:
                    pomocne.izlaz(self)

                pomocne.dodaj_lokalni_niz(self, c1.ime, self.ntip, int(c3.vrijednost))
                self.oblik = 'niz'
                self.broj_elemenata = int(c3.vrijednost)

                #zabilježi deklaraciju i tip!!!!!!!!!!!!!!!!!!!!

            elif isinstance(c1, ZK.IDN) and isinstance(c2, ZK.L_ZAGRADA) and \
                isinstance(c3, ZK.KR_VOID) and isinstance(c4, ZK.D_ZAGRADA):

                uvjet = pomocne.provjeri_deklaraciju_i_tipove(self, c1.ime, self.ntip)

                if uvjet == False:
                    pomocne.izlaz(self)

                if uvjet == None:
                    pomocne.dodaj_lokalnu_funkciju_void(self, c1.ime, self.ntip, False)

                self.je_funkcija = True
                self.pov = self.ntip
                self.parametri = 'void'
                self.tip = 'funkcija'
                # postavi tip za funkciju sta vraca void
                #ovu bas ne kuzim

                
            
            elif isinstance(c1, ZK.IDN) and isinstance(c2, ZK.L_ZAGRADA) and \
                isinstance(c3, lista_parametara) and isinstance(c4, ZK.D_ZAGRADA):

                c3.izvedi_svojstva()

                uvjet = pomocne.provjeri_deklaraciju_i_tipove(self, c1.ime, self.ntip, c3.tipovi)

                if uvjet == False:
                    pomocne.izlaz(self)

                if uvjet == None:
                    tipovi_tuplovi = list(zip(c3.tipovi, c3.imena))
                    pomocne.dodaj_lokalnu_funkciju(self, c1.ime, self.ntip, False, tipovi_tuplovi)

                else:
                    pomocne.izlaz(self)

                self.je_funkcija = True
                self.pov = self.ntip
                self.parametri = c3.tipovi
                self.tip = 'funkcija'
            else:
                pomocne.izlaz(self)

class inicijalizator(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tipovi = []
        self.tip = None
        self.broj_elemenata = None

    def izvedi_svojstva(self):

        if len(self.children) == 1:

            c1 = self.children[0]

            if isinstance(c1, izraz_pridruzivanja):
                c1.izvedi_svojstva()
                if c1.postaje_niz_znakova():
                    nz = c1.dohvati_NIZ_ZNAKOVA()
                    if nz == None:
                        pomocne.izlaz(self)

                    self.broj_elemenata = len(nz.duljina)
                    self.tipovi = ['char' for _ in range(self.broj_elemenata)]
                else:

                    self.broj_elemenata = 1
                    self.tip = c1.tip
                    self.oblik = c1.oblik
            else:
                pomocne.izlaz(self)
        
        elif len(self.children) == 3:
            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, ZK.L_VIT_ZAGRADA) and isinstance(c2, lista_izraza_pridruzivanja) \
                and isinstance(c3, ZK.D_VIT_ZAGRADA):

                c2.izvedi_svojstva()
                self.broj_elemenata = c2.broj_elemenata
                self.tipovi = c2.tipovi


            else:
                pomocne.izlaz(self)

        else: 
            pomocne.izlaz(self)
class lista_izraza_pridruzivanja(GS.Cvor):
    def __init__(self, value, dubina = 0, parent = None):
        GS.Cvor.__init__(self, value, dubina, parent)
        self.tipovi = []
        self.broj_elemenata = None

    def izvedi_svojstva(self):
        if len(self.children) == 1:

            c1 = self.children[0]

            if isinstance(c1, izraz_pridruzivanja):

                c1.izvedi_svojstva()
                self.tipovi = [c1.tip]
                self.broj_elemenata = 1

            else:
                pomocne.izlaz(self)
        elif len(self.children) == 3:

            c1 = self.children[0]
            c2 = self.children[1]
            c3 = self.children[2]

            if isinstance(c1, lista_izraza_pridruzivanja) and isinstance(c2, ZK.ZAREZ) and \
                isinstance(c3, izraz_pridruzivanja):

                c1.izvedi_svojstva()
                c3.izvedi_svojstva()

                self.broj_elemenata = c1.broj_elemenata + 1
                self.tipovi = copy.deepcopy(c1.tipovi)
                self.tipovi.append(c3.tip)
            else:
                pomocne.izlaz(self)

        else:
            pomocne.izlaz(self)
