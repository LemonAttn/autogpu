from autogpu import gpu, watch, login
import config

# 登陆
# login.login()


# 监控gpu
gpu_info = watch.watch_gpu(config = config, gpu = 'RTX 3090')
print(gpu_info)


# 购买gpu
# pytorch(2.5.1, 2.3.0, 2.1.2, 2.1.0, 2.0.0)
gpu.use(config = config, gpu = 'RTX 3090', pytorch = '2.1.2')

# 钱包信息
# wallet = watch.watch_wallet(config)
# print(wallet)