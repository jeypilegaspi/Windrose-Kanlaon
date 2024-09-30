import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Add this import at the top if using an image
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class WindroseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windrose Graph Generator")
        self.root.geometry("800x600")

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create the frames for tool selection and main interface
        self.tool_selection_frame = tk.Frame(root)
        self.create_tool_selection_page()

        # Placeholder for the selected file path and graph list
        self.file_path = None
        self.figures = []
        self.current_fig_index = -1  # Track current figure being displayed

        # Placeholder for the figure canvas
        self.canvas = None

    def create_tool_selection_page(self):
        """Create the initial tool selection page with buttons."""
        self.tool_selection_frame.pack(fill="both", expand=True)

        # Label for tool selection
        label = tk.Label(self.tool_selection_frame, text="Select a Tool", font=("Arial", 16))
        label.pack(pady=20)

        # Button for Windrose Generator
        windrose_btn = tk.Button(self.tool_selection_frame, text="Windrose Generator", command=self.load_windrose_page)
        windrose_btn.pack(pady=10)

        # Button for other tool (Placeholder)
        other_tool_btn = tk.Button(self.tool_selection_frame, text="Other Tool", command=self.run_other_tool)
        other_tool_btn.pack(pady=10)

    def load_windrose_page(self):
        """Load the main page for Windrose Generator."""
        self.tool_selection_frame.pack_forget()
        self.create_windrose_interface()

    def create_windrose_interface(self):
        """Create the interface for Windrose Generator."""
        self.main_frame = tk.Frame(self.root)  # Create a new frame for the windrose generator
        self.main_frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(self.main_frame)
        header_frame.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)

        # Back button (arrow) at the top left corner
        arrow_image = Image.open("arrow_back.png")  # Load your image file
        arrow_image = arrow_image.resize((30, 30), Image.Resampling.LANCZOS)  # Resize if necessary
        arrow_photo = ImageTk.PhotoImage(arrow_image)

        self.back_btn = tk.Button(header_frame, image=arrow_photo, command=self.back_to_selection, borderwidth=0)
        self.back_btn.image = arrow_photo  # Keep a reference to avoid garbage collection
        self.back_btn.pack(side=tk.LEFT)

        # Buttons for file selection and actions
        self.select_file_btn = tk.Button(self.main_frame, text="Select JSON File", command=self.load_file)
        self.select_file_btn.pack(pady=20)

        #self.generate_graph_btn = tk.Button(self.main_frame, text="Generate Graphs", command=self.generate_graphs, state=tk.DISABLED)
        #self.generate_graph_btn.pack(pady=10)

        self.clear_btn = tk.Button(self.main_frame, text="Clear", command=self.clear_graphs, state=tk.DISABLED)
        self.clear_btn.pack(pady=10)

        # Navigation buttons
        self.prev_btn = tk.Button(self.main_frame, text="< Previous", command=self.show_prev_graph, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, padx=10)

        self.next_btn = tk.Button(self.main_frame, text="Next >", command=self.show_next_graph, state=tk.DISABLED)
        self.next_btn.pack(side=tk.RIGHT, padx=10)

    def back_to_selection(self):
        """Return to the tool selection page."""
        self.main_frame.pack_forget()  # Remove the windrose interface
        self.tool_selection_frame.pack(fill="both", expand=True)  # Show tool selection page
        self.clear_graphs()  # Clear any previous selections or graphs

    def load_file(self):
        """Allow user to select a JSON file."""
        try:
            self.file_path = filedialog.askopenfilename(
                title="Select File",
                filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
            )
            if self.file_path:
                with open(self.file_path, 'r') as f:
                    json.load(f)  # Test if the selected file is a valid JSON file
                #self.generate_graph_btn.config(state=tk.NORMAL)
                #messagebox.showinfo("File Selected", f"File selected: {os.path.basename(self.file_path)}")
                self.run_windrose_generator()
            else:
                raise FileNotFoundError("No file was selected.")
        except FileNotFoundError as fnf_error:
            messagebox.showwarning("File Selection Error", str(fnf_error))
        except json.JSONDecodeError:
            messagebox.showwarning("Invalid File", "The selected file is not a valid JSON file.")
        except Exception as e:
            messagebox.showwarning("Error", f"An unexpected error occurred: {str(e)}")

    def generate_graphs(self):
        """Generate graphs based on the selected JSON file."""
        self.run_windrose_generator()

    def run_windrose_generator(self):
        """Generate windrose graphs."""
        if self.file_path is None:
            messagebox.showwarning("No File", "Please select a JSON file first.")
            return

        try:
            # Read the JSON data
            with open(self.file_path, 'r') as f:
                data = json.load(f)

            if 'windrose' not in data or not isinstance(data['windrose'], list):
                raise ValueError("The JSON file format is incorrect. 'windrose' data is missing or improperly structured.")

            self.figures.clear()
            self.current_fig_index = -1

            for entry in data['windrose']:
                date = entry['date']
                time = entry['time']
                measurements = entry['data']

                colors = ['red', 'green', 'blue', 'orange', 'purple']
                directions = ['E', 'ENE', 'NE', 'NNE', 'N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE']
                labels = ["~1.5km", "~3km", "~5-6km", "~9km", "~12km"]
                radii = []
                wind_dir = []

                for idx in range(5):
                    radii.append(measurements[idx]['speed_kph'])
                    dir_dict = {
                        'E': 0, 'ENE': 2 * np.pi / 16, 'NE': 2 * 2 * np.pi / 16,
                        'NNE': 3 * 2 * np.pi / 16, 'N': 4 * 2 * np.pi / 16,
                        'NNW': 5 * 2 * np.pi / 16, 'NW': 6 * 2 * np.pi / 16,
                        'WNW': 7 * 2 * np.pi / 16, 'W': 8 * 2 * np.pi / 16,
                        'WSW': 9 * 2 * np.pi / 16, 'SW': 10 * 2 * np.pi / 16,
                        'SSW': 11 * 2 * np.pi / 16, 'S': 12 * 2 * np.pi / 16,
                        'SSE': 13 * 2 * np.pi / 16, 'SE': 14 * 2 * np.pi / 16,
                        'ESE': 15 * 2 * np.pi / 16
                    }
                    wind_dir.append(dir_dict[measurements[idx]['direction']])

                fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'polar': True})
                bars = ax.bar(wind_dir, radii, width=2 * np.pi / 16, color=colors[:len(radii)], alpha=0.5)
                ax.set_xticks(np.linspace(0.0, 2 * np.pi, len(directions), endpoint=False))
                ax.set_xticklabels(directions)
                ax.set_title(f"Windrose ({time}, {date})", va='bottom')
                ax.legend(bars, labels[:len(radii)], loc='upper right', bbox_to_anchor=(1.2, 1.1))

                self.figures.append(fig)

            if self.figures:
                self.current_fig_index = 0
                self.show_graph()

                if len(self.figures) > 1:
                    self.prev_btn.config(state=tk.NORMAL)
                    self.next_btn.config(state=tk.NORMAL)
                self.clear_btn.config(state=tk.NORMAL)

        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            messagebox.showwarning("Error", str(e))

    def show_graph(self):
        """Display the graph corresponding to the current_fig_index."""
        if 0 <= self.current_fig_index < len(self.figures):
            fig = self.figures[self.current_fig_index]
            if self.canvas:
                self.canvas.get_tk_widget().pack_forget()

            self.canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=(50,50))

    def show_next_graph(self):
        """Show the next graph in the list."""
        if self.current_fig_index < len(self.figures) - 1:
            self.current_fig_index += 1
            self.show_graph()

    def show_prev_graph(self):
        """Show the previous graph in the list."""
        if self.current_fig_index > 0:
            self.current_fig_index -= 1
            self.show_graph()

    def clear_graphs(self):
        """Clear the graphs from the window and reset the application."""
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            self.canvas = None
        self.figures.clear()
        self.current_fig_index = -1
        #self.generate_graph_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)

    def run_other_tool(self):
        """Placeholder for another tool's functionality."""
        messagebox.showinfo("Other Tool", "This tool is currently under development.")

    def on_closing(self):
        """Handle the window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
            self.root.destroy()

# Main application entry
if __name__ == "__main__":
    root = tk.Tk()
    app = WindroseApp(root)
    root.mainloop()
