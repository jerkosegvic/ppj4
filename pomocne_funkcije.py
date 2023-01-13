import GenerativnoStablo as GS
import ProgramskoStablo as PS
import zavrsni_klase as ZK
import nezavrsni_klase as NK
import deklaracije as D

def provjeri_idn(cvor):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if cvor.ime in blok_cvor.tablica_lokalnih_varijabli.keys() or \
       cvor.ime in blok_cvor.nasljedena_tablica_varijabli.keys() or \
       cvor.ime in blok_cvor.tablica_lokalnih_funkcija.keys() or \
       cvor.ime in blok_cvor.nasljedena_tablica_funkcija.keys():
        return True
    return False

def provjeri_valjanost_argumenata(cvor, argumenti):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if isinstance(cvor, NK.definicija_funkcije):
        idn = cvor.ime
        if idn != None:
            if idn in blok_cvor.tablica_lokalnih_funkcija.keys():
                dek = blok_cvor.tablica_lokalnih_funkcija[idn]
                if isinstance(dek, D.funkcija):
                    if dek.parametri == None and argumenti == None:
                        return True
                    elif dek.parametri == None or argumenti == None:
                        return False
                    if len(dek.parametri) == len(argumenti):
                        for i in range(len(dek.argumenti)):
                            if dek.parametri[i].tip != argumenti[i]:
                                return False
                        return True
                    else:
                        return False

            elif idn in blok_cvor.nasljedena_tablica_funkcija.keys():
                dek = blok_cvor.nasljedena_tablica_funkcija[idn]
                if isinstance(dek, D.funkcija):
                    if dek.parametri == None and argumenti == None:
                        return True
                    elif dek.parametri == None or argumenti == None:
                        return False
                    if len(dek.parametri) == len(argumenti):
                        for i in range(len(dek.parametri)):
                            if dek.parametri[i].tip != argumenti[i]:
                                return False
                        return True
                    else:
                        return False
    return False

def provjeri_valjanost_argumenata_postfiks(cvor, argumenti):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if isinstance(cvor, NK.postfiks_izraz):
        idn = cvor.dohvati_idn()  
        #print("idn mi je ", idn)      
        if idn != None:
            if idn.ime in blok_cvor.tablica_lokalnih_funkcija.keys():
                dek = blok_cvor.tablica_lokalnih_funkcija[idn.ime]
                #print("dek mi je ", dek, " a argumenti su ", argumenti, " a tip dek-a je ", dek.tip , " a parametri su ", dek.parametri[0].tip)
                if isinstance(dek, D.funkcija):
                    #print("zakljucio sam da ovo je funkcija")
                    if dek.parametri == None and argumenti == None:
                        return True
                    elif dek.parametri == None or argumenti == None:
                        return False
                    if len(dek.parametri) == len(argumenti):
                        #print("i tu sam doso")
                        for i in range(len(dek.parametri)):
                            if dek.parametri[i].tip != argumenti[i]:
                                return False
                        return True
                    else:
                        return False

            elif idn.ime in blok_cvor.nasljedena_tablica_funkcija.keys():
                dek = blok_cvor.nasljedena_tablica_funkcija[idn.ime]
                if isinstance(dek, D.funkcija):
                    if dek.parametri == None and argumenti == None:
                        return True
                    elif dek.parametri == None or argumenti == None:
                        return False
                    if len(dek.parametri) == len(argumenti):
                        
                        for i in range(len(dek.parametri)):
                            if dek.parametri[i].tip != argumenti[i] and argumenti[i] != 'char':
                                #print(dek.parametri[i].tip)
                                #print(argumenti[i])
                                return False
                        return True
                    else:
                        return False
    return False

def provjeri_cast(tip1, tip2):
    #print("tipovi su " + tip1 + " i " + tip2)
    if tip1.startswith('const'):
        tip1 = tip1[6 : len(tip1) - 1]
    if tip2.startswith('const'):
        tip2 = tip2[6 : len(tip2) - 1]


    if tip2 != "int" and tip2 != "char":
        return False
    if tip1 == "int" or tip1 == "char":

        return True
    return False
    

