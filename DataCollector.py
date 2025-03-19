from WebScraper import HTMLParser, ExtractText
import csv
import os
from datetime import datetime
import concurrent.futures

def ErrorStorer(idx):
    with open("error.txt", "a", encoding="utf-8") as f:
        f.write(f"Error at index: {idx}\n")

def ParseAndReturn(url, idx):
    try:
        soup = HTMLParser.get_soup(url)
    except Exception as e:
        raise Exception(f"Error fetching URL {url}: {e}")
    paragraphs = ExtractText.get_para(soup, bangla_only=True)
    if not paragraphs:
        raise Exception("No Bangla text found")
    headings = ExtractText.get_tags(soup, ["h1"], min_length=1, bangla_only=True)
    if headings:
        startingparser = "<#START-ASTHA#> " + headings[0]
    else:
        startingparser = "<#START-ASTHA#> Heading not found"
    endingparser = "<#END-ASTHA#>"
    paragraphs.insert(0, startingparser)
    paragraphs.append(endingparser)
    current_date = datetime.now().date().isoformat()
    rows = [[p, url, current_date] for p in paragraphs]
    return rows

def process_url(i, baseUrl):
    url = baseUrl + str(i)
    try:
        rows = ParseAndReturn(url, i)
        print(f"Processed index {i}")
        return (i, rows)
    except Exception as e:
        ErrorStorer(i)
        print(f"Error at index {i}: {e}")
        return (i, None)

def flush_to_csv(data_batch, filename):
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["text", "source_url", "date"])
        writer.writerows(data_batch)

def main():
    baseUrl = "https://www.bd-pratidin.com/national/2025/03/18/"
    csv_filename = "trainData.csv"
    batch_size = 500
    collected_data = []
    print("Please, see the last line of the CSV file and enter the starting index. Be careful with the index to avoid duplicates.")
    while True:
        try:
            start_index = int(input("\nPlease, enter the starting index (MUST): ")) + 1
            if 0 < start_index < 1100000:
                break
        except Exception:
            print("Invalid input. Please enter a valid number.")
    try:
        end_index = int(input("Please, enter the ending index (optional): "))
        if end_index > 1100000 or end_index < 0 or end_index < start_index:
            end_index = 1100000
    except Exception:
        end_index = 1100000
    indices = range(start_index, end_index)
    max_workers = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, rows in executor.map(lambda i: process_url(i, baseUrl), indices):
            if rows:
                collected_data.extend(rows)
            if len(collected_data) >= batch_size:
                flush_to_csv(collected_data, csv_filename)
                collected_data = []
    if collected_data:
        flush_to_csv(collected_data, csv_filename)
    print("Data collection complete.")

if __name__ == "__main__":
    main()
