#!/usr/bin/env python3
"""
Seviye testi üreticisi — tek UI çeviri tablosundan 10 dilde test sayfası basar.
Sorular HEP İngilizce (öğretilen dil), sadece arayüz/sonuç metni çevrilir.
Kullanım: python3 scripts/build_level_test.py
"""
import os, json

SITE = "https://linguabattle.net"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["tr", "en", "de", "fr", "es", "ar", "hi", "ru", "pt", "ja"]
RTL = {"ar"}
LABEL = {"tr":"🇹🇷 Türkçe","en":"🇬🇧 English","de":"🇩🇪 Deutsch","fr":"🇫🇷 Français",
 "es":"🇪🇸 Español","ar":"🇸🇦 العربية","hi":"🇮🇳 हिन्दी","ru":"🇷🇺 Русский","pt":"🇵🇹 Português","ja":"🇯🇵 日本語"}

# Her dilde test sayfasının yol adı (SEO için yerel)
SLUG = {"tr":"seviye-testi","en":"english-level-test","de":"englisch-niveau-test",
        "fr":"test-de-niveau-anglais","es":"test-de-nivel-ingles","ar":"ikhtibar-mustawa",
        "hi":"angrezi-level-test","ru":"test-urovnya","pt":"teste-de-nivel-ingles","ja":"eigo-level-test"}

PLAY = "https://play.google.com/store/apps/details?id=com.linguabattle.app"
APPSTORE = "https://apps.apple.com/app/id6761505565"

# 20 soru — TÜM dillerde aynı (İngilizce). lvl skorlama içindir, gösterilmez.
QUESTIONS = [
  {"lvl":"A1","q":"She ___ a teacher.","opts":["are","is","am"],"ok":1},
  {"lvl":"A1","q":"I ___ coffee every morning.","opts":["drinks","drinking","drink"],"ok":2},
  {"lvl":"A1","q":"There ___ three books on the table.","opts":["are","is","be"],"ok":0},
  {"lvl":"A1","q":"This is ___ apple.","opts":["the","an","a"],"ok":1},
  {"lvl":"A2","q":"Yesterday we ___ to the cinema.","opts":["went","go","goes"],"ok":0},
  {"lvl":"A2","q":"She is ___ than her brother.","opts":["tall","tallest","taller"],"ok":2},
  {"lvl":"A2","q":"___ you ever been to London?","opts":["Did","Have","Are"],"ok":1},
  {"lvl":"A2","q":"I'm good ___ playing chess.","opts":["in","on","at"],"ok":2},
  {"lvl":"B1","q":"If it rains, we ___ at home.","opts":["will stay","stay","stayed"],"ok":0},
  {"lvl":"B1","q":"I've lived here ___ 2019.","opts":["for","from","since"],"ok":2},
  {"lvl":"B1","q":"The report ___ by the team last week.","opts":["was written","wrote","is writing"],"ok":0},
  {"lvl":"B1","q":"She asked me where I ___ from.","opts":["was","am","be"],"ok":0},
  {"lvl":"B2","q":"He suggested ___ a break.","opts":["to take","take","taking"],"ok":2},
  {"lvl":"B2","q":"By next year, she ___ here for a decade.","opts":["will work","will have worked","works"],"ok":1},
  {"lvl":"B2","q":"I wish I ___ more time to study.","opts":["had","have","will have"],"ok":0},
  {"lvl":"B2","q":"It's high time we ___ home.","opts":["go","will go","went"],"ok":2},
  {"lvl":"C1","q":"___ had I arrived when the phone rang.","opts":["Hard","Hardly","Rarely than"],"ok":1},
  {"lvl":"C1","q":"She spoke as though she ___ everything.","opts":["knew","knows","has known"],"ok":0},
  {"lvl":"C1","q":"The proposal was met with ___ enthusiasm.","opts":["considering","considerate","considerable"],"ok":2},
  {"lvl":"C1","q":"Not only ___ late, but he also forgot the files.","opts":["he was","was he","he is"],"ok":1},
]

