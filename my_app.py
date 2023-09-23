from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from apify_client import ApifyClient
from datetime import datetime
import matplotlib.pyplot as plt

from flask import Flask, request, render_template
from apify_client import ApifyClient
import pandas as pd
import mysql.connector
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from afinn import Afinn
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('wordnet')
import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel

from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

app = Flask(__name__, static_url_path='/static', static_folder='static')
afinn = Afinn()
instagram_client = ApifyClient("apify_api_ZPgkbd9Cnp424hni18t5uAzMHhz1ud2gBBhU")
facebook_client = ApifyClient("apify_api_TREn6wGABw3ijaggDChucNKYPdwEvA3R4YLQ")
twitter_client = ApifyClient("apify_api_ZPgkbd9Cnp424hni18t5uAzMHhz1ud2gBBhU")

@app.route('/')
def index():
    return render_template('firstpage.html')

@app.route('/get_started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        # Process the input from getstarted.html
        platform = request.form.get('platform')
        content_type = request.form.get('content_type')

        # Your processing logic here

        # After processing, you can redirect back to firstpage.html or any other page
        return redirect(url_for('index'))

    return render_template('getstarted.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    platform = request.form.get('platform')
    content_type = request.form.get('content_type')

    if platform == 'instagram':
        option = request.form['instagramOption']

        if (option == "comments"):
            URL = request.form['instagramCommentsURL']

            run_input = {
              "directUrls": [URL],
               "resultsLimit": 100,
            }
            run = instagram_client.actor("apify/instagram-comment-scraper").call(run_input=run_input)

            results_list = []
            comment_container = []

            for item in instagram_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            comment_string = ''.join(comment_container)

            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"

            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)
    

        
        
        elif (option == 'posts'):
            username = request.form['instagramPostsURL']

            run_input = {
            "username": [username],
            "resultsLimit": 30,
            }

            run = instagram_client.actor("apify/instagram-post-scraper").call(run_input=run_input)

            results_list = []
            comment_container = []

            for item in instagram_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            comment_string = ''.join(comment_container)
        
            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"




            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)



        
        elif (option == "profile"):
            instagram_url = request.form['instagramUsername']
            run_input = {
                "username": [instagram_url],
                "resultsLimit": 30,
            }

            run = instagram_client.actor("apify/instagram-post-scraper").call(run_input=run_input)
            result_list_profile = []
            for item in instagram_client.dataset(run["defaultDatasetId"]).iterate_items():
                result_list_profile.append(item)
            data = pd.DataFrame(result_list_profile)

            run_input = {"usernames": [instagram_url]}
            run = instagram_client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
            result_list3 = []
            for item in instagram_client.dataset(run["defaultDatasetId"]).iterate_items():
                result_list3.append(item)
            data1 = pd.DataFrame(result_list3)
            columns_to_pass = ['profilePicUrlHD', 'url', 'biography', 'followersCount', 'followsCount', 'verified', 'username','postsCount']
            profile_data = data1[columns_to_pass].iloc[0].to_dict()


            average_likes = int(data['likesCount'].mean())
            average_comments = int(data['commentsCount'].mean())
            data['likesCount'] = data['likesCount'].astype(int)  # Convert likesCount to integer
            last_10_posts = data.head(10)
            x_likes = range(1, 11)  # Post number
            y_likes = last_10_posts['likesCount'].tolist()

            # Calculate Comments per Post (last 10 posts)
            data['commentsCount'] = data['commentsCount'].astype(int)  # Convert commentsCount to integer
            x_comments = range(1, 11)  # Post number
            y_comments = last_10_posts['commentsCount'].tolist()
            # Calculate Engagement Rate
            total_likes = data['likesCount'].sum()
            total_comments = data['commentsCount'].sum()
            total_posts = len(data)
            engagement_rate = (total_likes + total_comments) / total_posts
            data['timestamp'] = data['timestamp'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y %H:%M:%S"))
            data = data.sort_values(by='timestamp', ascending=False)
            return render_template(
                'instagram_profile.html', 
                data=data,
                profile_data=profile_data, 
                average_likes=average_likes, 
                average_comments=average_comments,
                x_likes=x_likes,
                y_likes=y_likes,
                x_comments=x_comments,
                y_comments=y_comments,
                engagement_rate=engagement_rate,
                likes_data = y_likes,
                comments_data = y_comments
            )
        
        elif (option == 'hashtag'):
            Hashtag = request.form['instagramHashtagsInput']

           # Prepare the Actor input
            run_input = {
            "hashtags": [Hashtag],
            "resultsLimit": 20,
            }

            # Run the Actor and wait for it to finish
            run = instagram_client.actor("apify/instagram-hashtag-scraper").call(run_input=run_input)

            results_list = []
            comment_container = []

            for item in instagram_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            comment_string = ''.join(comment_container)
        
            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"


            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)




    elif platform == 'facebook':
        option = request.form['facebookOption']

        if (option == 'page'):
            Page_URL = request.form['facebookPageURL']

            run_input = { "startUrls": [
                { "url": Page_URL }
            ] }

            run = facebook_client.actor("apify/facebook-pages-scraper").call(run_input=run_input)

            results_list = []
            comment_container = []

            for item in facebook_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            comment_string = ''.join(comment_container)
        
            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"


            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)



        elif (option == 'group'):
            Group_URL = request.form['facebookGroupURL']

            run_input = {
            "startUrls": [{ "url": Group_URL}],
            "resultsLimit": 20,
            }

            run = facebook_client.actor("apify/facebook-groups-scraper").call(run_input=run_input)

            results_list = []
            comment_container = []

            for item in facebook_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            comment_string = ''.join(comment_container)

            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"


            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)



        if (option == 'review'):
            Review_URL = request.form['facebookReviewURL']

            run_input = {
                "startUrls": [{ "url": Review_URL}],
                "resultsLimit": 10,
            }

            run = facebook_client.actor("apify/facebook-reviews-scraper").call(run_input=run_input)

            results_list = []
            comment_container = []

            for item in facebook_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            comment_string = ''.join(comment_container)

            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"



            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)


        if (option == 'comments'):
            Comment_URL = request.form['facebookCommentsURL']

            run_input = {
                "startUrls": [{ "url": Comment_URL}],
                "resultsLimit": 50,
                "includeNestedComments": True,
                "viewOption": "RANKED_UNFILTERED",
            }

            run = facebook_client.actor("apify/facebook-comments-scraper").call(run_input=run_input)

            results_list = []
            comment_container = []

            for item in facebook_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"


            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)




    elif platform == 'twitter':
        option = request.form['twitterOption']

        if (option == 'comments'):
            twitter_Profile = request.form['twitterCommentsURL']

            run_input = {
                "handles": [twitter_Profile],
                "tweetsDesired": 100,
                "addUserInfo": True,
                "startUrls": [],
                "proxyConfig": { "useApifyProxy": True },
            }

            run = twitter_client.actor("quacker/twitter-scraper").call(run_input=run_input)
        
            results_list = []
            comment_container = []

            for item in twitter_client.dataset(run["defaultDatasetId"]).iterate_items():
                results_list.append(item)

            df = pd.DataFrame(results_list)

            text_series_list = [df['full_text'].astype(str)]

            text_strings = ['\n'.join(text_series) for text_series in text_series_list]

            for text_string in text_strings:
                comment_container.append(text_string)

            comment_string = ''.join(comment_container)

            words = comment_string.split()

            positive_words = []
            negative_words = []
            neutral_words = []
    
            for word in words:
                sentiment_score = afinn.score(word)
                
                if sentiment_score >= 0.05:
                    positive_words.append(word)
                elif sentiment_score <= -0.05:
                    negative_words.append(word)
                else:
                    neutral_words.append(word)

            sid_obj = SentimentIntensityAnalyzer()

            sentiment_dict = sid_obj.polarity_scores(comment_string)

            negative = sentiment_dict['neg']*100
            neutral = sentiment_dict['neu']*100
            positive = sentiment_dict['pos']*100
            total = ""
            # decide sentiment as positive, negative and neutral
            if sentiment_dict['compound'] >= 0.05 :
                total = "Positive"

            elif sentiment_dict['compound'] <= - 0.05 :
                total = "Negative"

            else :
                total = "Neutral"


            return render_template('result.html',overall_sentiment = sentiment_dict, nega = negative, posi = positive, neut = neutral, final = total, positive_list=positive_words, negative_list=negative_words, neutral_list=neutral_words)

    return "No data scraped."

def format_timestamp(timestamp):
   
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Format the datetime object as desired (DD/MM/YYYY HR:MIN:SEC)
    formatted_timestamp = dt.strftime("%d/%m/%Y %H:%M:%S")
    
    return formatted_timestamp

# Register the custom filter with Flask
app.jinja_env.filters['format_timestamp'] = format_timestamp

if __name__ == '__main__':
    app.run(debug=True)
