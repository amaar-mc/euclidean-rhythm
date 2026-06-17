"""Basic usage examples for euclidean-rhythm."""

from __future__ import annotations

from euclidean_rhythm import euclidean, evenness, necklace, rhythmic_oddity, rotate, syncopation


def main() -> None:
    # Generate the son clave: 3 onsets over 8 steps
    son = euclidean(pulses=3, steps=8)
    print(f"Son clave (3/8):       {son}")
    print(f"  As pattern:          {''.join('x' if v else '.' for v in son)}")

    # Generate the bossa nova clave: 5 onsets over 8 steps
    bossa = euclidean(pulses=5, steps=8)
    print(f"Bossa nova (5/8):      {bossa}")
    print(f"  As pattern:          {''.join('x' if v else '.' for v in bossa)}")

    # Rotate the son clave by 4 steps
    rotated = rotate(son, steps=4)
    print(f"Son clave rotated 4:   {rotated}")

    # Necklace (canonical form)
    print(f"Son clave necklace:    {necklace(son)}")
    print(f"Rotated necklace:      {necklace(rotated)}")
    print(f"  Same? {necklace(son) == necklace(rotated)}")

    # Evenness scores
    print(f"Evenness (son, 3/8):   {evenness(son):.4f}")
    print(f"Evenness (bossa, 5/8): {evenness(bossa):.4f}")
    print(f"Evenness (4/8, max):   {evenness(euclidean(pulses=4, steps=8)):.4f}")

    # Syncopation scores
    print(f"Syncopation (son):     {syncopation(son)}")
    print(f"Syncopation (4/8):     {syncopation(euclidean(pulses=4, steps=8))}")

    # Rhythmic oddity
    print(f"Oddity (son clave):    {rhythmic_oddity(son)}")
    print(f"Oddity (0,4 in 8):     {rhythmic_oddity([1, 0, 0, 0, 1, 0, 0, 0])}")


if __name__ == "__main__":
    main()
