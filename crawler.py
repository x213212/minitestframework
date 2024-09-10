from threading import Lock
# import requests
# session = requests.Session()
json_result = 'results.json'
json_online = 'online_bugzilla.json'
json_merged = 'final_results.json'
online_json_result = {}
online_json_result['ID'] = []
online_type = {}
online_status = {}
lock = Lock()

# Bug monitor
total_count = 0
bug_list = {}

def get_bug_status(bugid, type_t=None):
    global total_count
    # r = session.get(
    #     "http://xxx/bugzilla/show_bug.cgi?id="+str(get_id))
    # soup = BeautifulSoup(r.text, "html.parser")
    get_bug_status = 1

    lock.acquire()
    # if type_t == None or component in type_t:
    online_json_result['ID'].append(bugid)
    # Bug monitor
    total_count += 1
    lock.release()

    return "- Get Bug Id: " + bugid + " Online Status Done."
