# This file is used for tests -- statements about how your program should work. 
## Currently these are "integration tests" -- we run the whole program and see if what happens matches what we expect

import itertools # Because I'm too lazy for lists
import sys # manipulate the state of python 

def test_basic(mocker, capsys): 
    # Make sure we can get a basic game over state. 

    # replace the normal 'input()' function with our own.
    # This is called a mock
    # Instead of asking the user for input every time, I instead create a function that returns:
    ## "McSpiff" the first time its called (for our character name)
    ## "left" the next 5 times its called
    # this mimics our basic game loop
    mocker.patch('builtins.input').side_effect = itertools.chain(['McSpiff'], itertools.repeat('left', 5)) 

    # we force python to unload the game code if its already been loaded, otherwise do nothing
    sys.modules.pop('game', None)

    # kick off our game!
    import game

    # Instead of writing the output to the user, we instead capture it so we can look at what it contains
    captured = capsys.readouterr()

    # Test that the output contains 'GAME OVER'
    assert 'GAME OVER' in captured.out

def test_handle_whitespace(mocker, capsys):
    # similar to test_basic, make sure we can still handle whitespace in our input
    mocker.patch('builtins.input').side_effect = itertools.chain(['McSpiff '], itertools.repeat('left     ', 5)) 
    sys.modules.pop('game', None)
    import game
    captured = capsys.readouterr()
    assert 'GAME OVER' in captured.out


def test_get_monk(mocker, capsys):
    # similar to test_basic, but instead of a game over, we make sure we get the monk in our party
    mocker.patch('builtins.input').side_effect = itertools.chain(['McSpiff', 'right', 'no', 'yes', 'no' ], itertools.repeat('left', 5))
    sys.modules.pop('game', None)
    import game
    captured = capsys.readouterr()
    assert 'The monk thanks you for your kindness and follows you down the road' in captured.out

def test_monk_dies_at_bridge(mocker, capsys):
    # Make sure that we can add a monk to our party, and later kill him
    # This is one of the more important tests, since its stateful
    mocker.patch('builtins.input').side_effect = itertools.chain(['McSpiff', 'right', 'no', 'yes', 'no' ], itertools.repeat('left', 5))
    sys.modules.pop('game', None)
    import game
    captured = capsys.readouterr()
    print(captured.out)
    assert 'he falls off the side of the bridge.' in captured.out


def test_die_at_mimic(mocker, capsys):
    # Similar to our first test, test_basic, but follows a few state transitions
    mocker.patch('builtins.input').side_effect = itertools.chain(['McSpiff', 'right', 'yes'], itertools.repeat('left', 5))
    sys.modules.pop('game', None)
    import game
    captured = capsys.readouterr()
    assert 'The chest is full of fangs that bite down on your arm, servering it. You bleed to death!' in captured.out