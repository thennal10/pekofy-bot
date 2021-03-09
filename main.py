import praw
import string
from datetime import datetime
import time
import random
from replies import Replies
import credentials
import pekofy as peko  # because it sounds better

bot_name = credentials.bot_name
author = credentials.author
reddit = praw.Reddit(client_id=credentials.client_id,
                     client_secret=credentials.client_secret,
                     username=credentials.bot_name,
                     password=credentials.bot_pass,
                     user_agent=credentials.user_agent)
subreddit_list = ['u_'+bot_name, 'u_'+author, 'hololive', 'VirtualYoutubers', 'Hololewd', 'okbuddyhololive',
                  'goodanimemes', 'VtuberV8', 'Priconne', 'AmeliaWatson']
subreddit = reddit.subreddit('+'.join(subreddit_list))
keyphrase = '!pekofy'
keyphrase_delete = '!unpekofy'
replies = Replies()


def reply_f(reply_message, action_type, comment_obj):
    """
    reply to a comment

    :param reply_message: the message that's gonna be sent
    :type reply_message: string
    :param action_type: description of the current action for easier debugging
    :type action_type: string
    :param comment_obj: the comment to reply
    :type comment_obj: praw.models.Comment
    """
    global comments_replied
    comments_replied += 1

    # if it couldn't be pekofied, give a random pekora clip
    if reply_message in ["NOTHING_CHANGED", "NO_LETTER"]:
        reply_message = random.choice(replies.nothing_changed_reply_list)

    # all things set, ready to comment. Last chance to check if the reply is already commented.
    if already_replied_to(comment_obj, reply_message):
        return
    try:
        comment_obj.reply(reply_message)
    except Exception as e:  # unable to comment on the post, potential ban
        comments_replied -= 1
        print(f"Couldn't reply: {e}")
        print(f'Tried comment: https://www.reddit.com{comment_obj.permalink}')
        print(f'Reply: {reply_message}')
        print("------------------------")
        notify_author(e, comment_obj, reply_message)
        return
    print(f"{action_type}: https://www.reddit.com{comment_obj.permalink}")
    print(f"Message: {reply_message}")
    print("------------------------")


def already_replied_to(comment, reply):
    """ returns if already replied the same type of comment or not """
    comment.refresh()
    comment.replies.replace_more()
    child_comments = comment.replies.list()
    for top_comment in child_comments:
        if top_comment.parent().id != comment.id:
            break
        if top_comment.author == bot_name:
            if top_comment.body == reply:
                print("ALREADY REPLIED, CONTINUING...")
                print("------------------------")
                return True
            for attribute, value in replies.__dict__.items():
                if isinstance(value, str):
                    if top_comment.body == value:
                        print(f"ALREADY REPLIED WITH `{attribute}`, CONTINUING...")
                        print("------------------------")
                        return True
                if isinstance(value, list):
                    if top_comment.body in value and reply in value:
                        print(f"ALREADY REPLIED WITH `{attribute}`, CONTINUING...")
                        print("------------------------")
                        return True
    return False


def notify_author(exception, comment="None", tried_reply="None"):
    """ Notifies to the author, don't forget to whitelist the bot if your PM's are closed """

    title = datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
    if comment != "None" and tried_reply != "None":
        body = f'{bot_name} has run into an error: {exception}\n' \
               f'Here\'s the [link](https://www.reddit.com{comment.permalink}) to the comment.\n' \
               f'Tried to reply this: {tried_reply}'
    else:
        body = f'{bot_name} has run into an error: {exception}\n'
    reddit.redditor(author).message(title, body)


def reply_chance(percent):
    return random.randint(0, 100) <= percent


usage_limit = 3  # limiter to prevent spam
comments_replied = 0
comments_scanned = 0

# time is used for exponential back off in case reddit server is unable to respond
initial_wait_time = 10
current_wait_time = initial_wait_time
max_wait_time = 600

