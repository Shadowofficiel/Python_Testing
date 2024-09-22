import json
from flask import Flask, render_template, request, redirect, flash, url_for

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        # Message flash pour les emails non valides
        flash("Désolé, vous n'êtes pas un secrétaire. Veuillez réessayer.")
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Récupérer les réservations déjà effectuées par le club (ajout d'une clé dans clubs ou competitions)
    if 'placesBooked' not in club:
        club['placesBooked'] = 0  # Initialiser à 0 si la clé n'existe pas encore

    totalPlacesBooked = club['placesBooked'] + placesRequired

    # Vérification de la limite de 12 places
    if totalPlacesBooked > 12:
        flash(f"Vous ne pouvez pas réserver plus de 12 places au total pour une compétition. Vous avez déjà réservé {club['placesBooked']} places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification des points disponibles du club
    if placesRequired > int(club['points']):
        flash(f"Vous ne pouvez réserver que {club['points']} places en fonction de vos points disponibles.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification des places disponibles pour la compétition
    if placesRequired > int(competition['numberOfPlaces']):
        flash(f"Il n'y a pas assez de places disponibles. Vous avez demandé {placesRequired} places, mais il n'en reste que {competition['numberOfPlaces']}.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Mettre à jour les places réservées par le club et les places disponibles dans la compétition
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    club['placesBooked'] += placesRequired  # Mise à jour du nombre total de places réservées par le club

    flash(f"Réservation réussie! Vous avez réservé {placesRequired} places. Total des places réservées : {club['placesBooked']}.")
    
    # Vérifier si le concours est complet
    if competition['numberOfPlaces'] == 0:
        flash(f"Le concours {competition['name']} est maintenant complet.")

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

# TODO: Add route for points display
