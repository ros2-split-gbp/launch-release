# Copyright 2019 Open Source Robotics Foundation, Inc.
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

import os
import sys
import unittest

import ament_index_python

import launch
import launch.actions

import launch_testing
import launch_testing.asserts
import launch_testing.tools

import pytest


def get_test_process_action(*, args=[]):
    test_proc_path = os.path.join(
        ament_index_python.get_package_prefix('launch_testing'),
        'lib/launch_testing',
        'terminating_proc'
    )
    return launch.actions.ExecuteProcess(
        cmd=[sys.executable, test_proc_path, *args],
        name='terminating_proc',
        # This is necessary to get unbuffered output from the process under test
        additional_env={'PYTHONUNBUFFERED': '1'},
    )


@pytest.mark.launch_test
def generate_test_description(ready_fn):
    return launch.LaunchDescription([
        launch_testing.util.KeepAliveProc(),
        launch.actions.OpaqueFunction(function=lambda context: ready_fn()),
    ])


class TestTerminatingProc(unittest.TestCase):

    def test_no_args(self, launch_service, proc_output, proc_info):
        """Test terminating_proc without command line arguments."""
        proc_action = get_test_process_action()
        with launch_testing.tools.launch_process(launch_service, proc_action) as dut:
            proc_info.assertWaitForStartup(process=dut, timeout=2)
            proc_output.assertWaitFor('Starting Up', process=dut, timeout=2)
            proc_output.assertWaitFor('Emulating Work', process=dut, timeout=2)
            proc_output.assertWaitFor('Done', process=dut, timeout=2)
            proc_output.assertWaitFor('Shutting Down', process=dut, timeout=2)
            proc_info.assertWaitForShutdown(process=dut, timeout=2)
        launch_testing.asserts.assertExitCodes(proc_info, process=dut)

    def test_with_args(self, launch_service, proc_output, proc_info):
        """Test terminating_proc with some command line arguments."""
        proc_action = get_test_process_action(args=['--foo', 'bar'])
        with launch_testing.tools.launch_process(launch_service, proc_action) as dut:
            proc_info.assertWaitForStartup(process=dut, timeout=2)
            proc_output.assertWaitFor('Starting Up', process=dut, timeout=2)
            proc_output.assertWaitFor(
                "Called with arguments ['--foo', 'bar']", process=dut, timeout=2
            )
            proc_output.assertWaitFor('Emulating Work', process=dut, timeout=2)
            proc_output.assertWaitFor('Done', process=dut, timeout=2)
            proc_output.assertWaitFor('Shutting Down', process=dut, timeout=2)
            proc_info.assertWaitForShutdown(process=dut, timeout=2)
        launch_testing.asserts.assertExitCodes(proc_info, process=dut)

    def test_unhandled_exception(self, launch_service, proc_output, proc_info):
        """Test terminating_proc forcing an unhandled exception."""
        proc_action = get_test_process_action(args=['--exception'])
        with launch_testing.tools.launch_process(launch_service, proc_action) as dut:
            proc_info.assertWaitForStartup(process=dut, timeout=2)
            proc_output.assertWaitFor('Starting Up', process=dut, timeout=2)
            proc_output.assertWaitFor(
                "Called with arguments ['--exception']", process=dut, timeout=2
            )
            proc_info.assertWaitForShutdown(process=dut, timeout=2)
        launch_testing.asserts.assertExitCodes(
            proc_info, process=dut, allowable_exit_codes=[1]
        )
