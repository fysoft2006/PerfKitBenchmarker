# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A measured interval that generates timing samples."""

from contextlib import contextmanager
import time

from perfkitbenchmarker import sample


class TimedInterval(object):
  """A measured interval that generates timing samples.

  Attributes:
    name: A string used to prefix generated samples' names.
    start_time: A float containing the time in seconds since the epoch, recorded
      at the beginning of a call to Measure, or None if Measure was not called.
    stop_time: A float containing the time in seconds since the epoch, recorded
      at the end of a call to Measure, or None if Measure was not called.
  """

  def __init__(self, name):
    """Create a named interval.

    Args:
      name: A string used to prefix the generated samples' names.
    """
    self._name = name
    self._start_time = None
    self._stop_time = None

  @property
  def name(self):
    return self._name

  @property
  def start_time(self):
    return self._start_time

  @property
  def stop_time(self):
    return self._stop_time

  @contextmanager
  def Measure(self):
    """Records the start and stop time of the enclosed interval."""
    self._start_time = time.time()
    yield
    self._stop_time = time.time()

  def GenerateSamples(self, include_timestamps=False):
    """Generates samples based on the times recorded in Measure.

    Args:
      include_runtime: A Boolean that controls whether samples containing the
        start and stop timestamps are added to the generated list.

    Returns:
      A list of Samples. If Measure has not been called, the list is empty.
      Otherwise, the list contains at least one Sample. The first Sample
      contains the elapsed time between the start and stop timestamps. If
      include_timestamps is True, a second and third Sample will be included.
      The second Sample will contain the start timestamp, and the third Sample
      will contain the stop timestamp.
    """
    samples = []
    if self._stop_time is not None:
      elapsed_time = self._stop_time - self._start_time
      samples.append(sample.Sample(
          self._name + ' Runtime', elapsed_time, 'seconds'))
      if include_timestamps:
        samples.append(sample.Sample(
            self._name + ' Start Timestamp', self._start_time, 'seconds'))
        samples.append(sample.Sample(
            self._name + ' Stop Timestamp', self._stop_time, 'seconds'))
    return samples