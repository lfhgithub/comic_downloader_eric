import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import argparse
import time

# This is a comment

def get_available_comics():
    # Note: gocomics.com uses JS rendering, so we use a hardcoded list of popular comics
    comics = ['garfield', 'peanuts', 'dilbert', 'calvinandhobbes', 'pluggers', 'foxtrot', 'bignate', 'pearlsbeforeswine', 'nonsequitur', 'wizardofid', 'beetlebailey', 'blondie', 'familycircus', 'hagar', 'ziggy', 'shoe']
    return sorted(comics)

def get_comic_url(comic_name, date):
    return f"https://www.gocomics.com/{comic_name}/{date.year}/{date.month:02d}/{date.day:02d}"

def download_image(comic_name, date, output_dir):
    url = get_comic_url(comic_name, date)
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
    filename = f"{comic_name}_{date.strftime('%Y-%m-%d')}.png"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(img_response.content)
    print(f"Downloaded {filename}")
    time.sleep(1)  # delay to avoid rate limiting

def main():
    comics = get_available_comics()
    if not comics:
        print("No comics available.")
        return
    print("Available comics:", ', '.join(comics))
    parser = argparse.ArgumentParser(description='Download comics from gocomics.com')
    parser.add_argument('--comic', type=str, required=True, help='Comic name (e.g., garfield)')
    parser.add_argument('--start-date', type=str, default='2025-11-27', help='Start date YYYY-MM-DD')
    parser.add_argument('--end-date', type=str, default='2025-11-27', help='End date YYYY-MM-DD')
    args = parser.parse_args()
    if args.comic not in comics:
        print(f"Comic '{args.comic}' not available. Available: {', '.join(comics)}")
        return
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    comics_dir = 'comics'
    os.makedirs(comics_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = os.path.join(comics_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving PNGs to: {os.path.abspath(output_dir)}")
    current_date = start_date
    while current_date <= end_date:
        download_image(args.comic, current_date, output_dir)
        current_date += timedelta(days=1)

if __name__ == '__main__':
    main()