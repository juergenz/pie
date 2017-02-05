__all__ = ['Callback', 'ModeScriptCallback']


class Callback:

    def __init__(self, name, parameter):

        self.name = name
        self.parameter = parameter

        if name == 'ManiaPlanet.PlayerChat':
            self.playerid = parameter[0]
            self.login = parameter[1]
            self.text = parameter[2]
            self.isCommand = parameter[3]
            return

        if name == 'TrackMania.PlayerCheckpoint':
            self.playerid = parameter[0]
            self.login = parameter[1]
            self.time_score = parameter[2]
            self.current_lap = parameter[3]
            self.checkpoint_index = parameter[4]
            return

        if name == 'TrackMania.PlayerFinish':
            self.playerid = parameter[0]
            self.login = parameter[1]
            self.time_score = parameter[2]
            return

        if name == 'ManiaPlanet.PlayerManialinkPageAnswer':
            self.playerid = parameter[0]
            self.login = parameter[1]
            self.answer = parameter[2]
            self.entries = parameter[3]
            return

        if name == 'ManiaPlanet.PlayerConnect':
            self.login = parameter[0]
            self.isSpectator = parameter[1]
            return

        if name == 'ManiaPlanet.PlayerDisconnect':
            self.login = parameter[0]
            self.DisconnectionReason = parameter[1]
            return

        if name == 'ManiaPlanet.MapListModified':
            self.CurrentMapIndex = parameter[0]
            self.NextMapIndex = parameter[1]
            self.IsListModified = parameter[2]
            return


class ModeScriptCallback:

    def __init__(self, name, parameter):

        self.name = parameter[0]
        self.parameter = parameter[1]