# Google Play Store Review Scraper
# This script fetches reviews from Google Play Store based on specified ratings
# and exports them to an Excel file

# Install required packages if not already installed
# !pip install google-play-scraper pandas openpyxl

import pandas as pd
from google_play_scraper import Sort, reviews, reviews_all
import time
from datetime import datetime

def fetch_reviews(app_id, rating_filter=None, count=500, sort_option="newest", review_type=None):
    """
    Fetch reviews for a specific app with various filter options
    
    Parameters:
    app_id (str): The app ID from Google Play Store
    rating_filter (int or list): Rating(s) to filter by (1-5)
    count (int): Number of reviews to fetch
    sort_option (str): How to sort reviews ('newest' or 'relevant')
    review_type (str): Type of reviews to fetch ('all', 'positive', 'critical')
    
    Returns:
    list: List of review dictionaries
    """
    all_reviews = []
    
    # Set sort option
    sort_method = Sort.NEWEST if sort_option.lower() == 'newest' else Sort.MOST_RELEVANT
    
    # Convert single rating to list if provided
    if rating_filter is not None and not isinstance(rating_filter, list):
        rating_filter = [rating_filter]
    
    # Handle review type filters
    if review_type and review_type.lower() == 'positive':
        # Positive reviews are considered 4-5 stars
        rating_filter = [4, 5]
        print(f"Fetching positive reviews (4-5 stars) sorted by {sort_option}...")
    elif review_type and review_type.lower() == 'critical':
        # Critical reviews are considered 1-3 stars
        rating_filter = [1, 2, 3]
        print(f"Fetching critical reviews (1-3 stars) sorted by {sort_option}...")
    
    # If no rating filter is specified, fetch all ratings
    if rating_filter is None:
        print(f"Fetching {count} reviews (all ratings) sorted by {sort_option}...")
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en',
                country='us',
                sort=sort_method,
                count=count
            )
            all_reviews.extend(result)
            print(f"Fetched {len(result)} reviews")
        except Exception as e:
            print(f"Error fetching reviews: {str(e)}")
    else:
        # Fetch reviews for each rating in the filter
        for rating in rating_filter:
            print(f"Fetching reviews with {rating} star rating sorted by {sort_option}...")
            try:
                result, continuation_token = reviews(
                    app_id,
                    lang='en',
                    country='us',
                    sort=sort_method,
                    count=count,
                    filter_score_with=rating
                )
                all_reviews.extend(result)
                print(f"Fetched {len(result)} reviews with {rating} stars")
                
                # Add a small delay to avoid being rate-limited
                time.sleep(2)
            except Exception as e:
                print(f"Error fetching {rating} star reviews: {str(e)}")
    
    print(f"Total reviews fetched: {len(all_reviews)}")
    return all_reviews

def reviews_to_excel(reviews_data, output_filename=None):
    """
    Convert reviews data to a DataFrame and save as Excel
    
    Parameters:
    reviews_data (list): List of review dictionaries
    output_filename (str): Name of the Excel file to save
    
    Returns:
    pandas.DataFrame: DataFrame containing the reviews
    """
    # Convert reviews to DataFrame
    df = pd.DataFrame(reviews_data)
    
    # Select and rename relevant columns
    if not df.empty:
        # Check which columns exist in the dataframe
        columns_to_keep = []
        column_mapping = {
            'reviewId': 'Review ID',
            'userName': 'User Name',
            'content': 'Review Content',
            'score': 'Rating',
            'thumbsUpCount': 'Thumbs Up',
            'reviewCreatedVersion': 'App Version',
            'at': 'Review Date',
            'replyContent': 'Developer Reply',
            'repliedAt': 'Reply Date'
        }
        
        for col in column_mapping:
            if col in df.columns:
                columns_to_keep.append(col)
        
        # Keep only relevant columns that exist
        df = df[columns_to_keep]
        
        # Rename columns
        column_rename = {col: column_mapping[col] for col in columns_to_keep}
        df = df.rename(columns=column_rename)
        
        # Format dates if they exist
        if 'Review Date' in df.columns:
            df['Review Date'] = pd.to_datetime(df['Review Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        if 'Reply Date' in df.columns and not df['Reply Date'].isna().all():
            df['Reply Date'] = pd.to_datetime(df['Reply Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Generate default filename if not provided
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"playstore_reviews_{timestamp}.xlsx"
    
    # Ensure filename has .xlsx extension
    if not output_filename.endswith('.xlsx'):
        output_filename += '.xlsx'
    
    # Save to Excel
    df.to_excel(output_filename, index=False, engine='openpyxl')
    print(f"Reviews saved to {output_filename}")
    
    return df

# Interactive function to run in Jupyter
def scrape_play_store_reviews():
    print("Google Play Store Review Scraper")
    print("--------------------------------")
    
    # Get app ID
    app_id = input("Enter the app ID (e.g., com.example.app): ").strip()
    
    # Get review type filter first
    print("\nSelect review type filter:")
    print("1. All reviews")
    print("2. Positive reviews (4-5 stars)")
    print("3. Critical reviews (1-3 stars)")
    print("4. Custom star ratings")
    review_type_choice = input("Enter your choice (1-4): ").strip()
    
    ratings = None
    review_type = None
    
    if review_type_choice == '2':
        review_type = 'positive'
    elif review_type_choice == '3':
        review_type = 'critical'
    elif review_type_choice == '4':
        # Get custom rating filter
        rating_input = input("Enter ratings to filter by (1-5, comma-separated): ").strip()
        try:
            ratings = [int(r.strip()) for r in rating_input.split(',')]
            # Validate ratings
            ratings = [r for r in ratings if 1 <= r <= 5]
            if not ratings:
                print("Invalid ratings. Using all ratings.")
                ratings = None
        except:
            print("Invalid input. Using all ratings.")
            ratings = None
    
    # Get sort option
    print("\nSelect sort order:")
    print("1. Most recent reviews")
    print("2. Most relevant reviews")
    sort_choice = input("Enter your choice (1-2): ").strip()
    
    sort_option = "newest" if sort_choice != '2' else "relevant"
    
    # Get count
    count_input = input("\nEnter number of reviews to fetch per rating (default: 500): ").strip()
    try:
        count = int(count_input) if count_input else 500
    except:
        print("Invalid input. Using default: 500")
        count = 500
    
    # Get output filename
    output_filename = input("Enter output filename (or leave blank for default): ").strip()
    output_filename = output_filename if output_filename else None
    
    # Fetch reviews
    print("\nFetching reviews...")
    reviews_data = fetch_reviews(app_id, ratings, count, sort_option, review_type)
    
    # Save to Excel
    if reviews_data:
        df = reviews_to_excel(reviews_data, output_filename)
        return df
    else:
        print("No reviews fetched.")
        return None

# Run the scraper when executed directly
if __name__ == "__main__":
    scrape_play_store_reviews()