#!/bin/bash

file_url="https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip"
filename="checkpoints_v2_0417.zip" 

# 存储的文件夹名称
target_directory="."
target_path="$target_directory/$filename"
unzip_target_path="." 

# 创建目标目录
mkdir -p $target_directory

# 检查目标文件是否已存在
if [ ! -f "$target_path" ]; then
    echo "文件不存在，正在下载..."
    # 下载文件
    wget $file_url -O $target_path
    echo "文件下载完成。"
fi

# 检查解压目标是否已经存在
if [ ! -d "$unzip_target_path" ]; then
    echo "开始解压文件..."
    # 解压文件
    if [[ $filename =~ \.tar\.gz$ ]]; then
        tar -xzf $target_path -C $target_directory
    elif [[ $filename =~ \.zip$ ]]; then
        unzip $target_path -d $unzip_target_path
    fi
    echo "解压完成。"
else
    echo "解压目标已存在，跳过解压。"
fi