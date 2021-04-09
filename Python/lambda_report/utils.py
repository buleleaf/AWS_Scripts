def read_instance_names_from_file(filename='{}-missing-metrics.csv'.format(os.environ['AWS_DEFAULT_REGION'])):
    """Reads a csv with the list of servers that are missing metrics"""
    with open(filename, newline='') as csvfile:
        return [r for r in csv.reader(csvfile)]

def add_csv_to_set(ec2_instances):
    for instances in read_instance_names_from_file():
        for i in instances:
            ec2_instances.add(i)
    return instances
    