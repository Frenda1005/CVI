import pandas as pd
import os
import sys

def calculate_h_percentage(sequence, target_subsequence, file_index, base_path):
    # Find the start index of the target subsequence in the sequence
    start_index = sequence.find(target_subsequence)
    if start_index == -1:
        print(f"Subsequence not found in sequence {file_index}")
        return None  # Return None if the subsequence is not found
    end_index = start_index + len(target_subsequence)
    
    # Construct file path
    file_path = os.path.join(base_path, f"Job_{file_index}.csv")  # Files are named as Job_1.csv, Job_2.csv, ...
    
    # Load the character mapping file
    try:
        character_data = pd.read_csv(file_path, header=None).iloc[1]  # Load the second row that contains the mapping data
        relevant_data = character_data[start_index:end_index]  # Extract only the relevant portion for the subsequence
        
        # Count 'H' in the mapping
        h_count = (relevant_data == 'H').sum()
        percentage = (h_count / len(relevant_data)) * 100
        return percentage
    except Exception as e:
        print(f"Error processing file Job_{file_index}.csv: {e}")
        return None

def main(construct_file, target_subsequence, output_dir):
    # Load the protein construct
    protein_sequences = pd.read_csv(construct_file, header=None)
    
    # Define the base path for your character mapping files
    base_path = os.path.join(output_dir, 'helix_results')
    
    # Apply the function to all sequences, with each sequence's index matching its corresponding file number
    results = []
    for index, row in protein_sequences.iterrows():
        seq_percentage = calculate_h_percentage(row.iloc[0], target_subsequence, index + 1, base_path)  # index + 1 if your files start from Job_1.csv
        results.append(seq_percentage)
    
    # Save the results to a CSV file
    result_df = pd.DataFrame(results, columns=['Percentage of H'])
    output_file = os.path.join(output_dir, f'Helix_{target_subsequence}.csv')
    result_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python calculate_helix_percentage.py <construct_file> <target_subsequence> <output_dir>")
        sys.exit(1)
    
    construct_file = sys.argv[1]
    target_subsequence = sys.argv[2]
    output_dir = sys.argv[3]
    
    main(construct_file, target_subsequence, output_dir)
