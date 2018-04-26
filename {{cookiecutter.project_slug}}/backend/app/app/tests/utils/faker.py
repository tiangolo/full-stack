import os

from faker import Faker

fake = Faker()

use_seed = os.getenv('SEED')
if use_seed:
    fake.seed(use_seed)
