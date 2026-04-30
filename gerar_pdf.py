import os

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
    from reportlab.pdfgen import canvas
except ImportError:
    print("Erro: Bibliotecas Pillow ou ReportLab não encontradas.")
    exit(1)

# Caminhos
img_bg_path = "quintal.png"
img_micha_path = "foto_micha.jpeg"
out_pdf = "Convite_Micha_Vinil.pdf"

if not os.path.exists(img_bg_path) or not os.path.exists(img_micha_path):
    print(f"Erro: As imagens '{img_bg_path}' ou '{img_micha_path}' não foram encontradas.")
    exit(1)

print("Prensando o Vinil com a Arte Oficial e a Foto do Anfitrião no Centro...")

w, h = 1080, 1080

# 1. PREPARAR O FUNDO (quintal.png)
bg = Image.open(img_bg_path).convert("RGBA")
size = min(bg.width, bg.height)
left = (bg.width - size) / 2
top = (bg.height - size) / 2
bg = bg.crop((left, top, left + size, top + size))
bg = bg.resize((w, h), Image.Resampling.LANCZOS)

# Filtro Premium escuro no fundo para dar destaque ao centro
converter = ImageEnhance.Brightness(bg)
bg = converter.enhance(0.35) 

# Leve textura
vintage_overlay = Image.new("RGBA", (w, h), (10, 15, 10, 50))
bg = Image.alpha_composite(bg, vintage_overlay)

# 2. PREPARAR A FOTO CENTRAL (foto_micha.jpeg em formato circular)
micha = Image.open(img_micha_path).convert("RGBA")
# Crop quadrado focando no centro
m_size = min(micha.width, micha.height)
m_left = (micha.width - m_size) / 2
m_top = (micha.height - m_size) / 2
micha = micha.crop((m_left, m_top, m_left + m_size, m_top + m_size))

# Tamanho do círculo central (ex: 560x560)
circle_size = 560
micha = micha.resize((circle_size, circle_size), Image.Resampling.LANCZOS)

# Criar máscara circular perfeita
mask = Image.new("L", (circle_size, circle_size), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.ellipse((0, 0, circle_size, circle_size), fill=255)
micha.putalpha(mask)

# Posicionamento centralizado (levemente para cima para dar espaço ao texto embaixo)
center_x = (w - circle_size) // 2
center_y = (h - circle_size) // 2 - 80 

# Colar a foto circular no fundo
bg.paste(micha, (center_x, center_y), micha)

draw = ImageDraw.Draw(bg)

# Bordas luxuosas do círculo (Selo de Ouro)
draw.ellipse(
    [center_x, center_y, center_x + circle_size, center_y + circle_size],
    outline=(250, 204, 21, 220), width=4
)
draw.ellipse(
    [center_x - 8, center_y - 8, center_x + circle_size + 8, center_y + circle_size + 8],
    outline=(255, 255, 255, 40), width=1
)

# Marca de desgaste do vinil (Ring Wear na borda externa do disco)
draw.ellipse([(35, 35), (w-35, h-35)], outline=(255, 255, 255, 15), width=6)
draw.ellipse([(45, 45), (w-45, h-45)], outline=(0, 0, 0, 30), width=3)

# Degradê Inferior para destacar a tipografia e o botão
overlay = Image.new("RGBA", (w, h), (0,0,0,0))
draw_overlay = ImageDraw.Draw(overlay)
for y in range(int(h * 0.5), h):
    alpha = int(245 * ((y - h * 0.5) / (h * 0.5)))
    draw_overlay.line([(0, y), (w, y)], fill=(10, 10, 10, alpha))
bg = Image.alpha_composite(bg, overlay)

draw = ImageDraw.Draw(bg)

# Fontes e Tamanhos adequados
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 110)
    font_tagline = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
    font_regular = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 25)
    font_stereo = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
except:
    font_title = font_tagline = font_regular = font_stereo = ImageFont.load_default()

site_gold = (250, 204, 21, 255)
site_white = (255, 255, 255, 255)

# Selos Clássicos do LP
draw.text((50, 50), "STEREO\n33 ⅓ RPM", font=font_stereo, fill=site_white)
draw.text((w - 150, 50), "LADO A\nFaixa 1", font=font_stereo, fill=site_white, align="right")

def center_text(d, text, font, y, color, shadow=True):
    bbox = d.textbbox((0, 0), text, font=font)
    x = (w - (bbox[2] - bbox[0])) / 2
    if shadow:
        d.text((x+3, y+3), text, font=font, fill=(0,0,0,220))
    d.text((x, y), text, font=font, fill=color)

# Tipografia Final
center_text(draw, "SAMBA, RESENHA & CERVEJA GELADA", font_tagline, h - 380, site_gold)
center_text(draw, "QUINTAL DO MICHA", font_title, h - 330, site_white)
center_text(draw, "17 DE MAIO | DOMINGO ÀS 13H | BAIRRO SÃO MARCOS", font_regular, h - 190, site_white)

# Botão Interativo: Padrão Oficial do Site
btn_w, btn_h = 550, 80
btn_x = (w - btn_w) // 2
btn_y = h - 130

# Desenha botão dourado arredondado
draw.rounded_rectangle([btn_x, btn_y, btn_x+btn_w, btn_y+btn_h], radius=40, fill=site_gold)

bbox_btn = draw.textbbox((0, 0), "CONFIRMAR PRESENÇA", font=font_tagline)
tx = btn_x + (btn_w - (bbox_btn[2] - bbox_btn[0])) / 2
ty = btn_y + (btn_h - (bbox_btn[3] - bbox_btn[1])) / 2 - 5
draw.text((tx, ty), "CONFIRMAR PRESENÇA", font=font_tagline, fill=(0,0,0,255))

# Salvar Imagem Final
temp_jpg = "arte_vinil.jpg"
bg.convert("RGB").save(temp_jpg, quality=95)

# 2. GERAR PDF INTERATIVO
pdf_w, pdf_h = 800, 800
c = canvas.Canvas(out_pdf, pagesize=(pdf_w, pdf_h))
c.drawImage(temp_jpg, 0, 0, width=pdf_w, height=pdf_h)

# Link Clicável
url = "https://convite-festa-kdqetm6a95vnqfnkzvfacq.streamlit.app/"
scale_x = pdf_w / w
scale_y = pdf_h / h
rect_x1 = btn_x * scale_x
rect_x2 = (btn_x + btn_w) * scale_x
rect_y1 = (h - (btn_y + btn_h)) * scale_y
rect_y2 = (h - btn_y) * scale_y

c.linkURL(url, (rect_x1, rect_y1, rect_x2, rect_y2), relative=0)
c.save()

if os.path.exists(temp_jpg):
    os.remove(temp_jpg)

print("Sucesso! Vinil Masterpiece gerado com fundo duplo.")
