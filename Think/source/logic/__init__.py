from treelib import Node, Tree
from copy import copy
from itertools import *
from sys import getsizeof
from datetime import datetime
from core import config


class Task:
    def __init__(self, r: int):
        self.step = 1
        self.r = r
        self.d1, self.d2, self.d3, self.d4, self.d5, self.d6, self.d7, self.d8 = config['task']['d']

        self.c1, self.c2, self.c3, self.c4 = config['task']['c']

        self.start_date = datetime.now()

    def overload(self, count_of_workers: int, result: int, count: int):
        result += count * self.c1
        return count_of_workers, result, count

    def sleep(self, count_of_workers: int, result: int, count: int):
        result += count * self.c2
        return count_of_workers, result, count

    def hire(self, count_of_workers: int, result: int, count: int):
        result += count * self.c3
        count_of_workers += count
        return count_of_workers, result, count

    def unhire(self, count_of_workers: int, result: int, count: int):
        result += count * self.c4
        count_of_workers -= count
        return count_of_workers, result, count

    def __show(self, other: dict, day, total_nodes: int) -> None:
        print(' | '.join(
            [f'{item}: {other[item]} bytes' for item in list(
                other.keys())]) + f' | Day: {day} | Total nodes: {total_nodes} | Elapsed: {int((datetime.now() - self.start_date).total_seconds())} sec.',
              end='\r')

    def __verbose(self, items):
        items = [x.__name__ for x in items]
        verbose_view = []
        if 'overload' in items:
            c = items.count("overload")
            verbose_view.append(f'{c if c != 1 else ""}C1')
        if 'sleep' in items:
            c = items.count("sleep")
            verbose_view.append(f'{c if c != 1 else ""}C2')
        if 'hire' in items:
            c = items.count("hire")
            verbose_view.append(f'{c if c != 1 else ""}C3')
        if 'unhire' in items:
            c = items.count("unhire")
            verbose_view.append(f'{c if c != 1 else ""}C4')

        verbose_view = '+'.join(verbose_view)
        if not verbose_view:
            verbose_view = '</>'

        return verbose_view

    def calculate(self, days_up_to=8):
        total_memory = 0
        tree = Tree()
        price = 0
        count_of_workers = self.r
        tree.create_node("Root", f'd0_0', data={'cnt': count_of_workers, 'price': price})  # Day 0 or Root
        days = enumerate(([v for v in vars(self) if v.startswith('d')]))

        for di, day in days:
            print()
            need_workers = getattr(self, day)
            prev_day = f'd{di}'
            di += 1
            current_day = f'd{di}'

            if di == 1:
                methods = []

                if count_of_workers < need_workers:
                    methods.append(self.overload)
                    methods.append(self.hire)
                elif count_of_workers > need_workers:
                    methods.append(self.sleep)
                    methods.append(self.unhire)

                delta = abs(count_of_workers - need_workers)
                tries = product(methods, repeat=delta)
                tries = [[y.__name__ for y in x] for x in tries]
                tries = [tuple(sorted(x)) for x in tries]
                tries = list(set(tries))
                tries = [[getattr(self, y) for y in x] for x in tries]
                #  tries = list(set([tuple(sorted([y.__name__ for y in x])) for x in product(methods, repeat=delta)]))

                for i, item in enumerate(tries):
                    tmp_res = copy(price)
                    tmp_cow = copy(count_of_workers)
                    for x in item:
                        tmp_cow, tmp_res, _ = x(tmp_cow, tmp_res, self.step)

                    verbose_view = self.__verbose(item)

                    tree.create_node(str(f'C:{tmp_cow}|P:{tmp_res}|V:{verbose_view}|N:{day}_{i}|R:{need_workers}'),
                                     f'{day}_{i}',
                                     data={'cnt': tmp_cow, 'price': tmp_res, 'total_price': tmp_res,
                                           'vw': verbose_view}, parent='d0_0')

                    self.__show({'Tree': getsizeof(tree.nodes), 'Steps': getsizeof(tries)}, current_day,
                                len(tree.nodes))
            else:
                nodes_names = [x for x in tree.nodes if prev_day in x]
                epoch = 0
                for nd_i, nname in enumerate(nodes_names):
                    pnode = tree.get_node(nname)
                    pcnt = pnode.data['cnt']
                    pprice = pnode.data['price']
                    ptotal_price = pnode.data['total_price']

                    delta = abs(pcnt - need_workers)

                    methods = []

                    if pcnt < need_workers:
                        methods.append(self.overload)
                        methods.append(self.hire)
                    elif pcnt > need_workers:
                        methods.append(self.sleep)
                        methods.append(self.unhire)

                    tries = product(methods, repeat=delta)
                    tries = [[y.__name__ for y in x] for x in tries]
                    tries = [tuple(sorted(x)) for x in tries]
                    tries = list(set(tries))
                    tries = [[getattr(self, y) for y in x] for x in tries]

                    for i, item in enumerate(tries):
                        tmp_res = copy(pprice)
                        tmp_cow = copy(pcnt)
                        tmp_tp = copy(ptotal_price)

                        new_price = 0
                        for x in item:
                            tmp_cow, new_price, _ = x(tmp_cow, new_price, self.step)

                        verbose_view = self.__verbose(item)

                        tree.create_node(
                            str(f'C:{tmp_cow}|P:{new_price}|V:{verbose_view}|N:{current_day}_{epoch}|R:{need_workers}'),
                            f'{current_day}_{epoch}',
                            data={'cnt': tmp_cow, 'price': new_price, 'total_price': new_price + tmp_tp,
                                  'vw': verbose_view}, parent=nname)
                        epoch += 1

                        self.__show({'Tree': getsizeof(tree.nodes), 'Steps': getsizeof(tries)}, current_day,
                                    len(tree.nodes))
            if di == days_up_to:
                break

        print()
        print('Tree built. Resolving min path...')

        last_nodes = [x for x in tree.nodes if x.startswith(f'd{days_up_to}_')]
        vals = [tree.get_node(x).data['total_price'] for x in last_nodes]
        min_val = min(vals)
        min_name = last_nodes[vals.index(min_val)]
        node = tree.get_node(min_name)
        fullpath = [node.data['vw']]
        tmp = node
        while True:
            try:
                cur = tree.parent(tmp.identifier)
                fullpath.append(cur.data['vw'])
                tmp = cur
            except:
                break

        fullpath.reverse()

        print(f'Min price is: {min_val} | Tag: {f"({node.tag})"} | Name: {min_name} | FullPath={" + ".join(fullpath)}')

        return min_val

        # tree.to_graphviz('result')

        # tree.show()
