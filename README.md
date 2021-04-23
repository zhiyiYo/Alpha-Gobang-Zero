<p align="center">
  <img width="12%" align="center" src="app/resource/images/icon/二哈.png" alt="logo">
</p>
  <h1 align="center">
  Alpha Gobang Zero
</h1>

<p align="center">
   基于自对弈强化学习的五子棋机器人
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
    <img src="https://img.shields.io/badge/PyQt-5.13.2-blue?color=00B16A" alt="PyQt 5.13.2"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/OS-Windows%2010-blue?color=00B16A" alt="OS Window10"/>
  </a>
</p>

<div align="center">
<img src="docs/screenshot/游戏界面.png" alt="游戏界面" width="75%" style="box-shadow: 0 1px 15px rgba(27, 31, 35, .15)"/>
<br>
<img src="docs/screenshot/设置界面.png" alt="设置界面" width="75%" style="box-shadow: 0 1px 15px rgba(27, 31, 35, .15)"/>
</div>



## 策略-价值网络
* 网络组成 (各个模块的具体信息参见 [项目大纲](docs/项目大纲.md))
  * `ConvBlock` × 1
  * `ResidueBlock` × 4
  * `PolicyHead` × 1
  * `ValueHead` × 1
* 网络可视化

  ![模型架构](docs/screenshot/模型架构.png)

## 快速开始
1. 创建虚拟环境并安装依赖包:

    ```shell
    conda create -n Alpha_Gobang_Zero python=3.8
    conda activate Alpha_Gobang_Zero
    pip install -r requirements.txt
    ```

2. 安装 `PyTorch`，具体操作参见博客 [Pytorch 的安装](https://blog.csdn.net/qq_23013309/article/details/103965619)；


3. 开始游戏:

    ```shell
    python game.py
    ```

## 训练模型
* 开始训练:

    ```shell
    python train.py
    ```
    
* 误差曲线

  ![误差曲线](docs/screenshot/误差曲线.png)
  
## 博客
* [《如何使用自对弈强化学习训练一个五子棋机器人Alpha Gobang Zero》](https://www.cnblogs.com/zhiyiYo/p/14683450.html)

## 参考文献
* [Mastering the game of Go without human knowledge](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ)
* [Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm](https://arxiv.org/abs/1712.01815)

## 证书
```
MIT License

Copyright (c) 2021 Zhengzhi Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
