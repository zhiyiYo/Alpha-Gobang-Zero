# Alpha Gobang Zero
基于自对弈强化学习的五子棋机器人。

## 界面
* 快乐游戏
  ![游戏界面](docs/screenshot/游戏界面.png)
* 配置游戏
  ![设置界面](docs/screenshot/设置界面.png)

## 快速开始
1. 创建虚拟环境并安装依赖包:

    ```shell
    conda create -n Alpha_Gobang_Zero python=3.8
    conda activate Alpha_Gobang_Zero
    pip install -r requirements.txt
    ```

2. 安装 `PyTorch`，具体操作参见 [博客](https://blog.csdn.net/qq_23013309/article/details/103965619)；

3. 训练模型:

    ```shell
    python train_alpha_gobang_zero.py
    ```

4. 开始游戏:

    ```shell
    python alpha_gobang_zero.py
    ```

## Reference
* [Mastering the game of Go without human knowledge](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ)
* [Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm](https://arxiv.org/abs/1712.01815)