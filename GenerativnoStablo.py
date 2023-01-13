class Cvor:
    korijen = None
    cid = 0
    tablice = []
    cvorovi = []
    def __init__(self, value, dubina = 0, parent = None):
        self.value = value
        self.children = []
        self.parent = parent
        self.dubina = dubina
        self.nasljedna = []
        self.izvedena = []
        self.red = None
        self.znak = None
        self.oblik = None
        self.id = Cvor.cid
        Cvor.cid += 1
        Cvor.cvorovi.append(self)

    def dodaj_za_zavrsni(self, red, znak):
        self.red = red
        self.znak = znak

    def go_up(self, n):
        if self.parent == None:
            return self
        if n == 0:
            return self
        else:
            return self.parent.go_up(n-1)
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self):
        return self.dubina*" " + self.value + ' id: ' + str(self.id)  + ' oblik je ' + str(self.oblik) 

    def print_tree(self):
        print(self)
        for child in self.children:
            child.print_tree()
    
    #def provjeri(self):
        