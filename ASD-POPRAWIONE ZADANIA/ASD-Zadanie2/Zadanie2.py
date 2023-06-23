import os
import json
from collections import Counter

class WęzełHuffmana:
    def __init__(self, znak, częstotliwość):
        self.znak = znak
        self.częstotliwość = częstotliwość
        self.lewy = None
        self.prawy = None

    def __lt__(self, inny):
        return self.częstotliwość < inny.częstotliwość


class KolejkaPriorytetowa:
    def __init__(self):

        self.kopiec = []

      #dodanie do kopca
    def dodaj(self, element):
        self.kopiec.append(element)
        self.przesun_w_górę(len(self.kopiec) - 1)

    # ukladanie wartosci w kopcu(sprawdza czy element na danym indexie jest mniejszy od swojego rodzica jesli tak zamienia go miejscami.) 
    def przesun_w_górę(self, index):
        rodzic = (index - 1) // 2

        if index > 0 and self.kopiec[index] < self.kopiec[rodzic]:
            self.kopiec[index], self.kopiec[rodzic] = self.kopiec[rodzic], self.kopiec[index]
            self.przesun_w_górę(rodzic)


    #Po ułożeniu pobieramy najmnieszą wartość zamienniamy ją z ostatnią wartoscia i wyrzucamy
    def pobierz_min(self):

        if len(self.kopiec) == 0:
            return None
        
        min_element = self.kopiec[0]
        self.kopiec[0] = self.kopiec[-1]
        self.kopiec.pop()
        
        #przywracamy kopiec
        self.napraw_kopiec_w_doł(0)

        return min_element

     
    def napraw_kopiec_w_doł(self, index):

        dziecko_lewe = 2 * index + 1
        dziecko_prawe = 2 * index + 2

        #najmniesza wartosc w kopcu 0 (index)
        Najmniejsza_wartosc = index

        #sprawdzamy czy lewe dziecko jest najmniejsze jesli tak zamiana tak samo z drugim 
        if dziecko_lewe < len(self.kopiec) and self.kopiec[dziecko_lewe] < self.kopiec[Najmniejsza_wartosc]:
            Najmniejsza_wartosc = dziecko_lewe

        if dziecko_prawe < len(self.kopiec) and self.kopiec[dziecko_prawe] < self.kopiec[Najmniejsza_wartosc]:
            Najmniejsza_wartosc = dziecko_prawe


        if Najmniejsza_wartosc != index:
            self.kopiec[index], self.kopiec[Najmniejsza_wartosc] = self.kopiec[Najmniejsza_wartosc], self.kopiec[index]
            self.napraw_kopiec_w_doł(Najmniejsza_wartosc)


class DrzewoHuffmana:
    def __init__(self):
        self.korzeń = None

 #   Tworzymy kolejke priorytetowa->Tworzymy obiekt WęzełHuffmana -> dodajemy go do kolejki
    def buduj_drzewo(self, tabela_częstotliwości):
        kolejka_priorytetowa = KolejkaPriorytetowa()

        for znak, częstotliwość in tabela_częstotliwości.items():
            węzeł = WęzełHuffmana(znak, częstotliwość)
            kolejka_priorytetowa.dodaj(węzeł)

        # Wyciagamy dwa wezly o ! NAMNIEJSZYCH CZESTOTLIWOSCIACH (heapq.heappop) ! LW I PW
        while len(kolejka_priorytetowa.kopiec) > 1:
            lewy_węzeł = kolejka_priorytetowa.pobierz_min()
            prawy_węzeł = kolejka_priorytetowa.pobierz_min()

             # EXTRACTMIN RIGHT LW PW 
            złączona_częstotliwość = lewy_węzeł.częstotliwość + prawy_węzeł.częstotliwość

              #ERROR 
            # złączony_znak = lewy_węzeł.znak + prawy_węzeł.znak pytanie
            # złączony_węzeł = WęzełHuffmana(złączony_znak, złączona_częstotliwość)

            złączony_węzeł = WęzełHuffmana(None, złączona_częstotliwość)

            złączony_węzeł.lewy = lewy_węzeł
            złączony_węzeł.prawy = prawy_węzeł

            # Dodanie elementu po EXTRACTMIN tego zlaczonego wezla
            kolejka_priorytetowa.dodaj(złączony_węzeł)

        self.korzeń = kolejka_priorytetowa.pobierz_min()

    def buduj_tabelę_kodowania(self):
        tabela_kodowania = {}
        self.buduj_scieżkę(self.korzeń, "", tabela_kodowania)
        return tabela_kodowania

    def buduj_scieżkę(self, węzeł, obecny_kod, tabela_kodowania):
        if węzeł.znak is not None:
            tabela_kodowania[węzeł.znak] = obecny_kod
            print(f"Znak: | {węzeł.znak} | Ścieżka: {obecny_kod}, Liczba wystąpień: {węzeł.częstotliwość}\n")
            return
        self.buduj_scieżkę(węzeł.lewy, obecny_kod + "0", tabela_kodowania)
        self.buduj_scieżkę(węzeł.prawy, obecny_kod + "1", tabela_kodowania)

#MAIN

def kompresuj_plik(plik_wejściowy, plik_wyjściowy, plik_slowniczka):
    with open(plik_wejściowy, 'r') as plik:
        tekst = plik.read()

    tabela_częstotliwości = Counter(tekst)

    drzewo_huffmana = DrzewoHuffmana()
    drzewo_huffmana.buduj_drzewo(tabela_częstotliwości)

    # Zamienie na binarke
    tabela_kodowania = drzewo_huffmana.buduj_tabelę_kodowania()

    with open(plik_slowniczka, 'w') as plik:
        json.dump(tabela_kodowania, plik)

    # Wyrównanie do pełnych bajtów tak aby potem zapisać go jako asci zeby go zakomprosować  
    zakodowany_tekst = ''.join(tabela_kodowania[znak] for znak in tekst)
    wyrównanie = 8 - len(zakodowany_tekst) % 8
    zakodowany_tekst += wyrównanie * "0"

    tablica_bajtów = bytearray()
    for i in range(0, len(zakodowany_tekst), 8):
        bajt = zakodowany_tekst[i:i + 8]
        tablica_bajtów.append(int(bajt, 2))

    #   ord(znak) konwetuje znak na jego kod ASCII
    with open(plik_wyjściowy, 'wb') as plik:
        plik.write(bytes([wyrównanie]))
        for znak, częstotliwość in tabela_częstotliwości.items():
            plik.write(bytes([ord(znak), częstotliwość]))
        plik.write(tablica_bajtów)


print("--------------------------------------------------------------")
print("              SŁOWNICZEK")
print("ZLICZENIE ILOŚCI WYSTĄPIEŃ I ŚCIEŻKI")
print("--------------------------------------------------------------")

plik_wejściowy = "input.txt"
plik_wyjściowy = "skompresowany.bin"
plik_slowniczka = "slowniczek.txt"
kompresuj_plik(plik_wejściowy, plik_wyjściowy, plik_slowniczka)

rozmiar_wejściowy = os.path.getsize(plik_wejściowy)
rozmiar_skompresowany = os.path.getsize(plik_wyjściowy)
rozmiar_slowniczka = os.path.getsize(plik_slowniczka)

print("--------------------------------------------------------------")
print("Rozmiar pliku wejściowego:", rozmiar_wejściowy, "bajtów")
print("Rozmiar skompresowanego pliku:", rozmiar_skompresowany, "bajtów")
print("Rozmiar pliku słowniczka:", rozmiar_slowniczka, "bajtów")
print("--------------------------------------------------------------")
