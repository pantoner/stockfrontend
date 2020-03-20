import rolling 
import time

def convertime(opentimenp):
    opentimestr = str(opentimenp)
    thistime1 = int(opentimestr[:10])
    thisdate1 = time.strftime("%d %B, %Y", time.localtime(thistime1))
    return thisdate1

def getcloud(closelist,highlist,lowlist,datelist,symbol):
    todaysdate = datelist[0]
    todaysdate = convertime(todaysdate)
    h_max9 = rolling.Max(highlist, 9)
    high9 = list(h_max9)
    h_max9 = rolling.Max(highlist, 9)
    l_min9 = rolling.Min(lowlist, 9)
    high9 = list(h_max9)
    low9 = list(l_min9)
    high9+low9
    tenkan_sen = [(x + y)/2 for x, y in zip(high9,low9)]
    h_max26 = rolling.Max(highlist, 26)
    l_min26 = rolling.Min(lowlist, 26)
    high26 = list(h_max26)
    low26 = list(l_min26)
    high26+low26
    kijun_sen = [(x + y)/2 for x, y in zip(high26,low26)]
    sa = [(x + y)/2 for x, y in zip(kijun_sen,tenkan_sen)]
    clouda = (sa[26] - closelist[0])/closelist[0]
    kijun_sen2 = (kijun_sen[0] - closelist[0])/closelist[0]
    tenkan_sen2 = (tenkan_sen[0] - closelist[0])/closelist[0]
    h_max52 = rolling.Max(highlist, 52)
    l_min52 = rolling.Min(lowlist, 52)
    high52 = list(h_max52)
    low52 = list(l_min52)
    sb = [(x + y)/2 for x, y in zip(high52,low52)]
    cloudb = (sb[26] - closelist[0])/closelist[0]
    outcomedict = {'todaysdate':todaysdate, 'symbol':symbol,'sacloud':clouda,'sbcloud':cloudb,'kijun_sen':kijun_sen2,\
    'tenkan_sen2':tenkan_sen2}
    print(outcomedict)


def getcloud2(closelist,highlist,lowlist):
    h_max9 = rolling.Max(highlist, 9)
    high9 = list(h_max9)
    h_max9 = rolling.Max(highlist, 9)
    l_min9 = rolling.Min(lowlist, 9)
    high9 = list(h_max9)
    low9 = list(l_min9)
    high9+low9
    tenkan_sen = [(x + y)/2 for x, y in zip(high9,low9)]
    h_max26 = rolling.Max(highlist, 26)
    l_min26 = rolling.Min(lowlist, 26)
    high26 = list(h_max26)
    low26 = list(l_min26)
    high26+low26
    kijun_sen = [(x + y)/2 for x, y in zip(high26,low26)]
    sa = [(x + y)/2 for x, y in zip(kijun_sen,tenkan_sen)]
    clouda = (sa[26] - closelist[0])/closelist[0]
    kijun_sen2 = (kijun_sen[0] - closelist[0])/closelist[0]
    tenkan_sen2 = (tenkan_sen[0] - closelist[0])/closelist[0]
    h_max52 = rolling.Max(highlist, 52)
    l_min52 = rolling.Min(lowlist, 52)
    high52 = list(h_max52)
    low52 = list(l_min52)
    sb = [(x + y)/2 for x, y in zip(high52,low52)]
    cloudb = (sb[26] - closelist[0])/closelist[0]
    outcomedict = {'sacloud':clouda,'sbcloud':cloudb,'kijun_sen':kijun_sen2,\
    'tenkan_sen2':tenkan_sen2}
    print(outcomedict)


