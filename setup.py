from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, uuid, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Exeos:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://app.exeos.network",
            "Referer": "https://app.exeos.network/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://api.exeos.network"
        self.ref_code = "REFZ26PQGAF" # U can change it with yours
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.user_nodes = []
        self.node_datas = []

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Setup {Fore.BLUE + Style.BRIGHT}Exeos - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []

    def save_nodes(self, new_nodes):
        filename = "nodes.json"
        try:
            if not os.path.exists(filename):
                with open(filename, 'w') as file:
                    json.dump([], file, indent=4)

            if os.path.getsize(filename) == 0:
                existing_nodes = []
            else:
                with open(filename, 'r') as file:
                    existing_nodes = json.load(file)

            for new_node in new_nodes:
                email = new_node["Email"]
                token = new_node["Token"]
                new_node_list = new_node.get("Nodes", [])

                found = False
                for existing_node in existing_nodes:
                    if existing_node["Email"] == email:
                        found = True

                        existing_node["Token"] = token

                        if not existing_node.get("Nodes"):
                            existing_node["Nodes"] = new_node_list
                        else:
                            existing_node_ids = {node["nodeId"] for node in existing_node["Nodes"]}
                            for node in new_node_list:
                                if node["nodeId"] not in existing_node_ids:
                                    existing_node["Nodes"].append(node)
                        break

                if not found:
                    existing_nodes.append(new_node)

            with open(filename, 'w') as file:
                json.dump(existing_nodes, file, indent=4)

        except Exception as e:
            self.log(f"Save Nodes Failed: {str(e)}")
            return []
    
    async def load_proxies(self, proxy_choice: int):
        filename = "proxy.txt"
        try:
            if proxy_choice == 1:
                response = await asyncio.to_thread(requests.get, "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
        
    def generate_node_id(self):
        node_id = str(uuid.uuid4())
        return f"node:ext:{node_id}"

    def mask_account(self, account):
        if '@' in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"

    def print_question(self):
        count = 0
        rotate = False

        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Create New Nodes{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Use Exiting Nodes{Style.RESET_ALL}")
                option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if option in [1, 2]:
                    option_type = "Create New" if option == 1 else "Use Exiting"
                    print(f"{Fore.GREEN + Style.BRIGHT}{option_type} Nodes Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED+Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        if option == 1:
            while True:
                try:
                    count = int(input(f"{Fore.YELLOW + Style.BRIGHT}How Many Nodes Do You Want to Create For Each Account? -> {Style.RESET_ALL}").strip())
                    if count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Monosans Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return option, count, choose, rotate
    
    async def email_login(self, email: str, password: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/auth/web/email/login"
        data = json.dumps({"email":email, "password":password, "referralCode":self.ref_code})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def user_data(self, email: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/account/web/me"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[email]}"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="chrome110")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def process_user_login(self, email: str, password: str, use_proxy: bool, rotate_proxy: bool):
        proxy = self.get_next_proxy_for_account(email) if use_proxy else None

        if rotate_proxy:
            while True:
                login = await self.email_login(email, password, proxy)
                if login and login.get("status") == "success":
                    self.access_tokens[email] = login["data"]["token"]

                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Status :{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
                    )
                    return True
                
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Status :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Rotating Proxy {Style.RESET_ALL}"
                )

                proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                await asyncio.sleep(5)
                continue
                
        login = await self.email_login(email, password, proxy)
        if login and login.get("status") == "success":
            self.access_tokens[email] = login["data"]["token"]

            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Status :{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
            )
            return True
        
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Proxy  :{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Status :{Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT} Login Failed {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT} Skipping This Account {Style.RESET_ALL}"
        )
        return False
            
    async def process_get_exiting_nodes(self, email: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            
        user = await self.user_data(email, proxy)
        if user and user.get("status") == "success":
            exciting_nodes = user["data"]["networkNodes"]

            if isinstance(exciting_nodes, list) and len(exciting_nodes) == 0:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Nodes  :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} No Node Ids Found {Style.RESET_ALL}"
                )
                return self.node_datas

            for node in exciting_nodes:
                node_id = node["nodeId"]
                self.node_datas.append({"nodeId":node_id})

            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Nodes  :{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} You Have {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(exciting_nodes)} Node Ids{Style.RESET_ALL}"
            )
            return self.node_datas

        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Nodes  :{Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT} GET Exiting Node Ids Failed {Style.RESET_ALL}"
        )
        return self.node_datas
                
    async def process_create_new_nodes(self, nodes_count: int):
        for i in range(nodes_count):
            node_id = self.generate_node_id()
            self.node_datas.append({"nodeId":node_id})

        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Nodes  :{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {nodes_count} Node Ids {Style.RESET_ALL}"
            f"{Fore.GREEN + Style.BRIGHT}Have Been Created Successfully{Style.RESET_ALL}"
        )
        return self.node_datas

    async def process_accounts(self, email, password, option, nodes_count, use_proxy, rotate_proxy):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(email)} {Style.RESET_ALL}"
        )

        logined = await self.process_user_login(email, password, use_proxy, rotate_proxy)
        if logined:

            if option == 1:
                node_datas = await self.process_create_new_nodes(nodes_count)
                self.user_nodes.append({"Email":email, "Token":self.access_tokens[email], "Nodes":node_datas})
                self.save_nodes(self.user_nodes)

            elif option == 2:
                node_datas = await self.process_get_exiting_nodes(email, use_proxy)
                self.user_nodes.append({"Email":email, "Token":self.access_tokens[email], "Nodes":node_datas})
                self.save_nodes(self.user_nodes)

            self.log(f"{Fore.GREEN + Style.BRIGHT}Your Node Datas Have Been Saved Successfully{Style.RESET_ALL}")

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED+Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
                return

            option, nodes_count, proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if proxy_choice in [1, 2]:
                use_proxy = True

            
            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(proxy_choice)

            separator = "=" * 25
            for idx, account in enumerate(accounts, start=1):
                if account:
                    email = account["Email"]
                    password = account["Password"]

                    if not "@" in email or not password:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}Status :{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid Account, {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Skipped.{Style.RESET_ALL}"
                        )
                        continue

                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {idx} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}Of{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {len(accounts)} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                    )

                    await self.process_accounts(email, password, option, nodes_count, use_proxy, rotate_proxy)
                    await asyncio.sleep(3)

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*68)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Exeos()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Exeos - BOT{Style.RESET_ALL}                                       "                              
        )