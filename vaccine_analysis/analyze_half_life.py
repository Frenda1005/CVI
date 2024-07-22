import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import chromedriver_autoinstaller

def extract_half_life(text, pattern):
    match = re.search(pattern, text)
    if match:
        return match.group(1) + " " + match.group(2)
    return None

def analyze_half_life(file_path, output_file):
    sequences_df = pd.read_csv(file_path, header=None)
    print(f"Loaded {len(sequences_df)} sequences from {file_path}")

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    driver.get('https://web.expasy.org/protparam/')

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sequence', 'Half-life Mammalian (in vitro)', 'Half-life Yeast (in vivo)', 'Half-life E. coli (in vivo)', 'Instability Index'])

    for index, row in sequences_df.iterrows():
        sequence = row.iloc[0]
        print(f"Analyzing sequence {index + 1}/{len(sequences_df)}: {sequence}")

        try:
            textarea = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'sequence'))
            )
            textarea.clear()
            textarea.send_keys(sequence)

            compute_button = driver.find_element(By.XPATH, '//input[@value="Compute parameters"]')
            driver.execute_script("arguments[0].scrollIntoView(true);", compute_button)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Compute parameters"]')))

            attempts = 3
            for attempt in range(attempts):
                try:
                    compute_button.click()
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(2)

            time.sleep(5)
            half_life_mammalian = half_life_yeast = half_life_ecoli = instability_index_value = None

            try:
                content = driver.page_source
                half_life_start = content.find("The estimated half-life is:")
                instability_index_start = content.find("Instability index:")

                if half_life_start != -1:
                    half_life_end = content.find("<b>", half_life_start)
                    half_life_text = content[half_life_start:half_life_end]
                    half_life_mammalian = extract_half_life(half_life_text, r"(\d+\.*\d*) (hours) \(mammalian reticulocytes, in vitro\)")
                    half_life_yeast = extract_half_life(half_life_text, r"(\d+\.*\d*) (hours) \(yeast, in vivo\)")
                    if not half_life_yeast:
                        half_life_yeast = extract_half_life(half_life_text, r"(\d+) (min) \(yeast, in vivo\)")
                    half_life_ecoli = extract_half_life(half_life_text, r"(\d+\.*\d*) (hours) \(Escherichia coli, in vivo\)")

                if instability_index_start != -1:
                    instability_index_end = content.find("<b>", instability_index_start)
                    instability_index_text = content[half_life_start:half_life_end]

                    if "The instability index (II) is computed to be" in instability_index_text:
                        instability_index_value = instability_index_text.split("The instability index (II) is computed to be")[1].split()[0]

            except Exception as e:
                print(f"Error processing sequence {index}: {e}")

            with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([sequence, half_life_mammalian, half_life_yeast, half_life_ecoli, instability_index_value])
            print(f"Sequence {index + 1} analysis complete")

            driver.back()
            time.sleep(2)

        except Exception as e:
            print(f"Error with sequence {index}: {e}")

    driver.quit()
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    input_file_path = sys.argv[1]  # Get the input file path from the command line
    output_file_path = sys.argv[2]  # Get the output file path from the command line
    analyze_half_life(input_file_path, output_file_path)
