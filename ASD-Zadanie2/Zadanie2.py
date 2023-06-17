import heapq
import os
from collections import Counter

#FUNKCJE/OBIEKTY

# Obiekt jak w Javie ( konstruktor self to samo co this) i porównanie ze sobą częstotliwosci poszczególneych wezłówHuffmana
class WęzełHuffmana:
    def __init__(self, znak, częstotliwość):
        self.znak = znak
        self.częstotliwość = częstotliwość
        self.lewy = None
        self.prawy = None

    
    def __lt__(self, inny):
        return self.częstotliwość < inny.częstotliwość


class DrzewoHuffmana:
    def __init__(self):
        self.korzeń = None

    #   Tworzymy kolejke priorytetowa->Tworzymy obiekt WęzełHuffmana -> dodajemy go do kolejki
    def buduj_drzewo(self, tabela_częstotliwości):

        kolejka_priorytetowa = []

        for znak, częstotliwość in tabela_częstotliwości.items():
            węzeł = WęzełHuffmana(znak, częstotliwość)

            heapq.heappush(kolejka_priorytetowa, węzeł)

        
        # Wyciagamy dwa wezly o ! NAMNIEJSZYCH CZESTOTLIWOSCIACH (heapq.heappop) ! LW I PW
        while len(kolejka_priorytetowa) > 1:

            lewy_węzeł = heapq.heappop(kolejka_priorytetowa)
            prawy_węzeł = heapq.heappop(kolejka_priorytetowa)

            # EXTRACTMIN RIGHT LW PW 
            złączona_częstotliwość = lewy_węzeł.częstotliwość + prawy_węzeł.częstotliwość

             #ERROR 
            # złączony_znak = lewy_węzeł.znak + prawy_węzeł.znak pytanie
            # złączony_węzeł = WęzełHuffmana(złączony_znak, złączona_częstotliwość)

            złączony_węzeł = WęzełHuffmana(None, złączona_częstotliwość)
            złączony_węzeł.lewy = lewy_węzeł
            złączony_węzeł.prawy = prawy_węzeł
            
            # Dodanie elementu po EXTRACTMIN tego zlaczonego wezla
            heapq.heappush(kolejka_priorytetowa, złączony_węzeł)

          
        self.korzeń = heapq.heappop(kolejka_priorytetowa)
     
    def buduj_tabelę_kodowania(self):

        tabela_kodowania = {}
        
        self.buduj_sciezke(self.korzeń, "", tabela_kodowania)
        return tabela_kodowania

      
    def buduj_sciezke(self, węzeł, obecny_kod, tabela_kodowania):

        # Jeśli nie jest to ExtractMin zlaczonego tekstu przypisujemy znakowi sciezke i w zaleznosci czy idzie w prawo czy w lewo dodajemy 0/1 (tutaj pytanie)
        if węzeł.znak is not None:
            tabela_kodowania[węzeł.znak] = obecny_kod
            
            print(f"Znak: | {węzeł.znak} | Ścieżka: {obecny_kod}, Liczba wystąpień: {węzeł.częstotliwość}")
            return

        self.buduj_sciezke(węzeł.lewy, obecny_kod + "0", tabela_kodowania)
        self.buduj_sciezke(węzeł.prawy, obecny_kod + "1", tabela_kodowania)




#MAIN


def kompresuj_plik(plik_wejściowy, plik_wyjściowy):
    with open(plik_wejściowy, 'r') as plik:
        tekst = plik.read()

    tabela_częstotliwości = Counter(tekst)

    drzewo_huffmana = DrzewoHuffmana()

    drzewo_huffmana.buduj_drzewo(tabela_częstotliwości)
    
    # Zamienie na binarke
    tabela_kodowania = drzewo_huffmana.buduj_tabelę_kodowania()

    # To co zostalo zamienione polacz w calosc
    zakodowany_tekst = ''.join(tabela_kodowania[znak] for znak in tekst)

     # Wyrównanie do pełnych bajtów tak aby potem zapisać go jako asci zeby go zakomprosować  
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
print("              SLOWNICZEK")
print("ZLICZENIE ILOŚCI WYSTĄPIEŃ I ŚCIEŻKI")
print("--------------------------------------------------------------")


plik_wejściowy = "input.txt"
plik_wyjściowy = "skompresowany.bin"
kompresuj_plik(plik_wejściowy, plik_wyjściowy)

rozmiar_wejściowy = os.path.getsize(plik_wejściowy)
rozmiar_skompresowany = os.path.getsize(plik_wyjściowy)


print("--------------------------------------------------------------")
print("Rozmiar pliku wejściowego:", rozmiar_wejściowy, "bajtów")
print("Rozmiar skompresowanego pliku:", rozmiar_skompresowany, "bajtów")
print("--------------------------------------------------------------")
