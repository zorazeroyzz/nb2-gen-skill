#!/usr/bin/env python3
"""NB2 通用工具函数"""
import requests, base64, json, re, os, sys

DEFAULT_URL = "https://ai.ajiai.top/v1/chat/completions"
DEFAULT_KEY = ""  # 请设置环境变量 NB2_API_KEY
DEFAULT_MODEL = "AJbanana3-4k"

def get_config():
    key = os.environ.get("NB2_API_KEY", DEFAULT_KEY)
    if not key:
        print("Error: NB2_API_KEY not set", file=sys.stderr)
        print("请设置环境变量: export NB2_API_KEY='sk-你的key'", file=sys.stderr)
        sys.exit(1)
    return {
        "url": os.environ.get("NB2_API_URL", DEFAULT_URL),
        "key": key,
        "model": os.environ.get("NB2_MODEL", DEFAULT_MODEL),
    }

def image_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def make_image_content(path):
    b64 = image_to_b64(path)
    ext = path.rsplit(".", 1)[-1].lower()
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    return {"type": "image_url", "image_url": {"url": f"data:image/{mime};base64,{b64}"}}

def make_text_content(text):
    return {"type": "text", "text": text}

def call_api(messages, config=None, temperature=0.8, top_p=0.95):
    cfg = config or get_config()
    headers = {
        "Authorization": f"Bearer {cfg['key']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": cfg["model"],
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "response_modalities": ["IMAGE"]
    }
    
    try:
        resp = requests.post(cfg["url"], headers=headers, json=payload, timeout=180)
        if resp.status_code != 200:
            print(f"API Error ({resp.status_code}): {resp.text[:300]}", file=sys.stderr)
            return None, f"api_error:{resp.status_code}"
        
        data = resp.json()
        choices = data.get("choices", [])
        
        for choice in choices:
            finish = choice.get("finish_reason", "")
            if finish == "content_filter":
                print("BLOCKED by content filter", file=sys.stderr)
                return None, "blocked"
            
            msg = choice.get("message", {})
            content = msg.get("content", "")
            
            if isinstance(content, str):
                # Try to find base64 image in the content
                match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', content)
                if match:
                    return base64.b64decode(match.group(1)), None
                
                # Some APIs return JSON with image data
                try:
                    json_content = json.loads(content)
                    if "image" in json_content:
                        img_data = json_content["image"]
                        if isinstance(img_data, str):
                            return base64.b64decode(img_data), None
                except:
                    pass
        
        return None, "no_image"
    except requests.exceptions.Timeout:
        print("API Timeout", file=sys.stderr)
        return None, "timeout"
    except Exception as e:
        print(f"API Exception: {e}", file=sys.stderr)
        return None, str(e)

def save_image(img_bytes, output_path):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_bytes)
    print(f"Saved: {output_path} ({len(img_bytes)} bytes)")

def parse_size(size_str):
    """Parse size string to imageConfig format"""
    size_map = {
        "1k": "1K", "1K": "1K",
        "2k": "2K", "2K": "2K",
        "4k": "4K", "4K": "4K",
    }
    return size_map.get(size_str, "4K")

def parse_aspect(aspect_str):
    """Parse aspect ratio string"""
    aspect_map = {
        "1:1": "1:1",
        "2:3": "2:3",
        "3:2": "3:2",
        "4:3": "4:3",
        "3:4": "3:4",
        "16:9": "16:9",
        "9:16": "9:16",
    }
    return aspect_map.get(aspect_str, "2:3")
