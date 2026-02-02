import tkinter as tk
from tkinter import font
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#2E2E2E')  # Dark background
        
        self.expression = ""
        
        # Create display
        self.display = tk.Entry(root, font=('Arial', 24), justify='right', 
                               bg='#1E1E1E', fg='white', insertbackground='white')
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        
        # Configure grid weights
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        
        # Button layout
        buttons = [
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3),
            ('ln', 2, 0), ('√', 2, 1), ('x²', 2, 2), ('xʸ', 2, 3),
            ('π', 3, 0), ('e', 3, 1), ('(', 3, 2), (')', 3, 3),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3),
            ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('+', 7, 3),
            ('C', 8, 0), ('CE', 8, 1), ('←', 8, 2), ('!', 8, 3)
        ]
        
        # Create buttons
        button_font = font.Font(family='Arial', size=16, weight='bold')
        for (text, row, col) in buttons:
            if text == '':
                continue
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
            else:
                btn = tk.Button(root, text=text, font=button_font, 
                               command=lambda t=text: self.append(t),
                               bg='#1565C0', fg='white')
            
            btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
    
    def append(self, char):
        """Append character to expression"""
        self.expression += str(char)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)
    
    def calculate(self):
        """Calculate the result"""
        try:
            # Evaluate expression with math functions
            result = eval(self.expression, {"__builtins__": None}, {"math": math})
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.expression = str(result)
        except ZeroDivisionError:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error: Div by 0")
            self.expression = ""
        except ValueError as e:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, f"Math Error: {str(e)}")
            self.expression = ""
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")
            self.expression = ""
    
    def append_function(self, func):
        """Append mathematical function to expression"""
        if func == 'sin':
            self.expression += 'math.sin('
        elif func == 'cos':
            self.expression += 'math.cos('
        elif func == 'tan':
            self.expression += 'math.tan('
        elif func == 'log':
            self.expression += 'math.log10('
        elif func == 'ln':
            self.expression += 'math.log('
        elif func == '√':
            self.expression += 'math.sqrt('
        elif func == 'x²':
            self.expression += '**2'
        elif func == 'xʸ':
            self.expression += '**'
        elif func == '!':
            self.expression += 'math.factorial('
        elif func in ['(', ')']:
            self.expression += func
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)
    
    def append_constant(self, const):
        """Append mathematical constant to expression"""
        if const == 'π':
            self.expression += str(math.pi)
        elif const == 'e':
            self.expression += str(math.e)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
