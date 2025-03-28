from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, uuid, os, pytz


wib = pytz.timezone('Asia/Jakarta')

class Exeos:
    def __init__(self) -> None:
        ua = FakeUserAgent().random
        self.dashboard_headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://app.exeos.network",
            "Referer": "https://app.exeos.network/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": ua
        }
        self.extension_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://ijapofapbjjfegefdmhhgijgkillnogl",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": ua
        }
        self.code = "REFZ26PQGAF"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.proxy_nodes = {}

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
    
    def print_message(self, account, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
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
                print("1. Use Exiting Nodes")
                print("2. Create New Nodes")
                connection_choice = int(input("Choose [1/2] -> ").strip())
                if connection_choice in [1, 2]:
                    break
                else:
                    print(f"{Fore.RED+Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        while True:
            try:
                print("1. Run With Monosans Proxy")
                print("2. Run With Private Proxy")
                print("3. Run Without Proxy")
                proxy_choice = int(input("Choose [1/2/3] -> ").strip())

                if proxy_choice in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if proxy_choice == 1 else 
                        "Run With Private Proxy" if proxy_choice == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        nodes_count = 0
        if proxy_choice in [1, 2]:
            while True:
                try:
                    nodes_count = int(input("How Many Nodes Do You Want to Run For Each Account? -> ").strip())
                    if nodes_count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        return nodes_count, proxy_choice, connection_choice
        
    async def get_ip_address(self, email: str, node_id: str, proxy=None, retries=5):
        url = "https://api.ipify.org/?format=json"
        headers = {
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="safari15_5")
                response.raise_for_status()
                result = response.json()
                return result['ip']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.WHITE, 
                    f"Node ID: {node_id} "
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} GET IP Address Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
    
    async def email_login(self, email: str, password: str, proxy=None, retries=5):
        url = "https://api.exeos.network/auth/web/email/login"
        data = json.dumps({"email":email, "password":password, "referralCode":self.code})
        headers = {
            **self.dashboard_headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                response.raise_for_status()
                result = response.json()
                return result['data']['token']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"Login Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            
    async def user_data(self, email: str, proxy=None, retries=5):
        url = "https://api.exeos.network/account/web/me"
        headers = {
            **self.dashboard_headers,
            "Authorization": f"Bearer {self.access_tokens[email]}",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="safari15_5")
                response.raise_for_status()
                result = response.json()
                return result['data']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"GET User Data Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            
    async def ext_stats(self, email: str, password: str, node_id: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://api.exeos.network/extension/stats"
        data = json.dumps({"extensionId":node_id})
        headers = {
            **self.extension_headers,
            "Authorization": f"Bearer {self.access_tokens[email]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    await self.process_get_access_token(email, password, use_proxy)
                    headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                    continue
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.WHITE, 
                    f"Node ID: {node_id} "
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Perform Stats Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
    
    async def ext_connect(self, email: str, password: str, node_id: str, ip_address: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://api.exeos.network/extension/connect"
        data = json.dumps({"extensionId":node_id, "ip":ip_address})
        headers = {
            **self.extension_headers,
            "Authorization": f"Bearer {self.access_tokens[email]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    await self.process_get_access_token(email, password, use_proxy)
                    headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                    continue
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.WHITE, 
                    f"Node ID: {node_id} "
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Connect Node Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
    
    async def ext_liveness(self, email: str, password: str, node_id: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://api.exeos.network/extension/liveness"
        data = json.dumps({"extensionId":node_id})
        headers = {
            **self.extension_headers,
            "Authorization": f"Bearer {self.access_tokens[email]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    await self.process_get_access_token(email, password, use_proxy)
                    headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                    continue
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.WHITE, 
                    f"Node ID: {node_id} "
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Perform Liveness Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
            
    async def process_get_access_token(self, email: str, password: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(email) if use_proxy else None
        token = None
        while token is None:
            token = await self.email_login(email, password, proxy)
            if not token:
                proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                await asyncio.sleep(5)
                continue
            
            self.access_tokens[email] = token
            self.print_message(email, proxy, Fore.GREEN, "Login Success")
            return self.access_tokens[email]
        
    async def process_get_ip_address(self, email: str, node_id: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(f"{email}_{node_id}") if use_proxy else None
        ip_address = None
        while ip_address is None:
            ip_address = await self.get_ip_address(email, node_id, proxy)
            if not ip_address:
                proxy = self.get_next_proxy_for_account(f"{email}_{node_id}") if use_proxy else None
                await asyncio.sleep(5)
                continue
            
            self.print_message(email, proxy, Fore.WHITE, 
                f"Node ID: {node_id}"
                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT}GET IP Address Success{Style.RESET_ALL}"
            )
            return ip_address
        
    async def process_get_stats(self, email: str, password: str, node_id: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(f"{email}_{node_id}") if use_proxy else None
        stats = None
        while stats is None:
            stats = await self.ext_stats(email, password, node_id, use_proxy, proxy)
            if stats and stats.get("status") == "success":
                ip_address = stats.get("data", {}).get("nodeExtension", {}).get("ip", None)
                if ip_address is None:
                    ip_address = await self.process_get_ip_address(email, node_id, use_proxy)
                self.print_message(email, proxy, Fore.WHITE, 
                    f"Node ID: {node_id}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}Perform Stats Success{Style.RESET_ALL}"
                )
                return ip_address
            else:
                continue

    async def process_connect_node(self, email: str, password: str, node_id: str, use_proxy: bool):
        ip_address = await self.process_get_stats(email, password, node_id, use_proxy)
        if ip_address:
            proxy = self.get_next_proxy_for_account(f"{email}_{node_id}") if use_proxy else None
            connect = None
            while connect is None:
                connect = await self.ext_connect(email, password, node_id, ip_address, use_proxy, proxy)
                if connect and connect.get("status") == "success":
                    uptime_total = connect.get("data", {}).get("uptimeTotal")
                    self.print_message(email, proxy, Fore.WHITE, 
                        f"Node ID: {node_id} "
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Node Connected {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{uptime_total}{Style.RESET_ALL}"
                    )
                    return True
                else:
                    continue

    async def process_send_liveness(self, email: str, password: str, node_id: str, use_proxy: bool):
        connected = await self.process_connect_node(email, password, node_id, use_proxy)
        if connected:
            while True:
                await asyncio.sleep(10 * 60)
                proxy = self.get_next_proxy_for_account(f"{email}_{node_id}") if use_proxy else None
                liveness = await self.ext_liveness(email, password, node_id, use_proxy, proxy)
                if liveness and liveness.get("status") == "success":
                    earning_today = liveness.get("updatedData", {}).get("nodeExtension", {}).get("todayRewards", 0)
                    earning_total = liveness.get("updatedData", {}).get("nodeExtension", {}).get("totalRewards", 0)
                    uptime_total = liveness.get("updatedData", {}).get("nodeExtension", {}).get("uptimeTotal", 0)
                    self.print_message(email, proxy, Fore.WHITE, 
                        f"Node ID: {node_id}"
                        f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}Perform Liveness Success{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}Earning:{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Today {earning_today} PTS{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Total {earning_total} PTS {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT} Uptime Total: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{uptime_total}{Style.RESET_ALL}"
                    )
                elif liveness and liveness.get("status") == "fail":
                    self.print_message(email, proxy, Fore.WHITE, 
                        f"Node ID: {node_id} "
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Perform Liveness Failed: {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Too Early For Next Liveness{Style.RESET_ALL}"
                    )
                    connected = await self.process_connect_node(email, password, node_id, use_proxy)

    async def process_user_nodes(self, email: str, nodes_count: int, use_proxy: bool, connection_choice: int):
        proxy = self.get_next_proxy_for_account(email) if use_proxy else None
        nodes = []
        if connection_choice == 1:
            user = None
            while user is None:
                user = await self.user_data(email, proxy)
                if not user:
                    proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                    await asyncio.sleep(5)
                    continue

                exciting_nodess = user.get("networkNodes", [])
                if use_proxy:
                    if isinstance(exciting_nodess, list) and len(exciting_nodess) == 0:
                        for _ in range(nodes_count):
                            node_id = self.generate_node_id()
                            nodes.append({"nodeId":node_id})
                        return nodes
                
                    for node_ids in exciting_nodess[:nodes_count]:
                        if node_ids:
                            node_id = node_ids.get("nodeId")
                            nodes.append({"nodeId":node_id})
                    return nodes
                
                for node_ids in exciting_nodess[:1]:
                    if node_ids:
                        node_id = node_ids.get("name")
                        nodes.append({"nodeId":node_id})

                return nodes
                
        if use_proxy:
            for _ in range(nodes_count):
                node_id = self.generate_node_id()
                nodes.append({"nodeId":node_id})

            return nodes
        
        node_id = self.generate_node_id()
        nodes.append({"nodeId":node_id})

        return nodes
        
    async def process_accounts(self, email: str, password: str, nodes_count: int, use_proxy: bool, connection_choice: int):
        self.access_tokens[email] = await self.process_get_access_token(email, password, use_proxy)
        if self.access_tokens[email]:
            nodes = await self.process_user_nodes(email, nodes_count, use_proxy, connection_choice)
            if nodes:
                tasks = []
                for node in nodes:
                    if node:
                        node_id = node.get("nodeId")
                        tasks.append(asyncio.create_task(self.process_send_liveness(email, password, node_id, use_proxy)))
                
                await asyncio.gather(*tasks)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED+Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
                return

            nodes_count, proxy_choice, connection_choice = self.print_question()

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

            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            while True:
                tasks = []
                for account in accounts:
                    if account:
                        email = account['Email']
                        password = account['Password']

                        if "@" in email and password:
                            tasks.append(asyncio.create_task(self.process_accounts(email, password, nodes_count, proxy_choice, connection_choice)))
                        
                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
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