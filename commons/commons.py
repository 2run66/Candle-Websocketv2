import yaml

try:
    with open('./config.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    pairs = config['pairs']
    intervals = config['intervals']
    redis_port = config['redis_port']
    redis_host = config['redis_host']

except Exception as e:
    print(e)
    exit(-1)
