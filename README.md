# Alpha Gobang Zero
基于强化学习的五子棋机器人。

## 快速开始
1. 创建虚拟环境并安装依赖包:

    ```shell
    conda create -n Alpha_Gobang_Zero python=3.8
    conda activate Alpha_Gobang_Zero
    pip install -r requirements.txt
    ```

2. 安装 `PyTorch`；

3. 根据电脑是否装有 `NVIDIA` 显卡，设置 `~config.config` 中 `is_use_gpu` 的值；

4. 开始游戏:

    ```shell
    python alpha_gobang_zero.py
    ```
