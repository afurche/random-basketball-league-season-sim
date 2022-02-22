import numpy.random as npr
from player import Player
import names


class PlayerGenerator:
    position_attribute_wages = {

        "PG": {"layups": (75, 99),
               "mid_range": (70, 99),
               "long_range": (70, 99),
               "passing": (80, 99),
               "ball_handling": (80, 99),
               "paint_defence": (30, 80),
               "perimeter_defence": (65, 99),
               "stealing": (70, 99),
               "blocking": (20, 65)},

        "SG": {"layups": (75, 99),
               "mid_range": (70, 99),
               "long_range": (70, 99),
               "passing": (70, 95),
               "ball_handling": (80, 99),
               "paint_defence": (45, 90),
               "perimeter_defence": (70, 99),
               "stealing": (75, 99),
               "blocking": (45, 70)},

        "SF": {"layups": (75, 99),
               "mid_range": (70, 99),
               "long_range": (65, 99),
               "passing": (65, 90),
               "ball_handling": (70, 90),
               "paint_defence": (70, 95),
               "perimeter_defence": (65, 95),
               "stealing": (60, 90),
               "blocking": (60, 90)},

        "PF": {"layups": (80, 99),
               "mid_range": (70, 95),
               "long_range": (20, 70),
               "passing": (55, 75),
               "ball_handling": (30, 60),
               "paint_defence": (75, 99),
               "perimeter_defence": (40, 75),
               "stealing": (45, 85),
               "blocking": (75, 99)},

        "C": {"layups": (70, 99),
              "mid_range": (65, 99),
              "long_range": (55, 99),
              "passing": (80, 99),
              "ball_handling": (80, 99),
              "paint_defence": (70, 85),
              "perimeter_defence": (50, 80),
              "stealing": (80, 99),
              "blocking": (50, 65)},
    }

    @classmethod
    def generate_player(cls, position, team_name):

        return Player(names.get_first_name(gender='male'),
                      names.get_last_name(),
                      position,
                      [npr.randint(val[0], val[1]) for val in cls.position_attribute_wages[position].values()],
                      team_name
                      )


