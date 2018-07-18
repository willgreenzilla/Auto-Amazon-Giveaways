import asyncio
import getpass
import logging
import json
import re
import numpy
from pyppeteer import launch
from lib.prize import GiveAwayPrize
from colorama import init, Fore, Back, Style

with open('lib\creds.json') as data_file:
    data = json.load(data_file)

amazon_user = data['username']
amazon_pwd = data['password']
amazon_pages = data['give_page_count']

init(autoreset=True)
RANDOM_VAL = [7, 3, 2, 5, 10, 9, 6]
RANDOM_PAGE = list(range(0, amazon_pages))

class GiveAwayBot(object):
    def __init__(self):
        self.email = None
        self.password = None
        self.browser = None
        self.ga_prizes = {}

    async def _nav_to_ga(self, login_page):
        await login_page.goto('https://www.amazon.com/ga/giveaways?pageId=' + str(numpy.random.choice(RANDOM_PAGE)))
        return login_page

    async def login(self, init=True):
        email_input_box = '#ap_email'
        password_input_box = '#ap_password'
        #remember_me = '#rememberMe'
        sign_in_button = '#signInSubmit'

        async def get_browser():
            return await launch(headless=False)

        async def check_for_continue(login_page):
            continue_button = '#continue'
            is_continue_present = await login_page.querySelector(continue_button)
            if is_continue_present:
                await login_page.click(continue_button)
            else:
                pass
        
        login_msg = Fore.LIGHTYELLOW_EX + 'Log into Amazon...'
        print(login_msg)
        if init:
            email_msg = 'Enter your Amazon email address: '
            pass_msg = 'Enter your Amazon password: '
            self.email = amazon_user
            self.password = amazon_pwd

        self.browser = await get_browser()
        login_page = await self.browser.newPage()
        await login_page.setViewport({'width': 1900, 'height': 1000})
        await login_page.goto(
            'https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fgiveaway%2Fhome%2Fref%3Dnav_custrec_signin&switch_account='
            )
        await login_page.type(email_input_box, self.email)
        await check_for_continue(login_page)
        await login_page.waitForSelector(password_input_box, timeout=5000)
        await login_page.type(password_input_box, self.password)
        #await self.browser.click(remember_me)
        await login_page.click(sign_in_button)
        await asyncio.sleep(2)
        # this will navigate to root Giveaway page after successful login and return the page.
        ga_page = await self._nav_to_ga(login_page)
        await asyncio.sleep(2)
        return ga_page
        #await self.browser.close()

    async def get_page_giveaways(self, ga_page):
        giveaway_grid_selector = '#giveaway-grid'
        giveaway_grid = await ga_page.querySelector(giveaway_grid_selector)
        if giveaway_grid:
            page_giveaways = await giveaway_grid.xpath('*/*')
            return page_giveaways
        else:
            return None

    def display_ga_process(self, ga_name):
        ga_process = Fore.CYAN + Style.BRIGHT + 'Processing GiveAway:{0}  {1}'.format(Style.RESET_ALL, ga_name)
        print(ga_process)

    async def check_for_entered(self, prize_page):
        #await prize_page.waitForSelector('.qa-giveaway-result-text')
        ga_result_element = await prize_page.querySelector('.qa-giveaway-result-text')
        airy = await prize_page.querySelector('#airy-container')
        play_airy = await prize_page.querySelector('.airy-play-toggle-hint')        
        if ga_result_element:
            ga_result = await prize_page.evaluate(
                '(ga_result_element) => ga_result_element.textContent',
                ga_result_element
            )
            if "didn't win" in ga_result:
                msg = Fore.MAGENTA + Style.BRIGHT + "    **** Already entered giveaway and you didn't win. ****"
                print(msg)
            return True
        elif airy:
            msg = Fore.MAGENTA + Style.BRIGHT + "    **** Stupid Amazon Video, skipping. ****"
            print(msg)            
            return True                        
        else:
            return False
    
    async def display_ga_result(self, prize_page):
        await prize_page.waitForSelector('.qa-giveaway-result-text')
        ga_result_element = await prize_page.querySelector('.qa-giveaway-result-text')
        ga_result = await prize_page.evaluate(
            '(ga_result_element) => ga_result_element.textContent',
            ga_result_element
        )
        if "didn't win" in ga_result:
            msg = Fore.YELLOW + Style.BRIGHT + "  **** You entered the giveaway but did not win. ****"
            print(msg)
        elif "entry has been received" in ga_result:
            msg = Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "  **** You submitted an entry to this giveaway. ****"
            print(msg)
        else:
            msg = Fore.GREEN + Style.BRIGHT + "   **** Maybe you won?? ****"
            print(msg)

    async def no_req_giveaways(self):
        for prize in self.ga_prizes:
            if ' ' in self.ga_prizes[prize]['Requirement'] and self.ga_prizes[prize]['Entered'] is False and 'Follow' not in self.ga_prizes[prize]['Requirement']:
                self.display_ga_process(self.ga_prizes[prize]['Name'])
                prize_page = await self.browser.newPage()
                await prize_page.setViewport({'width': 1900, 'height': 1000})
                await prize_page.goto(self.ga_prizes[prize]['Url'])
                # testing a random sleep methodology to avoid bot detection / captcha.
                await asyncio.sleep(numpy.random.choice(RANDOM_VAL))
                ga_entry = await self.check_for_entered(prize_page)
                if ga_entry is False:
                    await asyncio.sleep(numpy.random.choice(RANDOM_VAL))
                    prize_box = await prize_page.querySelector('#box_click_target')
                    enter_button = await prize_page.querySelector('#enterSubmitForm')
                    enter_video = await prize_page.querySelector('#videoSubmitForm')
                    video_text = await prize_page.querySelector('#giveaway-youtube-video-watch-text')
                    book = await prize_page.querySelector('#submitForm')
                    if prize_box:
                        await asyncio.sleep(numpy.random.choice(RANDOM_VAL))
                        await prize_box.click()
                        msg = Fore.MAGENTA + Style.BRIGHT + "    **** I should have clicked the prize box?. ****"
                        print(msg)  
                    elif enter_button:
                        await enter_button.click()
                    elif book:
                        await book.click()                        
                    elif video_text:
                        msg = Fore.MAGENTA + Style.BRIGHT + "    **** Waiting 30 seconds. ****"
                        print(msg)
                        await asyncio.sleep(32)
                        msg2 = Fore.MAGENTA + Style.BRIGHT + "    **** 30 Seconds is over, Entering Contest. ****"
                        print(msg2)                        
                        await enter_video.click()                      
                    else:
                        await asyncio.sleep(1)
                        await prize_page.close()
                        msg = Fore.MAGENTA + Style.BRIGHT + "    **** Timed out :: Close page. ****"
                        print(msg)
                    await asyncio.sleep(numpy.random.choice(RANDOM_VAL))
                    await self.display_ga_result(prize_page)
                    await asyncio.sleep(1)
                    await prize_page.close()                        
                else:
                    msg = Fore.MAGENTA + Style.BRIGHT + "    **** Not sure what happen, Or there's nothing to do :: skipping. ****"
                    print(msg)
                    await asyncio.sleep(1)                     
                    await prize_page.close()
                    
    async def check_for_last_page(self, ga_page):
        last_page = await ga_page.xpath("//li[@class='a-disabled a-last']")
        if last_page:
            msg = Fore.LIGHTWHITE_EX + Style.BRIGHT + "**** The Last GiveAway Page has been reached.  Exiting... ****"
            print(msg)
            return True
        else:
            return False

    async def iterate_page(self, ga_page):
        next_page = await ga_page.xpath("//li[@class='a-last']")
        if next_page:
            next_page_href = await ga_page.evaluate(
                '(next_page) => next_page.firstChild.href',
                next_page[0]
            )
            msg = Fore.LIGHTGREEN_EX + Style.BRIGHT + "**** Moving to next giveaway page... ****"
            await ga_page.goto(next_page_href)
            return ga_page
        else:
            msg = Fore.LIGHTRED_EX + Style.BRIGHT + "**** Could not find Next Page for GiveAways, Exiting... ****"
            print(msg)
            quit(1)
            
    async def process_giveaways(self, ga_page):

        async def create_ga_prize(giveaway):

            def parse_prize_url(url):
                ga_url = re.search(r'(^.*)(?=\?)', url)
                return ga_url.group(0)

            prize_name_element = await giveaway.querySelector('.giveawayPrizeNameContainer')
            prize_name = await ga_page.evaluate(
                '(prize_name_element) => prize_name_element.textContent',
                prize_name_element
            )
            prize_req_element = await giveaway.querySelector('.giveawayParticipationInfoContainer')
            prize_req = await ga_page.evaluate(
                '(prize_req_element) => prize_req_element.textContent',
                prize_req_element
            )
            prize_href = await ga_page.evaluate(
                '(giveaway) => giveaway.href',
                giveaway
            )
            prize_url = parse_prize_url(prize_href)
            ga_prize = GiveAwayPrize()
            ga_prize.set_prize_name(prize_name)
            ga_prize.set_prize_req(prize_req)
            ga_prize.set_prize_url(prize_url)
            self.ga_prizes[len(self.ga_prizes)] = {
                'Name': ga_prize.get_prize_name(),
                'Requirement': ga_prize.get_prize_req(),
                'Url': ga_prize.get_prize_url(),
                'Entered': False
            }
        
        page_giveaways = await self.get_page_giveaways(ga_page)
        if page_giveaways:
            for giveaway in page_giveaways:
                await create_ga_prize(giveaway)
            await self.no_req_giveaways()
        else:
            print('*** no giveaways returned ***')
