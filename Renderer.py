class Renderer:
    def __init__(self):
        self._drawing_devtools_ = False

    def set_devtools_enabled(self, devtools):
        self._drawing_devtools_ = devtools

    def _get_debug_bar_(self, gamemap):
        return ''
        # if not DEV:
        #     return ''
        # return '({pos[0]:0=2}, {pos[1]:0=2}), {walls}, Points: {points}.'.format(
        #     pos=player_pos,
        #     walls='Walls' if SOLID_WALLS else 'No Walls',
        #     points=points
        # )

    def draw(self, gamemap):
        # Clear the screen
        print('\033[2J', end='')

        for line in gamemap:
            str = ''
            for char in line:
                if char is None:
                    str += '  '
                else:
                    rendered = char.render()
                    str += rendered if len(rendered) >= 2 else rendered + ' '  # Auto pad with a space
            print(str, end='\n\r')

        if self._drawing_devtools_:
            print(self._get_debug_bar_(gamemap))