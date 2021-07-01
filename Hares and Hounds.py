"Am folosit python 3.7 si pycharm in caz ca aveti probleme la rulare"
"Ideea a fost ca in clasa Joc sa avem parametrii de Pozitie a iepurelui si a dulailor, iar de fiecare data cand dorim"
"Sa cream o noua stare cu o mutare efectuata, trebuie sa apelam constructorul clasei Joc."
"Acum nu mi se pare o idee atat de buna cred ca m am complicat destul de mult si aiurea"

"Cand playerul este Iepure:"
"Problema pe care o intampin este ca dupa 2 mutari ale cpu-ului nu se mai face nici o mutare"
"Alta problema ar fi ca cele 2 prime mutari sunt mereu aceleasi"
"Cand playerul este dulaul:"
"Problema este ca cpu muta iepurele doar o data si mereu pe aceeasi poz adica 7(0, 3)"
"Din ce am observat aceste prime mutari, sunt primele valide(dupa folosirea fct valid) dupa calculul pozitiei vechi +"
"Unui tuplu din lista vecinilor, dar nu imi dau seama unde ar fi problema exact"
import time


# O functie ajutatoare care afiseaza o matice cu numere
def print_joc_numbers():
    print("  0 1 2 3 4")
    print("0   1 4 7   ")
    print("   /|\|/|\   ")
    print("1 0 2 5 8 10 ")
    print("   \|/|\|/  ")
    print("2   3 6 9")


