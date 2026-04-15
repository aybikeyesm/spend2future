import os
import re
import random
import streamlit as st

st.set_page_config(
    page_title="Spend2Future",
    page_icon="🌿",
    layout="wide",
)

BAD_FUTURE_CANDIDATES = [
    "bad_future.png",
    "/Users/aybikeeskibozkurt/Desktop/bad_future.png",
]
MID_FUTURE_CANDIDATES = [
    "mid_future.png",
    "/Users/aybikeeskibozkurt/Desktop/mid_future.png",
]
GOOD_FUTURE_CANDIDATES = [
    "good_future.png",
    "/Users/aybikeeskibozkurt/Desktop/good_future.png",
]

PRESET_USERS = {
    "aybike@example.com": {
        "user_id": "aybike@example.com",
        "points": 120,
        "streak": 16,
        "premium": True,
        "full_name": "Aybike",
        "age_range": "19-22",
        "city": "Istanbul",
        "goal": "Karbon azaltmak",
        "transport_habit": "Toplu taşıma",
        "climate_interest": "Oldukça ilgiliyim",
        "carbon_awareness": "Oldukça farkındayım",
        "school_or_job": "Üniversite öğrencisi",
        "shopping_style": "İhtiyaç odaklı",
        "food_style": "Dengeli",
        "motivation": "Daha sürdürülebilir bir yaşam kurmak istiyorum.",
    }
}

