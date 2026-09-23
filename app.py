# -*- coding: utf-8 -*-
import streamlit as st
import io
import math
import random
from PIL import Image, ImageDraw

def generate_dobble_combinations(n):
    """Generiert die Symbol-Verteilung nach der endlichen projektiven Ebene."""
    cards = []
    cards.append([i for i in range(n + 1)])
    for j in range(n):
        card = [0]
        for k in range(n):
            card.append(n + 1 + n * j + k)
        cards.append(card)
    for i in range(n):
        for j in range(n):
            card = [i + 1]
            for k in range(n):
                val = n + 1 + n * k + (i * k + j) % n
                card.append(val)
            cards.append(card)
    return cards
'''
#Ohne Verkleinerung der Bilder
def create_dobble_pdf_bytes(uploaded_files, n=5):
    required_images = n**2 + n + 1
    
    images = []
    # Bilder direkt aus dem Streamlit-Upload in den Speicher laden
    for file in uploaded_files[:required_images]:
        images.append(Image.open(file).convert("RGBA"))
        
    card_combinations = generate_dobble_combinations(n)
    
    # DIN A4 Einstellungen bei 300 DPI
    a4_width = 2480
    a4_height = 3508
    card_size = 1100 
    radius = card_size // 2

    margin_x = (a4_width - (2 * card_size)) // 3
    margin_y = (a4_height - (2 * card_size)) // 3

    pages = []
    current_page = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))
    cards_on_current_page = 0
    
    # Ladebalken für die Benutzeroberfläche
    progress_bar = st.progress(0)

    for idx, combination in enumerate(card_combinations):
        card_img = Image.new('RGBA', (card_size, card_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card_img)
        
        draw.ellipse((0, 0, card_size - 1, card_size - 1), 
                     fill=(255, 255, 255, 255), 
                     outline=(0, 0, 0, 255), width=3)
        
        ring_rotation = random.uniform(0, 2 * math.pi)
        centers = []
        centers.append((radius, radius))
        
        ring_radius = radius * 0.55 
        for i in range(5):
            angle = ring_rotation + i * (2 * math.pi / 5)
            x = radius + ring_radius * math.cos(angle)
            y = radius + ring_radius * math.sin(angle)
            centers.append((x, y))
            
        random.shuffle(centers)
        
        for pos, img_index in enumerate(combination):
            icon = images[img_index].copy()
            
            scale_factor = random.uniform(0.6, 1.0)
            max_icon_size = int(radius * 0.65)
            new_size = int(max_icon_size * scale_factor)
            
            icon.thumbnail((new_size, new_size), Image.Resampling.LANCZOS)
            angle = random.uniform(0, 360)
            icon = icon.rotate(angle, expand=True, fillcolor=(0,0,0,0)) 
            
            offset_x = random.uniform(-25, 25)
            offset_y = random.uniform(-25, 25)
            
            cx, cy = centers[pos]
            paste_x = int(cx + offset_x - icon.width / 2)
            paste_y = int(cy + offset_y - icon.height / 2)
            
            card_img.paste(icon, (paste_x, paste_y), icon)
            
        row = cards_on_current_page // 2
        col = cards_on_current_page % 2
        
        x_pos = margin_x + col * (card_size + margin_x)
        y_pos = margin_y + row * (card_size + margin_y)
        
        current_page.paste(card_img, (x_pos, y_pos), card_img)
        cards_on_current_page += 1
        
        if cards_on_current_page == 4 or (idx == len(card_combinations) - 1):
            pages.append(current_page)
            current_page = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))
            cards_on_current_page = 0
            
        # UI aktualisieren
        progress_bar.progress((idx + 1) / len(card_combinations))

    # PDF in den Arbeitsspeicher schreiben
    pdf_buffer = io.BytesIO()
    if pages:
        # format="PDF" ist zwingend nötig, da BytesIO keine Dateiendung hat
        pages[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pages[1:], resolution=300.0)
        
    return pdf_buffer.getvalue()
'''
def create_dobble_pdf_bytes(uploaded_files, n=5):
    required_images = n**2 + n + 1
    
    images = []
    # Bilder laden und SOFORT verkleinern, um RAM zu sparen
    for file in uploaded_files[:required_images]:
        img = Image.open(file).convert("RGBA")
        # 400x400 reicht für die Druckqualität der kleinen Symbole völlig aus
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        images.append(img)
        
    card_combinations = generate_dobble_combinations(n)
    
    # DIN A4 Einstellungen bei 300 DPI
    a4_width = 2480
    a4_height = 3508
    card_size = 1100 
    radius = card_size // 2

    margin_x = (a4_width - (2 * card_size)) // 3
    margin_y = (a4_height - (2 * card_size)) // 3

    pages = []
    current_page = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))
    cards_on_current_page = 0
    
    progress_bar = st.progress(0)

    for idx, combination in enumerate(card_combinations):
        card_img = Image.new('RGBA', (card_size, card_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card_img)
        
        draw.ellipse((0, 0, card_size - 1, card_size - 1), 
                     fill=(255, 255, 255, 255), 
                     outline=(0, 0, 0, 255), width=3)
        
        ring_rotation = random.uniform(0, 2 * math.pi)
        centers = []
        centers.append((radius, radius))
        
        ring_radius = radius * 0.55 
        for i in range(5):
            angle = ring_rotation + i * (2 * math.pi / 5)
            x = radius + ring_radius * math.cos(angle)
            y = radius + ring_radius * math.sin(angle)
            centers.append((x, y))
            
        random.shuffle(centers)
        
        for pos, img_index in enumerate(combination):
            icon = images[img_index].copy()
            
            scale_factor = random.uniform(0.6, 1.0)
            max_icon_size = int(radius * 0.65)
            new_size = int(max_icon_size * scale_factor)
            
            # Da das Bild schon auf max 400x400 vor-verkleinert wurde, 
            # geht dieser Schritt nun blitzschnell und speicherschonend
            icon.thumbnail((new_size, new_size), Image.Resampling.LANCZOS)
            angle = random.uniform(0, 360)
            icon = icon.rotate(angle, expand=True, fillcolor=(0,0,0,0)) 
            
            offset_x = random.uniform(-25, 25)
            offset_y = random.uniform(-25, 25)
            
            cx, cy = centers[pos]
            paste_x = int(cx + offset_x - icon.width / 2)
            paste_y = int(cy + offset_y - icon.height / 2)
            
            card_img.paste(icon, (paste_x, paste_y), icon)
            
        row = cards_on_current_page // 2
        col = cards_on_current_page % 2
        
        x_pos = margin_x + col * (card_size + margin_x)
        y_pos = margin_y + row * (card_size + margin_y)
        
        current_page.paste(card_img, (x_pos, y_pos), card_img)
        cards_on_current_page += 1
        
        if cards_on_current_page == 4 or (idx == len(card_combinations) - 1):
            pages.append(current_page)
            # Wichtig: Speichereffizient leere Seite erstellen
            current_page = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))
            cards_on_current_page = 0
            
        progress_bar.progress((idx + 1) / len(card_combinations))

    pdf_buffer = io.BytesIO()
    if pages:
        pages[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pages[1:], resolution=300.0)
        
    return pdf_buffer.getvalue()
