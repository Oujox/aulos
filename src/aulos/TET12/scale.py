from aulos._core import DiatonicScale, NondiatonicScale

from .key import Key
from .pitchclass import PitchClass


class Major(
    DiatonicScale[Key, PitchClass],
    intervals=[2, 2, 1, 2, 2, 2, 1],
    key=Key,
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
):
    """Whole tone scale

    * A scale composed entirely of whole steps.
    * Characterized by its ambiguous, dreamlike sound with no leading tone.
    * The whole tone scale contains only six notes in total.
    * Commonly used in impressionist music, creating a floating, ethereal atmosphere.
    * Its symmetrical structure gives it a unique sound, with no tendency to resolve to a tonic.
    """