TEXT = {
    "tr": {
        "appearance_title": "🎨 Görünüm ve Dil",
        "theme": "Tema",
        "language": "Dil",
        "light": "Açık",
        "dark": "Koyu",
        "profile_summary": "👤 Profil Özeti",
        "plan": "Sürüm",
        "premium": "💎 Premium",
        "standard": "🔓 Free Version",
        "level": "Seviye",
        "badge": "Rozet",
        "points": "Puan",
        "streak": "Seri",
        "welcome_big": "Spend2Future",
        "welcome_sub": "Bugünkü seçimlerin, yarının dünyasını oluşturur.",
        "hero_box_title": "🌿 Daha bilinçli alışkanlıklar, daha iyi bir gelecek",
        "hero_box_text": "Karbon ayak izin ve yaşam tarzına göre sana özel bir gelecek senaryosu oluştur.",
        "demo_account": "Hazır premium hesap: aybike@example.com",
        "start": "Başla",
        "register_title": "📝 Kayıt Oluştur / Giriş Yap",
        "login_tab": "Giriş Yap",
        "signup_tab": "Kayıt Ol",
        "email": "E-posta",
        "email_ph": "ornek@mail.com",
        "email_help": "Geçerli bir e-posta adresi gir.",
        "full_name": "Ad Soyad",
        "age_range": "Yaş Aralığı",
        "city": "Şehir",
        "school_or_job": "Okul / Meslek",
        "goal": "Ana hedefin",
        "transport_habit": "Genel ulaşım alışkanlığın",
        "climate_interest": "İklim değişikliği ve sürdürülebilirlik ilgini nasıl tanımlarsın?",
        "carbon_awareness": "Karbon ayak izi farkındalığın",
        "shopping_style": "Alışveriş yaklaşımın",
        "food_style": "Beslenme yaklaşımın",
        "motivation": "Bu uygulamayı neden kullanmak istiyorsun?",
        "register_btn": "Kayıt Ol",
        "login_btn": "Giriş Yap",
        "fill_required": "Lütfen zorunlu alanları doldur.",
        "email_invalid": "Lütfen geçerli bir e-posta adresi gir.",
        "email_not_found": "Bu e-posta kayıtlı değil.",
        "email_exists": "Bu e-posta zaten kayıtlı. Giriş yapmayı dene.",
        "local_info": "Bu sürüm Supabase olmadan çalışır.",
        "welcome": "Hoş geldin",
        "analysis_title": "🌍 Yaşam Tarzı Analizi",
        "transport": "🚗 En sık kullandığın ulaşım türü",
        "clothes": "👕 Ayda aldığın yeni kıyafet sayısı",
        "meat": "🥩 Haftada et tükettiğin gün sayısı",
        "shower": "🚿 Ortalama duş süren (dakika)",
        "takeaway": "🍔 Haftada dışarıdan yemek / sipariş sayın",
        "energy": "💡 Ev içi enerji kullanım düzeyin",
        "analyze": "🔍 Analiz Et",
        "score": "Skor",
        "future_cmp": "🎥 Gelecek Karşılaştırması",
        "current_path": "😟 Mevcut yol",
        "mid_path": "🌤️ Geçiş senaryosu",
        "better_path": "🌿 Daha iyi gelecek",
        "ai_future": "🖼️ Senin gelecek senaryon",
        "tips": "💡 Sana özel öneriler",
        "future_premium_only": "Bu bölüm sadece Premium kullanıcılar için açık.",
        "checklist": "✅ Premium Checklist",
        "daily": "Günlük",
        "weekly": "Haftalık",
        "monthly": "Aylık",
        "quote_1": "✨ Küçük değişiklikler büyük fark yaratır.",
        "quote_2": "🌍 Bugün yaptığın seçimler yarını oluşturur.",
        "quote_3": "💚 Mükemmel olman gerekmiyor, ilerlemen yeterli.",
        "starter": "🌱 Beginner",
        "aware": "🌍 Aware",
        "better": "✨ Better Future",
        "conscious": "💚 Conscious",
        "builder": "🔥 Future Builder",
        "new_explorer": "💡 Yeni Kaşif",
        "starter_badge": "🌱 Başlangıç Rozeti",
        "progress_badge": "✨ İlerleme Rozeti",
        "eco_badge": "🌍 Eko Başarı",
        "streak_badge": "🏆 14 Gün Serisi",
        "logout": "Çıkış Yap",
        "image_missing": "Görsel bulunamadı:",
        "ages": ["15-18", "19-22", "23-30", "31+"],
        "goals": ["Karbon azaltmak", "Daha az harcamak", "Su tasarrufu", "Daha dengeli yaşam"],
        "transport_habits": ["Çoğunlukla araba", "Toplu taşıma", "Yürüyüş ağırlıklı"],
        "climate_interests": ["Yeni öğreniyorum", "İlgim var", "Oldukça ilgiliyim", "Bu konuda aktifim"],
        "carbon_levels": ["Hiç bilmiyorum", "Biraz biliyorum", "Orta düzeyde biliyorum", "Oldukça farkındayım"],
        "education_options": ["Lise", "Üniversite öğrencisi", "Yeni mezun", "Çalışıyorum", "Diğer"],
        "shopping_options": ["Minimal", "İhtiyaç odaklı", "Karışık", "Sık alışveriş yaparım"],
        "food_options": ["Bitki ağırlıklı", "Dengeli", "Et ağırlıklı", "Karışık"],
        "transport_choices": ["Araba", "Toplu taşıma", "Yürüyüş"],
        "energy_choices": ["Düşük", "Orta", "Yüksek"],
    },
    "en": {
        "appearance_title": "🎨 Appearance & Language",
        "theme": "Theme",
        "language": "Language",
        "light": "Light",
        "dark": "Dark",
        "profile_summary": "👤 Profile Summary",
        "plan": "Version",
        "premium": "💎 Premium",
        "standard": "🔓 Free Version",
        "level": "Level",
        "badge": "Badge",
        "points": "Points",
        "streak": "Streak",
        "welcome_big": "Spend2Future",
        "welcome_sub": "Today’s choices shape tomorrow’s world.",
        "hero_box_title": "🌿 Smarter habits, better future",
        "hero_box_text": "Build a personal future scenario based on your carbon footprint and lifestyle.",
        "demo_account": "Ready premium account: aybike@example.com",
        "start": "Start",
        "register_title": "📝 Create Account / Sign In",
        "login_tab": "Sign In",
        "signup_tab": "Sign Up",
        "email": "Email",
        "email_ph": "example@mail.com",
        "email_help": "Enter a valid email address.",
        "full_name": "Full Name",
        "age_range": "Age Range",
        "city": "City",
        "school_or_job": "School / Job",
        "goal": "Main Goal",
        "transport_habit": "General transport habit",
        "climate_interest": "How would you describe your interest in climate change and sustainability?",
        "carbon_awareness": "Carbon footprint awareness",
        "shopping_style": "Shopping style",
        "food_style": "Food style",
        "motivation": "Why do you want to use this app?",
        "register_btn": "Sign Up",
        "login_btn": "Sign In",
        "fill_required": "Please fill the required fields.",
        "email_invalid": "Please enter a valid email address.",
        "email_not_found": "This email is not registered.",
        "email_exists": "This email is already registered. Try signing in.",
        "local_info": "This version works without Supabase.",
        "welcome": "Welcome",
        "analysis_title": "🌍 Lifestyle Analysis",
        "transport": "🚗 Main transport type",
        "clothes": "👕 New clothes per month",
        "meat": "🥩 Days per week eating meat",
        "shower": "🚿 Average shower length (minutes)",
        "takeaway": "🍔 Takeaway / delivery per week",
        "energy": "💡 Home energy usage level",
        "analyze": "🔍 Analyze",
        "score": "Score",
        "future_cmp": "🎥 Future Comparison",
        "current_path": "😟 Current path",
        "mid_path": "🌤️ Transition path",
        "better_path": "🌿 Better future",
        "ai_future": "🖼️ Your future scenario",
        "tips": "💡 Personalized suggestions",
        "future_premium_only": "This section is only available for Premium users.",
        "checklist": "✅ Premium Checklist",
        "daily": "Daily",
        "weekly": "Weekly",
        "monthly": "Monthly",
        "quote_1": "✨ Small changes create big impact.",
        "quote_2": "🌍 The choices you make today shape tomorrow.",
        "quote_3": "💚 Progress matters more than perfection.",
        "starter": "🌱 Beginner",
        "aware": "🌍 Aware",
        "better": "✨ Better Future",
        "conscious": "💚 Conscious",
        "builder": "🔥 Future Builder",
        "new_explorer": "💡 New Explorer",
        "starter_badge": "🌱 Starter Badge",
        "progress_badge": "✨ Progress Badge",
        "eco_badge": "🌍 Eco Badge",
        "streak_badge": "🏆 14 Day Streak",
        "logout": "Log Out",
        "image_missing": "Image not found:",
        "ages": ["15-18", "19-22", "23-30", "31+"],
        "goals": ["Reduce carbon", "Spend less", "Save water", "Live more balanced"],
        "transport_habits": ["Mostly car", "Public transport", "Mostly walking"],
        "climate_interests": ["Just learning", "Interested", "Highly interested", "Actively engaged"],
        "carbon_levels": ["I do not know", "A little aware", "Moderately aware", "Highly aware"],
        "education_options": ["High school", "University student", "Recent graduate", "Working", "Other"],
        "shopping_options": ["Minimal", "Need-based", "Mixed", "Frequent shopper"],
        "food_options": ["Plant-based", "Balanced", "Meat-heavy", "Mixed"],
        "transport_choices": ["Car", "Public Transport", "Walking"],
        "energy_choices": ["Low", "Medium", "High"],
    },
}


