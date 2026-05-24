from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Functions.cacheManagement import getCachedData, setCache

# Setup Selenium to use Chrome
def vkprimeResolve(vkprimeUrl):
    if vkprimeUrl.endswith('.mp4'):
        return vkprimeUrl
    if '/' not in vkprimeUrl:
        vkprimeUrl = f'https://vkprime.com/embed-{vkprimeUrl}.html'
    cachedUrl = getCachedData(key=vkprimeUrl)
    if cachedUrl:
        print("giving cached data")
        return cachedUrl
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode to avoid opening a window
    ### Added extra to run in server
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Required for some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcomes resource limitations
    options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/chrome"
    # service = Service("/opt/render/project/.render/chromedriver/chromedriver")
    driver = webdriver.Chrome(options=options)
    ### Extra ends here

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the URL
    driver.get(vkprimeUrl)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "script"))
    )

    # Get page content after it fully loads
    content = driver.page_source

    # Clean up
    driver.quit()
    html = BeautifulSoup(content, 'html.parser')
    listScript = html.select('script')[-2].text.split("|")
    if '720p' in listScript:
        indexUrl = listScript.index("720p") + 1
    else :
        indexUrl = listScript.index("360p") + 1
    indexvkcdn = listScript.index("vkcdn5") + 1
    finalUrl = f'https://{listScript[indexvkcdn]}.vkcdn5.com/{listScript[indexUrl]}/v.mp4'
    setCache(key=vkprimeUrl, value=finalUrl, hourTimeout=3)
    print("data is cached")
    # print("list is", listScript)
    # print("this is inside vkprime", finalUrl)
    return finalUrl

# url = 'https://vkprime.com/embed-03eedw2ydzdp.html'
# finalUrl = vkprimeResolve(url)
# print(finalUrl)



# eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('a.49={"1n":{"1m":{}}};1e 8=a("48").47({46:[{14:"4://16.15.7/45/v.1s",1r:"44"},{14:"4://16.15.7/43/v.1s",1r:"42"}],41:"4://16.15.7/i/40/3z/18.3y",3x:\'./s/\',"3w":{"14":"","3v":"","1a":"l","b":"3u-3t"},3s:"1q%",3r:"1q%",3q:"3p",3o:"3n.3m",3l:{3k:{"3j":"#1p","3i":"#3h"},3g:{"3f":"#1p","3e":"3d(13,13,13,0.3)"}},3c:{3b:\'9\',3a:{e:{g:"e",f:[\'4://12.7/11-z-y-w-u/e-t/\',\'4://9.d.c/9?39=38\',\'4://9.d.c/?n=m\',\'\',\'\']},37:{g:"36",f:[\'\',\'\']},35:{g:"34",f:[\'\',\'4://9.d.c/?n=m\']},33:{g:"32",f:[\'4://9.d.c/?n=m\',\'\',\'4://12.7/11-z-y-w-u/e-t/\']},1o:{g:"1o",f:[\'\',\'\',\'4://12.7/11-z-y-w-u/e-t/\',\'4://9.d.c/?n=m\']}}},31:{},30:\'2z\',2y:"l",2x:"l",2w:"2v",2u:"l",2t:[0.25,0.5,1,1.5,2.0],2s:"2r",1n:{"1m":{}},2q:[],2p:"0",2o:"4://19.7"});8.1l("./s/1k/2n.1j","2m 1i",6(){8.1h(8.1g()+10)},"2l");8.1l("./s/1k/1f.1j","2k 1i",6(){8.1h(8.1g()-10)},"1f");1e o,r,q=0;a().h(\'2j\',6(x){k(5>0&&x.b>=5&&r!=1){r=1;$(\'p.2i\').2h(\'2g\')}k(q==0&&x.b>=1d&&x.b<=(1d+2)){q=x.b}});a().h(\'2f\',6(x){1c(x)});a().h(\'2e\',6(){$(\'p.1b\').2d()});6 1c(x){$(\'p.1b\').1a();k(o)2c;o=1;j=0;k(2b.2a===29){j=1}$.28(\'4://19.7/27?26=24&23=18&22=21-20-1z-1y-1x&1w=1&j=\'+j,6(17){$(\'#1v\').1u(17)})}a().h(\'1t\',6(){});',36,154,'||||https||function|com|player8|vast|jwplayer|position|xyz|yomeno|pre|tag|offset|on||adb|if|true|11624|tcid|vvplay|div|x2ok|vvad|player8177|roll|1c35782c6341||9e82||4fb3|dcaf||fe3f21e4|0af2a962b0102942d9a7df351b20be55|255|file|vkcdn5|ovhprime0|data|1ovclo1r6vfh|vkprime|hide|video_ad|doPlay|825|var|backward|getPosition|seek|10s|svg|skins|addButton|ping|plugins|post|3298da|100|label|mp4|ready|html|fviews|embed|b1a5d0b913b7fb220d224df6eca4d07d|1732267903|78|202|884893|hash|file_code|view||op|dl|get|undefined|cRAds|window|return|show|complete|play|slow|fadeIn|video_ad_fadein|time|Backward|forward|Forward|forward1|aboutlink|abouttext|tracks|start|startparam|playbackRates|playbackRateControls|html5|primary|hlshtml|androidhls|metadata|preload|cast|900|thirdmid|600|secmid|300|firstmid|7680|spot_id|schedule|client|advertising|rgba|rail|progress|timeslider|29b765|iconsActive|icons|controlbar|skin|50|1835|duration|uniform|stretching|height|width|bar|control|link|logo|base|jpg|00176|01|image|192p|k44si3elu3zgds2ywogcv3z3tiu77vocx4gmsbvy64d6wjbq7px5hvg3qkeq|360p|k44si3elu3zgds2ywogcv3z3tiu77vocx4gmsbvy6uvoujbq7px6cheohaja|sources|setup|vplayer|defaults'.split('|')))






