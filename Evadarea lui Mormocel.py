""""Structura este aceeasi ca la laborator"""
"Evadarea lui Mormocel"

import copy
import math
import time

"Clasa frunza o folosesc pentru a stoca datele citite din fisier stochez id - ul coordonatele numarul de insecte si greutatea"


class Frunza:
    def __init__(self, ident_frunza, x, y, nr_insecte, greutate, greutate_broasca=0):
        self.ident_frunza = ident_frunza
        self.x = x
        self.y = y
        self.nr_insecte = nr_insecte
        self.greutate = greutate
        self.greutate_broasca = greutate_broasca

    def __str__(self):
        return "(id_frunza: {}, x: {}, y:{}, insecte: {}, greutate: {}, greutate_broasca: {})" \
            .format(self.ident_frunza, self.x, self.y, self.nr_insecte, self.greutate, self.greutate_broasca)

    def __repr__(self):
        return f"(id={self.ident_frunza}, x={self.x}, y={self.y}, nr_insecte={self.nr_insecte}, greutate={self.greutate}, greutate_broasca={self.greutate_broasca}) "



def distanta_puncte(x1, y1, x2, y2):
    #Aceasta este distanta euclidiana dintre 2 puncte. Este admisibila
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    #Aceasta este distanta Chebysev. Tot admisibila
    #return max((x1 - x2), (y1 - y2))
    #Aceasta este distanta euclidiana dintre 2 puncte inmultita cu o constanta. Nu este admisibila
    #return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)*123
        #euclidiana 
"Functia returneaza distanta de la un punct la cercul care formeaza lacul"


def distanta_mal(x1, y1):
    return raza - distanta_puncte(0, 0, x1, y1)


class Nod:
    "in info retin obiecte de tip frunza"

    def __init__(self, info):
        self.info = info
        self.h = distanta_mal(self.info.x, self.info.y)

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Problema:
    "In clasa problema creez noduri cu frunzele citite si caut nodul de start"

    def __init__(self, frunze, raza, greutatea_initiala, nod_start):
        self.raza = raza
        self.greutatea_initiala = greutatea_initiala
        self.nod_start = nod_start
        self.noduri = [0] * len(frunze)
        for i in range(len(frunze)):
            self.noduri[i] = Nod(frunze[i])
        self.nod_start = self.cauta_nod_nume(nod_start)

    "Cautam dupa ident_frunza"

    def cauta_nod_nume(self, info):
        """Stiind doar informatia "info" a unui nod,
		trebuie sa returnati fie obiectul de tip Nod care are acea informatie,
		fie None, daca nu exista niciun nod cu acea informatie."""
        ### TO DO ... DONE
        for nod in self.noduri:
            if nod.info.ident_frunza == info:
                return nod
        return None


""" Sfarsit definire problema """

