# from openxlab.model import download
from huggingface_hub import hf_hub_download  # Load model directly
import os
from modelscope import snapshot_download

# 方法一：使用modelscope下载
# model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm-chat-7b', cache_dir='/Volumes/WD_BLACK/models', revision='v1.0.3')


# 方法二：使用huggingface-cli下载
# 设置环境变量
# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
# 下载模型
# os.system('huggingface-cli download --resume-download internlm/internlm-chat-7b --local-dir your_path')


# 方法三：使用huggingface-hub下载
# hf_hub_download(repo_id="internlm/internlm-7b", filename="config.json")

# 方法四：使用openxlab下载
# download(model_repo='OpenLMLab/InternLM-7b', model_name='InternLM-7b', output='your local path')



# 下载embedding模型

# 设置环境变量
# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载模型
os.system('huggingface-cli download --resume-download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --local-dir ./model/sentence-transformer')
# model_dir = snapshot_download('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
#                               cache_dir='/Volumes/WD_BLACK/models')
