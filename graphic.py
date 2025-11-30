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

        