from report.models import AppDaily, FrameworkDaily, DriverDaily, ProtocolDaily


class TeamUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_team_daily(user):
        if user == "app":
            return AppDaily
        elif user == "framework":
            return FrameworkDaily
        elif user == "driver":
            return DriverDaily
        elif user == "protocol":
            return ProtocolDaily
