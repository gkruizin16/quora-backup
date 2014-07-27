from quora import Quora, Activity
import click
import os
import json

def sync_items(old, new):
    # need to come up with a faster way to do this
    # db implementations will be much faster
    ids = []
    for item in old:
        ids.append(item['id'])
    for item in new:
        if item['id'] not in ids:
            old.append(item)
    return old

def backup(new, filepath):
    if os.path.isfile(filepath):
        with open(filepath) as outfile:
            old = json.load(outfile)
        old = sync_items(old, new)
        with open(filepath, 'w') as outfile:
            json.dump(old, outfile)
    else:
        with open(filepath, 'w') as outfile:
          json.dump(new, outfile)

@click.command()
@click.option('--path', '-p', help='specify a path to store the JSON files at')
@click.argument('user')
def sync(user, path):
    if path is None:
        path = os.getcwd()
    quora = Quora()
    activity = quora.get_activity(user)
    backup(activity.answers, os.path.join(path, 'answers.json'))
    backup(activity.questions, os.path.join(path, 'questions.json'))
    backup(activity.upvotes, os.path.join(path, 'upvotes.json'))
    backup(activity.question_follows, os.path.join(path, 'question_follows.json'))
    # backup(activity.user_follows, os.path.join(path, 'user_follows.json'))

if __name__ == '__main__':
    sync()