import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import zipfile
DEBUG = False

BASE_DIR = Path(__file__).parent.parent.parent
SERVICE_PATH = os.path.join(BASE_DIR, 'service')
sys.path.append(SERVICE_PATH)

load_dotenv(os.path.join(SERVICE_PATH, '.env'))
if not DEBUG:
    PROXY_HOST = os.getenv('PROXY_HOST')  # rotating proxy or host
    PROXY_PORT = os.getenv('PROXY_PORT')  # port
    PROXY_USER = os.getenv('PROXY_USER')  # username
    PROXY_PASS = os.getenv('PROXY_PASS')  # password

    manifest_json = """	
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


