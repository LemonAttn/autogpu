from autogpu import gpu, watch
import config

# 监控gpu
gpu_info = watch.watch_gpu(config = config, gpu = 'RTX 4090')
print(gpu_info)

# 购买gpu
gpu.use(config = config, gpu = 'RTX 4090')