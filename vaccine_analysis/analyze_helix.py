import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from bs4 import BeautifulSoup

# Function to process each sequence
def process_sequence(driver, sequence, job_name, email):
    driver.get('http://bioinf.cs.ucl.ac.uk/psipred/')  # Refresh the page before each sequence
    try:
        # Find the textarea and input the sequence
        textarea = WebDriverWait(driver, 3600).until(
            EC.presence_of_element_located((By.NAME, 'input_data'))
        )
        textarea.clear()
        textarea.send_keys(sequence)

        # Find the job name input and enter a job name
        job_name_input = driver.find_element(By.NAME, 'job_name')
        job_name_input.clear()
        job_name_input.send_keys(job_name)

        # Find the email input and enter the email
        email_input = driver.find_element(By.NAME, 'email')
        email_input.clear()
        email_input.send_keys(email)

        # Submit the form
        submit_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="submit"]')
        submit_button.click()

        # Wait for the result page to load and display the results
        WebDriverWait(driver, 3600).until(
            EC.presence_of_element_located((By.ID, 'sequence_plot'))
        )

        # Wait for the overlay to disappear
        WebDriverWait(driver, 3600).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay'))
        )

        # Extract the secondary structure information
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        container = soup.find('g', {'id': 'container'})
        positions = []
        structures = []
        if container:
            rects = container.find_all('rect', {'class': 'rect'})
            for rect in rects:
                title = rect.find('title')
                if title:
                    parts = title.text.split()
                    positions.append(parts[1])  # Pos value
                    structures.append(parts[3])  # ss value
        
        print(f"Processed sequence with job name {job_name}")
        return positions, structures

    except Exception as e:
        print(f"Error processing sequence {job_name}: {str(e)}")
        return [], []

def analyze_helix(construct_file, download_dir, email):
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing.enabled": True}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    results_directory = os.path.join(download_dir, 'helix_results')
    os.makedirs(results_directory, exist_ok=True)

    with open(construct_file, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            sequence = row[0]
            job_name = f"Job_{i + 1}"
            positions, structures = process_sequence(driver, sequence, job_name, email)
            if positions and structures:
                result_file_path = os.path.join(results_directory, f"{job_name}.csv")
                with open(result_file_path, 'w', newline='') as result_file:
                    writer = csv.writer(result_file)
                    writer.writerow(positions)
                    writer.writerow(structures)

    driver.quit()

if __name__ == "__main__":
    import sys
    construct_file = sys.argv[1]
    download_dir = sys.argv[2]
    email = sys.argv[3]
    analyze_helix(construct_file, download_dir, email)