def init_state():
    defaults = {
        "current_user": "",
        "email": "",
        "points": 0,
        "streak": 0,
        "premium": False,
        "score": None,
        "registered": False,
        "show_register": False,
        "full_name": "",
        "age_range": "",
        "city": "",
        "goal": "",
        "transport_habit": "",
        "climate_interest": "",
        "carbon_awareness": "",
        "school_or_job": "",
        "shopping_style": "",
        "food_style": "",
        "motivation": "",
        "theme": "light",
        "language": "tr",
        "saved_users": PRESET_USERS.copy(),
        "daily_tasks": {
            "Su tasarrufu yaptım": False,
            "Işıkları kapattım": False,
            "Toplu taşıma / yürüyüş yaptım": False,
        },
        "weekly_tasks": {
            "1 gün bitki ağırlıklı beslendim": False,
            "Gereksiz alışveriş yapmadım": False,
            "Evde yemek yaptım": False,
        },
        "monthly_tasks": {
            "Elektrik kullanımımı gözden geçirdim": False,
            "Tüketim planımı yaptım": False,
            "Karbon hedefimi değerlendirdim": False,
        },
        "last_analysis": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def t(key: str):
    return TEXT[st.session_state.language].get(key, key)


def resolve_image(candidates):
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def apply_theme():
    is_dark = st.session_state.theme == "dark"

    text_main = "#ffffff" if is_dark else "#000000"
    accent = "#7ee0b5" if is_dark else "#1d8a62"
    bg_top = "#0f1d18" if is_dark else "#f7fcf8"
    bg_mid = "#173229" if is_dark else "#e5f5ea"
    bg_bottom = "#214236" if is_dark else "#d6ecd9"
    card_bg = "rgba(18, 34, 28, 0.88)" if is_dark else "rgba(255,255,255,0.93)"
    border = "rgba(152,214,187,0.14)" if is_dark else "rgba(44,114,86,0.10)"
    sidebar_bg = "rgba(12,25,20,0.82)" if is_dark else "rgba(255,255,255,0.78)"
    input_bg = "rgba(255,255,255,0.08)" if is_dark else "rgba(255,255,255,0.94)"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at 12% 10%, rgba(126,224,181,0.12), transparent 24%),
                linear-gradient(180deg, {bg_top} 0%, {bg_mid} 48%, {bg_bottom} 100%);
        }}
        [data-testid="stHeader"] {{ background: transparent; }}
        [data-testid="stSidebar"] {{
            background: {sidebar_bg};
            border-right: 1px solid {border};
        }}
        [data-testid="stSidebar"] * {{
            color: {text_main} !important;
        }}
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] input {{
            background: {input_bg} !important;
            color: {text_main} !important;
            border-color: {border} !important;
        }}
        html, body, p, span, div, label, li, h1, h2, h3, h4, h5, h6,
        .stMarkdown, .stCaption, .stAlert, [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"] {{
            color: {text_main} !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] > div {{
            color: {text_main} !important;
            background: {input_bg} !important;
        }}
        .block-container {{
            padding-top: 1.1rem;
            padding-bottom: 3rem;
        }}
        .card {{
            background: {card_bg};
            border: 1px solid {border};
            border-radius: 24px;
            padding: 22px;
            margin-bottom: 16px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.10);
        }}
        .hero-wrap {{
            display: flex;
            justify-content: center;
            margin-bottom: 18px;
        }}
        .hero-cloud {{
            position: relative;
            width: min(920px, 100%);
            padding: 56px 30px 44px 30px;
            border-radius: 60px;
            background: {card_bg};
            border: 1px solid {border};
            text-align: center;
            box-shadow: 0 20px 45px rgba(0,0,0,0.10);
        }}
        .hero-cloud::before {{
            content: "";
            position: absolute;
            width: 150px;
            height: 150px;
            left: 70px;
            top: -38px;
            border-radius: 50%;
            background: inherit;
            border: 1px solid {border};
            z-index: -1;
        }}
        .hero-cloud::after {{
            content: "";
            position: absolute;
            width: 190px;
            height: 190px;
            right: 82px;
            top: -58px;
            border-radius: 50%;
            background: inherit;
            border: 1px solid {border};
            z-index: -1;
        }}
        .hero-mini {{
            position: absolute;
            width: 110px;
            height: 110px;
            left: 220px;
            top: -46px;
            border-radius: 50%;
            background: inherit;
            border: 1px solid {border};
            z-index: -1;
        }}
        .hero-title {{
            font-size: 58px;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 12px;
            color: {accent} !important;
        }}
        .hero-sub {{
            font-size: 20px;
            font-weight: 600;
            color: {text_main} !important;
            margin-bottom: 18px;
        }}
        .hero-box-title {{
            font-size: 28px;
            font-weight: 800;
            color: {text_main} !important;
            margin-bottom: 10px;
        }}
        .hero-box-text {{
            font-size: 16px;
            line-height: 1.7;
            color: {text_main} !important;
            max-width: 740px;
            margin: 0 auto 12px auto;
        }}
        .hero-demo {{
            font-size: 14px;
            font-weight: 700;
            color: {text_main} !important;
        }}
        .stButton button {{
            background: linear-gradient(135deg, #78d2ab 0%, #59b78f 100%);
            color: white !important;
            border: none;
            border-radius: 14px;
            font-weight: 700;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hydrate_session_from_user(user: dict):
    st.session_state.current_user = user.get("user_id", "")
    st.session_state.email = user.get("user_id", "")
    st.session_state.points = user.get("points", 0)
    st.session_state.streak = user.get("streak", 0)
    st.session_state.premium = user.get("premium", False)
    st.session_state.full_name = user.get("full_name", "")
    st.session_state.age_range = user.get("age_range", "")
    st.session_state.city = user.get("city", "")
    st.session_state.goal = user.get("goal", "")
    st.session_state.transport_habit = user.get("transport_habit", "")
    st.session_state.climate_interest = user.get("climate_interest", "")
    st.session_state.carbon_awareness = user.get("carbon_awareness", "")
    st.session_state.school_or_job = user.get("school_or_job", "")
    st.session_state.shopping_style = user.get("shopping_style", "")
    st.session_state.food_style = user.get("food_style", "")
    st.session_state.motivation = user.get("motivation", "")
    st.session_state.registered = True
    st.session_state.show_register = False


def is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def calculate_score(transport, clothes, meat, shower, takeaway, energy):
    score = 100
    if transport in ["Araba", "Car"]:
        score -= 30
    elif transport in ["Toplu taşıma", "Public Transport"]:
        score -= 10
    if clothes > 3:
        score -= 20
    if meat > 4:
        score -= 20
    if shower > 8:
        score -= 15
    if takeaway > 4:
        score -= 15
    if energy in ["Yüksek", "High"]:
        score -= 15
    elif energy in ["Orta", "Medium"]:
        score -= 5
    return max(0, score)


def get_image(score):
    if score < 35:
        return resolve_image(BAD_FUTURE_CANDIDATES)
    if score < 65:
        return resolve_image(MID_FUTURE_CANDIDATES)
    return resolve_image(GOOD_FUTURE_CANDIDATES)


def get_message(score):
    if st.session_state.language == "tr":
        if score < 35:
            return "😟 Mevcut alışkanlıkların daha yoğun tüketim ve daha zorlayıcı bir gelecek oluşturuyor."
        if score < 65:
            return "🌤️ Geleceğin tamamen olumsuz değil, ama bazı seçimlerin çevresel baskı yaratabilir."
        return "🌿 Daha sürdürülebilir ve dengeli bir geleceğe yakın görünüyorsun."
    if score < 35:
        return "😟 Your current habits point to a more resource-intensive and difficult future."
    if score < 65:
        return "🌤️ Your future is not entirely negative, but some choices may increase environmental pressure."
    return "🌿 You are close to a more sustainable and balanced future."


def get_recommendations(transport, clothes, meat, shower, takeaway, energy):
    items = []
    if st.session_state.language == "tr":
        if transport in ["Araba", "Car"]:
            items.append("Haftada en az 2 gün toplu taşıma veya yürüyüş dene.")
        else:
            items.append("Düşük karbonlu ulaşım alışkanlığını sürdür.")
        if clothes > 3:
            items.append("Bu ay ihtiyaç dışı kıyafet alımını azaltmayı dene.")
        if meat > 4:
            items.append("Haftada 1-2 gün daha bitki ağırlıklı beslenebilirsin.")
        if shower > 8:
            items.append("Duş süreni birkaç dakika azaltmayı dene.")
        if takeaway > 4:
            items.append("Daha fazla evde yemek hazırlamak hem bütçeye hem çevreye iyi gelir.")
        if energy in ["Yüksek", "High"]:
            items.append("Gereksiz ışıkları ve cihazları kapatma rutini oluştur.")
        if not items:
            items.append("Alışkanlıkların oldukça dengeli görünüyor, bunu koru.")
    else:
        if transport in ["Car", "Araba"]:
            items.append("Try public transport or walking at least 2 days a week.")
        else:
            items.append("Keep your low-carbon transport habit.")
        if clothes > 3:
            items.append("Try reducing unnecessary clothing purchases this month.")
        if meat > 4:
            items.append("Try 1-2 more plant-based days each week.")
        if shower > 8:
            items.append("Try shortening your shower by a few minutes.")
        if takeaway > 4:
            items.append("Preparing more meals at home helps both your budget and the environment.")
        if energy in ["High", "Yüksek"]:
            items.append("Build a routine of switching off unnecessary lights and devices.")
        if not items:
            items.append("Your habits look balanced. Keep going.")
    return items


def get_level(points):
    if points < 20:
        return t("starter")
    if points < 50:
        return t("aware")
    if points < 100:
        return t("better")
    if points < 150:
        return t("conscious")
    return t("builder")


def get_badge(points, streak):
    if streak >= 14:
        return t("streak_badge")
    if points >= 100:
        return t("eco_badge")
    if points >= 50:
        return t("progress_badge")
    if points >= 20:
        return t("starter_badge")
    return t("new_explorer")


def get_quote():
    return random.choice([t("quote_1"), t("quote_2"), t("quote_3")])


def show_image_or_warning(path: str, caption: str):
    if path and os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.info(f"{t('image_missing')} {caption}")


def reset_user():
    st.session_state.current_user = ""
    st.session_state.email = ""
    st.session_state.points = 0
    st.session_state.streak = 0
    st.session_state.premium = False
    st.session_state.score = None
    st.session_state.registered = False
    st.session_state.show_register = False
    st.session_state.full_name = ""
    st.session_state.age_range = ""
    st.session_state.city = ""
    st.session_state.goal = ""
    st.session_state.transport_habit = ""
    st.session_state.climate_interest = ""
    st.session_state.carbon_awareness = ""
    st.session_state.school_or_job = ""
    st.session_state.shopping_style = ""
    st.session_state.food_style = ""
    st.session_state.motivation = ""
    st.session_state.last_analysis = None


init_state()
apply_theme()

with st.sidebar:
    st.markdown(f"## {t('appearance_title')}")
    selected_theme = st.selectbox(
        t("theme"),
        ["light", "dark"],
        format_func=lambda x: t("light") if x == "light" else t("dark"),
        index=0 if st.session_state.theme == "light" else 1,
    )
    selected_language = st.selectbox(
        t("language"),
        ["tr", "en"],
        format_func=lambda x: "Türkçe" if x == "tr" else "English",
        index=0 if st.session_state.language == "tr" else 1,
    )

    if selected_theme != st.session_state.theme or selected_language != st.session_state.language:
        st.session_state.theme = selected_theme
        st.session_state.language = selected_language
        st.rerun()

    st.caption(t("local_info"))

    if st.session_state.registered:
        st.markdown("---")
        st.markdown(f"## {t('profile_summary')}")
        st.write(f"**{st.session_state.full_name}**")
        if st.session_state.email:
            st.write(st.session_state.email)
        if st.session_state.city:
            st.write(st.session_state.city)
        st.write(f"**{t('plan')}:** {t('premium') if st.session_state.premium else t('standard')}")
        st.write(f"**{t('level')}:** {get_level(st.session_state.points)}")
        st.write(f"**{t('badge')}:** {get_badge(st.session_state.points, st.session_state.streak)}")
        st.write(f"**{t('points')}:** {st.session_state.points}")
        st.write(f"**{t('streak')}:** {st.session_state.streak}")

        if st.button(t("logout"), use_container_width=True):
            reset_user()
            st.rerun()

if not st.session_state.show_register and not st.session_state.registered:
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-cloud">
                <div class="hero-mini"></div>
                <div class="hero-title">{t('welcome_big')}</div>
                <div class="hero-sub">{t('welcome_sub')}</div>
                <div class="hero-box-title">{t('hero_box_title')}</div>
                <div class="hero-box-text">{t('hero_box_text')}</div>
                <div class="hero-demo">{t('demo_account')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button(t("start"), use_container_width=True):
            st.session_state.show_register = True
            st.rerun()

if st.session_state.show_register and not st.session_state.registered:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## {t('register_title')}")
    st.caption(t("demo_account"))

    login_tab, signup_tab = st.tabs([t("login_tab"), t("signup_tab")])

    with login_tab:
        login_email = st.text_input(
            t("email"),
            key="login_email",
            placeholder=t("email_ph"),
            help=t("email_help"),
        )
        if st.button(t("login_btn"), key="login_button", use_container_width=True):
            login_email_clean = login_email.strip().lower()
            if not login_email_clean:
                st.warning(t("fill_required"))
            elif not is_valid_email(login_email_clean):
                st.warning(t("email_invalid"))
            else:
                existing_user = st.session_state.saved_users.get(login_email_clean)
                if existing_user:
                    hydrate_session_from_user(existing_user)
                    st.rerun()
                else:
                    st.warning(t("email_not_found"))

    with signup_tab:
        email = st.text_input(
            t("email"),
            key="signup_email",
            placeholder=t("email_ph"),
            help=t("email_help"),
        )
        full_name = st.text_input(t("full_name"))
        age_range = st.selectbox(t("age_range"), t("ages"))
        city = st.text_input(t("city"))
        school_or_job = st.selectbox(t("school_or_job"), t("education_options"))
        goal = st.selectbox(t("goal"), t("goals"))
        transport_habit = st.selectbox(t("transport_habit"), t("transport_habits"))
        climate_interest = st.selectbox(t("climate_interest"), t("climate_interests"))
        carbon_awareness = st.selectbox(t("carbon_awareness"), t("carbon_levels"))
        shopping_style = st.selectbox(t("shopping_style"), t("shopping_options"))
        food_style = st.selectbox(t("food_style"), t("food_options"))
        motivation = st.text_area(t("motivation"))

        if st.button(t("register_btn"), key="register_button", use_container_width=True):
            email_clean = email.strip().lower()
            full_name_clean = full_name.strip()

            if not email_clean or not full_name_clean:
                st.warning(t("fill_required"))
            elif not is_valid_email(email_clean):
                st.warning(t("email_invalid"))
            elif email_clean in st.session_state.saved_users:
                st.warning(t("email_exists"))
            else:
                user_data = {
                    "user_id": email_clean,
                    "points": 0,
                    "streak": 0,
                    "premium": False,
                    "full_name": full_name_clean,
                    "age_range": age_range,
                    "city": city.strip(),
                    "school_or_job": school_or_job,
                    "goal": goal,
                    "transport_habit": transport_habit,
                    "climate_interest": climate_interest,
                    "carbon_awareness": carbon_awareness,
                    "shopping_style": shopping_style,
                    "food_style": food_style,
                    "motivation": motivation.strip(),
                }
                st.session_state.saved_users[email_clean] = user_data
                hydrate_session_from_user(user_data)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.registered:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### {t('welcome')}, {st.session_state.full_name}")
    st.caption(get_quote())
    a, b, c = st.columns(3)
    with a:
        st.metric(t("points"), st.session_state.points)
    with b:
        st.metric(t("streak"), st.session_state.streak)
    with c:
        st.metric(t("score"), st.session_state.score if st.session_state.score is not None else "-")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### {t('analysis_title')}")
    transport = st.selectbox(t("transport"), t("transport_choices"))
    clothes = st.slider(t("clothes"), 0, 10, 2)
    meat = st.slider(t("meat"), 0, 7, 3)
    shower = st.slider(t("shower"), 1, 20, 8)
    takeaway = st.slider(t("takeaway"), 0, 7, 2)
    energy = st.selectbox(t("energy"), t("energy_choices"))

    if st.button(t("analyze"), use_container_width=True):
        st.session_state.score = calculate_score(transport, clothes, meat, shower, takeaway, energy)
        st.session_state.last_analysis = {
            "transport": transport,
            "clothes": clothes,
            "meat": meat,
            "shower": shower,
            "takeaway": takeaway,
            "energy": energy,
        }
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.last_analysis is not None and st.session_state.score is not None:
        last = st.session_state.last_analysis
        score = st.session_state.score
        recommendations = get_recommendations(
            last["transport"],
            last["clothes"],
            last["meat"],
            last["shower"],
            last["takeaway"],
            last["energy"],
        )

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric(t("score"), f"{score}/100")
        st.progress(score / 100)
        st.write(get_message(score))
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.premium:
            bad_path = resolve_image(BAD_FUTURE_CANDIDATES)
            mid_path = resolve_image(MID_FUTURE_CANDIDATES)
            good_path = resolve_image(GOOD_FUTURE_CANDIDATES)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"### {t('future_cmp')}")
            left, middle, right = st.columns(3)
            with left:
                show_image_or_warning(bad_path, t("current_path"))
            with middle:
                show_image_or_warning(mid_path, t("mid_path"))
            with right:
                show_image_or_warning(good_path, t("better_path"))
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"### {t('future_cmp')}")
            st.info(t("future_premium_only"))
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {t('ai_future')}")
        show_image_or_warning(get_image(score), "AI Scenario")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {t('tips')}")
        for item in recommendations:
            st.write(f"- {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.premium:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {t('checklist')}")
        st.markdown(f"#### {t('daily')}")
        for task in st.session_state.daily_tasks:
            st.session_state.daily_tasks[task] = st.checkbox(
                task,
                value=st.session_state.daily_tasks[task],
                key=f"daily_{task}",
            )

        st.markdown(f"#### {t('weekly')}")
        for task in st.session_state.weekly_tasks:
            st.session_state.weekly_tasks[task] = st.checkbox(
                task,
                value=st.session_state.weekly_tasks[task],
                key=f"weekly_{task}",
            )

        st.markdown(f"#### {t('monthly')}")
        for task in st.session_state.monthly_tasks:
            st.session_state.monthly_tasks[task] = st.checkbox(
                task,
                value=st.session_state.monthly_tasks[task],
                key=f"monthly_{task}",
            )
        st.markdown("</div>", unsafe_allow_html=True)

