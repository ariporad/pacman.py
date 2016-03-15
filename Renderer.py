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

    def _clear_screen_(self, gamemap):
        lines = len(gamemap) + 1
        if self._drawing_devtools_: lines += 1
        print("\033[{!s}A".format(lines))

    def draw(self, gamemap):
        output = ''

        self._clear_screen_(gamemap)

        for line in gamemap:
            for char in line:
                if char is None:
                    output += '  '
                else:
                    rendered = char.render()
                    output += rendered if len(rendered) >= 2 else rendered + ' '  # Auto pad with a space
            output += '\n'

        print(output)

        if self._drawing_devtools_:
            print(self._get_debug_bar_(gamemap))