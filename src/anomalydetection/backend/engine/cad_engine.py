# -*- coding: utf-8 -*-
#
# Originally ported from https://github.com/smirmik/CAD
#
# Contextual Anomaly Detector
# Copyright (C) 2016 Mikhail Smirnov <smirmik@gmail.com>
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

import operator
import sys

from anomalydetection.backend.engine import BaseEngine
from anomalydetection.backend.entities.output_message import AnomalyResult


class ContextOperator(object):

    def __init__(self, max_left_semi_cntx_len):

        self.max_left_semi_cntx_len = max_left_semi_cntx_len
        self.facts_dics = [{}, {}]
        self.semi_context_dics = [{}, {}]
        self.semi_context_values_lists = [[], []]
        self.crossed_semi_contexts_lists = [[], []]
        self.contexts_values_list = []
        self.new_context_id = False

    def get_context_by_facts(self, new_contexts_list, zero_level=0):

        num_added_contexts = 0

        for left_facts, right_facts in new_contexts_list:

            left_hash = hash(left_facts)
            right_hash = hash(right_facts)

            next_left_semi_context_number = len(self.semi_context_dics[0])
            left_semi_context_i_d = self.semi_context_dics[0].setdefault(
                left_hash, next_left_semi_context_number)
            if left_semi_context_i_d == next_left_semi_context_number:
                left_semi_context_values = [[], len(left_facts), 0, {}]
                self.semi_context_values_lists[0].append(left_semi_context_values)
                for fact in left_facts:
                    semi_context_list = self.facts_dics[0].setdefault(fact, [])
                    semi_context_list.append(left_semi_context_values)

            next_right_semi_context_number = len(self.semi_context_dics[1])
            right_semi_context_id = self.semi_context_dics[1].setdefault(
                right_hash, next_right_semi_context_number)
            if right_semi_context_id == next_right_semi_context_number:
                right_semi_context_values = [[], len(right_facts), 0]
                self.semi_context_values_lists[1].append(right_semi_context_values)
                for fact in right_facts:
                    semi_context_list = self.facts_dics[1].setdefault(fact, [])
                    semi_context_list.append(right_semi_context_values)

            next_free_context_id_number = len(self.contexts_values_list)
            context_id = \
                self.semi_context_values_lists[0][left_semi_context_i_d][3].setdefault(
                    right_semi_context_id, next_free_context_id_number)

            if context_id == next_free_context_id_number:
                num_added_contexts += 1
                context_values = [0, zero_level, left_hash, right_hash]

                self.contexts_values_list.append(context_values)
                if zero_level:
                    self.new_context_id = context_id
                    return True
            else:
                context_values = self.contexts_values_list[context_id]

                if zero_level:
                    context_values[1] = 1
                    return False

        return num_added_contexts

    def context_crosser(self,
                        left_or_right,
                        facts_list,
                        new_context_flag=False,
                        potential_new_contexts=list()):

        num_new_contexts = None
        if left_or_right == 0:
            if len(potential_new_contexts) > 0:
                num_new_contexts = self.get_context_by_facts(potential_new_contexts)
            else:
                num_new_contexts = 0

        for semi_context_values in self.crossed_semi_contexts_lists[left_or_right]:
            semi_context_values[0] = []
            semi_context_values[2] = 0

        for fact in facts_list:
            for semi_context_values in self.facts_dics[left_or_right].get(fact, []):
                semi_context_values[0].append(fact)

        new_crossed_values = []
        for semi_context_values in self.semi_context_values_lists[left_or_right]:
            len_semi_context_values0 = len(semi_context_values[0])
            semi_context_values[2] = len_semi_context_values0
            if len_semi_context_values0 > 0:
                new_crossed_values.append(semi_context_values)

        self.crossed_semi_contexts_lists[left_or_right] = new_crossed_values

        if left_or_right:
            return self.update_contexts_and_get_active(new_context_flag)
        else:
            return num_new_contexts

    def update_contexts_and_get_active(self, new_context_flag):

        active_contexts = []
        num_selected_context = 0
        potential_new_context_list = []

        for left_semi_cntx_vals in self.crossed_semi_contexts_lists[0]:
            for right_semi_context_id, context_id in left_semi_cntx_vals[3].items():
                if self.new_context_id != context_id:
                    context_values = self.contexts_values_list[context_id]
                    right_semi_context_value0, \
                        right_semi_context_value1, \
                        right_semi_context_value2 = \
                        self.semi_context_values_lists[1][right_semi_context_id]

                    less_than_max_len = \
                        left_semi_cntx_vals[2] <= self.max_left_semi_cntx_len
                    if left_semi_cntx_vals[1] == left_semi_cntx_vals[2]:
                        num_selected_context += 1
                        if right_semi_context_value2 > 0:
                            if right_semi_context_value1 == right_semi_context_value2:
                                context_values[0] += 1
                                active_contexts.append(
                                    [context_id, context_values[0],
                                     context_values[2],
                                     context_values[3]])

                            elif context_values[1] \
                                    and new_context_flag \
                                    and less_than_max_len:
                                potential_new_context_list.append(
                                    tuple(
                                        [
                                            tuple(left_semi_cntx_vals[0]),
                                            tuple(right_semi_context_value0)
                                        ]
                                    )
                                )

                    elif context_values[
                        1] and new_context_flag and right_semi_context_value2 > 0 and \
                            left_semi_cntx_vals[2] <= self.max_left_semi_cntx_len:
                        potential_new_context_list.append(tuple(
                            [tuple(left_semi_cntx_vals[0]),
                             tuple(right_semi_context_value0)]))

        self.new_context_id = False

        return active_contexts, num_selected_context, potential_new_context_list