def u_petlji(cvor):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    #print("blok cvor koji provjeravam je " + str(cvor.id) + ", a tip mu je ", blok_cvor.tip)
    if blok_cvor.tip == "for" or blok_cvor.tip == "while":
        return True
    else:
        if blok_cvor.parent == None:
            return False
        else:
            return u_petlji(cvor.parent)

def u_void_funkciji(cvor):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if blok_cvor.return_tip == "void":
        return True
    else:
        if blok_cvor.parent == None:
            return False
        else:
            return u_void_funkciji(cvor.parent)

def tip_funkcije(cvor, trazeni_tip):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if blok_cvor.tip == "funkcija":
        #print(blok_cvor.return_tip)
        if blok_cvor.return_tip == trazeni_tip or blok_cvor.return_tip == 'int':
            return True
        else:
            return False
    else:
        if blok_cvor.parent == None:
            return False
        else:
            return tip_funkcije(cvor.parent, trazeni_tip)

def provjeri_egzistenciju(cvor, ime):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if ime in blok_cvor.tablica_lokalnih_funkcija.keys() or \
       ime in blok_cvor.nasljedena_tablica_funkcija.keys():
        return True
    else:
        if blok_cvor.parent == None:
            return False
        else:
            return provjeri_egzistenciju(cvor.parent, ime)

def provjeri_definiciju(cvor, ime):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if ime in blok_cvor.tablica_lokalnih_funkcija.keys():
        dek = blok_cvor.tablica_lokalnih_funkcija[ime]
        if isinstance(dek, D.funkcija):
            return dek.definirana
        else:
            return False
    elif ime in blok_cvor.nasljedena_tablica_funkcija.keys():
        dek = blok_cvor.nasljedena_tablica_funkcija[ime]
        if isinstance(dek, D.funkcija):
            return dek.definirana
        else:
            return False
    else:
        if blok_cvor.parent == None:
            return False
        else:
            return provjeri_definiciju(cvor.parent, ime)

def dodaj_lokalnu_funkciju_void(cvor, ime, tip, definirana):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    blok_cvor.dodaj_lokalnu_funkciju_void(ime, tip, definirana)

def dodaj_lokalnu_funkciju(cvor, ime, tip, definirana, parametri):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    blok_cvor.dodaj_lokalnu_funkciju(ime, tip, definirana, parametri)

def dodaj_argumente(cvor, argumenti):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    for arg in argumenti:
        if arg[0].startswith('niz'):
            #print(arg[0])
            novo = arg[0][4 : len(arg[0]) - 1]
            blok_cvor.dodaj_lokalni_niz(arg[1], novo, -1)
        else:
            blok_cvor.dodaj_lokalnu_varijablu(arg[1], arg[0])

def provjeri_identifikator_lokalno(cvor, ime):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if ime in blok_cvor.tablica_lokalnih_varijabli.keys():
        return True
    else:
        return False

def provjeri_deklaraciju_i_tipove(cvor, ime, tip, parametri = None):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if ime not in blok_cvor.tablica_lokalnih_funkcija.keys():
        return None
    
    dek = blok_cvor.tablica_lokalnih_funkcija[ime]
    if isinstance(dek, D.funkcija):
        if dek.tip == tip:
            if parametri == None and dek.parametri == None:
                return True
            elif parametri == None or dek.parametri == None:
                return False
            if len(dek.parametri) == len(parametri):
                for i in range(len(dek.parametri)):
                    if dek.parametri[i].tip != parametri[i]:
                        return False
                return True
            else:
                return False
        else:
            return False
    return False
    
def izlaz(cvor):
    out = ""
    out += cvor.value + " ::=" 
    for dijete in cvor.children:
        if dijete.red != None:
            out += " " + dijete.value + "(" + str(dijete.red) + ',' + str(dijete.znak) +")"
        else:
            out += " " + str(dijete.value) 
    print(out)
    exit(0) 

