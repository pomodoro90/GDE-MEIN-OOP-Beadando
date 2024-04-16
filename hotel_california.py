from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
import random


class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 19900)


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 24990)


class Szalloda:
    def __init__(self, nev):
        self.nev = "Hotel California"
        self.szobak = [EgyagyasSzoba(101), EgyagyasSzoba(102),
                       KetagyasSzoba(201), KetagyasSzoba(202), KetagyasSzoba(203)]


class FoglalasiRendszer:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.foglalasok = {}
        self.legutolso_foglalas_id = 0

    def foglalas(self, szobaszam, datum):
        if datum < date.today():
            return "Hiba: A foglalás dátuma nem lehet korábbi, mint a mai nap."

        for foglalas in self.foglalasok.values():
            if foglalas['szobaszam'] == szobaszam and foglalas['datum'] == datum:
                return "Hiba: A szoba már foglalt erre a dátumra."

        self.legutolso_foglalas_id += 1
        foglalas_id = self.legutolso_foglalas_id
        self.foglalasok[foglalas_id] = {'szobaszam': szobaszam, 'datum': datum}
        ar = next(szoba.ar for szoba in self.szalloda.szobak if szoba.szobaszam == szobaszam)

        if szobaszam == 101:
            valasztott_szoba = "Egyágyas"
        elif szobaszam == 102:
            valasztott_szoba = "Egyágyas"
        else:
            valasztott_szoba = "Kétágyas"

        return f"Foglalása sikeres! Foglalási ID: {foglalas_id}, Választott időpont: {datum}, Szoba típusa: {valasztott_szoba}, Ára: {ar} Ft"

    def foglalas_lemondas(self, foglalas_id):
        if foglalas_id in self.foglalasok:
            del self.foglalasok[foglalas_id]
            return "Foglalás lemondva."
        else:
            return "Hiba: Érvénytelen foglalás ID."

    def foglalasok_listazasa(self):
        for id, foglalas in self.foglalasok.items():
            print(f"ID: {id}, Dátum: {foglalas['datum']}, Szobaszám: {foglalas['szobaszam']}")


def veletlenszeru_foglalasok(foglalasi_rendszer):
    ma = date.today()
    for _ in range(5):
        szoba = random.choice(foglalasi_rendszer.szalloda.szobak)
        napok = random.randint(0, 365)
        datum = ma + timedelta(days=napok)
        foglalasi_rendszer.foglalas(szoba.szobaszam, datum)


def datum_formatum_ellenorzese():
    while True:
        datum_str = input("Adja meg a dátumot (ÉÉÉÉ-HH-NN formátumban): ")
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
            if datum < datetime.now().date():
                print("A dátum nem lehet a múltban. Próbálja újra.")
                continue
            return datum
        except ValueError:
            print("Érvénytelen dátum formátum. Próbálja újra.")


def szobaszam_ellenorzese():
    valid_szobaszamok = ("101", "102", "201", "202", "203")
    while True:
        szoba_szama = input("Adja meg a szobaszámot: ")
        if szoba_szama not in valid_szobaszamok:
            print("Érvénytelen szobaszám, válasszon a fentiek közül!")
        else:
            return int(szoba_szama)


def cli():
    logo = """
            ______      __ _    ___ ___  _    ___ _ 
        |_|/ \\||_ |    /  |_||   | |_/ \\|_)|\\| | |_|
        | |\\_/||__|__  \\__| ||___|_| \\_/| \\| |_|_| |
    """
    szalloda = Szalloda("Hotel California")
    foglalasi_rendszer = FoglalasiRendszer(szalloda)
    veletlenszeru_foglalasok(foglalasi_rendszer)
    print(logo)
    print(f"\nÜdvözöljük a {szalloda.nev}-ban!")
    while True:
        print("\nOPCIÓK:")
        print("1. Szobafoglalás")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Válasszon egy menüpontot: ")
        print("\n")
        if valasztas == "1":
            print("Választható szobáink a következők:\nEgyágyas szobák: 101, 102\nKétágyas szobák: 201, 202, 203")
            szobaszam = szobaszam_ellenorzese()
            datum = datum_formatum_ellenorzese()
            print(foglalasi_rendszer.foglalas(szobaszam, datum))
        elif valasztas == "2":
            foglalas_id = int(input("Adja meg a foglalás sorszámát (ID): "))
            print(foglalasi_rendszer.foglalas_lemondas(foglalas_id))
        elif valasztas == "3":
            foglalasi_rendszer.foglalasok_listazasa()
        elif valasztas == "4":
            print("Viszontlátásra!")
            break
        else:
            print("Nincs ilyen opció, kérem válasszon újra! ")


if __name__ == "__main__":
    cli()