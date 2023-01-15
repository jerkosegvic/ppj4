import copy
import deklaracije as dek

class Cvor:
    korijen = None
    cid = 0
    cvorovi = []
    def __init__(self, value, nasv = {}, nasf = {}, tip = None, rt = None, dubina = 0, parent = None, dubina_bloka = 0):
        self.value = value
        self.dubina = dubina
        self.dubina_bloka = dubina_bloka
        self.parent = parent
        self.children = []
        self.tablica_lokalnih_varijabli = {}
        self.tablica_lokalnih_funkcija = {}
        self.nasljedena_tablica_varijabli = nasv
        self.nasljedena_tablica_funkcija = nasf
        self.tip = tip
        self.return_tip = rt
        self.id = Cvor.cid
        Cvor.cid += 1
        Cvor.cvorovi.append(self)

    def get_sp(self):
        min = 0
        if self.parent == None:
            return None

        for i in self.tablica_lokalnih_varijabli.keys():
            if self.tablica_lokalnih_varijabli[i].adresa < min:
                min = self.tablica_lokalnih_varijabli[i].adresa
        
        for i in self.nasljedna_tablica_varijabli.keys():
            if self.nasljedena_tablica_varijabli[i].adresa == None:
                continue
            if self.nasljedena_tablica_varijabli[i].adresa < min:
                min = self.nasljedena_tablica_varijabli[i].adresa
        
        return min

    def add_child(self, child):
        self.children.append(child)
    
    def go_up(self, n):
        if self.parent == None:
            return self
        if n == 0:
            return self
        else:
            return self.parent.go_up(n-1)
    
    def get_adresa(self, ime):
        if ime in self.tablica_lokalnih_varijabli.keys():
            return self.tablica_lokalnih_varijabli[ime].adresa
        if ime in self.nasljedena_tablica_varijabli.keys():
            return self.nasljedena_tablica_varijabli[ime].adresa
        return None

    def __str__(self):
        if self.parent == None:
            return self.dubina*" " + self.value + ", tip je " + str(self.tip) + ", vraca " + str(self.return_tip) +  ", ID: " + str(self.id) + ", parent: None"    
        return self.dubina*" " + self.value + ", tip je " + str(self.tip) + ", vraca " + str(self.return_tip) +  ", ID: " + str(self.id) + ", parent ID: " + str(self.parent.id)
    
    def print_tree(self):
        print(self)
        for child in self.children:
            child.print_tree()

    def update_tablice(self):
        if self.parent == None:
            self.nasljedena_tablica_varijabli = {}
            self.nasljedena_tablica_funkcija = {}
        else:
            nas = copy.deepcopy(self.parent.nasljedena_tablica_varijabli)
            nas.update(self.parent.tablica_lokalnih_varijabli)
            self.nasljedena_tablica_varijabli = nas 
            
            nas = copy.deepcopy(self.parent.nasljedena_tablica_funkcija)
            nas.update(self.parent.tablica_lokalnih_funkcija)
            self.nasljedena_tablica_funkcija = nas
    def dodaj_lokalnu_varijablu(self, ime, tip, value = None, ADR = None):
        if ime in self.tablica_lokalnih_varijabli.keys():
            return False
        else:
            if ADR == None:
                ADR = self.get_sp()
                if ADR != None:
                    ADR -=4
            self.tablica_lokalnih_varijabli[ime] = dek.varijabla(ime, tip, value, ADR)
            return True

    def dodaj_lokalni_niz(self, ime, tip, duljina, values = [], ADR = None):
        if ime in self.tablica_lokalnih_varijabli.keys():
            return False
        else:
            if ADR == None:
                ADR = self.get_sp()
                if ADR != None:
                    ADR -=4
            self.tablica_lokalnih_varijabli[ime] = dek.niz(ime, tip, duljina, values, ADR)
            return True

    def dodaj_lokalnu_funkciju_void(self, ime, tip, definirana):
        if ime in self.tablica_lokalnih_funkcija.keys():
            return False
        else:
            self.tablica_lokalnih_funkcija[ime] = dek.funkcija(ime, tip, definirana)
            return True

    
    def dodaj_lokalnu_funkciju(self, ime, tip, definirana, parametri_tuple):
        # parametri_tuple je lista od tupleova (ime, tip)
        if ime in self.tablica_lokalnih_funkcija.keys():
            return False
        else:
            parametri = []
            for parametar in parametri_tuple:
                np = dek.varijabla(parametar[1], parametar[0])
                parametri.append(np)
            self.tablica_lokalnih_funkcija[ime] = dek.funkcija(ime, tip, definirana, parametri)
            return True