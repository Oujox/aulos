from ..implements.scale import HarmonicMinor, Major, MelodicMinor


class Ionian(
    Major,
    intervals=Major.intervals,
    shift=0,
):
    """Ionian mode (Major scale)

    * Also known as the major scale.
    * A diatonic scale with a happy, bright, or resolved sound.
    * Composed of the intervals: [2, 2, 1, 2, 2, 2, 1].
    * The foundation of Western music harmony and melody.
    * Frequently used in a wide variety of musical genres.
    * This mode starts at the root of the major scale (no shift).
    """


class Dorian(
    Major,
    intervals=Major.intervals,
    shift=1,
):
    """Dorian mode

    * A minor scale with a raised 6th degree.
    * Composed of the intervals: [2, 1, 2, 2, 2, 1, 2].
    * Known for its jazzy, bluesy character, balancing between major and minor.
    * The 6th degree distinguishes Dorian from the natural minor scale.
    * Often used in jazz, blues, and rock for improvisation.
    * This mode starts from the 2nd degree of the major scale.
    """


class Phrygian(
    Major,
    intervals=Major.intervals,
    shift=2,
):
    """Phrygian mode

    * A minor scale with a lowered 2nd degree.
    * Composed of the intervals: [1, 2, 2, 2, 1, 2, 2].
    * Known for its dark, exotic, or Spanish flavor.
    * The lowered 2nd degree gives it a distinct, dissonant sound.
    * Common in flamenco music and jazz.
    * This mode starts from the 3rd degree of the major scale.
    """


class Lydian(
    Major,
    intervals=Major.intervals,
    shift=3,
):
    """Lydian mode

    * A major scale with a raised 4th degree.
    * Composed of the intervals: [2, 2, 2, 1, 2, 2, 1].
    * Known for its bright, dreamy, or floating sound.
    * The raised 4th degree gives it a unique flavor, often used in jazz fusion and progressive rock.
    * This mode starts from the 4th degree of the major scale.
    """


class Mixolydian(
    Major,
    intervals=Major.intervals,
    shift=4,
):
    """Mixolydian mode

    * A major scale with a lowered 7th degree.
    * Composed of the intervals: [2, 2, 1, 2, 2, 1, 2].
    * Known for its bluesy or dominant sound.
    * The lowered 7th degree gives it a less resolved sound compared to the Ionian mode.
    * Often used in rock, blues, and funk.
    * This mode starts from the 5th degree of the major scale.
    """


class Aeorian(
    Major,
    intervals=Major.intervals,
    shift=5,
):
    """Aeolian mode (Natural minor scale)

    * A natural minor scale with no raised or lowered degrees.
    * Composed of the intervals: [2, 1, 2, 2, 1, 2, 2].
    * Known for its melancholic, somber, or sad sound.
    * The foundation for the minor scale in Western music.
    * Often used in classical, rock, and pop music.
    * This mode starts from the 6th degree of the major scale.
    """


class Locrian(
    Major,
    intervals=Major.intervals,
    shift=6,
):
    """Locrian mode

    * A minor scale with a lowered 2nd and 5th degree.
    * Composed of the intervals: [1, 2, 2, 1, 2, 2, 2].
    * Known for its dissonant, unstable, and tense sound.
    * The lowered 5th degree gives it a diminished quality.
    * Rarely used in classical or contemporary music, but found in experimental and avant-garde genres.
    * This mode starts from the 7th degree of the major scale.
    """


class Dorian_f2(
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=1,
):
    """Dorian flat 2 mode (Dorian #2)

    * A modified version of the Dorian mode with a lowered 2nd degree.
    * Composed of the intervals: [1, 2, 2, 2, 2, 1, 2].
    * Known for its exotic, tense sound.
    * This mode is often used in jazz and fusion for a darker minor sound.
    * This mode starts from the 2nd degree of the melodic minor scale.
    """


class Lydian_s5(
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=2,
):
    """Lydian sharp 5 mode (Lydian #5)

    * A Lydian mode with a raised 5th degree.
    * Composed of the intervals: [2, 2, 2, 1, 3, 1, 2].
    * Known for its otherworldly, dreamlike quality.
    * The raised 5th degree creates an augmented chord quality.
    * Often used in jazz and experimental music for rich harmonic tension.
    * This mode starts from the 3rd degree of the melodic minor scale.
    """


