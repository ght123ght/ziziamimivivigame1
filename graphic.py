import tkinter as tk
from tkinter import ttk, messagebox
import random

class MemoryGameApp:
    def __init__(self, master):
        self.master = master
        master.title("Memory Game")
        master.geometry("900x600")  # Добавил начальный размер окна
        master.minsize(800, 500)  # Минимальный размер окна
        master.configure(bg="#1a1a2e")  # Темно-синий фон по умолчанию, как в первом коде

        # --- Цвета и шрифты ---
        self.colors = {
            'bg': "#1a1a2e",  # Основной цвет фона (темно-синий)
            'sidebar_bg': "#16213e",  # Цвет фона боковой панели (темно-синий)
            'card_bg': "#0f3469",  # Цвет фона карточек (темно-синий, когда закрыты)
            'card_fg': "#e94560",  # Цвет переднего плана карточки (розовато-красный, когда открыты)
            'text': "#ffffff",  # Цвет текста (белый)
            'button_bg': "#4caf50",  # Цвет фона кнопки (зеленый)
            'button_fg': "#ffffff",  # Цвет переднего плана кнопки (белый)
            'combobox_bg': "#32374b",  # Цвет фона выпадающего списка
            'combobox_fg': "#ffffff",  # Цвет переднего плана выпадающего списка
            'gameover_bg': "#0f3460",  # Цвет фона окна Game over (темно-синий)
            'card_matched_bg': "#0a2a47",  # Более темный синий для совпавших карт
            'card_hidden_text': "#1a1a2e",  # Темный цвет для скрытого текста (фон карточки)
            'player1_turn_bg': "#ffd700",  # Золотой для хода Игрока 1
            'player2_turn_bg': "#87ceeb"  # Небесно-голубой для хода Игрока 2 / AI
        }
        self.custom_font = ("Helvetica", 14, "bold")  
        self.card_font = ("Helvetica", 28, "bold")  

        self.difficulty_levels = {
            "Easy": {"grid": (4, 4), "symbols": ["✧", "♡", "？", "❀", "⨳", "◍", "★", "▨"]}, 
            "Medium": {"grid": (4, 5), "symbols": ["✧", "♡", "？", "❀", "⨳", "◍", "★", "▨", "✿", "⬦"]}, 
            "Hard": {"grid": (5, 6), "symbols": ["✧", "♡", "？", "❀", "⨳", "◍", "★", "▨", "✿", "⬦", "ᶻz", "⊹", "✹", "◉", "✄"]}
       
        }
        self.game_modes = ["Single Player", "Two Players", "Player vs. AI"]

        self.current_difficulty = "Easy"
        self.current_game_mode = "Single Player"


        self.style = ttk.Style()
        self._configure_styles()


        self.sidebar = tk.Frame(master, width=250, bg=self.colors['sidebar_bg'])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # Предотвращает изменение размера сайдбара

        self.game_frame = tk.Frame(master, bg=self.colors['bg'])
        self.game_frame.pack(side="right", fill="both", expand=True)

        self.cards_frame = tk.Frame(self.game_frame, bg=self.colors['bg'])
        self.cards_frame.pack(expand=True)  # Карты будут в этой рамке


        self.cards = []
        self.flipped_cards = []
        self.match_count = 0
        self.total_pairs = 0
        self.moves = 0
        self.game_over = False
        self.can_click = True
        self.game_timer_id = None
        self.start_time = None


        self.player_scores = {"Player 1": 0, "Player 2": 0, "Computer": 0}
        self.current_player = "Player 1"
        self.ai_memory = {}

        self.create_sidebar()
        self.start_new_game()


    def _configure_styles(self):

        self.style.theme_create("modern", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": self.colors['combobox_bg'],
                    "fieldbackground": self.colors['combobox_bg'],
                    "background": self.colors['button_bg'],
                    "foreground": self.colors['combobox_fg'],
                    "font": self.custom_font,
                    "bordercolor": self.colors['button_bg'],
                    "arrowcolor": self.colors['button_fg']
                },
                "map": {
                    "background": [("active", self.colors['button_bg'])],
                    "fieldbackground": [("active", self.colors['combobox_bg'])]
                }
            }
        })
        self.style.theme_use("modern")
        self.master.option_add('*TCombobox*Listbox.font', self.custom_font)
        self.master.option_add('*TCombobox*Listbox.selectBackground', self.colors['card_fg'])
        self.master.option_add('*TCombobox*Listbox.selectForeground', self.colors['text'])


    def create_sidebar(self):
       
        title_label = tk.Label(self.sidebar, text="Memory Game",
                               font=("Helvetica", 24, "bold"),
                               bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        title_label.pack(pady=(30, 10))

        subtitle_label = tk.Label(self.sidebar, text="Проверим вашу память!",
                                  font=("Helvetica", 16, "italic"),
                                  bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        subtitle_label.pack(pady=(0, 30))

       
        self.game_mode_label = tk.Label(self.sidebar, text="Game Mode:",
                                        font=self.custom_font,
                                        bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.game_mode_label.pack(pady=(0, 5))

        self.game_mode_combobox = ttk.Combobox(self.sidebar, values=self.game_modes,
                                               state="readonly", font=self.custom_font, width=15)
        self.game_mode_combobox.set(self.current_game_mode)
        self.game_mode_combobox.pack(pady=(0, 10))
        self.game_mode_combobox.bind("<<ComboboxSelected>>", self._on_game_mode_change)

        
        self.difficulty_label = tk.Label(self.sidebar, text="Difficulty:",
                                         font=self.custom_font,
                                         bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.difficulty_label.pack(pady=(0, 5))

        self.difficulty_combobox = ttk.Combobox(self.sidebar, values=list(self.difficulty_levels.keys()),
                                                state="readonly", font=self.custom_font, width=15)
        self.difficulty_combobox.set(self.current_difficulty)
        self.difficulty_combobox.pack(pady=(0, 20))
        self.difficulty_combobox.bind("<<ComboboxSelected>>", self._on_difficulty_change)


       
        self.current_player_label = tk.Label(self.sidebar, text="Ход: Игрок 1",
                                             font=("Helvetica", 16, "bold"),
                                             bg=self.colors['sidebar_bg'], fg=self.colors['player1_turn_bg'])
        self.current_player_label.pack(pady=(10, 5))

        self.player1_score_label = tk.Label(self.sidebar, text="Игрок 1: 0",
                                            font=self.custom_font,
                                            bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.player1_score_label.pack(pady=5)

        self.player2_score_label = tk.Label(self.sidebar, text="Игрок 2: 0",
                                            font=self.custom_font,
                                            bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.player2_score_label.pack(pady=5)

        
        self.moves_label = tk.Label(self.sidebar, text="Попытки: 0",
                                    font=self.custom_font,
                                    bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.moves_label.pack(pady=10)

        self.time_label = tk.Label(self.sidebar, text="Время: 0:00",
                                   font=self.custom_font,
                                   bg=self.colors['sidebar_bg'], fg=self.colors['text'])
        self.time_label.pack(pady=10)

        
        self.new_game_button = tk.Button(self.sidebar, text="Новая Игра",
                                         font=self.custom_font,
                                         bg=self.colors['button_bg'], fg=self.colors['button_fg'],
                                         relief=tk.FLAT,
                                         command=self.start_new_game)
        self.new_game_button.pack(pady=30)
        self.new_game_button.bind("<Enter>", lambda e: e.widget.config(bg="#d816b8"))
        self.new_game_button.bind("<Leave>", lambda e: e.widget.config(bg=self.colors['button_bg']))

        self._update_player_labels_visibility()


    def create_game_grid(self):

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        self.cards = []

        rows, cols = self.difficulty_levels[self.current_difficulty]["grid"]
        symbols = self.difficulty_levels[self.current_difficulty]["symbols"] * 2
        random.shuffle(symbols)

        self.total_pairs = len(symbols) // 2

        for i in range(rows):
            for j in range(cols):

                self.cards_frame.grid_rowconfigure(i, weight=1)
                self.cards_frame.grid_columnconfigure(j, weight=1)

                card_idx = i * cols + j

                card_canvas = tk.Canvas(self.cards_frame, width=80, height=100,
                                        bg=self.colors['card_bg'], highlightthickness=0)
                card_canvas.grid(row=i, column=j, padx=5, pady=5, sticky="nsew") # Added sticky
                card_canvas.bind("<Button-1>", lambda e, idx=card_idx: self.on_card_click(idx))


                card_canvas.create_rectangle(5, 5, 75, 95, fill=self.colors['card_bg'],
                                             outline=self.colors['card_fg'], width=2, tags="border")


                symbol_text_id = card_canvas.create_text(40, 50, text=symbols[card_idx],
                                                         font=self.card_font, 
                                                         fill=self.colors['card_hidden_text'], 
                                                         state=tk.HIDDEN,
                                                         tags="symbol")


                self.cards.append({
                    "canvas": card_canvas,
                    "symbol": symbols[card_idx],
                    "text_id": symbol_text_id,
                    "is_revealed": False,
                    "is_matched": False
                })
                