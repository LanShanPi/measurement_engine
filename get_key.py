
# 生成鉴权用的 API Key
import secrets
# 目前的key：706a7e968f94bf81eff199e2f0af125b16b08e3de597c2f63350c3c9cb79668d
def generate_api_key(length=32):
    """
    生成一个指定长度的随机API Key，默认长度为32字节（转换成十六进制后为64字符）。
    你可以根据需要调整长度。
    """
    return secrets.token_hex(length)

if __name__ == "__main__":
    # 生成一个随机的 API Key
    api_key = generate_api_key()
    print(f"Your API Key: {api_key}")