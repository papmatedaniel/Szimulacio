"""Ez a kód egy szavanna szimulációt valósít meg"""

import random
import os


class Allat:
    """Állat osztály"""

    def __init__(self, faj: str, pozicio: tuple[int, int], maxeletkor: int, szaporodasiido: int) -> None:
        self.faj = faj  # Állat faja: növényevő/húsevő(ragadozó)
        self.eletkor = 0  # Állat életkora
        self.maxeletkor = maxeletkor  # Állat maximális életkora
        self.pozicio = pozicio  # Állat pozíciója((x,y) koordináta)
        self.ehsegszint = (
            0  # Állat éhségszintje, húsevőnél évente növeljük, ha eszik 0-ra állítjuk
        )
        self.szaporodott_az_evben = False  # Ha szaporodott az évben True ellenben False
        self.szaporodasiido = szaporodasiido  # Növényevő - 2, Ragadozó - 3


class Szimulacio:
    """Állatok mozgásának szimulációja"""

    def __init__(self) -> None:
        self.szavanna = [["." for _ in range(20)] for _ in range(20)]  # 20x20 mátrix
        self.jatekev = 0  # Aktuális játkév
        self.allatok = set()  # Állat objektumok(életkor, faj, kor) tárolása
        self.novenyevok_cellaja = set()  # Növényevők (x,y) koordinátája
        self.ragadozok_cellaja = set()  # Ragadozók (x,y) koordinátája
        self.ujszulott_allatok = set()  # Külön tároljuk az újszülött állatobjektumokat
        self.novenyevo_ujszulottek_cellaja = (
            set()
        )  # Újszülött növényevők (x,y) koordinátája
        self.ragadozo_ujszulottek_cellaja = (
            set()
        )  # Újszülött ragadozók (x,y) koordinátája
        self.szabadcellak = set()  # Üres cellák koordinátája(x,y)

    def cellak_frissitese(self) -> None:
        """Frissíti a ragadozók, növényevők, újszülöttek celláját, +szabadcellakat"""
        self.novenyevok_cellaja = {
            i.pozicio for i in self.allatok if i.faj == "novenyevo"
        }
        self.ragadozok_cellaja = {i.pozicio for i in self.allatok if i.faj == "husevo"}
        self.novenyevo_ujszulottek_cellaja = {
            i.pozicio for i in self.ujszulott_allatok if i.faj == "novenyevo"
        }
        self.ragadozo_ujszulottek_cellaja = {
            i.pozicio for i in self.ujszulott_allatok if i.faj == "husevo"
        }

        osszes_elfoglalt_cella = (
            self.ragadozok_cellaja
            | self.novenyevok_cellaja
            | self.novenyevo_ujszulottek_cellaja
            | self.ragadozo_ujszulottek_cellaja
        )
        palya_osszes_cellaja = {(x, y) for x in range(20) for y in range(20)}
        szabadcellak = palya_osszes_cellaja - osszes_elfoglalt_cella
        self.szabadcellak = szabadcellak

    def allatgeneralo(self, faj: str, pozicio: tuple[int, int]) -> None:
        """Legenerálja az adott állatot, és belerakja az újszülött_allatok-ba"""
        ragadozo_eletkor = random.randint(9, 12)  # Ragadozó maxéletkora 9-12 év
        novenyevo_eletkor = random.randint(11, 14)  # Növényevő maxéletkora 11-14 év
        if faj == "novenyevo":  # Ha az állat növényevő
            szaporodasiido = 2  # Akkor 2 évente szaporodhat
            maxeletkor = novenyevo_eletkor
        else:
            szaporodasiido = 3  # Ha ragadozó, akkor 3 évente szaporodhat
            maxeletkor = ragadozo_eletkor

        self.ujszulott_allatok.add(
            Allat(faj, pozicio, maxeletkor, szaporodasiido)
        )  # Újszülött létrehozása

    def szavanna_frissito(self) -> None:
        """Minden év végén frissítjük, és kinyomtatjuk a szavannát"""
        self.szavanna = [
            ["." for _ in range(20)] for _ in range(20)
        ]  # Friss üres 20x20-as szavanna
        for allat in self.allatok:
            x, y = allat.pozicio
            if allat.faj == "novenyevo":  # Ha az állat növényevő
                self.szavanna[y][x] = (
                    "\033[32mN\033[0m"  # Akkor a játéktérben N-el jelöljük a helyét
                )
            else:
                self.szavanna[y][x] = (
                    "\033[31mR\033[0m"  # Ha pedig ragadozó, akkor R-el jelöljük
                )

    def kezdeti_allatok_generalasa(self) -> None:
        """Legeneráljuk a 0 év állatait."""
        allat_szamlalo = 0
        while allat_szamlalo != 180:  # Ez 180 állat generálásáig megy
            veletlen_pozicio = (
                random.randint(0, 19),
                random.randint(0, 19),
            )  # Véletlen koordináta a 20x20 mátrixban
            if veletlen_pozicio in self.szabadcellak:
                veletlen_allat = random.randint(1, 100)
                if (
                    veletlen_allat < 65
                ):  # 65% esély arra, hogy az állat növényevő legyen
                    veletlen_ev = random.randint(11, 14)
                    faj = "novenyevo"
                    szaporodasiido = 2
                else:  # 35%esély pedig arra, hogy húsevő
                    veletlen_ev = random.randint(9, 12)
                    szaporodasiido = 3
                    faj = "husevo"
                self.allatok.add(
                    Allat(faj, veletlen_pozicio, veletlen_ev, szaporodasiido)
                )  # Az állatokat hozzáadjuk
                allat_szamlalo += 1  # Növeljük a hozzáadott állatok számát

    def jatekev_novelo(self) -> None:
        """Minden évben megnöveli 1-el a játékévet"""
        self.jatekev += 1

    def ujszulott_allatok_kezelese(self) -> None:
        """Az újszülötteketet kezeli"""
        self.allatok.update(
            self.ujszulott_allatok
        )  # Az újszülötteket hozzáadjuk az állatokhoz.
        self.ujszulott_allatok = set()  # Az újszülötteket pedig kiürítjük

    def eletkornovelo(self) -> None:
        """Növeli az állatok életkorát"""
        for allat in self.allatok:
            allat.eletkor += 1

    def ehsegnovelo(self) -> None:
        """Növeli a ragadozók éhség szintjét."""
        for allat in self.allatok:
            if allat.faj == "husevo":
                allat.ehsegszint += 1

    def meghal(self) -> None:
        """Ha az állat elérte a maximális életkorát,
        akkor meghal, vagy ragadozónál az éhségszint eléri a 2-t"""
        meghalt = set()
        for allat in self.allatok:
            if allat.eletkor + 1 >= allat.maxeletkor or allat.ehsegszint >= 3:
                meghalt.add(allat)
        self.allatok = self.allatok - meghalt

    def egysugarukor(self, pozicio: tuple[int, int]) -> set:
        """Kiszámolja a pályán belül xy pozíció mellett
        lévő cellákat, és visszadja annak listáját"""
        iranyok = {
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, -1),
            (-1, 1),
        }  # Irányok
        egysugaru_szabadkord = set()
        x1, y1 = pozicio
        for x2, y2 in iranyok:
            uj_pozicio = (x1 + x2, y1 + y2)
            if 0 <= uj_pozicio[0] <= 19 and 0 <= uj_pozicio[1] <= 19:
                egysugaru_szabadkord.add(uj_pozicio)
        return egysugaru_szabadkord

    def allatmozgato(self, pozicio: tuple[int, int]) -> tuple:
        """Az állat mellett visszaad egy szabad helyet, ha van,
        ellenkező esetben a saját koordinátáját adja vissza."""
        szabadhelyek = self.egysugarukor(pozicio) & self.szabadcellak
        if szabadhelyek:
            return random.choice(list(szabadhelyek))
        return pozicio

    def szaporodas(self, allat: Allat) -> bool:
        """Megpróbál új utódot létrehozni, visszatér azzal, hogy sikerült-e"""
        allatpozicio = allat.pozicio
        faj = allat.faj
        szaporodasiido = allat.szaporodasiido
        if faj == "novenyevo":
            fajcellaja = self.novenyevok_cellaja
        else:
            fajcellaja = self.ragadozok_cellaja

        if self.egysugarukor(allatpozicio) & fajcellaja:
            for masik_allat in self.allatok:
                if (
                    masik_allat.faj == faj
                    and masik_allat.eletkor % szaporodasiido == 0
                    and masik_allat.ehsegszint == 0
                    and allatpozicio != masik_allat.pozicio
                    and masik_allat.pozicio in self.egysugarukor(allatpozicio)
                ):
                    utod_lehetseges_helye = self.szabadcellak & (
                        self.egysugarukor(allatpozicio)
                        | self.egysugarukor(masik_allat.pozicio)
                        - {allatpozicio}
                        - {masik_allat.pozicio}
                    )
                    if utod_lehetseges_helye:
                        masik_allat.szaporodott_az_evben = True
                        allat.szaporodott_az_evben = True
                        ujutodpozicio = random.choice(list(utod_lehetseges_helye))
                        # print(allatpozicio, masik_allat.pozicioja, ujutodpozicio)
                        self.allatgeneralo(masik_allat.faj, ujutodpozicio)
                        return True
        return False

    def novenyevo_mozgas(self, allatpozicio: tuple[int, int], allatobjektum: Allat) -> None:
        """Átmozgatja a növényevőket szabad helyre, ha van."""
        self.szavanna[allatpozicio[1]][allatpozicio[0]] = "."
        allatobjektum.pozicio = self.allatmozgato(allatpozicio)
        self.szavanna[allatpozicio[1]][allatpozicio[0]] = "N"

    def husevo_mozgas(self, allatpozicio: tuple[int, int], allatobjektum: Allat) -> None:
        """A húsevő mellett lévő egyik növényevőt fefalja
        A meghalt állatot kiveszi a set-ből
        Ha nincs növényevő, a közelében, akkor egy random koordinátára
        lép ha van üres hely mellette.."""
        novenyevok = set()
        if self.egysugarukor(allatpozicio) & self.novenyevok_cellaja:
            novenyevok.update(self.allatok)
        if self.egysugarukor(allatpozicio) & self.novenyevo_ujszulottek_cellaja:
            novenyevok.update(self.ujszulott_allatok)
        eltavolitando = set()
        for preda in novenyevok:
            if preda.faj == "novenyevo" and preda.pozicio in self.egysugarukor(
                allatpozicio
            ):
                allatobjektum.ehsegszint = 0
                allatobjektum.pozicio = preda.pozicio
                eltavolitando.add(preda)
                break
        else:
            allatobjektum.pozicio = self.allatmozgato(allatpozicio)
        self.allatok = self.allatok - eltavolitando
        self.ujszulott_allatok = self.ujszulott_allatok - eltavolitando

    def fuggvenyhivasok(self) -> None:
        """Meghívjuk a függvényeket minden év elején"""
        self.szavanna_frissito()
        for i in peldany.szavanna:  # Végig iterál a szavannán
            print(*i)  # Kiírja a szavannát soronként
        input("Nyomj entert")  # A következő év szimulációját érjük el az inputtal
        os.system("cls") | os.system("clear")
        self.jatekev_novelo()  # Növeli a játékévet
        print(self.jatekev, "ÉV")  # Kiírja az éppen aktuális játékévet
        self.ujszulott_allatok_kezelese()  # Kezeli az újszülötteket
        self.eletkornovelo()  # Minden állat életkorát megnöveli 1-el
        self.ehsegnovelo()  # Ragadozók éhségszintjét növeli 1-el
        self.meghal()  # Ha az állat öregségben/éhezésben meghal, akkor eltávolítja
        self.cellak_frissitese()  # Frissíti a cellákat
        print("Szabad cellák száma: ", len(self.szabadcellak))
        print("Ragadozók száma: ", len(self.ragadozok_cellaja))
        print("Növényevők száma: ", len(self.novenyevok_cellaja))


