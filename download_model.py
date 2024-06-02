# 安装ModelScope
# pip install modelscope

from modelscope import snapshot_download
model_dir = snapshot_download('pzc163/chatTTS',cache_dir='.')