""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
		Cuprinde o referinta catre nodul in sine (din graf)
		dar are ca proprietati si valorile specifice algoritmului A* (f si g).
		Se presupune ca h este proprietate a nodului din graf

	"""

    problema = None  # atribut al clasei

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf  # obiect de tip Nod
        self.parinte = parinte  # obiect de tip Nod
        self.g = g  # costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        """
			Functie care calculeaza drumul asociat unui nod din arborele de cautare.
			Functia merge din parinte in parinte pana ajunge la radacina
		"""
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        """
			Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
			Verificarea se face mergand din parinte in parinte pana la radacina
			Se compara doar informatiile nodurilor (proprietatea info)
			Returnati True sau False.

			"nod" este obiect de tip Nod (are atributul "nod.info")
			"self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
		"""
        ### TO DO ... DONE
        nod_c = self
        while nod_c.parinte is not None:
            if nod.info.ident_frunza == nod_c.nod_graf.info.ident_frunza:
                return True
            nod_c = nod_c.parinte
        return False

    "Un prim tip de expandeaza imi da diferit si nu am stiut pe care sa aleg"

    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
		si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
		sau lista vida, daca nu exista niciunul.
		(Fiecare tuplu contine un obiect de tip Nod si un numar.)
		"""

        l_succesori = []

        frunza_curenta = self.nod_graf
        "Trecem prin fiecare frunza"
        for frunza in problema.noduri:
            "Verificam daca este vorba de aceasi frunza"
            if frunza_curenta.info.ident_frunza == frunza.info.ident_frunza:
                continue
            "Generam toate posibilitatiile de insecte"
            for insecte_consumate in range(0, frunza.info.nr_insecte + 1):
                "Verificam daca este posibila saritura si daca mormocel poate sta pe frunza"
                if distanta_puncte(frunza_curenta.info.x, frunza_curenta.info.y, frunza.info.x,
                                   frunza.info.y) <= frunza.info.greutate / 3:
                    if frunza_curenta.info.greutate_broasca <= frunza.info.greutate:
                        "Calculam greutatea noua adaugand la greutatea broscutei numarul de insecte consumat(generat mai devreme) si scazand 1 pentru costul sariturii"
                        greutate_noua = frunza.info.greutate_broasca + insecte_consumate - 1
                        "Daca broscuta ajunge la greutate = 0 moare si nu vrem asta :)"
                        if greutate_noua != 0:
                            "Creem un nod nou si ii dam append la lista de succesori"
                            frunza_noua = copy.deepcopy(frunza)
                            frunza_noua.info.nr_insecte -= insecte_consumate
                            frunza_noua.info.greutate_broasca = greutate_noua
                            l_succesori.append((frunza_noua,
                                                distanta_puncte(frunza_curenta.info.x, frunza_curenta.info.y,
                                                                frunza.info.x, frunza.info.y)))
        "Returnam lista de copii"
        return l_succesori


    # se modifica in functie de problema
    def test_scop(self):
        "Verificam daca se poate face saritura "
        return distanta_mal(self.nod_graf.info.x, self.nod_graf.info.y) <= self.nod_graf.info.greutate_broasca / 3

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
    sir = "["
    for x in l:
        sir += str(x) + " \n"
    sir += "]"
    return sir


def in_lista(l, nod):
    """
		lista "l" contine obiecte de tip NodParcurgere
		"nod" este de tip Nod
	"""
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None


