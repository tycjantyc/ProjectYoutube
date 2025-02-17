import requests
import json
from pytube import YouTube
import isodate
from googleapiclient.discovery import build
import yt_dlp


def search_youtube_videos(query, API_KEY, YOUTUBE_SEARCH_URL, max_results=5):
    """
    Search for YouTube videos based on a query.
    :param query: Keywords or tags for searching videos.
    :param max_results: Number of video results to return.
    :return: List of video URLs matching the search criteria.
    """

    results_per_request = 50  # Max results per API request
    video_urls = []
    next_page_token = None

    while len(video_urls) < max_results:
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'videoDuration':'short',
            'maxResults': min(results_per_request, max_results - len(video_urls)),
            'key': API_KEY
        }

        if next_page_token:
            params['pageToken'] = next_page_token

        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        if response.status_code != 200:
            print(f"Error: API request failed with status code {response.status_code}")
            return []
        
        search_results = response.json()
        items = search_results.get('items', [])
        video_urls.extend(
            f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            for item in items
        )

        # Check for the next page token
        next_page_token = search_results.get('nextPageToken')
        if not next_page_token:
            break

    return video_urls


def download_youtube_video(video_url, output_path='videos/'):
    """
    Download a YouTube video by URL.
    :param video_url: URL of the YouTube video.
    :param output_path: Directory path to save the downloaded video.
    """
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path)
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Error downloading video: {e}")

def download_video(url, download_path='videos/'):
    try:
        ydl_opts = {
            'format': 'best',  # Choose the best quality available
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',  # Specify output template
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            print(f"Downloaded: {title}")
    except Exception as e:
        print(f"Error downloading video: {e}")

def get_video_details(video_url, API_KEY):

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    # Extract the video ID from the URL
    video_id = video_url.split('v=')[1]

    # Make a request to the YouTube Data API
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()

    # Extract the relevant details from the response
    if response['items']:

        video_data = response['items'][0]
        title = video_data['snippet']['title']
        description = video_data['snippet']['description']
        views = video_data['statistics']['viewCount']
        duration_iso = video_data['contentDetails']['duration']
        duration = isodate.parse_duration(duration_iso)

        return {
            "title": title,
            "description": description,
            "views": views,
            "duration": duration
        }
    else:
        return "Video not found."