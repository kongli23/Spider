import requests

url = 'http://index.baidu.com/api/SearchApi/index?area=0&word=seo优化&days=90'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': 'BIDUPSID=5BEDEBA72FF8562CA64E0B1604B3A775; PSTM=1588231843; BAIDUID=5BEDEBA72FF8562C1C331455C8F712CF:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=145785_146722_147207_142019_148321_147090_147894_148867_148209_148714_148434_147279_148002_148824_147830_148439_148754_147889_146573_148523_147346_127969_146550_147024_147353_146732_138425_131423_147528_107319_147138_148949_140312_147990_144966_149280_145607_148071_148659_148345_144762_147546_145399_148868_147604_148104_110085; H_PS_PSSID=32095_1427_31671_21079_31254_32045_30823_31847; delPer=0; PSINO=6; BDUSS=9iYUYzMVVZekJ1MGF6dFJoVVlEdnltT0NOWUJwUFhOVVlJaURmYnpXcjVuQk5mSUFBQUFBJCQAAAAAAAAAAAEAAAAFNIyuZGlub3NzegAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPkP7F75D-xeTW; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1592532121; bdindexid=f3lvred3kqq8ehhlapi70drph6; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1592532129; RT="z=1&dm=baidu.com&si=fx1jw5iqin7&ss=kblki7iw&sl=6&tt=8bu&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=fja&ul=99zm"',
    'Referer': 'http://index.baidu.com/v2/main/index.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}
resp = requests.get(url,headers=headers)
text = resp.content.decode('utf-8')
print(text)