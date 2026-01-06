# Reken Oefening

Een interactief oefenprogramma gericht op rekenvaardigheid voor kinderen in groep 5. De focus ligt op het verhogen van het tempo en het opbouwen van zelfvertrouwen door middel van adaptieve moeilijkheidsgraad en positieve bekrachtiging.

## Features (MVP)

- **Optellen en aftrekken tot 20** - Sommen worden automatisch gegenereerd
- **Adaptief algoritme** - Bij goede antwoorden stijgt de moeilijkheid, bij fouten daalt deze weer
- **Prikkelarm design** - Rustige pastelkleuren, veel witruimte, geen felle animaties
- **Groot numeriek toetsenbord** - Speciaal ontworpen voor tablets en touch-apparaten
- **Zachte foutafhandeling** - Geen harde "FOUT" meldingen, alleen subtiele correctie
- **Positieve bekrachtiging** - Sterretjes en bemoedigende berichten bij goede antwoorden
- **Sessie-overzicht** - Na elke sessie een positieve samenvatting

## Screenshots

### Startscherm
![Startscherm](https://github.com/user-attachments/assets/a69e3f1f-7567-46f0-b6c4-d09efa846293)

### Oefenen
![Oefenen](https://github.com/user-attachments/assets/1b3178c8-d171-41d6-96d1-2fa4f236a1b0)

### Streak indicator
![Streak](https://github.com/user-attachments/assets/c81d433d-628e-4952-8a1d-fcfca6c4dd4d)

### Sessie samenvatting
![Samenvatting](https://github.com/user-attachments/assets/73a7033e-2bdb-48c6-89e8-437df73d20f2)

## Installatie

```bash
# Clone de repository
git clone https://github.com/Mullheimer/reken_oefening.git
cd reken_oefening

# Installeer dependencies
npm install

# Start de development server
npm run dev
```

## Gebruik

1. Open de app in een browser (standaard op `http://localhost:5173`)
2. Klik op "Start met oefenen! 🚀"
3. Los de sommen op met het numerieke toetsenbord of je fysieke toetsenbord
4. Klik op ✓ of druk op Enter om je antwoord te controleren
5. Klik op "Klaar met oefenen" voor een overzicht van je sessie

## Scripts

- `npm run dev` - Start de development server
- `npm run build` - Bouw de productie-versie
- `npm run preview` - Preview de productie build
- `npm run lint` - Run ESLint

## Technologie

- **React 19** - UI framework
- **Vite** - Build tool
- **CSS** - Styling (geen externe libraries voor minimale footprint)

## Roadmap

- [x] **MVP**: React app met sommen-generator (optellen/aftrekken tot 20) en basis UI
- [ ] **Versie 1.1**: Implementatie van tafels en uitgebreid adaptief algoritme
- [ ] **Versie 1.2**: Subtiele timer en beloningssysteem
- [ ] **Versie 2.0**: Backend integratie voor AI-gestuurde regelgeneratie en opslag

## Doelgroep

Primaire gebruiker: Kind (Groep 5), prikkelgevoelig, onzeker bij fouten, heeft moeite met tafels, werkt aan tempo.

## Licentie

Private project
