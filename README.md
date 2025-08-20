# Problem 1

## URL Shortener API (Flask)

This is a simple **URL Shortener REST API** built with **Flask**.  
It allows you to create short URLs, list all generated URLs, and optionally redirect to the original URL.

---

##  Features
- Create short URLs (`POST /shorturls`)  
- List all stored short URLs (`GET /shorturls`)  
- Redirect to original URL (`GET /<shortcode>`)  
- In-memory storage (data clears when server restarts)  

---

## Requirements
- Python 3.8+  
- Flask  

Install dependencies:
```bash
pip install flask
