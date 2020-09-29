from aigames.main import AiGamesTest


def test_aigames():
    # test aigames without any subcommands or arguments
    with AiGamesTest() as app:
        app.run()
        assert app.exit_code == 0


def test_aigames_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with AiGamesTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_ttt():
    argv = ['ttt', '-p1', 'RandomPlayer', '-p2', 'RandomPlayer']
    with AiGamesTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data['N'] == 1
        assert output.find('#Games   : 1')

    argv = ['ttt', '-N', '2', '-p1', 'RandomPlayer', '-p2', 'RandomPlayer']
    with AiGamesTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data['N'] == 2
        assert output.find('#Games   : 2')
