from bs4 import BeautifulSoup as bs
import requests
import json
import urllib
import re
import operator

api_key = 'AIzaSyAj4EeorHRFlXalLXhBfosuWdOoiAuIWGk'

print("\nExample youtube playlist link: https://www.youtube.com/playlist?list=PLLssT5z_DsK-h9vYZkQkYNWcItqhlRJLN \n")

playlist_link = raw_input("Enter a link to a youtube playlist: ")

print("Calculating total playlist length...")

request = requests.get(playlist_link);

page = request.text;

soup = bs(page, 'html.parser');

res = soup.findAll('tr', {'class': 'pl-video yt-uix-tile '})

def getId(response):
    return response.get("data-video-id");

video_id_list = map(getId, res);

def getVideoLength(video_id):
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails"
    response = urllib.urlopen(searchUrl).read()
    data = json.loads(response)
    duration = data['items'][0]['contentDetails']['duration']
    duration_min_sec_array = re.split('PT|M|S', duration)
    sliced_array_elements = slice(1, 3);
    duration_min_sec = duration_min_sec_array[sliced_array_elements]
    if duration_min_sec[1] == '':
        duration_min_sec[1] = 0;

    if duration_min_sec[0] == '':
        duration_min_sec[0] = 0;
    return map(int, duration_min_sec)

video_lengths = map(getVideoLength, video_id_list);
total_length = [sum(pair[0] for pair in video_lengths), sum(pair[1] for pair in video_lengths)]

def reduceToBelow60(number):
    while number > 60:
        number -= 60;
    return number;


hh = (total_length[0] / 60) + (total_length[1] / 3600)
mm = reduceToBelow60((total_length[1] / 60) + total_length[0])
ss = reduceToBelow60(total_length[1])
total_length_hh_mm_ss = [hh, mm, ss];

print 'Total length of playlist is %i hours %i minutes %i seconds.' % (hh, mm, ss)
