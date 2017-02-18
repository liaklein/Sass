import os
import time
import facial_recognize as fr
from slackclient import SlackClient
from slacker import Slacker
# from Pillow import Image
import urllib, cStringIO

def handle_command(parsed, score):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Analyzing Photo from: " + parsed['user'] + " in " + parsed[
        'channel']
    slack_client.api_call(
        "chat.postMessage",
        channel=parsed['channel'],
        text=response,
        as_user=True)

def handle_score(
        score, channel,
        command):  #this gets called when a user wants to see the score
    #doesn't edit score, so doesn't need to return it
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="Score\n" + str(sorted(score)),
        as_user=True)  #we will make it look nicer later

def handle_registration(score, image, sender):
    fr.enroll_player(image, sender)  #need to register in gallery
    score[sender] = 0  #when you register your score gets initialized to zero
    return score

def handle_kill():
    #get all of the registered players who are in the photo
    f = open("grace.jpg","r+")
    image_file = f.read()
    image = image_file.encode("base64")
    players = fr.get_players_from_image(image)
    #increment the sender's score by how many people they got
    print players

handle_kill()
