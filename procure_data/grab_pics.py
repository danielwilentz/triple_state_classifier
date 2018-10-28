import praw
import urllib.request
import glob
import os
from PIL import Image
from client_info import reddit_info

def scrape_earthporn(output_path, search_term):
    """
    Function to scrape the r/earthporn subreddit, download images from it, and save them to a local directory
    :param: output_path: type: str | output path to directory to save images to
    :param: search_term: type: str | string for search term, such as "Hawaii", "Arizona", or "Washington"
    """

    # API information
    reddit = praw.Reddit(client_id = reddit_info['client_id'],
                         client_secret = reddit_info['client_secret'],
                         user_agent = reddit_info['user_agent'],
                         username = reddit_info['username'],
                         password = reddit_info['password'])

    # Remove all contents of output directory
    files = glob.glob(output_path + '/*')
    for f in files:
        os.remove(f)

    # Create an empty directory ./pics
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Prepare search term variants
    if search_term[0].isupper():
        search_terms = search_term + '+' + search_term[0].lower() + search_term[1:]
    else:
        search_terms = search_term + '+' + search_term[0].upper() + search_term[1:]

    # Download Images
    earthporn = reddit.subreddit('earthporn')
    for submission in earthporn.search(search_terms, sort='relevance', syntax='lucene', time_filter='all', limit=300):
        print(submission.title)
        try:
            urllib.request.urlretrieve(submission.url, output_path + '/' + submission.title[0:100] + '.jpg')
        except urllib.error.HTTPError:
            continue
        except FileNotFoundError:
            continue
        except urllib.error.URLError:
            continue


def filter_images(output_path, by_res=True, by_ar=True, min_width=2000, min_height=2000):
    """
    :param output_path: directory of images
    :param by_res: toggle to filter by resolution, set to true
    :param by_ar: toggle to filter by aspect ratio, set to true
    :param min_width: minimum width required
    :param min_height: minimum height required
    :return:
    """
    for img in os.listdir(output_path):
        print(img)
        try:
            im = Image.open(output_path + '/' + img)
            width, height = im.size
            print('width: ', width, 'height: ', height)
            if by_res:
                if width < min_width or height < min_height:
                    print('deleting image because it does not meet resolution requirements')
                    os.remove(output_path + '/' + img)
                    continue
            if by_ar:
                if width//height < 1:
                    print('deleting image because it does not meet aspect ratio requirements')
                    os.remove(output_path + '/' + img)
        except OSError:
            os.remove(output_path + '/' + img)


if __name__ == '__main__':
    scrape_earthporn('/Users/danielwilentz/Desktop/get_profesh/web_development/pulled_pics/hawaii')
    filter_images('/Users/danielwilentz/Desktop/web_development/pulled_pics/pics')


