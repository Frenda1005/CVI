import tkinter as tk
from tkinter import filedialog, messagebox
import os
import itertools
import csv
import subprocess

def run_half_life_analysis(construct_file, output_file, callback=None):
    try:
        subprocess.run(["python", "vaccine_analysis/analyze_half_life.py", construct_file, output_file], check=True)
        print("Half-life analysis completed successfully.")
        if callback:
            callback()
    except subprocess.CalledProcessError as e:
        print(f"Error during half-life analysis: {e}")

def run_immunogenicity_analysis(input_file, download_dir, callback=None):
    try:
        subprocess.run(["python", "vaccine_analysis/analyze_immunogenicity.py", input_file, download_dir], check=True)
        print("Immunogenicity analysis completed successfully.")
        if callback:
            callback()
    except subprocess.CalledProcessError as e:
        print(f"Error during immunogenicity analysis: {e}")

def summarize_immunogenicity_scores(input_dir, output_file, callback=None):
    try:
        subprocess.run(["python", "vaccine_analysis/summarize_immunogenicity_scores.py", input_dir, output_file], check=True)
        print(f"Summarized immunogenicity scores saved to {output_file}")
        if callback:
            callback()
    except subprocess.CalledProcessError as e:
        print(f"Error during immunogenicity summarization: {e}")

def run_helix_analysis(construct_file, download_dir, email, callback=None):
    try:
        subprocess.run(["python", "vaccine_analysis/analyze_helix.py", construct_file, download_dir, email], check=True)
        print("Helix analysis completed successfully.")
        if callback:
            callback()
    except subprocess.CalledProcessError as e:
        print(f"Error during helix analysis: {e}")

def calculate_helix_percentage(construct_file, target_subsequence, output_dir, callback=None):
    try:
        subprocess.run(["python", "vaccine_analysis/calculate_helix_percentage.py", construct_file, target_subsequence, output_dir], check=True)
        print(f"Helix percentage calculation for {target_subsequence} completed successfully.")
        if callback:
            callback()
    except subprocess.CalledProcessError as e:
        print(f"Error during helix percentage calculation for {target_subsequence}: {e}")

class VaccineAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vaccine Structure Analysis")
        
        self.sequences_label = tk.Label(root, text="Enter sequences (comma-separated):")
        self.sequences_label.pack()
        self.sequences_entry = tk.Entry(root, width=100)
        self.sequences_entry.pack()

        self.linker_label = tk.Label(root, text="Enter linker sequence:")
        self.linker_label.pack()
        self.linker_entry = tk.Entry(root, width=50)
        self.linker_entry.pack()

        self.output_label = tk.Label(root, text="Select output directory:")
        self.output_label.pack()
        self.output_button = tk.Button(root, text="Browse", command=self.browse_output_directory)
        self.output_button.pack()
        self.output_dir = tk.StringVar()
        self.output_entry = tk.Entry(root, textvariable=self.output_dir, width=50)
        self.output_entry.pack()

        self.run_button = tk.Button(root, text="Run Analysis", command=self.run_analysis)
        self.run_button.pack()

        self.run_helix_button = tk.Button(root, text="Run Helix Analysis Only", command=self.run_helix_only)
        self.run_helix_button.pack()

    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        self.output_dir.set(directory)

    def generate_constructs(self, sequences, linker, output_file):
        perms = itertools.permutations(sequences)
        constructs = [linker.join(perm) for perm in perms]
        
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for construct in constructs:
                writer.writerow([construct])
        print(f"Constructs written to {output_file}")

    def run_analysis(self):
        sequences = self.sequences_entry.get().split(',')
        linker = self.linker_entry.get()
        output_dir = self.output_dir.get()

        if not sequences or not linker or not output_dir:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        experiment_dir = os.path.join(output_dir, 'experiment', 'experiment1')
        immunogenicity_dir = os.path.join(experiment_dir, 'immunogenicity_results')
        os.makedirs(experiment_dir, exist_ok=True)
        os.makedirs(immunogenicity_dir, exist_ok=True)

        construct_file = os.path.join(experiment_dir, 'constructs.csv')
        output_file = os.path.join(experiment_dir, 'halflife.csv')
        summary_file = os.path.join(experiment_dir, 'total_immunogenicity_score.csv')

        self.generate_constructs(sequences, linker, construct_file)

        email = "your_email@example.com"  # Update with your email

        run_half_life_analysis(
            construct_file,
            output_file,
            callback=lambda: run_immunogenicity_analysis(
                output_file,
                immunogenicity_dir,
                callback=lambda: summarize_immunogenicity_scores(
                    immunogenicity_dir,
                    summary_file,
                    callback=lambda: run_helix_analysis(
                        construct_file,
                        experiment_dir,
                        email,
                        callback=lambda: [calculate_helix_percentage(construct_file, seq, experiment_dir) for seq in sequences]
                    )
                )
            )
        )

    def run_helix_only(self):
        sequences = self.sequences_entry.get().split(',')
        linker = self.linker_entry.get()
        output_dir = self.output_dir.get()

        if not sequences or not linker or not output_dir:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        experiment_dir = os.path.join(output_dir, 'experiment', 'experiment1')
        os.makedirs(experiment_dir, exist_ok=True)

        construct_file = os.path.join(experiment_dir, 'constructs.csv')
        email = "your_email@example.com"  # Update with your email

        run_helix_analysis(
            construct_file,
            experiment_dir,
            email,
            callback=lambda: [calculate_helix_percentage(construct_file, seq, experiment_dir) for seq in sequences]
        )
