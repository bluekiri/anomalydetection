# -*- coding:utf-8 -*- #
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import multiprocessing
import threading
import time

from rx.concurrency.mainloopscheduler.asyncioscheduler import asyncio


class Concurrency(object):

    queues_lock = threading.Lock()
    threads_lock = threading.Lock()
    processes_lock = threading.Lock()
    locks_lock = threading.Lock()

    threads = {}
    processes = {}
    queues = {}
    locks = {}

    _threads = []
    _processes = []

    @staticmethod
    def get_queue(name, mp=False):
        if name not in Concurrency.queues:
            with Concurrency.queues_lock:
                if name not in Concurrency.queues:
                    if mp:
                        Concurrency.queues[name] = multiprocessing.Queue()
                    else:
                        Concurrency.queues[name] = asyncio.Queue()
        return Concurrency.queues[name]

    @staticmethod
    def append_process(process):
        with Concurrency.processes_lock:
            Concurrency._processes.append(process)
            process.start()
            Concurrency.processes[process.pid] = \
                Concurrency._processes.index(process)

    @staticmethod
    def append_thread(thread):
        with Concurrency.threads_lock:
            Concurrency._threads.append(thread)
            thread.start()
            Concurrency.threads[thread.ident] = \
                Concurrency._threads.index(thread)

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
        Concurrency.append_thread(thread)
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
        Concurrency.append_process(process)
        if join:
            process.join(timeout)

        return process.pid

    @staticmethod
    def get_thread(ident):
        return Concurrency._threads[Concurrency.threads[ident]]

    @staticmethod
    def get_process(pid):
        return Concurrency._processes[Concurrency.processes[pid]]

    @staticmethod
    def kill_process(pid):
        Concurrency.get_process(pid).terminate()

    @staticmethod
    def get_lock(name):
        if name not in Concurrency.locks:
            with Concurrency.locks_lock:
                if name not in Concurrency.locks:
                    Concurrency.locks[name] = threading.Lock()
        return Concurrency.locks[name]

    @staticmethod
    def schedule_release(name, timeout=0):
        def release_async(_timeout):
            time.sleep(_timeout)
            Concurrency.get_lock(name).release()
        Concurrency.run_thread(target=release_async,
                               args=(timeout,))
