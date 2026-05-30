<div align="center">

# 🎮 Elle3ba _ Game

**A fully-featured Python implementation of the classic Quoridor board game**

##  About the Game

**Quoridor** is a two-player abstract strategy game. Each player controls a pawn and must race to the opposite side of the board. On each turn, a player may either:

- 🏃 **Move their pawn** one step (or jump over the opponent)
- 🧱 **Place a wall** to block the opponent's path
- GitHub: https://github.com/MohamedWanis-05/python_quoridor
- Video Demo: https://drive.google.com/drive/folders/15vTs4gQgHzbGLTzBqdQN6E-afAUkI4_d?usp=sharing

> ⚠️ Walls can never completely trap a player — a valid path to the goal must always exist.

---

##  Features

| Feature | Description |
|---|---|
| 🎮 **Two Game Modes** | Player vs Player (1v1) or Player vs AI (1vAI) |
| 📐 **Three Board Sizes** | Choose between 5×5, 7×7, or 9×9 grids |
| 🤖 **AI Difficulty** | Easy and Medium and Hard AI opponents |
| 👻 **Wall Preview** | Ghost wall appears on hover before placing |
| 🟢 **Move Highlights** | Green dots show all legal moves each turn |
| 🔀 **Jump Mechanics** | Jump over opponent, including diagonal jumps |
| 🔍 **BFS Validation** | Walls that trap a player are automatically rejected |
| 📊 **Live UI** | Turn indicators, wall counts, and win messages |
| 🔁 **Quick Reset** | Reset or return to main menu at any time |

---

##  Project Structure

```
Elle3ba-main/
├── main.py                  # Entry point — game loop and event handling
├── requirements.txt         # Python dependencies
│
├── game/
│   ├── board.py             # Board state, player positions, wall placement
│   ├── constants.py         # Colors, tile size, window size, FPS
│   ├── player.py            # Player class (ID + walls remaining)
│   ├── rules.py             # Move resolution, wall checks, winner detection
│
├── ai/
│   ├── easy_ai.py           # Easy AI — BFS pathfinding + random wall blocking
│   ├── medium_ai.py         # Medium AI — defensive walls + shortest-path sprint
|    ├── hard_ai.py           # Hard Minimax with alpha-beta pruning
│   ├── minimax.py
│   └── pathfinding.py       # BFS utility — validates paths remain open
│
├── ui/
│   ├── Homescreen.py        # Main menu (mode, size, difficulty selection)
│   ├── renderer.py          # In-game rendering (grid, players, walls, panel)
```

---

## ⚙ Requirements

| Requirement | Version |
|---|---|
| Python | 3.8 or higher |
| pygame | Latest stable |

---

##  Installation

**1. Clone the repository**
```bash
git clone https://github.com/MohamedWanis-05/python_quoridor
cd ./python_quoridor
```

**2. Install dependencies**
```bash
pip install pygame
```

**3. Run the game**
```bash
python main.py
```

---

## 🕹️ How to Play

| Step | Action |
|---|---|
| 1️⃣ | Launch the game — the **Main Menu** appears |
| 2️⃣ | Choose a **game mode**: 1v1 or 1vAI |
| 3️⃣ | *(AI mode only)* Click the difficulty button to cycle: Easy → Medium → Hard |
| 4️⃣ | Pick a **board size**: 5×5, 7×7, or 9×9 |
| 5️⃣ | Click **START** and race to the other side! |

**On your turn you can:**
- ⌨️ Press a movement key to move your pawn (green dots show valid squares)
- 🖱️ Left-click near an intersection to place a wall (hover to preview it)
- The number on your pawn = your **remaining walls**

---

## Controls

### Player 1 — Arrow Keys

| Action | Key |
|:---:|:---:|
| Move Up | `↑` |
| Move Down | `↓` |
| Move Left | `←` |
| Move Right | `→` |
| Diagonal Up-Left | `U` |
| Diagonal Up-Right | `O` |
| Diagonal Down-Left | `J` |
| Diagonal Down-Right | `L` |

###  Player 2 — WASD Keys

| Action | Key |
|:---:|:---:|
| Move Up | `W` |
| Move Down | `S` |
| Move Left | `A` |
| Move Right | `D` |
| Diagonal Up-Left | `Q` |
| Diagonal Up-Right | `E` |
| Diagonal Down-Left | `Z` |
| Diagonal Down-Right | `C` |

###  Wall Placement

| Method | How |
|---|---|
| Place a wall | **Left-click** near any grid intersection |
| Preview a wall | **Hover** near an intersection (ghost appears) |
| Orientation | Determined automatically by your cursor's angle to the intersection |

###  In-Game Buttons

| Button | Action |
|---|---|
| 🏠 Main Menu | Return to the main menu |
| 🔁 Reset Game | Restart the current match from scratch |

---

##  AI Difficulty Levels

| Level | Strategy | Wall Usage |
|:---:|---|---|
| 🟢 **Easy** | BFS shortest path to goal row | 25% chance per turn to randomly block the human |
| 🟠 **Medium** | Compares both paths — sprints when ahead, blocks when behind | Targets human's very next step |
| 🔴 **Hard** |  Minimax with alpha-beta pruning | Smart lookahead wall placement |

---

## 🗺 Roadmap

| Status | Feature |
|:---:|---|
| ✅ | 1v1 local multiplayer |
| ✅ | Easy & Medium AI |
| ✅ | Wall ghost preview |
| ✅ | BFS wall validation |
| ✅ | Valid move highlights |
| ✅ | Hard AI (Minimax) |

---








</div>