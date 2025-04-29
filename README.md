# Nazwa Zadanie 2

Krótki program CLI do zarządzania zadaniami z obsługą plików, dekoratorem mierzącym czas wykonania.

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/Vernli/zadanie2
   ```
2. Wejdź do katalogu projektu:
   ```bash
   cd zadanie2
   ```
3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
4. (Opcjonalnie) Utwórz i aktywuj środowisko wirtualne:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Windows: venv\\Scripts\\activate
   ```

## Użycie

1. Uruchom skrypt:
   ```bash
   python task_manager.py
   ```
2. Korzystaj z interaktywnego menu, wybierając opcje dla:
   - dodawania zadań
   - usuwania zadań
   - przełączania stanu wykonania
   - edycji zadania
   - zapisu/odczytu z pliku

## Dokumentacja

Aby wygenerować dokumentację bazującą na docstringach:
```bash
pydoc -w task_manager
```
Wynikiem będzie plik `task_manager.html` w katalogu projektu.

## Autor

Dawid Krajewski

## Licencja

MIT License

