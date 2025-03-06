from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Media Extraction API is running!"

@app.route("/extract_media", methods=["POST"])
def extract_media():
    data = request.get_json()
    url = data.get("url")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to the URL and wait for JavaScript to load
        page.goto(url, timeout=60000)  
        page.wait_for_load_state("networkidle")  

        # Extract visible images & videos
        images = [img.get_attribute("src") for img in page.query_selector_all("img")]
        videos = [video.get_attribute("src") for video in page.query_selector_all("video")]

        browser.close()

    return jsonify({"media_links": images + videos if images + videos else ["No media found."]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
