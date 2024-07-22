# CVI
Vaccine property app
# Vaccine Structure Analysis

This project provides a graphical user interface (GUI) for analyzing vaccine protein structures. The analysis includes generating constructs, calculating half-life, immunogenicity analysis, summarizing scores, and helix analysis.

## Project Structure


## Requirements

- Python 3.6+
- pip (Python package installer)

## Installation

1. **Clone the repository:**

    ```bash
    git clone <(https://github.com/Frenda1005/CVI.git)>  // or directly download from github
    cd CVI_UI
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the main application:**

    ```bash
    python main.py
    ```

2. **Usage:**

    - **Enter sequences**: Provide the sequences separated by commas.
    - **Enter linker sequence**: Provide the linker sequence.
    - **Select output directory**: Browse and select the output directory.
    - **Run Analysis**: Click the button to run the full analysis pipeline.

## Scripts Description

- `analyze_half_life.py`: Script for calculating the half-life of protein constructs.
- `analyze_helix.py`: Script for performing helix analysis on protein constructs.
- `analyze_immunogenicity.py`: Script for analyzing the immunogenicity of protein constructs.
- `calculate_helix_percentage.py`: Script for calculating the percentage of helices in protein constructs.
- `protparam_analyzer.py`: Script for analyzing protein parameters.
- `sequence_generator.py`: Script for generating protein sequence constructs.
- `summarize_immunogenicity_scores.py`: Script for summarizing immunogenicity scores.
- `ui.py`: Contains the main GUI code.
- `main.py`: Entry point for running the GUI application.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

