# projekt 'Steady as she goes!'

Szukanie najkrótszej trasy dla statku

Struktura projektu (najważniejsze pliki):
```
/
├─ examples/        - folder z przykładami
├─ frontend/  
│  ├─ window.py     - okno edytora, interakcja z użytkowniiem
│  ├─ table.py      - model opisujący Qt<->tablice pythonowe
│  ├─ visualise.py - wizualizacja z matplotlib
├─ mapsolver/       - "biblioteka" do rozwiązywaina problemu
│  ├─ mynode.py     - prosta klasa węzła w grafie
│  ├─ solver.py     - algorytm BSF do grafu
├─ main.py          - główny plik, po prostu wywołuje funkcje frontend.start()
├─ doc.pdf          - dokumentacja
```

Proszę przeczytać `doc.pdf`
