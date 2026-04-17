from PIL import Image
import pytesseract

# 이미지 열기
captcha_image = Image.open("string.png")

# 텍스트 추출
captcha_text = pytesseract.image_to_string(captcha_image)

print("CAPTCHA 내용:", captcha_text)