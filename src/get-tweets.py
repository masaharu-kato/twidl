"""
    Twitter API Test: Get tweets
"""
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Union
import requests
import requests_oauthlib

class Twitter:
    URL_FMT = 'https://api.twitter.com/1.1/%s.json'

    def __init__(self):
        with open('conf/apikeys.json') as f:
            _APICFG = json.load(f)

        self.session = requests_oauthlib.OAuth1Session(
            _APICFG['Twitter']['API_Key'],
            _APICFG['Twitter']['API_Secret_Key'],
            _APICFG['Twitter']['Access_Token'],
            _APICFG['Twitter']['Access_Token_Secret'],
        )

    def get(self, twurl, **params):
        res = self.session.get(self.URL_FMT % twurl, params=params)
        assert res.status_code == 200
        return json.loads(res.text)

def save_as_json(data:Union[List, Dict], path:Path):
    with path.open(mode='w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def printd(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)

def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-u', '--username', required=True)
    argp.add_argument('-o', '--output', required=True)
    args = argp.parse_args()
    dir_out = Path(args.output)
    dir_out.mkdir(parents=True, exist_ok=True)

    twitter = Twitter()

    res = twitter.get('friends/ids', screen_name=args.username, count=5000)
    friend_ids = res['ids']
    save_as_json(res, dir_out/'friend_ids.json')
    
    for user_id in friend_ids:

        res = twitter.get('users/show', user_id=user_id)
        username = str(res['screen_name'])
        printd(username, '', end='')

        c_dir_out = dir_out/username
        c_dir_out.mkdir(exist_ok=True)
        save_as_json(res, c_dir_out/'profile.json')

        c_dir_res = c_dir_out/'res'
        c_dir_res.mkdir(exist_ok=True)

        max_id = None
        total_data = []

        while data := twitter.get(
            'statuses/user_timeline',
            user_id=user_id, max_id=max_id, count=200, trim_user=True
        ):
            init_max_id = max_id
            printd('.', end='')
            total_data.extend(data)
            # Save images
            for tweet in data:
                max_id = tweet['id_str']
                for media in [
                    *(tweet.get('entities', {}).get('media', [])),
                    *(tweet.get('extended_entities', {}).get('media', []))
                ]:
                    url = str(media.get('media_url'))
                    if url:
                        cpath = c_dir_res/(url.split('/')[-1])
                        if not cpath.exists():
                            res = requests.get(url)
                            with cpath.open(mode='wb') as f:
                                f.write(res.content)
            if init_max_id == max_id:
                break

        # Save tweets
        save_as_json(total_data, c_dir_out/'tweets.json')

        printd('OK.')


if __name__ == '__main__':
    main()
