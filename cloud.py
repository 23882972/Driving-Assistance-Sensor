import BlynkLib
import time

# 替换为你的 Blynk 模板 ID、名称和 Auth Token
BLYNK_TEMPLATE_ID = "TMPL6csW7nFJ6"
BLYNK_TEMPLATE_NAME = "AAA"
BLYNK_AUTH_TOKEN = "8lOPKEwSzuOs6BI1Y-Iy2rn31o5KjA4f"

# 初始化 Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# 这个部分 Raspberry Pi 不需要手动处理 WiFi 连接
# 因为 Pi 的 WiFi 连接由操作系统管理

def setup():
    print("Starting Blynk connection...")

def loop():
    blynk.run()  # 保持与 Blynk 平台的连接

if __name__ == "__main__":
    setup()
    while True:
        loop()
        time.sleep(1)  # 每秒钟运行一次
