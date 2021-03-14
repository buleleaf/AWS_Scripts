import boto3
import pprint


def get_ecs_services(client):
    ecs_serv_list = client.list_services(
        cluster='fathom-ecs-cluster-staging',
        maxResults=100

    )
    return(ecs_serv_list['serviceArns'])


def describe_ecs(client, ecs_services):
    task_def = []

    for ecs_service in ecs_services:
        service = client.describe_services(
            cluster='atlas-microservices-prod',
            services=[ecs_service]
        )
        task_def.append(service)
    task_def_result = []
    for task in task_def:
        for service in task['services']:
            for task in service['deployments']:
                if (task['taskDefinition']):
                    task_def_result.append(task['taskDefinition'])
    return(task_def_result)

def describe_ecs_task(client, ecs_list):
    ecs_images = []
    for taskId in ecs_list:
        taskDefinition = client.describe_task_definition(
            taskDefinition=taskId
        )
        for cont_def in taskDefinition['taskDefinition']['containerDefinitions']:
            if (cont_def['image']):
                ecs_images.append(cont_def['image'])
    return(ecs_images)

def main():
    """Main."""

client = boto3.client('ecs', 'us-west-2')
ecs_services = get_ecs_services(client)
ecs_list = describe_ecs(client, ecs_services)
ecs_task = describe_ecs_task(client, ecs_list)

for images in ecs_task:
    print(images.split('/')[-1].split(':'))


# pp = pprint.PrettyPrinter(indent=2)

# pp.pprint(ecs_task)

if __name__ == '__main__':
    main()
