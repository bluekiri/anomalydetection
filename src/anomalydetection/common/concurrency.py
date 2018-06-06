# -*- coding:utf-8 -*- #

import multiprocessing
import threading


class Concurrency(object):

    threads = []
    processes = []

    @staticmethod
    def run_thread(group=None, target=None, name=None, args=(), kwargs={}):
        thread = threading.Thread(
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs)
        thread.start()
        Concurrency.threads.append(thread)

    @staticmethod
    def run_process(group=None, target=None, name=None, args=(), kwargs={}):
        process = multiprocessing.Process(
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs)
        process.start()
        Concurrency.processes.append(process)

