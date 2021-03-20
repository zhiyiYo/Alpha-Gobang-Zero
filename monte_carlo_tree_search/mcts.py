# coding:utf-8
import random
from math import log, sqrt
from typing import List

import numpy as np

from .state import State


class Node:
    """ 蒙特卡洛树节点 """

    def __init__(self, state: State, parent=None):
        """
        Parameters
        ----------
        state: State
            当前局面
        """
        self.state = state
        self.parent = parent
        self.visit_times = 1
        self.win_times = 0
        self.children = []  # type:List[Node]

    def add_child(self, state: State):
        """ 添加子节点 """
        child = Node(state, self)
        self.children.append(child)

    def is_full_expand(self):
        """ 是否全展开 """
        return len(self.state.available_poses) == len(self.children)


class MCTree:
    """ 蒙特卡洛树 """

    def __init__(self, root: Node, c=sqrt(2)):
        """
        Parameters
        ----------
        root: Node
            根节点

        c: float
            UCT 算法中的探索常数，UCT公式为::

                reward = wi/ni + c * sqrt(log(N)/ni)
        """
        self.root = root
        self.c = c

    def search(self, iter_time: int):
        """ 蒙特卡洛搜索

        Parameters
        ----------
        iter_time: int
            迭代次数
        """
        # 如果只剩下一个落子位置，就直接返回该位置
        if len(self.root.state.available_poses) == 1:
            return self.root.state.available_poses[0]

        for i in range(iter_time):
            node = self.__select()
            color = self.__simulation(node)
            self.__back_propagation(node, color)
        return self.__get_best_child()

    def __select(self) -> Node:
        """ 选择一个子节点 """
        node = self.root
        while not node.state.is_game_over():
            if node.is_full_expand():
                node = self.__get_best_child()
            else:
                return self.__expand()
        return node

    def __expand(self, node: Node):
        """ 拓展节点 """
        states = [c.state for c in node.children]
        state = node.state.next_state()
        while state in states:
            state = node.state.next_state()
        node.add_child(state)
        return node.children[-1]

    def __simulation(self, node: Node):
        """ 随机模拟一局 """
        while not node.state.is_game_over():
            state = node.state.next_state()
        return state.color

    def __back_propagation(self, node: Node, color: int):
        """ 反向传播 """
        while node.parent:
            node.visit_times += 1
            node.win_times += int(color == node.state.color)
            node = node.parent

    def __get_best_child(self):
        """ 返回最佳子节点 """
        best_score = 0
        best_children = []
        for c in self.root.children:
            exploit = c.win_times / c.visit_times
            explore = sqrt(2 * log(self.root.visit_times) / c.visit_times)
            score = exploit + explore
            if score == best_score:
                best_children.append(c)
            elif score > best_score:
                best_children = [c]
                best_score = score

        return random.choice(best_children)
