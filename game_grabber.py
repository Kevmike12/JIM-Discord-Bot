import requests, json


class SteamGameGrabber(object):

    def __init__(self):

        self.url = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.start_tag = "var rgGames"
        self.end_tag = "var rgChangingGames"

        self.last_data = {}

    def send_request(self):

        try:
            response = requests.get(self.url, headers=self.headers)
            raw_data = str(response.content, encoding="utf-8")
        except:
            return [False, "Something Wrong! Connection Lost!"]

        else:
            if response.status_code == 200:
                return [True, raw_data]
            else:
                return [False, "Check Your Connection ( status_code is Not 200 )!"]

    def pars_data(self, get_input):

        def find_between(s, first, last):

            try:
                start = s.index(first) + len(first)
                end = s.index(last, start)
            except:
                return [False, "Parsing Error"]
            else:
                return [True, s[start:end]]

        if "<title>Steam Community :: Error</title>" in get_input:
            return [False, "I Can Not Find This ID on Steam Server"]

        if '<div class="profile_private_info">' in get_input:
            return [False, "This profile is private, I can not Decode it, sorry."]

        get_data = find_between(get_input, self.start_tag, self.end_tag)

        if get_data[0] is True:

            dict_data = json.loads(get_data[1].strip().lstrip("=").rstrip(";").strip())

            try:
                for box in dict_data:

                    game_id = str(box['appid']).strip()
                    game_name = box['name'].strip()

                    if game_name in self.last_data:
                        pass

                    else:

                        self.last_data[game_name] = game_id
            except:
                return [False, "Format is Wrong"]

            else:
                return [True, self.last_data]

        else:
            return [False, get_data[1]]

    def call_all(self, get_id):

        if get_id.strip() == "":
            return "Please Insert Your Steam ID"

        else:
            new_id = self.URLstrip(get_id)

            if 'id' in get_id:
                self.url = 'http://steamcommunity.com/id/{0}/games/?tab=all'.format(new_id)
            elif 'profile' in get_id:
                self.url = 'http://steamcommunity.com/profiles/{0}/games/?tab=all'.format(new_id)

            get_state_1 = self.send_request()

            if get_state_1[0] is True:

                get_state_2 = self.pars_data(get_state_1[1])
                return get_state_2[1]

            else:
                return get_state_1[1]

    def URLstrip(self, url):
        if 'id' in url:
            part = url.find('id')
            new_id = url[int(part)+3:len(url)]
            return new_id
        elif 'profile' in url:
            part = url.find('profiles')
            new_id = url[int(part)+9:len(url)]
            return new_id

def getSameGames(user_list):
    total_games = []
    final_list = []
    for user in user_list:
        your_id = user
        make_object = SteamGameGrabber()
        get_result = make_object.call_all(your_id)
        for names, appid in get_result.items():
            total_games.append(names)
    for item in total_games:
        if total_games.count(item) >= len(user_list):
            final_list.append(item)
    new = set(final_list)
    return(new)
