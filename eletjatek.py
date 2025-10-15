import random
import time


class EletjatekSzimulator:

    def __init__(self, OszlopokSzama, SorokSzama) -> None:
        self.OszlopokSzama = OszlopokSzama + 2
        self.SorokSzama = SorokSzama + 2
        self.matrix = [["X" for _ in range(self.OszlopokSzama) ] for _ in range(self.SorokSzama)]
        for i in range(1, self.OszlopokSzama-1):
            for j in range(1, self.SorokSzama-1):
                self.matrix[i][j] = random.choice(["S", " "])

    def megjelenit(self):
        [print(*i) for i in self.matrix]

    def kovetkezoallapot(self):
        # ujmatrix = self.matrix[:]
        for i in range(1, self.OszlopokSzama-1):
            for j in range(1, self.SorokSzama-1):
                elem = self.matrix[i][j]
                iranyok = [(0, 1), (0,-1), (1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0)]
                melletti_s = []
                szabadhely = []
                for k in iranyok:
                    if self.matrix[i+k[0]][j+k[1]] == "S":
                         melletti_s.append((i+k[0], j+k[1]))
                    if self.matrix[i+k[0]][j+k[1]] == " ":
                        szabadhely.append((i+k[0], j+k[1]))


                 
                
                if len(melletti_s) < 2 or len(melletti_s) > 3 and elem == "S":
                    self.matrix[i][j] = " "
                if len(melletti_s) == 3 and elem == " ":
                    uj_i, uj_j = random.choice(szabadhely)
                    self.matrix[uj_i][uj_j] = "S"

        # self.matrix = ujmatrix
    
    def run(self):
        self.megjelenit()
        self.kovetkezoallapot()
                    
                    



valamii = EletjatekSzimulator(10, 10)
while True:
    if input("Üss entert: ") == "":
        valamii.run()

# 75 perc

        
    
