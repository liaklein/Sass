import os
import base64
import time
import facial_recognize as fr
import yoyo as yy
from slackclient import SlackClient
from slacker import Slacker
import requests
import cStringIO
import operator
# from Pillow import Image

def get_pretty_user(user_id):
    info = slacker_client.users.info(user_id)
    return info.body['user']['name']

def handle_command(parsed):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if 'kill' in parsed['type']:
        handle_kill(parsed['image'], parsed['user'], parsed['channel'])
        return
    if 'enroll' in parsed['type']:
        result = handle_registration(parsed['image'], parsed['user'])['result']
        if result.get('error'):
            response = "Error: " + result['error']
        else:
            response = "User " + get_pretty_user(parsed['user']) + " successfully registered!"
    if 'score' in parsed['type']:
        response = "Score is yet to be implemented"
        handle_score(parsed['channel'])
        return
    slack_client.api_call(
        "chat.postMessage",
        channel=parsed['channel'],
        text=response,
        as_user=True)

def handle_score(
        channel,
        ):  #this gets called when a user wants to see the score

    sorted_score = sorted(score.items(), key=operator.itemgetter(1))
    strscore = ""

    for x in sorted_score:
        strscore = strscore + get_pretty_user(x[0]) + ": " + str(x[1]) + "\n"

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="Score\n"
         + strscore,
        as_user=True)  #we will make it look nicer later

def handle_registration(image_file, sender):
    image_64 = base64.b64encode(image_file).decode('ascii')
    if score.get(sender) == None:
        score[sender] = 0
    return fr.enroll_player(image_64, sender)  #need to register in gallery


def handle_kill(image, sender, channel):
    if sender not in score:
        slack_client.api_call(
            "chat.postMessage",
            channel=parsed['channel'],
            text="Sorry, you (" + get_pretty_user(sender) + ") aren't enrolled yet.",
            as_user=True)
        return
    image_files = yy.getImages(image)
    print image_files
    image_64_list = []
    for im in image_files:
        with open(im, "rb") as f:
            image_64_list.append(base64.b64encode(f.read()).decode('ascii'))
    error, players = fr.get_players_from_image(image_64_list)
    if error == "ERROR":
        print("did not detect player in picture")
        slack_client.api_call(
            "chat.postMessage",
            channel=parsed['channel'],
            text="Sorry, couldn't find a player in the picture.",
            as_user=True)
        return
    players = list(set(players))
    #increment the sender's score by how many people they got
    score[sender] = score[sender] + len(players)
    if len(players) > 0:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text="Scored a point!\n" + get_pretty_user(sender)
             + " : " + str(score[sender]),
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
                text = get_pretty_user(player) + " : " + str(score[player]),
            as_user=True)
    else:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text="People were detected, but none of them seem to be players. Try again!\n",
            as_user=True)


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
            print(output)
            if output:
                if "message" in output['type']:
                    if output.get("subtype",
                                  None) and "file_share" in output['subtype']:
                        f = output['file']
                        headers = {'Authorization': 'Bearer ' + SLACK_BOT_TOKEN}
                        image_data = requests.get(f['url_private_download'], headers=headers).content
                        if 'enroll' in output['file']['title'].lower():
                            ty = 'enroll'
                            image = image_data
                        else:
                            file_name = ".tmp-image-file"
                            with open(file_name, "wb+") as fil:
                                fil.write(image_data)
                            ty = 'kill'
                            image = file_name
                        return {
                            'image': image,
                            'channel': output['channel'],
                            'user': output['user'],
                            'type': ty
                        }
                    elif output.get('text', None) and "!score" in output['text']:
                        return {
                            'type': 'score',
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

        for user in fr.get_gallery_users():
            if 'Elizabeth' not in user:
                score[user] = 0

        print score

        READ_WEBSOCKET_DELAY = 1
        if slack_client.rtm_connect():
            print("StarterBot connected and running!")
            while True:
                parsed = parse_slack_output(slack_client.rtm_read())
                if parsed:
                    handle_command(parsed)
                    time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
    else:
        print('Cannot get BOT_ID')
