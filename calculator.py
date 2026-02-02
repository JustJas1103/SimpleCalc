import tkinter as tk
from tkinter import font, messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("500x800")
        self.root.resizable(False, False)
        self.root.configure(bg='#2E2E2E')  # Dark background
        
        self.expression = ""
        self.display_expression = ""  # User-friendly display
        self.history = []  # Calculation history
        
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
        
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.clear_action('←'))
        self.root.bind('<Escape>', lambda e: self.clear_action('C'))
        self.root.focus_set()
    
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
        """Update both displays"""
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
        """Append character to expression"""
        self.expression += str(char)
        self.display_expression += str(char)
        self.update_displays()
        self.status_bar.config(text=f"Added: {char}")
    
    def calculate(self):
        """Calculate the result"""
        try:
            # Evaluate expression with math functions
            result = eval(self.expression, {"__builtins__": None}, {"math": math})
            # Add to history
            self.history.append((self.display_expression, result))
            # Update displays
            self.display_expression = str(result)
            self.expression = str(result)
            self.update_displays()
            self.status_bar.config(text="Calculation complete")
        except ZeroDivisionError:
            self.display_expression = "Error: Division by zero"
            self.expression = ""
            self.update_displays()
            self.status_bar.config(text="Error: Division by zero", fg='#FF6B6B')
        except ValueError as e:
            self.display_expression = f"Math Error: {str(e)}"
            self.expression = ""
            self.update_displays()
            self.status_bar.config(text=f"Math Error: {str(e)}", fg='#FF6B6B')
        except:
            self.display_expression = "Invalid expression"
            self.expression = ""
            self.update_displays()
            self.status_bar.config(text="Invalid expression", fg='#FF6B6B')
    
    def append_function(self, func):
        """Append mathematical function to expression"""
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
        self.status_bar.config(text=f"Function: {func}")
    
    def append_constant(self, const):
        """Append mathematical constant to expression"""
        if const == 'π':
            self.expression += str(math.pi)
            self.display_expression += 'π'
        elif const == 'e':
            self.expression += str(math.e)
            self.display_expression += 'e'
        self.update_displays()
        self.status_bar.config(text=f"Constant: {const}")
    
    def special_action(self, action):
        """Handle special actions"""
        if action == 'Ans' and self.history:
            last_result = self.history[-1][1]
            self.expression += str(last_result)
            self.display_expression += 'Ans'
            self.update_displays()
            self.status_bar.config(text="Inserted last answer")
        elif action == 'Hist':
            self.show_history()
        elif action == '±':
            # Toggle sign of last number
            if self.expression and self.expression[-1].isdigit():
                # Find the last number and negate it
                import re
                match = re.search(r'(\d+\.?\d*)$', self.expression)
                if match:
                    num = float(match.group(1))
                    negated = str(-num)
                    self.expression = self.expression[:-len(match.group(1))] + negated
                    self.display_expression = self.display_expression[:-len(match.group(1))] + negated
                    self.update_displays()
                    self.status_bar.config(text="Sign changed")
    
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
        """Show calculation history"""
        if not self.history:
            messagebox.showinfo("History", "No calculations yet!")
            return
        
        history_text = "Calculation History:\n\n"
        for i, (expr, result) in enumerate(self.history[-10:], 1):  # Show last 10
            history_text += f"{i}. {expr} = {result}\n"
        
        messagebox.showinfo("Calculation History", history_text)
    
    def clear_action(self, action):
        """Handle clear actions"""
        if action == 'C':
            # Clear all
            self.expression = ""
            self.display_expression = ""
            self.update_displays()
            self.status_bar.config(text="Cleared all", fg='#888888')
        elif action == 'CE':
            # Clear entry
            self.expression = ""
            self.display_expression = ""
            self.update_displays()
            self.status_bar.config(text="Cleared entry", fg='#888888')
        elif action == '←':
            # Backspace
            if self.expression:
                self.expression = self.expression[:-1]
                self.display_expression = self.display_expression[:-1]
                self.update_displays()
                self.status_bar.config(text="Backspace", fg='#888888')

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
