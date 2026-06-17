#!/usr/bin/env python3
"""
LinguaBattle SEO sayfa üreticisi.
content/*.json  ->  her dil için tam SEO'lu statik HTML (JS render YOK).
Ayrıca sitemap.xml + robots.txt üretir.

Kullanım:  python3 scripts/build_seo_pages.py
"""
import json, os, glob, html

SITE = "https://linguabattle.net"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

LANGS = ["tr", "en", "de", "fr", "es", "ar", "hi", "ru", "pt", "ja"]
RTL = {"ar"}

# Builder dışında üretilen statik sayfalar (seviye testi — build_level_test.py).
# Sitemap'e dahil edilir. Slug'lar build_level_test.py'deki SLUG ile aynı olmalı.
EXTRA_PAGES = [
    "/tr/seviye-testi", "/en/english-level-test", "/de/englisch-niveau-test",
    "/fr/test-de-niveau-anglais", "/es/test-de-nivel-ingles", "/ar/ikhtibar-mustawa",
    "/hi/angrezi-level-test", "/ru/test-urovnya", "/pt/teste-de-nivel-ingles",
    "/ja/eigo-level-test",
]
# Seviye testi yol+banner metni (build_level_test.py SLUG ile senkron)
TEST_SLUG = {"tr":"seviye-testi","en":"english-level-test","de":"englisch-niveau-test",
    "fr":"test-de-niveau-anglais","es":"test-de-nivel-ingles","ar":"ikhtibar-mustawa",
    "hi":"angrezi-level-test","ru":"test-urovnya","pt":"teste-de-nivel-ingles","ja":"eigo-level-test"}
TEST_BANNER = {
 "tr":("📊 İngilizce Seviye Testi","20 soruda seviyeni öğren — ücretsiz, kayıt yok.","Teste başla →"),
 "en":("📊 English Level Test","Find your level in 20 questions — free, no signup.","Start the test →"),
 "de":("📊 Englisch Niveau-Test","Finde dein Niveau in 20 Fragen — kostenlos, ohne Anmeldung.","Test starten →"),
 "fr":("📊 Test de Niveau d'Anglais","Trouve ton niveau en 20 questions — gratuit, sans inscription.","Commencer →"),
 "es":("📊 Test de Nivel de Inglés","Descubre tu nivel en 20 preguntas — gratis, sin registro.","Empezar →"),
 "ar":("📊 اختبار مستوى الإنجليزية","اعرف مستواك في 20 سؤالًا — مجاني، بدون تسجيل.","ابدأ الاختبار →"),
 "hi":("📊 अंग्रेज़ी लेवल टेस्ट","20 सवालों में अपना स्तर जानें — मुफ़्त, बिना रजिस्ट्रेशन।","टेस्ट शुरू करें →"),
 "ru":("📊 Тест на уровень английского","Узнай свой уровень за 20 вопросов — бесплатно, без регистрации.","Начать тест →"),
 "pt":("📊 Teste de Nível de Inglês","Descubra seu nível em 20 perguntas — grátis, sem cadastro.","Começar →"),
 "ja":("📊 英語レベルテスト","20問でレベルを判定 — 無料・登録不要。","テストを始める →"),
}

# Dile çevrili yol segmenti (URL): /tr/kelime/get , /de/wort/get ...
SEG = {"tr":"kelime","en":"word","de":"wort","fr":"mot","es":"palabra",
       "ar":"kalima","hi":"shabd","ru":"slovo","pt":"palavra","ja":"tango"}

LANG_LABEL = {"tr":"🇹🇷 Türkçe","en":"🇬🇧 English","de":"🇩🇪 Deutsch","fr":"🇫🇷 Français",
  "es":"🇪🇸 Español","ar":"🇸🇦 العربية","hi":"🇮🇳 हिन्दी","ru":"🇷🇺 Русский","pt":"🇵🇹 Português","ja":"🇯🇵 日本語"}

