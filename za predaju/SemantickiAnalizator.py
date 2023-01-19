import sys
import GenerativnoStablo as GS
import nezavrsni_klase as NK
import ProgramskoStablo as PS
import pomocne_funkcije as pomocne
import zavrsni_klase as ZK
import copy

ulaz = sys.stdin.read()
lines = ulaz.split('\n')
if lines[len(lines) - 1] == '':
    lines.pop()
#print(lines)

trenutni_blok = PS.Cvor("Globalni blok")
PS.Cvor.korijen = trenutni_blok
trenutni = None
dubina = 0
dubina_bloka = 0

def novi_cvor(fullvalue, dubina = 0, parent = None):
    novi = None
    value_list = fullvalue.split(' ')
    value = value_list[0]
    if True:
        if value == "<primarni_izraz>":
            novi = NK.primarni_izraz(value, dubina, parent)
        elif value == "<postfiks_izraz>":
            novi = NK.postfiks_izraz(value, dubina, parent)
        elif value == "<lista_argumenata>":
            novi = NK.lista_argumenata(value, dubina, parent)
        elif value == "<unarni_izraz>":
            novi = NK.unarni_izraz(value, dubina, parent)
        elif value == "<unarni_operator>":
            novi = NK.unarni_operator(value, dubina, parent)
        elif value == "<cast_izraz>":
            novi = NK.cast_izraz(value, dubina, parent)
        elif value == "<ime_tipa>":
            novi = NK.ime_tipa(value, dubina, parent)
        elif value == "<specifikator_tipa>":
            novi = NK.specifikator_tipa(value, dubina, parent)
        elif value == "<multiplikativni_izraz>":
            novi = NK.multiplikativni_izraz(value, dubina, parent)
        elif value == "<aditivni_izraz>":
            novi = NK.aditivni_izraz(value, dubina, parent)
        elif value == "<odnosni_izraz>":
            novi = NK.odnosni_izraz(value, dubina, parent)
        elif value == "<jednakosni_izraz>":
            novi = NK.jednakosni_izraz(value, dubina, parent)
        elif value == "<bin_i_izraz>":
            novi = NK.bin_i_izraz(value, dubina, parent)
        elif value == "<bin_xili_izraz>":
            novi = NK.bin_xili_izraz(value, dubina, parent)
        elif value == "<bin_ili_izraz>":
            novi = NK.bin_ili_izraz(value, dubina, parent)
        elif value == "<log_i_izraz>":
            novi = NK.log_i_izraz(value, dubina, parent)
        elif value == "<log_ili_izraz>":
            novi = NK.log_ili_izraz(value, dubina, parent)
        elif value == "<izraz_pridruzivanja>":
            novi = NK.izraz_pridruzivanja(value, dubina, parent)
        elif value == "<izraz>":
            novi = NK.izraz(value, dubina, parent)
        elif value == "<slozena_naredba>":
            global trenutni_blok
            global dubina_bloka
            novi = NK.slozena_naredba(value, dubina, parent)
            inst = None
            rv = None
            if isinstance(parent, NK.definicija_funkcije):
                inst = "funkcija"
                rv = parent.children[0].children[-1].children[0].tip
            
            elif isinstance(parent.parent , NK.naredba_grananja):
                if len(parent.parent.children) == 5:
                    inst = "if"
                else:
                    inst = "else"

            elif isinstance(parent.parent , NK.naredba_petlje):
                inst = parent.parent.children[0].tip
            
            #nas = copy.deepcopy(trenutni_blok.nasljedena_tablica)
            #nas.update(trenutni_blok.tablica_lokalnih)
            pnovi = PS.Cvor(value, {}, {}, inst, rv, trenutni_blok.dubina + 1, trenutni_blok, dubina)
            trenutni_blok.add_child(pnovi)
            trenutni_blok = pnovi
            dubina_bloka = dubina
            #print(dubina_bloka)
            #print("mijenjam neki kurac1")
            #print(trenutni)
            #print(trenutni_blok)
        elif value == "<lista_naredbi>":
            novi = NK.lista_naredbi(value, dubina, parent)
        elif value == "<naredba>":
            novi = NK.naredba(value, dubina, parent)
        elif value == "<izraz_naredba>":
            novi = NK.izraz_naredba(value, dubina, parent)
        elif value == "<naredba_grananja>":
            novi = NK.naredba_grananja(value, dubina, parent)
        elif value == "<naredba_petlje>":
            novi = NK.naredba_petlje(value, dubina, parent)
        elif value == "<naredba_skoka>":
            novi = NK.naredba_skoka(value, dubina, parent)
        elif value == "<prijevodna_jedinica>":
            novi = NK.prijevodna_jedinica(value, dubina, parent)
        elif value == "<vanjska_deklaracija>":
            novi = NK.vanjska_deklaracija(value, dubina, parent)
        elif value == "<definicija_funkcije>":
            novi = NK.definicija_funkcije(value, dubina, parent)
        elif value == "<lista_parametara>":
            novi = NK.lista_parametara(value, dubina, parent)
        elif value == "<deklaracija_parametra>":
            novi = NK.deklaracija_parametra(value, dubina, parent)
        elif value == "<lista_deklaracija>":
            novi = NK.lista_deklaracija(value, dubina, parent)
        elif value == "<deklaracija>":
            novi = NK.deklaracija(value, dubina, parent)
        elif value == "<lista_init_deklaratora>":
            novi = NK.lista_init_deklaratora(value, dubina, parent)
        elif value == "<init_deklarator>":
            novi = NK.init_deklarator(value, dubina, parent)
        elif value == "<izravni_deklarator>":
            novi = NK.izravni_deklarator(value, dubina, parent)
        elif value == "<inicijalizator>":
            novi = NK.inicijalizator(value, dubina, parent)
        elif value == "<lista_izraza_pridruzivanja>":
            novi = NK.lista_izraza_pridruzivanja(value, dubina, parent)
        elif value == "IDN":
            novi = ZK.IDN(value, value_list[2], dubina, parent)
        elif value == "BROJ":
            novi = ZK.BROJ(value, value_list[2], dubina, parent)
        elif value == "ZNAK":
            novi = ZK.ZNAK(value, value_list[2], dubina, parent)
        elif value == "NIZ_ZNAKOVA":
            novi = ZK.NIZ_ZNAKOVA(value, value_list[2], dubina, parent)
        elif value == "KR_BREAK":
            novi = ZK.KR_BREAK(value, dubina, parent)
        elif value == "KR_CONTINUE":
            novi = ZK.KR_CONTINUE(value, dubina, parent)
        elif value == "KR_RETURN":
            novi = ZK.KR_RETURN(value, dubina, parent)
        elif value == "KR_IF":
            novi = ZK.KR_IF(value, dubina, parent)
        elif value == "KR_ELSE":
            novi = ZK.KR_ELSE(value, dubina, parent)
        elif value == "KR_WHILE":
            novi = ZK.KR_WHILE(value, dubina, parent)
        elif value == "KR_FOR":
            novi = ZK.KR_FOR(value, dubina, parent)
        elif value == "KR_DO":
            novi = ZK.KR_DO(value, dubina, parent)
        elif value == "KR_INT":
            novi = ZK.KR_INT(value, dubina, parent)
        elif value == "KR_CHAR":
            novi = ZK.KR_CHAR(value, dubina, parent)
        elif value == "KR_VOID":
            novi = ZK.KR_VOID(value, dubina, parent)
        #define elif value ==s for all classes from zavrsni_klase.py
        elif value == "KR_CONST":
            novi = ZK.KR_CONST(value, dubina, parent)
        elif value == "PLUS":
            novi = ZK.PLUS(value, dubina, parent)
        elif value == "MINUS":
            novi = ZK.MINUS(value, dubina, parent)
        elif value == "OP_INC":
            novi = ZK.OP_INC(value, dubina, parent)
        elif value == "OP_DEC":
            novi = ZK.OP_DEC(value, dubina, parent)
        elif value == "OP_PUTA":
            novi = ZK.OP_PUTA(value, dubina, parent)
        elif value == "OP_DIJELI":
            novi = ZK.OP_DIJELI(value, dubina, parent)
        elif value == "OP_MOD":
            novi = ZK.OP_MOD(value, dubina, parent)
        elif value == "OP_NEG":
            novi = ZK.OP_NEG(value, dubina, parent)
        elif value == "OP_TILDA":
            novi = ZK.OP_TILDA(value, dubina, parent)
        elif value == "OP_PRIDRUZI":
            novi = ZK.OP_PRIDRUZI(value, dubina, parent)
        elif value == "OP_LT":
            novi = ZK.OP_LT(value, dubina, parent)
        elif value == "OP_GT":
            novi = ZK.OP_GT(value, dubina, parent)
        elif value == "OP_LTE":
            novi = ZK.OP_LTE(value, dubina, parent)
        elif value == "OP_GTE":
            novi = ZK.OP_GTE(value, dubina, parent)
        elif value == "OP_EQ":
            novi = ZK.OP_EQ(value, dubina, parent)
        elif value == "OP_NEQ":
            novi = ZK.OP_NEQ(value, dubina, parent)
        elif value == "OP_I":
            novi = ZK.OP_I(value, dubina, parent)
        elif value == "OP_ILI":
            novi = ZK.OP_ILI(value, dubina, parent)
        elif value == "OP_BIN_I":
            novi = ZK.OP_BIN_I(value, dubina, parent)
        elif value == "OP_BIN_ILI":
            novi = ZK.OP_BIN_ILI(value, dubina, parent)
        elif value == "OP_BIN_XILI":
            novi = ZK.OP_BIN_XILI(value, dubina, parent)
        elif value == "ZAREZ":
            novi = ZK.ZAREZ(value, dubina, parent)
        elif value == "TOCKAZAREZ":
            novi = ZK.TOCKAZAREZ(value, dubina, parent)
        elif value == "L_ZAGRADA":
            novi = ZK.L_ZAGRADA(value, dubina, parent)
        elif value == "D_ZAGRADA":
            novi = ZK.D_ZAGRADA(value, dubina, parent)
        elif value == "L_VIT_ZAGRADA":
            novi = ZK.L_VIT_ZAGRADA(value, dubina, parent)
        elif value == "D_VIT_ZAGRADA":
            novi = ZK.D_VIT_ZAGRADA(value, dubina, parent)
        elif value == "L_UGL_ZAGRADA":
            novi = ZK.L_UGL_ZAGRADA(value, dubina, parent)
        elif value == "D_UGL_ZAGRADA":
            novi = ZK.D_UGL_ZAGRADA(value, dubina, parent)
