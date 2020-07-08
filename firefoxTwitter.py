import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from twitterUserInfo import username, password #This section contain users info in another file



class Twitter():
    def __init__(self, username, password):

        
        self.browser = webdriver.Firefox()
        self.username = username
        self.password = password


    def signIn(self):
        self.browser.get("https://twitter.com/login")
        time.sleep(2)

        usernameInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]/div/input")
        passwordInput = self.browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[2]/label/div/div[2]/div/input')

        usernameInput.send_keys(self.username)
        
        passwordInput.send_keys(self.password)

        time.sleep(2)

        submitButton = self.browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[3]/div')
        submitButton.click()

        time.sleep(3)

    def search(self, hashtag): #Search a certain hashtag and take the tweets with another file that name "tweets.txt"
        searchInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input")
        searchInput.send_keys(hashtag)
        time.sleep(2)
        searchInput.send_keys(Keys.ENTER)
        time.sleep(2)

        results = []

        list = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]")
        time.sleep(2)
        print("count: "+ str(len(list)))

        for i in list:
            results.append(i.text)

        loopCounter = 0
        last_height = self.browser.execute_script("return document.documentElement.scrollHeight")
        while True:
            if loopCounter > 5: #Scroll down the page 5 times
                break
            self.browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = self.browser.execute_script("return document.documentElement.scrollHeight")
            if last_height == new_height:
                break
            last_height = new_height
            loopCounter+=1

            list = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]")
            time.sleep(2)
            print("count: "+ str(len(list)))

            for i in list:
                results.append(i.text)
        
        count = 1
        with open("tweets.txt","w",encoding="UTF-8") as file:
            for item in results:
                file.write(f"{count}-{item}\n")
                count+=1


twitter = Twitter(username, password)

twitter.signIn()
twitter.search("fenerbahçe") #Hashtag