# Lokalize UI metinleri
UI = {
 "tr":{"home":"Ana sayfa","words":"Kelimeler","meanings":"Anlamları","conj":"Çekimler","listen":"dinle",
   "appTitle":"Pratik yap, unutma","appDesc":"Öğrendiğin kelimeyi düelloda pekiştir.",
   "dl":"Google Play'den indir","dlAlt":"App Store'dan indir",
   "duel":"Günde 5 dakika <b>kelime düellosu</b> — rakibinle yarış, kelimeleri kalıcı kıl.",
   "pres":"Şimdiki","past":"Geçmiş","pp":"Past Participle"},
 "en":{"home":"Home","words":"Words","meanings":"Meanings","conj":"Forms","listen":"listen",
   "appTitle":"Practice & remember","appDesc":"Lock in the word with a quick duel.",
   "dl":"Get it on Google Play","dlAlt":"Download on the App Store",
   "duel":"5 minutes a day of <b>word duels</b> — race an opponent, make words stick.",
   "pres":"Present","past":"Past","pp":"Past Participle"},
 "de":{"home":"Start","words":"Wörter","meanings":"Bedeutungen","conj":"Formen","listen":"anhören",
   "appTitle":"Üben & merken","appDesc":"Festige das Wort mit einem Duell.",
   "dl":"Bei Google Play","dlAlt":"Im App Store laden",
   "duel":"5 Minuten täglich <b>Wort-Duelle</b> — tritt gegen Gegner an.",
   "pres":"Präsens","past":"Präteritum","pp":"Partizip II"},
 "fr":{"home":"Accueil","words":"Mots","meanings":"Significations","conj":"Formes","listen":"écouter",
   "appTitle":"Pratique & mémorise","appDesc":"Ancre le mot avec un duel rapide.",
   "dl":"Sur Google Play","dlAlt":"Sur l'App Store",
   "duel":"5 min/jour de <b>duels de mots</b> — affronte un adversaire.",
   "pres":"Présent","past":"Passé","pp":"Participe passé"},
 "es":{"home":"Inicio","words":"Palabras","meanings":"Significados","conj":"Formas","listen":"escuchar",
   "appTitle":"Practica y recuerda","appDesc":"Fija la palabra con un duelo.",
   "dl":"En Google Play","dlAlt":"En el App Store",
   "duel":"5 min al día de <b>duelos de palabras</b> — compite con un rival.",
   "pres":"Presente","past":"Pasado","pp":"Participio"},
 "ar":{"home":"الرئيسية","words":"كلمات","meanings":"المعاني","conj":"التصريفات","listen":"استمع",
   "appTitle":"تدرّب وتذكّر","appDesc":"ثبّت الكلمة بمبارزة سريعة.",
   "dl":"من Google Play","dlAlt":"من App Store",
   "duel":"5 دقائق يوميًا من <b>مبارزات الكلمات</b> — تنافس مع خصم.",
   "pres":"المضارع","past":"الماضي","pp":"التصريف الثالث"},
 "hi":{"home":"होम","words":"शब्द","meanings":"अर्थ","conj":"रूप","listen":"सुनें",
   "appTitle":"अभ्यास करें और याद रखें","appDesc":"डुएल से शब्द पक्का करें।",
   "dl":"Google Play पर पाएं","dlAlt":"App Store पर पाएं",
   "duel":"रोज़ 5 मिनट <b>शब्द डुएल</b> — प्रतिद्वंद्वी से मुकाबला करें।",
   "pres":"वर्तमान","past":"भूत","pp":"तृतीय रूप"},
 "ru":{"home":"Главная","words":"Слова","meanings":"Значения","conj":"Формы","listen":"слушать",
   "appTitle":"Практика и запоминание","appDesc":"Закрепи слово в дуэли.",
   "dl":"В Google Play","dlAlt":"В App Store",
   "duel":"5 минут в день <b>дуэлей слов</b> — сразись с соперником.",
   "pres":"Настоящее","past":"Прошедшее","pp":"Причастие"},
 "pt":{"home":"Início","words":"Palavras","meanings":"Significados","conj":"Formas","listen":"ouvir",
   "appTitle":"Pratique e lembre","appDesc":"Fixe a palavra com um duelo.",
   "dl":"No Google Play","dlAlt":"Na App Store",
   "duel":"5 min por dia de <b>duelos de palavras</b> — desafie um oponente.",
   "pres":"Presente","past":"Passado","pp":"Particípio"},
 "ja":{"home":"ホーム","words":"単語","meanings":"意味","conj":"活用","listen":"聞く",
   "appTitle":"練習して覚える","appDesc":"デュエルで単語を定着。",
   "dl":"Google Playで入手","dlAlt":"App Storeで入手",
   "duel":"1日5分の<b>単語デュエル</b> — 相手と競争。",
   "pres":"現在","past":"過去","pp":"過去分詞"},
}

