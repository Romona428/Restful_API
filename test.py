import jwt  # 确保是这样导入

# 生成 token 的示例
token = jwt.encode(
    {'user_id': 'some_user_id', 'timestamp': int(time.time())}, 
    'your_secret_key', 
    algorithm='HS256'
)