class Joc:
    """
    Clasa joc tine minte tabla de joc si pozitiile dulailor si ale iepurilor
    De fiecare data cand apelez constructorul cu alte pozitii de iepure sau dulai se modifica si matricea
    """
    NR_COLOANE = 5
    NR_LINII = 3
    SIMBOLURI_JUC = ['C', 'I']
    JMIN = None
    JMAX = None
    GOL = '*'
    # O lista de vecini pentru iepurii care nu pot merge pe diag
    neighbors_hare_no_diag = [
        (0, 1), (0, -1), (1, 0), (-1, 0)
    ]
    # O lista de vecini pentru iepuri
    neighbors_hare = [
        (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)
    ]
    # O lista de vecini pentru dulai
    neighbors_hounds = [
        (1, 1), (-1, 1), (0, 1), (1, 0), (-1, 0)
    ]
    # O lista de vecini pentru dulaii care nu pot merge pe diag
    neighbors_hounds_no_diag = [
        (0, 1), (1, 0), (-1, 0)
    ]

    # cand se apeleaza functia fara parametrii se initializeaza automat starea initiala, iar cand se schimba parametrii hounds_pos si hare_pos se schimba si matricea
    def __init__(self, tabla=None, hare_pos=(1, 4), hounds_pos=None):
        if hounds_pos is None:
            hounds_pos = [(0, 1), (1, 0), (2, 1)]
        if hare_pos is None:
            hare_pos = (1, 4)
        self.matr = tabla or [
            [(-1, ' '), (1, '*'), (4, '*'), (7, '*'), (-1, ' ')],
            [(0, '*'), (2, '*'), (5, '*'), (8, '*'), (10, '*')],
            [(-1, ' '), (3, '*'), (6, '*'), (9, '*'), (-1, ' ')]
        ]
        self.hare_pos = hare_pos
        self.hounds_pos_old = None
        self.hounds_pos = hounds_pos
        "Daca pozitia pe care este iepurasului este ocupata de * o schimbam in I"
        if self.matr[self.hare_pos[0]][self.hare_pos[1]][1] == "*":
            self.matr[self.hare_pos[0]][self.hare_pos[1]] = (self.matr[self.hare_pos[0]][self.hare_pos[1]][0], "I")
        "Pentru fiecare pozitie a dulailor o schimbam in C"
        for h_p in self.hounds_pos:
            if self.matr[h_p[0]][h_p[1]][1] == "*":
                self.matr[h_p[0]][h_p[1]] = (self.matr[h_p[0]][h_p[1]][0], "C")

    "Verificam daca a scapat iepurasul"

    def hare_escaped(self):
        """Verificam daca iepurele se alfa pe pozitia 0 a scapat implicit"""
        if self.matr[1][0][1] == 'I':
            return 'I'
        "Daca se afla in stanga cainilor pe axa y. Nu este cea mai eficienta metoda si corecta:("
        if self.hare_pos[1] < self.hounds_pos[0][1] and self.hare_pos[1] < self.hounds_pos[1][1] and self.hare_pos[1] \
                < self.hounds_pos[2][1]:
            return 'I'

        return False

    "Verificam daca castiga jocul dulaii"

    def hare_no_escape(self):
        if self.matr[1][4][1] == 'I' and self.matr[0][3][1] == 'C' and self.matr[1][3][1] == 'C' and self.matr[2][3][
            1] == 'C':
            return 'C'
        if self.matr[2][2][1] == 'I' and self.matr[1][2][1] == 'C' and self.matr[2][1][1] == 'C' and self.matr[2][3][
            1] == 'C':
            return 'C'
        if self.matr[0][2][1] == 'I' and self.matr[1][2][1] == 'C' and self.matr[0][1][1] == 'C' and self.matr[0][3][
            1] == 'C':
            return 'C'
        return False

    def final(self):
        # verificam daca a scapat iepurele
        if self.hare_escaped() == 'I':
            rez = 'I'
            if rez:
                return rez
        # Verificam daca nu a scapat
        if self.hare_no_escape() == 'C':
            rez = 'C'
            if rez:
                return rez
        else:
            return False

    "Verificam daca pozitia se mai afla in matrice"

    def valid(self, x, y):
        if 0 <= x <= self.NR_LINII - 1 and 0 <= y <= self.NR_COLOANE - 1:
            return True
        else:
            return False

    "Functia de expandeaza pentru iepuri"

    def mutari_hares(self):
        l_mutari = []
        hare_pos_old = self.hare_pos
        "Verificam daca se afla pe o pozitie care nu poate merge pe diag"
        if self.hare_pos in [(0, 2), (2, 2), (1, 1), (1, 3)]:
            "Trecem prin lista de vecini in care nu poate sa mearga pe diag"
            for neighbor_pos in self.neighbors_hare_no_diag:
                "Calculam noua pozitie pentru iepure dupa x si y"
                x_new = hare_pos_old[0] + neighbor_pos[0]
                y_new = hare_pos_old[1] + neighbor_pos[1]
                "Verificam daca nu cumva a iesit din matrice"
                if self.valid(x_new, y_new):
                    "Verificam sa nu fie cumva pe colturile nefolosite"
                    if self.matr[x_new][y_new][1] == ' ':
                        continue
                    "Verificam sa nu fie pe un caine"
                    if (x_new, y_new) in self.hounds_pos:
                        continue
                    if self.matr[x_new][y_new][1] == '*':
                        hare_pos_nou = (x_new, y_new)
                        "Creeem o noua tabla cu noua pozitie a iepurelui si ii dam append la lista de mutari si facem update la pozitii"
                        l_mutari.append(Joc(None, hare_pos_nou, self.hounds_pos))
        else:
            "Trecem prin lista de vecini"
            for neighbor_pos in self.neighbors_hare:
                "Calculam noua pozitie pentru iepure dupa x si y"
                x_new = hare_pos_old[0] + neighbor_pos[0]
                y_new = hare_pos_old[1] + neighbor_pos[1]
                "Verificam daca nu cumva a iesit din matrice"
                if self.valid(x_new, y_new):
                    "Verificam sa nu fie cumva pe colturile nefolosite"
                    if self.matr[x_new][y_new][1] == ' ':
                        continue
                    "Verificam sa nu fie pe un caine"
                    if (x_new, y_new) in self.hounds_pos:
                        continue
                    if self.matr[x_new][y_new][1] == '*':
                        hare_pos_nou = (x_new, y_new)
                        "Creeem o noua tabla cu noua pozitie a iepurelui si ii dam append la lista de mutari si facem update la pozitii"
                        l_mutari.append(Joc(None, hare_pos_nou, self.hounds_pos))
        return l_mutari

    "Functia de generare a mutarilor dulailor cu diagonale"

    def mutari_hounds(self, hound_number, hound_pos):
        l_mutari = []
        "Trecem prin vectorul vecinilor"
        for neighbor_pos in self.neighbors_hounds:
            "Calc noua poz pe care se va afla daca se face mutarea"
            x_new = hound_pos[0] + neighbor_pos[0]
            y_new = hound_pos[1] + neighbor_pos[1]
            "verificam sa nu cumva sa iasa din matrice"
            if self.valid(x_new, y_new):
                "Verificam sa nu fie pozitie nefolosibila adica sa nu fie in colturi, sa nu fie pozitie de iepure sau alt dulau"
                if self.matr[x_new][y_new][1] == ' ':
                    continue
                if (x_new, y_new) in self.hare_pos or (x_new, y_new) in self.hounds_pos:
                    continue
                if self.matr[x_new][y_new][1] == '*':
                    "Daca totul este ok, cream o tabla noua si updatam pozitiile "
                    n_hounds_pos = self.hounds_pos[:hound_number] + [(x_new, y_new)] + \
                                   self.hounds_pos[hound_number + 1:]
                    l_mutari.append(Joc(None, self.hare_pos, n_hounds_pos))

        return l_mutari

    "Functia de generare a mutarilor dulailor fara diagonale aceeasi ca cea de mai sus doar ca folosim vectorul fara diag"

    def mutari_hounds_no_diag(self, hound_number, hound_pos):
        l_mutari = []
        "Trecem prin vectorul vecinilor fara mutari pe diagonala"
        for neighbor_pos in self.neighbors_hounds_no_diag:
            "Calc noua poz si o verificam"
            x_new = hound_pos[0] + neighbor_pos[0]
            y_new = hound_pos[1] + neighbor_pos[1]
            if self.valid(x_new, y_new):
                "Verificam sa nu fie pozitie nefolosibila, sa nu fie pozitie de iepure sau alt dulau"
                if self.matr[x_new][y_new][1] == ' ':
                    continue
                if (x_new, y_new) in self.hare_pos or (x_new, y_new) in self.hounds_pos:
                    continue
                if self.matr[x_new][y_new][1] == '*':
                    "Daca totul este ok, cream o tabla noua si updatam pozitiile "
                    n_hounds_pos = self.hounds_pos[:hound_number] + [(x_new, y_new)] + self.hounds_pos[
                                                                                       hound_number + 1:]
                    l_mutari.append(Joc(None, self.hare_pos, n_hounds_pos))

        return l_mutari

    "Fuctia principala de mutari. Daca jucatorul opus este dulau trecem prin toti dulaii cu un for ii luam pozitia"
    "Daca pozitia acestuia este 2(1, 1) sau 8(1, 3) sau 4(0,2) sau 6(2, 2) apelam functia de generare a mutariilor"
    "Doar pentru miscari pe orizontala si verticala. Daca este pe orice alta pozitie apelam functia care face miscari"
    "Si pe diagonala"
    "Pentru miscarile iepurelui se face verificarea de pozitie(daca se poate misca pe diag) in functie"

    def mutari(self, jucator_opus):
        hounds_pos = self.hounds_pos
        if jucator_opus == "C":
            for hound_number in range(0, 3):
                hound_pos = hounds_pos[hound_number]
                if hound_pos in [(0, 2), (2, 2), (1, 1), (1, 3)]:
                    return self.mutari_hounds_no_diag(hound_number, hound_pos)
                else:
                    return self.mutari_hounds(hound_number, hound_pos)
        else:
            return self.mutari_hares()

    def fct_euristica(self):
        # distanta manhattan dintre pozitia fiecarui dulau si a iepurelui
        euristica = 0
        for hound_pos in self.hounds_pos:
            # calculam |poz_dulau_x - poz_iepure.x|
            euristica_x = abs(hound_pos[0] - self.hare_pos[0])
            # calculam |poz_dulau_y - poz_iepure.y|
            euristica_y = abs(hound_pos[1] - self.hare_pos[1])
            # le adunam
            euristica_sum = euristica_x + euristica_y
            # suma celor 3 dist rep euristica
            euristica += euristica_sum
        return euristica

    def fct_euristica_2(self, euristica=0):
        # distanta chebyshev dintre pozitiile dulailor si a iepurelui
        for hound_pos in self.hounds_pos:
            # calculam |poz_dulau_x - poz_iepure.x|
            euristica_x = abs(hound_pos[0] - self.hare_pos[0])
            # calculam |poz_dulau_y - poz_iepure.y|
            euristica_y = abs(hound_pos[1] - self.hare_pos[1])
            # calculam max dintre cele 2 valori
            euristica_sum = max(euristica_x, euristica_y)
            euristica += euristica_sum
        return euristica

    "O euristica de test"

    def fct_euristica_3(self):
        # o alta euristica ar putea fi numarul de mutari ale iepurelui
        mutari_iepure = self.mutari_hares()
        return len(mutari_iepure)

    "Functia de estimare a scorului este neschimbata"

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (999 + adancime)
        elif t_final == Joc.JMIN:
            return (-999 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()

    "Afisarea dupa modelul dat"

    def __str__(self):

        sir = '    '
        for col in range(self.NR_COLOANE):
            if self.matr[0][col][1] != ' ':
                sir += ("     ".join(str(self.matr[0][col][1])) + " ")
        sir += ("\n")
        sir += ("   /|\|/|\  ")
        sir += ("\n")
        sir += '  '
        for col in range(self.NR_COLOANE):
            if self.matr[1][col][1] != ' ':
                sir += (" ".join(str(self.matr[1][col][1])) + " ")
        sir += ("\n")
        sir += ("   \|/|\|/ ")
        sir += ("\n")
        sir += '    '
        for col in range(self.NR_COLOANE):
            if self.matr[2][col][1] != ' ':
                sir += ("  ".join(str(self.matr[2][col][1])) + " ")
        return sir


"99% Neschimbata"


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = []
        "Am schimbat aici deoarece imi dadea o eroare dubioasa pycharm ul"
        for mutare in l_mutari:
            stare_aux = Stare(tabla_joc=mutare, j_curent=juc_opus, adancime=self.adancime - 1, parinte=self)
            l_stari_mutari.append(stare_aux)
        return l_stari_mutari

    def __str__(self):
        # sir = str(self.tabla_joc.hounds_pos)
        sir = str(self.tabla_joc) + "\n(Juc curent: " + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """

"Neschimbata"


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor = stare.stare_aleasa.scor
    return stare


"Neschimbata"


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare


"Nu este schimbata"


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print(stare_curenta.tabla_joc.scor)
            print("Remiza!")
        else:
            print(stare_curenta.tabla_joc.scor)
            print("A castigat " + final)

        return True

    return False


"O functie care verifica daca un dulau s a mutat pe verticala"


def hound_moves_counter(y, y_old):
    if y == y_old:
        return True
    else:
        return False

"O functie care verifica daca se face mutare pe diag de pe o pozitie nepotrivita (hardcoded)"

def diag_verification(x, y, x_old, y_old):
    if x_old == 1 and y_old == 1 and x == 0 and y == 2:
        return False
    if x_old == 1 and y_old == 1 and x == 2 and y == 2:
        return False
    if x_old == 0 and y_old == 2 and x == 1 and y == 1:
        return False
    if x_old == 0 and y_old == 2 and x == 1 and y == 3:
        return False
    if x_old == 1 and y_old == 3 and x == 0 and y == 2:
        return False
    if x_old == 1 and y_old == 3 and x == 2 and y == 2:
        return False
    if x_old == 2 and y_old == 2 and x == 1 and y == 1:
        return False
    if x_old == 2 and y_old == 2 and x == 1 and y == 3:
        return False
    return True


def main():
    "Partea de validarea a inputului initial este luata din codul de Connect4/TicTacToe"
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui 1 pentru usor 3 pentru mediu 5 pentru greu: ")
        if n in ['1', '3', '5']:
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2))).upper()
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    "/Validare input initial"

    # initializare tabla
    print("Starea initiala:")

    print_joc_numbers()

    "variabile globale ca sa poate modifica si calculatorul si playerul. Nu stiu daca sunt neeaparat folositoare dar " \
    "daca a mers asa nu am mai schimbat "
    global hounds_cnt
    hounds_cnt = 0
    global new_hounds_pos
    new_hounds_pos = [(0, 1), (1, 0), (2, 1)]
    global hare_moves
    hare_moves = (1, 4)

    "Cream tabla de start"
    tabla_curenta = Joc(None, hare_moves, new_hounds_pos)

    # creeare stare initiala
    stare_curenta = Stare(tabla_curenta, 'C', Stare.ADANCIME_MAX)  # Dulaii muta primii muta primii
    print(str(stare_curenta))

    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # Muta jucatorul
            t_inainte_C = int(round(time.time() * 1000))

            raspuns_valid = False
            while not raspuns_valid:
                try:
                    if Joc.JMIN == 'C':

                        "Aici incepe partea de exit"

                        ex = input(
                            "Daca doriti sa continuati jocul apasati orice tasta si apasati ENTER. Daca doriti sa opriti jocul tastati exit si apasati tasta ENTER\n")

                        if ex == "exit":
                            print("Scorul user-ului este:")
                            print(stare_curenta.scor)
                            print("Scorul cpu-ului este:")
                            stare_curenta.j_curent = stare_curenta.jucator_opus()
                            exit()

                        "\exit"

                        "Validarea pozitiei curente a dulaului"

                        print("Selectati pozitia dulaului!")
                        moves_from_x = int(input("move hound from x:"))
                        moves_from_y = int(input("move hound from y:"))
                        moves_from = (moves_from_x, moves_from_y)
                        if moves_from not in stare_curenta.tabla_joc.hounds_pos:
                            print("Nu ati ales un dulau potrivit!\n")

                        "Aici se incheie partea de validare a pozitiei curente a dulaului"

                        hound_number = stare_curenta.tabla_joc.hounds_pos.index(moves_from)
                        print("Spuneti unde doriti sa mearga dulaul!")
                        moves_x = int(input("move hound to x:"))
                        moves_y = int(input("move hound to y:"))

                        "Validarea mutarii"

                        "Sa nu iasa din tabla de joc"
                        if not 0 <= moves_x <= 2:
                            print("Nu e o alegere buna deoarece depasiti limita jocului cu pozitia x!\n")
                            continue
                        if not 0 <= moves_y <= 4:
                            print("Nu e o alegere buna deoarece depasiti limita jocului cu pozitia y!\n")
                            continue

                        "Sa nu mutam cu mai mult de o casuta"
                        if abs(moves_from_x - moves_x) > 1:
                            print("Nu e o alegere buna deoarece se incearca mutarea cu 2 pozitii pe x!\n")
                            continue
                        if abs(moves_from_y - moves_y) > 1:
                            print("Nu e o alegere buna deoarece se incearca mutarea cu 2 pozitii pe y!\n")
                            continue
                        "Verificam mutarea pe diag"
                        if not diag_verification(moves_x, moves_y, moves_from_x, moves_from_y):
                            print("Nu puteti muta dulaul pe diagonala de pe pozitiile 2(1,1), 8(2,2), 4(0,2), 6(1,3)\n")
                            continue

                        next_position = (moves_x, moves_y)
                        if next_position == stare_curenta.tabla_joc.hare_pos:
                            print("Nu puteti muta dulaul peste un iepure!\n")
                            continue
                        if next_position in stare_curenta.tabla_joc.hounds_pos:
                            print("Nu puteti muta un dulau peste alt dulau!\n")
                            continue
                        "Aici se incheie partea de validarea a mutarii unui dulau"

                        "Testam daca dulaii se muta de 10 ori pe verticala"

                        if hound_moves_counter(moves_y, moves_from_y):
                            hounds_cnt += 1
                        else:
                            hounds_cnt = 0

                        if hounds_cnt == 10:
                            print("Dulaii se misca de 10 runde pe verticala deci Iepurasul a castigat!\n")
                            print(str(stare_curenta))
                            print("Scorul user-ului este:")
                            print(stare_curenta.scor)
                            print("Scorul cpu-ului este:")
                            stare_curenta.j_curent = stare_curenta.jucator_opus()
                            exit()

                        "/Se incheie testarea celor 10 runde"
                        print(hounds_cnt)
                        "Aici se face mutarea efectiva a dulailor modificand hounds_pos din tabla curenta si apeland din nou constructorul starii pentru a creea"
                        "O noua tabla de joc cu pozitiile dulailor schimbate"
                        if moves_from in new_hounds_pos:
                            new_hounds_pos[hound_number] = next_position
                        tabla_curenta.hounds_pos = new_hounds_pos
                        stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

                        raspuns_valid = True

                    if Joc.JMIN == 'I':
                        "exit"

                        ex = input(
                            "Daca doriti sa continuati jocul apasati orice tasta si dati ENTER. Daca doriti sa opriti jocul tastati exit si apasati tasta ENTER\n")

                        if ex == "exit":
                            print("Scorul user-ului este:")
                            print(stare_curenta.scor)
                            print("Scorul cpu-ului este:")
                            stare_curenta.j_curent = stare_curenta.jucator_opus()
                            print(stare_curenta.scor)
                            exit()

                        "\exit"

                        print("Unde doriti sa mutati iepurasul?")
                        print("Nu puteti muta iepurele pe diagonala de pe pozitiile 2, 8, 4, 6!")
                        moves_to_x = int(input("move hare to x:"))
                        moves_to_y = int(input("move hare to y:"))
                        hares_moves = (moves_to_x, moves_to_y)
                        old_pos = stare_curenta.tabla_joc.hare_pos
                        "Validari pentru mutare"

                        "Verificam sa nu putem muta iepure peste iepure"
                        if old_pos == (moves_to_x, moves_to_y):
                            print("Nu puteti muta iepurasul peste alt iepure!\n")
                            continue
                        "Verificam sa nu putem muta peste dulau"
                        if hare_moves in stare_curenta.tabla_joc.hounds_pos:
                            print("Nu puteti muta iepurele peste un dulau!\n")
                            continue
                        "Sa nu iasa din tabla de joc"
                        if not 0 <= moves_to_x <= 2:
                            print("Nu e o alegere buna deoarece depasiti limita jocului cu pozitia x!\n")
                            continue
                        if not 0 <= moves_to_y <= 4:
                            print("Nu e o alegere buna deoarece depasiti limita jocului cu pozitia y!\n")
                            continue
                        "Sa nu mutam cu mai mult de o casuta"
                        if abs(old_pos[0] - moves_to_x) > 1:
                            print("Nu e o alegere buna deoarece se incearca mutarea cu 2 pozitii pe x!\n")
                            continue
                        if abs(old_pos[1] - moves_to_y) > 1:
                            print("Nu e o alegere buna deoarece se incearca mutarea cu 2 pozitii pe y!\n")
                            continue
                        "Verificam sa nu se mute pe diag"
                        if not diag_verification(moves_to_x, moves_to_y, old_pos[0], old_pos[1]):
                            print("Nu puteti muta iepurasul pe diagonala de pe pozitiile 2, 8, 4, 6!\n")
                            continue

                        "Se incheie partea de validari pentru mutare"

                        "Aici se face mutarea efectiva modificand hare_pos din tabla curenta si apeland din nou constructorul starii pentru a creea"
                        "O noua tabla de joc cu pozitia iepurelui schimbata"
                        tabla_curenta.hare_pos = hares_moves
                        stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[1], Stare.ADANCIME_MAX)

                        raspuns_valid = True

                except ValueError:
                    print("Miscare invalida!\n")

            print_joc_numbers()
            t_dupa_C = int(round(time.time() * 1000))
            print("Jucatorul a \"gandit\" timp de " + str(t_dupa_C - t_inainte_C) + " milisecunde.")
            # testem daca e final
            if (afis_daca_final(stare_curenta)):
                print("Scorul user-ului este:")
                print(stare_curenta.scor)
                print("Scorul cpu-ului este:")
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                print(stare_curenta.scor)
                break

            stare_curenta.j_curent = stare_curenta.jucator_opus()
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            # posibila eroare
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta.tabla_joc))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if (afis_daca_final(stare_curenta)):
                print("Scorul user-ului este:")
                print(stare_curenta.scor)
                print("Scorul cpu-ului este:")
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                print(stare_curenta.scor)
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()
