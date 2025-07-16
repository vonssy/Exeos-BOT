from curl_cffi import requests
from datetime import datetime
from colorama import *
import asyncio, random, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.65 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.133 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (X11; Arch Linux; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36 Edg/113.0.1774.35",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36 Edg/112.0.1722.64",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.64 Safari/537.36 Edg/111.0.1661.54",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36 Edg/112.0.1722.68",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36 OPR/99.0.4788.77",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36 OPR/98.0.4759.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36 Brave/1.52.129",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36 Brave/1.51.110",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36 Vivaldi/6.1.3035.100",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36 Vivaldi/6.0.2979.22",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/114.0.5735.91 Safari/537.36"
]

class Exeos:
    def __init__(self) -> None:
        self.BASE_API = "https://api.exeos.network/extension"
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.ip_address = {}

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
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}Exeos - BOT
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
        filename = "nodes.json"
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
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = await asyncio.to_thread(requests.get, "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
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

    def mask_account(self, account):
        if '@' in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
    
    def print_message(self, account, node_id, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{self.mask_account(account)}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Node Id:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {node_id} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
        
    async def check_connection(self, email: str, node_id: str, proxy=None):
        url = "https://api.ipify.org?format=json"
        proxies = {"http":proxy, "https":proxy} if proxy else None
        await asyncio.sleep(3)
        try:
            response = await asyncio.to_thread(requests.get, url=url, proxies=proxies, timeout=30, impersonate="chrome110", verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.print_message(email, node_id, proxy, Fore.RED, f"Connection Not 200 OK: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")  
            return None
    
    async def node_stats(self, email: str, node_id: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/stats"
        data = json.dumps({"extensionId":node_id})
        headers = self.HEADERS[f'{email}_{node_id}'].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            proxies = {"http":proxy, "https":proxy} if proxy else None
            await asyncio.sleep(5)
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=60, impersonate="chrome110", verify=False)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    continue
                self.print_message(email, node_id, proxy, Fore.RED, f"Update Stats Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
                return None
    
    async def node_connect(self, email: str, node_id: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/connect"
        data = json.dumps({"extensionId":node_id, "ip":self.ip_address[node_id]})
        headers = self.HEADERS[f'{email}_{node_id}'].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            proxies = {"http":proxy, "https":proxy} if proxy else None
            await asyncio.sleep(5)
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=60, impersonate="chrome110", verify=False)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    continue
                self.print_message(email, node_id, proxy, Fore.RED, f"Node Not Connected: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
                return None
    
    async def node_liveness(self, email: str, node_id: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/liveness"
        data = json.dumps({"extensionId":node_id})
        headers = self.HEADERS[f'{email}_{node_id}'].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            proxies = {"http":proxy, "https":proxy} if proxy else None
            await asyncio.sleep(5)
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxies=proxies, timeout=60, impersonate="chrome110", verify=False)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    continue
                self.print_message(email, node_id, proxy, Fore.RED, f"Maintain Liveness Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
                return None
        
    async def process_check_connection(self, email: str, node_id: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(node_id) if use_proxy else None

            is_valid = await self.check_connection(email, node_id, proxy)
            if is_valid:
                self.ip_address[node_id] = is_valid["ip"]
                return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(node_id)
        
    async def process_node_stats(self, email: str, node_id: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            is_valid = await self.process_check_connection(email, node_id, use_proxy, rotate_proxy)
            if is_valid:
                proxy = self.get_next_proxy_for_account(node_id) if use_proxy else None

                update = await self.node_stats(email, node_id, proxy)
                if update:
                    self.print_message(email, node_id, proxy, Fore.GREEN, "Stats Updated Successfully")
                    return True
        
    async def process_node_connect(self, email: str, node_id: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            update = await self.process_node_stats(email, node_id, use_proxy, rotate_proxy)
            if update:
                proxy = self.get_next_proxy_for_account(node_id) if use_proxy else None

                connect = await self.node_connect(email, node_id, proxy)
                if connect and connect.get("status") == "success":
                    uptime_total = connect.get("data", {}).get("uptimeTotal")

                    self.print_message(email, node_id, proxy, Fore.GREEN, "Node Is Connected "
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{uptime_total}{Style.RESET_ALL}"
                    )
                    return True
        
    async def process_node_liveness(self, email: str, node_id: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For a Hours For Maintaining Liveness...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            await asyncio.sleep(1 * 60 * 60)

            proxy = self.get_next_proxy_for_account(node_id) if use_proxy else None

            liveness = await self.node_liveness(email, node_id, proxy)
            if liveness and liveness.get("status") == "success":
                earn_today = liveness.get("updatedData", {}).get("nodeExtension", {}).get("todayRewards", 0)
                earn_total = liveness.get("updatedData", {}).get("nodeExtension", {}).get("totalRewards", 0)
                uptime_total = liveness.get("updatedData", {}).get("nodeExtension", {}).get("uptimeTotal", 0)

                self.print_message(email, node_id, proxy, Fore.GREEN, "Maintain Liveness Success"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Earning:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Today {earn_today} PTS{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Total {earn_total} PTS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{uptime_total}{Style.RESET_ALL}"
                )

            elif liveness and liveness.get("status") == "fail":
                await self.process_node_connect(email, node_id, use_proxy, rotate_proxy)
                continue
        
    async def process_accounts(self, email: str, nodes: list, use_proxy: bool, rotate_proxy: bool):
        tasks = []

        async def process_node_session(node):
            node_id = node.get("nodeId")

            if node_id:
                self.HEADERS[f'{email}_{node_id}'] = {
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Origin": "chrome-extension://ijapofapbjjfegefdmhhgijgkillnogl",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-Storage-Access": "active",
                    "User-Agent": random.choice(USER_AGENT)
                }

                connected = await self.process_node_connect(email, node_id, use_proxy, rotate_proxy)
                if connected:
                    tasks.append(asyncio.create_task(self.process_node_liveness(email, node_id, use_proxy, rotate_proxy)))

        await asyncio.gather(*[process_node_session(node) for node in nodes if node])

        await asyncio.gather(*tasks)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED+Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
                return

            proxy_choice, rotate_proxy = self.print_question()

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

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*75)

            tasks = []
            for idx, account in enumerate(accounts, start=1):
                if account:
                    email = account["Email"]
                    token = account["Token"]
                    nodes = account["Nodes"]

                    if not "@" in email or not token:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{self.mask_account(email)}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid Nodes Data {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    if not nodes or isinstance(nodes, list) and len(nodes) == 0:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{self.mask_account(email)}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} No Nodes Loaded {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    self.access_tokens[email] = token

                    tasks.append(asyncio.create_task(self.process_accounts(email, nodes, proxy_choice, rotate_proxy)))
                    
            await asyncio.gather(*tasks)

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