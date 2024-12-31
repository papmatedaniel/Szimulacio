import random

class Allat:
    def __init__(self, faj, pozicioja, maxeletkor, szaporodasiido):
        self.faj = faj #Itt tároljuk a állat faját, vagy növényevő, vagy húsevő(ragadozó)
        self.eletkor = 0 #Itt tároljuk az állat aktuális életkorát
        self.maxeletkor = maxeletkor #Itt tároljuk az állat maximális életkorát
        self.pozicioja = pozicioja #Itt tároljuk az állat pozícióját((x,y) koordináta)
        self.ehsegszint = 0 #Itt tároljuk az állat éhségszitjét, ha ragadozó, akkor minden évben növeljük, ha eszik az évben akkor 0-ra állítjuk
        self.szaporodott_az_evben = False #Ez a változó tárolja, hogy szaporodott e az évben, ez felel azért hogy szaporodási évben ne szaporodhasson kettőször
        self.szaporodasiido = szaporodasiido #Itt tároljuk, hogy hány évente szaporodhat az állat. Növényevő 2 évente, ragadozó 3 évente

class Szimulacio:
    def __init__(self):
        self.tabla = [["." for _ in range(20)] for _ in range(20)]#20x20 mátrix, vizuálisan megjeleníti az állatokat(pozicio, nem)
        self.jatekev = 0 #Itt tároljuk az aktuális játékévet.
        self.allatok = set()#Ide rakjuk az állat objektumot(életkor, faj, kor)
        self.novenyevokcellaja = set()#Itt tároljuk a növényevők celláját
        self.ragadozokcellaja = set() #Itt tároljuk a ragadozók celláját
        self.ujszulottek = set()#Újszülötteket külön setbe gyűjtjük, hogy ne menet közbe addoljuk bele az allatokba
                                #Miután lefutott az adott év, az újszülötteket, belerakjuk az állatokba
        self.novenyevoujszulottekcellaja = set()#Itt tároljuk a növényevő újszülöttek celláját
        self.husevoujszulottekcellaja = set()#Itt tároljuk a húsevő újszülöttek celláját
        self.szabadcellak = set()#Itt tároljuk a szabad cellákat ahova léphet az állat, kerülhet az új utód

    def frissitofuggveny(self):
        """Frissíti a ragadozók, növényevők, újszülöttek, szabadcellákat"""
        self.novenyevokcellaja = {i.pozicioja for i in self.allatok if i.faj == "novenyevo"}
        self.ragadozokcellaja = {i.pozicioja for i in self.allatok if i.faj == "husevo"}
        self.novenyevoujszulottekcellaja = {i.pozicioja for i in self.ujszulottek if i.faj == "novenyevo"}
        self.husevoujszulottekcellaja = {i.pozicioja for i in self.ujszulottek if i.faj == "husevo"}

        osszes_elfoglalt_cella = self.ragadozokcellaja | self.novenyevokcellaja | self.novenyevoujszulottekcellaja | self.husevoujszulottekcellaja
        palya_osszes_cellaja = {(x,y) for x in range(20) for y in range(20)}
        szabadcellak = palya_osszes_cellaja - osszes_elfoglalt_cella
        self.szabadcellak = szabadcellak

    def allatgeneralo(self, faj, pozicio):
        "Legenárlja az adott állatot, és belerakja az állatok set-be"
        husevoeletkor = random.randint(9, 12)
        novenyevoeletkor = random.randint(11,14)
        if faj == "novenyevo": #Ha az állat növényevő
            szaporodasiido = 2 #Akkor 2 évente szaporodhat
            maxeletkor = novenyevoeletkor #A maxéletkora pedig 9,12 éve
        else:
            szaporodasiido = 3 #Ha húsevő akkor pedig, 3 évente
            maxeletkor = husevoeletkor

        self.ujszulottek.add(Allat(faj, pozicio, maxeletkor, szaporodasiido)) #Létrejön az újszülött

    def tablafrissito(self):
        """Minden év végén frissítjük, és kinyomtatjuk a tábla adatait"""
        self.tabla = [["." for _ in range(20)] for _ in range(20)] #Friss üres 20x20-as játéktér
        for i in self.allatok:
            x,y = i.pozicioja
            if i.faj == "novenyevo": #Ha az állat növényevő
                self.tabla[y][x] = "\033[32mN\033[0m" #Akkor a játéktérben N-el jelöljük a helyét
            else:
                self.tabla[y][x] = "\033[31mR\033[0m" #Ha pedig ragadozó, akkor R-el jelöljük

    def kezdetiallatokgeneralasa(self):
        "Legeneráljuk a 0 év állatait."
        szamlalo = 0 
        while szamlalo != 180: #Ez 180 állat generálásáig megy
            veletlen_pozicio = (random.randint(0, 19), random.randint(0, 19)) #Véletlen koordináta a 20x20 mátrixban
            if veletlen_pozicio in self.szabadcellak: #Ha a véletlenkoordináta még nem lett felhasználva
                veletlen_allat = random.randint(1, 100) 
                if veletlen_allat < 65: #65% esély arra, hogy az állat növényevő legyen
                    veletlen_ev = random.randint(11, 14)
                    faj = "novenyevo"
                    szaporodasiido = 2
                else: #35%esély pedig arra, hogy húsevő
                    veletlen_ev = random.randint(9, 12)
                    szaporodasiido = 3
                    faj = "husevo"
                self.allatok.add(Allat(faj, veletlen_pozicio, veletlen_ev, szaporodasiido)) #Az állatokat hozzáadjuk
                szamlalo += 1 #Növeljük a hozzáadott állatok számát

    def jatekevnovelo(self):
        """Minden évben megnöveli 1-el a játékévet"""
        self.jatekev += 1
    
    def ujszulottekkezelese(self):
        """Az újszülötteketet kezeli"""
        self.allatok.update(self.ujszulottek) #Az újszülötteket hozzáadjuk az állatokhoz.
        self.ujszulottek = set() #Az újszülötteket pedig kiürítjük.

    def eletkornovelo(self):
        "Növeli az állatok életkorát"
        for i in self.allatok:
            i.eletkor += 1

    def ehsegnovelo(self):
        "Növeli a húsevők éhség szintjét."
        for i in self.allatok:
            if i.faj == "husevo":
                i.ehsegszint += 1

    def meghal(self):
        "Ha az állat elérte a maximális életkorát, akkor meghal, vagy húsevőnél az éhségszint eléri a 2-t"
        meghalt = set()
        for i in self.allatok:
            if i.eletkor + 1 >= i.maxeletkor or i.ehsegszint >= 3:
                meghalt.add(i)
        self.allatok = self.allatok - meghalt

    def egysugarukor(self, pozicio):
        "Kiszámolja a pályán belül xy pozíció mellett lévő cellákat, és visszadja annak listáját"
        iranyok = {(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)} #Irányok
        egysugaru_szabadkord = set() 
        x1, y1 = pozicio
        for x2, y2 in iranyok:
            uj_pozicio = (x1 + x2, y1 + y2)
            if 0 <= uj_pozicio[0] <= 19 and 0 <= uj_pozicio[1] <= 19:
                egysugaru_szabadkord.add(uj_pozicio)
        return egysugaru_szabadkord
    
    def allatmozgato(self, pozicio):
        "Az állat mellett visszaad egy szabad helyet, ha van, ellenkező esetben a saját koordinátáját adja vissza."
        szabadhelyek = self.egysugarukor(pozicio) & self.szabadcellak
        if szabadhelyek:
            return random.choice(list(szabadhelyek))
        else:
            return pozicio

    def szaporodas(self, allat):
        allatpozicio = allat.pozicioja
        faj = allat.faj
        szaporodasiido = allat.szaporodasiido
        if faj == "novenyevo":
            fajcellaja = self.novenyevokcellaja
        else:
            fajcellaja = self.ragadozokcellaja
        """Ha ivarérett az állat, (ha húsevő nem éhes) akkor kikeresi a mellette lévő fajtársakat."""
        """Ha van fajtárs mellette, akkor végigmegy rajtuk"""
        """Addig megy amíg talál ivarérett fajtársat"""
        """Kigyűjti a két szülő 1 egységsugarú körében lévő pályán belüli cellákat"""
        """Kigyűjti belőlük a szabad cellákat"""
        """Ha van szabad cella, akkor berakja őket egy listába, és random.choiceval létrehozza az utódot."""
        """Új utód objektumot hoz létre"""
        """A 2 szülő tulajdonságát átállítjuk, hogy szaporodott."""
        """Ha sikerül új utódot létrehozni, True-t ad vissza, ellenben False-t"""
        """Ha False, akkor meghívjuk a mozgás függvényt, és utána újra megpróbál mozogni."""
        if self.egysugarukor(allatpozicio) & fajcellaja:
            for i in self.allatok:
                if i.faj == faj and i.eletkor % szaporodasiido == 0 and i.ehsegszint == 0 and allatpozicio != i.pozicioja and i.pozicioja in self.egysugarukor(allatpozicio):
                    utodlehetsegeshelye = self.szabadcellak & (self.egysugarukor(allatpozicio) | self.egysugarukor(i.pozicioja) - {allatpozicio} - {i.pozicioja})
                    if utodlehetsegeshelye:
                        i.szaporodott_az_evben = True
                        allat.szaporodott_az_evben = True
                        ujutodpozicio = random.choice(list(utodlehetsegeshelye))
                        # print(allatpozicio, i.pozicioja, ujutodpozicio)
                        self.allatgeneralo(i.faj, ujutodpozicio)
                        return True
        return False

    def novenyevomozgas(self, allatpozicio, allatobjektum):
        """Átmozgatja szabad helyre, ha van."""
        self.tabla[allatpozicio[1]][allatpozicio[0]] = "."
        allatobjektum.pozicioja = self.allatmozgato(allatpozicio)
        self.tabla[allatpozicio[1]][allatpozicio[0]] = "N"
    
    def husevomozgas(self, allatpozicio, allatobjektum):
        "A húsevő mellett lévő egyik növényevőt fefalja"
        "A meghalt állatot kiveszi a set-ből"
        "Ha nincs növényevő, a közelében, akkor egy random koordinátára lép ha van üres hely mellette.."
        novenyevok = set()
        if self.egysugarukor(allatpozicio) & self.novenyevokcellaja:
            novenyevok.update(self.allatok)
        if self.egysugarukor(allatpozicio) & self.novenyevoujszulottekcellaja:
            novenyevok.update(self.ujszulottek)
        eltavolitando = set()
        for i in novenyevok:
            if i.faj == "novenyevo" and i.pozicioja in self.egysugarukor(allatpozicio):
                allatobjektum.ehsegszint = 0
                allatobjektum.pozicioja = i.pozicioja
                eltavolitando.add(i)
                break
        else:
            allatobjektum.pozicioja = self.allatmozgato(allatpozicio)
        self.allatok = self.allatok - eltavolitando
        self.ujszulottek = self.ujszulottek - eltavolitando
        

