import tkinter as tk
from tkinter import font, messagebox, ttk
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Modern Calculator")
        self.root.geometry("550x850")
        self.root.resizable(False, False)

        # Theme settings
        self.dark_mode = True
        self.themes = {
            'dark': {
                'bg': '#1a1a2e',
                'secondary_bg': '#16213e',
                'accent': '#0f3460',
                'button_bg': '#533483',
                'button_hover': '#6b46a3',
                'text': '#ffffff',
                'text_secondary': '#b0b0b0',
                'success': '#4ade80',
                'error': '#f87171',
                'warning': '#fbbf24'
            },
            'light': {
                'bg': '#f8fafc',
                'secondary_bg': '#ffffff',
                'accent': '#e2e8f0',
                'button_bg': '#6366f1',
                'button_hover': '#4f46e5',
                'text': '#1e293b',
                'text_secondary': '#64748b',
                'success': '#10b981',
                'error': '#ef4444',
                'warning': '#f59e0b'
            }
        }

        self.apply_theme()
        self.expression = ""
        self.display_expression = ""
        self.history = []

        self.create_header()
        self.create_display()
        self.create_buttons()
        self.create_footer()

        # Bind events
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.clear_action('←'))
        self.root.bind('<Escape>', lambda e: self.clear_action('C'))
        
        # Create display frame
        display_frame = tk.Frame(root, bg='#2E2E2E')
        display_frame.grid(row=0, column=0, columnspan=5, sticky='nsew', padx=10, pady=5)
        
        # Main display (shows result)
        self.display = tk.Entry(display_frame, font=('Arial', 28), justify='right', 
                               bg='#1E1E1E', fg='white', insertbackground='white', 
                               state='readonly')
        self.display.pack(fill='both', expand=True, pady=(0, 5))
        
        # Expression display (shows current input)
        self.expression_display = tk.Entry(display_frame, font=('Arial', 16), justify='right',
                                          bg='#252525', fg='#CCCCCC', insertbackground='white',
                                          state='readonly')
        self.expression_display.pack(fill='both', expand=True)
        
        # Status bar
        self.status_bar = tk.Label(root, text="Ready", bg='#2E2E2E', fg='#888888', 
                                  font=('Arial', 10), anchor='w')
        self.status_bar.grid(row=1, column=0, columnspan=5, sticky='ew', padx=10, pady=(0, 10))
        
        # Configure grid weights
        for i in range(2, 11):  # Rows 2-10 for buttons
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):  # 5 columns now
            self.root.grid_columnconfigure(i, weight=1)
        
        # Button layout - more intuitive organization
        buttons = [
            # Row 2: Trigonometric functions
            ('sin', 2, 0), ('cos', 2, 1), ('tan', 2, 2), ('π', 2, 3), ('e', 2, 4),
            # Row 3: Logarithmic and roots
            ('log', 3, 0), ('ln', 3, 1), ('√', 3, 2), ('x²', 3, 3), ('xʸ', 3, 4),
            # Row 4: Parentheses and factorial
            ('(', 4, 0), (')', 4, 1), ('!', 4, 2), ('C', 4, 3), ('CE', 4, 4),
            # Row 5: Numbers and operations
            ('7', 5, 0), ('8', 5, 1), ('9', 5, 2), ('/', 5, 3), ('←', 5, 4),
            ('4', 6, 0), ('5', 6, 1), ('6', 6, 2), ('*', 6, 3), ('Ans', 6, 4),
            ('1', 7, 0), ('2', 7, 1), ('3', 7, 2), ('-', 7, 3), ('Hist', 7, 4),
            ('0', 8, 0), ('.', 8, 1), ('=', 8, 2), ('+', 8, 3), ('±', 8, 4),
        ]
        
        # Create buttons
        button_font = font.Font(family='Arial', size=14, weight='bold')
        self.button_tooltips = {
            'sin': 'Sine function', 'cos': 'Cosine function', 'tan': 'Tangent function',
            'log': 'Logarithm base 10', 'ln': 'Natural logarithm', '√': 'Square root',
            'x²': 'Square (x²)', 'xʸ': 'Power (x^y)', '!': 'Factorial',
            'π': 'Pi constant', 'e': 'Euler\'s number', 'Ans': 'Last answer',
            'Hist': 'Show history', '±': 'Change sign', '←': 'Backspace'
        }
        
        for (text, row, col) in buttons:
            if text == '=':
                btn = tk.Button(root, text=text, font=button_font, 
                               command=self.calculate, bg='#2E7D32', fg='white')
            elif text in ['C', 'CE', '←']:
                btn = tk.Button(root, text=text, font=button_font, 
                               command=lambda t=text: self.clear_action(t), 
                               bg='#B71C1C', fg='white')
            elif text in ['+', '-', '*', '/', 'sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'xʸ', '!', '(', ')']:
                btn = tk.Button(root, text=text, font=button_font, 
                               command=lambda t=text: self.append_function(t), 
                               bg='#7B1FA2', fg='white')
            elif text in ['π', 'e']:
                btn = tk.Button(root, text=text, font=button_font, 
                               command=lambda t=text: self.append_constant(t), 
                               bg='#FF6F00', fg='white')
            elif text in ['Ans', 'Hist', '±']:
                btn = tk.Button(root, text=text, font=button_font, 
                               command=lambda t=text: self.special_action(t), 
                               bg='#FF9800', fg='white')
            else:
                btn = tk.Button(root, text=text, font=button_font, 
                               command=lambda t=text: self.append(t),
                               bg='#1565C0', fg='white')
            
            btn.grid(row=row, column=col, sticky='nsew', padx=3, pady=3)
            
            # Add tooltip
            if text in self.button_tooltips:
                self.create_tooltip(btn, self.button_tooltips[text])
        
        self.root.focus_set()
    
    def apply_theme(self):
        """Apply the current theme"""
        theme = self.themes['dark' if self.dark_mode else 'light']
        self.root.configure(bg=theme['bg'])
        self.current_theme = theme
    
    def create_header(self):
        """Create the header with title and theme toggle"""
        header_frame = tk.Frame(self.root, bg=self.current_theme['bg'], height=60)
        header_frame.grid(row=0, column=0, columnspan=5, sticky='ew', padx=20, pady=(20, 10))
        header_frame.grid_propagate(False)

        # Title
        title_label = tk.Label(header_frame, text="🧮 Modern Calculator",
                              font=('Segoe UI', 18, 'bold'), fg=self.current_theme['text'],
                              bg=self.current_theme['bg'])
        title_label.pack(side='left')

        # Theme toggle button
        self.theme_btn = tk.Button(header_frame, text="☀️" if self.dark_mode else "🌙",
                                  font=('Segoe UI', 12), bg=self.current_theme['button_bg'],
                                  fg='white', relief='flat', padx=10, pady=5,
                                  command=self.toggle_theme)
        self.theme_btn.pack(side='right')
        self.create_button_hover_effect(self.theme_btn, self.current_theme['button_hover'])
    
    def create_display(self):
        """Create the modern display area"""
        display_frame = tk.Frame(self.root, bg=self.current_theme['secondary_bg'],
                                relief='flat', bd=0)
        display_frame.grid(row=1, column=0, columnspan=5, sticky='nsew', padx=20, pady=(0, 20))

        # Expression display (current input)
        self.expression_display = tk.Entry(display_frame, font=('Consolas', 14),
                                          justify='right', bg=self.current_theme['accent'],
                                          fg=self.current_theme['text_secondary'],
                                          insertbackground=self.current_theme['text'],
                                          relief='flat', bd=0, state='readonly')
        self.expression_display.pack(fill='x', padx=15, pady=(15, 5), ipady=8)

        # Main display (result)
        self.display = tk.Entry(display_frame, font=('Segoe UI', 32, 'bold'),
                               justify='right', bg=self.current_theme['secondary_bg'],
                               fg=self.current_theme['text'], insertbackground=self.current_theme['text'],
                               relief='flat', bd=0, state='readonly')
        self.display.pack(fill='x', padx=15, pady=(5, 15), ipady=10)

        # Status bar
        self.status_bar = tk.Label(display_frame, text="✨ Welcome! Start calculating...",
                                  bg=self.current_theme['secondary_bg'],
                                  fg=self.current_theme['text_secondary'],
                                  font=('Segoe UI', 10), anchor='center')
        self.status_bar.pack(fill='x', padx=15, pady=(0, 10))
    
    def create_buttons(self):
        """Create modern styled buttons"""
        # Configure grid
        for i in range(2, 12):  # Rows 2-11 for buttons
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

        # Button configurations
        button_config = {
            'sin': {'text': 'sin', 'bg': self.current_theme['button_bg'], 'icon': '📐'},
            'cos': {'text': 'cos', 'bg': self.current_theme['button_bg'], 'icon': '📐'},
            'tan': {'text': 'tan', 'bg': self.current_theme['button_bg'], 'icon': '📐'},
            'π': {'text': 'π', 'bg': '#ff6b6b', 'icon': '🥧'},
            'e': {'text': 'e', 'bg': '#ff6b6b', 'icon': 'ℯ'},
            'log': {'text': 'log', 'bg': self.current_theme['button_bg'], 'icon': '📊'},
            'ln': {'text': 'ln', 'bg': self.current_theme['button_bg'], 'icon': '📈'},
            '√': {'text': '√', 'bg': self.current_theme['button_bg'], 'icon': '📏'},
            'x²': {'text': 'x²', 'bg': self.current_theme['button_bg'], 'icon': '🔳'},
            'xʸ': {'text': 'xʸ', 'bg': self.current_theme['button_bg'], 'icon': '⬆️'},
            '(': {'text': '(', 'bg': '#4ecdc4', 'icon': '('},
            ')': {'text': ')', 'bg': '#4ecdc4', 'icon': ')'},
            '!': {'text': '!', 'bg': self.current_theme['button_bg'], 'icon': '❗'},
            'C': {'text': 'C', 'bg': '#ff4757', 'icon': '🗑️'},
            'CE': {'text': 'CE', 'bg': '#ff4757', 'icon': '🔄'},
            '7': {'text': '7', 'bg': '#3742fa', 'icon': '7'},
            '8': {'text': '8', 'bg': '#3742fa', 'icon': '8'},
            '9': {'text': '9', 'bg': '#3742fa', 'icon': '9'},
            '/': {'text': '/', 'bg': '#ffa502', 'icon': '➗'},
            '←': {'text': '←', 'bg': '#ff4757', 'icon': '⬅️'},
            '4': {'text': '4', 'bg': '#3742fa', 'icon': '4'},
            '5': {'text': '5', 'bg': '#3742fa', 'icon': '5'},
            '6': {'text': '6', 'bg': '#3742fa', 'icon': '6'},
            '*': {'text': '*', 'bg': '#ffa502', 'icon': '✖️'},
            'Ans': {'text': 'Ans', 'bg': '#2ed573', 'icon': '💡'},
            '1': {'text': '1', 'bg': '#3742fa', 'icon': '1'},
            '2': {'text': '2', 'bg': '#3742fa', 'icon': '2'},
            '3': {'text': '3', 'bg': '#3742fa', 'icon': '3'},
            '-': {'text': '-', 'bg': '#ffa502', 'icon': '➖'},
            'Hist': {'text': 'Hist', 'bg': '#2ed573', 'icon': '📚'},
            '0': {'text': '0', 'bg': '#3742fa', 'icon': '0'},
            '.': {'text': '.', 'bg': '#3742fa', 'icon': '•'},
            '=': {'text': '=', 'bg': '#2ed573', 'icon': '✅'},
            '+': {'text': '+', 'bg': '#ffa502', 'icon': '➕'},
            '±': {'text': '±', 'bg': '#ffa502', 'icon': '🔄'}
        }

        # Button layout
        buttons = [
            ('sin', 2, 0), ('cos', 2, 1), ('tan', 2, 2), ('π', 2, 3), ('e', 2, 4),
            ('log', 3, 0), ('ln', 3, 1), ('√', 3, 2), ('x²', 3, 3), ('xʸ', 3, 4),
            ('(', 4, 0), (')', 4, 1), ('!', 4, 2), ('C', 4, 3), ('CE', 4, 4),
            ('7', 5, 0), ('8', 5, 1), ('9', 5, 2), ('/', 5, 3), ('←', 5, 4),
            ('4', 6, 0), ('5', 6, 1), ('6', 6, 2), ('*', 6, 3), ('Ans', 6, 4),
            ('1', 7, 0), ('2', 7, 1), ('3', 7, 2), ('-', 7, 3), ('Hist', 7, 4),
            ('0', 8, 0), ('.', 8, 1), ('=', 8, 2), ('+', 8, 3), ('±', 8, 4),
        ]

        self.button_tooltips = {
            'sin': 'Sine function 📐', 'cos': 'Cosine function 📐', 'tan': 'Tangent function 📐',
            'log': 'Logarithm base 10 📊', 'ln': 'Natural logarithm 📈', '√': 'Square root 📏',
            'x²': 'Square (x²) 🔳', 'xʸ': 'Power (x^y) ⬆️', '!': 'Factorial ❗',
            'π': 'Pi constant 🥧', 'e': 'Euler\'s number ℯ', 'Ans': 'Last answer 💡',
            'Hist': 'Show history 📚', '±': 'Change sign 🔄', '←': 'Backspace ⬅️',
            'C': 'Clear all 🗑️', 'CE': 'Clear entry 🔄', '=': 'Calculate ✅'
        }

        for (text, row, col) in buttons:
            config = button_config[text]
            btn = tk.Button(self.root, text=f"{config['icon']}\n{config['text']}",
                           font=('Segoe UI', 10, 'bold'), bg=config['bg'], fg='white',
                           relief='flat', bd=0, padx=5, pady=5, command=self.get_button_command(text))

            btn.grid(row=row, column=col, sticky='nsew', padx=3, pady=3)
            self.create_button_hover_effect(btn, self.adjust_color_brightness(config['bg'], 1.2))

            # Add tooltip
            if text in self.button_tooltips:
                self.create_tooltip(btn, self.button_tooltips[text])
    
    def create_footer(self):
        """Create footer with helpful info"""
        footer_frame = tk.Frame(self.root, bg=self.current_theme['bg'], height=40)
        footer_frame.grid(row=12, column=0, columnspan=5, sticky='ew', padx=20, pady=(10, 20))
        footer_frame.grid_propagate(False)

        help_text = tk.Label(footer_frame, text="💡 Tip: Use keyboard shortcuts! Press 's' for sin, 'c' for cos, etc.",
                            bg=self.current_theme['bg'], fg=self.current_theme['text_secondary'],
                            font=('Segoe UI', 9))
        help_text.pack(expand=True)
    
    def create_button_hover_effect(self, button, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)

        def on_leave(e):
            # Reset to original color based on button text
            original_color = self.get_button_original_color(button.cget('text').split('\n')[-1])
            button.config(bg=original_color)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def get_button_original_color(self, text):
        """Get the original color for a button"""
        color_map = {
            'sin': self.current_theme['button_bg'], 'cos': self.current_theme['button_bg'],
            'tan': self.current_theme['button_bg'], 'π': '#ff6b6b', 'e': '#ff6b6b',
            'log': self.current_theme['button_bg'], 'ln': self.current_theme['button_bg'],
            '√': self.current_theme['button_bg'], 'x²': self.current_theme['button_bg'],
            'xʸ': self.current_theme['button_bg'], '(': '#4ecdc4', ')': '#4ecdc4',
            '!': self.current_theme['button_bg'], 'C': '#ff4757', 'CE': '#ff4757',
            '7': '#3742fa', '8': '#3742fa', '9': '#3742fa', '/': '#ffa502', '←': '#ff4757',
            '4': '#3742fa', '5': '#3742fa', '6': '#3742fa', '*': '#ffa502', 'Ans': '#2ed573',
            '1': '#3742fa', '2': '#3742fa', '3': '#3742fa', '-': '#ffa502', 'Hist': '#2ed573',
            '0': '#3742fa', '.': '#3742fa', '=': '#2ed573', '+': '#ffa502', '±': '#ffa502'
        }
        return color_map.get(text, self.current_theme['button_bg'])
    
    def adjust_color_brightness(self, color, factor):
        """Adjust color brightness"""
        # Simple color adjustment for hover effects
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))

            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def create_tooltip(self, widget, text):
        """Create a modern tooltip"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+15}+{event.y_root+15}")

            label = tk.Label(tooltip, text=text, bg='#333333', fg='white',
                           font=('Segoe UI', 9), relief='solid', borderwidth=1,
                           padx=8, pady=4)
            label.pack()

            def hide_tooltip():
                tooltip.destroy()

            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())

        widget.bind('<Enter>', show_tooltip)
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()

        # Update all UI elements
        self.root.configure(bg=self.current_theme['bg'])
        self.theme_btn.config(text="☀️" if self.dark_mode else "🌙")

        # Update header
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=self.current_theme['bg'])
            elif isinstance(child, tk.Label):
                if "Modern Calculator" in child.cget('text'):
                    child.configure(bg=self.current_theme['bg'], fg=self.current_theme['text'])
                elif "Tip:" in child.cget('text'):
                    child.configure(bg=self.current_theme['bg'], fg=self.current_theme['text_secondary'])

        # Update displays
        self.expression_display.configure(bg=self.current_theme['accent'],
                                        fg=self.current_theme['text_secondary'])
        self.display.configure(bg=self.current_theme['secondary_bg'],
                              fg=self.current_theme['text'])
        self.status_bar.configure(bg=self.current_theme['secondary_bg'],
                                 fg=self.current_theme['text_secondary'])

        # Update buttons (this is complex, so we'll recreate them)
        self.create_buttons()
    
    def get_button_command(self, text):
        """Get the appropriate command for a button"""
        if text == '=':
            return self.calculate
        elif text in ['C', 'CE', '←']:
            return lambda: self.clear_action(text)
        elif text in ['+', '-', '*', '/', 'sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'xʸ', '!', '(', ')']:
            return lambda: self.append_function(text)
        elif text in ['π', 'e']:
            return lambda: self.append_constant(text)
        elif text in ['Ans', 'Hist', '±']:
            return lambda: self.special_action(text)
        else:
            return lambda: self.append(text)
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, bg='#FFFFE0', fg='black', 
                           font=('Arial', 10), relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)
    
    def update_displays(self):
        """Update both displays with modern styling"""
        self.expression_display.config(state='normal')
        self.expression_display.delete(0, tk.END)
        self.expression_display.insert(tk.END, self.display_expression)
        self.expression_display.config(state='readonly')
        
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        if self.expression:
            try:
                result = eval(self.expression, {"__builtins__": None}, {"math": math})
                self.display.insert(tk.END, str(result))
            except:
                self.display.insert(tk.END, "")
        self.display.config(state='readonly')
    
    def append(self, char):
        """Append character to expression with visual feedback"""
        self.expression += str(char)
        self.display_expression += str(char)
        self.update_displays()
        self.status_bar.config(text=f"✨ Added: {char}", fg=self.current_theme['success'])
        self.animate_button_press()
    
    def calculate(self):
        """Calculate with enhanced feedback and celebration"""
        try:
            result = eval(self.expression, {"__builtins__": None}, {"math": math})
            self.history.append((self.display_expression, result))
            self.display_expression = str(result)
            self.expression = str(result)
            self.update_displays()
            self.status_bar.config(text="🎉 Calculation complete!", fg=self.current_theme['success'])
            self.animate_success()
        except ZeroDivisionError:
            self.display_expression = "🚫 Cannot divide by zero!"
            self.expression = ""
            self.update_displays()
            self.status_bar.config(text="❌ Division by zero", fg=self.current_theme['error'])
        except ValueError as e:
            self.display_expression = f"🚫 Math error: {str(e)}"
            self.expression = ""
            self.update_displays()
            self.status_bar.config(text=f"❌ Math error: {str(e)}", fg=self.current_theme['error'])
        except:
            self.display_expression = "🚫 Invalid expression"
            self.expression = ""
            self.update_displays()
            self.status_bar.config(text="❌ Invalid expression", fg=self.current_theme['error'])
    
    def append_function(self, func):
        """Append mathematical function with enhanced display"""
        if func == 'sin':
            self.expression += 'math.sin('
            self.display_expression += 'sin('
        elif func == 'cos':
            self.expression += 'math.cos('
            self.display_expression += 'cos('
        elif func == 'tan':
            self.expression += 'math.tan('
            self.display_expression += 'tan('
        elif func == 'log':
            self.expression += 'math.log10('
            self.display_expression += 'log('
        elif func == 'ln':
            self.expression += 'math.log('
            self.display_expression += 'ln('
        elif func == '√':
            self.expression += 'math.sqrt('
            self.display_expression += '√('
        elif func == 'x²':
            self.expression += '**2'
            self.display_expression += '²'
        elif func == 'xʸ':
            self.expression += '**'
            self.display_expression += '^'
        elif func == '!':
            self.expression += 'math.factorial('
            self.display_expression += '!'
        elif func in ['(', ')']:
            self.expression += func
            self.display_expression += func
        self.update_displays()
        self.status_bar.config(text=f"🔧 Function: {func}", fg=self.current_theme['warning'])
    
    def append_constant(self, const):
        """Append mathematical constant with celebration"""
        if const == 'π':
            self.expression += str(math.pi)
            self.display_expression += 'π'
        elif const == 'e':
            self.expression += str(math.e)
            self.display_expression += 'e'
        self.update_displays()
        self.status_bar.config(text=f"🎯 Constant: {const}", fg=self.current_theme['success'])
    
    def special_action(self, action):
        """Handle special actions with enhanced feedback"""
        if action == 'Ans' and self.history:
            last_result = self.history[-1][1]
            self.expression += str(last_result)
            self.display_expression += 'Ans'
            self.update_displays()
            self.status_bar.config(text="💡 Used last answer!", fg=self.current_theme['success'])
        elif action == 'Hist':
            self.show_history()
        elif action == '±':
            if self.expression and self.expression[-1].isdigit():
                import re
                match = re.search(r'(\d+\.?\d*)$', self.expression)
                if match:
                    num = float(match.group(1))
                    negated = str(-num)
                    self.expression = self.expression[:-len(match.group(1))] + negated
                    self.display_expression = self.display_expression[:-len(match.group(1))] + negated
                    self.update_displays()
                    self.status_bar.config(text="🔄 Sign changed!", fg=self.current_theme['warning'])
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        char = event.char
        if char.isdigit() or char in '+-*/.()':
            self.append(char)
        elif char in ['s', 'c', 't', 'l', 'r']:  # First letters of functions
            if char == 's':
                self.append_function('sin')
            elif char == 'c':
                self.append_function('cos')
            elif char == 't':
                self.append_function('tan')
            elif char == 'l':
                self.append_function('log')
            elif char == 'r':
                self.append_function('√')
    
    def show_history(self):
        """Show calculation history with modern styling"""
        if not self.history:
            messagebox.showinfo("📚 Calculation History", "✨ No calculations yet!\nStart calculating to build your history.")
            return
        
        history_text = "📚 Your Calculation History:\n" + "="*40 + "\n\n"
        for i, (expr, result) in enumerate(self.history[-15:], 1):  # Show last 15
            history_text += f"#{len(self.history)-15+i:2d}. {expr:20} = {result}\n"
        
        history_text += "\n💡 Tip: Use 'Ans' button to reuse results!"
        messagebox.showinfo("📚 Calculation History", history_text)
    
    def clear_action(self, action):
        """Handle clear actions with enhanced feedback"""
        if action == 'C':
            self.expression = ""
            self.display_expression = ""
            self.update_displays()
            self.status_bar.config(text="🗑️ Cleared all", fg=self.current_theme['text_secondary'])
        elif action == 'CE':
            self.expression = ""
            self.display_expression = ""
            self.update_displays()
            self.status_bar.config(text="🔄 Cleared entry", fg=self.current_theme['text_secondary'])
        elif action == '←':
            if self.expression:
                self.expression = self.expression[:-1]
                self.display_expression = self.display_expression[:-1]
                self.update_displays()
                self.status_bar.config(text="⬅️ Backspace", fg=self.current_theme['text_secondary'])
    
    def animate_button_press(self):
        """Subtle animation for button presses"""
        # Could add more sophisticated animations here
        pass
    
    def animate_success(self):
        """Celebration animation for successful calculations"""
        # Could add confetti or other effects here
        # For now, just change the status temporarily
        def reset_status():
            self.status_bar.config(text="✨ Ready for next calculation!", fg=self.current_theme['text_secondary'])
        
        self.root.after(2000, reset_status)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ModernCalculator(root)
    root.mainloop()
