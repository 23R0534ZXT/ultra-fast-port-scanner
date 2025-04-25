# Ultra-Fast Port Scanner
# Auteur/Author: 23R
# Créé/Created: April 2025
# Description (FR): Scanner de ports réseau ultra-rapide utilisant des sockets non-bloquants, multithreading et Tkinter.
# Description (EN): Ultra-fast network port scanner using non-blocking sockets, multithreading, and Tkinter.
# Dépendances/Requirements: Python 3.8+, tkinter (inclus/included)

import tkinter as tk
from tkinter import messagebox
import socket
import threading
import json
from queue import Queue
import errno
import time

# Variables globales / Global variables
scan_running = False
results = []
queue = Queue()
lock = threading.Lock()

def scan_port(host, port):
    """
    FR: Vérifie si un port est ouvert sur un hôte donné avec socket non-bloquant.
    EN: Checks if a port is open on a given host using non-blocking socket.
    
    Args:
        host (str): Adresse IP ou domaine / IP address or domain.
        port (int): Numéro du port / Port number.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    
    try:
        sock.connect((host, port))
    except BlockingIOError:
        pass  # Connexion en cours, vérifier plus tard
    except socket.gaierror:
        sock.close()
        return None
    except OSError as e:
        if e.errno != errno.EINVAL:  # Ignorer erreurs non pertinentes
            sock.close()
            return None

    # Attendre brièvement pour vérifier la connexion
    start_time = time.time()
    while time.time() - start_time < 0.05:  # Attente max de 50ms
        try:
            sock.send(b'')
            sock.close()
            return port
        except OSError:
            time.sleep(0.001)
    
    sock.close()
    return None

def worker(host, log_widget):
    """
    FR: Fonction exécutée par chaque thread pour scanner les ports.
    EN: Worker function run by each thread to scan ports.
    
    Args:
        host (str): Hôte à scanner / Host to scan.
        log_widget (tk.Text): Widget pour afficher les résultats / Widget to display results.
    """
    global results
    while not queue.empty() and scan_running:
        port = queue.get()
        open_port = scan_port(host, port)
        if open_port:
            with lock:
                results.append(open_port)
                log_widget.insert(tk.END, f"Port {open_port} ouvert/open\n")
                log_widget.yview(tk.END)
        queue.task_done()

def start_scan(host, start_port, end_port, log_widget, num_threads=50):
    """
    FR: Lance le scan des ports avec plusieurs threads.
    EN: Starts port scanning with multiple threads.
    
    Args:
        host (str): Hôte à scanner / Host to scan.
        start_port (int): Port de départ / Start port.
        end_port (int): Port de fin / End port.
        log_widget (tk.Text): Widget pour afficher les résultats / Widget to display results.
        num_threads (int): Nombre de threads / Number of threads.
    """
    global scan_running, results, queue
    results = []
    queue = Queue()
    log_widget.delete(1.0, tk.END)
    log_widget.insert(tk.END, f"Scan ultra-rapide de {host} (ports {start_port}-{end_port})...\n")
    log_widget.yview(tk.END)

    # Remplir la file avec les ports / Fill the queue with ports
    for port in range(start_port, end_port + 1):
        queue.put(port)

    # Lancer les threads / Start threads
    threads = []
    for _ in range(min(num_threads, end_port - start_port + 1)):
        t = threading.Thread(target=worker, args=(host, log_widget))
        t.start()
        threads.append(t)

    # Attendre la fin des threads / Wait for threads to finish
    for t in threads:
        t.join()

    if scan_running:
        log_widget.insert(tk.END, "Scan terminé/Scan completed.\n")
        if results:
            with open("scan_results.json", "w") as f:
                json.dump({"host": host, "open_ports": results}, f)
            log_widget.insert(tk.END, "Résultats sauvegardés dans scan_results.json\n")
        else:
            log_widget.insert(tk.END, "Aucun port ouvert trouvé/No open ports found.\n")
    scan_running = False

def start_gui():
    """
    FR: Crée l'interface graphique Tkinter pour le scanner.
    EN: Sets up the Tkinter GUI for the scanner.
    """
    def start_scan_thread():
        """FR: Valide les entrées et lance le scan.
           EN: Validates inputs and starts the scan."""
        global scan_running
        if scan_running:
            messagebox.showinfo("Info", "Scan déjà en cours/Scan already running.")
            return

        host = host_entry.get()
        try:
            start_port = int(start_port_entry.get())
            end_port = int(end_port_entry.get())
        except ValueError:
            messagebox.showerror("Erreur/Error", "Ports doivent être des nombres/Ports must be numbers.")
            return

        if not host:
            messagebox.showerror("Erreur/Error", "Entrez un hôte/Enter a host.")
            return
        if not (1 <= start_port <= end_port <= 66000):
            messagebox.showerror("Erreur/Error", "Ports entre 1 et 66000/Ports between 1 and 66000.")
            return

        scan_running = True
        threading.Thread(target=start_scan, args=(host, start_port, end_port, log_widget)).start()

    def scan_all():
        """FR: Lance un scan complet des ports 1-66000.
           EN: Starts a full scan of ports 1-66000."""
        global scan_running
        if scan_running:
            messagebox.showinfo("Info", "Scan déjà en cours/Scan already running.")
            return

        host = host_entry.get()
        if not host:
            messagebox.showerror("Erreur/Error", "Entrez un hôte/Enter a host.")
            return

        start_port_entry.delete(0, tk.END)
        start_port_entry.insert(0, "1")
        end_port_entry.delete(0, tk.END)
        end_port_entry.insert(0, "66000")

        scan_running = True
        threading.Thread(target=start_scan, args=(host, 1, 66000, log_widget)).start()

    def stop_scan():
        """FR: Arrête le scan.
           EN: Stops the scan."""
        global scan_running
        if scan_running:
            scan_running = False
            messagebox.showinfo("Arrêt/Stop", "Scan arrêté/Scan stopped.")
        else:
            messagebox.showinfo("Arrêt/Stop", "Aucun scan en cours/No scan running.")

    # FR: Configure la fenêtre / EN: Set up the window
    root = tk.Tk()
    root.title("Ultra-Fast Port Scanner - by 23R")

    tk.Label(root, text="Hôte/Host (IP ou domaine/domain):").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    host_entry = tk.Entry(root)
    host_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Port de départ/Start port:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    start_port_entry = tk.Entry(root)
    start_port_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Port de fin/End port:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    end_port_entry = tk.Entry(root)
    end_port_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(root, text="Lancer/Start", bg="green", fg="white", command=start_scan_thread).grid(row=3, column=1, pady=10)
    tk.Button(root, text="Tous scanner/Scan all", bg="blue", fg="white", command=scan_all).grid(row=4, column=1, pady=10)
    tk.Button(root, text="Arrêter/Stop", bg="red", fg="white", command=stop_scan).grid(row=5, column=1, pady=10)

    log_widget = tk.Text(root, height=10, width=50)
    log_widget.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
