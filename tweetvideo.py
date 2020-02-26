import tweepy
import os
import io
import urllib.request
import subprocess
import glob
import stat
from google.cloud import vision
from google.cloud.vision import types
import keys
from PIL import Image, ImageDraw, ImageFont
import PIL

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_key = keys.access_key
access_secret = keys.access_secret

def get_all_tweets(account1,number1,filepath):
        #files = glob.glob('C:/Users/Vanquish/Desktop/pyve/VisionApi/downloadimage/')
        #for f in files:
            #os.chmod(f, stat.S_IWRITE)
            #os.remove(f)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        alltweets = []
        account = account1
        number = number1
        while (int(number) > 200):
                raise Exception('The number you entered is biger than 200, please enter a number less than 200')
        try:
                new_tweets = api.user_timeline(screen_name = account,count=1)
        except:
                raise Exception('This is not a valid Twitter account')
        alltweets.extend(new_tweets)
        try:
                oldest = alltweets[-1].id - 1
        except:
                raise Exception('This account does not have this many tweets')
        tweetnum = 1
        while(tweetnum <= int(number)):
                new_tweets = api.user_timeline(screen_name = account, count=1, max_id = oldest)
                alltweets.extend(new_tweets)
                tweetnum += 1
                oldest = alltweets[-1].id - 1

        outtweets = []
        fileorder = 1
        for tweet in alltweets:
                try:
                        url = str(tweet.entities['media'][0]['media_url'])
                        name = filepath + str(fileorder) + '.jpg'
                        urllib.request.urlretrieve(url,name)
                        fileorder += 1
                except (NameError, KeyError):
                       
                        pass
                else:
                        
                        outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])
        #imagenum = fileorder - 1
        #print(str(imagenum)+'images detected')
        return fileorder
def googlevision(account1,number1,filepath1, filepath2):
        filenumber = int(get_all_tweets(account1,number1,filepath1))
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'TweetImage-ef41c01d2f34.json'
        client = vision.ImageAnnotatorClient()
        path = filepath2
        file_name = 1
        if(filenumber == 1):
                print("No image posted by this account in the recent tweets")
        while(file_name < filenumber):
                addtxt = Image.open(os.path.join(path, str(file_name) + '.jpg'))
                draw = ImageDraw.Draw(addtxt)
                with io.open(os.path.join(path, str(file_name) + '.jpg'),'rb') as image_file:
                        content = image_file.read()
                image = vision.types.Image(content = content)
                response = client.face_detection(image=image)
                faces = response.face_annotations
                # Names of likelihood from google.cloud.vision.enums
                likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
                person = 1
                flag = 0
                (x, y) = (50,200)
                font = ImageFont.truetype('Roboto-Bold.ttf', size=20)
                color = 'rgb(213,53,123)'
                for face in faces:
                        flag = 1
                        if (likelihood_name[face.anger_likelihood] == 'VERY_LIKELY'):
                                message = ('Person' + str(person) + ' is very likely to be angery')
                        elif (likelihood_name[face.anger_likelihood] == 'LIKELY'):
                                message = ('Person' + str(person) + ' is likely to be angery')
                        elif (likelihood_name[face.joy_likelihood] == 'VERY_LIKELY'):
                                message = ('Person' + str(person) + ' is very likely to be happy')
                        elif (likelihood_name[face.joy_likelihood] == 'LIKELY'):
                                message = ('Person' + str(person) + ' is likely to be happy')
                        elif (likelihood_name[face.surprise_likelihood] == 'VERY_LIKELY'):
                                message = ('Person' + str(person) + ' is very likely to be surprised')
                        elif (likelihood_name[face.surprise_likelihood] == 'LIKELY'):
                                message = ('Person' + str(person) + ' is likely to be surprised')
                        else:
                                message = ('Unable to determine person' + str(person))
                        draw.text((x, y), message, fill=color, font=font)
                        person += 1
                        x += 25
                
                if (flag == 0):
                        message = ('No face detected')
                        draw.text((x, y), message, fill=color, font=font)
                addtxt = addtxt.save(os.path.join(path, str(file_name) + 'txt.jpg'))
                if response.error.message:
                        raise Exception(
                                '{}\nFor more info on error messages, check: '
                                'https://cloud.google.com/apis/design/errors'.format(
                                        response.error.message))
                file_name += 1

def Image2Video(videoname, filepath1):
        subprocess.call('ffmpeg -framerate 1/3 -start_number 1 -i '+ filepath1 +'%1dtxt.jpg '+ videoname +'.avi')

