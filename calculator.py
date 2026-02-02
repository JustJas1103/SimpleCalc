import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2E2E2E')  # Dark background
        
        self.expression = ""
        
        # Create display
        self.display = tk.Entry(root, font=('Arial', 24), justify='right', 
                               bg='#1E1E1E', fg='white', insertbackground='white')
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        
        # Configure grid weights
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        
        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('CE', 5, 1), ('←', 5, 2), ('', 5, 3)
        ]
        
        # Create buttons
        button_font = font.Font(family='Arial', size=18, weight='bold')
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
            elif text in ['+', '-', '*', '/']:
                btn = tk.Button(root, text=text, font=button_font, 
                               command=lambda t=text: self.append(t), 
                               bg='#E65100', fg='white')
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
            result = eval(self.expression)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.expression = str(result)
        except ZeroDivisionError:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error: Div by 0")
            self.expression = ""
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")
            self.expression = ""
    
    def clear_action(self, action):
        """Handle clear actions"""
        if action == 'C':
            # Clear all
            self.expression = ""
            self.display.delete(0, tk.END)
        elif action == 'CE':
            # Clear entry
            self.expression = ""
            self.display.delete(0, tk.END)
        elif action == '←':
            # Backspace
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
