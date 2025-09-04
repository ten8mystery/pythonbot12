from requests import post, get
from threading import Thread
from time import time,sleep
import base64
import itertools

usedproxies = set()
totalproxies = 0

def divLists(threads) :
    global usedproxies,totalproxies
    proxies = []
    proxysources = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",]
    for proxysource in proxysources :
        try :
            proxies+=list(set(get(proxysource).text.splitlines()))
        except :
            pass
    proxies=set(proxies)-usedproxies
    totalproxies=len(proxies)
    proxygroups = list([] for _ in range(threads))
    for index, proxy in enumerate(proxies):
        proxygroups[index % threads].append(proxy)
    return proxygroups

def likeItem(proxygroup, data) :
    global usedproxies
    stime = time()
    for proxy in proxygroup :
        try :
            if time() - stime >= 5*60 :
                return
            if post(data[0],data=data[1],headers={"User-Agent":"","Content-Type":"application/x-www-form-urlencoded","Cookie":"gd=1"},proxies={"http":proxy,"https":proxy},timeout=10).text.startswith("1") :
                print(f"Sent View!")
            #usedproxies.add(proxy)
        except :
            pass
    while True :
        if time() - stime >= 5*60 :
            return
        sleep(5)

if __name__ == "__main__" :
    while True : 
        command = input("Select Command -> '0' Close Program, '1' Start LikeBot V2 : ")
        if command == "0" :
            break
        elif command == "1" :
            # ItemID , Type (1 = level, 2 = list)
            item = ["125587165","1"]
            data = ["endpoint","data"]
            if item[1] == "1" :
                data[0] = "https://www.boomlings.com/database/downloadGJLevel22.php"
                data[1] = f"levelID={item[0]}&inc=1&udid=1&secret=Wmfd2893gb7"
            else :
                data[0] = "https://www.boomlings.com/database/getGJLevels21.php"
                data[1] = f"str={item[0]}&inc=1&type=25&udid=1&secret=Wmfd2893gb7"
            while True :
                try :
                    threads = int(input("How many Threads do you want? : ")) #generally recommended a few tens to hundreds for speed
                    if threads > 0 :
                        break
                    else :
                        print("Threads have to be over 0!")
                except ValueError :
                    print("Threads have to be a Number!")
            while True :
                try :
                    proxygroups = divLists(threads)
                    print(f"Proxies fetched : {totalproxies}")
                    threadslist = [Thread(target=likeItem,args=(proxygroups[index],data))for index in range(threads)]
                    for thread in threadslist :
                        thread.start()
                    for thread in threadslist :
                        thread.join()
                    print("Finished Current Proxy Batch!")
                except :
                    pass
        else :
            print("Invalid Command!")
