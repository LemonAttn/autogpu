from autogpu import gpu, watch, login
import config

# 登陆
# login.login()


# 监控gpu
# gpu_info = watch.watch_gpu(config = config, gpu = 'RTX 4090')
# print(gpu_info)


# 购买gpu
gpu.use(config = config, gpu = 'RTX 3090')

# 钱包信息
# wallet = watch.watch_wallet(config)
# print(wallet)