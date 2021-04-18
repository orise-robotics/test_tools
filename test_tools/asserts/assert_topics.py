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

import time

from typing import List
from typing import Tuple

from rclpy.node import Node

__internal_node = Node('internal_node')


def assertTopics(expected: List[Tuple[str, List[str]]], timeout_sec: float):
    """
    Check if a list of topic names and types is available after node discovery.

    :param expected: List of tuples. The first element of each tuple is the topic
                     name and the second element is a list of topic types.

    :param timeout_sec Seconds to wait
    """
    topics = _get_topic_names_and_types(expected, timeout_sec)
    assert topics is not None, \
        f'Test failed due to timeout. No topic has been found for {timeout_sec} secs'

    for expected_topic in expected:
        assert expected_topic in topics, f'{expected_topic} not found in {topics}'


def _get_topic_names_and_types(expected, timeout_sec):
    """Make sure discovery has found all 'expected' topics."""
    start = time.monotonic()
    while True:
        topics = __internal_node.get_topic_names_and_types()
        now = time.monotonic()
        if all(expected_topic in topics for expected_topic in expected):
            return topics
        elif (now - start) < timeout_sec:
            continue
        else:
            return None