peldany = Szimulacio()
print(peldany.jatekev, " ÉV")  # Kiírja az aktuális játákévet
peldany.cellak_frissitese()  # Frissíti a cellákat
peldany.kezdeti_allatok_generalasa()  # Feltölti állatokkal az osztályt
peldany.cellak_frissitese()  # Frissíti a cellákat

print("Szabad cellák száma: ", len(peldany.szabadcellak))
print("Ragadozók száma: ", len(peldany.ragadozok_cellaja))
print("Növényevők száma: ", len(peldany.novenyevok_cellaja))

# Szimuláció elindítása
peldany.fuggvenyhivasok()

for _ in range(100):  # 100 év szimulációja
    peldany.fuggvenyhivasok()
    for allat in peldany.allatok:  # Végigmegy az állatokon
        if allat.eletkor % allat.szaporodasiido == 0:  # Ha szaporodási évebn van
            if not allat.szaporodott_az_evben:  # Ha még nem szaporodott az évben.
                SZAPORODIK = peldany.szaporodas(
                    allat
                )  # Meghívjuk a szaporodás függvényt
                if not SZAPORODIK:  # Ha nem sikerült szaporodnia
                    if allat.faj == "novenyevo":  # Ha növényevő
                        peldany.novenyevo_mozgas(
                            allat.pozicio, allat
                        )  # Átmozgatjuk egy másik helyre
                        peldany.cellak_frissitese()  # Frissítjük a cellákat
                    else:  # Ha húsevő
                        peldany.husevo_mozgas(
                            allat.pozicio, allat
                        )  # Átmozgatjuk egy másik helyre
                        peldany.cellak_frissitese()  # Frissítjük a cellákat
                    peldany.szaporodas(allat)  # Újra megpróbál szaporodni
                else:
                    peldany.cellak_frissitese()  # Ha elsőre sikerült szaporodnia, akkor frissítjük a cellákat
            else:  # Ha már szaporodott az évben, de még nem mozgott, akkor átmozgatjuk.
                if allat.faj == "novenyevo":  # Ha növényevő
                    peldany.novenyevo_mozgas(
                        allat.pozicio, allat
                    )  # Átmozgatjuk egy másik helyre
                    peldany.cellak_frissitese()  # Frissítjük a cellákat
                else:  # Ha húsevő
                    peldany.husevo_mozgas(
                        allat.pozicio, allat
                    )  # Átmozgatjuk egy másik helyre
                    peldany.cellak_frissitese()  # Frissítjük a cellákat
            peldany.szaporodas(allat)  # Újra megpróbál szaporodni
            peldany.cellak_frissitese()  # frissítjük a cellákat
        else:  # Ha nincs szaporodási évben, akkor átmozgatjuk
            if allat.faj == "novenyevo":  # Ha növényevő
                peldany.novenyevo_mozgas(
                    allat.pozicio, allat
                )  # Meghívjuk a növényevők mozgása függvényt
                peldany.cellak_frissitese()  # Frissítjük a cellákat
            else:  # Ha húsevő
                peldany.husevo_mozgas(
                    allat.pozicio, allat
                )  # Meghívjük a húsevőmozgása függvényt
                peldany.cellak_frissitese()  # Frissítjük a cellákat
        peldany.cellak_frissitese()  # Frissítjük a cellákat
