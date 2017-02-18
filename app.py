import os
import time
from slackclient import SlackClient

def handle_command(command, channel, score):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Analyzing Photo at: " + command
    slack_client.api_call(
        "chat.postMessage", channel=channel, text=response, as_user=True)

def handle_score():
    pass

def handle_registration():
    pass

def handle_kill():
    pass

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
                if "message" in output["type"] and output[
                        'subtype'] and "file_share" in output['subtype']:
                    return output['file']['id'], output['channel']
    return None, None


if __name__ == "__main__":
    score = {} #score board starts out at empty dictionary
    with open('.slack_bot_token') as f:
        SLACK_BOT_TOKEN = f.readline().strip()
    BOT_NAME = 'sassbot'
    slack_client = SlackClient(SLACK_BOT_TOKEN)
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
                command, channel = parse_slack_output(slack_client.rtm_read())
                if command and channel:
                    handle_command(command, channel, score)
                    time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
    else:
        print('Cannot get BOT_ID')
