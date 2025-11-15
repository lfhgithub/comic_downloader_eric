import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import argparse
import time

def get_comic_url(date):
    return f"https://www.gocomics.com/garfield/{date.year}/{date.month:02d}/{date.day:02d}"

def download_image(date, output_dir):
    url = get_comic_url(date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"No comic for {date.strftime('%Y-%m-%d')}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tag = soup.find('img', class_='Comic_comic__image__6e_Fw')
    if not img_tag:
        print(f"Image not found for {date.strftime('%Y-%m-%d')}")
        return
    img_url = img_tag['src']
    img_response = requests.get(img_url, headers=headers)
    if img_response.status_code != 200:
        print(f"Failed to download image for {date.strftime('%Y-%m-%d')}")
        return
    filename = f"garfield_{date.strftime('%Y-%m-%d')}.png"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(img_response.content)
    print(f"Downloaded {filename}")
    time.sleep(1)  # delay to avoid rate limiting

def main():
    parser = argparse.ArgumentParser(description='Download Garfield comics')
    parser.add_argument('--start-date', type=str, default='2023-11-15', help='Start date YYYY-MM-DD')
    parser.add_argument('--end-date', type=str, default='2023-11-17', help='End date YYYY-MM-DD')
    parser.add_argument('--output-dir', type=str, default='garfield_comics', help='Output directory')
    args = parser.parse_args()
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    os.makedirs(args.output_dir, exist_ok=True)
    current_date = start_date
    while current_date <= end_date:
        download_image(current_date, args.output_dir)
        current_date += timedelta(days=1)

if __name__ == '__main__':
    main()