#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Spectrum Equalizer

@Author: Otkupman D.G.
@Description: color gradient divider with GUI
@License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from colorsys import hsv_to_rgb, rgb_to_hsv, rgb_to_hls
import pyperclip
import webbrowser
import math

class SpectrumDivider:
    def __init__(self, root):
        self.root = root
        self.root.title("Spectrum Equalizer: Color Gradient Divider ©ODVk")
        self.root.geometry("800x600")
        self.root.minsize(700, 165)
        
        # Set application icon
        icon = "iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAACfSURBVEhL7ZYxCsJAEEU/ewytIuixxDZFzrAsmNMINmm320YPkwPEZvyzpLQZyKaQefDCbBj+bwdCSikSYxQAm6l5mqtAh19LW6n5IefMma8LHekbmD/AgytXeqirHR3oRPljoj09CY7MutEnnbHw+6J3eq65mh9SSvXRCs0P69wULzHhJSa8xISXmPASE39UwqtiHdtQ8/e4Vna4u0S+506xyGRzk5QAAAAASUVORK5CYII="
        img = tk.PhotoImage(data=icon)
        self.root.tk.call("wm", "iconphoto", root._w, img)
        
        # Default colors and settings
        self.start_color = (255, 0, 0)
        self.end_color = (127, 0, 255)
        self.algorithm_var = tk.StringVar(value="linear")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main control panel
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill=tk.X)
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(control_frame, text="Algorithm")
        algo_frame.pack(side=tk.LEFT)
        
        tk.Radiobutton(
            algo_frame, 
            text="Linear", 
            variable=self.algorithm_var, 
            value="linear"
        ).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(
            algo_frame, 
            text="Circular", 
            variable=self.algorithm_var, 
            value="circular"
        ).pack(side=tk.LEFT)
        
        # Color selection controls
        color_select_frame = tk.Frame(control_frame)
        color_select_frame.pack(side=tk.LEFT, padx=10)
        
        # Start color controls
        self.start_color_btn = tk.Button(
            color_select_frame, 
            text="Start", 
            command=lambda: self.choose_color('start')
        )
        self.start_color_btn.pack(side=tk.LEFT, padx=5)
        
        # Color preview displays
        self.start_color_display = tk.Canvas(
            color_select_frame, 
            width=20, 
            height=20, 
            bg=self.rgb_to_hex(self.start_color),
            relief="sunken",
            borderwidth=2
        )
        self.start_color_display.pack(side=tk.LEFT, padx=5)

        tk.Label(color_select_frame, text="→").pack(side=tk.LEFT)

        # End color controls
        self.end_color_display = tk.Canvas(
            color_select_frame, 
            width=20, 
            height=20, 
            bg=self.rgb_to_hex(self.end_color),
            relief="sunken",
            borderwidth=2
        )
        self.end_color_display.pack(side=tk.LEFT, padx=5)
        
        self.end_color_btn = tk.Button(
            color_select_frame, 
            text="End", 
            command=lambda: self.choose_color('end')
        )
        self.end_color_btn.pack(side=tk.LEFT, padx=5)
        
        # Number of colors input
        input_frame = tk.Frame(control_frame)
        input_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(input_frame, text="Colors:").pack(side=tk.LEFT)
        self.num_colors_entry = tk.Entry(input_frame, width=5)
        self.num_colors_entry.pack(side=tk.LEFT, padx=5)
        self.num_colors_entry.insert(0, "22")
        self.num_colors_entry.bind('<Return>', lambda event: self.generate_colors()) # Enter
        
        # Action buttons
        btn_frame = tk.Frame(control_frame)
        btn_frame.pack(side=tk.LEFT, padx=10)
        
        generate_btn = tk.Button(
            btn_frame, 
            text="Generate", 
            borderwidth=5, 
            command=self.generate_colors
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        copy_all_btn = tk.Button(
            btn_frame, 
            text="Copy all", 
            command=self.copy_all_colors, 
            borderwidth=3, 
            relief="ridge"
        )
        copy_all_btn.pack(side=tk.LEFT)
        
        # Developer link
        link_frame = tk.Frame(control_frame)
        link_frame.pack(side=tk.RIGHT)
        
        def open_github(event):
            webbrowser.open_new(r"https://github.com/Otkupman")
            
        github_link = tk.Label(
            link_frame, 
            text="GitHub", 
            fg="blue", 
            cursor="hand2",
            font=('Arial', 10, 'underline')
        )
        github_link.pack()
        github_link.bind("<Button-1>", open_github)
        
        # Main display area
        display_frame = tk.Frame(self.root)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Color spectrum display
        self.canvas = tk.Canvas(
            display_frame, 
            bg='black', 
            height=39,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.X, pady=(0, 5))
        
        # Color information table
        table_frame = tk.Frame(display_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(
            table_frame, 
            columns=('RGB', 'HEX', 'HSV', 'HSL', 'CMYK'), 
            show='headings',
            selectmode='browse'
        )
        
        # Configure table columns with equal width
        col_width = 130
        columns = ['RGB', 'HEX', 'HSV', 'HSL', 'CMYK']
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='w', width=col_width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, 
            orient="vertical", 
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu for copying options
        self.context_menu = tk.Menu(self.root, tearoff=0)
        for option in columns:
            self.context_menu.add_command(
                label=f"Copy {option}", 
                command=lambda o=option: self.copy_color(o.lower())
            )
        
        # Bind events
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.copy_on_double_click)
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to HEX string"""
        return "#%02x%02x%02x" % rgb
    
    def rgb_to_cmyk(self, rgb):
        """Convert RGB to CMYK percentages"""
        r, g, b = [x/255 for x in rgb]
        
        if (r, g, b) == (0, 0, 0):
            return (0, 0, 0, 100)
            
        k = 1 - max(r, g, b)
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        
        return (
            round(c * 100, 1),
            round(m * 100, 1),
            round(y * 100, 1),
            round(k * 100, 1)
        )
    
    def get_text_color(self, bg_rgb):
        """Calculate optimal text color (black or white) based on background color"""
        # Calculate relative luminance (per ITU-R BT.709)
        r, g, b = [x/255 for x in bg_rgb]
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return 'black' if luminance > 0.4 else 'white'
    
    def choose_color(self, which):
        """Open color picker dialog and update selected color"""
        color = colorchooser.askcolor(title=f"Choose {which} color")
        if color[0]:
            rgb = tuple(int(c) for c in color[0])
            hex_color = color[1]
            if which == 'start':
                self.start_color = rgb
                self.start_color_display.config(bg=hex_color)
            else:
                self.end_color = rgb
                self.end_color_display.config(bg=hex_color)
    
    def generate_colors(self, event=None):
        """Generate gradient colors between start and end colors using selected algorithm"""
        try:
            num_colors = int(self.num_colors_entry.get())
            if num_colors < 1:
                raise ValueError("Must be positive number")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return
        
        # Clear previous results
        self.canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Convert colors to HSV for interpolation
        start_hsv = rgb_to_hsv(*[x/255 for x in self.start_color])
        end_hsv = rgb_to_hsv(*[x/255 for x in self.end_color])
        
        # Generate gradient colors
        self.colors = []
        for i in range(num_colors):
            ratio = i / (num_colors - 1) if num_colors > 1 else 0
            
            if self.algorithm_var.get() == "linear":
                # Linear interpolation through HSV space
                hue = start_hsv[0] + (end_hsv[0] - start_hsv[0]) * ratio
                sat = start_hsv[1] + (end_hsv[1] - start_hsv[1]) * ratio
                val = start_hsv[2] + (end_hsv[2] - start_hsv[2]) * ratio
                
                # Simple hue wrapping
                hue = hue % 1.0
            else:
                # Circular interpolation - shortest path around color wheel
                hue = self.interpolate_hue_circular(start_hsv[0], end_hsv[0], ratio)
                sat = start_hsv[1] + (end_hsv[1] - start_hsv[1]) * ratio
                val = start_hsv[2] + (end_hsv[2] - start_hsv[2]) * ratio
            
            # Convert back to RGB
            r, g, b = hsv_to_rgb(hue, sat, val)
            rgb = (int(r*255), int(g*255), int(b*255))
            
            # Calculate all color representations
            hsv = (round(hue*360, 1), round(sat*100, 1), round(val*100, 1))
            h, l, s = rgb_to_hls(r, g, b)
            hsl = (round(h*360, 1), round(s*100, 1), round(l*100, 1))
            cmyk = self.rgb_to_cmyk(rgb)
            
            self.colors.append((rgb, hsv, hsl, cmyk))
        
        # Display color spectrum
        self.draw_spectrum()
        
        # Populate color table
        self.fill_color_table()
    
    def interpolate_hue_circular(self, start, end, ratio):
        """Interpolate hue taking shortest path around color wheel"""
        # Calculate shortest path
        if abs(end - start) > 0.5:
            if start < end:
                start += 1
            else:
                end += 1
                
        hue = start + (end - start) * ratio
        
        # Wrap around if needed
        return hue % 1
    
    def draw_spectrum(self):
        """Draw the color spectrum gradient"""
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 1:  # Default width if window not rendered yet
            canvas_width = 800
        
        num_colors = len(self.colors)
        color_width = canvas_width / num_colors
        
        for i, (rgb, *_) in enumerate(self.colors):
            x1 = i * color_width
            x2 = (i+1) * color_width
            color_hex = self.rgb_to_hex(rgb)
            self.canvas.create_rectangle(
                x1, 0, x2, 40, 
                fill=color_hex, 
                outline=color_hex,
                width=0
            )
    
    def fill_color_table(self):
        """Fill the table with color information and set appropriate text colors"""
        for i, (rgb, hsv, hsl, cmyk) in enumerate(self.colors):
            rgb_str = f"{rgb[0]}, {rgb[1]}, {rgb[2]}"
            hex_str = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            hsv_str = f"{hsv[0]}°, {hsv[1]}%, {hsv[2]}%"
            hsl_str = f"{hsl[0]}°, {hsl[1]}%, {hsl[2]}%"
            cmyk_str = f"{cmyk[0]}%, {cmyk[1]}%, {cmyk[2]}%, {cmyk[3]}%"
            
            color_hex = self.rgb_to_hex(rgb)
            text_color = self.get_text_color(rgb)
            
            self.tree.insert(
                '', 'end', 
                values=(rgb_str, hex_str, hsv_str, hsl_str, cmyk_str), 
                tags=(color_hex,)
            )
            self.tree.tag_configure(
                color_hex, 
                background=color_hex,
                foreground=text_color
            )
    
    def show_context_menu(self, event):
        """Show context menu on right click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def copy_on_double_click(self, event):
        """Copy HEX code on double click"""
        self.copy_color('hex')
    
    def copy_color(self, mode):
        """Copy color value to clipboard in specified format"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item_index = self.tree.index(selected_item[0])
        color_data = self.colors[item_index]
        rgb = color_data[0]
        
        if mode == 'rgb':
            text = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
        elif mode == 'hex':
            text = self.rgb_to_hex(rgb)
        elif mode == 'hsv':
            hsv = color_data[1]
            text = f"hsv({hsv[0]}°, {hsv[1]}%, {hsv[2]}%)"
        elif mode == 'hsl':
            hsl = color_data[2]
            text = f"hsl({hsl[0]}°, {hsl[1]}%, {hsl[2]}%)"
        elif mode == 'cmyk':
            cmyk = color_data[3]
            text = f"cmyk({cmyk[0]}%, {cmyk[1]}%, {cmyk[2]}%, {cmyk[3]}%)"
        
        pyperclip.copy(text)
        messagebox.showinfo(
            "Copied", 
            f"Value copied to clipboard:\n{text}",
            parent=self.root
        )
    
    def copy_all_colors(self):
        """Copy all colors to clipboard in all formats"""
        if not hasattr(self, 'colors') or not self.colors:
            messagebox.showwarning(
                "Error", 
                "Generate colors first",
                parent=self.root
            )
            return
        
        color_list = []
        for i, (rgb, hsv, hsl, cmyk) in enumerate(self.colors):
            color_list.append(
                f"Color {i+1}:\n"
                f"RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}\n"
                f"HEX: {self.rgb_to_hex(rgb)}\n"
                f"HSV: {hsv[0]}°, {hsv[1]}%, {hsv[2]}%\n"
                f"HSL: {hsl[0]}°, {hsl[1]}%, {hsl[2]}%\n"
                f"CMYK: {cmyk[0]}%, {cmyk[1]}%, {cmyk[2]}%, {cmyk[3]}%"
            )
        
        pyperclip.copy("\n\n".join(color_list))
        messagebox.showinfo(
            "Copied", 
            "All colors copied to clipboard",
            parent=self.root
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = SpectrumDivider(root)
    root.mainloop()