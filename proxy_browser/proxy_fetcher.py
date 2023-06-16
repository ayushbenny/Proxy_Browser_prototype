import subprocess
import socket
import threading
import tkinter as tk
from tkinter import ttk
import requests
import lxml.html as lh


class ProxyFetcher:
    """
    ProxyFetcher is a class responsible for fetching a list of available proxy servers from a website.

    Args:
        url (str): The URL of the website to fetch the proxy list from.

    Attributes:
        url (str): The URL of the website to fetch the proxy list from.

    Methods:
        fetch_proxies(): Fetches the list of available proxy servers from the specified website.

    Example:
        fetcher = ProxyFetcher()
    """

    def __init__(self, host=None, port=None, country=None, code=None) -> None:
        """
        Initialize the Proxy class.

        Args:
            host (str): The host of the proxy server.
            port (int): The port number of the proxy server.
            country (str): The country associated with the proxy server.
            code (str): The code associated with the proxy server.

        Returns:
            None
        """
        self.host = host
        self.port = port
        self.country = country
        self.code = code
        self._proxy_url()
        self._proxy_fetcher()
        self._proxy_status_checker()
        self.proxy_gui()

    def _proxy_url(self):
        """
        Retrieve a list of available proxy URLs.

        Returns:
            response: The response object containing the retrieved data.
        """
        url = "https://free-proxy-list.net"
        response = requests.get(url)
        return response

    def _proxy_fetcher(self):
        """
        Fetches the ports, IP addresses, countries, and other details from the websites.

        Returns:
            proxy_list (list): A list of dictionaries containing proxy details.
                Each dictionary has the following keys: 'ip', 'port', 'code', 'country'.
        """
        url_response = self._proxy_url()
        html_content = url_response._content
        doc = lh.fromstring(html_content)
        tr_elements = doc.xpath('//*[@id="list"]//tr')
        proxy_dict = {}
        proxy_list = []
        for length in range(1, len(tr_elements)):
            ip = tr_elements[length][0].text_content()
            port = tr_elements[length][1].text_content()
            code = tr_elements[length][2].text_content()
            country = tr_elements[length][3].text_content()
            proxy_dict = {"ip": ip, "port": port, "code": code, "country": country}
            proxy_list.append(proxy_dict)
        return proxy_list

    def _proxy_status_checker(self):
        """
        Check the status of the proxies to determine if they are active.

        Returns:
            active_proxy_list (list): A list of dictionaries containing active proxy details.
                Each dictionary has the following keys: 'ip', 'port', 'code', 'country'.
        """
        proxy_list = self._proxy_fetcher()
        active_proxy_list = []
        lock = threading.Lock()

        def check_proxy(proxy):
            """
            Check the status of a single proxy.

            Args:
                proxy (dict): A dictionary containing proxy details.
                    It should have the keys 'ip', 'port', 'code', and 'country'.

            Returns:
                None
            """
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                proxy_address = (proxy.get("ip"), int(proxy.get("port")))
                sock.connect(proxy_address)
                if sock:
                    active_proxy = dict(
                        ip=proxy.get("ip"),
                        port=proxy.get("port"),
                        country=proxy.get("country"),
                        code=proxy.get("code"),
                    )
                    with lock:
                        active_proxy_list.append(active_proxy)
            except ConnectionRefusedError:
                print(
                    f"HOST > {proxy.get('ip')} and the corresponding PORT > {proxy.get('port')} is not active"
                )
            except TimeoutError:
                print(
                    f"HOST > {proxy.get('ip')} and the corresponding PORT > {proxy.get('port')} connection timeout"
                )

        threads = []
        for proxy in proxy_list:
            thread = threading.Thread(target=check_proxy, args=(proxy,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        return active_proxy_list

    def proxy_gui(self):
        """
        Create a graphical user interface (GUI) for Proxy chooser.

        Returns:
            None
        """
        active_proxy_list = self._proxy_status_checker()
        proxy_formatter = []

        def browser_proxy_creater():
            """
            Create a browser session with the selected proxy.

            Returns:
                None
            """
            if browser_dropdown.get() == "Google":
                proxy_info = proxy_dropdown.get()
                ip_start_index = proxy_info.find(":") + 2
                ip_end_index = proxy_info.find(",", ip_start_index)
                ip = proxy_info[ip_start_index:ip_end_index]
                port_start_index = proxy_info.find("Port: ") + len("Port: ")
                port_end_index = proxy_info.find(",", port_start_index)
                port = proxy_info[port_start_index:port_end_index]
                PROXY = f"{ip}:{port}"
                URL = "https://www.google.com/"
                command = f"google-chrome-stable --proxy-server={PROXY} {URL}"
                subprocess.Popen(command, shell=True)

        for item in active_proxy_list:
            ip = item["ip"]
            port = item["port"]
            country = item["country"]
            code = item["code"]
            proxy_formatter.append(
                f"IP: {ip}, Port: {port}, Country: {country}, Code: {code}"
            )
        window = tk.Tk()
        window.title("Ambush Proxy Client")
        browser_dropdown_label = tk.Label(window, text="Choose your Browser")
        browser_dropdown_label.pack()
        browser_dropdown = ttk.Combobox(window, width=40, values=["Google"])
        browser_dropdown.pack()
        proxy_dropdown_label = tk.Label(window, text="Choose your Proxy")
        proxy_dropdown_label.pack()
        proxy_dropdown = ttk.Combobox(window, width=40, values=proxy_formatter)
        proxy_dropdown.pack()
        launch_button = ttk.Button(window, text="Launch", command=browser_proxy_creater)
        launch_button.pack()
        window.mainloop()


proxy_instance = ProxyFetcher()
