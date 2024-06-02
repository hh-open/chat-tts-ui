from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import soundfile as sf
import os
import sys
import random
import datetime
from typing import Optional
from fastapi.responses import FileResponse

# 获取当前文件绝对路径
current_file_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(os.path.join(base_dir, 'ChatTTS'))
import ChatTTS

app = FastAPI()

# 初始化模型
model_path = os.path.join(base_dir, 'model', 'chatTTS')
chat = ChatTTS.Chat()
chat.load_models(source='local', local_path=model_path)

# Sample a speaker from Gaussian.
rand_spk = chat.sample_random_speaker()

class TextToSpeechRequest(BaseModel):
    text: str
    temperature: Optional[float] = 0.3
    top_k: Optional[int] = 20
    top_p: Optional[float] = 0.8

@app.post("/text-to-speech/")
async def create_audio(request: TextToSpeechRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required.")
    params_infer_code = {
        # 'spk_emb': rand_spk,
        }
    
    if request.temperature:
        params_infer_code['temperature'] = request.temperature
    if request.top_k:
        params_infer_code['top_K'] = request.top_k
    if request.top_p:
        params_infer_code['top_P'] = request.top_p
    

    # 根据传入参数调用模型推理
    wavs = chat.infer([request.text],params_infer_code=params_infer_code)
    audio_data = np.array(wavs[0])
    if audio_data.ndim == 1:
        audio_data = np.expand_dims(audio_data, axis=0)
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        
    output_file = f'outputs/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-{random.randint(1000, 9999)}.wav'
    sf.write(output_file, audio_data.T, 24000)
    
    return FileResponse(output_file, media_type='audio/wav', filename=os.path.basename(output_file))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8806)