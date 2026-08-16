# Farm Player 🌾

Mini player de musica desktop, sempre visivel por cima das outras janelas (widget flutuante).
Visual cozy estilo **Stardew Valley** misturado com bordas **blocky/pixeladas** ao estilo
Minecraft, decorado com **lirios**.

Stack: Electron + Vite + HTML/CSS/JS puro (sem framework).

## Instalar

```bash
npm install
```

## Correr em modo dev

Isto arranca o Vite (dev server em `http://localhost:5173`) e abre a janela Electron
ligada a esse servidor, com hot reload:

```bash
npm run start
```

Se preferires correr cada parte manualmente em dois terminais:

```bash
# terminal 1
npm run dev

# terminal 2 (depois do Vite arrancar)
npm run electron
```

## Build

```bash
npm run build
```

Gera os ficheiros estaticos em `dist/`. Com `dist/` gerado, `npm run electron`
carrega a build em vez do dev server (ver `main.cjs`, controlado por `app.isPackaged`).

## Adicionar musicas

1. Coloca os ficheiros `.mp3` dentro de `assets/audio/`.
2. Edita `src/playlist.js` e acrescenta uma entrada por musica:

   ```js
   export const playlist = [
     { title: "Nome da musica", artist: "Nome do artista", file: "assets/audio/nome-do-ficheiro.mp3" },
   ];
   ```

Enquanto o array estiver vazio, a interface mostra "Nenhuma musica adicionada"
no lugar do "now playing".

## Onde trocar cada imagem

Todas as imagens vivem em `assets/images/`. Enquanto um ficheiro nao existir, o
CSS (`src/style.css`) mostra um placeholder desenhado so com CSS (cores/gradientes
que seguem a paleta farm/blocky). Assim que colocares um ficheiro com o **mesmo
nome** na pasta, ele passa a aparecer automaticamente por cima do placeholder —
**nao e preciso mexer no codigo**.

| Ficheiro                       | Onde aparece                                              |
| ------------------------------ | ----------------------------------------------------------- |
| `frame.png`                    | Moldura exterior da janela (estilo tabuas de madeira)       |
| `window_button_close.png`      | Botao de fechar a janela (canto superior direito)           |
| `window_button_min.png`        | Botao de minimizar a janela                                 |
| `window_button_max.png`        | Botao de maximizar (reservado para uso futuro)               |
| `button_prev.png`               | Botao "faixa anterior"                                       |
| `button_play.png`               | Botao "play" (estado parado)                                  |
| `button_pause.png`              | Botao "pause" (estado a tocar)                                |
| `button_next.png`               | Botao "proxima faixa"                                        |
| `progress_bar_bg.png`          | Fundo da barra de progresso (estilo barra de XP)              |
| `progress_bar_fill.png`        | Preenchimento da barra de progresso                          |
| `lily_icon.png`                 | Icone de lirio (titlebar + marcador na barra de progresso)   |
| `album_placeholder.png`        | Ilustracao central (radio/jukebox na casa de fazenda)         |

## Funcionalidades

- Janela sem moldura do SO, sempre no topo (`alwaysOnTop`)
- Arrastar a janela pela titlebar
- Fechar / minimizar via botoes da titlebar
- Play / pause, faixa anterior / seguinte
- Barra de progresso clicavel (clicar avança para esse ponto da musica)
- Nome da musica, artista, tempo atual e duracao total
- Mensagem "Nenhuma musica adicionada" quando a playlist esta vazia

## Estrutura

```
farm-player/
├── main.cjs           # processo principal do Electron
├── preload.cjs         # ponte segura (contextBridge) para a interface
├── index.html
├── src/
│   ├── app.js           # logica do player (audio, controlos, progresso)
│   ├── playlist.js       # array de musicas
│   └── style.css         # tema visual farm/blocky
└── assets/
    ├── images/           # imagens (ver tabela acima)
    └── audio/             # ficheiros .mp3
```
