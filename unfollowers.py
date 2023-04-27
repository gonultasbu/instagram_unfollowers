from instagram_private_api import Client, ClientCompatPatch
import numpy as np 
import time
import getpass 
import sys
import os 
import socket

def get_all_followers(client, user_id):
    rank_token = client.uuid
    followers = []
    max_id = None
    while True:
        try:
            if max_id is not None:
                results = client.user_followers(user_id, rank_token, max_id=max_id)
            else:
                results = client.user_followers(user_id, rank_token)
        except socket.timeout:
            time.sleep(1)
            continue
        max_id = results.get("next_max_id")
        followers.extend(results['users'])
        if max_id is None:
            break
        time.sleep(0.5)
    return followers

def get_all_following(client, user_id):
    rank_token = client.uuid
    following = []
    max_id = None
    while True:
        try:
            if max_id is not None:
                results = client.user_following(user_id, rank_token, max_id=max_id)
            else:
                results = client.user_following(user_id, rank_token)
        except socket.timeout:
            time.sleep(1)
            continue
        max_id = results.get("next_max_id")
        following.extend(results['users'])
        if max_id is None:
            break
        time.sleep(0.5)
    return following


def list_diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1] 
    return li_dif 

print("\n \nIMPORTANT DISCLAIMER: DO NOT USE THIS TOOL TOO FREQUENTLY (MORE THAN SEVERAL TIMES IN A MINUTE), YOUR ACCOUNT MIGHT GET FLAGGED! \n \n ")

WHICH_USERNAME = input(f"Which username do you want to get the unfollowers for? \n")
USER_NAME = input(f"What is your instagram username? \n")
PASSWORD = getpass.getpass(prompt=f'What is your instagram password? (Your input might not appear on console, just type and press enter.) \n')

try: 
    api = Client(USER_NAME, PASSWORD)
except:
    sys.exit('Login unsucessful, wrong password?')

# results = api.feed_timeline()
rnk_token_1 = api.generate_uuid()
rnk_token_2 = api.generate_uuid()
# u_id = api.authenticated_user_id
u_id = api.username_info(WHICH_USERNAME)['user']['pk']
fwing = api.user_following(u_id, rnk_token_1,max_id='0')
fwers = api.user_followers(u_id, rnk_token_2,max_id='0')
fwing_list = []
fwers_list = []
fwing_list.append(np.sort([fwing['users'][idx]['username'] for idx in np.arange(len(fwing['users']))]))
fwers_list.append(np.sort([fwers['users'][idx]['username'] for idx in np.arange(len(fwers['users']))]))
fwing_nmid = fwing.get('next_max_id')
fwers_nmid = fwers.get('next_max_id')

# followers = get_all_followers(api, u_id)
print('Parsing the following list! Please be patient. There is a delay to prevent your account from getting flagged!')
while (fwing_nmid is not None):
    time.sleep(np.random.rand(1)[0]*2)
    fwing = api.user_following(u_id, rnk_token_1, max_id=fwing_nmid)
    fwing_list.append(np.sort([fwing['users'][idx]['username'] for idx in np.arange(len(fwing['users']))]))
    fwing_nmid = fwing.get('next_max_id')

print('Parsing the followers list! Please be patient. There is a delay to prevent your account from getting flagged!')
while (fwers_nmid is not None):
    time.sleep(np.random.rand(1)[0]*2)
    fwers = api.user_followers(u_id, rnk_token_2, max_id=fwers_nmid)
    fwers_list.append(np.sort([fwers['users'][idx]['username'] for idx in np.arange(len(fwers['users']))]))
    fwers_nmid = fwers.get('next_max_id')
    
fwers_list_flat = [j for sub in fwers_list for j in sub]
fwing_list_flat = [j for sub in fwing_list for j in sub]

print('Here are the unfollowers! \n\n')
print(np.sort(list_diff(fwers_list_flat, fwing_list_flat)))

print('_________________________________________')
print('Here are the followers you are not following! \n\n')
print(np.sort(list_diff(fwing_list_flat, fwers_list_flat)))

os.system("pause")