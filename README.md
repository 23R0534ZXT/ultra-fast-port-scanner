# Ultra-Fast Port Scanner

**FR** : Un scanner de ports réseau ultra-rapide en Python, créé par **23R**.  
**EN** : An ultra-fast network port scanner in Python, built by **23R**.

Ce projet utilise **sockets non-bloquants** et **multithreading** pour vérifier les ports ouverts et **Tkinter** pour une interface graphique simple.  
This project uses **non-blocking sockets** and **multithreading** to check open ports and **Tkinter** for a simple GUI.

---

## Fonctionnalités / Features

- **Interface intuitive / Intuitive GUI**  
  Champs pour hôte, plage de ports, avec boutons "Lancer", "Tous scanner" et "Arrêter".

- **Scan ultra-rapide / Ultra-fast scanning**  
  Utilise des sockets non-bloquants et plusieurs threads pour scanner 1-66000 en quelques minutes.

- **Résultats clairs / Clear results**  
  Affiche les ports ouverts dans l’interface et les sauvegarde en JSON.

- **Scan complet / Full scan**  
  Bouton "Tous scanner" pour vérifier tous les ports de 1 à 66000.

---

## Prérequis / Requirements

- Python 3.8+
- Bibliothèques : `tkinter`, `socket`, `json`, `queue` (inclus avec Python)

Pas de dépendances externes nécessaires / No external dependencies required.

## Installation / Setup

1. Clonez le dépôt / Clone the repo:
   ```bash
   git clone https://github.com/yourusername/ultra-fast-port-scanner.git
   ```
2. Lancez le scanner / Run the scanner:
   ```bash
   python port_scanner.py
   ```

## Utilisation / Usage

1. Ouvrez l’interface / Open the GUI.  
2. Entrez un hôte (IP ou domaine, ex. : 127.0.0.1) / Enter a host (IP or domain, e.g., 127.0.0.1).  
3. Pour un scan personnalisé, entrez une plage de ports (ex. : 1-1000) / For a custom scan, enter a port range (e.g., 1-1000).  
4. Cliquez sur **Lancer** pour un scan personnalisé ou **Tous scanner** pour 1-66000 / Click **Start** for a custom scan or **Scan all** for 1-66000.  
5. Cliquez sur **Arrêter** pour arrêter / Click **Stop** to stop.  
6. Les résultats sont sauvegardés dans `scan_results.json` si des ports sont ouverts.

## Notes

- **FR** : Ce projet est pour apprendre le scanning réseau, pas pour des usages malveillants. Utilisez-le sur des systèmes que vous avez l’autorisation de scanner.  
- **EN** : This project is for learning network scanning, not for malicious use. Only scan systems you have permission to scan.  
- Testez sur votre machine (ex. : 127.0.0.1) pour éviter tout problème.  
- Le scan est optimisé pour la vitesse maximale, mais peut manquer des ports sur des réseaux lents.

## Licence / License

Sous **licence MIT**. Voir [LICENSE](LICENSE) pour plus d’infos.  
Under **MIT License**. See [LICENSE](LICENSE) for details.

## Auteur / Author

**23R** 
