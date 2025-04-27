# LinkedIn Bot Automation

Ce projet automatise l'envoi de demandes de connexion LinkedIn à des profils ciblés via Selenium.

## ⚠️ Sécurité
- **Ne partagez jamais vos identifiants LinkedIn !**
- Le fichier `.env` (qui contient vos identifiants) est ignoré par git et ne doit jamais être poussé sur GitHub.

## Installation
1. Clonez le repo :
   ```bash
   git clone <url-du-repo>
   cd <nom-du-repo>
   ```
2. Installez les dépendances :
   ```bash
   pip3 install -r requirements.txt
   ```
3. Installez ChromeDriver (compatible avec votre version de Chrome).

## Configuration
1. Créez un fichier `.env` à la racine du projet :
   ```env
   LINKEDIN_EMAIL=ton.email@exemple.com
   LINKEDIN_PASSWORD=tonMotDePasseSuperSecret
   ```
2. **Ne partagez jamais ce fichier !**

## Utilisation
Lancez le bot :
```bash
python3 linkedin_bot.py
```

Le bot va :
- Se connecter à LinkedIn
- Chercher les profils des entreprises ciblées
- Scroller et paginer automatiquement
- Cliquer sur les boutons "Se connecter" et envoyer les invitations

## Personnalisation
- Modifiez la liste `target_companies` dans `linkedin_bot.py` pour cibler d'autres entreprises.
- Adaptez les limites de connexion si besoin (attention à ne pas spammer !).

## Disclaimer
- L'automatisation LinkedIn peut violer leurs conditions d'utilisation. Utilisez ce script à vos risques et périls.
- LinkedIn peut restreindre ou bannir votre compte en cas d'abus. 