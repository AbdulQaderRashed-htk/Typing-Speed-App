import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import winsound  # For Windows sound effects
from threading import Thread

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("MonkeyTypingPro")
        self.root.geometry("900x700")
        self.root.configure(bg="#121212")
        self.root.option_add('*TCombobox*Listbox*Background', '#252525')
        self.root.option_add('*TCombobox*Listbox*Foreground', 'white')
        
        # Custom fonts
        self.title_font = ("Segoe UI", 28, "bold")
        self.subtitle_font = ("Segoe UI", 12)
        self.mono_font = ("Consolas", 12)
        self.stats_font = ("Segoe UI", 14)
        
        # Sample texts
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog while programming in Python.",
            "To be or not to be, that is the question that many programmers ask when debugging.",
            "The rain in Spain stays mainly in the plain, just like bugs stay in your code until fixed.",
            "Programming is the art of telling another human what one wants the computer to do.",
            "Four score and seven years ago our fathers brought forth on this continent a new language."
        ]
        
        # Sound effects
        self.sound_on = True
        self.key_sound = lambda: winsound.PlaySound('click.wav', winsound.SND_ASYNC | winsound.SND_FILENAME) if self.sound_on else None
        
        # Create UI
        self.create_widgets()
        
        # Test variables
        self.test_active = False
        self.start_time = None
        self.current_words = []
        self.correct_words = 0
        self.total_words = 0
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#121212")
        header_frame.pack(fill="x", pady=(0, 20))
        
        self.title_label = tk.Label(
            header_frame, 
            text="VelocityType Pro", 
            font=self.title_font, 
            fg="#4facfe", 
            bg="#121212"
        )
        self.title_label.pack(side="left")
        
        # Settings button
        settings_btn = tk.Button(
            header_frame,
            text="⚙️",
            command=self.toggle_sound,
            font=("Segoe UI", 14),
            bg="#252525",
            fg="white",
            bd=0,
            relief="flat",
            padx=10
        )
        settings_btn.pack(side="right")
        
        # Test area container
        test_frame = tk.Frame(main_frame, bg="#252525", bd=0, highlightthickness=0)
        test_frame.pack(fill="both", expand=True)
        
        # Sample text
        sample_container = tk.Frame(test_frame, bg="#252525")
        sample_container.pack(fill="x", pady=(10, 5), padx=10)
        
        tk.Label(
            sample_container, 
            text="TYPE THIS TEXT:", 
            font=self.subtitle_font, 
            fg="#aaaaaa", 
            bg="#252525"
        ).pack(anchor="w")
        
        self.sample_display = tk.Text(
            test_frame, 
            height=6, 
            width=80, 
            font=self.mono_font,
            bg="#252525",
            fg="#ffffff",
            insertbackground="white",
            wrap="word",
            padx=15,
            pady=15,
            bd=0,
            highlightthickness=0
        )
        self.sample_display.pack(fill="x", padx=10, pady=(0, 20))
        self.sample_display.config(state="disabled")
        
        # User input
        input_container = tk.Frame(test_frame, bg="#252525")
        input_container.pack(fill="x", pady=(10, 5), padx=10)
        
        tk.Label(
            input_container, 
            text="YOUR TYPING:", 
            font=self.subtitle_font, 
            fg="#aaaaaa", 
            bg="#252525"
        ).pack(anchor="w")
        
        self.input_display = tk.Text(
            test_frame, 
            height=6, 
            width=80, 
            font=self.mono_font,
            bg="#252525",
            fg="#ffffff",
            insertbackground="white",
            wrap="word",
            padx=15,
            pady=15,
            bd=0,
            highlightthickness=0
        )
        self.input_display.pack(fill="x", padx=10, pady=(0, 20))
        self.input_display.bind("<Key>", self.play_key_sound)
        self.input_display.bind("<KeyRelease>", self.check_progress)
        
        # Stats display
        stats_frame = tk.Frame(test_frame, bg="#252525")
        stats_frame.pack(fill="x", pady=(10, 20), padx=10)
        
        self.wpm_label = self.create_stat_label(stats_frame, "WPM", "0")
        self.accuracy_label = self.create_stat_label(stats_frame, "ACCURACY", "100%")
        self.word_acc_label = self.create_stat_label(stats_frame, "WORD ACC", "100%")
        self.time_label = self.create_stat_label(stats_frame, "TIME", "0.0s")
        
        # Start button
        self.start_button = tk.Button(
            test_frame,
            text="START NEW TEST",
            command=self.start_test,
            font=("Segoe UI", 12, "bold"),
            bg="#4facfe",
            fg="white",
            activebackground="#00f2fe",
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=30,
            pady=12
        )
        self.start_button.pack(pady=(0, 20))
        
        # Results display
        self.results_display = tk.Label(
            test_frame, 
            text="", 
            font=("Segoe UI", 16, "bold"), 
            fg="#4facfe", 
            bg="#252525"
        )
        self.results_display.pack(fill="x", pady=(0, 10))
        
    def create_stat_label(self, parent, title, value):
        frame = tk.Frame(parent, bg="#252525")
        frame.pack(side="left", expand=True)
        
        tk.Label(
            frame, 
            text=title, 
            font=self.subtitle_font, 
            fg="#aaaaaa", 
            bg="#252525"
        ).pack()
        
        label = tk.Label(
            frame, 
            text=value, 
            font=self.stats_font, 
            fg="white", 
            bg="#252525"
        )
        label.pack()
        return label
    
    def play_key_sound(self, event=None):
        if self.sound_on and event.char.isprintable():
            Thread(target=self.key_sound).start()
    
    def toggle_sound(self):
        self.sound_on = not self.sound_on
        message = "Sound: ON" if self.sound_on else "Sound: OFF"
        messagebox.showinfo("Settings", message)
    
    def start_test(self):
        """Start a new typing test"""
        sample_text = random.choice(self.sample_texts)
        self.current_words = sample_text.split()
        self.correct_words = 0
        self.total_words = 0
        
        self.sample_display.config(state="normal")
        self.sample_display.delete(1.0, tk.END)
        
        # Insert with colored tags for word-by-word comparison
        self.sample_display.insert(1.0, sample_text)
        self.sample_display.tag_config("correct", foreground="#4facfe")
        self.sample_display.tag_config("wrong", foreground="#ff6b6b")
        self.sample_display.config(state="disabled")
        
        self.input_display.delete(1.0, tk.END)
        self.input_display.focus_set()
        
        self.start_time = time.time()
        self.test_active = True
        
        # Reset stats
        self.wpm_label.config(text="0")
        self.accuracy_label.config(text="100%")
        self.word_acc_label.config(text="100%")
        self.time_label.config(text="0.0s")
        self.results_display.config(text="")
    
    def check_progress(self, event=None):
        """Check typing progress and update stats"""
        if not self.test_active:
            return
            
        user_text = self.input_display.get(1.0, tk.END).strip()
        sample_text = self.sample_display.get(1.0, tk.END).strip()
        
        # Calculate stats
        elapsed = time.time() - self.start_time
        
        # Character-level accuracy
        correct_chars = 0
        for i in range(min(len(user_text), len(sample_text))):
            if user_text[i] == sample_text[i]:
                correct_chars += 1
        char_accuracy = (correct_chars / len(user_text)) * 100 if user_text else 100
        
        # Word-level accuracy
        user_words = user_text.split()
        correct_words = 0
        for i in range(min(len(user_words), len(self.current_words))):
            if user_words[i] == self.current_words[i]:
                correct_words += 1
        word_accuracy = (correct_words / len(user_words)) * 100 if user_words else 100
        
        # WPM calculation (5 chars = 1 word)
        wpm = (len(user_text) / 5) / (elapsed / 60) if elapsed > 0 else 0
        
        # Update UI
        self.wpm_label.config(text=f"{wpm:.1f}")
        self.accuracy_label.config(text=f"{char_accuracy:.1f}%")
        self.word_acc_label.config(text=f"{word_accuracy:.1f}%")
        self.time_label.config(text=f"{elapsed:.1f}s")
        
        # Check if test is complete
        if len(user_text) >= len(sample_text):
            self.finish_test()
    
    def finish_test(self):
        """Finish the test and show results"""
        self.test_active = False
        elapsed = time.time() - self.start_time
        user_text = self.input_display.get(1.0, tk.END).strip()
        
        # Final calculations
        wpm = (len(user_text) / 5) / (elapsed / 60)
        
        # Character accuracy
        correct_chars = 0
        for i in range(min(len(user_text), len(self.sample_display.get(1.0, tk.END).strip()))):
            if user_text[i] == self.sample_display.get(1.0, tk.END)[i]:
                correct_chars += 1
        char_accuracy = (correct_chars / len(user_text)) * 100
        
        # Word accuracy
        user_words = user_text.split()
        correct_words = 0
        for i in range(min(len(user_words), len(self.current_words))):
            if user_words[i] == self.current_words[i]:
                correct_words += 1
        word_accuracy = (correct_words / len(user_words)) * 100
        
        # Show results
        self.results_display.config(
            text=f"TEST COMPLETE! • {wpm:.1f} WPM • {char_accuracy:.1f}% Accuracy • {word_accuracy:.1f}% Word Accuracy"
        )

if __name__ == "__main__":
    root = tk.Tk()
    
    # Windows 10/11 style
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = TypingSpeedTest(root)
    root.mainloop()