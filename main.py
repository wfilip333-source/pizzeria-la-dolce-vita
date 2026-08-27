from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

reviews = [
    {
        "name": "Marco V.",
        "rating": 5,
        "comment": "Najlepsza pizza w całym Los Santos! Prawdziwe włoskie ciasto, a nie jakaś tektura z Cluckin' Bell. Polecam każdemu z Mirror Park!",
        "date": "25 lutego 2026"
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Dolce Vita | Pizzeria & Trattoria - Los Santos</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #c0392b; --primary-dark: #962d22; --accent: #d4ac0d; --dark: #1a1a1a; --light: #fdfbf7; --gray: #7f8c8d; }
        * { box-sizing: border-box; margin: 0; padding: 0; scroll-behavior: smooth; }
        body { font-family: 'Poppins', sans-serif; background-color: var(--light); color: var(--dark); line-height: 1.6; }
        header { background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1920&q=80') no-repeat center center/cover; color: white; min-height: 90vh; display: flex; flex-direction: column; justify-content: space-between; text-align: center; position: relative; }
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 8%; background: rgba(0,0,0,0.4); backdrop-filter: blur(5px); position: fixed; width: 100%; top: 0; z-index: 1000; }
        .logo-area { display: flex; align-items: center; gap: 12px; }
        .logo-area i { font-size: 2rem; color: var(--accent); }
        .logo-area h1 { font-family: 'Playfair Display', serif; font-size: 1.6rem; color: white; }
        .nav-links { list-style: none; display: flex; gap: 30px; }
        .nav-links a { color: white; text-decoration: none; transition: color 0.3s; }
        .nav-links a:hover { color: var(--accent); }
        .hero-content { margin: auto; max-width: 800px; padding: 0 20px; }
        .hero-content h2 { font-family: 'Playfair Display', serif; font-size: 3.5rem; margin-bottom: 20px; color: #fff; }
        .hero-content p { font-size: 1.2rem; margin-bottom: 30px; color: #ddd; }
        .btn { display: inline-block; background-color: var(--primary); color: white; padding: 12px 30px; border-radius: 30px; text-decoration: none; font-weight: 500; border: none; cursor: pointer; }
        .btn:hover { background-color: var(--primary-dark); }
        section { padding: 80px 10%; }
        .section-title { text-align: center; font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 15px; color: var(--dark); }
        .section-subtitle { text-align: center; color: var(--gray); margin-bottom: 50px; font-size: 1.1rem; }
        .menu-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
        .menu-item { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        .menu-img { height: 200px; width: 100%; object-fit: cover; }
        .menu-details { padding: 20px; }
        .menu-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .menu-header h3 { font-family: 'Playfair Display', serif; font-size: 1.3rem; }
        .price { color: var(--primary); font-weight: 600; font-size: 1.1rem; }
        .menu-details p { color: var(--gray); font-size: 0.9rem; }
        .info-container { display: grid; grid-template-columns: 1fr 1fr; gap: 50px; align-items: center; background: white; border-radius: 15px; padding: 40px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); }
        .info-details ul { list-style: none; margin-top: 20px; }
        .info-details li { margin-bottom: 15px; display: flex; align-items: center; gap: 15px; font-size: 1.05rem; }
        .info-details li i { color: var(--primary); font-size: 1.2rem; width: 25px; }
        .map-placeholder { background: #e5e3df; height: 350px; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; position: relative; overflow: hidden; border: 2px solid #ddd; }
        .map-placeholder img { width: 100%; height: 100%; object-fit: cover; opacity: 0.8; }
        .map-overlay-text { position: absolute; background: rgba(0,0,0,0.7); color: white; padding: 10px 20px; border-radius: 5px; font-weight: 500; }
        .reviews-section { background-color: #f7f4ed; }
        .reviews-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin-bottom: 50px; }
        .review-card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.03); }
        .review-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .review-author { font-weight: 600; }
        .stars { color: var(--accent); }
        .review-date { font-size: 0.8rem; color: var(--gray); margin-top: 10px; display: block; }
        .review-form-container { background: white; max-width: 700px; margin: 0 auto; padding: 40px; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-family: inherit; }
        .form-group textarea { resize: vertical; height: 120px; }
        footer { background: var(--dark); color: white; text-align: center; padding: 30px; font-size: 0.9rem; }
        @media(max-width: 768px) { .info-container { grid-template-columns: 1fr; } .nav-links { display: none; } .hero-content h2 { font-size: 2.5rem; } }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo-area">
                <i class="fa-solid fa-pizza-slice"></i>
                <h1>La Dolce Vita</h1>
            </div>
            <ul class="nav-links">
                <li><a href="#menu">Menu</a></li>
                <li><a href="#lokalizacja">Lokalizacja</a></li>
                <li><a href="#opinie">Opinie</a></li>
            </ul>
        </nav>
        <div class="hero-content">
            <h2>Autentyczny Smak Włoch w Sercu Los Santos</h2>
            <p>Ręcznie robiona pizza wypiekana w tradycyjnym piecu opalanym drewnem. Prawdziwe składniki, niepowtarzalny klimat.</p>
            <a href="#menu" class="btn">Sprawdź Menu</a>
        </div>
        <div style="height: 50px;"></div>
    </header>

    <section id="menu">
        <h2 class="section-title">Nasze Menu</h2>
        <p class="section-subtitle">Wybierz coś dla siebie – na miejscu lub z dostawą pod drzwi</p>
        <div class="menu-grid">
            <div class="menu-item">
                <img src="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80" alt="Margherita" class="menu-img">
                <div class="menu-details">
                    <div class="menu-header"><h3>Margherita Tradizionale</h3><span class="price">$24</span></div>
                    <p>Świeży sos pomidorowy San Marzano, mozzarella fior di latte, świeża bazylia i oliwa extra virgin.</p>
                </div>
            </div>
            <div class="menu-item">
                <img src="https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=600&q=80" alt="Diavola" class="menu-img">
                <div class="menu-details">
                    <div class="menu-header"><h3>Diavola Piccante</h3><span class="price">$29</span></div>
                    <p>Sos pomidorowy, mozzarella, pikantna włoska spianata calabra, jalapeño i miód akacjowy.</p>
                </div>
            </div>
            <div class="menu-item">
                <img src="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80" alt="Quattro Formaggi" class="menu-img">
                <div class="menu-details">
                    <div class="menu-header"><h3>Quattro Formaggi</h3><span class="price">$32</span></div>
                    <p>Biały sos śmietanowy, mozzarella, gorgonzola, ser wędzony scamorza oraz parmezan D.O.P.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="lokalizacja">
        <h2 class="section-title">Gdzie Nas Znajdziesz?</h2>
        <p class="section-subtitle">Odwiedź nasz lokal lub zamów dowóz na terenie całego miasta</p>
        <div class="info-container">
            <div class="info-details">
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 15px;">La Dolce Vita Los Santos</h3>
                <p>Nasz lokal mieści się w spokojnej, malowniczej okolicy Mirror Park, niedaleko jeziora. Czekamy na Ciebie z rozpalonym piecem!</p>
                <ul>
                    <li><i class="fa-solid fa-location-dot"></i> <span>Mirror Park Blvd, Los Santos</span></li>
                    <li><i class="fa-solid fa-clock"></i> <span>Codziennie: 12:00 – 00:00</span></li>
                    <li><i class="fa-solid fa-phone"></i> <span>Tel: 555-DOLCE-VITA</span></li>
                </ul>
            </div>
            <div class="map-placeholder">
                <img src="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=800&q=80" alt="Mapa">
                <div class="map-overlay-text"><i class="fa-solid fa-map-pin"></i> Mirror Park, Los Santos</div>
            </div>
        </div>
    </section>

    <section id="opinie" class="reviews-section">
        <h2 class="section-title">Opinie Klientów</h2>
        <p class="section-subtitle">Zobacz, co mówią o nas mieszkańcy Los Santos, lub zostaw swoją opinię!</p>
        <div class="reviews-grid">
            {% for review in reviews %}
            <div class="review-card">
                <div class="review-header">
                    <span class="review-author">{{ review.name }}</span>
                    <span class="stars">{% for i in range(review.rating) %}★{% endfor %}</span>
                </div>
                <p>{{ review.comment }}</p>
                <span class="review-date"><i class="fa-regular fa-calendar"></i> {{ review.date }}</span>
            </div>
            {% endfor %}
        </div>
        <div class="review-form-container">
            <h3 style="font-family: 'Playfair Display', serif; font-size: 1.5rem; margin-bottom: 20px; text-align: center;">Dodaj Swoją Opinię</h3>
            <form action="/add-review" method="POST">
                <div class="form-group">
                    <label for="name">Twoje Imię i Nazwisko / Pseudonim</label>
                    <input type="text" id="name" name="name" required placeholder="np. Giovanni Rossi">
                </div>
                <div class="form-group">
                    <label for="rating">Ocena</label>
                    <select id="rating" name="rating">
                        <option value="5">★★★★★ (5/5 - Rewelacja)</option>
                        <option value="4">★★★★☆ (4/5 - Bardzo dobrze)</option>
                        <option value="3">★★★☆☆ (3/5 - Średnio)</option>
                        <option value="2">★★☆☆☆ (2/5 - Słabo)</option>
                        <option value="1">★☆☆☆☆ (1/5 - Tragedia)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="comment">Twoja opinia</label>
                    <textarea id="comment" name="comment" required placeholder="Napisz, co sądzisz o naszym jedzeniu..."></textarea>
                </div>
                <button type="submit" class="btn" style="width: 100%;">Opublikuj Opinię</button>
            </form>
        </div>
    </section>

    <footer>
        <p>&copy; 2026 Pizzeria La Dolce Vita | Los Santos. Wszelkie prawa zastrzeżone.</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, reviews=reviews)

@app.route('/add-review', methods=['POST'])
def add_review():
    name = request.form.get('name')
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment')
    date_str = datetime.now().strftime("%d %B %Y")
    if name and comment:
        reviews.insert(0, {"name": name, "rating": rating, "comment": comment, "date": date_str})
    return redirect(url_for('index') + '#opinie')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)