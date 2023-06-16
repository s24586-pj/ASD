import random
import time


# Ustawienie wielkosci tablic,losowanie...
rozmiar = 1000000
         
tablica = [random.randint(0, rozmiar) for _ in range(rozmiar)]
posortowana_tablica = sorted(tablica)
odwrotnie_posortowana_tablica = sorted(tablica, reverse=True)


def heapsort(tablica):
    def tworz_kopiec(tablica, n, i):
        najwiekszy = i
        lewy = 2 * i + 1
        prawy = 2 * i + 2

        if lewy < n and tablica[i] < tablica[lewy]:
            najwiekszy = lewy

        if prawy < n and tablica[najwiekszy] < tablica[prawy]:
            najwiekszy = prawy

        if najwiekszy != i:
            tablica[i], tablica[najwiekszy] = tablica[najwiekszy], tablica[i]
            tworz_kopiec(tablica, n, najwiekszy)

    n = len(tablica)

    for i in range(n // 2-1,-1,-1):
        tworz_kopiec(tablica, n, i)

    for i in range(n - 1, 0, -1):
        tablica[i], tablica[0] = tablica[0], tablica[i]
        tworz_kopiec(tablica, i, 0)


def quicksort(tablica):
    def podziel(tablica, lewy, prawy):
        i = lewy - 1
        os = tablica[prawy]

        for j in range(lewy, prawy):
            if tablica[j] < os:
                i += 1
                tablica[i], tablica[j] = tablica[j], tablica[i]

        tablica[i + 1], tablica[prawy] = tablica[prawy], tablica[i + 1]
        return i + 1

    def quicksort_pomocniczy(tablica, lewy, prawy):
        if lewy < prawy:
            pi = podziel(tablica, lewy, prawy)
            quicksort_pomocniczy(tablica, lewy, pi - 1)
            quicksort_pomocniczy(tablica, pi + 1, prawy)
    quicksort_pomocniczy(tablica, 0, len(tablica) - 1)




# def sortowanie_babelkowe(tablica):
#     n = len(tablica)
#     for i in range(n):
#         for j in range(0, n - i - 1):
#             if tablica[j] > tablica[j + 1]:
#                 tablica[j], tablica[j + 1] = tablica[j + 1], tablica[j]






# sluzy do sprawddzania czasu time.time()

# Pomiar czasu dla Heapsort 
startowy_czas = time.time()
heapsort(tablica[:])
koncowy_czas = time.time()
czas_heapsort = koncowy_czas - startowy_czas

# Pomiar czasu dla Quicksort 
startowy_czas = time.time()
quicksort(tablica[:])
koncowy_czas = time.time()
czas_quicksort = koncowy_czas - startowy_czas

# Pomiar czasu dla QuicksortO 
startowy_czas = time.time()
heapsort(posortowana_tablica[:])
koncowy_czas = time.time()
czas_heapsortO = koncowy_czas - startowy_czas

# Pomiar czasu dla Quicksort 
# startowy_czas = time.time()
# sortowanie_babelkowe(posortowana_tablica[:])
# koncowy_czas = time.time()
# czas_sortowanie_babelkoweO = koncowy_czas - startowy_czas



# # Pomiar czasu dla Sortowania bąbelkowego
# startowy_czas = time.time()
# sortowanie_babelkowe(tablica[:])
# koncowy_czas = time.time()
# czas_sortowanie_babelkowe = koncowy_czas - startowy_czas



# Wyświetlenie wyników
print("Czasy działania algorytmów:")
print("Heapsort:", czas_heapsort)
print("Quicksort:", czas_quicksort)
# print("Sortowanie bąbelkowe:", czas_sortowanie_babelkoweO)



print("Heapsort odwrotny:", czas_heapsortO)
# print("Sortowanie bąbelkowe odwrotne:", czas_sortowanie_babelkoweO)