# Arayüz çevirileri + her CEFR seviyesi için açıklama
UI = {
 "tr":{"title":"İngilizce Seviye Testi","titleTag":"İngilizce Seviye Testi (Ücretsiz, CEFR A1-C2) | LinguaBattle",
   "desc":"Ücretsiz İngilizce seviye testi: 20 soruda seviyeni öğren (A1-C2). Kayıt yok — sonunda CEFR seviyen ve pratik önerisi.",
   "home":"Ana sayfa","h1a":"İngilizce","h1b":"Seviye Testi",
   "lede":"20 soruda İngilizce seviyeni öğren. Ücretsiz, kayıt yok, 5 dakika. Sonunda CEFR seviyeni (A1–C2) ve sana uygun pratik önerisini göreceksin.",
   "start":"Teste başla →","meta":"20 soru · ~5 dakika · İngilizce dilbilgisi","qword":"Soru",
   "rlevel":"Senin İngilizce seviyen:","rscore":"{n} sorudan {s} doğru","ctaTitle":"{lv} seviyene uygun pratik yap",
   "ctaDesc":"LinguaBattle'da {lv} seviyene göre kelime düellosu ve derslerle ilerle. Günde 5 dakika yeter.",
   "dl":"Google Play'den indir","dlAlt":"App Store'dan indir","retry":"↺ Testi tekrar çöz",
   "L":{"C1":"İleri seviye. Karmaşık metinleri anlıyor, akıcı konuşuyorsun. Hedefin C2 ve nüansları yakalamak.",
        "B2":"Üst-orta seviye. Çoğu konuda rahat iletişim kuruyorsun. İncelikleri derinleştirerek C1'e geçebilirsin.",
        "B1":"Orta seviye. Günlük durumlarda kendini ifade edebiliyorsun. Zamanları pekiştirerek B2'ye çıkabilirsin.",
        "A2":"Temel seviye. Basit cümleler kurabiliyorsun. Düzenli pratikle B1'e hızla geçebilirsin.",
        "A1":"Başlangıç seviyesi. Temelleri öğreniyorsun. Günde birkaç dakika pratikle hızla ilerlersin."}},
 "en":{"title":"English Level Test","titleTag":"English Level Test (Free, CEFR A1-C2) | LinguaBattle",
   "desc":"Free English level test: find your level in 20 questions (A1-C2). No signup — get your CEFR level and a practice tip.",
   "home":"Home","h1a":"English","h1b":"Level Test",
   "lede":"Find your English level in 20 questions. Free, no signup, 5 minutes. You'll get your CEFR level (A1–C2) and a practice tip.",
   "start":"Start the test →","meta":"20 questions · ~5 min · English grammar","qword":"Question",
   "rlevel":"Your English level is:","rscore":"{s} correct out of {n}","ctaTitle":"Practice at your {lv} level",
   "ctaDesc":"On LinguaBattle, progress with word duels and lessons at your {lv} level. Just 5 minutes a day.",
   "dl":"Get it on Google Play","dlAlt":"Download on the App Store","retry":"↺ Retake the test",
   "L":{"C1":"Advanced. You understand complex texts and speak fluently. Aim for C2 and mastering nuance.",
        "B2":"Upper-intermediate. You communicate comfortably on most topics. Deepen nuance to reach C1.",
        "B1":"Intermediate. You can express yourself in everyday situations. Solidify tenses to reach B2.",
        "A2":"Elementary. You can make simple sentences. With regular practice you'll reach B1 fast.",
        "A1":"Beginner. You're learning the basics. A few minutes a day will move you forward quickly."}},
 "de":{"title":"Englisch Niveau-Test","titleTag":"Englisch Niveau-Test (Kostenlos, CEFR A1-C2) | LinguaBattle",
   "desc":"Kostenloser Englisch-Test: Finde dein Niveau in 20 Fragen (A1-C2). Ohne Anmeldung — mit CEFR-Niveau und Übungstipp.",
   "home":"Start","h1a":"Englisch","h1b":"Niveau-Test",
   "lede":"Finde dein Englischniveau in 20 Fragen. Kostenlos, ohne Anmeldung, 5 Minuten. Du erhältst dein CEFR-Niveau (A1–C2) und einen Übungstipp.",
   "start":"Test starten →","meta":"20 Fragen · ~5 Min · englische Grammatik","qword":"Frage",
   "rlevel":"Dein Englischniveau ist:","rscore":"{s} von {n} richtig","ctaTitle":"Übe auf deinem {lv}-Niveau",
   "ctaDesc":"Mach bei LinguaBattle mit Wort-Duellen und Lektionen auf deinem {lv}-Niveau Fortschritte. Nur 5 Minuten am Tag.",
   "dl":"Bei Google Play","dlAlt":"Im App Store laden","retry":"↺ Test wiederholen",
   "L":{"C1":"Fortgeschritten. Du verstehst komplexe Texte und sprichst fließend. Ziel: C2 und Nuancen meistern.",
        "B2":"Obere Mittelstufe. Du kommunizierst sicher zu den meisten Themen. Vertiefe Nuancen für C1.",
        "B1":"Mittelstufe. Du drückst dich in Alltagssituationen aus. Festige Zeitformen für B2.",
        "A2":"Grundstufe. Du bildest einfache Sätze. Mit regelmäßiger Übung erreichst du schnell B1.",
        "A1":"Anfänger. Du lernst die Grundlagen. Ein paar Minuten täglich bringen dich schnell voran."}},
 "fr":{"title":"Test de Niveau d'Anglais","titleTag":"Test de Niveau d'Anglais (Gratuit, CEFR A1-C2) | LinguaBattle",
   "desc":"Test d'anglais gratuit : trouve ton niveau en 20 questions (A1-C2). Sans inscription — niveau CECR et conseil de pratique.",
   "home":"Accueil","h1a":"Anglais","h1b":"Test de Niveau",
   "lede":"Trouve ton niveau d'anglais en 20 questions. Gratuit, sans inscription, 5 minutes. Tu obtiendras ton niveau CECR (A1–C2) et un conseil.",
   "start":"Commencer le test →","meta":"20 questions · ~5 min · grammaire anglaise","qword":"Question",
   "rlevel":"Ton niveau d'anglais est :","rscore":"{s} bonnes réponses sur {n}","ctaTitle":"Entraîne-toi à ton niveau {lv}",
   "ctaDesc":"Sur LinguaBattle, progresse avec des duels de mots et des leçons à ton niveau {lv}. 5 minutes par jour suffisent.",
   "dl":"Sur Google Play","dlAlt":"Sur l'App Store","retry":"↺ Refaire le test",
   "L":{"C1":"Avancé. Tu comprends des textes complexes et parles couramment. Vise le C2 et la maîtrise des nuances.",
        "B2":"Intermédiaire supérieur. Tu communiques aisément sur la plupart des sujets. Approfondis pour atteindre le C1.",
        "B1":"Intermédiaire. Tu t'exprimes dans les situations courantes. Consolide les temps pour atteindre le B2.",
        "A2":"Élémentaire. Tu fais des phrases simples. Avec une pratique régulière, tu atteindras vite le B1.",
        "A1":"Débutant. Tu apprends les bases. Quelques minutes par jour te feront progresser vite."}},
 "es":{"title":"Test de Nivel de Inglés","titleTag":"Test de Nivel de Inglés (Gratis, CEFR A1-C2) | LinguaBattle",
   "desc":"Test de inglés gratis: descubre tu nivel en 20 preguntas (A1-C2). Sin registro — nivel MCER y consejo de práctica.",
   "home":"Inicio","h1a":"Inglés","h1b":"Test de Nivel",
   "lede":"Descubre tu nivel de inglés en 20 preguntas. Gratis, sin registro, 5 minutos. Obtendrás tu nivel MCER (A1–C2) y un consejo.",
   "start":"Empezar el test →","meta":"20 preguntas · ~5 min · gramática inglesa","qword":"Pregunta",
   "rlevel":"Tu nivel de inglés es:","rscore":"{s} aciertos de {n}","ctaTitle":"Practica en tu nivel {lv}",
   "ctaDesc":"En LinguaBattle, avanza con duelos de palabras y lecciones en tu nivel {lv}. Bastan 5 minutos al día.",
   "dl":"En Google Play","dlAlt":"En el App Store","retry":"↺ Repetir el test",
   "L":{"C1":"Avanzado. Entiendes textos complejos y hablas con fluidez. Apunta al C2 y a dominar los matices.",
        "B2":"Intermedio alto. Te comunicas con comodidad en casi todo. Profundiza para llegar al C1.",
        "B1":"Intermedio. Te expresas en situaciones cotidianas. Consolida los tiempos para llegar al B2.",
        "A2":"Elemental. Haces frases simples. Con práctica regular llegarás pronto al B1.",
        "A1":"Principiante. Aprendes lo básico. Unos minutos al día te harán avanzar rápido."}},
 "ar":{"title":"اختبار مستوى الإنجليزية","titleTag":"اختبار مستوى الإنجليزية (مجاني، CEFR A1-C2) | LinguaBattle",
   "desc":"اختبار إنجليزية مجاني: اعرف مستواك في 20 سؤالًا (A1-C2). بدون تسجيل — مستواك حسب CEFR ونصيحة للتدرّب.",
   "home":"الرئيسية","h1a":"الإنجليزية","h1b":"اختبار المستوى",
   "lede":"اعرف مستواك في الإنجليزية في 20 سؤالًا. مجاني، بدون تسجيل، 5 دقائق. ستحصل على مستواك حسب CEFR (A1–C2) ونصيحة.",
   "start":"ابدأ الاختبار →","meta":"20 سؤالًا · ~5 دقائق · قواعد الإنجليزية","qword":"سؤال",
   "rlevel":"مستواك في الإنجليزية:","rscore":"{s} صحيحة من {n}","ctaTitle":"تدرّب على مستواك {lv}",
   "ctaDesc":"في LinguaBattle، تقدّم بمبارزات الكلمات والدروس على مستواك {lv}. 5 دقائق يوميًا تكفي.",
   "dl":"من Google Play","dlAlt":"من App Store","retry":"↺ أعد الاختبار",
   "L":{"C1":"متقدّم. تفهم النصوص المعقّدة وتتحدّث بطلاقة. هدفك C2 وإتقان الفروق الدقيقة.",
        "B2":"فوق المتوسط. تتواصل بأريحية في معظم المواضيع. عمّق الفروق للوصول إلى C1.",
        "B1":"متوسط. تعبّر عن نفسك في المواقف اليومية. ثبّت الأزمنة للوصول إلى B2.",
        "A2":"مبتدئ متقدّم. تكوّن جملًا بسيطة. بالتدرّب المنتظم ستصل إلى B1 بسرعة.",
        "A1":"مبتدئ. تتعلّم الأساسيات. بضع دقائق يوميًا تتقدّم بسرعة."}},
 "hi":{"title":"अंग्रेज़ी स्तर परीक्षा","titleTag":"अंग्रेज़ी लेवल टेस्ट (मुफ़्त, CEFR A1-C2) | LinguaBattle",
   "desc":"मुफ़्त अंग्रेज़ी लेवल टेस्ट: 20 सवालों में अपना स्तर जानें (A1-C2)। बिना रजिस्ट्रेशन — CEFR स्तर और अभ्यास सुझाव।",
   "home":"होम","h1a":"अंग्रेज़ी","h1b":"लेवल टेस्ट",
   "lede":"20 सवालों में अपना अंग्रेज़ी स्तर जानें। मुफ़्त, बिना रजिस्ट्रेशन, 5 मिनट। आपको अपना CEFR स्तर (A1–C2) और सुझाव मिलेगा।",
   "start":"टेस्ट शुरू करें →","meta":"20 सवाल · ~5 मिनट · अंग्रेज़ी व्याकरण","qword":"सवाल",
   "rlevel":"आपका अंग्रेज़ी स्तर है:","rscore":"{n} में से {s} सही","ctaTitle":"अपने {lv} स्तर पर अभ्यास करें",
   "ctaDesc":"LinguaBattle पर अपने {lv} स्तर के अनुसार शब्द डुएल और पाठों से आगे बढ़ें। रोज़ 5 मिनट काफ़ी है।",
   "dl":"Google Play पर पाएं","dlAlt":"App Store पर पाएं","retry":"↺ टेस्ट फिर से दें",
   "L":{"C1":"उन्नत। आप जटिल पाठ समझते हैं और धाराप्रवाह बोलते हैं। लक्ष्य C2 और बारीकियाँ।",
        "B2":"उच्च-मध्यम। आप ज़्यादातर विषयों पर आराम से बात करते हैं। C1 के लिए गहराई बढ़ाएँ।",
        "B1":"मध्यम। आप रोज़मर्रा में खुद को व्यक्त कर सकते हैं। B2 के लिए काल पक्के करें।",
        "A2":"प्रारंभिक। आप सरल वाक्य बनाते हैं। नियमित अभ्यास से जल्दी B1 तक पहुँचेंगे।",
        "A1":"शुरुआती। आप मूल बातें सीख रहे हैं। रोज़ कुछ मिनट से तेज़ी से आगे बढ़ेंगे।"}},
 "ru":{"title":"Тест на уровень английского","titleTag":"Тест на уровень английского (бесплатно, CEFR A1-C2) | LinguaBattle",
   "desc":"Бесплатный тест по английскому: узнай свой уровень за 20 вопросов (A1-C2). Без регистрации — уровень CEFR и совет.",
   "home":"Главная","h1a":"Английский","h1b":"тест на уровень",
   "lede":"Узнай свой уровень английского за 20 вопросов. Бесплатно, без регистрации, 5 минут. Получишь свой уровень CEFR (A1–C2) и совет.",
   "start":"Начать тест →","meta":"20 вопросов · ~5 мин · грамматика английского","qword":"Вопрос",
   "rlevel":"Ваш уровень английского:","rscore":"{s} из {n} верно","ctaTitle":"Практикуйтесь на уровне {lv}",
   "ctaDesc":"В LinguaBattle продвигайтесь с дуэлями слов и уроками на вашем уровне {lv}. Всего 5 минут в день.",
   "dl":"В Google Play","dlAlt":"В App Store","retry":"↺ Пройти заново",
   "L":{"C1":"Продвинутый. Вы понимаете сложные тексты и свободно говорите. Цель — C2 и нюансы.",
        "B2":"Выше среднего. Вы свободно общаетесь по большинству тем. Углубляйте нюансы для C1.",
        "B1":"Средний. Вы выражаете себя в повседневных ситуациях. Закрепите времена для B2.",
        "A2":"Элементарный. Вы строите простые предложения. С практикой быстро дойдёте до B1.",
        "A1":"Начальный. Вы учите основы. Несколько минут в день — и вы быстро продвинетесь."}},
 "pt":{"title":"Teste de Nível de Inglês","titleTag":"Teste de Nível de Inglês (Grátis, CEFR A1-C2) | LinguaBattle",
   "desc":"Teste de inglês grátis: descubra seu nível em 20 perguntas (A1-C2). Sem cadastro — nível CEFR e dica de prática.",
   "home":"Início","h1a":"Inglês","h1b":"Teste de Nível",
   "lede":"Descubra seu nível de inglês em 20 perguntas. Grátis, sem cadastro, 5 minutos. Você terá seu nível CEFR (A1–C2) e uma dica.",
   "start":"Começar o teste →","meta":"20 perguntas · ~5 min · gramática inglesa","qword":"Pergunta",
   "rlevel":"Seu nível de inglês é:","rscore":"{s} certas de {n}","ctaTitle":"Pratique no seu nível {lv}",
   "ctaDesc":"No LinguaBattle, avance com duelos de palavras e lições no seu nível {lv}. Bastam 5 minutos por dia.",
   "dl":"No Google Play","dlAlt":"Na App Store","retry":"↺ Refazer o teste",
   "L":{"C1":"Avançado. Você entende textos complexos e fala fluentemente. Mire o C2 e dominar nuances.",
        "B2":"Intermediário superior. Você se comunica bem na maioria dos temas. Aprofunde para o C1.",
        "B1":"Intermediário. Você se expressa no dia a dia. Consolide os tempos para o B2.",
        "A2":"Elementar. Você faz frases simples. Com prática regular chegará rápido ao B1.",
        "A1":"Iniciante. Você aprende o básico. Alguns minutos por dia farão você avançar rápido."}},
 "ja":{"title":"英語レベルテスト","titleTag":"英語レベルテスト（無料・CEFR A1-C2）| LinguaBattle",
   "desc":"無料の英語レベルテスト：20問であなたのレベルを判定（A1-C2）。登録不要 — CEFRレベルと練習のヒント付き。",
   "home":"ホーム","h1a":"英語","h1b":"レベルテスト",
   "lede":"20問であなたの英語レベルを判定。無料・登録不要・5分。CEFRレベル（A1〜C2）と練習のヒントが分かります。",
   "start":"テストを始める →","meta":"20問 · 約5分 · 英文法","qword":"問題",
   "rlevel":"あなたの英語レベルは：","rscore":"{n}問中{s}問正解","ctaTitle":"{lv}レベルで練習しよう",
   "ctaDesc":"LinguaBattleで、あなたの{lv}レベルに合わせた単語デュエルとレッスンで上達。1日5分でOK。",
   "dl":"Google Playで入手","dlAlt":"App Storeで入手","retry":"↺ もう一度受ける",
   "L":{"C1":"上級。複雑な文章を理解し流暢に話せます。目標はC2とニュアンスの習得。",
        "B2":"中上級。ほとんどの話題で快適に意思疎通できます。C1へ向けて深めましょう。",
        "B1":"中級。日常の場面で自分を表現できます。時制を固めてB2へ。",
        "A2":"初級。簡単な文が作れます。継続的な練習ですぐB1に届きます。",
        "A1":"入門。基礎を学習中。1日数分でどんどん前進します。"}},
}