def a_star():
    """
    Functia care implementeaza algoritmul A-star
    """
    ### TO DO ... DONE

    afisari_nr = 1
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere
    while len(open) > 0:
        nod_curent = open.pop(0)  # scoatem primul element din lista open
        # fout.write(f"({})")
        closed.append(nod_curent)  # si il adaugam la finalul listei closed

        # testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
        if nod_curent.test_scop():
            break

        # print("Succesorii nodului: ", nod_curent)

        l_succesori = nod_curent.expandeaza()  # contine tupluri de tip (Nod, numar)
        for (nod_succesor, cost_succesor) in l_succesori:
            # "nod_curent" este tatal, "nod_succesor" este fiul curent

            # daca fiul nu e in drumul dintre radacina si tatal sau (adica nu se creeaza un circuit)
            if not nod_curent.contine_in_drum(nod_succesor):
                # print("Succesor: ")
                # print(nod_succesor)
                # print("Cost succesor: ", cost_succesor)
                # print()
                # calculez valorile g si f pentru "nod_succesor" (fiul)
                g_succesor = nod_curent.g + cost_succesor  # g-ul tatalui + cost muchie(tata, fiu)
                f_succesor = g_succesor + nod_succesor.h  # g-ul fiului + h-ul fiului

                # verific daca "nod_succesor" se afla in closed
                # (si il si sterg, returnand nodul sters in nod_parcg_vechi
                nod_parcg_vechi = in_lista(closed, nod_succesor)

                if nod_parcg_vechi is not None:  # "nod_succesor" e in closed
                    # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                    # 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista closed)
                    # atunci actualizez parintele, g si f
                    # si apoi voi adauga "nod_nou" in lista open
                    if f_succesor < nod_parcg_vechi.f:
                        closed.remove(nod_parcg_vechi)  # scot nodul din lista closed
                        nod_parcg_vechi.parinte = nod_curent  # actualizez parintele
                        nod_parcg_vechi.g = g_succesor  # actualizez g
                        nod_parcg_vechi.f = f_succesor  # actualizez f
                        nod_nou = nod_parcg_vechi  # setez "nod_nou", care va fi adaugat apoi in open

                else:
                    # daca nu e in closed, verific daca "nod_succesor" se afla in open
                    nod_parcg_vechi = in_lista(open, nod_succesor)

                    if nod_parcg_vechi is not None:  # "nod_succesor" e in open
                        # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                        # 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista open)
                        # atunci scot nodul din lista open
                        # 		(pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
                        # actualizez parintele, g si f
                        # si apoi voi adauga "nod_nou" in lista open (la noua pozitie corecta in sortare)
                        if f_succesor < nod_parcg_vechi.f:
                            open.remove(nod_parcg_vechi)
                            nod_parcg_vechi.parinte = nod_curent
                            nod_parcg_vechi.g = g_succesor
                            nod_parcg_vechi.f = f_succesor
                            nod_nou = nod_parcg_vechi

                    else:  # cand "nod_succesor" nu e nici in closed, nici in open
                        nod_nou = NodParcurgere(nod_graf=nod_succesor, parinte=nod_curent, g=g_succesor)
                    # se calculeaza f automat in constructor

                if nod_nou:
                    # inserare in lista sortata crescator dupa f
                    # (si pentru f-uri egale descrescator dupa g)
                    i = 0
                    while i < len(open):
                        if open[i].f < nod_nou.f:
                            i += 1
                        else:
                            while i < len(open) and open[i].f == nod_nou.f and open[i].g > nod_nou.g:
                                i += 1
                            break

                    open.insert(i, nod_nou)
    "Calculam timpul de rulare"
    timp = int(round(time.time() * 1000))
    print("" + str(timp - timp_start) + " milisecunda/milisecunde!")
    "Daca in lista open nu exista elemente nu s au realizat sarituri"
    if len(open) == 0:
        fout.write("Din pacate, broscuta nu are scapare!")
    else:
        "Afisam frunza radacina"
        fout.write(
            f"{afisari_nr})Broscuta se afla pe frunza initiala: {rad_arbore.nod_graf.info.ident_frunza}({rad_arbore.nod_graf.info.x})({rad_arbore.nod_graf.info.y}). Greutate broscuta: {rad_arbore.nod_graf.info.greutate_broasca}\n")
        afisari_nr += 1
        "Calculam drumul"
        drum = nod_curent.drum_arbore()
        for nod in drum:
            if nod != rad_arbore:
                "Cautam frunza de pe care s a sarit pentru a calcula insectele mancate"
                nod_anterior = Problema.cauta_nod_nume(problema, nod.nod_graf.info.ident_frunza)
                fout.write(
                    f"{afisari_nr})Broscuta a sarit de la {nod.parinte.nod_graf.info.ident_frunza}({nod.parinte.nod_graf.info.x}),({nod.parinte.nod_graf.info.y}) la {nod.nod_graf.info.ident_frunza}({nod.nod_graf.info.x})({nod.nod_graf.info.y}).")
                fout.write(
                    f"Broscuta a mancat {nod_anterior.info.nr_insecte - nod.nod_graf.info.nr_insecte} insecte. Greutate broscuta:{nod.nod_graf.info.greutate_broasca}\n")
                afisari_nr += 1
        fout.write(f"{afisari_nr})Broscuta a ajuns la mal in {afisari_nr - 2} sarituri.")


timp_start = 0
if __name__ == "__main__":

    lista_fisiere_input = ["233_Predescu_Eduard_Lab6_Pb7_input_1.in", "233_Predescu_Eduard_Lab6_Pb7_input_2.in", "233_Predescu_Eduard_Lab6_Pb7_input_3.in", "233_Predescu_Eduard_Lab6_Pb7_input_4.in"]
    lista_fisiere_output = ["233_Predescu_Eduard_Lab6_Pb7_output_1.out", "233_Predescu_Eduard_Lab6_Pb7_output_2.out", "233_Predescu_Eduard_Lab6_Pb7_output_3.out", "233_Predescu_Eduard_Lab6_Pb7_output_4.out"]
    for i in range(0, 4):
        fin = open(lista_fisiere_input[i], "r")
        fout = open(lista_fisiere_output[i], "w")
        raza = float(fin.readline())
        greutate_initiala = float(fin.readline())
        nod_start = fin.readline().strip()
        frunze = []
        for lines in fin:
            id_frunza, x, y, nr_insecte, greutate_max = lines.split()
            frunze.append(
                Frunza(id_frunza, float(x), float(y), int(nr_insecte), float(greutate_max), int(greutate_initiala)))
        timp_start = int(round(time.time() * 1000))
        problema = Problema(frunze, raza, greutate_initiala, nod_start)
        NodParcurgere.problema = problema
        a_star()
        print("Pentru " + str(lista_fisiere_input[i]) + " timpul de rulare a fost:")
