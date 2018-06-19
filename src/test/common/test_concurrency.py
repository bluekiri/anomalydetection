# -*- coding:utf-8 -*- #
import time
import unittest
from queue import Queue, Empty

from anomalydetection.common.concurrency import Concurrency

from test import LoggingMixin


class TestKafkaStreamBackend(unittest.TestCase, LoggingMixin):

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

    def test_run_thread_no_join(self):

        q = Queue()
        wait = 1
        Concurrency.run_thread(target=self.compute,
                               name="the_answer",
                               args=(42, q, wait),
                               join=False)

        with self.assertRaises(Empty) as ex:  # noqa: F841
            q.get_nowait()

        time.sleep(wait)
        self.assertEqual(42, q.get_nowait())

    def test_run_process(self):

        q = Concurrency.get_queue("mp_queue", mp=True)
        Concurrency.run_process(target=self.compute,
                                name="the_answer",
                                args=(42, q,),
                                join=True)

        self.assertEqual(42, q.get())