# === STREAMLIT OBERFLÄCHE ===
st.set_page_config(page_title="Horcas Dobble Generator", page_icon="")

st.title("Dobble-Spiel Generator")
st.write("Lade hier deine 31 Bilder hoch. Das Programm generiert daraus mit ziemlich spannender Mathematik eine PDF-Datei.")

# Datei-Upload Widget
uploaded_files = st.file_uploader(
    "Bilder auswaehlen (exakt 31 benoetigt)", 
    type=['png', 'jpg', 'jpeg'], 
    accept_multiple_files=True
)

if uploaded_files:
    # Anzeige, wie viele Bilder bereits hochgeladen wurden
    st.metric(label="Hochgeladene Bilder", value=f"{len(uploaded_files)} / 31")
    
    if len(uploaded_files) >= 31:
        st.success("Alle benoetigten Bilder sind da!")
        
        # Button zum Starten der Generierung
        if st.button("Druck-PDF generieren"):
            with st.spinner("Berechne Kombinationen und layoute Karten..."):
                # Funktion aufrufen, die uns die reinen PDF-Daten zurückgibt
                pdf_bytes = create_dobble_pdf_bytes(uploaded_files, n=5)
                
            st.balloons() # Kleiner visueller Effekt bei Abschluss
            
            # Download-Button anzeigen
            st.download_button(
                label="Fertiges PDF Herunterladen",
                data=pdf_bytes,
                file_name="Danke_Luca_du_bist_ein_Schatz.pdf",
                mime="application/pdf"
            )
    else:
        st.warning(f"Es fehlen noch {31 - len(uploaded_files)} Bilder.")