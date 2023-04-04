# Zadanie1 - wywołania systemowe

Zwrócić pid procesu mającego najdłuższą ścieżkę przodków prowadzącą do procesu nie mającego rodzica, zwrócić długość tej ścieżki.

## Rozwiązanie

Zmodyfikowałem serwer mm, dodając w nim nowe wywołania `GETLCHN` i `GETLCHNPID`. w pliku `usr/src/mm/misc.c` jest ich implementacja. Obydwa robią to samo, ale jeden zwraca pid procesu, a drugi długość ścieżki.
Rozwiązanie nie jest w stu procentach optymalne, ale wystarczające w przeciętnych warunkach (można utrzymywać pomocniczą tabelę, żeby ograniczyć powtórne sprawdzanie tych samych procesów w drzewie, choć wymaga to dodatkowych nakładów obliczeniowych).

w folderze `usr/tmp` jest przykładowy program, który tworzy łańcuch procesów, w celu sprawdzenia co zwróci wywołanie systemowe. Przykładowe wyniki:

| Wygenerowany łańcuch | Wynik wywołania systemowego |
|----------------------|-----------------------------|
| 5                    | 8                           |
| 10                   | 13                          |
| 15                   | 18                          |
| 25                   | 28                          |

Syscall zawsze zwraca liczbę większą o 3, niż to, o co poprosiliśmy program testujący, i jest to poprawne, ponieważ przed naszym programem są jeszcze procesy wcześniej w hierarchii (np. INIT, sh).



