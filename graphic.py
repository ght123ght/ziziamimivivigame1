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

        