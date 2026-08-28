from flask import Flask, render_template_string, request, redirect, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = 'la_dolce_vita_secret_key_997'

# TUTAJ WKLEJ SWÓJ LINK DO WEBHOOKA Z DISCORDA:
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/TWOJ_WEBHOOK_ID/TWOJ_WEBHOOK_TOKEN'

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
        :root { --primary: #c0392b; --primary-dark: #962d22; --accent: #d4ac0d; --dark: #1a1a1a; --light: #f7f4ed; --card-bg: #ffffff; --gray: #7f8c8d; }
        * { box-sizing: border-box; margin: 0; padding: 0; scroll-behavior: smooth; }
        body { font-family: 'Poppins', sans-serif; background-color: var(--light); color: var(--dark); line-height: 1.6; }
        
        header { 
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                        url('https://cdn.discordapp.com/attachments/1537171868388167901/1542652759562526872/tlo.jpg?ex=6a9202d6&is=6a90b156&hm=13681af929c503113093a010b39182c67d9fae6f0ef411c3dbbfac89df9aa1db&') no-repeat center center; 
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

        .hero-content { margin: auto; max-width: 800px; padding: 0 20px; }
        .hero-content h2 { font-family: 'Playfair Display', serif; font-size: 3.2rem; margin-bottom: 20px; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
        .hero-content p { font-size: 1.2rem; margin-bottom: 30px; color: #f0f0f0; }
        .btn { display: inline-block; background-color: var(--primary); color: white; padding: 12px 30px; border-radius: 30px; text-decoration: none; font-weight: 500; border: none; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background-color: var(--primary-dark); }
        
        section { padding: 80px 10%; background-color: var(--light); }
        .section-title { text-align: center; font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 15px; color: var(--dark); }
        .section-subtitle { text-align: center; color: var(--gray); margin-bottom: 50px; font-size: 1.1rem; }
        
        .menu-image-container { text-align: center; max-width: 700px; margin: 0 auto; background: #111; padding: 15px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .menu-image-container img { width: 100%; height: auto; border-radius: 10px; }

        .info-container { display: grid; grid-template-columns: 1fr 1fr; gap: 50px; align-items: center; background: var(--card-bg); border-radius: 15px; padding: 40px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); }
        .info-details ul { list-style: none; margin-top: 20px; }
        .info-details li { margin-bottom: 15px; display: flex; align-items: center; gap: 15px; font-size: 1.05rem; }
        .info-details li i { color: var(--primary); font-size: 1.2rem; width: 25px; }
        .map-placeholder { height: 350px; border-radius: 10px; overflow: hidden; position: relative; border: 2px solid #ddd; }
        .map-placeholder img { width: 100%; height: 100%; object-fit: cover; }

        .form-container { background: var(--card-bg); max-width: 800px; margin: 0 auto; padding: 40px; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-family: inherit; background-color: #fff; }
        .form-group textarea { resize: vertical; height: 100px; }
        
        .form-section-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; color: var(--primary); margin: 30px 0 20px 0; padding-bottom: 5px; border-bottom: 2px solid var(--primary); }

        .recruit-info-banner { background: #fdf2e9; border-left: 5px solid var(--accent); padding: 20px; border-radius: 8px; margin-bottom: 30px; font-size: 1.05rem; color: #7d6608; line-height: 1.5; }
        .recruit-info-banner i { margin-right: 8px; }

        .success-box { background: #e8f8f5; border: 2px solid #27ae60; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; }
        .success-box i { font-size: 3rem; color: #27ae60; margin-bottom: 15px; }
        .success-box h3 { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #27ae60; margin-bottom: 10px; }
        .success-box p { color: #2c3e50; font-size: 1.1rem; }

        footer { background: var(--dark); color: white; text-align: center; padding: 30px; font-size: 0.9rem; }
        @media(max-width: 768px) { .info-container { grid-template-columns: 1fr; } .nav-links { display: none; } .hero-content h2 { font-size: 2.2rem; } }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo-area">
                <img src="https://cdn.discordapp.com/attachments/1535405503109144726/1542567147803517070/ChatGPT_Image_24_sie_2026_20_20_53.png?ex=6a91b31b&is=6a90619b&hm=68b622543aeb6317230fdcb55559ffcf95d741b24ee18e1e4f2bd36475fddeaa&" alt="Logo" class="logo-img">
                <h1>La Dolce Vita</h1>
            </div>
            <ul class="nav-links">
                <li><a href="/#menu">Menu</a></li>
                <li><a href="/#lokalizacja">Lokalizacja</a></li>
                <li><a href="/rekrutacja">Rekrutacja</a></li>
            </ul>
        </nav>
        <div class="hero-content">
            {% if request.path == '/rekrutacja' %}
                <h2 style="color: var(--accent); text-transform: uppercase; letter-spacing: 2px;">Rekrutacja do Zespołu</h2>
                <p>Jesteś w oficjalnej kategorii rekrutacyjnej. Podania są sprawdzane w ciągu 48h, a wyniki pojawią się na naszym Discordzie!</p>
                <a href="/" class="btn">Wróć do strony głównej</a>
            {% else %}
                <h2>Autentyczny Smak Włoch w Sercu Los Santos</h2>
                <p>Ręcznie robiona pizza wypiekana w tradycyjnym piecu. Prawdziwe składniki i niepowtarzalny klimat.</p>
                <a href="/#menu" class="btn">Sprawdź Menu</a>
            {% endif %}
        </div>
        <div style="height: 50px;"></div>
    </header>

    {% if request.path == '/rekrutacja' %}
    <section>
        <h2 class="section-title">Formularz Rekrutacyjny</h2>
        <p class="section-subtitle">Dołącz do zespołu La Dolce Vita i twórz z nami klimatyczne RP w Los Santos!</p>
        
        <div class="form-container">
            <div class="recruit-info-banner">
                <i class="fa-solid fa-circle-info"></i> <strong>Ważne informacje:</strong> Wszystkie nadesłane podania trafiają bezpośrednio do zarządu na Discordzie i są sprawdzane w ciągu <strong>48 godzin</strong>.
            </div>

            {% if success %}
            <div class="success-box">
                <i class="fa-solid fa-circle-check"></i>
                <h3>Sukces!</h3>
                <p>Podanie zostało wysłane pomyślnie na Discorda La Dolce Vita. Oczekuj na wynik!</p>
                <a href="/rekrutacja" class="btn" style="margin-top: 20px;">Wyślij kolejne podanie</a>
            </div>
            {% else %}
            <form action="/submit-application" method="POST">
                
                <div class="form-section-title">--- INFORMACJE OOC ---</div>
                
                <div class="form-group">
                    <label>Nick na Discord</label>
                    <input type="text" name="ooc_discord_nick" required placeholder="np. nick_discord">
                </div>
                <div class="form-group">
                    <label>Discord ID</label>
                    <input type="text" name="ooc_discord_id" required placeholder="np. 123456789012345678">
                </div>
                <div class="form-group">
                    <label>Wiek</label>
                    <input type="text" name="ooc_age" required placeholder="Twój wiek rzeczywisty">
                </div>
                <div class="form-group">
                    <label>Doświadczenie w Roleplay (gdzie i ile grałeś/aś)</label>
                    <textarea name="ooc_experience" required placeholder="Opisz swoje doświadczenie..."></textarea>
                </div>
                <div class="form-group">
                    <label>Czas na grę (ile h tygodniowo)</label>
                    <input type="text" name="ooc_time" required placeholder="np. 15-20h">
                </div>
                <div class="form-group">
                    <label>Znajomość regulaminu (0/10)</label>
                    <input type="text" name="ooc_rules" required placeholder="np. 9/10">
                </div>

                <div class="form-section-title">--- INFORMACJE IC ---</div>

                <div class="form-group">
                    <label>Imię i Nazwisko postaci</label>
                    <input type="text" name="ic_name" required placeholder="np. Giovanni Rossi">
                </div>
                <div class="form-group">
                    <label>Wiek postaci</label>
                    <input type="text" name="ic_age" required placeholder="np. 28 lat">
                </div>
                <div class="form-group">
                    <label>Numer telefonu</label>
                    <input type="text" name="ic_phone" required placeholder="np. 555-1234">
                </div>
                <div class="form-group">
                    <label>Doświadczenie</label>
                    <input type="text" name="ic_exp" required placeholder="Poprzednie miejsca pracy itp.">
                </div>
                <div class="form-group">
                    <label>Krótki opis postaci (cechy, historia)</label>
                    <textarea name="ic_desc" required placeholder="Opisz swoją postać..."></textarea>
                </div>
                <div class="form-group">
                    <label>Dlaczego akurat nasza restauracja?</label>
                    <textarea name="ic_why" required placeholder="Powód wyboru La Dolce Vita..."></textarea>
                </div>
                <div class="form-group">
                    <label>Sytuacja RP: Klient zaczyna robić awanturę i rzucać jedzeniem. Jak reaguje Twoja postać? (Opisz działania)</label>
                    <textarea name="ic_situation" required placeholder="Opisz reakcję postaci krok po kroku..."></textarea>
                </div>

                <button type="submit" class="btn" style="width: 100%; margin-top: 20px;">Wyślij Podanie</button>
            </form>
            {% endif %}
        </div>
    </section>
    {% else %}
    <section id="menu">
        <h2 class="section-title">Nasze Menu</h2>
        <p class="section-subtitle">Oficjalne ceny i specjały La Dolce Vita</p>
        <div class="menu-image-container">
            <img src="https://cdn.discordapp.com/attachments/1541512104614432842/1542502122577338479/content.png?ex=6a91768c&is=6a90250c&hm=d2992a0c9c509993a2af231ef6d37a93002ad46d2c982d02b3d953c77f927148&" alt="Menu La Dolce Vita">
        </div>
    </section>

    <section id="lokalizacja">
        <h2 class="section-title">Gdzie Nas Znajdziesz?</h2>
        <p class="section-subtitle">Odwiedź nasz lokal w dzielnicy Del Perro / plaża w Los Santos</p>
        <div class="info-container">
            <div class="info-details">
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 15px;">La Dolce Vita Los Santos</h3>
                <p>Nasz lokal znajduje się w świetnej lokalizacji niedaleko wybrzeża i molo w zachodnim Los Santos.</p>
                <ul>
                    <li><i class="fa-solid fa-location-dot"></i> <span>Del Perro / Plaża, Los Santos</span></li>
                    <li><i class="fa-solid fa-clock"></i> <span>Czynne: Całodobowo (24/7)</span></li>
                </ul>
            </div>
            <div class="map-placeholder">
                <img src="https://cdn.discordapp.com/attachments/1541512104614432843/1542488327561683005/36873c94-a767-4e1c-9b13-fcc21fe45e01.png?ex=6a9169b3&is=6a901833&hm=2edb247931893c6f341e1852a86d8cabf2aa96c8596d452844956750ca9eff2b&" alt="Mapa Los Santos">
            </div>
        </div>
    </section>
    {% endif %}

    <footer>
        <p>&copy; 2026 Pizzeria La Dolce Vita | Los Santos. Wszelkie prawa zastrzeżone.</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/rekrutacja')
def rekrutacja():
    success = request.args.get('success') == 'true'
    return render_template_string(HTML_TEMPLATE, success=success)

@app.route('/submit-application', methods=['POST'])
def submit_application():
    # Pobieramy dane z formularza
    discord_nick = request.form.get('ooc_discord_nick')
    discord_id = request.form.get('ooc_discord_id')
    ooc_age = request.form.get('ooc_age')
    ooc_exp = request.form.get('ooc_experience')
    ooc_time = request.form.get('ooc_time')
    ooc_rules = request.form.get('ooc_rules')
    
    ic_name = request.form.get('ic_name')
    ic_age = request.form.get('ic_age')
    ic_phone = request.form.get('ic_phone')
    ic_exp = request.form.get('ic_exp')
    ic_desc = request.form.get('ic_desc')
    ic_why = request.form.get('ic_why')
    ic_situation = request.form.get('ic_situation')

    # Treść wiadomości wysyłana na Discorda
    discord_message = {
        "content": "🚨 **Nowe podanie do La Dolce Vita!** 🚨",
        "embeds": [
            {
                "title": f"Postać IC: {ic_name}",
                "color": 12632256,
                "fields": [
                    {"name": "👤 OOC Discord", "value": f"{discord_nick} (ID: `{discord_id}`)", "inline": True},
                    {"name": "📅 OOC Wiek", "value": ooc_age, "inline": True},
                    {"name": "⏰ Czas na grę", "value": ooc_time, "inline": True},
                    {"name": "📖 Regulamin", "value": ooc_rules, "inline": True},
                    {"name": "💼 Doświadczenie OOC", "value": ooc_exp, "inline": False},
                    {"name": "📝 IC (Wiek / Tel)", "value": f"Wiek: {ic_age} | Tel: {ic_phone}", "inline": False},
                    {"name": "💡 Poprzednie doświadczenie IC", "value": ic_exp, "inline": False},
                    {"name": "👤 Opis postaci", "value": ic_desc, "inline": False},
                    {"name": "❓ Dlaczego my?", "value": ic_why, "inline": False},
                    {"name": "🎬 Sytuacja RP", "value": ic_situation, "inline": False}
                ]
            }
        ]
    }

    # Wysłanie powiadomienia na Twój kanał Discord przez Webhook
    if https://discord.com/api/webhooks/1543037930187006023/z2YORxjAm0lCune1Iu2RoJXyXC4Pc9xVTfbtlZqZzUKsThHz9wryR2YnWghQwueJQEWH != 'https://discord.com/api/webhooks/TWOJ_WEBHOOK_ID/TWOJ_WEBHOOK_TOKEN':
        try:
            requests.post(https://discord.com/api/webhooks/1543037930187006023/z2YORxjAm0lCune1Iu2RoJXyXC4Pc9xVTfbtlZqZzUKsThHz9wryR2YnWghQwueJQEWH, json=discord_message)
        except Exception as e:
            print(f"Błąd wysyłania na Discorda: {e}")

    return redirect(url_for('rekrutacja', success='true'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
