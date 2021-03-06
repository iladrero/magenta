# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Polyphonic RNN model."""

# internal imports

import magenta
from magenta.models.polyphonic_rnn import polyphony_encoder_decoder
from magenta.models.shared import events_rnn_model


class PolyphonicRnnModel(events_rnn_model.EventSequenceRnnModel):
  """Class for RNN polyphonic sequence generation models."""

  def generate_polyphonic_sequence(
      self, num_steps, primer_sequence, temperature=1.0, beam_size=1,
      branch_factor=1, steps_per_iteration=1):
    """Generate a polyphonic track from a primer polyphonic track.

    Args:
      num_steps: The integer length in steps of the final track, after
          generation. Includes the primer.
      primer_sequence: The primer sequence, a PolyphonicSequence object.
      temperature: A float specifying how much to divide the logits by
         before computing the softmax. Greater than 1.0 makes tracks more
         random, less than 1.0 makes tracks less random.
      beam_size: An integer, beam size to use when generating tracks via
          beam search.
      branch_factor: An integer, beam search branch factor to use.
      steps_per_iteration: An integer, number of steps to take per beam search
          iteration.
    Returns:
      The generated PolyphonicSequence object (which begins with the provided
      primer track).
    """
    return self._generate_events(num_steps, primer_sequence, temperature,
                                 beam_size, branch_factor, steps_per_iteration)


default_configs = {
    'polyphony': events_rnn_model.EventSequenceRnnConfig(
        magenta.protobuf.generator_pb2.GeneratorDetails(
            id='polyphony',
            description='Polyphonic RNN'),
        magenta.music.OneHotEventSequenceEncoderDecoder(
            polyphony_encoder_decoder.PolyphonyOneHotEncoding()),
        magenta.common.HParams(
            batch_size=64,
            rnn_layer_sizes=[256, 256, 256],
            dropout_keep_prob=0.5,
            skip_first_n_losses=10,
            clip_norm=5,
            initial_learning_rate=0.001,
            decay_steps=1000,
            decay_rate=0.95)),
}

