# -*- coding:utf-8 -*- #

import multiprocessing
import threading


class Concurrency(object):

    threads = []
    processes = []

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

        return thread.ident

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

        return process.pid

    # TODO: Implement terminate
