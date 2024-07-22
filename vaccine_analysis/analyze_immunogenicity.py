# import sys
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_autoinstaller

# def find_element(driver, by, value, timeout=20):
#     try:
#         return WebDriverWait(driver, timeout).until(
#             EC.presence_of_element_located((by, value))
#         )
#     except Exception as e:
#         print(f"Error finding element by {by} with value {value}: {e}")
#         return None

# def analyze_immunogenicity(file_path, download_dir):
#     sequences_df = pd.read_csv(file_path)
#     # sequences_df = pd.read_csv(file_path, header=None)
#     print(f"Loaded {len(sequences_df)} sequences from {file_path}")

#     chromedriver_autoinstaller.install()
#     options = webdriver.ChromeOptions()
#     prefs = {
#         "download.default_directory": download_dir,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True
#     }
#     options.add_experimental_option("prefs", prefs)
#     driver = webdriver.Chrome(options=options)

#     driver.get('http://tools.iedb.org/CD4episcore/')

#     for index, row in sequences_df.iterrows():
#         sequence = row[0]
#         print(f"Processing sequence {index + 1}/{len(sequences_df)}: {sequence}")

#         try:
#             textarea = find_element(driver, By.NAME, 'sequence_text')
#             if textarea:
#                 textarea.clear()
#                 textarea.send_keys(sequence)
#             else:
#                 raise Exception("Textarea not found")
            
#             time.sleep(2)  

#             submit_button = find_element(driver, By.XPATH, '//input[@value="Submit"]')
#             if submit_button:
#                 submit_button.click()
#             else:
#                 raise Exception("Submit button not found")

#             time.sleep(20)  # Adjust this time as necessary

#             download_link = find_element(driver, By.LINK_TEXT, 'Download result')
#             if download_link:
#                 file_name = f"cd4episcore_results_{index + 1}.csv"
#                 driver.execute_script("arguments[0].setAttribute('download', arguments[1])", download_link, file_name)
#                 download_link.click()
#             else:
#                 raise Exception("Download link not found")

#             time.sleep(5)  # Adjust this time as necessary

#             driver.get('http://tools.iedb.org/CD4episcore/')
#             time.sleep(2)  # Adjust this time as necessary

#         except Exception as e:
#             print(f"Error with sequence {index}: {e}")

#     driver.quit()
#     print("Immunogenicity analysis completed.")

# if __name__ == "__main__":
#     input_file_path = sys.argv[1]  # Get the input file path from the command line
#     download_dir = sys.argv[2]  # Get the download directory from the command line
#     analyze_immunogenicity(input_file_path, download_dir)
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

def find_element(driver, by, value, timeout=20):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception as e:
        print(f"Error finding element by {by} with value {value}: {e}")
        return None

def analyze_immunogenicity(file_path, download_dir, threshold):
    sequences_df = pd.read_csv(file_path)
    print(f"Loaded {len(sequences_df)} sequences from {file_path}")

    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    driver.get('http://tools.iedb.org/CD4episcore/')

    for index, row in sequences_df.iterrows():
        sequence = row[0]
        print(f"Processing sequence {index + 1}/{len(sequences_df)}: {sequence}")

        try:
            textarea = find_element(driver, By.NAME, 'sequence_text')
            if textarea:
                textarea.clear()
                textarea.send_keys(sequence)
            else:
                raise Exception("Textarea not found")

            # Set the threshold
            threshold_dropdown = find_element(driver, By.ID, 'id_threshold')
            if threshold_dropdown:
                select = Select(threshold_dropdown)
                select.select_by_visible_text(str(threshold))
            else:
                raise Exception("Threshold dropdown not found")

            time.sleep(2)

            submit_button = find_element(driver, By.XPATH, '//input[@value="Submit"]')
            if submit_button:
                submit_button.click()
            else:
                raise Exception("Submit button not found")

            time.sleep(20)  # Adjust this time as necessary

            download_link = find_element(driver, By.LINK_TEXT, 'Download result')
            if download_link:
                file_name = f"cd4episcore_results_{index + 1}.csv"
                driver.execute_script("arguments[0].setAttribute('download', arguments[1])", download_link, file_name)
                download_link.click()
            else:
                raise Exception("Download link not found")

            time.sleep(5)  # Adjust this time as necessary

            driver.get('http://tools.iedb.org/CD4episcore/')
            time.sleep(2)  # Adjust this time as necessary

        except Exception as e:
            print(f"Error with sequence {index}: {e}")

    driver.quit()
    print("Immunogenicity analysis completed.")

if __name__ == "__main__":
    input_file_path = sys.argv[1]  # Get the input file path from the command line
    download_dir = sys.argv[2]  # Get the download directory from the command line
    threshold = int(sys.argv[3])  # Get the threshold from the command line
    analyze_immunogenicity(input_file_path, download_dir, threshold)
