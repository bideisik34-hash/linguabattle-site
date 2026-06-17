#!/usr/bin/env python3
"""
İçerik doğrulayıcı — her content/*.json'un 10 dili tam ve doğru mu kontrol eder.
build'den ÖNCE çalıştır: python3 scripts/check_content.py
Hata varsa kırmızı listeler, çıkış kodu 1 döner (sorunlu deploy önlenir).
"""
import json, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
LANGS = ["tr", "en", "de", "fr", "es", "ar", "hi", "ru", "pt", "ja"]
REQUIRED = ["pos", "title", "metaDesc", "lede", "means", "relTitle", "rel",
            "idiomTitle", "idioms", "quizQ", "quizA", "quizOk"]

def main():
    files = sorted(glob.glob(os.path.join(CONTENT, "*.json")))
    errors = []
    for f in files:
        name = os.path.basename(f)
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            errors.append(f"{name}: JSON BOZUK — {e}")
            continue
        if "word" not in data:
            errors.append(f"{name}: 'word' eksik")
        for lang in LANGS:
            if lang not in data:
                errors.append(f"{name}: '{lang}' dili EKSİK")
                continue
            d = data[lang]
            for key in REQUIRED:
                if key not in d or d[key] in ("", None, []):
                    errors.append(f"{name} [{lang}]: '{key}' boş/eksik")
            # means ve quizA tutarlılığı
            if isinstance(d.get("means"), list) and len(d["means"]) == 0:
                errors.append(f"{name} [{lang}]: 'means' boş liste")
            if isinstance(d.get("quizA"), list):
                if d.get("quizOk", 0) >= len(d["quizA"]):
                    errors.append(f"{name} [{lang}]: quizOk index aralık dışı")
            for i, m in enumerate(d.get("means", [])):
                for mk in ("def", "en", "t"):
                    if mk not in m:
                        errors.append(f"{name} [{lang}]: means[{i}].{mk} eksik")

    print(f"Kontrol edildi: {len(files)} kelime × {len(LANGS)} dil")
    if errors:
        print(f"\n❌ {len(errors)} SORUN bulundu:")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)
    print("✅ Tüm kelimeler 10 dilde tam ve doğru. Build'e hazır.")

if __name__ == "__main__":
    main()
