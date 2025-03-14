# Google Play Store Review Scraper

A Python tool that allows you to fetch and analyze reviews from Google Play Store with customizable filtering options.

## Features

- Fetch reviews for any app on Google Play Store by app ID
- Filter reviews by rating (1-5 stars)
- Filter by review type (positive, critical, or all)
- Sort reviews by recency or relevance
- Specify the number of reviews to fetch
- Export results to Excel with properly formatted columns
- Interactive command-line interface

## Prerequisites

Make sure you have Python 3.6+ installed. Then install the required packages:

```bash
pip install google-play-scraper pandas openpyxl
```

## Usage

### Running the Script

Simply run the script and follow the interactive prompts:

```bash
python play_store_scraper.py
```

The script will guide you through:
1. Entering the app ID
2. Selecting a review filter (all, positive, critical, or custom ratings)
3. Choosing sort order (newest or most relevant)
4. Specifying how many reviews to fetch
5. Naming your output file

### Finding an App ID

The app ID is the identifier in the Play Store URL. For example:
- In `https://play.google.com/store/apps/details?id=com.spotify.music`
- The app ID is `com.spotify.music`

### Using as a Module

You can also import the functions in your own code:

```python
from play_store_scraper import fetch_reviews, reviews_to_excel

# Fetch 100 positive reviews for Spotify
reviews = fetch_reviews(
    app_id="com.spotify.music",
    review_type="positive",
    count=100,
    sort_option="newest"
)

# Export to Excel
df = reviews_to_excel(reviews, "spotify_reviews.xlsx")
```

## Available Options

### Review Types
- `all`: All reviews regardless of rating
- `positive`: Reviews with 4-5 stars
- `critical`: Reviews with 1-3 stars
- `custom`: Specify exact star ratings (e.g., only 1-star and 5-star)

### Sort Options
- `newest`: Most recent reviews first
- `relevant`: Most relevant reviews first (as determined by Google)

## Sample Output

The Excel file contains the following columns (when available):
- Review ID
- User Name
- Review Content
- Rating
- Thumbs Up
- App Version
- Review Date
- Developer Reply
- Reply Date

## Notes

- The script includes a small delay between requests to avoid rate limiting
- Default settings retrieve reviews in English from the US store
- Google Play Store may rate-limit excessive requests

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Feel free to fork this repository and submit pull requests. You can also open issues for bug reports or feature requests.