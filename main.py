from flask import Flask, render_template_string, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'la_dolce_vita_secret_key_997'

reviews = [
    {
        "id": 1,
        "name": "Marco V.",
        "rating": 5,
        "comment": "Najlepsza pizza w całym Los Santos! Prawdziwe włoskie ciasto.",
        "date": "25 lutego 2026"
    },
    {
        "id": 2,
        "name": "Kamil GTA",
        "rating": 5,
        "comment": "Klimat super, jedzenie szybko podane.",
        "date": "26 lutego 2026"
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pizzeria - La Dolce Vita</title>
    <link rel="icon" type="image/png" href="https://cdn.discordapp.com/attachments/1535405503109144726/1542567147803517070/ChatGPT_Image_24_sie_2026_20_20_53.png">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #c0392b; --primary-dark: #962d22; --accent: #d4ac0d; --dark: #1a1a1a; --light: #fdfbf7; --gray: #7f8c8d; }
        * { box-sizing: border-box; margin: 0; padding: 0; scroll-behavior: smooth; }
        body { font-family: 'Poppins', sans-serif; background-color: var(--light); color: var(--dark); line-height: 1.6; }
        
        header { 
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                        url('https://cdn.discordapp.com/attachments/1537171868388167901/1542652759562526872/tlo.jpg') no-repeat center center; 
            background-size: cover;
            color: white; 
            min-height: 90vh; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            text-align: center; 
            position: relative; 
        }
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 8%; background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); position: fixed; width: 100%; top: 0; z-index: 1000; }
        
        .logo-area { display: flex; align-items: center; gap: 12px; }
        .logo-img { height: 50px; width: 50px; object-fit: contain; border-radius: 50%; background: white; padding: 2px; }
        .logo-area h1 { font-family: 'Playfair Display', serif; font-size: 1.5rem; color: white; }
        
        .nav-links { list-style: none; display: flex; gap: 25px; align-items: center; }
        .nav-links a { color: white; text-decoration: none; transition: color 0.3s; font-weight: 500; }
        .nav-links a:hover { color: var(--accent); }
        .admin-badge { background: var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; }

        .hero-content { margin: auto; max-width: 800px; padding: 0 20px; }
        .hero-content h2 { font-family: 'Playfair Display', serif; font-size: 3.2rem; margin-bottom: 20px; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
        .hero-content p { font-size: 1.2rem; margin-bottom: 30px; color: #f0f0f0; }
        .btn { display: inline-block; background-color: var(--primary); color: white; padding: 12px 30px; border-radius: 30px; text-decoration: none; font-weight: 500; border: none; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background-color: var(--primary-dark); }
        
        section { padding: 80px 10%; }
        .section-title { text-align: center; font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 15px; color: var(--dark); }
        .section-subtitle { text-align: center; color: var(--gray); margin-bottom: 50px; font-size: 1.1rem; }
        
        .menu-image-container { text-align: center; max-width: 700px; margin: 0 auto; background: #111; padding: 15px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .menu-image-container img { width: 100%; height: auto; border-radius: 10px; }

        .info-container { display: grid; grid-template-columns: 1fr 1fr; gap: 50px; align-items: center; background: white; border-radius: 15px; padding: 40px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); }
        .info-details ul { list-style: none; margin-top: 20px; }
        .info-details li { margin-bottom: 15px; display: flex; align-items: center; gap: 15px; font-size: 1.05rem; }
        .info-details li i { color: var(--primary); font-size: 1.2rem; width: 25px; }
        .map-placeholder { height: 350px; border-radius: 10px; overflow: hidden; position: relative; border: 2px solid #ddd; }
        .map-placeholder img { width: 100%; height: 100%; object-fit: cover; }
        
        .reviews-section { background-color: #f7f4ed; }
        .rating-overview { text-align: center; margin-bottom: 30px; font-size: 1.3rem; font-weight: 600; }
        .rating-overview span { color: #d4ac0d; font-size: 1.8rem; }
        .reviews-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin-bottom: 50px; }
        .review-card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.03); position: relative; }
        .review-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .review-author { font-weight: 600; }
        .stars { color: #d4ac0d; letter-spacing: 2px; }
        .review-date { font-size: 0.8rem; color: var(--gray); margin-top: 10px; display: block; }
        .delete-btn { background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 5px; font-size: 0.8rem; cursor: pointer; margin-top: 10px; }
        .delete-btn:hover { background: #c0392b; }

        .review-form-container { background: white; max-width: 700px; margin: 0 auto; padding: 40px; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-family: inherit; }
        .form-group textarea { resize: vertical; height: 120px; }
        
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 2000; justify-content: center; align-items: center; }
        .modal-content { background: white; padding: 30px; border-radius: 10px; width: 300px; text-align: center; }
        .modal-content input { width: 100%; padding: 10px; margin: 15px 0; border: 1px solid #ddd; border-radius: 5px; }

        footer { background: var(--dark); color: white; text-align: center; padding: 30px; font-size: 0.9rem; }
        @media(max-width: 768px) { .info-container { grid-template-columns: 1fr; } .nav-links { display: none; } .hero-content h2 { font-size: 2.2rem; } }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo-area">
                <img src="https://cdn.discordapp.com/attachments/1535405503109144726/1542567147803517070/ChatGPT_Image_24_sie_2026_20_20_53.png" alt="Logo" class="logo-img">
                <h1>La Dolce Vita</h1>
            </div>
            <ul class="nav-links">
                <li><a href="#menu">Menu</a></li>
                <li><a href="#lokalizacja">Lokalizacja</a></li>
                <li><a href="#opinie">Opinie</a></li>
                {% if session.get('is_admin') %}
                    <li><a href="/logout" class="admin-badge">Wyloguj (Admin)</a></li>
                {% else %}
                    <li><a href="#" onclick="document.getElementById('loginModal').style.display='flex'; return false;">Panel Administratora</a></li>
                {% endif %}
            </ul>
        </nav>
        <div class="hero-content">
            <h2>Autentyczny Smak Włoch w Sercu Los Santos</h2>
            <p>Ręcznie robiona pizza wypiekana w tradycyjnym piecu. Prawdziwe składniki i niepowtarzalny klimat.</p>
            <a href="#menu" class="btn">Sprawdź Menu</a>
        </div>
        <div style="height: 50px;"></div>
    </header>

    <section id="menu">
        <h2 class="section-title">Nasze Menu</h2>
        <p class="section-subtitle">Oficjalne ceny i specjały La Dolce Vita</p>
        <div class="menu-image-container">
            <img src="https://cdn.discordapp.com/attachments/1541512104614432842/1542502122577338479/content.png" alt="Menu La Dolce Vita">
        </div>
    </section>

    <section id="lokalizacja">
        <h2 class="section-title">Gdzie Nas Znajdziesz?</h2>
        <p class="section-subtitle">Odwiedź nasz lokal w dzielnicy Del Perro / plaża w Los Santos</p>
        <div class="info-container">
            <div class="info-details">
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 15px;">La Dolce Vita Los Santos</h3>
                <p>Nasz lokal znajduje się w świetnej lokalizacji niedaleko wybrzeża i molo w zachodnim Los Santos (lokalizacja zaznaczona kością na mapie).</p>
                <ul>
                    <li><i class="fa-solid fa-location-dot"></i> <span>Del Perro / Plaża, Los Santos</span></li>
                    <li><i class="fa-solid fa-clock"></i> <span>Czynne: Całodobowo (24/7)</span></li>
                </ul>
            </div>
            <div class="map-placeholder">
                <img src="https://cdn.discordapp.com/attachments/1541512104614432843/1542488327561683005/36873c94-a767-4e1c-9b13-fcc21fe45e01.png" alt="Mapa Los Santos">
            </div>
        </div>
    </section>

    <section id="opinie" class="reviews-section">
        <h2 class="section-title">Opinie Klientów</h2>
        <p class="section-subtitle">Zobacz, co mówią o nas klienci, lub zostaw swoją opinię!</p>
        
        <div class="rating-overview">
            Średnia ocena: <span>{{ avg_rating }} / 5.0</span>
            <div style="font-size: 1rem; color: #7f8c8d; margin-top: 5px;">Na podstawie sumy wszystkich ocen ({{ total_reviews }} opinii)</div>
        </div>

        <div class="reviews-grid">
            {% for review in reviews %}
            <div class="review-card">
                <div class="review-header">
                    <span class="review-author">{{ review.name }}</span>
                    <span class="stars">{% for i in range(review.rating) %}★{% endfor %}</span>
                </div>
                <p>{{ review.comment }}</p>
                <span class="review-date"><i class="fa-regular fa-calendar"></i> {{ review.date }}</span>
                
                {% if session.get('is_admin') %}
                <form action="/delete-review/{{ review.id }}" method="POST" style="margin-top: 10px;">
                    <button type="submit" class="delete-btn"><i class="fa-solid fa-trash"></i> Usuń opinię</button>
                </form>
                {% endif %}
            </div>
            {% endfor %}
        </div>

        <div class="review-form-container">
            <h3 style="font-family: 'Playfair Display', serif; font-size: 1.5rem; margin-bottom: 20px; text-align: center;">Dodaj Swoją Opinię</h3>
            <form action="/add-review" method="POST">
                <div class="form-group">
                    <label for="name">Twoje Imię / Pseudonim</label>
                    <input type="text" id="name" name="name" required placeholder="np. Giovanni">
                </div>
                <div class="form-group">
                    <label for="rating">Ocena (w gwiazdkach)</label>
                    <select id="rating" name="rating">
                        <option value="5">★★★★★ (5/5)</option>
                        <option value="4">★★★★☆ (4/5)</option>
                        <option value="3">★★★☆☆ (3/5)</option>
                        <option value="2">★★☆☆☆ (2/5)</option>
                        <option value="1">★☆☆☆☆ (1/5)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="comment">Twoja opinia</label>
                    <textarea id="comment" name="comment" required placeholder="Napisz coś o jedzeniu..."></textarea>
                </div>
                <button type="submit" class="btn" style="width: 100%;">Opublikuj Opinię</button>
            </form>
        </div>
    </section>

    <div id="loginModal" class="modal">
        <div class="modal-content">
            <h3>Panel Właściciela</h3>
            <form action="/login" method="POST">
                <input type="password" name="password" placeholder="Hasło administratora" required>
                <button type="submit" class="btn" style="width: 100%;">Zaloguj</button>
                <button type="button" onclick="document.getElementById('loginModal').style.display='none'" style="margin-top: 10px; background: none; border: none; color: #7f8c8d; cursor: pointer;">Zamknij</button>
            </form>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 Pizzeria La Dolce Vita | Los Santos. Wszelkie prawa zastrzeżone.</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    if reviews:
        total_score = sum(r['rating'] for r in reviews)
        avg_rating = round(total_score / len(reviews), 1)
    else:
        avg_rating = 0.0

    return render_template_string(
        HTML_TEMPLATE, 
        reviews=reviews, 
        avg_rating=avg_rating,
        total_reviews=len(reviews)
    )

@app.route('/add-review', methods=['POST'])
def add_review():
    name = request.form.get('name')
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment')
    date_str = datetime.now().strftime("%d %B %Y")
    
    if name and comment:
        new_id = reviews[0]['id'] + 1 if reviews else 1
        reviews.insert(0, {"id": new_id, "name": name, "rating": rating, "comment": comment, "date": date_str})
    return redirect(url_for('index') + '#opinie')

@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if session.get('is_admin'):
        global reviews
        reviews = [r for r in reviews if r['id'] != review_id]
    return redirect(url_for('index') + '#opinie')

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == 'admin123':
        session['is_admin'] = True
    return redirect(url_for('index') + '#opinie')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index') + '#opinie')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
