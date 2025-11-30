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