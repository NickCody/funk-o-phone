import asyncio
from pyartnet import ArtNetNode
from pynput import keyboard
import math


def waitKey():
    with keyboard.Events() as events:
        events.get(1e6)


async def main():
    # Run this code in your async function
    node = ArtNetNode('127.0.0.1', 6454)

    # Create universe 0
    universe = node.add_universe(1)

    # Add a channel to the universe which consists of 3 values
    # Default size of a value is 8Bit (0..255) so this would fill
    # the DMX values 1..3 of the universe
    channel = universe.add_channel(start=6, width=3)

    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background
    angle = 0
    while True:
        angle += 0.05
        v = max(0, min(255, (math.sin(angle)+1) * 128))
        channel.set_values([v, v, v])
        await asyncio.sleep(1/60)

if __name__ == "__main__":
    asyncio.run(main())
