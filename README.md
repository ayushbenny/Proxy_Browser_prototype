# Proxy Class

The Proxy class provides functionality for managing and using proxy servers. It allows you to retrieve a list of available proxies, check their status, and launch browser sessions with selected proxies.

## Class Definition

```python
class Proxy:
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
        ...

    def _proxy_url(self):
        """
        Retrieve a list of available proxy URLs.

        Returns:
            response: The response object containing the retrieved data.
        """
        ...

    def _proxy_fetcher(self):
        """
        Fetches the ports, IP addresses, countries, and other details from the websites.

        Returns:
            proxy_list (list): A list of dictionaries containing proxy details.
                Each dictionary has the following keys: 'ip', 'port', 'code', 'country'.
        """
        ...

    def _proxy_status_checker(self):
        """
        Check the status of the proxies to determine if they are active.

        Returns:
            active_proxy_list (list): A list of dictionaries containing active proxy details.
                Each dictionary has the following keys: 'ip', 'port', 'code', 'country'.
        """
        ...

    def proxy_gui(self):
        """
        Create a graphical user interface (GUI) for Proxy chooser.

        Returns:
            None
        """
        ...
Usage
Instantiate the Proxy class with the desired host, port, country, and code parameters. You can then use the class methods to retrieve available proxies, check their status, and launch browser sessions with selected proxies.

python
Copy code
# Example usage

# Instantiate the Proxy class
proxy = Proxy(host='example.com', port=8080, country='US', code='US-01')

# Retrieve available proxies
proxy_list = proxy._proxy_fetcher()

# Check proxy status
active_proxy_list = proxy._proxy_status_checker()

# Launch browser session with selected proxy
proxy.proxy_gui()
Make sure to replace the placeholder values with your desired values.

Requirements
The following libraries are required to use the Proxy class:

requests
lxml
tkinter
subprocess
threading
socket
tkinter.ttk
```
