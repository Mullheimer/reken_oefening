# reken_oefening
Oefenplatform voor kinderen in groep 5 die moeten werken aan rekenvaardigheid en zelfvertrouwen

## Beschrijving
Een adaptieve leer-app in een rustgevend groen thema, ontworpen voor een kind in groep 5. Het programma helpt bij rekenen, typen en spelling door het niveau slim aan te passen: uitdagender bij succes en eenvoudiger bij fouten om demotivatie te voorkomen. De focus ligt op tempo en zelfvertrouwen via positieve feedback en subtiele tijdsdruk, zonder foutmeldingen. Perfect voor veilig oefenen rekensommen tot 200 in een prikkelarme omgeving.

## Functies
- **Adaptieve moeilijkheid**: Automatische aanpassing van het niveau gebaseerd op prestaties
- **Drie oefentypen**: Rekenen, typen en spelling
- **Positieve feedback**: Alleen motiverende berichten, geen foutmeldingen
- **Rustgevend groen thema**: Prikkelarme omgeving voor betere focus
- **Subtiele tijdsdruk**: Visuele timer om tempo aan te moedigen zonder stress
- **Voortgangsregistratie**: Houdt score en niveau bij

## Technologie
- **Backend**: Django met Django REST Framework
- **Frontend**: React
- **Database**: SQLite (voor ontwikkeling)

## Installatie

### Backend (Django)
```bash
# Installeer dependencies
pip install -r requirements.txt

# Voer migraties uit
python manage.py migrate

# Start de Django server
python manage.py runserver
```

De backend draait op `http://localhost:8000`

**Belangrijk voor productie**: De Django SECRET_KEY in `backend/settings.py` is een development key. Voor productie moet deze in een omgevingsvariabele worden gezet.

### Frontend (React)
```bash
# Ga naar de frontend directory
cd frontend

# Installeer dependencies
npm install

# Start de React app
npm start
```

De frontend draait op `http://localhost:3000`

## Gebruik
1. Start eerst de Django backend server
2. Start daarna de React frontend
3. Open je browser en ga naar `http://localhost:3000`
4. Kies een oefentype (Rekenen, Typen, of Spelling)
5. Beantwoord de vragen en zie je niveau automatisch aanpassen!

## Moeilijkheidsgraad Systeem
- **Niveau 1-10**: Automatisch aangepast op basis van prestaties
- **Omhoog**: Na 3 opeenvolgende correcte antwoorden
- **Omlaag**: Na 2 opeenvolgende foute antwoorden
- **Rekenen**: Van optellen tot 20 tot optellen/aftrekken tot 200
- **Typen**: Van korte tot lange woorden
- **Spelling**: Van eenvoudige tot uitdagende woorden

## Ontwikkeling
Dit project is gebouwd met minimale wijzigingen en focus op functionaliteit. Alle code is direct in de repository zonder onnodige complexiteit.
