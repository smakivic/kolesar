import risar
import random


class Ovira:

    def __init__(self):
        self.sirina = random.randint(30, 80)
        self.x0 = random.randint(1, risar.maxX - self.sirina - 1)
        self.x1 = self.x0 + self.sirina
        self.y1 = 25
        self.y0 = 0
        self.barva = risar.rjava
        self.body = risar.pravokotnik(self.x0, self.y0, self.x1, self.y1, self.barva)
        self.udareno = False

    def promjeni_boju(self):
        self.barva = risar.barva(212, 93, 93)
        risar.odstrani(self.body)
        self.body = risar.pravokotnik(self.x0, self.y0, self.x1, self.y1, self.barva)

    def update(self):
        self.y1 += 1
        self.y0 += 1
        self.body.setPos(self.x0, self.y0)

    def daj_koordinate(self):
        return (self.x0, self.y0, self.x1, self.y1)


class Kolesar:
    def __init__(self):
        self.y = risar.maxY - 141
        self.x = random.randint(1, risar.maxX - 41)
        self.body = risar.slika(self.x, self.y, 'kolesar.png')
        self.zivoti = 3
        self.poeni = 0

    def update(self):
        self.body.setPos(self.x, self.y)

    def idi_lijevo(self):
        if self.x > 1:
            self.x -= 2
        self.update()

    def idi_desno(self):
        if self.x < risar.maxX - 46:
            self.x += 2
        self.update()

    def provjeri_udar(self, objekat):

        x1_min, y1_min, x1_max, y1_max = self.x + 10, self.y + 40, self.x + 30, self.y + 60
        x2_min, y2_min, x2_max, y2_max = objekat.daj_koordinate()
        return (x1_min < x2_max) and (x1_max > x2_min) and (y1_min < y2_max) and (y1_max > y2_min)


nagrade = [("flowers.png", 1), ("bottle.png", 1), ("stones.png", 2), ("grass.png", 3), ("walker.png", 4),
           ("scooter.png", 2)]


class Nagrade:

    def __init__(self):
        self.x0 = random.randint(1, risar.maxX - 36)
        self.y0 = 1
        self.y1 = 41
        self.x1 = self.x0 + 35
        self.slika, self.poeni = nagrade[random.randint(0, len(nagrade) - 1)]
        self.body = risar.slika(self.x0, self.y0, self.slika)

    def update(self):
        self.y1 += 1
        self.y0 += 1
        self.body.setPos(self.x0, self.y0)

    def daj_koordinate(self):
        return (self.x0, self.y0, self.x1, self.y1)


from PyQt5.QtMultimedia import QSound

objekti = []
kolesarec = Kolesar()
zivoti = risar.besedilo(risar.maxX - 50, 1, str(kolesarec.zivoti), velikost=40)
broj_nagrada = 0
nagrada = risar.besedilo(1, 1, str(kolesarec.poeni), velikost=40)

pozadinski_zvuk = QSound('arcade.wav')

pozadinski_zvuk.play()

while True:

    if pozadinski_zvuk.isFinished():
        pozadinski_zvuk.play()

    if risar.levo():
        kolesarec.idi_lijevo()

    if risar.desno():
        kolesarec.idi_desno()

    if random.random() < 0.01:
        objekti.append(Nagrade())
        broj_nagrada += 1

    if len(objekti) - broj_nagrada < 20:
        if random.random() < 0.02:
            objekti.append(Ovira())
    for objekat in objekti:
        objekat.update()
        if isinstance(objekat, Ovira):
            if kolesarec.provjeri_udar(objekat) and not objekat.udareno:
                if kolesarec.zivoti == 1:
                    risar.odstrani(zivoti)
                    risar.besedilo(risar.maxX - 50, 1, '0', velikost=40)
                    pozadinski_zvuk.stop()
                    objekat.promjeni_boju()
                    QSound.play('explosion.wav')
                    risar.stoj()
                else:
                    kolesarec.zivoti -= 1
                    objekat.promjeni_boju()
                    QSound.play('explosion.wav')
                    objekat.udareno = True

                risar.odstrani(zivoti)
                zivoti = risar.besedilo(risar.maxX - 50, 1, str(kolesarec.zivoti), velikost=40)
            if objekat.y1 == risar.maxY - 1:
                risar.odstrani(objekat.body)
                objekti.remove(objekat)
        else:
            if kolesarec.provjeri_udar(objekat):
                kolesarec.poeni += objekat.poeni
                QSound.play('jump.wav')
                risar.odstrani(objekat.body)
                objekti.remove(objekat)
                risar.odstrani(nagrada)
                nagrada = risar.besedilo(1, 1, str(kolesarec.poeni), velikost=40)
            if objekat.y1 == risar.maxY - 1:
                risar.odstrani(objekat.body)
                objekti.remove(objekat)
    risar.obnovi()
    risar.cakaj(0.002)






