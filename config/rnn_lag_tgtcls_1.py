import os
import cPickle

from blocks import roles
from blocks.bricks import Rectifier
from blocks.filter import VariableFilter
from blocks.initialization import IsotropicGaussian, Constant

import data
from model.rnn_lag_tgtcls import Model, Stream

class EmbedderConfig(object):
    __slots__ = ('dim_embeddings', 'embed_weights_init')

pre_embedder = EmbedderConfig()
pre_embedder.embed_weights_init = IsotropicGaussian(0.001)
pre_embedder.dim_embeddings = [ 
    ('week_of_year', 52, 10),
    ('day_of_week', 7, 10),
    ('qhour_of_day', 24 * 4, 10),
    ('day_type', 3, 10),
    ('taxi_id', 448, 10),
]

post_embedder = EmbedderConfig()
post_embedder.embed_weights_init = IsotropicGaussian(0.001)
post_embedder.dim_embeddings = [ 
    ('origin_call', data.origin_call_train_size, 10), 
    ('origin_stand', data.stands_size, 10),
]

with open(os.path.join(data.path, 'arrival-clusters.pkl')) as f: tgtcls = cPickle.load(f)

hidden_state_dim = 100 
weights_init = IsotropicGaussian(0.01)
biases_init = Constant(0.001)

rec_to_out_dims = [200, 1000]
in_to_rec_dims = [200]

dropout = 0.5
dropout_inputs = VariableFilter(bricks=[Rectifier], name='output')

noise = 0.01
noise_inputs = VariableFilter(roles=[roles.PARAMETER])

batch_size = 10
batch_sort_size = 10
