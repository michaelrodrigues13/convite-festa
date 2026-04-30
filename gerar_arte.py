import os

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
except ImportError:
    print("Erro: Biblioteca Pillow não encontrada.")
    exit(1)

# Caminhos
img_bg_path = "quintal.png"
img_micha_path = "foto_micha.jpeg"
out_path = "arte_whatsapp.jpg"

if not os.path.exists(img_bg_path) or not os.path.exists(img_micha_path):
    print("Erro: As imagens 'quintal.png' e 'foto_micha.jpeg' são necessárias.")
    exit(1)

print("Gerando Arte Estática (Capa de Vinil)...")

w, h = 1080, 1080

# 1. PREPARAR O FUNDO (quintal.png)
bg = Image.open(img_bg_path).convert("RGBA")
size = min(bg.width, bg.height)
left = (bg.width - size) / 2
top = (bg.height - size) / 2
bg = bg.crop((left, top, left + size, top + size))
bg = bg.resize((w, h), Image.Resampling.LANCZOS)

converter = ImageEnhance.Brightness(bg)
bg = converter.enhance(0.35) 

vintage_overlay = Image.new("RGBA", (w, h), (10, 15, 10, 50))
bg = Image.alpha_composite(bg, vintage_overlay)

# 2. PREPARAR A FOTO CENTRAL (Selo do Vinil)
micha = Image.open(img_micha_path).convert("RGBA")
m_size = min(micha.width, micha.height)
m_left = (micha.width - m_size) / 2
m_top = (micha.height - m_size) / 2
micha = micha.crop((m_left, m_top, m_left + m_size, m_top + m_size))

circle_size = 560
micha = micha.resize((circle_size, circle_size), Image.Resampling.LANCZOS)

mask = Image.new("L", (circle_size, circle_size), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.ellipse((0, 0, circle_size, circle_size), fill=255)
micha.putalpha(mask)

center_x = (w - circle_size) // 2
center_y = (h - circle_size) // 2 - 80 
bg.paste(micha, (center_x, center_y), micha)

draw = ImageDraw.Draw(bg)

# Bordas do Selo
draw.ellipse([center_x, center_y, center_x + circle_size, center_y + circle_size], outline=(250, 204, 21, 220), width=4)
draw.ellipse([center_x - 8, center_y - 8, center_x + circle_size + 8, center_y + circle_size + 8], outline=(255, 255, 255, 40), width=1)

# Desgaste Ring Wear
draw.ellipse([(35, 35), (w-35, h-35)], outline=(255, 255, 255, 15), width=6)
draw.ellipse([(45, 45), (w-45, h-45)], outline=(0, 0, 0, 30), width=3)

# Degradê Inferior
overlay = Image.new("RGBA", (w, h), (0,0,0,0))
draw_overlay = ImageDraw.Draw(overlay)
for y in range(int(h * 0.5), h):
    alpha = int(245 * ((y - h * 0.5) / (h * 0.5)))
    draw_overlay.line([(0, y), (w, y)], fill=(10, 10, 10, alpha))
bg = Image.alpha_composite(bg, overlay)

draw = ImageDraw.Draw(bg)

try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 110)
    font_tagline = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
    font_regular = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 25)
    font_stereo = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    font_link = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 25)
except:
    font_title = font_tagline = font_regular = font_stereo = font_link = ImageFont.load_default()

site_gold = (250, 204, 21, 255)
site_white = (255, 255, 255, 255)

# Textos Clássicos
draw.text((50, 50), "STEREO\n33 ⅓ RPM", font=font_stereo, fill=site_white)
draw.text((w - 150, 50), "LADO A\nFaixa 1", font=font_stereo, fill=site_white, align="right")

def center_text(d, text, font, y, color, shadow=True):
    bbox = d.textbbox((0, 0), text, font=font)
    x = (w - (bbox[2] - bbox[0])) / 2
    if shadow: d.text((x+3, y+3), text, font=font, fill=(0,0,0,220))
    d.text((x, y), text, font=font, fill=color)

# Tipografia Principal
center_text(draw, "SAMBA, RESENHA & CERVEJA GELADA", font_tagline, h - 380, site_gold)
center_text(draw, "QUINTAL DO MICHA", font_title, h - 330, site_white)
center_text(draw, "17 DE MAIO | DOMINGO ÀS 13H | BAIRRO SÃO MARCOS", font_regular, h - 190, site_white)

# Chamada para o Link (no lugar do botão do PDF)
center_text(draw, "CONFIRME PRESENÇA ACESSANDO O LINK ABAIXO:", font_tagline, h - 110, site_gold)
center_text(draw, "convite-festa-kdqetm6a95vnqfnkzvfacq.streamlit.app", font_link, h - 60, site_white)

# Salvar
bg.convert("RGB").save(out_path, quality=95)
print(f"Sucesso! Arte estática salva em {out_path}")