while 1:
    try:  # exception handling at it's finest (lol)
        # scan each comment
        for comment in subreddit.stream.comments():
            comments_scanned += 1
            body = comment.body.lower()

            # comment has been deleted or it's author is the bot itself, move on
            if not comment.author or comment.author == bot_name:
                continue

            # pain peko (not used regex for faster results)
            if body in ["pain", "pain.", "pain...", "pain peko"] and reply_chance(50):
                reply_f(replies.pain_peko_reply, "Pain peko'd", comment)

            # hey moona
            if "moona" in body and "pekora" in body and reply_chance(25):
                reply_f(replies.hey_moona_reply, "Hey Moona'd", comment)

            # feedback gratitude
            if comment.parent_id != comment.link_id:  # not top level comment
                if comment.parent().author:  # parent comment is not deleted
                    if comment.parent().author.name == bot_name:  # replying to the bot

                        # positive feedback reply
                        if any(word in body for word in ["good", "best", "amazing", "based"]) and "bot" in body:
                            reply_f(random.choice(replies.thanks), "Thanked", comment)
                        elif "love you" in body:
                            reply_f(random.choice(replies.loves), "Loved", comment)
                        elif "cute" in body:
                            reply_f(random.choice(replies.cutes), "Cute'd", comment)

                        # negative feedback reply
                        elif "bad" in body and "bot" in body:
                            reply_f(random.choice(replies.sorrys), "Sorried", comment)
                        # others
                        elif "insult me peko" in body:
                            reply_f(random.choice(replies.insults), "Insulted", comment)


            # both pekofy and unpekofy written
            if keyphrase in comment.body and keyphrase_delete in comment.body:
                reply_f(replies.confused_reply, "Confused", comment)
                continue

            # if keyword found, try to pekofy
            if keyphrase in comment.body:

                # can't pekofy due to comment not having any parent
                if not comment.parent().author:
                    continue

                # parent is a post, pekofy accordingly
                if comment.parent_id == comment.link_id:
                    if comment.submission.selftext:  # either text or link post
                        reply_f(peko.pekofy(comment.submission.title + '\n\n' + comment.submission.selftext),
                                "Pekofied text/link post", comment)
                    else:  # image post, only pekofy title
                        reply_f(peko.pekofy(comment.submission.title), "Pekofied post title", comment)
                    continue

                # don't pekofy if limit already reached.
                if comment.parent().body == replies.limit_reached_reply and comment.parent().author == bot_name:
                    continue

                # someone tried to break it by recursive calling, kindly say no
                if keyphrase in comment.parent().body:
                    reply_f(replies.no_recursion_reply, "No'd", comment)
                    continue

                # if same sentence has been pekofied too much already, don't pekofy
                current_usage = 0
                comment_climb = comment
                for i in range(usage_limit):
                    if comment_climb.parent_id == comment_climb.link_id:
                        break
                    if comment_climb.parent().author and comment_climb.parent().author == bot_name:
                        comment_climb = comment_climb.parent()
                        if comment_climb.parent_id == comment_climb.link_id:
                            break
                        if comment_climb.parent().author and keyphrase in comment_climb.parent().body:
                            comment_climb = comment_climb.parent()
                            current_usage += 1
                if current_usage == usage_limit:
                    reply_f(replies.limit_reached_reply, "Limit reached", comment)
                    continue

                # someone tried to pekofy a good/bad bot reply, don't pekofy
                if comment.parent().body:
                    if "good bot" == comment.parent().body.lower() or "good bot." == comment.parent().body.lower() or \
                            "bad bot" == comment.parent().body.lower() or "bad bot." == comment.parent().body.lower():
                        reply_f(replies.bot_score_abuse_reply, "Potential abuse prevented", comment)
                        continue

                # try to reply to the comment
                reply_f(peko.pekofy(comment.parent().body), "Pekofied", comment)

            # delete keyphrase found
            if keyphrase_delete in comment.body and comment.parent().author == bot_name and comment.parent().body:
                print("Unpekofied: ")
                print(f'Reply: {comment.parent().body}')
                comment.parent().delete()
                print("------------------------")

            # More than [50] comments has been scanned without an incident, reset wait time.
            if comments_scanned % 50 == 0:
                current_wait_time = initial_wait_time
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Terminating...")
        break
    except praw.exceptions.RedditAPIException as e:
        print(f"RedditAPIException: {e}")
        notify_author(e)
    except praw.exceptions.PRAWException as e:
        print(f"PRAWException: {e}")
        notify_author(e)
    except Exception as e:
        print(e)
        notify_author(e)
    finally:
        print("------------------------")
        print(f"Replied comments so far: {comments_replied}")
        print(f"Scanned comments so far: {comments_scanned}")
        comments_replied = 0
        comments_scanned = 0

        # not-so-exponential back off
        time.sleep(current_wait_time)
        if not current_wait_time > max_wait_time:
            current_wait_time *= 2
