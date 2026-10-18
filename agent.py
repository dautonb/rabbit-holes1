import html
import os
import random
import requests

# Cấu hình từ thông tin bạn cung cấp
ORTHOGONAL_API_KEY = "orth_live_NFY755JrMiRCyGWAOso5X8X8tgEPcauf"
TELEGRAM_BOT_TOKEN = "8804138155:AAFFvQHiE9pQKryOGUDXHSgAOYUzi2HGONo"
TELEGRAM_CHAT_ID = "5152496526"


def search_quirky_topics():
  # Danh sách từ khóa tìm kiếm các chủ đề kỳ quặc trên Internet
  queries = [
      "bizarre internet history mystery website",
      "weird dead technology that came back",
      "strange things people bought online virtual land history",
      "obscure weird historical internet phenomena",
  ]
  chosen_query = random.choice(queries)

  url = "https://api.orthogonal.com/v1/run"
  headers = {
      "Authorization": f"Bearer {ORTHOGONAL_API_KEY}",
      "Content-Type": "application/json",
  }
  payload = {"api": "serper", "path": "/search", "query": {"q": chosen_query}}

  try:
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
      data = response.json()
      results = data.get("data", {}).get("organic", [])
      return results
    else:
      print(f"Lỗi gọi Orthogonal API: {response.status_code} - {response.text}")
      return []
  except Exception as e:
    print(f"Exception khi gọi API: {e}")
    return []


def generate_html_post(search_results):
  if not search_results:
    return (
        "🤖 <b>Bản tin Kỳ quặc Internet Hôm nay</b>\n\n"
        "Hôm nay hệ thống chưa tìm thấy dữ liệu mới từ mạng, agent sẽ thử lại"
        " vào khung giờ tiếp theo!"
    )

  # Lấy ngẫu nhiên một kết quả thú vị để phân tích
  item = random.choice(search_results[:5]) if search_results else {}
  title = item.get("title", "Một câu chuyện kỳ lạ trên mạng")
  snippet = item.get("snippet", "Không có mô tả chi tiết.")
  link = item.get("link", "https://google.com")

  # Làm sạch các ký tự HTML đặc biệt để tránh lỗi cú pháp
  safe_title = html.escape(title)
  safe_snippet = html.escape(snippet)

  html_content = f"""🧩 <b>Chủ đề Kỳ quặc Internet Hôm nay</b>

<b>📌 Chuyện gì xảy ra:</b>
{safe_title}

<i>Mô tả:</i> {safe_snippet}

<b>💡 Điều gì thú vị?</b>
Câu chuyện này thu hút sự tò mò bởi những khía cạnh độc lạ, phản ánh một góc khuất kỳ thú hoặc sự sáng tạo khó hiểu của con người trên không gian mạng.

<b>🔗 Nguồn đáng đọc tiếp:</b>
• <a href="{link}">{safe_title}</a>
"""
  return html_content


def send_telegram_message(text):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": text,
      "parse_mode": "HTML",  # Sử dụng chế độ HTML an toàn hơn cho dữ liệu web
      "disable_web_page_preview": False,
  }
  response = requests.post(url, json=payload)
  if response.status_code == 200:
    print("Đã gửi tin nhắn HTML lên Telegram thành công!")
  else:
    print(f"Lỗi gửi Telegram: {response.status_code} - {response.text}")


if __name__ == "__main__":
  print("Đang tìm kiếm chủ đề kỳ quặc...")
  results = search_quirky_topics()
  post_content = generate_html_post(results)
  print("Đang gửi nội dung lên Telegram...")
  send_telegram_message(post_content)
