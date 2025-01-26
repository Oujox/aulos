from ..scale import DiatonicScale, NondiatonicScale
from .note import Key, PitchClass


class Major(
    DiatonicScale[Key, PitchClass],
    intervals=[2, 2, 1, 2, 2, 2, 1],
    key=Key,
    pitchclass=PitchClass,
):
    """Major scale (Ionian mode)

    * Consisting of a specific pattern of whole and half steps: [2, 2, 1, 2, 2, 2, 1].
    * The most commonly used scale in Western music, characterized by a happy or bright sound.
    * Derived from the diatonic system, starting from the root note and ascending.
    * Frequently used as the foundation for other musical scales and modes.
    """


class Minor(
    DiatonicScale[Key, PitchClass],
    intervals=[2, 1, 2, 2, 1, 2, 2],
    key=Key,
    pitchclass=PitchClass,
):
    """Minor scale (Aeolian mode)

    * Consists of the following intervals: [2, 1, 2, 2, 1, 2, 2].
    * Known for its melancholic, somber, or sad sound.
    * The natural minor scale, often used in classical, rock, and pop music.
    * The third degree is lowered by a half-step compared to the major scale.
    * Forms the basis for many modal scales, including the harmonic and melodic minor scales.
    """


class HarmonicMinor(
    DiatonicScale[Key, PitchClass],
    intervals=[2, 1, 2, 2, 1, 3, 1],
    key=Key,
    pitchclass=PitchClass,
):
    """Harmonic minor scale

    * Consists of the following intervals: [2, 1, 2, 2, 1, 3, 1].
    * A variation of the natural minor scale with a raised 7th degree.
    * Known for its exotic, dramatic sound, often used in classical and metal music.
    * The raised 7th degree creates an augmented second between the 6th and 7th degrees.
    * Frequently used to create tension in chord progressions.
    """


class MelodicMinor(
    DiatonicScale[Key, PitchClass],
    intervals=[2, 1, 2, 2, 2, 2, 1],
    key=Key,
    pitchclass=PitchClass,
):
    """Melodic minor scale

    * Consists of the following intervals: [2, 1, 2, 2, 2, 2, 1].
    * In its ascending form, both the 6th and 7th degrees are raised.
    * Known for its smooth, sophisticated sound, often used in jazz and classical music.
    * The descending form typically uses the natural minor scale (Aeolian mode).
    * The raised 6th and 7th degrees help avoid awkward intervals in melodic motion.
    """


class Pentatonic(
    NondiatonicScale[Key, PitchClass],
    extensions=[[0], [0], [0], [], [0], [0], []],
    base=Major,
    key=Key,
    pitchclass=PitchClass,
):
    """Pentatonic scale

    * A five-note scale derived from the major scale.
    * Composed of the notes: 1, 2, 3, 5, 6 in relation to the major scale.
    * Known for its simplicity and versatility, commonly used in folk, blues, and rock music.
    * The pentatonic scale omits the 4th and 7th degrees of the major scale.
    * Works well in both major and minor contexts, creating a neutral or balanced sound.
    """


class MinorPentatonic(
    NondiatonicScale[Key, PitchClass],
    extensions=[[0], [], [0], [0], [0], [], [0]],
    base=Minor,
    key=Key,
    pitchclass=PitchClass,
):
    """Minor pentatonic scale

    * A five-note scale derived from the natural minor scale.
    * Composed of the notes: 1, 3, 4, 5, 7 in relation to the natural minor scale.
    * Known for its bluesy, soulful sound, commonly used in rock, blues, and jazz music.
    * Omits the 2nd and 6th degrees of the minor scale.
    * Provides a simple yet expressive framework for improvisation and melody.
    """


class Bluenote(
    NondiatonicScale[Key, PitchClass],
    extensions=[[0], [0], [-1, 0], [0], [-1, 0], [0], [-1, 0]],
    base=Major,
    key=Key,
    pitchclass=PitchClass,
):
    """Bluenote scale

    * A variation of the pentatonic scale with the addition of flat 5 (blue note).
    * Composed of the notes: 1, 2, 3, 4, 5b, 6, 7.
    * Characterized by its "bluesy" sound, used extensively in jazz, blues, and rock.
    * The flat 5 creates a distinct tension and release, making it effective for expressive improvisation.
    * Often associated with the "blue" feeling, evoking melancholy or sadness.
    """


class Diminish(
    NondiatonicScale[Key, PitchClass],
    extensions=[[0], [0], [-1], [0, 1], [1], [0], [0]],
    base=Major,
    key=Key,
    pitchclass=PitchClass,
):
    """Diminish scale

    * A symmetrical scale that alternates between whole and half steps.
    * Composed of the intervals: [2, 1, 2, 1, 2, 1, 2].
    * Known for its tension-filled, dissonant sound.
    * Frequently used in jazz and classical music for chromatic and diminished chord progressions.
    * The scale's symmetrical nature creates repeated patterns and interesting melodic possibilities.
    """


class CombDiminish(
    NondiatonicScale[Key, PitchClass],
    extensions=[[0], [-1], [-1, 0], [1], [0], [0], [-1]],
    base=Major,
    key=Key,
    pitchclass=PitchClass,
):
    """CombDiminish scale

    * A combination of diminished and whole-tone scale patterns.
    * Composed of alternating diminished and whole-step intervals, creating a hybrid structure.
    * Known for its mysterious, unconventional sound, often used in jazz and avant-garde music.
    * The scale's hybrid nature allows for chromatic movement and unusual chord progressions.
    """


class Wholetone(
    NondiatonicScale[Key, PitchClass],
    extensions=[[0], [0], [0], [1], [1], [1], []],
    base=Major,
    key=Key,
    pitchclass=PitchClass,
):
    """Whole tone scale

    * A scale composed entirely of whole steps.
    * Characterized by its ambiguous, dreamlike sound with no leading tone.
    * The whole tone scale contains only six notes in total.
    * Commonly used in impressionist music, creating a floating, ethereal atmosphere.
    * Its symmetrical structure gives it a unique sound, with no tendency to resolve to a tonic.
    """


class Ionian(
    Major,
    intervals=Major.intervals,
    shift=0,
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
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
    key=Key,
    pitchclass=PitchClass,
):
    """Altered Super Locrian mode (Altered scale with Super Locrian qualities)

    * A highly altered scale that is often used in jazz and fusion.
    * Composed of the intervals: [1, 2, 1, 2, 1, 2, 2].
    * Known for its extreme dissonance and tension, incorporating all possible alterations of the major scale.
    * Features a mix of both diminished and augmented intervals, contributing to its complex and unstable sound.
    * Often used in jazz over dominant chords to create maximum harmonic tension and to resolve to tonic chords.
    * This mode starts from the 7th degree of the harmonic minor scale.
    """