class Lydian_f7(
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=3,
):
    """Lydian flat 7 mode (Lydian b7)

    * A Lydian mode with a lowered 7th degree.
    * Composed of the intervals: [2, 2, 2, 2, 1, 2, 1].
    * Known for its mix of major and dominant qualities.
    * Often used in jazz, fusion, and progressive rock.
    * This mode starts from the 4th degree of the melodic minor scale.
    """


class Mixolydian_f6(
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=4,
):
    """Mixolydian flat 6 mode (Mixolydian b6)

    * A Mixolydian mode with a lowered 6th degree.
    * Composed of the intervals: [2, 2, 1, 2, 1, 2, 2].
    * Known for its bluesy, jazzy sound.
    * The lowered 6th degree gives it a minor quality while maintaining the dominant 7th.
    * This mode is commonly used in jazz and fusion.
    * This mode starts from the 5th degree of the melodic minor scale.
    """


class Aeorian_f5(
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=5,
):
    """Aeolian flat 5 mode (Aeolian b5)

    * A natural minor scale with a lowered 5th degree.
    * Composed of the intervals: [2, 1, 2, 1, 2, 2, 2].
    * Known for its dark, exotic sound, often used in jazz and metal.
    * This mode creates a diminished quality by lowering the 5th degree.
    * This mode starts from the 6th degree of the melodic minor scale.
    """


class SuperLocrian(
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=6,
):
    """Super Locrian mode (Altered scale)

    * A scale with altered 2nd, 3rd, 4th, 5th, 6th, and 7th degrees.
    * Composed of the intervals: [1, 2, 1, 2, 1, 2, 2].
    * Known for its highly dissonant, tension-filled sound.
    * Often used in jazz over diminished or dominant chords.
    * The altered scale is a tool for creating complex harmonies.
    * This mode starts from the 7th degree of the melodic minor scale.
    """


class Locrian_n6(
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=1,
):
    """Locrian natural 6 mode (Locrian #6)

    * A Locrian mode with a raised 6th degree.
    * Composed of the intervals: [1, 2, 2, 1, 2, 3, 1].
    * Known for its eerie, dissonant sound with a slight major flavor due to the raised 6th degree.
    * This mode is used in jazz and contemporary music for unusual, dissonant harmonic progressions.
    * This mode starts from the 2nd degree of the harmonic minor scale.
    """


class Ionian_s5(
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=2,
):
    """Ionian sharp 5 mode (Ionian #5)

    * A major scale with a raised 5th degree.
    * Composed of the intervals: [2, 2, 1, 2, 3, 1, 1].
    * Known for its bright sound with a dramatic twist due to the sharp 5th.
    * Often used in fusion and experimental music to create harmonic tension.
    * This mode starts from the 3rd degree of the harmonic minor scale.
    """


class Dorian_s4(
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=3,
):
    """Dorian sharp 4 mode (Dorian #4)

    * A Dorian mode with a raised 4th degree.
    * Composed of the intervals: [2, 1, 2, 3, 2, 1, 2].
    * Known for its tension and dark character.
    * Often used in jazz and fusion for a modern, complex sound.
    * This mode starts from the 4th degree of the harmonic minor scale.
    """


class Mixolydian_f9(
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=4,
):
    """Mixolydian flat 9 mode (Phrygian Dominant)

    * A Mixolydian mode with a lowered 9th degree.
    * Composed of the intervals: [1, 2, 2, 2, 1, 2, 2].
    * Known for its exotic, Middle Eastern flavor.
    * Often used in flamenco, metal, and jazz to create tension and drama.
    * This mode starts from the 5th degree of the harmonic minor scale.
    """


class Lydian_s2(
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=5,
):
    """Lydian flat 2 mode (Lydian b2)

    * A Lydian mode with a lowered 2nd degree.
    * Composed of the intervals: [1, 3, 2, 1, 2, 2, 2].
    * Known for its dramatic, exotic sound with a raised 4th and lowered 2nd degree.
    * Often used in avant-garde and fusion music to create tension and mystery.
    * This mode starts from the 6th degree of the harmonic minor scale.
    """


class AlteredSuperLocrian(
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=6,
):
    """Altered Super Locrian mode (Altered scale with Super Locrian qualities)

    * A highly altered scale that is often used in jazz and fusion.
    * Composed of the intervals: [1, 2, 1, 2, 1, 2, 2].
    * Known for its extreme dissonance and tension, incorporating all possible alterations of the major scale.
    * Features a mix of both diminished and augmented intervals, contributing to its complex and unstable sound.
    * Often used in jazz over dominant chords to create maximum harmonic tension and to resolve to tonic chords.
    * This mode starts from the 7th degree of the harmonic minor scale.
    """
