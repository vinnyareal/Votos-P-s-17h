import os
import sys
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

W, H = 1080, 1920
FPS = 25

AUDIO_PATH = r"c:\Users\Vinicius\analise-eleicoes-2026\video\narracao_antonio.mp3"
OUTPUT_VIDEO = r"c:\Users\Vinicius\analise-eleicoes-2026\video\analise_eleicoes_2026_vertical.mp4"
TEMP_VIDEO = r"c:\Users\Vinicius\analise-eleicoes-2026\video\temp_no_audio.mp4"
TOTAL_DURATION = 68.42
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

print(f"Gerando vídeo vertical (9:16) com Voz Neural de {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames a {FPS} FPS)...")

# Fontes
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 62)
FONT_HEADING = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 46)
FONT_BIG_NUM = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 96)
FONT_REGULAR = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 34)
FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 38)
FONT_BADGE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28)
FONT_CAPTION = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 32)

SCENES = [
    {
        "start": 0.0,
        "end": 10.5,
        "tag": "ELEIÇÕES 2026 • 2º TURNO",
        "title": "O QUE HOUVE COM OS VOTOS\nAPURADOS APÓS AS 17H?",
        "subtitle": "A verdade matemática dos dados oficiais do TSE",
        "caption": "O que realmente aconteceu com os votos apurados depois das 5 da tarde no segundo turno de ontem? Vamos aos fatos e aos dados oficiais do TSE."
    },
    {
        "start": 10.5,
        "end": 24.5,
        "tag": "TOTALIZAÇÃO FINAL TSE",
        "title": "PLACAR OFICIAL CONSOLIDADO",
        "subtitle": "100% das urnas apuradas no Brasil",
        "caption": "Lula foi reeleito com mais de 64 milhões de votos contra 59,8 milhões de Flávio Bolsonaro — uma vantagem de mais de 4,4 milhões de votos."
    },
    {
        "start": 24.5,
        "end": 40.5,
        "tag": "DECISÃO JUDICIAL • 16H32",
        "title": "POR QUE HOUVE EXTENSÃO?",
        "subtitle": "Liminar do Min. Zanin (STF) autorizou voto até 19h",
        "caption": "Às 16h30, o Min. Zanin autorizou voto até 19h apenas onde faltou transporte na Bahia e por fortes chuvas no RJ. Seções normais fecharam às 17h."
    },
    {
        "start": 40.5,
        "end": 53.5,
        "tag": "LEVANTAMENTO OFICIAL",
        "title": "O NÚMERO REAL PÓS-17H",
        "subtitle": "34.330 votos em todo o território nacional",
        "caption": "Apenas 34.330 votos registrados no Brasil inteiro após as 17h. Isso é 0,03% dos votos válidos e menos de 1% da vantagem do vencedor."
    },
    {
        "start": 53.5,
        "end": TOTAL_DURATION + 1.0,
        "tag": "VEREDITO MATEMÁTICO",
        "title": "A DINÂMICA DA VIRADA",
        "subtitle": "A alternância das 19h46 e a confirmação às 21h08",
        "caption": "A virada de Lula às 20h24 foi matemática pura com a chegada do Nordeste. O impacto dos votos pós-17h no resultado é simplesmente zero."
    }
]