# eşikler (20 üzerinden)
THRESH = [(18,"C1"),(14,"B2"),(9,"B1"),(5,"A2"),(0,"A1")]

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Be Vietnam Pro',-apple-system,sans-serif;background:#000E23;color:#D9E6FF;line-height:1.6}
h1,h2,h3{font-family:'Plus Jakarta Sans',sans-serif}
a{color:#81ECFF;text-decoration:none}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;padding:14px 24px;background:rgba(0,14,35,.85);backdrop-filter:blur(12px);border-bottom:1px solid #384962}
.logo{display:flex;align-items:center;gap:9px;font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.15rem;background:linear-gradient(90deg,#A3FE00,#00E3FD);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo img{height:30px;width:auto;display:block;filter:invert(1) brightness(1.6)}
select{background:#04203E;color:#D9E6FF;border:1px solid #384962;border-radius:8px;padding:7px 10px;font-family:inherit;font-size:.85rem;cursor:pointer}
.wrap{max-width:680px;margin:0 auto;padding:36px 24px}
.crumb{font-size:.8rem;color:#9BACCA;margin-bottom:14px}
h1{font-size:2.2rem;font-weight:800;line-height:1.15;margin-bottom:10px}
h1 .g{background:linear-gradient(90deg,#A3FE00,#00E3FD);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.lede{color:#9BACCA;font-size:1.05rem;margin-bottom:24px}
.start{display:inline-block;background:#A3FE00;color:#3F6600;font-weight:700;font-family:'Plus Jakarta Sans';border-radius:12px;padding:14px 28px;font-size:1.05rem;box-shadow:0 0 28px rgba(163,254,0,.3);cursor:pointer;border:none}
.meta{margin-top:14px;color:#9BACCA;font-size:.85rem}
.progress{height:6px;background:#072647;border-radius:6px;overflow:hidden;margin-bottom:22px}
.progress div{height:100%;background:linear-gradient(90deg,#A3FE00,#00E3FD);width:0;transition:.3s}
.qnum{font-size:.82rem;color:#81ECFF;margin-bottom:8px}
.q{font-size:1.25rem;font-weight:600;font-family:'Plus Jakarta Sans';margin-bottom:18px;direction:ltr}
.opt{display:block;width:100%;text-align:left;background:#011A36;border:1px solid #384962;color:#D9E6FF;border-radius:12px;padding:14px 18px;margin-bottom:10px;font-family:inherit;font-size:1rem;cursor:pointer;transition:.15s;direction:ltr}
.opt:hover{border-color:#A3FE00;background:#04203E}
.hide{display:none}
.result{text-align:center}
.badge{display:inline-block;font-family:'Plus Jakarta Sans';font-weight:800;font-size:3rem;background:linear-gradient(90deg,#A3FE00,#00E3FD);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:8px 0}
.rlevel{font-size:1.1rem;color:#9BACCA;margin-bottom:6px}
.rdesc{background:#011A36;border:1px solid #384962;border-radius:14px;padding:18px;margin:18px 0;color:#9BACCA;text-align:start}
.score{color:#81ECFF;font-weight:600;margin-bottom:18px}
.cta{background:linear-gradient(160deg,#04203E,#011A36);border:1px solid #384962;border-radius:18px;padding:24px;margin-top:20px}
.cta h3{font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.2rem;margin-bottom:6px}
.cta p{color:#9BACCA;font-size:.9rem;margin-bottom:16px}
.store{display:block;background:#A3FE00;color:#3F6600;font-weight:700;font-family:'Plus Jakarta Sans';border-radius:11px;padding:13px;margin-bottom:9px;box-shadow:0 0 24px rgba(163,254,0,.28)}
.store.alt{background:#072647;color:#D9E6FF;box-shadow:none;border:1px solid #384962}
.retry{margin-top:16px;color:#81ECFF;background:none;border:none;font-family:inherit;font-size:.95rem;cursor:pointer;text-decoration:underline}
footer{max-width:680px;margin:0 auto;padding:32px 24px;border-top:1px solid #384962;color:#9BACCA;font-size:.82rem}"""

def url_for(lang): return f"{SITE}/{lang}/{SLUG[lang]}"

def switcher(cur):
    opts = "".join(f'<option value="/{l}/{SLUG[l]}"{" selected" if l==cur else ""}>{LABEL[l]}</option>' for l in LANGS)
    return f'<select onchange="location.href=this.value">{opts}</select>'

def build(lang):
    u = UI[lang]; rtl = lang in RTL
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{url_for(l)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{url_for("en")}">'
    qjson = json.dumps(QUESTIONS, ensure_ascii=False)
    ljson = json.dumps([{"min":m,"code":c,"desc":u["L"][c]} for m,c in THRESH], ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if rtl else 'ltr'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{u['titleTag']}</title>
<meta name="description" content="{u['desc']}">
<link rel="canonical" href="{url_for(lang)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:title" content="{u['title']}">
<meta property="og:description" content="{u['desc']}">
<meta property="og:url" content="{url_for(lang)}">
<meta property="og:image" content="{SITE}/assets/logo-icon.png">
<link rel="icon" type="image/png" href="/assets/logo-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@300;400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Quiz","name":"{u['title']}","about":"English level test (CEFR A1-C2)","educationalLevel":"A1-C2","url":"{url_for(lang)}"}}</script>
<style>{CSS}</style>
</head>
<body>
<div class="topbar">
  <a class="logo" href="/{lang}/"><img src="/assets/logo.svg" alt="LinguaBattle" width="30" height="30"><span>LinguaBattle</span></a>
  {switcher(lang)}
</div>
<div class="wrap">
  <nav class="crumb"><a href="/{lang}/">{u['home']}</a> › {u['title']}</nav>
  <section id="intro">
    <h1>{u['h1a']} <span class="g">{u['h1b']}</span></h1>
    <p class="lede">{u['lede']}</p>
    <button class="start" onclick="startQuiz()">{u['start']}</button>
    <div class="meta">{u['meta']}</div>
  </section>
  <section id="quiz" class="hide">
    <div class="progress"><div id="bar"></div></div>
    <div class="qnum" id="qnum"></div>
    <div class="q" id="qtext"></div>
    <div id="opts"></div>
  </section>
  <section id="result" class="hide result">
    <div class="rlevel">{u['rlevel']}</div>
    <div class="badge" id="rbadge">B1</div>
    <div class="score" id="rscore"></div>
    <div class="rdesc" id="rdesc"></div>
    <div class="cta">
      <h3 id="ctaTitle"></h3><p id="ctaDesc"></p>
      <a class="store" href="{PLAY}">▶ {u['dl']}</a>
      <a class="store alt" href="{APPSTORE}">{u['dlAlt']}</a>
    </div>
    <button class="retry" onclick="location.reload()">{u['retry']}</button>
  </section>
</div>
<footer>© 2026 LinguaBattle · {u['title']}</footer>
<script>
const Q={qjson}, L={ljson};
const QW={json.dumps(u['qword'])}, RSCORE={json.dumps(u['rscore'])}, CTATITLE={json.dumps(u['ctaTitle'])}, CTADESC={json.dumps(u['ctaDesc'])};
let idx=0,score=0;
function startQuiz(){{document.getElementById('intro').classList.add('hide');document.getElementById('quiz').classList.remove('hide');render();}}
function render(){{
  const q=Q[idx];
  document.getElementById('bar').style.width=(idx/Q.length*100)+'%';
  document.getElementById('qnum').textContent=QW+' '+(idx+1)+' / '+Q.length;
  document.getElementById('qtext').textContent=q.q;
  const o=document.getElementById('opts');o.innerHTML='';
  q.opts.forEach((opt,i)=>{{const b=document.createElement('button');b.className='opt';b.textContent=opt;b.onclick=()=>answer(i);o.appendChild(b);}});
}}
function answer(i){{if(i===Q[idx].ok)score++;idx++;if(idx<Q.length)render();else finish();}}
function finish(){{
  document.getElementById('quiz').classList.add('hide');
  document.getElementById('result').classList.remove('hide');
  const lv=L.find(l=>score>=l.min);
  document.getElementById('rbadge').textContent=lv.code;
  document.getElementById('rscore').textContent=RSCORE.replace('{{s}}',score).replace('{{n}}',Q.length);
  document.getElementById('rdesc').textContent=lv.desc;
  document.getElementById('ctaTitle').textContent=CTATITLE.replace('{{lv}}',lv.code);
  document.getElementById('ctaDesc').textContent=CTADESC.replace('{{lv}}',lv.code);
}}
</script>
</body>
</html>"""

def main():
    for lang in LANGS:
        out_dir = os.path.join(ROOT, lang)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, SLUG[lang] + ".html"), "w", encoding="utf-8") as f:
            f.write(build(lang))
    print(f"✅ {len(LANGS)} dilde seviye testi üretildi:")
    for lang in LANGS:
        print(f"   {SITE}/{lang}/{SLUG[lang]}")

if __name__ == "__main__":
    main()
