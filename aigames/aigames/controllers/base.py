from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

from ..games.ttt.game import Game as TTT

VERSION_BANNER = """
Basic games with AI %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


class Base(Controller):
    class Meta:
        label = "base"
        description = "Basic games with AI"
        epilog = "Usage: aigames (game)"
        title = "Games"
        arguments = [(
            ["-v", "--version"],
            {"action": "version", "version": VERSION_BANNER},
        )]

    def _default(self):
        self.app.args.print_help()

    @ex(
        help="Tic Tac Toe",
        description="Tic Tac Toe.",
        arguments=[
            (
                ["-p1"],
                {
                    "help": "Player 1 (X)",
                    "action": "store",
                    "choices": TTT.player_types(),
                    "default": TTT.player_types()[0],
                },
            ),
            (
                ["-p2"],
                {
                    "help": "Player 2 (O)",
                    "action": "store",
                    "choices": TTT.player_types(),
                    "default": TTT.player_types()[0],
                },
            ),
            (
                ["-N"],
                {
                    "help": "Number of games",
                    "action": "store",
                    "dest": "N",
                    "default": 1,
                },
            ),
            (
                ["--save_file"],
                {
                    "help": "Name of save file of games",
                    "action": "store",
                    "dest": "save_file",
                    "default": "ttt_data.csv",
                },
            ),
        ],
    )
    def ttt(self):
        log = self.app.log
        try:
            N = int(self.app.pargs.N)
            if N < 1:
                raise Exception("N is negative.")
        except Exception as e:
            log.error(e)
            log.error("N must be a positive integer")
            raise e

        args = {
            "p1": self.app.pargs.p1,
            "p2": self.app.pargs.p2,
            "N": N,
            "save_file": self.app.pargs.save_file,
        }
        self.app.render(args, "ttt_startup.jinja2")

        for i in range(N):
            game = TTT(args["p1"], args["p2"], args["save_file"])
            game.play()