def get_current_scene(t):
    for i, sc in enumerate(SCENES):
        if sc["start"] <= t < sc["end"]:
            return i, sc
    return len(SCENES) - 1, SCENES[-1]

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def render_frame(frame_idx):
    t = frame_idx / float(FPS)
    scene_idx, scene = get_current_scene(t)
    scene_progress = (t - scene["start"]) / max(0.1, (scene["end"] - scene["start"]))

    img = Image.new("RGB", (W, H), (8, 12, 22))
    draw = ImageDraw.Draw(img)

    # 1. Fundo com gradiente radial sutil
    center_y = int(600 + math.sin(t * 0.8) * 35)
    for r in range(400, 0, -25):
        alpha = int((1 - r / 400.0) * 22)
        draw.ellipse([W//2 - r, center_y - r, W//2 + r, center_y + r], fill=(15 + alpha, 25 + alpha*2, 45 + alpha*3))

    # 2. Barra de Histórias no Topo (Story Progress Bar)
    bar_y = 60
    bar_gap = 14
    total_bars = len(SCENES)
    bar_w = (W - 120 - (total_bars - 1) * bar_gap) / total_bars

    for b in range(total_bars):
        bx1 = 60 + b * (bar_w + bar_gap)
        bx2 = bx1 + bar_w
        draw.rounded_rectangle([bx1, bar_y, bx2, bar_y + 8], radius=4, fill=(40, 50, 70))
        if b < scene_idx:
            draw.rounded_rectangle([bx1, bar_y, bx2, bar_y + 8], radius=4, fill=(56, 189, 248))
        elif b == scene_idx:
            fill_w = bar_w * min(1.0, max(0.0, scene_progress))
            if fill_w > 0:
                draw.rounded_rectangle([bx1, bar_y, bx1 + fill_w, bar_y + 8], radius=4, fill=(56, 189, 248))

    # 3. Badge Superior
    draw_rounded_rect(draw, (W//2 - 250, 110, W//2 + 250, 165), radius=20, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    draw.text((W//2, 137), scene["tag"], font=FONT_BADGE, fill=(56, 189, 248), anchor="mm")

    # 4. Card Central Principal
    card_x1, card_y1, card_x2, card_y2 = 70, 220, W - 70, 1580
    draw_rounded_rect(draw, (card_x1, card_y1, card_x2, card_y2), radius=36, fill=(13, 20, 36), outline=(30, 41, 59), width=3)

    # 5. Conteúdo por cena
    if scene_idx == 0:
        draw.text((W//2, 340), "ELEIÇÕES PRESIDENCIAIS 2026", font=FONT_BADGE, fill=(245, 158, 11), anchor="mm")
        draw.text((W//2, 460), "O QUE REALMENTE HOUVE", font=FONT_TITLE, fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 540), "COM OS VOTOS APÓS AS 17H?", font=FONT_TITLE, fill=(56, 189, 248), anchor="mm")
        draw.line([140, 630, W - 140, 630], fill=(51, 65, 85), width=2)
        
        draw_rounded_rect(draw, (110, 680, W - 110, 1180), radius=28, fill=(19, 30, 52), outline=(56, 189, 248), width=2)
        draw.text((W//2, 750), "AUDITORIA OFICIAL", font=FONT_HEADING, fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 830), "• Dados Oficiais do TSE", font=FONT_SUBTITLE, fill=(148, 163, 184), anchor="mm")
        draw.text((W//2, 910), "• Decisão do STF (Min. Zanin)", font=FONT_SUBTITLE, fill=(148, 163, 184), anchor="mm")
        draw.text((W//2, 990), "• Contagem de Votos e Margem Real", font=FONT_SUBTITLE, fill=(148, 163, 184), anchor="mm")
        draw.text((W//2, 1070), "• Impacto Matemático no Resultado", font=FONT_SUBTITLE, fill=(148, 163, 184), anchor="mm")

        draw_rounded_rect(draw, (140, 1260, W - 140, 1480), radius=24, fill=(30, 41, 59))
        draw.text((W//2, 1340), "PLEITO DE 25 DE OUTUBRO DE 2026", font=FONT_HEADING, fill=(251, 191, 36), anchor="mm")
        draw.text((W//2, 1410), "Tribunal Superior Eleitoral", font=FONT_REGULAR, fill=(203, 213, 225), anchor="mm")

    elif scene_idx == 1:
        draw.text((W//2, 300), "TOTALIZAÇÃO FINAL (100%)", font=FONT_HEADING, fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 360), "124.082.273 votos válidos apurados", font=FONT_REGULAR, fill=(148, 163, 184), anchor="mm")

        draw_rounded_rect(draw, (110, 430, W - 110, 750), radius=28, fill=(153, 27, 27), outline=(239, 68, 68), width=3)
        draw.text((150, 480), "Lula (PT) — REELEITO", font=FONT_HEADING, fill=(255, 255, 255), anchor="lt")
        draw.text((150, 560), "51,79%", font=FONT_BIG_NUM, fill=(255, 255, 255), anchor="lt")
        draw.text((150, 680), "64.256.232 votos", font=FONT_SUBTITLE, fill=(254, 202, 202), anchor="lt")

        draw_rounded_rect(draw, (110, 800, W - 110, 1120), radius=28, fill=(30, 58, 138), outline=(59, 130, 246), width=3)
        draw.text((150, 850), "Flávio Bolsonaro (PL)", font=FONT_HEADING, fill=(255, 255, 255), anchor="lt")
        draw.text((150, 930), "48,21%", font=FONT_BIG_NUM, fill=(255, 255, 255), anchor="lt")
        draw.text((150, 1050), "59.826.041 votos", font=FONT_SUBTITLE, fill=(191, 219, 254), anchor="lt")

        draw_rounded_rect(draw, (110, 1180, W - 110, 1480), radius=28, fill=(15, 23, 42), outline=(245, 158, 11), width=3)
        draw.text((W//2, 1240), "VANTAGEM DE LULA", font=FONT_BADGE, fill=(245, 158, 11), anchor="mm")
        draw.text((W//2, 1330), "+4.430.191 VOTOS", font=FONT_HEADING, fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 1410), "Margem segura e irreversível de 3,58%", font=FONT_REGULAR, fill=(148, 163, 184), anchor="mm")

    elif scene_idx == 2:
        draw.text((W//2, 300), "A LIMINAR DO STF ÀS 16H32", font=FONT_HEADING, fill=(168, 85, 247), anchor="mm")
        draw.text((W//2, 360), "Entenda as regras de prorrogação até 19h", font=FONT_REGULAR, fill=(148, 163, 184), anchor="mm")

        cards_info = [
            ("TRANSPORTE E CHUVAS", "Falta comprovada de ônibus na Bahia e fortes\nchuvas no Rio de Janeiro retiveram eleitores.", (56, 189, 248)),
            ("URNAS FECHADAS ÀS 17H", "Seções que já haviam fechado às 17h foram\nmantidas lacradas. Não houve reabertura.", (234, 179, 8)),
            ("APENAS FILAS EM CURSO", "Votação estendida até 19h somente para quem\njá estava na fila com senha oficial.", (16, 185, 129))
        ]

        for idx, (head, desc, color) in enumerate(cards_info):
            cy = 440 + idx * 350
            draw_rounded_rect(draw, (110, cy, W - 110, cy + 300), radius=24, fill=(19, 27, 46), outline=color, width=2)
            draw.text((150, cy + 45), f"0{idx+1}. {head}", font=FONT_HEADING, fill=color, anchor="lt")
            for li, line in enumerate(desc.split('\n')):
                draw.text((150, cy + 125 + li * 55), line, font=FONT_SUBTITLE, fill=(226, 232, 240), anchor="lt")

    elif scene_idx == 3:
        draw.text((W//2, 300), "QUANTOS VOTOS FORAM?", font=FONT_HEADING, fill=(52, 211, 153), anchor="mm")
        draw.text((W//2, 360), "Levantamento oficial dos logs das urnas eletrônicas", font=FONT_REGULAR, fill=(148, 163, 184), anchor="mm")

        draw_rounded_rect(draw, (110, 430, W - 110, 770), radius=32, fill=(6, 78, 59), outline=(52, 211, 153), width=3)
        draw.text((W//2, 530), "34.330", font=ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 120), fill=(110, 231, 183), anchor="mm")
        draw.text((W//2, 650), "VOTOS COMPUTADOS APÓS AS 17H", font=FONT_HEADING, fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 720), "Apenas 0,028% do eleitorado nacional", font=FONT_REGULAR, fill=(209, 250, 229), anchor="mm")

        draw_rounded_rect(draw, (110, 830, W - 110, 1500), radius=28, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
        draw.text((W//2, 890), "COMPARAÇÃO PROPORCIONAL DIRETA", font=FONT_HEADING, fill=(255, 255, 255), anchor="mm")

        draw.text((150, 970), "Vantagem de Lula: 4.430.191 votos (100%)", font=FONT_SUBTITLE, fill=(56, 189, 248), anchor="lt")
        draw_rounded_rect(draw, (150, 1030, W - 150, 1110), radius=16, fill=(2, 132, 199))

        draw.text((150, 1170), "Votos pós-17h: 34.330 votos (0,77% da margem)", font=FONT_SUBTITLE, fill=(239, 68, 68), anchor="lt")
        bar_w_rel = max(18, int((34330 / 4430191.0) * (W - 300)))
        draw_rounded_rect(draw, (150, 1230, 150 + bar_w_rel, 1310), radius=16, fill=(239, 68, 68))

        draw.text((W//2, 1390), "Mesmo se 100% fossem de Flávio Bolsonaro,", font=FONT_SUBTITLE, fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 1450), "Lula ainda venceria por mais de 4,36 milhões de votos!", font=FONT_HEADING, fill=(245, 158, 11), anchor="mm")

    elif scene_idx == 4:
        draw.text((W//2, 300), "A CRONOLOGIA DA NOITE", font=FONT_HEADING, fill=(56, 189, 248), anchor="mm")
        draw.text((W//2, 360), "Entenda a alternância na apuração", font=FONT_REGULAR, fill=(148, 163, 184), anchor="mm")

        timeline = [
            ("19h46", "Flávio assume liderança temporária", "Sul e Sudeste apuram com maior rapidez inicial.", (59, 130, 246)),
            ("20h24", "Lula retoma a ponta (virada definitiva)", "Entrada massiva das urnas do Nordeste e capitais.", (239, 68, 68)),
            ("21h08", "TSE confirma Lula reeleito", "97,69% apurado com vitória matemática consolidada.", (16, 185, 129))
        ]

        for idx, (hora, evento, detalhe, cor) in enumerate(timeline):
            ty = 430 + idx * 260
            draw_rounded_rect(draw, (110, ty, W - 110, ty + 220), radius=22, fill=(19, 27, 46), outline=cor, width=2)
            draw.text((150, ty + 35), hora, font=FONT_HEADING, fill=cor, anchor="lt")
            draw.text((310, ty + 38), evento, font=FONT_SUBTITLE, fill=(255, 255, 255), anchor="lt")
            draw.text((150, ty + 125), detalhe, font=FONT_REGULAR, fill=(148, 163, 184), anchor="lt")

        draw_rounded_rect(draw, (110, 1260, W - 110, 1500), radius=28, fill=(6, 95, 70), outline=(52, 211, 153), width=3)
        draw.text((W//2, 1340), "✔ VEREDITO AUDITADO", font=FONT_HEADING, fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 1420), "Impacto dos votos pós-17h: RIGOROSAMENTE ZERO", font=FONT_SUBTITLE, fill=(167, 243, 208), anchor="mm")

    # 6. Card da Legenda
    cap_x1, cap_y1, cap_x2, cap_y2 = 60, 1620, W - 60, 1840
    draw_rounded_rect(draw, (cap_x1, cap_y1, cap_x2, cap_y2), radius=24, fill=(10, 15, 28), outline=(56, 189, 248), width=2)
    draw.text((cap_x1 + 30, cap_y1 + 25), "🎙️ LOCUÇÃO / LEGENDA", font=FONT_BADGE, fill=(245, 158, 11), anchor="lt")
    
    cap_text = scene["caption"]
    words = cap_text.split()
    lines = []
    curr_line = ""
    for word in words:
        test = (curr_line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=FONT_CAPTION)
        if bbox[2] - bbox[0] > (W - 180):
            lines.append(curr_line)
            curr_line = word
        else:
            curr_line = test
    if curr_line:
        lines.append(curr_line)

    for li, line in enumerate(lines[:2]):
        draw.text((cap_x1 + 30, cap_y1 + 75 + li * 52), line, font=FONT_CAPTION, fill=(255, 255, 255), anchor="lt")

    return img

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

cmd = [
    ffmpeg_exe,
    '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', f'{W}x{H}',
    '-pix_fmt', 'rgb24',
    '-r', str(FPS),
    '-i', '-',
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '22',
    '-pix_fmt', 'yuv420p',
    TEMP_VIDEO
]

print("Iniciando codificação de vídeo com FFMPEG...")
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

for f in range(TOTAL_FRAMES):
    if f % 150 == 0:
        print(f"Renderizando frame {f}/{TOTAL_FRAMES} ({(f/TOTAL_FRAMES)*100:.1f}%)...")
    img = render_frame(f)
    proc.stdin.write(img.tobytes())

proc.stdin.close()
proc.wait()
print("Codificação de vídeo concluída!")

# Juntar vídeo com o áudio de narração neural
if os.path.exists(AUDIO_PATH):
    print("Combinando vídeo com áudio de narração neural (Antonio)...")
    merge_cmd = [
        ffmpeg_exe,
        '-y',
        '-i', TEMP_VIDEO,
        '-i', AUDIO_PATH,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        OUTPUT_VIDEO
    ]
    subprocess.run(merge_cmd, check=True)
    if os.path.exists(TEMP_VIDEO):
        os.remove(TEMP_VIDEO)
    print(f"VÍDEO FINAL COM VOZ NEURAL GERADO EM: {OUTPUT_VIDEO}")
