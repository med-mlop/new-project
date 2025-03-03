from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'

# Configurer la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Prestige1234@'
app.config['MYSQL_DB'] = 'python'

mysql = MySQL(app)

# Route par défaut qui vérifie si l'utilisateur est connecté
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))  # Redirige vers la page d'accueil si l'utilisateur est connecté
    return redirect(url_for('login'))  # Sinon, redirige vers la page de login

# Page d'accueil qui est accessible uniquement si l'utilisateur est connecté
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'], message="Welcome!")
    return redirect(url_for('login'))  # Si pas connecté, redirige vers la page de login

# Page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        city = request.form['city']
        email = request.form['email']

        # Connexion à la base de données
        conn = mysql.connection
        cursor = conn.cursor()

        try:
            # Insérer l'utilisateur dans la base de données
            cursor.execute("INSERT INTO utilisateur (name, city, email) VALUES (%s, %s, %s)", (username, city, email))
            conn.commit()  # Valider l'insertion
            flash('Utilisateur enregistré avec succès', 'success')

            # Sauvegarder l'utilisateur dans la session
            session['username'] = username

        except Exception as e:
            conn.rollback()  # Annuler si erreur
            flash(f'Erreur lors de l\'enregistrement: {e}', 'danger')
        finally:
            cursor.close()

        return redirect(url_for('home'))  # Rediriger vers la page d'accueil après connexion réussie

    return render_template('login.html')  # Afficher le formulaire de connexion

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('username', None)  # Supprimer l'utilisateur de la session
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('login'))  # Rediriger vers la page de connexion après déconnexion

if __name__ == '__main__':
    app.run(debug=True)
