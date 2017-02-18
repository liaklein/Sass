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


def handle_kill(score, image, sender, channel):
    #get all of the registered players who are in the photo
    players = fr.get_players_from_image(image)
    #increment the sender's score by how many people they got
    score[sender] = score[sender] + len(players)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="Scored a point!\n" + sender + " : " + score[sender],
        as_user=True)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="Lost a point!\n",
        as_user=True)
    for player in players:  #decrement each player's score who got caught
        score[player] -= 1
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=player + " : " + score[player],
            as_user=True)
    return score


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print(output['type'])
            if output:
                if "message" in output["type"] and output.get(
                        "subtype", None) and "file_share" in output['subtype']:
                    f = output['file']
                    image_file = cStringIO.StringIO(
                        urllib.urlopen(f['url_private_download'])
                        .read()).read()
                    image_64 = image_file.encode("base64")
                    return {
                        'image': image_64,
                        'channel': output['channel'],
                        'user': output['user']
                    }
    return None


if __name__ == "__main__":
    score = {}  #score board starts out at empty dictionary
    with open('.slack_bot_token') as f:
        SLACK_BOT_TOKEN = f.readline().strip()
    BOT_NAME = 'sassbot'
    slack_client = SlackClient(SLACK_BOT_TOKEN)
    slacker_client = Slacker(SLACK_BOT_TOKEN)
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                BOT_ID = user.get('id')
    else:
        print("could not find bot user with the name " + BOT_NAME)
        exit()

    if BOT_ID:
        AT_BOT = "<@" + BOT_ID + ">"
        EXAMPLE_COMMAND = "do"

        slack_client = SlackClient(SLACK_BOT_TOKEN)

        READ_WEBSOCKET_DELAY = 1
        if slack_client.rtm_connect():
            print("StarterBot connected and running!")
            while True:
                parsed = parse_slack_output(slack_client.rtm_read())
                if parsed:
                    handle_command(parsed, score)
                    time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
    else:
        print('Cannot get BOT_ID')
