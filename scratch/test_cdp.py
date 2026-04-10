from playwright.sync_api import sync_playwright
import sys

def test_cdp():
    port = 9222
    print(f"Testing CDP connection on port {port}...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
            print("Successfully connected to browser.")
            print(f"Number of contexts: {len(browser.contexts)}")
            for i, context in enumerate(browser.contexts):
                print(f"Context {i} has {len(context.pages)} pages.")
                for j, page in enumerate(context.pages):
                    print(f"  Page {j}: {page.url}")
            browser.close()
        except Exception as e:
            print(f"Connection failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    test_cdp()