peldany = Szimulacio()
print(peldany.jatekev, " ÉV")  #Kiírja az aktuális játákévet
peldany.frissitofuggveny()  #Frissíti a cellákat
peldany.kezdetiallatokgeneralasa()  #Feltölti állatokkal az osztályt
peldany.frissitofuggveny()  #Frissíti a cellákat


for _ in range(100):  #100 év szimulációja
    peldany.tablafrissito()
    for i in peldany.tabla:  #Végig iterál a táblán
        print(*i)  #Kiírja a táblát soronként
    input()  #A következő év szimulációját érjük el az inputtal
    peldany.jatekevnovelo()  #Növeli a játékévet
    print(peldany.jatekev, " ÉV")  #Kiírja az éppen aktuális játékévet
    peldany.ujszulottekkezelese()  #Kezeli az újszülötteket
    peldany.eletkornovelo()  #Minden állat életkorát megnöveli 1-el
    peldany.ehsegnovelo()  #Ragadozók éhségszintjét növeli 1-el
    peldany.meghal()  #Ha az állat öregségben/éhezésben meghal, akkor eltávolítja
    peldany.frissitofuggveny()  #Frissíti a cellákat
    print("Szabad cellák száma: ", len(peldany.szabadcellak))
    print("ragadozók száma: ", len(peldany.ragadozokcellaja))
    print("növényevőkcellája: ", len(peldany.novenyevokcellaja))
    for allat in peldany.allatok:  #Végigmegy az állatokon
        if allat.eletkor % allat.szaporodasiido == 0: #Ha szaporodási évebn van
            if not allat.szaporodott_az_evben: #Ha még nem szaporodott az évben.
                szaporodik = peldany.szaporodas(allat) #Meghívjuk a szaporodás függvént
                if not szaporodik: #Ha nem sikerült szaporodnia
                    if allat.faj == "novenyevo": #Ha növényevő
                        peldany.novenyevomozgas(allat.pozicioja, allat)  #Átmozgatjuk egy másik helyre
                        peldany.frissitofuggveny() #Frissítjük a cellákat
                    else: #Ha húsevő
                        peldany.husevomozgas(allat.pozicioja, allat) #Átmozgatjuk egy másik helyre
                        peldany.frissitofuggveny() #Frissítjük a cellákat
                    peldany.szaporodas(allat) #Újra megpróbál szaporodni
                    peldany.frissitofuggveny() #frissítjük a cellákat
                else:
                    peldany.frissitofuggveny() #Ha elsőre sikerült szaporodnia, akkor frissítjük a cellákat
            else: #Ha már szaporodtt az évben, de még nem mozgott, akkor átmozgatjuk.
                if allat.faj == "novenyevo": #Ha növényevő
                        peldany.novenyevomozgas(allat.pozicioja, allat)  #Átmozgatjuk egy másik helyre
                        peldany.frissitofuggveny() #Frissítjük a cellákat
                else: #Ha húsevő
                    peldany.husevomozgas(allat.pozicioja, allat) #Átmozgatjuk egy másik helyre
                    peldany.frissitofuggveny() #Frissítjük a cellákat
                peldany.szaporodas(allat) #Újra megpróbál szaporodni
                peldany.frissitofuggveny() #frissítjük a cellákat


        else: #Ha nincs szaporodási évben, akkor átmozgatjuk
            if allat.faj == "novenyevo": #Ha növényevő
                peldany.novenyevomozgas(allat.pozicioja, allat) #Meghívjuk a növényevők mozgása függvényt
                peldany.frissitofuggveny() #Frissítjük a cellákat

            else: #Ha húsevő
                peldany.husevomozgas(allat.pozicioja, allat) #Meghívjük a húsevőmozgása függvényt
                peldany.frissitofuggveny() #Frissítjük a cellákat

        peldany.frissitofuggveny() #Frissítjük a cellákat
