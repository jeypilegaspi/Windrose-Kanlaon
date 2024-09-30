import tkinter as tk
from tkinter import filedialog, messagebox
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

        # Buttons
        self.select_file_btn = tk.Button(root, text="Select JSON File", command=self.load_file)
        self.select_file_btn.pack(pady=20)

        self.generate_graph_btn = tk.Button(root, text="Generate Graphs", command=self.generate_graphs, state=tk.DISABLED)
        self.generate_graph_btn.pack(pady=10)

        self.clear_btn = tk.Button(root, text="Clear", command=self.clear_graphs, state=tk.DISABLED)
        self.clear_btn.pack(pady=10)

        # Navigation buttons
        self.prev_btn = tk.Button(root, text="< Previous", command=self.show_prev_graph, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, padx=10)

        self.next_btn = tk.Button(root, text="Next >", command=self.show_next_graph, state=tk.DISABLED)
        self.next_btn.pack(side=tk.RIGHT, padx=10)

        # Placeholder for the selected file path and graph list
        self.file_path = None
        self.figures = []
        self.current_fig_index = -1  # Track current figure being displayed

        # Placeholder for the figure canvas
        self.canvas = None

    def load_file(self):
        """Allow user to select a JSON file."""
        try:
            self.file_path = filedialog.askopenfilename(
                title="Select JSON File",
                filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
            )

            if self.file_path:
                # Test if the selected file is a valid JSON file
                with open(self.file_path, 'r') as f:
                    json.load(f)

                # Enable the Generate Graph button once a valid file is selected
                self.generate_graph_btn.config(state=tk.NORMAL)
                messagebox.showinfo("File Selected", f"File selected: {os.path.basename(self.file_path)}")
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
        if self.file_path is None:
            messagebox.showwarning("No File", "Please select a JSON file first.")
            return

        try:
            # Read the JSON data
            with open(self.file_path, 'r') as f:
                data = json.load(f)

            # Validate JSON structure
            if 'windrose' not in data or not isinstance(data['windrose'], list):
                raise ValueError("The JSON file format is incorrect. 'windrose' data is missing or improperly structured.")

            # Clear any previous figures
            self.figures.clear()
            self.current_fig_index = -1

            # Generate the windrose plot for each entry in the JSON file
            for entry in data['windrose']:
                if 'date' not in entry or 'time' not in entry or 'data' not in entry:
                    raise ValueError("Missing required fields (date, time, data) in the JSON entry.")

                date = entry['date']
                time = entry['time']
                measurements = entry['data']

                colors = ['red', 'green', 'blue', 'orange', 'purple']
                directions = ['E', 'ENE', 'NE', 'NNE', 'N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE']
                labels = ["~1.5km", "~3km", "~5-6km", "~9km", "~12km"]

                radii = []
                wind_dir = []

                for idx in range(5):
                    if 'speed_kph' not in measurements[idx] or 'direction' not in measurements[idx]:
                        raise ValueError("Invalid data structure in the 'data' field of the JSON.")

                    radii.append(measurements[idx]['speed_kph'])
                    dir_dict = {
                        'E': 0, 'ENE': 2 * np.pi / 16, 'NE': 2 * 2 * np.pi / 16, 'NNE': 3 * 2 * np.pi / 16,
                        'N': 4 * 2 * np.pi / 16, 'NNW': 5 * 2 * np.pi / 16, 'NW': 6 * 2 * np.pi / 16, 
                        'WNW': 7 * 2 * np.pi / 16, 'W': 8 * 2 * np.pi / 16, 'WSW': 9 * 2 * np.pi / 16,
                        'SW': 10 * 2 * np.pi / 16, 'SSW': 11 * 2 * np.pi / 16, 'S': 12 * 2 * np.pi / 16,
                        'SSE': 13 * 2 * np.pi / 16, 'SE': 14 * 2 * np.pi / 16, 'ESE': 15 * 2 * np.pi / 16
                    }
                    wind_dir.append(dir_dict[measurements[idx]['direction']])

                # Create the windrose plot
                fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'polar': True})
                bars = ax.bar(wind_dir, radii, width=2 * np.pi / 16, color=colors[:len(radii)], alpha=0.35)

                ax.set_xticks(np.linspace(0.0, 2 * np.pi, len(directions), endpoint=False))
                ax.set_xticklabels(directions)
                ax.set_title(f"Windrose ({time}, {date})", va='bottom')

                # Add the legend
                ax.legend(bars, labels[:len(radii)], loc='upper right', bbox_to_anchor=(1.2, 1.1))
                # Store the figure
                self.figures.append(fig)

            # Display the first graph if any are generated
            if self.figures:
                self.current_fig_index = 0
                self.show_graph()

            # Enable the navigation and clear buttons
            if len(self.figures) > 1:
                self.prev_btn.config(state=tk.NORMAL)
                self.next_btn.config(state=tk.NORMAL)
            self.clear_btn.config(state=tk.NORMAL)

        except FileNotFoundError as fnf_error:
            messagebox.showwarning("File Error", str(fnf_error))
        except json.JSONDecodeError:
            messagebox.showwarning("Invalid JSON", "There was an error parsing the JSON file. Please check the format.")
        except ValueError as ve:
            messagebox.showwarning("Data Format Error", str(ve))
        except Exception as e:
            messagebox.showwarning("Error", f"An unexpected error occurred: {str(e)}")

    def show_graph(self):
        """Display the graph corresponding to the current_fig_index."""
        if 0 <= self.current_fig_index < len(self.figures):
            fig = self.figures[self.current_fig_index]

            # Clear any existing canvas before drawing new one
            if self.canvas:
                self.canvas.get_tk_widget().pack_forget()

            # Display the current figure
            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

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
            self.canvas.get_tk_widget().pack_forget()  # Remove the canvas from the GUI
            self.canvas = None  # Reset the canvas

        # Close all matplotlib figures
        for fig in self.figures:
            plt.close(fig)
        self.figures.clear()
        self.current_fig_index = -1

        # Disable the generate and clear buttons until a new file is selected
        self.generate_graph_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)

        # Reset the file path
        self.file_path = None

        messagebox.showinfo("Cleared", "Graphs and selections have been cleared.")

    def on_closing(self):
        """Handle window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Close all matplotlib figures if they exist
            for fig in self.figures:
                plt.close(fig)

            self.root.destroy()

# Main tkinter loop
if __name__ == "__main__":
    root = tk.Tk()
    app = WindroseApp(root)
    root.mainloop()
