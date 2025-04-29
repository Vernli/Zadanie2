f"""
Moduł task_manager:

Zapewnia klasy do zarządzania zadaniami w CLI:
- Zadanie: bazowa klasa zadania z możliwością dodatkowych atrybutów.
- ZadaniePiorytetowe: zadanie z priorytetem.
- ZadanieRegularne: zadanie powtarzalne.
- ManagerZadan: Wprowadzanie, odczytanie, sortowanie, zmiana statusu Zadania oraz zapis/odczyt zadań w pliku tekstowym.

Dodatkowo:
- dekorator @czas_wykonania mierzy czas wykonania operacji.
- dokumentacja metod i klas zawarta w docstringach.

Kod pobrany z: https://github.com/twoje-konto/twoje-repozytorium

Użycie pydoc do generacji HTML:
    pydoc -w task_manager

Tworzenie środowiska wirtualnego:
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
"""
from datetime import datetime
import os
import time


def czas_wykonania(func):
    """
    Dekorator mierzący czas wykonania funkcji.
    :param func: funkcja do opakowania
    :return: wynik funkcji
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Funkcja '{func.__name__}' wykonana w {end - start:.4f} s")
        return result
    return wrapper

class Zadanie:
    """
    Bazowa klasa zadania.

    :param tytul: tytuł zadania
    :param opis: opis zadania (domyślnie pusty)
    :param termin: termin realizacji (str YYYY-MM-DD lub date)
    :param kwargs: dodatkowe atrybuty zadania
    """
    def __init__(self, tytul, opis="", termin=None, **kwargs):
        self.tytul = tytul
        self.opis = opis
        if isinstance(termin, str):
            try:
                self.termin_wykonaia = datetime.strptime(termin, "%Y-%m-%d").date()
            except ValueError:
                self.termin_wykonaia = None
        else:
            self.termin_wykonaia = termin
        self.wykonane = False
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        """
        Zwraca reprezentację tekstową zadania, w tym wszystkie dodatkowe atrybuty.
        :return: string z tytułem, opisem, terminem, statusem i dodatkowymi polami
        """
        base = [f"Tytuł: {self.tytul}", f"Opis: {self.opis}", f"Termin: {self.termin_wykonaia}"]
        status = 'Wykonane' if self.wykonane else 'Niewykonane'
        base.append(f"Wykonany: {status}")
        # zbieramy dodatkowe atrybuty
        extras = []
        for k, v in self.__dict__.items():
            if k not in ('tytul','opis','termin_wykonaia','wykonane'):
                extras.append(f"{k}={v}")
        if extras:
            base.append("Dodatkowe: " + ", ".join(extras))
        return " | ".join(base)

    def wykonany(self):
        """
        Toggle stanu wykonania zadania.
        :return: None
        """
        self.wykonane = not self.wykonane

class ZadaniePiorytetowe(Zadanie):
    """
    Zadanie z priorytetem.

    :param priorytet: poziom priorytetu (domyślnie 'Średni')
    """
    def __init__(self, tytul, opis="", termin=None, priorytet="Średni", **kwargs):
        super().__init__(tytul, opis, termin, **kwargs)
        self.priorytet = priorytet

    def __str__(self):
        """
        Zwraca reprezentację zadania priorytetowego, w tym wszystkie dodatkowe atrybuty.
        """
        base = [f"Tytuł: {self.tytul}", f"Opis: {self.opis}", f"Termin: {self.termin_wykonaia}",
                f"Priorytet: {self.priorytet}"]
        status = 'Wykonane' if self.wykonane else 'Niewykonane'
        base.append(f"Wykonany: {status}")
        extras = []
        for k, v in self.__dict__.items():
            if k not in ('tytul', 'opis', 'termin_wykonaia', 'wykonane', 'priorytet'):
                extras.append(f"{k}={v}")
        if extras:
            base.append("Dodatkowe: " + ", ".join(extras))
        return " | ".join(base)

class ZadanieRegularne(Zadanie):
    """
    Zadanie powtarzalne.

    :param powtarzalnosc: interwał powtarzania (domyślnie 'codziennie')
    """
    def __init__(self, tytul, opis="", termin=None, powtarzalnosc="codziennie", **kwargs):
        super().__init__(tytul, opis, termin, **kwargs)
        self.powtarzalnosc = powtarzalnosc

    def __str__(self):
        """
        Zwraca reprezentację zadania regularnego, w tym wszystkie dodatkowe atrybuty.
        """
        base = [f"Tytuł: {self.tytul}", f"Opis: {self.opis}", f"Termin: {self.termin_wykonaia}",
                f"Powtarzalność: {self.powtarzalnosc}"]
        status = 'Wykonane' if self.wykonane else 'Niewykonane'
        base.append(f"Wykonany: {status}")
        extras = []
        for k, v in self.__dict__.items():
            if k not in ('tytul','opis','termin_wykonaia','wykonane','powtarzalnosc'):
                extras.append(f"{k}={v}")
        if extras:
            base.append("Dodatkowe: " + ", ".join(extras))
        return " | ".join(base)

class ManagerZadan:
    """
    Menedżer zadań: obsługa CRUD, toggle, zapis i odczyt.

    :param save_dir: katalog zapisu/odczytu (domyślnie katalog skryptu)
    """
    def __init__(self, save_dir=None):
        base = save_dir or os.path.dirname(os.path.abspath(__file__))
        self.save_dir = base
        self.zadania = []

    @czas_wykonania
    def dodaj_zadanie(self, zadanie=None, tytul=None, opis=None, termin=None, typ='zwykle', **kwargs):
        """
        Dodaje zadanie.
        :param zadanie: obiekt Zadanie (opcjonalnie)
        :param tytul: tytuł (jeśli nie przekazano obiektu)
        :param opis: opis
        :param termin: termin
        :param typ: 'zwykle', 'priorytet', 'regular'
        :param kwargs: dodatkowe atrybuty przekazane do konstruktora
        """
        if zadanie is None:
            if typ == 'priorytet':
                zad = ZadaniePiorytetowe(tytul, opis or "", termin, **kwargs)
            elif typ == 'regular':
                zad = ZadanieRegularne(tytul, opis or "", termin, **kwargs)
            else:
                zad = Zadanie(tytul, opis or "", termin, **kwargs)
        else:
            zad = zadanie
        self.zadania.append(zad)

    @czas_wykonania
    def usun_zadanie(self, zadanie=None, tytul=None):
        """
        Usuwa zadanie po obiekcie lub tytule.
        """
        target = zadanie or next((z for z in self.zadania if z.tytul == tytul), None)
        if target and target in self.zadania:
            self.zadania.remove(target)

    @czas_wykonania
    def oznacz_jako_wykonane(self, zadanie=None, tytul=None):
        """
        Oznacza zadanie jako wykonane.
        """
        target = zadanie or next((z for z in self.zadania if z.tytul == tytul), None)
        if target:
            target.wykonane = True

    @czas_wykonania
    def edytuj_zadanie(self, zadanie, nowy_tytul=None, nowy_opis=None, nowy_termin=None, **kwargs):
        """
        Edycja zadania.
        Dodatkowe parametry przez **kwargs.
        """
        if zadanie in self.zadania:
            if nowy_tytul:
                zadanie.tytul = nowy_tytul
            if nowy_opis:
                zadanie.opis = nowy_opis
            if nowy_termin:
                zadanie.termin_wykonaia = nowy_termin
            for k, v in kwargs.items():
                setattr(zadanie, k, v)

    @czas_wykonania
    def zapisz_do_pliku(self, nazwa_pliku="zadania.txt", encoding="utf-8"):  # argumenty domyślne
        """
        Zapisuje zadania do pliku.
        :param nazwa_pliku: nazwa pliku do zapisu
        :param encoding: kodowanie pliku
        """
        full_path = os.path.join(self.save_dir, nazwa_pliku)
        if os.path.commonpath([self.save_dir, full_path]) != self.save_dir:
            raise ValueError("Ścieżka spoza katalogu skryptu niedozwolona")
        with open(full_path, "w", encoding=encoding) as f:
            for z in self.zadania:
                typ = type(z).__name__
                parts = [typ, z.tytul, z.opis, str(z.termin_wykonaia)]
                extras = {k: v for k, v in z.__dict__.items() if k not in ("tytul","opis","termin_wykonaia","wykonane")}
                parts += [f"{k}={v}" for k, v in extras.items()]
                parts.append(f"wykonane={z.wykonane}")
                f.write(";".join(parts) + "\n")

    @czas_wykonania
    def wczytaj_z_pliku(self, nazwa_pliku="zadania.txt", encoding="utf-8"):  # argumenty domyślne
        """
        Wczytuje zadania z pliku.
        :param nazwa_pliku: nazwa pliku do odczytu
        :param encoding: kodowanie pliku
        """
        full_path = os.path.join(self.save_dir, nazwa_pliku)
        if os.path.commonpath([self.save_dir, full_path]) != self.save_dir:
            raise ValueError("Ścieżka spoza katalogu skryptu niedozwolona")
        with open(full_path, "r", encoding=encoding) as f:
            for line in f:
                parts = line.strip().split(";")
                typ, tytul, opis, termin_str = parts[0], parts[1], parts[2], parts[3]
                attr_pairs = parts[4:]
                attrs = {}
                for pair in attr_pairs:
                    k,v = pair.split("=",1)
                    attrs[k] = (v == "True") if v in ("True","False") else v
                date_val = datetime.strptime(termin_str, "%Y-%m-%d").date()
                if typ == "ZadaniePiorytetowe":
                    zad = ZadaniePiorytetowe(tytul, opis, date_val, **attrs)
                elif typ == "ZadanieRegularne":
                    zad = ZadanieRegularne(tytul, opis, date_val, **attrs)
                else:
                    zad = Zadanie(tytul, opis, date_val, **attrs)
                if attrs.get("wykonane"):
                    zad.wykonane = True
                self.zadania.append(zad)

    def __str__(self):
        """Zwraca listę zadań w formie tekstu."""
        return "\n".join(str(z) for z in self.zadania)

    def __contains__(self, zadanie):
        """Sprawdza, czy zadanie jest w menedżerze."""
        return zadanie in self.zadania


# --- Definicje klas Zadanie, ZadaniePiorytetowe, ZadanieRegularne, ManagerZadan (jak wyżej) ---

# Dokładna treść klas została pominięta dla skrótu

if __name__ == "__main__":
    """
    Punkt wejścia programu:
    Interaktywny interfejs CLI do zarządzania zadaniami.

    Dostępne opcje:
    1. Dodaj zadanie (priorytetowe lub regularne)
    2. Usuń zadanie po tytule
    3. Toggle stanu wykonania zadania
    4. Edytuj parametry zadania
    5. Wyświetl wszystkie zadania
    6. Wyświetl zadania posortowane po terminie wykonania
    7. Zapisz zadania do pliku tekstowego w katalogu skryptu
    8. Wczytaj zadania z pliku tekstowego w katalogu skryptu
    0. Wyjście z programu

    Aby wygenerować dokumentację HTML dla tego modułu użyj:
        pydoc -w task_manager
    """
    manager = ManagerZadan()
    manager.dodaj_zadanie(
        tytul="Przygotuj raport",
        opis="Raport kwartalny finansów",
        termin=datetime(2025, 5, 15).date(),
        typ='priorytet',
        priorytet="Wysoki",  # parametr specyficzny dla ZadaniePiorytetowe
        kategoria="Finanse",  # dodatkowy atrybut
        tagi="raport, pilot project"  # zostanie przetworzony na listę jeśli masz taką logikę
    )

    while True:
        print("Menu:")
        print("1. Dodaj zadanie")
        print("2. Usuń zadanie")
        print("3. Ustaw zadanie jako wykonane")
        print("4. Edytuj zadanie")
        print("5. Wyświetl wszystkie zadania")
        print("6. Wyświetl zadania posortowane po terminie wykonania")
        print("7. Zapisz zadania do pliku txt")
        print("8. Wczytaj zadania z pliku txt")
        print("0. Wyjście")

        choice = input("Wybierz opcję: ")

        if choice == '1':
            # Dodawanie zadania: wczytywanie danych od użytkownika
            tytul = input("Podaj tytuł: ")
            opis = input("Podaj opis: ")
            termin = input("Podaj termin wykonania [DD-MM-YYYY]: ")
            try:
                termin_date = datetime.strptime(termin, "%d-%m-%Y").date()
            except ValueError:
                print("Nieprawidłowy format terminu. Użyj DD-MM-YYYY.")
                continue
            typ = input("p=priorytetowe, r=regularne: ")
            if typ == 'p':
                priorytet = input("Podaj priorytet: ")
                zad = ZadaniePiorytetowe(tytul, opis, termin_date, priorytet)
            elif typ == 'r':
                powtarzalnosc = input("Podaj powtarzalność: ")
                zad = ZadanieRegularne(tytul, opis, termin_date, powtarzalnosc)
            else:
                print("Nieprawidłowy typ.")
                continue
            manager.dodaj_zadanie(zad)

        elif choice == '2':
            # Usuwanie zadania po tytule
            tytul = input("Tytuł do usunięcia: ")
            zad = next((z for z in manager.zadania if z.tytul == tytul), None)
            if zad:
                manager.usun_zadanie(zad)
            else:
                print("Nie znaleziono.")

        elif choice == '3':
            # Toggle stanu wykonania
            tytul = input("Tytuł wykonanego zadania: ")
            zad = next((z for z in manager.zadania if z.tytul == tytul), None)
            if zad:
                zad.wykonany()
            else:
                print("Nie znaleziono.")

        elif choice == '4':
            # Edycja zadania
            tytul = input("Tytuł do edycji: ")
            zad = next((z for z in manager.zadania if z.tytul == tytul), None)
            if zad:
                nowy = input("Nowy tytuł (ENTER aby pominąć): ")
                nowo = input("Nowy opis (ENTER aby pominąć): ")
                nyt = input("Nowy termin DD-MM-YYYY (ENTER aby pominąć): ")
                nyt_date = None
                if nyt:
                    try:
                        nyt_date = datetime.strptime(nyt, "%d-%m-%Y").date()
                    except ValueError:
                        print("Nieprawidłowy termin.")
                manager.edytuj_zadanie(zad, nowy or None, nowo or None, nyt_date)
            else:
                print("Nie znaleziono.")

        elif choice == '5':
            # Wyświetlanie wszystkich zadań
            print(manager)

        elif choice == '6':
            # Sortowanie zadań po terminie
            for z in sorted(manager.zadania, key=lambda x: x.termin_wykonaia or datetime.max.date()):
                print(z)

        elif choice == '7':
            # Zapis do pliku
            fn = input("Nazwa pliku: ")
            manager.zapisz_do_pliku(fn)

        elif choice == '8':
            # Wczytanie z pliku
            fn = input("Nazwa pliku: ")
            manager.wczytaj_z_pliku(fn)

        elif choice == '0':
            # Zakończenie programu
            break
        else:
            print("Nieprawidłowy wybór.")

