import requests
import json
import os

url = "https://api.tivihub.app/live-streams"

headers = {
    'accept': 'application/json',
    'user-agent': 'TeeviHub Pro/1.0.9 (com.tivihub.app; build:97; android 10)',
    'device-id': '89fb653344416e52',
    'app-id': 'com.tivihub.app',
    'app-version': '1.0.9',
    'Host': 'api.tivihub.app'
}

def main():
    try:
        print("API থেকে ডেটা ফেচ করা হচ্ছে...")
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"ব্যর্থ হয়েছে! Status Code: {response.status_code}")
            return

        data = response.json()

        # ১. JSON ফাইল সংরক্ষণ
        with open("channels.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("channels.json ফাইল আপডেট হয়েছে।")

        # ২. M3U প্লেলিস্ট তৈরি
        channels = data.get('data', data) if isinstance(data, dict) else data
        
        m3u_lines = ["#EXTM3U\n"]
        count = 0

        for ch in channels:
            name = ch.get('name') or ch.get('title') or ch.get('channel_name') or "Unknown Channel"
            stream_url = ch.get('stream_url') or ch.get('url') or ch.get('link') or ch.get('hls_url')
            logo = ch.get('logo') or ch.get('poster') or ch.get('icon') or ""
            group = ch.get('category') or ch.get('group') or ch.get('genre') or "Live Streams"

            if stream_url:
                m3u_lines.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                m3u_lines.append(f'{stream_url}\n')
                count += 1

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.writelines(m3u_lines)
            
        print(f"সফলভাবে {count}টি চ্যানেল সহ playlist.m3u ফাইল তৈরি হয়েছে!")

    except Exception as e:
        print(f"ত্রুটি: {e}")

if __name__ == "__main__":
    main()
