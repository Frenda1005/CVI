import pandas as pd
import os
import sys

# def summarize_immunogenicity_scores(input_dir, output_file):
#     summary_data = []
#     count = 1

#     for filename in os.listdir(input_dir):
#         if filename.endswith(".csv"):
#             old_file_path = os.path.join(input_dir, filename)
#             new_file_name = f"sequence_{count}.csv"
#             new_file_path = os.path.join(input_dir, new_file_name)
#             os.rename(old_file_path, new_file_path)

#             try:
#                 df = pd.read_csv(new_file_path)
#                 if 'Immunogenicity Score' in df.columns:
#                     file_sum = df['Immunogenicity Score'].sum()
#                     summary_data.append({'File': new_file_name, 'Total Immunogenicity Score': file_sum})
#                 else:
#                     print(f"Column 'Immunogenicity Score' not found in {filename}")
#             except Exception as e:
#                 print(f"Error processing {filename}: {e}")

#             count += 1

def summarize_immunogenicity_scores(input_dir, output_file):
    summary_data = []
    count = 1

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            old_file_path = os.path.join(input_dir, filename)
            new_file_name = f"sequence_{count}.csv"
            new_file_path = os.path.join(input_dir, new_file_name)
            os.rename(old_file_path, new_file_path)

            try:
                df = pd.read_csv(new_file_path)
                if 'Immunogenicity Score' in df.columns:
                    # Calculate the number of rows
                    num_rows = len(df)
                    
                    # Calculate the average of the "Immunogenicity Score"
                    average_immunogenicity = df['Immunogenicity Score'].mean()
                    
                    # Calculate the average of the top 5 "Immunogenicity Scores"
                    top_5_average_immunogenicity = df['Immunogenicity Score'].nlargest(5).mean()
                    
                    # Calculate the sum of all "Immunogenicity Scores"
                    sum_immunogenicity = df['Immunogenicity Score'].sum()
                    
                    summary_data.append({
                        'File': new_file_name,
                        'Total Immunogenicity Score': sum_immunogenicity,
                        'Number of Rows': num_rows,
                        'Average Immunogenicity Score': average_immunogenicity,
                        'Top 5 Average Immunogenicity Score': top_5_average_immunogenicity
                    })
                else:
                    print(f"Column 'Immunogenicity Score' not found in {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

            count += 1

    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(output_file, index=False)
        print(f"Summary immunogenicity scores saved to {output_file}")
    else:
        print("No valid CSV files found with 'Immunogenicity Score' column.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python summarize_immunogenicity_scores.py <input_dir> <output_file>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    summarize_immunogenicity_scores(input_dir, output_file)