class CADDetector(BaseEngine):
    """
    Contextual Anomaly Detector - Open Source Edition
    https://github.com/smirmik/CAD
    """

    def __init__(self,
                 min_value=-sys.maxsize,
                 max_value=sys.maxsize,
                 threshold=0.95,
                 rest_period=30,
                 max_left_semi_contexts_length=8,
                 max_active_neurons_num=16,
                 num_norm_value_bits=3):

        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.rest_period = rest_period
        self.threshold = threshold
        self.max_active_neurons_num = max_active_neurons_num
        self.num_norm_value_bits = num_norm_value_bits
        self.max_bin_value = 2 ** self.num_norm_value_bits - 1.0
        self.full_value_range = self.max_value - self.min_value
        if self.full_value_range == 0.0:
            self.full_value_range = self.max_bin_value
        self.min_value_step = self.full_value_range / self.max_bin_value
        self.left_facts_group = tuple()
        self.context_operator = ContextOperator(max_left_semi_contexts_length)
        self.potential_new_contexts = []
        self.last_predictioned_facts = []
        self.result_values_history = [1.0]

    def step(self, inp_facts):

        curr_sens_facts = tuple(sorted(set(inp_facts)))

        if len(self.left_facts_group) > 0 and len(curr_sens_facts) > 0:
            pot_new_zero_level_context = tuple([self.left_facts_group,
                                                curr_sens_facts])
            new_context_flag = self.context_operator.get_context_by_facts(
                [pot_new_zero_level_context], zero_level=1)
        else:
            pot_new_zero_level_context = False
            new_context_flag = False

        active_contexts, num_selected_context, potential_new_context_list = \
            self.context_operator.context_crosser(
                left_or_right=1,
                facts_list=curr_sens_facts,
                new_context_flag=new_context_flag)

        num_uniq_pot_new_context = \
            len(set(potential_new_context_list).union(
                [pot_new_zero_level_context])
                if pot_new_zero_level_context
                else set(potential_new_context_list))

        percent_selected_context_active = \
            len(active_contexts) / float(num_selected_context) \
            if num_selected_context > 0 else 0.0

        active_contexts = sorted(active_contexts,
                                 key=operator.itemgetter(1, 2, 3))
        active_neurons = \
            [activeContextInfo[0]
             for activeContextInfo in active_contexts[-self.max_active_neurons_num:]]

        curr_neur_facts = set([2 ** 31 + fact for fact in active_neurons])

        self.left_facts_group = set()
        self.left_facts_group.update(curr_sens_facts, curr_neur_facts)
        self.left_facts_group = tuple(sorted(self.left_facts_group))

        num_new_contexts = self.context_operator.context_crosser(
            left_or_right=0,
            facts_list=self.left_facts_group,
            potential_new_contexts=potential_new_context_list)

        num_new_contexts += 1 if new_context_flag else 0

        percent_added_context_to_uniq_pot_new = \
            num_new_contexts / float(num_uniq_pot_new_context) \
            if new_context_flag and num_uniq_pot_new_context > 0 else 0.0

        return percent_selected_context_active, percent_added_context_to_uniq_pot_new

    def get_anomaly_score(self, input_data):

        norm_input_value = \
            int((input_data["value"] - self.min_value) / self.min_value_step)
        bin_input_norm_value = \
            bin(norm_input_value).lstrip("0b").rjust(self.num_norm_value_bits, "0")

        out_sens = set(
            [s_num * 2 + (1 if curr_symb == "1" else 0)
             for s_num, curr_symb in enumerate(reversed(bin_input_norm_value))])

        anomaly_value0, anomaly_value1 = self.step(out_sens)

        current_anomaly_score = (1.0 - anomaly_value0 + anomaly_value1) / 2.0

        less_than_threshold = \
            max(self.result_values_history[-int(self.rest_period):]) < self.threshold
        returned_anomaly_score = current_anomaly_score \
            if less_than_threshold \
            else 0.0
        self.result_values_history.append(current_anomaly_score)

        return returned_anomaly_score

    def predict(self, value: float, **kwargs) -> AnomalyResult:
        anomaly_score = self.get_anomaly_score(
            {"timestamp": kwargs["ts"], "value": value})

        return AnomalyResult(0.0,
                             0.0,
                             anomaly_score,
                             (anomaly_score >= self.threshold))
