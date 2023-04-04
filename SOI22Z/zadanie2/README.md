# Zadanie 2

Zmieniony został algorytm szeregowania, w którym zdefiniowane są trzy grupy procesów. Każdy proces należący do grupy ma do dyspozycji określony przez grupę kwant czasu. Procesy w grupie, oraz same grupy, zmieniają się według polityki round-robin.

Zmieniona została struktura `proc` o nowe pole `group` informujące, do której grupy należy proces.

Nowy algorytm jest w `proc.c:sched()`.

Dodano również trzy wywołania systemowe, które sięgają do mikrokernela z różnymi potrzebami (zmiana przypisanych kwantów, obliczenie zużytego czasu użytkowego, zmiana grupy procesu).

W folderze `usr/tmp` są trzy programy do testowania funkcjonalności:
* `five_proc.c` tworzy trzy procesy w grupie 1 oraz dwa w grupie 2, które nic nie robią, ale można zbadać ich czas użytkowy. 
* `change_quant.c` pozwala zmieniać kwanty grup
* `time_groups.c` zwraca porównanie czasów, jakie wykorzystały procesy w grupach 1 i 2 (suma grupy 1 a grupy 2).
