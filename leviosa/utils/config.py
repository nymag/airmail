from functools import reduce

def buildConfig(transforms, config):
    return reduce(process, transforms, config)

# The function that the reduce runs
def process(config, fn):
    return fn(config)
