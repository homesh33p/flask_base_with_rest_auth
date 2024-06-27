from datetime import datetime,UTC
def decoded_exp_time_to_str(exp_timestamp):
    expire = datetime.fromtimestamp(exp_timestamp, tz=UTC)
    expire_str = expire.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return expire_str