#        elif value == _ :
#            novi = GS.Cvor(value, dubina, parent)
    if len(value_list) == 3:
        novi.dodaj_za_zavrsni(value_list[1], value_list[2])
    GS.Cvor.tablice.append(trenutni_blok.id)
    #print(novi)  

    return novi

for line in lines:
    bez_spaceova = line.lstrip()
    num_leading_spaces = len(line) - len(bez_spaceova)
    #print(bez_spaceova)
    if trenutni == None:
        #print("bez spaceova: " , end = " -> ")
        #print(bez_spaceova)
        trenutni = novi_cvor(bez_spaceova, dubina)
        GS.Cvor.korijen = trenutni
        dubina = num_leading_spaces
        #print(trenutni)
        continue

    if num_leading_spaces > dubina:
        dubina = num_leading_spaces
        novi = novi_cvor(bez_spaceova, dubina, trenutni)
        trenutni.add_child(novi)
        trenutni = novi
        

    elif num_leading_spaces < dubina:
        trenutni = trenutni.go_up(dubina - num_leading_spaces )
        dubina = num_leading_spaces
        if dubina < dubina_bloka:
            trenutni_blok = trenutni_blok.go_up(1)
            dubina_bloka = trenutni_blok.dubina_bloka
            #print("mijenjam neki kurac2")
            #print(trenutni)
            #print(trenutni_blok)
        novi = novi_cvor(bez_spaceova, dubina, trenutni.parent)
        trenutni.parent.add_child(novi)  
        trenutni = novi
        

    else:
        novi = novi_cvor(bez_spaceova, dubina, trenutni.parent)
        trenutni.parent.add_child(novi)
        trenutni = novi

    #print(trenutni)
    

#PS.Cvor.korijen.print_tree()
#GS.Cvor.korijen.print_tree()
GS.Cvor.korijen.izvedi_svojstva()
#pomocne.provjeri_main()
#pomocne.provjeri_definicije()

