import argparse
import subprocess
import os

def run_init_script():
    # 先运行 脚本 

    # script_path = "./init.sh"
    # os.chmod(script_path, 0o755)

    # subprocess.run([script_path], check=True)

    pass

def start_web():
    # 启动 Streamlit 前端界面
    web_path = os.path.join(os.getcwd(), 'web', 'web_page.py')
    subprocess.Popen(["streamlit", "run", web_path])

def start_server():
    # 启动 后端服务
    os.environ['PYTHONPATH'] = str(os.path.join(os.getcwd(), 'server')) + ':' + os.environ.get('PYTHONPATH', '')
    subprocess.Popen(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8806"])

if __name__ == "__main__":
    run_init_script()

    parser = argparse.ArgumentParser(description="启动前端和后端服务")
    parser.add_argument('--a', action='store_true', help='启动全部服务')
    parser.add_argument('--w', action='store_true', help='仅启动前端服务')
    parser.add_argument('--s', action='store_true', help='仅启动后端服务')

    args = parser.parse_args()

    if args.a:
        start_web()
        start_server()
    elif args.w:
        start_web()
    elif args.s:
        start_server()
