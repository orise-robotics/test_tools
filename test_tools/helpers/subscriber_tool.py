# Copyright 2021 Open Rise Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node


class SubscriberTool():

    def __init__(self, node: Node = None):
        self.__this_node = node if node is not None else Node('internal_node')
        self.__this_executor = MultiThreadedExecutor()
        self.__this_executor.add_node(self.__this_node)
        self.__msg = {}

    def create_subscription(self, topic_name, msg_type):
        self.__msg[topic_name] = None

        def _callback(msg):
            self.__this_node.get_logger().debug(
                f'called callback {topic_name}', throttle_duration_sec=0.1)

            self.__msg[topic_name] = msg

        self.__this_node.create_subscription(
            msg_type,
            topic_name,
            _callback,
            10)

    def await_for_msg(self, topic: str, timeout: float = None):
        self.__msg[topic] = None
        task = self.__this_executor.create_task(self._is_msg, topic)
        self.__this_executor.spin_until_future_complete(task, timeout)

        self.__this_node.get_logger().debug(f'is taks done? {task.done()}')
        self.__this_node.get_logger().debug(f'task result: {task.result().twist.twist}')

        return self.__msg[topic]

    async def _is_msg(self, topic):
        rclpy.spin_once(self.__this_node)  # force spin
        while self.__msg[topic] is None:
            continue
        return self.__msg[topic]
