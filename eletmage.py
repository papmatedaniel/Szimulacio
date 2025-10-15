import random
import time
import os
import sys
import msvcrt  # Csak Windows alatt elérhető a billentyűzet elérhetőségének ellenőrzéséhez

class EletjatekSzimulator:
    def __init__(self, sorok_szama, oszlopok_szama):
        self.OszlopokSzama = oszlopok_szama + 2
        self.SorokSzama = sorok_szama + 2
        self.Matrix = [[0] * self.OszlopokSzama for _ in range(self.SorokSzama)]

        for sor in range(1, self.SorokSzama - 1):
            for oszlop in range(1, self.OszlopokSzama - 1):
                self.Matrix[sor][oszlop] = random.randint(0, 1)

    def Megjelenit(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # képernyő törlése
        for sor in range(self.SorokSzama):
            sor_str = ""
            for oszlop in range(self.OszlopokSzama):
                if sor == 0 or sor == self.SorokSzama - 1 or oszlop == 0 or oszlop == self.OszlopokSzama - 1:
                    sor_str += "X"
                else:
                    sor_str += "S" if self.Matrix[sor][oszlop] == 1 else " "
            print(sor_str)

    def uj_cella_ertek(self, sor, oszlop):
        sz = (
            self.Matrix[sor - 1][oszlop - 1] + self.Matrix[sor - 1][oszlop] + self.Matrix[sor - 1][oszlop + 1] +
            self.Matrix[sor][oszlop - 1] +                             self.Matrix[sor][oszlop + 1] +
            self.Matrix[sor + 1][oszlop - 1] + self.Matrix[sor + 1][oszlop] + self.Matrix[sor + 1][oszlop + 1]
        )
        letezik = self.Matrix[sor][oszlop] == 1
        tuleli = letezik and (sz == 2 or sz == 3)
        uj_szuletik = not letezik and sz == 3
        return 1 if tuleli or uj_szuletik else 0

    def KovetkezoAllapot(self):
        ujmatrix = [[0] * self.OszlopokSzama for _ in range(self.SorokSzama)]
        for sor in range(1, self.SorokSzama - 1):
            for oszlop in range(1, self.OszlopokSzama - 1):
                ujmatrix[sor][oszlop] = self.uj_cella_ertek(sor, oszlop)
        self.Matrix = ujmatrix

    def Run(self):
        self.Megjelenit()
        self.KovetkezoAllapot()
        time.sleep(0.5)


def main():
    m = EletjatekSzimulator(20, 20)
    while True:
        if msvcrt.kbhit():
            break
        m.Run()

if __name__ == "__main__":
    main()
