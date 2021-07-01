#Predescu Eduard_Alexandru grupa 233 connect4

import time


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 7
    NR_LINII = 6
    NR_CONNECT = 4  # cu cate simboluri adiacente se castiga
    SIMBOLURI_JUC = ['X', '0']  # ['G', 'R'] sau ['X', '0']
    JMIN = None  # 'R'
    JMAX = None  # 'G'
    GOL = '.'

    def __init__(self, tabla=None):
        self.matr = tabla or [Joc.GOL] * (Joc.NR_COLOANE * Joc.NR_LINII)

    def final(self):
        # returnam simbolul jucatorului castigator daca are 4 piese adiacente
        # pe linie, coloana, diagonala \ sau diagonala /
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat jocul
        rez = False

        # verificam linii

        for i in range(self.NR_COLOANE):
            for j in range(self.NR_LINII - 3):
                if self.matr[j * self.NR_COLOANE + i] == self.matr[(j + 1) * self.NR_COLOANE + i] and \
                        self.matr[(j + 1) * self.NR_COLOANE + i] == self.matr[(j + 2) * self.NR_COLOANE + i] and \
                        self.matr[(j + 2) * self.NR_COLOANE + i] == self.matr[(j + 3) * self.NR_COLOANE + i] and \
                        self.matr[j * self.NR_COLOANE + i] != self.GOL:
                    rez = self.matr[j * self.NR_COLOANE + i]
            if rez:
                return rez

        # verificam coloane

        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE - 3):
                if self.matr[i * self.NR_COLOANE + j] == self.matr[i * self.NR_COLOANE + j + 1] and \
                        self.matr[i * self.NR_COLOANE + j + 1] == self.matr[i * self.NR_COLOANE + j + 2] and \
                        self.matr[i * self.NR_COLOANE + j + 2] == self.matr[i * self.NR_COLOANE + j + 3] and \
                        self.matr[i * self.NR_COLOANE + j] != self.GOL:
                    rez = self.matr[i * self.NR_COLOANE + j]

            if rez:
                return rez

        # verificam diagonale \
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                if self.matr[i * self.NR_COLOANE + j] == self.matr[(i + 1) * self.NR_COLOANE + (j + 1)] and \
                        self.matr[(i + 1) * self.NR_COLOANE + (j + 1)] == self.matr[
                    (i + 2) * self.NR_COLOANE + (j + 2)] and \
                        self.matr[(i + 2) * self.NR_COLOANE + (j + 2)] == self.matr[
                    (i + 3) * self.NR_COLOANE + (j + 3)] and \
                        self.matr[i * self.NR_COLOANE + j] != self.GOL:
                    rez = self.matr[i * self.NR_COLOANE + j]

            if rez:
                return rez

        # verificam diagonale /
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                if self.matr[i * self.NR_COLOANE + (j + self.NR_COLOANE - 1)] == self.matr[
                    (i + 1) * self.NR_COLOANE + (j + self.NR_COLOANE - 1 - 1)] and \
                        self.matr[(i + 1) * self.NR_COLOANE + (j + self.NR_COLOANE - 1 - 1)] == self.matr[
                    (i + 2) * self.NR_COLOANE + (j + self.NR_COLOANE - 2 - 1)] and \
                        self.matr[(i + 2) * self.NR_COLOANE + (j + self.NR_COLOANE - 2 - 1)] == self.matr[
                    (i + 3) * self.NR_COLOANE + (j + self.NR_COLOANE - 3 - 1)] and \
                        self.matr[i * self.NR_COLOANE + (j + self.NR_COLOANE - 1)] != self.GOL:
                    rez = self.matr[i * self.NR_COLOANE + (j + self.NR_COLOANE - 1)]

                if rez:
                    return rez

        if rez == False and Joc.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def mutari(self, jucator_opus):
        l_mutari = []

        for coloana in range(self.NR_COLOANE):
            if self.matr[coloana] != self.GOL:
                continue
            matr_noua = list(self.matr)

            for linie_adaugare in range(self.NR_LINII - 1, -1, -1):
                if matr_noua[linie_adaugare * self.NR_COLOANE + coloana] == self.GOL:
                    break
            matr_noua[linie_adaugare * self.NR_COLOANE + coloana] = jucator_opus

            l_mutari.append(Joc(matr_noua))

        return l_mutari

    def nr_intervale_deschise(self, jucator):
        # un interval de 4 pozitii adiacente (pe linie, coloana, diag \ sau diag /)
        # este deschis pt "jucator" daca nu contine "juc_opus"

        juc_opus = Joc.JMIN if jucator == Joc.JMAX else Joc.JMAX
        rez = 0

        # linii
        for i in range(self.NR_COLOANE):
            for j in range(self.NR_LINII - 3):
                if self.matr[j * self.NR_COLOANE + i] != juc_opus and \
                        self.matr[j * self.NR_COLOANE + i] == jucator and \
                        self.matr[(j + 1) * self.NR_COLOANE + i] != juc_opus and \
                        self.matr[(j + 2) * self.NR_COLOANE + i] != juc_opus and \
                        self.matr[(j + 3) * self.NR_COLOANE + i] != juc_opus:
                    rez += 1

        # coloane
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE - 3):
                if self.matr[i * self.NR_COLOANE + j] != juc_opus and \
                        self.matr[i * self.NR_COLOANE + j] == jucator and \
                        self.matr[i * self.NR_COLOANE + j + 1] != juc_opus and \
                        self.matr[i * self.NR_COLOANE + j + 2] != juc_opus and \
                        self.matr[i * self.NR_COLOANE + j + 3] != juc_opus:
                    rez += 1

        # diagonale \
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                if self.matr[i * self.NR_COLOANE + j] != juc_opus and \
                        self.matr[i * self.NR_COLOANE + j] == jucator and \
                        self.matr[(i + 1) * self.NR_COLOANE + (j + 1)] != juc_opus and \
                        self.matr[(i + 2) * self.NR_COLOANE + (j + 2)] != juc_opus and \
                        self.matr[(i + 3) * self.NR_COLOANE + (j + 3)] != juc_opus:
                    rez += 1
        # diagonale /
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                if self.matr[i * self.NR_COLOANE + (j + self.NR_COLOANE - 1)] != juc_opus and \
                        self.matr[i * self.NR_COLOANE + (j + self.NR_COLOANE - 1)] == jucator and \
                        self.matr[(i + 1) * self.NR_COLOANE + (j + self.NR_COLOANE - 1 - 1)] != juc_opus and \
                        self.matr[(i + 2) * self.NR_COLOANE + (j + self.NR_COLOANE - 2 - 1)] != juc_opus and \
                        self.matr[(i + 3) * self.NR_COLOANE + (j + self.NR_COLOANE - 3 - 1)] != juc_opus:
                    rez += 1

        return rez

    def fct_euristica(self):

        return self.nr_intervale_deschise(Joc.JMAX) - self.nr_intervale_deschise(Joc.JMIN)
        # o alata eruistica ar putea fi self.NR_CONNECT - cate piese are deja pe o linie/coloana/diagonala

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return 999 + adancime
        elif t_final == Joc.JMIN:
            return -999 - adancime
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()

    def __str__(self):
        sir = ''
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + ' '
        sir += '\n'

        for lin in range(self.NR_LINII):
            k = lin * self.NR_COLOANE
            sir += (" ".join([str(x) for x in self.matr[k: k + self.NR_COLOANE]]) + "\n")
        return sir


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
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent: " + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


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


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
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
        n = input("Adancime maxima a arborelui: ")
        if n.isdigit():
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

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)
    print(stare_curenta)
    linie = -1
    coloana = -1
    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    coloana = int(input("coloana = "))

                    if 0 <= coloana < Joc.NR_COLOANE:
                        if stare_curenta.tabla_joc.matr[coloana] != Joc.GOL:
                            print("Toata coloana este ocupata.")
                        else:
                            for linie in range(Joc.NR_LINII - 1, -1, -1):
                                if stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] == Joc.GOL:
                                    break
                            raspuns_valid = True

                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            # dupa iesirea din while sigur am valida coloana
            # deci pot plasa simbolul pe "tabla de joc"
            pozitie = linie * Joc.NR_COLOANE + coloana
            stare_curenta.tabla_joc.matr[pozitie] = Joc.JMIN

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta.tabla_joc))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()
