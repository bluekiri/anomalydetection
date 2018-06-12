# -*- coding:utf-8 -*- #
import logging
import multiprocessing
import threading

from rx import Observable
from rx.concurrency.mainloopscheduler.asyncioscheduler import asyncio


class Concurrency(object):

    lock = threading.Lock()
    supervised = False
    threads = []
    processes = []
    queues = {}

    @staticmethod
    def supervise() -> None:

        def debug_threads_or_processes(threads_or_processes):
            for item in threads_or_processes:
                logging.info(item)

        if not Concurrency.supervised:
            with Concurrency.lock:
                if not Concurrency.supervised:
                    Observable.interval(5000).subscribe(
                        lambda x: debug_threads_or_processes(Concurrency.threads))
                    Observable.interval(5000).subscribe(
                        lambda x: debug_threads_or_processes(Concurrency.processes))
                    Concurrency.supervised = True

    @staticmethod
    def run_thread(group=None,
                   target=None,
                   name=None,
                   args=(),
                   kwargs={},
                   join=None,
                   timeout=None):
        thread = threading.Thread(
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs)
        if not join:
            thread.daemon = True
        thread.start()
        Concurrency.threads.append(thread)
        if join:
            thread.join(timeout)

        Concurrency.supervise()
        return thread.ident

    @staticmethod
    def get_queue(name, mp=False):
        if name not in Concurrency.queues:
            with Concurrency.lock:
                if name not in Concurrency.queues:
                    if mp:
                        Concurrency.queues[name] = multiprocessing.Queue()
                    else:
                        Concurrency.queues[name] = asyncio.Queue()
        return Concurrency.queues[name]

    @staticmethod
    def run_process(group=None,
                    target=None,
                    name=None,
                    args=(),
                    kwargs={},
                    join=None,
                    timeout=None):
        process = multiprocessing.Process(
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs)
        if not join:
            process.daemon = True
        process.start()
        Concurrency.processes.append(process)
        if join:
            process.join(timeout)

        Concurrency.supervise()
        return process.pid

    # TODO: Implement terminate
