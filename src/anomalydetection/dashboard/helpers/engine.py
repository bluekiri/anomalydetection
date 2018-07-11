# -*- coding: utf-8 -*-
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

from anomalydetection.backend.engine.builder import BaseEngineBuilder


class EngineBuilderForm(object):

    def __init__(self, engine_builder: BaseEngineBuilder) -> None:
        super().__init__()
        self.engine_builder = engine_builder

    def __input_build(self, name):
        return {
            "label": name,
            "name": name,
            "type": "text",
            "id": "__{}".format(name),
            "value": getattr(self.engine_builder, name.replace("set_", "")),
            "placeholder": ""
        }

    def get_form(self):
        method_list = [func for func in dir(self.engine_builder)
                       if callable(getattr(self.engine_builder, func))]
        return list(map(self.__input_build,
                        filter(lambda x: x.startswith("set_"),
                               method_list)))
