from libqtile.widget.quick_exit import QuickExit


class QuickLaunch(QuickExit):

    def __init__(self, **config):
        super().__init__(**config)

    def update(self):
        if not self.is_counting:
            return
        
        if not self.launch_cmd:
            return

        self.countdown -= 1
        self.text = self.countdown_format.format(self.countdown)
        self.timer = self.timeout_add(self.timer_interval, self.update)
        self.draw()

        if self.countdown == 0:
            # TODO
            self.qtile.spawn(self.launch_cmd)
            return