PLAY = "https://play.google.com/store/apps/details?id=com.linguabattle.app"
APPSTORE = "https://apps.apple.com/app/id6761505565"

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Be Vietnam Pro',-apple-system,sans-serif;background:#000E23;color:#D9E6FF;line-height:1.6}
h1,h2,h3,.head{font-family:'Plus Jakarta Sans',sans-serif}
a{color:#81ECFF;text-decoration:none}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;padding:14px 24px;background:rgba(0,14,35,.85);backdrop-filter:blur(12px);border-bottom:1px solid #384962}
.logo{display:flex;align-items:center;gap:9px;font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.15rem;background:linear-gradient(90deg,#A3FE00,#00E3FD);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo img{height:30px;width:auto;display:block;filter:invert(1) brightness(1.6)}
select{background:#04203E;color:#D9E6FF;border:1px solid #384962;border-radius:8px;padding:7px 10px;font-family:inherit;font-size:.85rem;cursor:pointer}
.layout{max-width:1080px;margin:0 auto;padding:32px 24px;display:grid;grid-template-columns:1fr 300px;gap:32px;align-items:start}
@media(max-width:860px){.layout{grid-template-columns:1fr;gap:24px}}
.content{min-width:0}
.crumb{font-size:.8rem;color:#9BACCA;margin-bottom:14px}
h1{font-size:2.3rem;font-weight:800;line-height:1.15;margin-bottom:6px}
h1 .word{background:linear-gradient(90deg,#A3FE00,#00E3FD);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.pron{display:flex;gap:12px;align-items:center;color:#9BACCA;font-size:.95rem;margin-bottom:18px;flex-wrap:wrap}
.tag{background:#072647;border:1px solid #384962;border-radius:20px;padding:3px 12px;font-size:.78rem}
.speak{background:#04203E;border:1px solid #00E3FD;color:#81ECFF;border-radius:20px;padding:4px 13px;font-size:.8rem;cursor:pointer}
.lede{font-size:1.05rem;color:#9BACCA;margin-bottom:28px;padding-bottom:24px;border-bottom:1px solid #384962}
.sec{margin-bottom:30px}
.sec h2{font-size:1.25rem;font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.mean{background:#011A36;border:1px solid #384962;border-radius:14px;padding:16px 18px;margin-bottom:12px}
.mean .n{display:inline-block;min-width:24px;height:24px;line-height:24px;text-align:center;border-radius:7px;background:#A3FE00;color:#3F6600;font-weight:700;font-size:.8rem;margin-right:8px}
.mean .def{font-weight:600;color:#D9E6FF;font-size:1.02rem}
.mean .ex{margin-top:8px;padding-left:32px;color:#9BACCA}
.mean .ex .en{color:#DDFFAF;font-style:italic}
table{width:100%;border-collapse:collapse;background:#011A36;border:1px solid #384962;border-radius:14px;overflow:hidden}
th,td{padding:11px 14px;text-align:left;border-bottom:1px solid #384962;font-size:.95rem}
th{background:#072647;font-family:'Plus Jakarta Sans';font-weight:600;color:#81ECFF}
tr:last-child td{border-bottom:none}
.warn{color:#FD8B00}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chip{background:#04203E;border:1px solid #384962;border-radius:10px;padding:9px 14px;font-size:.9rem}
.chip:hover{border-color:#A3FE00;color:#DDFFAF}
.quiz{background:#011A36;border:1px solid #00E3FD;border-radius:14px;padding:18px}
.quiz .q{font-weight:600;margin-bottom:12px}
.quiz button{display:block;width:100%;text-align:left;background:#04203E;border:1px solid #384962;color:#D9E6FF;border-radius:9px;padding:11px 14px;margin-bottom:8px;font-family:inherit;font-size:.92rem;cursor:pointer}
.quiz button:hover{border-color:#00E3FD}
.quiz button.ok{background:rgba(163,254,0,.15);border-color:#A3FE00;color:#DDFFAF}
.quiz button.no{background:rgba(255,113,108,.12);border-color:#FF716C;color:#FF716C}
.appcol{position:sticky;top:80px}
@media(max-width:860px){.appcol{position:static}}
.appcard{background:linear-gradient(160deg,#04203E,#011A36);border:1px solid #384962;border-radius:18px;padding:22px;text-align:center}
.appcard .badge{font-size:2.4rem}
.appcard h3{font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.15rem;margin:10px 0 4px}
.appcard p{color:#9BACCA;font-size:.88rem;margin-bottom:16px}
.store{display:block;background:#A3FE00;color:#3F6600;font-weight:700;font-family:'Plus Jakarta Sans';border-radius:11px;padding:12px;margin-bottom:9px;box-shadow:0 0 24px rgba(163,254,0,.28)}
.store.alt{background:#072647;color:#D9E6FF;box-shadow:none;border:1px solid #384962}
.duel{margin-top:16px;padding-top:16px;border-top:1px solid #384962;font-size:.82rem;color:#9BACCA}
.duel b{color:#81ECFF}
footer{max-width:1080px;margin:0 auto;padding:32px 24px;border-top:1px solid #384962;color:#9BACCA;font-size:.82rem}"""

def esc(s): return html.escape(str(s), quote=True)

import re
def slugify(word):
    # "brain rot" -> "brain-rot", "a / an / the" -> "a-an-the"
    # (URL/dosya adı için; görünen 'word' değişmez)
    s = word.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)   # harf/rakam dışını tire yap
    return s.strip("-")                  # baş/sondaki tireleri at

def url_for(lang, word):
    return f"{SITE}/{lang}/{SEG[lang]}/{slugify(word)}"

def lang_switcher(word, cur):
    opts = []
    for l in LANGS:
        sel = " selected" if l == cur else ""
        opts.append(f'<option value="{url_for(l, word)}"{sel}>{LANG_LABEL[l]}</option>')
    return ('<select onchange="location.href=this.value">' + "".join(opts) + '</select>')

def build_page(word, pron, conj, lang, d):
    ui = UI[lang]
    rtl = lang in RTL
    dir_attr = "rtl" if rtl else "ltr"

    # hreflang + canonical
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{url_for(l, word)}">' for l in LANGS
    )
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{url_for("en", word)}">'

    # meanings
    means = ""
    for i, m in enumerate(d["means"], 1):
        means += (f'<div class="mean"><span class="n">{i}</span>'
                  f'<span class="def">{esc(m["def"])}</span>'
                  f'<div class="ex"><span class="en">"{esc(m["en"])}"</span> — {esc(m["t"])}</div></div>')

    # conjugation table (varsa)
    conj_html = ""
    if conj:
        conj_html = (f'<div class="sec"><h2>⚠️ <span class="warn">{ui["conj"]}</span></h2>'
                     f'<table><tr><th>{ui["pres"]}</th><th>{ui["past"]}</th><th>{ui["pp"]}</th></tr>'
                     f'<tr><td>{esc(conj[0])}</td><td>{esc(conj[1])}</td><td>{esc(conj[2])}</td></tr></table></div>')

    rel = "".join(f'<a class="chip">{esc(r)} →</a>' for r in d["rel"])
    idioms = "".join(f'<span class="chip">{esc(r)}</span>' for r in d["idioms"])
    quizbtns = "".join(
        f'<button onclick="ans(this,{str(i==d["quizOk"]).lower()})">{esc(a)}</button>'
        for i, a in enumerate(d["quizA"])
    )

    # JSON-LD structured data
    ld = {
        "@context":"https://schema.org","@type":"DefinedTerm",
        "name": word,"description": d["means"][0]["def"],
        "inDefinedTermSet": f"{SITE}/{lang}/",
        "url": url_for(lang, word)
    }
    faq = {
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name": d["title"],
            "acceptedAnswer":{"@type":"Answer","text": d["means"][0]["def"]}}]
    }
    ld_json = json.dumps(ld, ensure_ascii=False)
    faq_json = json.dumps(faq, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{dir_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(d["title"])} | LinguaBattle</title>
<meta name="description" content="{esc(d["metaDesc"])}">
<link rel="canonical" href="{url_for(lang, word)}">
{alts}
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(d["title"])}">
<meta property="og:description" content="{esc(d["metaDesc"])}">
<meta property="og:url" content="{url_for(lang, word)}">
<meta property="og:site_name" content="LinguaBattle">
<meta property="og:image" content="{SITE}/assets/logo-icon.png">
<meta name="twitter:card" content="summary">
<meta name="twitter:image" content="{SITE}/assets/logo-icon.png">
<link rel="icon" type="image/png" href="/assets/logo-icon.png">
<link rel="apple-touch-icon" href="/assets/logo-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{ld_json}</script>
<script type="application/ld+json">{faq_json}</script>
</head>
<body>
<div class="topbar">
  <a class="logo" href="/{lang}/"><img src="/assets/logo.svg" alt="LinguaBattle" width="30" height="30"><span>LinguaBattle</span></a>
  {lang_switcher(word, lang)}
</div>
<div class="layout">
  <main class="content">
    <nav class="crumb"><a href="/{lang}/">{ui["home"]}</a> › {ui["words"]} › {esc(word)}</nav>
    <h1><span class="word">{esc(word)}</span></h1>
    <div class="pron"><span class="tag">{esc(d["pos"])}</span><span>{esc(pron)}</span>
      <span class="speak" onclick="speak('{esc(word)}')">🔊 {ui["listen"]}</span></div>
    <p class="lede">{d["lede"]}</p>
    <section class="sec"><h2>📖 {ui["meanings"]}</h2>{means}</section>
    {conj_html}
    <section class="sec"><h2>🔄 {esc(d["relTitle"])}</h2><div class="chips">{rel}</div></section>
    <section class="sec"><h2>💬 {esc(d["idiomTitle"])}</h2><div class="chips">{idioms}</div></section>
    <section class="sec"><div class="quiz"><div class="q">❓ {esc(d["quizQ"])}</div>{quizbtns}</div></section>
  </main>
  <aside class="appcol">
    <div class="appcard"><div class="badge">⚔️</div>
      <h3>{ui["appTitle"]}</h3><p>{esc(ui["appDesc"])}</p>
      <a class="store" href="{PLAY}">▶ {ui["dl"]}</a>
      <a class="store alt" href="{APPSTORE}"> {ui["dlAlt"]}</a>
      <div class="duel">{ui["duel"]}</div></div>
  </aside>
</div>
<footer>© 2026 LinguaBattle · {esc(word)} · {lang}</footer>
<script>
function ans(b,ok){{b.className=ok?'ok':'no';}}
function speak(t){{if('speechSynthesis'in window){{var u=new SpeechSynthesisUtterance(t);u.lang='en-US';speechSynthesis.speak(u);}}}}
</script>
</body>
</html>"""

# Dil ana sayfası metinleri (her dil için)
HOME = {
 "tr":{"title":"LinguaBattle — İngilizce Kelime Anlamları ve Örnekler","metaDesc":"İngilizcenin en çok karıştırılan kelimeleri: anlamları, örnek cümleler ve fiil çekimleri. get, exit, embarrassed ve yüzlerce kelime — sonra uygulamada düelloyla pekiştir.","tagline":"İngilizcenin en çok <span class='g'>karıştırılan</span> kelimeleri","sub":"Her kelimenin gerçek anlamını, örnek cümlelerini ve çekimlerini öğren. Sonra uygulamada düelloyla pekiştir.","search":"🔍 Bir kelime ara…","popular":"Kelimeler","all":"Tüm konular"},
 "en":{"title":"LinguaBattle — English Word Meanings & Examples","metaDesc":"The most confusing English words explained: meanings, example sentences and verb forms. get, exit, embarrassed and hundreds more — then lock them in with a duel in the app.","tagline":"The most <span class='g'>confusing</span> English words","sub":"Learn each word's real meaning, example sentences and forms. Then lock them in with a duel in the app.","search":"🔍 Search a word…","popular":"Words","all":"All topics"},
 "de":{"title":"LinguaBattle — Englische Wörter: Bedeutung & Beispiele","metaDesc":"Die verwirrendsten englischen Wörter erklärt: Bedeutungen, Beispielsätze und Verbformen. get, exit, embarrassed und Hunderte mehr — dann im App-Duell festigen.","tagline":"Die <span class='g'>verwirrendsten</span> englischen Wörter","sub":"Lerne die echte Bedeutung jedes Wortes, Beispielsätze und Formen. Dann im App-Duell festigen.","search":"🔍 Wort suchen…","popular":"Wörter","all":"Alle Themen"},
 "fr":{"title":"LinguaBattle — Mots anglais : sens et exemples","metaDesc":"Les mots anglais les plus déroutants expliqués : sens, phrases d'exemple et formes verbales. get, exit, embarrassed et des centaines d'autres — puis ancrez-les avec un duel dans l'app.","tagline":"Les mots anglais les plus <span class='g'>déroutants</span>","sub":"Apprends le vrai sens de chaque mot, des phrases d'exemple et ses formes. Puis ancre-les avec un duel dans l'app.","search":"🔍 Chercher un mot…","popular":"Mots","all":"Tous les sujets"},
 "es":{"title":"LinguaBattle — Palabras en inglés: significados y ejemplos","metaDesc":"Las palabras inglesas más confusas explicadas: significados, frases de ejemplo y formas verbales. get, exit, embarrassed y cientos más — luego fíjalas con un duelo en la app.","tagline":"Las palabras inglesas más <span class='g'>confusas</span>","sub":"Aprende el significado real de cada palabra, frases de ejemplo y sus formas. Luego fíjalas con un duelo en la app.","search":"🔍 Buscar una palabra…","popular":"Palabras","all":"Todos los temas"},
 "ar":{"title":"LinguaBattle — معاني الكلمات الإنجليزية وأمثلتها","metaDesc":"شرح أكثر الكلمات الإنجليزية إرباكًا: المعاني وجُمل الأمثلة وصيغ الأفعال. get وexit وembarrassed والمئات غيرها — ثم ثبّتها بمبارزة في التطبيق.","tagline":"أكثر الكلمات الإنجليزية <span class='g'>إرباكًا</span>","sub":"تعلّم المعنى الحقيقي لكل كلمة وجُمل الأمثلة وصيغها. ثم ثبّتها بمبارزة في التطبيق.","search":"🔍 ابحث عن كلمة…","popular":"كلمات","all":"كل المواضيع"},
 "hi":{"title":"LinguaBattle — अंग्रेज़ी शब्दों के अर्थ और उदाहरण","metaDesc":"सबसे भ्रमित करने वाले अंग्रेज़ी शब्दों की व्याख्या: अर्थ, उदाहरण वाक्य और क्रिया रूप। get, exit, embarrassed और सैकड़ों और — फिर ऐप में डुएल से पक्का करें।","tagline":"सबसे <span class='g'>भ्रमित करने वाले</span> अंग्रेज़ी शब्द","sub":"हर शब्द का असली अर्थ, उदाहरण वाक्य और रूप सीखें। फिर ऐप में डुएल से पक्का करें।","search":"🔍 कोई शब्द खोजें…","popular":"शब्द","all":"सभी विषय"},
 "ru":{"title":"LinguaBattle — Английские слова: значения и примеры","metaDesc":"Самые путаемые английские слова с объяснением: значения, примеры предложений и формы глаголов. get, exit, embarrassed и сотни других — затем закрепите их в дуэли в приложении.","tagline":"Самые <span class='g'>путаемые</span> английские слова","sub":"Узнай настоящее значение каждого слова, примеры предложений и формы. Затем закрепи их в дуэли в приложении.","search":"🔍 Найти слово…","popular":"Слова","all":"Все темы"},
 "pt":{"title":"LinguaBattle — Palavras em inglês: significados e exemplos","metaDesc":"As palavras inglesas mais confusas explicadas: significados, frases de exemplo e formas verbais. get, exit, embarrassed e centenas mais — depois fixe-as com um duelo no app.","tagline":"As palavras inglesas mais <span class='g'>confusas</span>","sub":"Aprenda o significado real de cada palavra, frases de exemplo e suas formas. Depois fixe-as com um duelo no app.","search":"🔍 Buscar uma palavra…","popular":"Palavras","all":"Todos os tópicos"},
 "ja":{"title":"LinguaBattle — 英単語の意味と例文","metaDesc":"最も紛らわしい英単語を解説：意味、例文、活用形。get、exit、embarrassed など数百語 — そしてアプリのデュエルで定着。","tagline":"最も<span class='g'>紛らわしい</span>英単語","sub":"各単語の本当の意味・例文・活用形を学ぼう。そしてアプリのデュエルで定着。","search":"🔍 単語を検索…","popular":"単語","all":"すべてのトピック"},
}

def build_home(lang, entries):
    ui = UI[lang]; h = HOME[lang]
    rtl = lang in RTL
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{l}/">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/en/">'
    cards = ""
    for e in entries:
        if lang not in e["paths"]: continue
        cards += (f'<a class="wcard" href="{e["paths"][lang]}">'
                  f'<div class="w">{esc(e["word"])}</div>'
                  f'<span class="cat">{esc(e.get("category",""))}</span>'
                  f'<div class="d">{esc(e["desc"].get(lang,""))}</div></a>')
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if rtl else 'ltr'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(h['title'])}</title>
<meta name="description" content="{esc(h['metaDesc'])}">
<link rel="canonical" href="{SITE}/{lang}/">
{alts}
<meta property="og:title" content="{esc(h['title'])}">
<meta property="og:description" content="{esc(h['metaDesc'])}">
<meta property="og:image" content="{SITE}/assets/logo-icon.png">
<link rel="icon" type="image/png" href="/assets/logo-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}
.hero{{max-width:820px;margin:0 auto;padding:56px 24px 24px;text-align:center}}
.hero h1{{font-size:2.4rem;font-weight:800;line-height:1.15;margin-bottom:14px}}
.hero h1 .g{{background:linear-gradient(90deg,#A3FE00,#00E3FD);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.hero p{{color:#9BACCA;font-size:1.1rem;max-width:540px;margin:0 auto 24px}}
.searchwrap{{max-width:540px;margin:0 auto;position:relative;text-align:start}}
#search{{width:100%;background:#011A36;border:1px solid #384962;color:#D9E6FF;border-radius:14px;padding:14px 18px;font-family:inherit;font-size:1.05rem}}
#search:focus{{outline:none;border-color:#A3FE00}}
#results{{position:absolute;left:0;right:0;top:60px;background:#04203E;border:1px solid #384962;border-radius:14px;overflow:hidden;z-index:30;display:none}}
#results a{{display:flex;justify-content:space-between;gap:12px;padding:12px 16px;color:#D9E6FF;border-bottom:1px solid #072647}}
#results a:hover{{background:#072647}}
#results .rw{{font-family:'Plus Jakarta Sans';font-weight:700;color:#DDFFAF}}
#results .rd{{color:#9BACCA;font-size:.85rem}}
.section{{max-width:1000px;margin:0 auto;padding:32px 24px}}
.section h2{{font-size:1.4rem;font-weight:700;margin-bottom:18px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}
.wcard{{display:block;background:#011A36;border:1px solid #384962;border-radius:16px;padding:20px;transition:.18s}}
.wcard:hover{{border-color:#A3FE00;transform:translateY(-2px)}}
.wcard .w{{font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.4rem;background:linear-gradient(90deg,#A3FE00,#00E3FD);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.wcard .cat{{display:inline-block;margin-top:6px;font-size:.72rem;color:#81ECFF;background:#072647;border:1px solid #384962;border-radius:20px;padding:2px 10px}}
.wcard .d{{margin-top:10px;color:#9BACCA;font-size:.9rem}}
</style>
</head>
<body>
<div class="topbar">
  <a class="logo" href="/{lang}/"><img src="/assets/logo.svg" alt="LinguaBattle" width="30" height="30"><span>LinguaBattle</span></a>
  {lang_home_switcher(lang)}
</div>
<div class="hero">
  <h1>{h['tagline']}</h1>
  <p>{esc(h['sub'])}</p>
  <div class="searchwrap"><input id="search" type="text" autocomplete="off" placeholder="{esc(h['search'])}"><div id="results"></div></div>
</div>
<div class="section">
  <a href="/{lang}/{TEST_SLUG[lang]}" style="display:block;background:linear-gradient(135deg,#04203E,#011A36);border:1px solid #A3FE00;border-radius:18px;padding:24px;text-align:center;box-shadow:0 0 32px rgba(163,254,0,.12)">
    <div style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.4rem;margin-bottom:6px">{TEST_BANNER[lang][0]}</div>
    <div style="color:#9BACCA;margin-bottom:4px">{esc(TEST_BANNER[lang][1])}</div>
    <div style="color:#A3FE00;font-weight:600">{esc(TEST_BANNER[lang][2])}</div>
  </a>
</div>
<div class="section">
  <h2>{esc(h['all'])}</h2>
  <div class="grid">{cards}</div>
</div>
<footer>© 2026 LinguaBattle</footer>
<script>
const LANG='{lang}';let WORDS=[];
fetch('/words-index.json').then(r=>r.json()).then(d=>{{WORDS=d;}}).catch(()=>{{}});
const inp=document.getElementById('search'),box=document.getElementById('results');
inp.addEventListener('input',()=>{{const q=inp.value.trim().toLowerCase();if(!q){{box.style.display='none';return;}}
const hits=WORDS.filter(w=>w.word.toLowerCase().includes(q)).slice(0,8);
if(!hits.length){{box.innerHTML='';box.style.display='none';return;}}
box.innerHTML=hits.map(w=>{{const p=(w.paths&&w.paths[LANG])||(w.paths&&w.paths.en)||'#';const d=(w.desc&&w.desc[LANG])||'';return `<a href="${{p}}"><span class="rw">${{w.word}}</span><span class="rd">${{d}}</span></a>`;}}).join('');
box.style.display='block';}});
document.addEventListener('click',e=>{{if(!e.target.closest('.searchwrap'))box.style.display='none';}});
</script>
</body>
</html>"""

def lang_home_switcher(cur):
    opts = [f'<option value="/{l}/"{" selected" if l==cur else ""}>{LANG_LABEL[l]}</option>' for l in LANGS]
    return '<select onchange="location.href=this.value">' + "".join(opts) + '</select>'

def main():
    files = sorted(glob.glob(os.path.join(CONTENT, "*.json")))
    urls = []
    count = 0
    for f in files:
        data = json.load(open(f, encoding="utf-8"))
        word = data["word"]; pron = data.get("pron",""); conj = data.get("conj")
        for lang in LANGS:
            if lang not in data:
                print(f"  ! {word}: {lang} eksik, atlandı"); continue
            out_dir = os.path.join(ROOT, lang, SEG[lang])
            os.makedirs(out_dir, exist_ok=True)
            out = os.path.join(out_dir, slugify(word) + ".html")
            with open(out, "w", encoding="utf-8") as fp:
                fp.write(build_page(word, pron, conj, lang, data[lang]))
            urls.append(url_for(lang, word))
            count += 1
        print(f"✓ {word} → {len(LANGS)} dil")

    # sitemap.xml (hreflang'lı)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">'.replace("sitemap.org","sitemaps.org")]
    for f in files:
        data = json.load(open(f, encoding="utf-8")); word = data["word"]
        for lang in LANGS:
            if lang not in data: continue
            sm.append(f"  <url><loc>{url_for(lang, word)}</loc>")
            for l2 in LANGS:
                if l2 in data:
                    sm.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{url_for(l2, word)}"/>')
            sm.append("  </url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))

    # robots.txt
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

    # words-index.json — ana sayfa aramasını besler (her dil için yol + kısa açıklama)
    index = []
    for f in files:
        data = json.load(open(f, encoding="utf-8"))
        word = data["word"]
        entry = {"word": word, "category": data.get("category", ""), "paths": {}, "desc": {}}
        for lang in LANGS:
            if lang not in data:
                continue
            entry["paths"][lang] = f"/{lang}/{SEG[lang]}/{slugify(word)}"
            entry["desc"][lang] = data[lang]["means"][0]["def"]
        index.append(entry)
    open(os.path.join(ROOT, "words-index.json"), "w", encoding="utf-8").write(
        json.dumps(index, ensure_ascii=False, indent=2))

    # Dil ana sayfaları: /tr/index.html, /de/index.html ...
    home_count = 0
    for lang in LANGS:
        out_dir = os.path.join(ROOT, lang)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(build_home(lang, index))
        home_count += 1

    # sitemap'e dil ana sayfalarını da ekle
    home_sm = []
    for lang in LANGS:
        home_sm.append(f"  <url><loc>{SITE}/{lang}/</loc>")
        for l2 in LANGS:
            home_sm.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{SITE}/{l2}/"/>')
        home_sm.append("  </url>")
    # builder dışında elle üretilen statik sayfalar (interaktif testler vb.)
    for extra in EXTRA_PAGES:
        home_sm.append(f"  <url><loc>{SITE}{extra}</loc></url>")
    sm_content = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    sm_content = sm_content.replace("</urlset>", "\n".join(home_sm) + "\n</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm_content)

    print(f"\n✅ {count} kelime sayfası + {home_count} dil ana sayfası · sitemap + robots + words-index yazıldı")

if __name__ == "__main__":
    main()
