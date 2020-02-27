import threading
import tweetvideo
import queue

def queue_func(name, number, filepath1, filepath2):
    q = queue.Queue()
    q.put(tweetvideo.googlevision(name, number, filepath1, filepath2))
    q.put(tweetvideo.Image2Video(name, filepath1))
    while not queue.Empty():
        q.get()

def pipelining(names:list, numbers:list, filepath1:list, filepath2:list):
    """
    x = 0
    thread_list = []
    for i in range(len(names)):
        t1 = threading.Thread(target = tweetvideo.googlevision, name = 't1{}'.format(i), args = (names[i],numbers[i],filepath1[i],filepath2[i]))
        t1.start()
        thread_list.append(t1)
        
    for t in thread_list:
        t.join()
        tweetvideo.Image2Video(names[x],filepath1[x])
        x += 1
    """
    for i in range(len(names)):
        t1 = threading.Thread(target = queue_func, name = 't1{}'.format(i), args = (names[i],numbers[i],filepath1[i],filepath2[i]))
        t1.start()

if __name__ == "__main__":
    names = ['@OnePlus_USA','@realDonaldTrump','@LeagueOfLegends']
    filepath1 = ['C:/Users/Vanquish/Desktop/pyve/VisionApi/downloadimage1/',
        'C:/Users/Vanquish/Desktop/pyve/VisionApi/downloadimage2/',
        'C:/Users/Vanquish/Desktop/pyve/VisionApi/downloadimage3/']
    filepath2 = [r'C:\Users\Vanquish\Desktop\pyve\VisionApi\downloadimage1',
        r'C:\Users\Vanquish\Desktop\pyve\VisionApi\downloadimage2',
        r'C:\Users\Vanquish\Desktop\pyve\VisionApi\downloadimage3']
    numbers = [30,40,10]
    pipelining(names, numbers, filepath1, filepath2)

