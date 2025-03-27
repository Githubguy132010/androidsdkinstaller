# Android SDK Platform Tools Installer

Een gebruiksvriendelijke Windows GUI-installer voor de Android SDK Platform Tools.

## Vereisten

- Windows 10 of later
- Python 3.8 of later
- Administrator rechten voor installatie

## Installatie

1. Installeer de benodigde Python packages:
```bash
pip install -r requirements.txt
```

2. Start de installer:
```bash
python installer.py
```

## Functies

- Moderne en gebruiksvriendelijke GUI interface
- Aangepaste installatie directory selectie
- Automatische PATH configuratie optie
- Ingebouwde update checker
- Voortgangsindicatie tijdens installatie
- Uitgebreide foutafhandeling en logging

## Gebruik

1. Start de installer met administrator rechten
2. Kies een installatie directory
3. Selecteer of u de platform tools wilt toevoegen aan het systeem PATH
4. Controleer op updates (optioneel)
5. Klik op "Installeer" om het proces te starten

## Logging

Alle installatie-activiteiten worden gelogd in het bestand `installer.log`. Dit bestand kan nuttig zijn voor het oplossen van problemen.

## Probleemoplossing

Als u problemen ondervindt tijdens de installatie:

1. Controleer of u administrator rechten heeft
2. Zorg voor een stabiele internetverbinding
3. Controleer het logbestand voor meer details
4. Zorg dat uw antivirussoftware de installer niet blokkeert

## Licentie

Dit project is open source en beschikbaar onder de MIT-licentie. 