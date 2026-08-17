import time
import hashlib
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folder, który chcemy bezpiecznie monitorować (nasza piaskownica)
FOLDER_TO_MONITOR = "./monitored_folder"

# Funkcja kryptograficzna - oblicza unikalny odcisk palca (skrót SHA-256) pliku
def calculate_file_hash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            # Czytamy plik po kawałku, żeby nie zapchać RAM-u przy dużych plikach
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    except PermissionError:
        return "[BŁĄD BRAKU UPRAWNIEŃ]"

# Klasa, która reaguje na to, co zgłasza system operacyjny
class MonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"⚠️ [MODYFIKACJA] Zmieniono plik: {event.src_path}")
            new_hash = calculate_file_hash(event.src_path)
            print(f"   -> Nowy skrót SHA-256: {new_hash}\n")

    def on_created(self, event):
        if not event.is_directory:
            print(f"✅ [UTWORZENIE] Pojawił się nowy plik: {event.src_path}")
            new_hash = calculate_file_hash(event.src_path)
            print(f"   -> Skrót SHA-256: {new_hash}\n")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"❌ [USUNIĘCIE] Zniknął plik: {event.src_path}\n")

if __name__ == "__main__":
    # Sprawdzamy, czy folder do monitorowania w ogóle istnieje
    if not os.path.exists(FOLDER_TO_MONITOR):
        print(f"Błąd: Nie znaleziono folderu '{FOLDER_TO_MONITOR}'!")
        exit(1)

    print(f"--- File Integrity Monitor Uruchomiony ---")
    print(f"Nasłuchiwanie zmian w: {FOLDER_TO_MONITOR}")
    print("Naciśnij Ctrl+C, aby zatrzymać.\n")

    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_MONITOR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1) # Skrypt działa w pętli i czeka na zdarzenia
    except KeyboardInterrupt:
        observer.stop()
        print("\nZatrzymano monitorowanie.")
    
    observer.join()