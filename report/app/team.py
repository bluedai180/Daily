from report.models import AppDaily, FrameworkDaily, DriverDaily, ProtocolDaily, AppWeekly, FrameworkWeekly, \
    DriverWeekly, ProtocolWeekly, SPMDaily, SPMWeekly, App3Daily, App3Weekly


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
        elif user == "spm":
            return SPMDaily
        elif user == "app3":
            return App3Daily
        elif user == "director":
            return [AppDaily, DriverDaily, FrameworkDaily, ProtocolDaily, SPMDaily]

    @staticmethod
    def get_team_weekly(user):
        if user == "app":
            return AppWeekly
        elif user == "framework":
            return FrameworkWeekly
        elif user == "driver":
            return DriverWeekly
        elif user == "protocol":
            return ProtocolWeekly
        elif user == "spm":
            return SPMWeekly
        elif user == "app3":
            return App3Weekly
        elif user == "director":
            return [AppWeekly, DriverWeekly, FrameworkWeekly, ProtocolWeekly, SPMWeekly]
