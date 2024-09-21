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
    
    # Vérification si le nombre de places demandées est supérieur aux points disponibles
    if placesRequired > int(club['points']):
        flash(f"Vous ne pouvez réserver que {club['points']} places. Veuillez ajuster votre demande.")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Vérification si les places demandées dépassent les places disponibles pour la compétition
    if placesRequired > int(competition['numberOfPlaces']):
        flash(f"Il n'y a pas assez de places disponibles. Vous avez demandé {placesRequired} places, mais il n'en reste que {competition['numberOfPlaces']}.")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Si tout est valide, mise à jour des places disponibles et des points du club
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash('Réservation réussie!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

# TODO: Add route for points display
