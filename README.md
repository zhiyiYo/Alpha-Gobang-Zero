<p align="center">
  <img width="12%" align="center" src="app/resource/images/icon/二哈.png" alt="logo">
</p>
  <h1 align="center">
  Alpha Gobang Zero
</h1>

<p align="center">
  A gobang robot based on reinforcement learning
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Version-v1.0-blue.svg?color=00B16A" alt="Version v1.0"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.8.6-blue.svg?color=00B16A" alt="Python 3.8.6"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PyTorch-1.8.1-blue?color=00B16A" alt="PyTorch 1.8.1"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PyQt-5.15.2-blue?color=00B16A" alt="PyQt 5.15.2"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/OS-Win%2010%20|%20Win%2011-blue?color=00B16A" alt="OS Win10 | Win 11"/>
  </a>
</p>

<div align="center">
<img src="docs/screenshot/游戏界面.png" alt="游戏界面" width="70%"/>
</div>



## Policy-Value Net
* Network structure
  * `ConvBlock` × 1
  * `ResidueBlock` × 4
  * `PolicyHead` × 1
  * `ValueHead` × 1
* Network visualization
<div align="center">
<img src="docs/screenshot/模型架构.png" alt="模型架构" width="70%"/>
</div>

## Quick start
1. Create virtual environment:

    ```shell
    conda create -n Alpha_Gobang_Zero python=3.8
    conda activate Alpha_Gobang_Zero
    pip install -r requirements.txt
    ```

2. Install `PyTorch`，refer to the [blog](https://www.cnblogs.com/zhiyiYo/p/15865454.html) for details；


3. Start game:

    ```shell
    conda activate Alpha_Gobang_Zero
    python game.py
    ```

## Train model


  ```shell
  conda activate Alpha_Gobang_Zero
  python train.py
  ```


## Blog
[《如何使用自对弈强化学习训练一个五子棋机器人Alpha Gobang Zero》](https://www.cnblogs.com/zhiyiYo/p/14683450.html)

## Reference
* [《Mastering the game of Go without human knowledge》](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ)
* [《Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm》](https://arxiv.org/abs/1712.01815)


## FAQs
* **Why does the window get stuck when it is dragged?**

  Because the interface background uses acrylic effect, this problem will occur for some versions of win10. There are three solutions:

  * Upgrade win10 to the latest version.
  * Uncheck the check box of **Advanced system settings --> Performance --> Show window contents when dragging**.
  * Turn off the option to enable acrylic background in the setting interface.

* **Why does the configuration I modified in the settings interface not take effect immediately?**

  The modified configuration will take effect at the beginning of the next game.


## License
Alpha-Gobang-Zero is licensed under [GPLv3](./LICENSE).

Copyright © 2021 by zhiyiYo.
