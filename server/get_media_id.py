import json
import requests
import configparser


class Media(object):
    """docstring for Media"""
    def __init__(self, app_id, secret, picture_path):
        self.app_id = app_id
        self.secret = secret
        self.access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
        self.media_upload_url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
        self.picture = {'media': open(picture_path, 'rb')}
        self.access_token = self.get_access_token()

    def get_access_token(self):
        res = requests.get(url=self.access_token_url.format(appid=self.app_id, secret=self.secret))
        data = json.loads(res.text)
        access_token = data.get('access_token')
        return access_token

    def get_media_id(self):
        res = requests.post(url=self.media_upload_url.format(access_token=self.access_token), files=self.picture)
        data = json.loads(res.text)
        media_id = data.get('media_id')
        return media_id


if __name__ == '__main__':

    conf = configparser.ConfigParser()
    conf.read('/home/admin/bugaboo/server/config.ini')
    app_id = conf.get('app', 'app_id')
    app_secret = conf.get('app', 'app_secret')
    picture = conf.get('weixin', 'picture')
    md = Media(app_id=app_id, secret=app_secret, picture_path=picture)
    print("access_token", md.access_token)
    media_id = md.get_media_id()
    print("media_id", media_id)
    conf.set('weixin', 'media_id', media_id)
    data = {
        'award_1': 1,
        'award_2': 1,
        'award_3': 1,
        'award_4': 5,
        'award_5': 5,
    }
    for key in data:
        conf.set('raffle', key, data[key])
    with open('config.ini', 'w') as fp:
        conf.write(fp)


