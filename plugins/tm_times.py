import asyncio
import pie

class Time:

    def __init__(self, login, time_score, current_lap, checkpoint_index):

        self.login = login
        self.time_score = []
        self.current_lap = current_lap
        self.checkpoint_index = checkpoint_index
        self.time_score.append(time_score)
        self.is_finished = False
        self.next_cp_index = 1


    def newcp(self, login, time_score, current_lap, checkpoint_index):

        if checkpoint_index == self.next_cp_index:
            self.time_score.append(time_score)
            self.next_cp_index = self.next_cp_index + 1
            self.current_lap = current_lap
        else:
            raise Exception('error: cp count')



    def finish(self, login, time_score):

        if time_score == self.time_score[len(self.time_score) - 1]:
            self.is_finished = True
        else:
            raise Exception('error: finish time not equal to last cp')


class tm_times(pie.Plugin):

    def __init__(self):
        super().__init__()
        self._current_runs = {}


    @asyncio.coroutine
    def on_load(self):

        self.connect_event('TrackMania.PlayerCheckpoint', self.on_player_checkpoint)
        self.connect_event('TrackMania.PlayerFinish', self.on_player_finish)


    @asyncio.coroutine
    def on_player_checkpoint(self, callback):

        #yield from pie.chat_send(callback.name)
        #yield from pie.chat_send(callback.login)
        #yield from pie.chat_send(str(callback.time_score))
        #yield from pie.chat_send(str(callback.current_lap))
        #yield from pie.chat_send(str(callback.checkpoint_index))

        if callback.checkpoint_index == 0:
            # its a new run
            self._current_runs[callback.login] = Time(callback.login, callback.time_score, callback.current_lap, callback.checkpoint_index)
        else:
            self._current_runs[callback.login].newcp(callback.login, callback.time_score, callback.current_lap, callback.checkpoint_index)




    @asyncio.coroutine
    def on_player_finish(self, callback):

        #yield from pie.chat_send(callback.name)
        #yield from pie.chat_send(callback.login)
        #yield from pie.chat_send(str(callback.time_score))

        if not callback.time_score == 0:
            t = self._current_runs[callback.login]
            t.finish(callback.login, callback.time_score)
            yield from pie.chat_send(str(t.time_score))
            pie.send_event('pie.NewTime', t)
            #yield from pie.chat_send(str(_current_runs))