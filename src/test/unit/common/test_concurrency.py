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

import time
import unittest
from queue import Queue, Empty

from anomalydetection.common.concurrency import Concurrency
from anomalydetection.common.logging import LoggingMixin


class TestConcurrency(unittest.TestCase, LoggingMixin):

    @staticmethod
    def compute(res, queue, wait=0):
        time.sleep(wait)
        queue.put(res)

    def test_run_thread(self):

        q = Queue()
        Concurrency.run_thread(target=self.compute,
                               name="the_answer",
                               args=(42, q,),
                               join=True)

        self.assertEqual(42, q.get())

    @unittest.skip("FIXME")
    def test_run_thread_timeout_error(self):

        q = Concurrency.get_queue("mp_queue", mp=True)
        wait = 10

        with self.assertRaises(TimeoutError) as ex:  # noqa: F841
            ident = Concurrency.run_thread(target=self.compute,
                                           name="the_answer",
                                           args=(42, q, wait),
                                           join=True,
                                           timeout=1.0)
            time.sleep(2)
            print(Concurrency.get_thread(ident).isAlive())

    def test_run_thread_no_join(self):

        q = Queue()
        wait = 1
        Concurrency.run_thread(target=self.compute,
                               name="the_answer",
                               args=(42, q, wait),
                               join=False)

        with self.assertRaises(Empty) as ex:  # noqa: F841
            q.get_nowait()

        time.sleep(wait*2)
        self.assertEqual(42, q.get_nowait())

    def test_run_process(self):

        q = Concurrency.get_queue("mp_queue", mp=True)
        Concurrency.run_process(target=self.compute,
                                name="the_answer",
                                args=(42, q,),
                                join=True)

        self.assertEqual(42, q.get())

    def test_run_process_no_join(self):

        q = Concurrency.get_queue("mp_queue", mp=True)
        wait = 1
        Concurrency.run_process(target=self.compute,
                                name="the_answer",
                                args=(42, q, wait),
                                join=False)

        with self.assertRaises(Empty) as ex:  # noqa: F841
            q.get_nowait()

        time.sleep(wait*2)
        self.assertEqual(42, q.get_nowait())

    def test_kill_process(self):

        q = Concurrency.get_queue("mp_queue", mp=True)
        wait = 3
        pid = Concurrency.run_process(target=self.compute,
                                      name="the_answer",
                                      args=(42, q, wait),
                                      join=False)

        Concurrency.kill_process(pid)

        time.sleep(wait*2)
        with self.assertRaises(Empty) as ex:  # noqa: F841
            q.get_nowait()
