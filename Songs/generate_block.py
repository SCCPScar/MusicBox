"""
generate_block.py

Transforma a capa de album de uma musica (imagem normal, ex: print/download
do Spotify) num "bloco" fofo estilo Minecraft, para usar no music player.

COMO USAR
---------
1. Instala a Pillow (so precisas de fazer isto uma vez):
     pip install pillow

2. Guarda as capas de album numa pasta, por exemplo "covers/", com o nome
   IGUAL ao "id" da faixa em playlist.js. Exemplo:
     covers/anavitoria-ai-amor.jpg
     covers/bts-dimple.png

   (o "id" de cada faixa esta em playlist.js, campo "id")

3. Corre este script:
     python generate_block.py covers/ assets/images/blocks/

   Isto vai criar um bloco .png para cada capa encontrada, dentro de
   assets/images/blocks/ -- exatamente onde o playlist.js espera encontrar.

COMO FUNCIONA (explicacao simples)
-----------------------------------
Um bloco de Minecraft e basicamente um cubo visto em perspetiva isometrica:
- a face de CIMA e mais clara (recebe mais luz)
- a face da ESQUERDA e a cor "normal"
- a face da DIREITA e mais escura (sombra)

O script faz 3 coisas com a capa de album:
1. Reduz a imagem para poucos pixels (ex: 8x8) e volta a aumentar sem suavizar
   -> isto cria o efeito "pixelado" (pixel art) a partir da capa original.
2. Usa essa mini-imagem pixelada como textura da face de CIMA do bloco.
3. Escurece essa mesma paleta de cores para gerar as faces da esquerda e
   direita, dando o efeito 3D de bloco.

O resultado e um bloco reconhecivel (mantem as cores da capa original) mas
com a cara de Minecraft.
"""

import sys
import os
from PIL import Image, ImageEnhance, ImageDraw

PIXEL_SIZE = 8          # resolucao da pixelizacao (8x8 = bem "blocky")
OUTPUT_SIZE = 256        # tamanho final do bloco em pixels (quadrado)
TOP_HEIGHT_RATIO = 0.5   # quanto da altura total e a face de cima


def pixelate(img: Image.Image, pixel_size: int) -> Image.Image:
    """Reduz e amplia a imagem para criar o efeito pixel art."""
    small = img.resize((pixel_size, pixel_size), Image.BILINEAR)
    return small.resize((pixel_size, pixel_size), Image.NEAREST)


def make_face(pixelated: Image.Image, size: int, brightness: float) -> Image.Image:
    """Amplia a textura pixelada para o tamanho da face e ajusta o brilho."""
    face = pixelated.resize((size, size), Image.NEAREST)
    if brightness != 1.0:
        face = ImageEnhance.Brightness(face).enhance(brightness)
    return face


def build_block(cover_path: str, out_path: str) -> None:
    cover = Image.open(cover_path).convert("RGB")
    # corta para quadrado (usa o centro da imagem)
    w, h = cover.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    cover = cover.crop((left, top, left + side, top + side))

    pixelated = pixelate(cover, PIXEL_SIZE)

    canvas = Image.new("RGBA", (OUTPUT_SIZE, OUTPUT_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    top_h = int(OUTPUT_SIZE * TOP_HEIGHT_RATIO)
    side_h = OUTPUT_SIZE - top_h
    half_w = OUTPUT_SIZE // 2

    # --- face de cima (mais clara) ---
    top_face = make_face(pixelated, OUTPUT_SIZE, brightness=1.25)
    canvas.paste(top_face, (0, 0))

    # --- face esquerda (cor normal) ---
    left_face = make_face(pixelated, half_w, brightness=0.85)
    canvas.paste(left_face.crop((0, 0, half_w, side_h)), (0, top_h))

    # --- face direita (mais escura, sombra) ---
    right_face = make_face(pixelated, half_w, brightness=0.55)
    canvas.paste(right_face.crop((0, 0, half_w, side_h)), (half_w, top_h))

    # --- contorno pixelado escuro, estilo Minecraft ---
    outline_color = (30, 25, 20, 255)
    draw.rectangle([0, 0, OUTPUT_SIZE - 1, OUTPUT_SIZE - 1], outline=outline_color, width=4)
    draw.line([(0, top_h), (OUTPUT_SIZE, top_h)], fill=outline_color, width=4)
    draw.line([(half_w, top_h), (half_w, OUTPUT_SIZE)], fill=outline_color, width=4)

    canvas.save(out_path)


def main():
    if len(sys.argv) != 3:
        print("Uso: python generate_block.py <pasta_das_capas> <pasta_de_saida>")
        sys.exit(1)

    covers_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    valid_ext = (".jpg", ".jpeg", ".png", ".webp")
    found = 0
    for filename in sorted(os.listdir(covers_dir)):
        if filename.lower().endswith(valid_ext):
            track_id = os.path.splitext(filename)[0]
            in_path = os.path.join(covers_dir, filename)
            out_path = os.path.join(out_dir, f"{track_id}.png")
            build_block(in_path, out_path)
            print(f"OK  {filename}  ->  {out_path}")
            found += 1

    if found == 0:
        print(f"Nenhuma imagem encontrada em {covers_dir}")
    else:
        print(f"\n{found} blocos gerados em {out_dir}")


if __name__ == "__main__":
    main()
