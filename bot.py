from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Exeos:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://ijapofapbjjfegefdmhhgijgkillnogl",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://api.exeos.network/extension"
        self.ref_code = "REFZ26PQGAF" # U can change it with yours
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.ip_address = {}
        self.node_ids = {}

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
        
    async def check_connection(self, email: str, proxy=None):
        url = "https://api.ipify.org/?format=json"
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="chrome110")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self.print_message(email, self.node_ids[email], proxy, Fore.RED, f"Connection Not 200 OK: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
    
    async def node_stats(self, email: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/stats"
        data = json.dumps({"extensionId":self.node_ids[email]})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[email]}",
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
                return self.print_message(email, self.node_ids[email], proxy, Fore.RED, f"Update Stats Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
    
    async def node_connect(self, email: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/connect"
        data = json.dumps({"extensionId":self.node_ids[email], "ip":self.ip_address[email]})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[email]}",
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
                return self.print_message(email, self.node_ids[email], proxy, Fore.RED, f"Node Not Connected: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
    
    async def node_liveness(self, email: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/liveness"
        data = json.dumps({"extensionId":self.node_ids[email]})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[email]}",
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
                return self.print_message(email, self.node_ids[email], proxy, Fore.RED, f"Maintain Liveness Failed: {Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
        
    async def process_check_connection(self, email: str, use_proxy: bool, rotate_proxy: bool):
        proxy = self.get_next_proxy_for_account(self.node_ids[email]) if use_proxy else None
        
        if rotate_proxy:
            while True:
                is_valid = await self.check_connection(email, proxy)
                if is_valid and "ip" in is_valid:
                    self.ip_address[email] = is_valid["ip"]

                    self.print_message(email, self.node_ids[email], proxy, Fore.GREEN, "Connection 200 OK")
                    return True

                proxy = self.rotate_proxy_for_account(self.node_ids[email]) if use_proxy else None
                await asyncio.sleep(5)
                continue
                
        while True:
            is_valid = await self.check_connection(email, proxy)
            if is_valid and "ip" in is_valid:
                self.ip_address[email] = is_valid["ip"]

                self.print_message(email, self.node_ids[email], proxy, Fore.GREEN, "Connection 200 OK")
                return True

            await asyncio.sleep(5)
            continue
        
    async def process_node_stats(self, email: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(email, use_proxy, rotate_proxy)
        if is_valid:
            while True:
                proxy = self.get_next_proxy_for_account(self.node_ids[email]) if use_proxy else None

                update = await self.node_stats(email, proxy)
                if update:
                    self.print_message(email, self.node_ids[email], proxy, Fore.GREEN, "Stats Updated Successfully")
                    return True

                await asyncio.sleep(5)
                continue
        
    async def process_node_connect(self, email: str, use_proxy: bool, rotate_proxy: bool):
        update = await self.process_node_stats(email, use_proxy, rotate_proxy)
        if update:
            while True:
                proxy = self.get_next_proxy_for_account(self.node_ids[email]) if use_proxy else None

                connect = await self.node_connect(email, proxy)
                if connect and connect.get("status") == "success":
                    uptime_total = connect.get("data", {}).get("uptimeTotal")
                    self.print_message(email, self.node_ids[email], proxy, Fore.GREEN, "Node Is Connected "
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{uptime_total}{Style.RESET_ALL}"
                    )

                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT}Wait For a Hours For Miantaining Liveness...{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1 * 60 * 60)
                    return True

                await asyncio.sleep(5)
                continue
        
    async def process_node_liveness(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(self.node_ids[email]) if use_proxy else None

            liveness = await self.node_liveness(email, proxy)
            if liveness and liveness.get("status") == "success":
                earn_today = liveness.get("updatedData", {}).get("nodeExtension", {}).get("todayRewards", 0)
                earn_total = liveness.get("updatedData", {}).get("nodeExtension", {}).get("totalRewards", 0)
                uptime_total = liveness.get("updatedData", {}).get("nodeExtension", {}).get("uptimeTotal", 0)

                self.print_message(email, self.node_ids[email], proxy, Fore.GREEN, "Maintain Liveness Success"
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
                await self.process_node_connect(email, use_proxy, rotate_proxy)
                continue

            else:
                await asyncio.sleep(5)
                continue

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For a Hours For Miantaining Liveness...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            await asyncio.sleep(1 * 60 * 60)
        
    async def process_accounts(self, email: str, nodes: list, use_proxy: bool, rotate_proxy: bool):
        async def process_node_session(node):
            node_id = node.get("nodeId")
            if node_id:
                self.node_ids[email] = node_id

                connected = await self.process_node_connect(email, use_proxy, rotate_proxy)
                if connected:
                    asyncio.create_task(self.process_node_liveness(email, use_proxy, rotate_proxy))

        await asyncio.gather(*[process_node_session(node) for node in nodes if node])

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
            for account in accounts:
                if account:
                    email = account["Email"]
                    token = account["Token"]
                    nodes = account["Nodes"]

                    if not "@" in email or not token:
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