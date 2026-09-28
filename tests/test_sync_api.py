from neon.animation import Animation
from neon.terminal import Terminal


def test_sync_api_only():
    assert hasattr(Animation, "typewriter")
    assert hasattr(Animation, "pulse")
    assert hasattr(Animation, "fade")
    assert hasattr(Animation, "glitch")
    assert hasattr(Animation, "rainbow")
    assert hasattr(Animation, "spinner")
    assert not hasattr(Animation, "atypewriter")
    assert not hasattr(Animation, "apulse")
    assert not hasattr(Animation, "afade")
    assert not hasattr(Animation, "aglitch")
    assert not hasattr(Animation, "arainbow")
    assert not hasattr(Animation, "aspinner")
    assert hasattr(Terminal, "write")
    assert not hasattr(Terminal, "awrite")
