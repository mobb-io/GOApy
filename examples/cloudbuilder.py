
from Goap.Action import Actions
from Goap.Agent import Agent


class CloudBuild:

    PRIORITIES = [
        {'vpc': True, 'db': True, 'app': True},
        {'vpc': 'monitoring', 'db': 'monitoring', 'app': 'monitoring'},
    ]

    def __init__(self):
        # ACTIONS
        self.actions = Actions()
        # VPC/Network set
        self.actions.add_action(
            name='CreateVPC',
            pre_conditions={'vpc': False, 'db': False, 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )
        # DB set
        self.actions.add_action(
            name='CreateDB',
            pre_conditions={'vpc': True, 'db': False, 'app': False},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        self.actions.add_action(
            name='StopDB',
            pre_conditions={'vpc': True, 'db': 'started', 'app': False},
            effects={'vpc': True, 'db': 'stopped', 'app': False}
        )
        self.actions.add_action(
            name='StartDB',
            pre_conditions={'vpc': True, 'db': 'stopped', 'app': False},
            effects={'vpc': True, 'db': 'started', 'app': False}
        )
        self.actions.add_action(
            name='DestroyDB',
            pre_conditions={'vpc': True, 'db': 'not_health', 'app': False},
            effects={'vpc': True, 'db': False, 'app': False}
        )
        # APP set
        self.actions.add_action(
            name='CreateApp',
            pre_conditions={'vpc': True, 'db': True, 'app': False},
            effects={'vpc': True, 'db': True, 'app': True}
        )
        self.actions.add_action(
            name='StartApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'stopped'},
            effects={'vpc': True, 'db': True, 'app': 'started'}
        )
        self.actions.add_action(
            name='StopApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'started'},
            effects={'vpc': True, 'db': True, 'app': 'stopped'}
        )
        self.actions.add_action(
            name='DestroyApp',
            pre_conditions={'vpc': True, 'db': True, 'app': 'not_health'},
            effects={'vpc': True, 'db': True, 'app': False}
        )
        # inconsistent
        self.actions.add_action(
            name='DestroyInconsistentState',
            pre_conditions={'vpc': 'inconsistent', 'db': 'inconsistent', 'app': 'inconsistent'},
            effects={'vpc': False, 'db': False, 'app': False}
        )
        self.actions.add_action(
            name='Monitoring',
            pre_conditions={'vpc': True, 'db': True, 'app': True},
            effects={'vpc': 'monitoring', 'db': 'monitoring', 'app': 'monitoring'}
        )
        # init_state = {'vpc': False, 'app': False, 'db': False}
        init_goal = {'vpc': True, 'db': True, 'app': True}
        self.ai = Agent(name='CloudBuilder', priorities=self.PRIORITIES, actions=self.actions, goal=init_goal)

    def run_agent(self):
        self.ai.run()


if __name__ == '__main__':
    ai = CloudBuild()
    ai.run_agent()
