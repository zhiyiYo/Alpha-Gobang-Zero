# coding:utf-8
import random
from math import log, sqrt
from typing import List
from copy import deepcopy

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
        return len(self.state.available_actions) == len(self.children)


class MCTS:
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

        Returns
        -------
        action_pos: tuple
            落子位置
        """
        # 如果只剩下一个落子位置，就直接返回该位置
        if len(self.root.state.available_actions) == 1:
            return self.root.state.available_actions[0]

        for i in range(iter_time):
            node = self.__select()
            is_win = self.__default_policy(node.state)
            self.__back_propagation(node, is_win)
        return self.__get_best_child(self.root).state.pre_action

    def __select(self) -> Node:
        """ 选择一个子节点 """
        node = self.root
        while not node.state.is_game_over():
            if node.is_full_expand():
                node = self.__get_best_child(node)
            else:
                return self.__expand(node)
        return node

    def __expand(self, node: Node):
        """ 拓展节点 """
        pre_actions = {c.state.pre_action for c in node.children}
        available_actions = set(node.state.available_actions)
        action = random.choice(list(available_actions-pre_actions))
        state = node.state.do_action(action)
        node.add_child(state)
        return node.children[-1]

    def __default_policy(self, state: State):
        """ 随机模拟一局，判断当前状态是否获胜

        Parameters
        ----------
        state: `State`
            进行判断的当前状态

        Returns
        -------
        is_win: bool
            是否胜利
        """
        color = state.color
        while not state.is_game_over():
            state = state.next_state()
        # 考虑平局
        if not state.is_ends_in_a_draw:
            return (state.color != color)
        return None

    def __back_propagation(self, node: Node, is_win):
        # 记录进行随机模拟的节点颜色
        color = node.state.color
        """ 反向传播 """
        while node.parent:
            node.visit_times += 1
            # 考虑平局
            if is_win is not None:
                eq = (color == node.state.color)
                node.win_times += int((eq and is_win)
                                      or (not eq and not is_win))
            node = node.parent

    def __get_best_child(self, node: Node):
        """ 返回最佳子节点 """
        best_score = 0
        best_children = []
        for c in node.children:
            exploit = c.win_times / c.visit_times
            explore = sqrt(2 * log(node.visit_times) / c.visit_times)
            score = exploit + explore
            if score == best_score:
                best_children.append(c)
            elif score > best_score:
                best_children = [c]
                best_score = score
        return random.choice(best_children)