def tip_idn(cvor, ime):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    rrv = None

    if ime in blok_cvor.tablica_lokalnih_varijabli.keys():
        rrv = blok_cvor.tablica_lokalnih_varijabli[ime]
        
    elif ime in blok_cvor.tablica_lokalnih_funkcija.keys():
        rrv = blok_cvor.tablica_lokalnih_funkcija[ime]

    elif ime in blok_cvor.nasljedena_tablica_varijabli.keys():
        rrv = blok_cvor.nasljedena_tablica_varijabli[ime]

    elif ime in blok_cvor.nasljedena_tablica_funkcija.keys():
        rrv = blok_cvor.nasljedena_tablica_funkcija[ime]

    if rrv != None:
        if isinstance(rrv, D.niz):
            return "niz(" + rrv.tip + ")"
        else:
            return rrv.tip
    if blok_cvor.parent == None:
        return None
    else:
        return tip_idn(cvor.parent, ime)

def updateaj_blok(cvor):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    blok_cvor.update_tablice()

def dodaj_lokalnu_varijablu(cvor, ime, tip):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    blok_cvor.dodaj_lokalnu_varijablu(ime, tip)

def dodaj_lokalni_niz(cvor, ime, tip, duljina):
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    blok_cvor.dodaj_lokalni_niz(ime, tip, duljina)

def varijabla_je(cvor, idnn):
    if idnn == None:
        return True
    idn = idnn.ime
    id_bloka = GS.Cvor.tablice[cvor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if idn in blok_cvor.tablica_lokalnih_varijabli.keys() or idn in blok_cvor.nasljedena_tablica_varijabli.keys():
        return True
    else:
        return False

def nadi_oblik(scor, idnn):
    idn = idnn.ime
    id_bloka = GS.Cvor.tablice[scor.id]
    blok_cvor = PS.Cvor.cvorovi[id_bloka]
    if idn in blok_cvor.tablica_lokalnih_varijabli.keys():
        if isinstance(blok_cvor.tablica_lokalnih_varijabli[idn], D.varijabla):
            return 'var'
        else :
            return 'niz'
    elif idn in blok_cvor.tablica_lokalnih_funkcija.keys():
        return 'funkcija'

    elif idn in blok_cvor.nasljedena_tablica_varijabli.keys():
        if isinstance(blok_cvor.nasljedena_tablica_varijabli[idn], D.varijabla):
            return 'var'
        else :
            return 'niz'

    elif idn in blok_cvor.nasljedena_tablica_funkcija.keys():
        return 'funkcija'
    else:
        return None

def provjeri_main():
    cvor = PS.Cvor.korijen
    if 'main' not in cvor.tablica_lokalnih_funkcija.keys():
        print('main')
        exit(0)
    else:
        if cvor.tablica_lokalnih_funkcija['main'].tip != 'int':
            print('main')
            exit(0)
        if cvor.tablica_lokalnih_funkcija['main'].parametri != None:
            print('main')
            exit(0)

def provjeri_definicije():
    funkcije = {}
    cvor = PS.Cvor.korijen
    q = [cvor]
    while len(q) > 0:
        cvor = q.pop(0)
        for dijete in cvor.children:
            for i in dijete.tablica_lokalnih_funkcija.keys():
                ime = i + '(' + str(dijete.tablica_lokalnih_funkcija[i].parametri) + ')->' + dijete.tablica_lokalnih_funkcija[i].tip
                if ime in funkcije.keys():
                    if funkcije[ime] == 0 and dijete.tablica_lokalnih_funkcija[i].definirana == True:
                        funkcije[ime] = 1
                else:
                    funkcije[ime] = 0
                    if dijete.tablica_lokalnih_funkcija[i].definirana == True:
                        funkcije[ime] = 1
            q.append(dijete)

    for ime in funkcije.keys():
        if funkcije[ime] == 0:
            print('funkcija')
            exit(0)

