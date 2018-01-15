import unittest

from Goap.AutonomousAgent import AutomatonStateMachine


class AutonomousAgentTest(unittest.TestCase):

    def setUp(self):
        pass

    def testAll(self):
        from pprint import PrettyPrinter
        pp = PrettyPrinter(indent=4)
        # priorities = AutomatonPriorities([
        #     {'vpc_state': 'available', 'db_state': 'available', 'app_state': 'running'}
        # ])
        world_state_matrix = {
            "vpc_state": 'Unknown',
            "db_state": 'Unknown',
            "app_state": 'Unknown',
        }
        goal = {
            "vpc_state": "available",
            "db_state": "available",
            "app_state": "running",
        }
        aws_actions = Actions()
        aws_actions.add(
            name='CreateVPC',
            pre_conditions={'vpc_state': 'unavailable', 'db_state': 'unavailable', 'app_state': 'unavailable'},
            effects={'vpc_state': 'available', 'db_state': 'unavailable', 'app_state': 'unavailable'},
            shell='echo "vpc created"'
        )
        aws_actions.add(
            name='CreateDB',
            pre_conditions={'vpc_state': 'available', 'db_state': 'unavailable', 'app_state': 'unavailable'},
            effects={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'unavailable'},
            shell='echo "db created"'
        )
        aws_actions.add(
            name='CreateApp',
            pre_conditions={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'unavailable'},
            effects={'vpc_state': 'available', 'db_state': 'available', 'app_state': 'running'},
            shell='echo "app created" > /tmp/CreateApp.out'
        )
        aws_sensors = Sensors()
        aws_sensors.add(
            name='FindProjectVPC',
            # shell='aws ec2 describe-vpcs --filters "Name=tag-key,Values=Name","Name=tag-value,Values=vpc_plataformas_stg" --query "Vpcs[].State" --output text',
            shell='echo "unavailable"',
            binding='vpc_state'
        )
        aws_sensors.add(
            name='FindProjectDB',
            # shell='aws rds describe-db-instances --filters "Name=db-instance-id,Values=rds-oraculo" --query "DBInstances[].DBInstanceStatus" --output text',
            shell='echo "unavailable"',
            binding='db_state'
        )
        aws_sensors.add(
            name='CheckAppState',
            shell='echo "unavailable"',
            binding='app_state'
        )
        ai = AutomatonStateMachine(goal=goal, name='infra_builder', actions=aws_actions, sensors=aws_sensors,
                                   world_state=world_state_matrix)
        ai.sense()
        ai.plan()
        ai.act()
