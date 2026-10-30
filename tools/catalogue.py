"""Verified catalogue for the Musopen starter set.

Keys, catalogue numbers and movement headings checked against English Wikipedia
(and IMSLP for Borodin No. 1 and Suk Op. 35a), Oct 2026.
"""

ITEM = "MusopenKickstarterRecordings"
ITEM_URL = f"https://archive.org/details/{ITEM}"
LICENCE = "CC0 1.0"
LICENCE_URL = "http://creativecommons.org/publicdomain/zero/1.0/"

CNSO = "Czech National Symphony Orchestra"
MSQ = "Musopen String Quartet"

GOLDBERG = ["Aria"] + [f"Variatio {n}" + s for n, s in [
    (1, ""), (2, ""), (3, ". Canone all'Unisono"), (4, ""), (5, ""),
    (6, ". Canone alla Seconda"), (7, ". Al tempo di Giga"), (8, ""),
    (9, ". Canone alla Terza"), (10, ". Fughetta"), (11, ""),
    (12, ". Canone alla Quarta in moto contrario"), (13, ""), (14, ""),
    (15, ". Canone alla Quinta: Andante"), (16, ". Ouverture"), (17, ""),
    (18, ". Canone alla Sesta"), (19, ""), (20, ""),
    (21, ". Canone alla Settima"), (22, ". Alla breve"), (23, ""),
    (24, ". Canone all'Ottava"), (25, ". Adagio"), (26, ""),
    (27, ". Canone alla Nona"), (28, ""), (29, ""), (30, ". Quodlibet"),
]] + ["Aria da capo"]

# composer, surname, work, key, catalogue, performers, source dir (in staging),
# movements, wikipedia/imslp reference
WORKS = [
    dict(composer="Ludwig van Beethoven", surname="Beethoven",
         work="Symphony No. 3", key="E-flat major", cat="Op. 55", perf=CNSO,
         src="Beethoven - Symphony No 3 Eroica",
         mov=["Allegro con brio", "Marcia funebre: Adagio assai",
              "Scherzo: Allegro vivace", "Finale: Allegro molto"],
         ref="https://en.wikipedia.org/wiki/Symphony_No._3_(Beethoven)"),
    dict(composer="Johannes Brahms", surname="Brahms",
         work="Symphony No. 1", key="C minor", cat="Op. 68", perf=CNSO,
         src="Brahms - Symphony No 1 in C Major",
         mov=["Un poco sostenuto – Allegro – Meno allegro", "Andante sostenuto",
              "Un poco allegretto e grazioso",
              "Adagio – Più andante – Allegro non troppo, ma con brio – Più allegro"],
         ref="https://en.wikipedia.org/wiki/Symphony_No._1_(Brahms)"),
    dict(composer="Johannes Brahms", surname="Brahms",
         work="Symphony No. 2", key="D major", cat="Op. 73", perf=CNSO,
         src="Brahms - Symphony No2 in D major",
         mov=["Allegro non troppo", "Adagio non troppo",
              "Allegretto grazioso (quasi andantino)", "Allegro con spirito"],
         ref="https://en.wikipedia.org/wiki/Symphony_No._2_(Brahms)"),
    dict(composer="Johannes Brahms", surname="Brahms",
         work="Symphony No. 3", key="F major", cat="Op. 90", perf=CNSO,
         src="Brahms - Symphony No 3",
         mov=["Allegro con brio", "Andante", "Poco allegretto", "Allegro"],
         ref="https://en.wikipedia.org/wiki/Symphony_No._3_(Brahms)"),
    dict(composer="Johannes Brahms", surname="Brahms",
         work="Symphony No. 4", key="E minor", cat="Op. 98", perf=CNSO,
         src="Brahms - Symphony No 4 in E minor",
         mov=["Allegro non troppo", "Andante moderato", "Allegro giocoso",
              "Allegro energico e passionato"],
         ref="https://en.wikipedia.org/wiki/Symphony_No._4_(Brahms)"),
    dict(composer="Pyotr Ilyich Tchaikovsky", surname="Tchaikovsky",
         work="Symphony No. 6", key="B minor", cat="Op. 74", perf=CNSO,
         src="Tchaikovsky - Symphony Pathetique",
         mov=["Adagio – Allegro non troppo", "Allegro con grazia",
              "Allegro molto vivace", "Finale: Adagio lamentoso"],
         ref="https://en.wikipedia.org/wiki/Symphony_No._6_(Tchaikovsky)"),
    dict(composer="Ludwig van Beethoven", surname="Beethoven",
         work="String Quartet No. 6", key="B-flat major", cat="Op. 18 No. 6", perf=MSQ,
         src="String Quartets/Beethoven String Quartet in B flat Major Op 18",
         mov=["Allegro con brio", "Adagio ma non troppo", "Scherzo: Allegro",
              "La malinconia: Adagio – Allegretto quasi allegro"],
         ref="https://en.wikipedia.org/wiki/String_Quartet_No._6_(Beethoven)"),
    dict(composer="Alexander Borodin", surname="Borodin",
         work="String Quartet No. 1", key="A major", cat="", perf=MSQ,
         src="String Quartets/Borodin String Quartet No 1",
         mov=["Moderato – Allegro", "Andante con moto", "Scherzo: Prestissimo",
              "Andante – Allegro risoluto"],
         ref="https://imslp.org/wiki/String_Quartet_No.1_(Borodin,_Aleksandr)",
         note="Scherzo abridged in this recording, per IMSLP"),
    dict(composer="Alexander Borodin", surname="Borodin",
         work="String Quartet No. 2", key="D major", cat="", perf=MSQ,
         src="String Quartets/Borodin String Quartet No 2",
         mov=["Allegro moderato", "Scherzo: Allegro", "Notturno: Andante",
              "Finale: Andante – Vivace"],
         ref="https://en.wikipedia.org/wiki/String_Quartet_No._2_(Borodin)"),
    dict(composer="Antonín Dvořák", surname="Dvořák",
         work="String Quartet No. 12", key="F major", cat="Op. 96", perf=MSQ,
         src="String Quartets/Dvorak - American in F major",
         mov=["Allegro ma non troppo", "Lento", "Molto vivace",
              "Finale: Vivace ma non troppo"],
         ref="https://en.wikipedia.org/wiki/String_Quartet_No._12_(Dvo%C5%99%C3%A1k)"),
    dict(composer="Antonín Dvořák", surname="Dvořák",
         work="String Quartet No. 10", key="E-flat major", cat="Op. 51", perf=MSQ,
         src="String Quartets/Dvorak Quartet in F Major Op 51",
         mov=["Allegro ma non troppo", "Dumka: Andante con moto – Vivace",
              "Romanza: Andante con moto", "Finale: Allegro assai"],
         ref="https://en.wikipedia.org/wiki/String_Quartet_No._10_(Dvo%C5%99%C3%A1k)"),
    dict(composer="Joseph Haydn", surname="Haydn",
         work="String Quartet", key="D major", cat="Op. 64 No. 5, Hob. III:63", perf=MSQ,
         src="String Quartets/Haydn Quartet in D Major Op.64",
         mov=["Allegro moderato", "Adagio cantabile", "Menuetto: Allegretto",
              "Finale: Vivace"],
         ref="https://en.wikipedia.org/wiki/String_Quartets,_Op._64_(Haydn)"),
    dict(composer="Felix Mendelssohn", surname="Mendelssohn",
         work="String Quartet No. 6", key="F minor", cat="Op. 80", perf=MSQ,
         src="String Quartets/Mendelssohn Quartet in F Minor Op 80",
         mov=["Allegro vivace assai", "Allegro assai", "Adagio", "Finale: Allegro molto"],
         ref="https://en.wikipedia.org/wiki/String_Quartet_No._6_(Mendelssohn)"),
    dict(composer="Wolfgang Amadeus Mozart", surname="Mozart",
         work="String Quartet No. 15", key="D minor", cat="K. 421", perf=MSQ,
         src="String Quartets/Mozart Quartet D Minor K421",
         mov=["Allegro moderato", "Andante", "Menuetto: Allegretto",
              "Allegretto ma non troppo – Più allegro"],
         ref="https://en.wikipedia.org/wiki/String_Quartet_No._15_(Mozart)"),
    dict(composer="Wolfgang Amadeus Mozart", surname="Mozart",
         work="String Quartet No. 19", key="C major", cat="K. 465", perf=MSQ,
         src="String Quartets/Mozart Quartet in C Major K 465 ",
         mov=["Adagio – Allegro", "Andante cantabile", "Menuetto: Allegro", "Allegro molto"],
         ref="https://en.wikipedia.org/wiki/String_Quartet_No._19_(Mozart)"),
    dict(composer="Josef Suk", surname="Suk",
         work="Meditation on the Old Czech Chorale 'St. Wenceslas'", key="", cat="Op. 35a",
         perf=MSQ, src="String Quartets/Suk -Meditation", mov=[None],
         ref="https://imslp.org/wiki/Meditation_on_the_Old_Czech_Chorale_'St._Wenceslas',_Op.35a_(Suk,_Josef)"),
    *[dict(composer="Franz Schubert", surname="Schubert", work="Piano Sonata",
           key=k, cat=c, perf="Paul Pitman", src="Schubert - The Piano Sonatas",
           match=f"{c} -", mov=m, ref=r) for k, c, m, r in [
        ("E-flat major", "D. 568", ["Allegro moderato", "Andante molto",
                                    "Menuetto: Allegretto – Trio", "Allegro moderato"],
         "https://en.wikipedia.org/wiki/Piano_Sonata_in_E-flat_major,_D_568_(Schubert)"),
        ("A major", "D. 664", ["Allegro moderato", "Andante", "Allegro"],
         "https://en.wikipedia.org/wiki/Piano_Sonata_in_A_major,_D_664_(Schubert)"),
        ("A minor", "D. 784", ["Allegro giusto", "Andante", "Allegro vivace"],
         "https://en.wikipedia.org/wiki/Piano_Sonata_in_A_minor,_D_784_(Schubert)"),
        ("A minor", "D. 845", ["Moderato", "Andante poco mosso",
                               "Scherzo: Allegro vivace – Trio: Un poco più lento",
                               "Rondo: Allegro vivace"],
         "https://en.wikipedia.org/wiki/Piano_Sonata_in_A_minor,_D_845_(Schubert)"),
        ("D major", "D. 850", ["Allegro vivace", "Con moto", "Scherzo: Allegro vivace – Trio",
                               "Rondo: Allegro moderato"],
         "https://en.wikipedia.org/wiki/Piano_Sonata_in_D_major,_D_850_(Schubert)"),
        ("C minor", "D. 958", ["Allegro", "Adagio", "Menuetto: Allegro – Trio", "Allegro"],
         "https://en.wikipedia.org/wiki/Piano_Sonata_in_C_minor,_D_958_(Schubert)"),
        ("A major", "D. 959", ["Allegro", "Andantino",
                               "Scherzo: Allegro vivace – Trio: Un poco più lento",
                               "Rondo: Allegretto – Presto"],
         "https://en.wikipedia.org/wiki/Piano_Sonata_in_A_major,_D_959_(Schubert)"),
    ]],
    dict(composer="Johann Sebastian Bach", surname="Bach",
         work="Goldberg Variations", key="G major", cat="BWV 988", perf="Shelley Katz",
         src="Goldberg Variations", mov=GOLDBERG, numbered=False,
         ref="https://en.wikipedia.org/wiki/Goldberg_Variations"),
]

# ---- Recordings from outside the Musopen zip ---------------------------------
# Each names its own licence, source and files. A file is streamed from `url`; the local
# copy is fetched from `get` (converted to MP3 if it is not one). `perf` on a file names
# that track's performer when the work has several. Licences checked Oct 2026:
#
# Moonlight: Paul Pitman for Musopen. Commons: "Recording: {{PD-author}}" with Wikimedia
#   VRT permission ticket 2008012110017088 (Musopen's release), on all three files.
# Clair de lune: Laurens Goedhart, 2011. Commons: "recording={{cc-by-3.0}}"; the permission
#   is an archived copy of his SoundCloud page ("licensed under a Creative Commons License",
#   linking CC BY 3.0). CC BY: credit him, link the licence, say we converted it to MP3.
# Nocturnes: Musopen's "Set Chopin Free" Kickstarter (2013), released as public domain.
#   archive.org item licenseurl CC0 1.0 (a 2026 re-upload of Musopen's set, publisher
#   Musopen); Commons tags the same performances {{PD-author|Musopen}}, citing Musopen's
#   Kickstarter post 1193714. Performers from each file's tags, matching Commons.
COMMONS = "https://commons.wikimedia.org/wiki/File:"
UPLOAD = "https://upload.wikimedia.org/wikipedia/commons/"


def commons(path, name):
    """Stream from Commons' MP3 transcode (plays everywhere, sends CORS); keep the original."""
    return dict(url=f"{UPLOAD}transcoded/{path}/{name}/{name}.mp3", get=f"{UPLOAD}{path}/{name}",
                page=COMMONS + name)


MOONLIGHT_I = "Ludwig_van_Beethoven_-_sonata_no._14_in_c_sharp_minor_%27moonlight%27%2C_op._27_no._2_-_i._adagio_sostenuto.ogg"
CLAIR = "Clair_de_lune_%28Claude_Debussy%29_Suite_bergamasque.ogg"
CHOPIN_ITEM = "musopen-chopin-complete-works-flac"
CHOPIN_DL = f"https://archive.org/download/{CHOPIN_ITEM}/"


def chopin(name, perf):
    url = CHOPIN_DL + name.replace(" ", "%20").replace(",", "%2C")
    return dict(url=url, get=url, perf=perf, page=f"https://archive.org/details/{CHOPIN_ITEM}")


WORKS += [
    dict(composer="Ludwig van Beethoven", surname="Beethoven",
         work="Piano Sonata No. 14 'Moonlight'", key="C-sharp minor", cat="Op. 27 No. 2",
         perf="Paul Pitman", mov=["Adagio sostenuto", "Allegretto", "Presto agitato"],
         files=[commons("4/48", MOONLIGHT_I), commons("f/f5", "Moonlight_Sonata_Allegretto.ogg"),
                commons("1/1d", "Moonlight_Sonata_Presto.ogg")],
         licence="Public domain", licence_url=COMMONS + MOONLIGHT_I,
         source=COMMONS + MOONLIGHT_I,
         credit="Paul Pitman for Musopen, released to the public domain; via Wikimedia Commons.",
         ref="https://en.wikipedia.org/wiki/Piano_Sonata_No._14_(Beethoven)"),
    dict(composer="Claude Debussy", surname="Debussy",
         work="Suite bergamasque: Clair de lune", key="D-flat major", cat="L. 75",
         perf="Laurens Goedhart", mov=["Andante très expressif"], numbered=False,
         files=[commons("b/be", CLAIR)],
         licence="CC BY 3.0", licence_url="https://creativecommons.org/licenses/by/3.0/",
         source=COMMONS + CLAIR,
         credit="“Clair de lune” played by Laurens Goedhart (2011), CC BY 3.0, via Wikimedia Commons; "
                "converted to MP3.",
         ref="https://en.wikipedia.org/wiki/Suite_bergamasque"),
    dict(composer="Frédéric Chopin", surname="Chopin",
         work="Nocturnes", key="", cat="Op. 9 Nos. 1–3, Op. 27 No. 2, Op. 48 No. 1",
         perf="Olga Gurevich, Frank Levy, Xuan He, Luke Faulkner", numbered=False,
         # src for the markings: IMSLP (Op. 9) and the Op. 27 and Op. 48 Wikipedia pages
         mov=["Op. 9 No. 1 in B-flat minor: Larghetto", "Op. 9 No. 2 in E-flat major: Andante",
              "Op. 9 No. 3 in B major: Allegretto", "Op. 27 No. 2 in D-flat major: Lento sostenuto",
              "Op. 48 No. 1 in C minor: Lento"],
         files=[chopin("Nocturne in B flat minor, Op. 9 no. 1.mp3", "Olga Gurevich"),
                chopin("Nocturne in E flat major, Op. 9 no. 2.mp3", "Frank Levy"),
                chopin("Nocturne in B major, Op. 9 no. 3.mp3", "Xuan He"),
                chopin("Nocturne in D flat major, Op. 27 no. 2.mp3", "Frank Levy"),
                chopin("Nocturne in C minor, Op. 48 no. 1.mp3", "Luke Faulkner")],
         licence="CC0 1.0", licence_url="https://creativecommons.org/publicdomain/zero/1.0/",
         source=f"https://archive.org/details/{CHOPIN_ITEM}",
         credit="Musopen’s “Set Chopin Free” recordings (2013), CC0, via the Internet Archive.",
         ref="https://en.wikipedia.org/wiki/Nocturnes_(Chopin)"),
]


def album(w):
    s = w["work"]
    if w["key"]:
        s += f" in {w['key']}"
    if w["cat"]:
        s += f", {w['cat']}"
    return s


# ---- History notes, shown while the music plays ----------------------------
# Keyed by album(w). "work" shows as the first movement starts; movement notes
# are keyed by track number. Each note is under ~40 words.
#
# at: "start" (a few seconds in) | "after:N" (N seconds in) | "frac:F" (F of the
#     track) | "climax" (loudest passage) | "surge" (biggest rise from quiet to
#     loud) | "hush" (quietest stretch) | "end" (about a minute before the end).
#     Anything but "start"/"after" is resolved from the recording by
#     tools/note_timing.py and marked "check by ear".
# unsure: why a note needs checking (a claim not confirmed in the fetched source).
#
# Sources: the "ref" page of each work (Wikipedia or IMSLP, fetched Oct 2026)
# unless a comment names another.

def N(text, at="start", unsure=None):
    return dict(text=text, at=at, unsure=unsure)


W = "https://en.wikipedia.org/wiki/"
NOTES = {
    "Symphony No. 3 in E-flat major, Op. 55": dict(
        # src: W+"Symphony_No._3_(Beethoven)" (History: Napoleon, Ries's account, 1806 title)
        work=N("Composed mainly in 1803–04 with Napoleon in mind. When Napoleon crowned himself "
               "emperor in 1804, Beethoven reportedly tore the title page in half. It was published "
               "in 1806 as Sinfonia eroica."),
        movements={
            # src: same page (I. form; the "early" horn, mm. 394–395)
            1: [N("Two sharp chords, then the cellos give out the theme. This vast movement grows from "
                  "that plain rising arpeggio."),
                N("Near the end of the development a horn seems to come in early with the main theme "
                  "under the violins: a famous 'mistake' that Beethoven meant.", at="frac:0.56")],
            # src: same page (II. Marcia funebre)
            2: [N("A funeral march in C minor: a ternary march, large and amply developed, its main "
                  "theme returning like a refrain.")],
            # src: same page (III. trio)
            3: [N("A lively scherzo. In the trio, listen for three horns: the first time a symphony had "
                  "used three.", at="frac:0.45")],
            # src: same page (IV. Prometheus theme)
            4: [N("The finale's theme comes from Beethoven's own ballet The Creatures of Prometheus, about "
                  "the Titan who brought fire to humankind.")],
        }),

    "Symphony No. 1 in C minor, Op. 68": dict(
        # src: W+"Symphony_No._1_(Brahms)" (History; Bülow quote)
        work=N("Brahms worked on this symphony for about 21 years, from sketches in 1855 to the premiere "
               "in Karlsruhe on 4 November 1876. Hans von Bülow called it 'Beethoven's Tenth'."),
        movements={
            1: [N("The introduction climbs and falls against a pounding low C in the timpani, Brahms "
                  "announcing his symphony under Beethoven's shadow.",
                  unsure="timpani pedal not stated on the fetched page")],
            # src: same page (Andante sostenuto; long violin solo)
            2: [N("A tender Andante in E major, far from C minor. Near the end a long violin solo "
                  "recalls Beethoven's late quartets and Missa Solemnis.", at="end")],
            3: [N("Instead of a Beethoven-style scherzo, a gentle intermezzo: 'a little allegretto, "
                  "graceful'.")],
            # src: same page (1868 card to Clara Schumann)
            4: [N("The horn call: in September 1868 Brahms sent this alphorn tune to Clara Schumann "
                  "on a card. 'Thus blew the shepherd's horn today!'", at="frac:0.17"),
                N("Then the broad string tune of the Allegro. Its kinship with Beethoven's 'Ode to Joy' "
                  "is part of why it was called 'Beethoven's Tenth'.", at="frac:0.3",
                  unsure="the Ode to Joy likeness is not on the fetched page")],
        }),

    "Symphony No. 2 in D major, Op. 73": dict(
        # src: W+"Symphony_No._2_(Brahms)" (composition; letter of 22 Nov 1877)
        work=N("Written in summer 1877 at Pörtschach on the Wörthersee. Brahms told his publisher it was "
               "'so melancholy that you will not be able to bear it'. It is among his sunniest works."),
        movements={
            # src: same page (bar 82, the "Lullaby" theme)
            1: [N("It opens with a three-note turn in the low strings, answered by horns. Much of the "
                  "symphony grows from it.", unsure="the three-note motif is not described on the fetched page"),
                N("Violas and cellos now sing a second theme close to Brahms's famous Lullaby.", at="frac:0.12")],
            # src: same page (movement list: B major)
            2: [N("Adagio non troppo, in B major: the most searching movement, opening with a long, "
                  "wandering cello melody.")],
            3: [N("A gentle dance in G major led by the oboe, twice interrupted by quicker Presto episodes "
                  "built from the same tune.", unsure="the oboe lead is not stated on the fetched page")],
            # src: same page (instrumentation: trombones, tuba)
            4: [N("Allegro con spirito: it builds to a jubilant D-major ending, trombones and tuba "
                  "blazing.", at="end")],
        }),

    "Symphony No. 3 in F major, Op. 90": dict(
        # src: W+"Symphony_No._3_(Brahms)" (composition, Frei aber froh, premiere)
        work=N("Written in summer 1883 at Wiesbaden. Brahms, 50 and a bachelor, called himself 'Frei "
               "aber froh', free but happy. Hans Richter premiered it in Vienna on 2 December 1883."),
        movements={
            # src: same page (F–A–F motto)
            1: [N("Listen for the motto F–A–F in the opening chords. It runs through the whole symphony, "
                  "often read as Brahms's 'free but happy'.")],
            # src: same page (movement list: Andante, C major)
            2: [N("A quiet Andante in C major, opening with clarinets and bassoons like a hymn.",
                  unsure="the wind scoring of the opening is not stated on the fetched page")],
            # src: same page (movement list: Poco allegretto, C minor)
            3: [N("Poco allegretto in C minor: the cellos sing one of Brahms's best-known melodies, "
                  "later taken up by the horn.", unsure="the horn reprise is not stated on the fetched page")],
            # src: same page (finale fades to a quiet ending)
            4: [N("The finale storms in F minor, then dissolves: the symphony ends quietly, the motto "
                  "settling into F major.", at="end")],
        }),

    "Symphony No. 4 in E minor, Op. 98": dict(
        # src: W+"Symphony_No._4_(Brahms)" (Mürzzuschlag 1884; Meiningen premiere)
        work=N("Begun in 1884 at Mürzzuschlag in the Austrian Alps. Brahms conducted the premiere in "
               "Meiningen on 25 October 1885. It was his last symphony."),
        movements={
            # src: same page (chain of descending thirds)
            1: [N("The violins open with a chain of falling thirds, sighing two notes at a time.")],
            # src: same page (E Phrygian theme)
            2: [N("Horns announce the theme in the old Phrygian church mode before the strings warm it "
                  "into E major.")],
            # src: same page (the only scherzo-like movement; triangle)
            3: [N("The only scherzo-like movement in Brahms's symphonies, and the only one with a "
                  "triangle. Listen for it.")],
            # src: same page (passacaglia; theme adapted from Bach's BWV 150)
            4: [N("A passacaglia: variations over a repeating theme that Brahms adapted from the "
                  "closing chaconne of Bach's cantata BWV 150."),
                N("The variations gather to their climax: the Baroque form carrying Brahms's darkest "
                  "symphonic ending.", at="climax")],
        }),

    "Symphony No. 6 in B minor, Op. 74": dict(
        # src: W+"Symphony_No._6_(Tchaikovsky)" (written Feb–Aug 1893 at Klin; premiere nine days before death)
        work=N("Written between February and August 1893 in a small house in Klin. Tchaikovsky "
               "conducted the premiere in Saint Petersburg nine days before he died."),
        movements={
            1: [N("It begins in near darkness: a lone bassoon, low, over divided double basses.",
                  unsure="the opening bassoon solo is not described on the fetched page"),
                N("After the second theme fades almost to nothing, the full orchestra crashes in: one of "
                  "the most startling entries in the symphonic repertoire.", at="surge")],
            # src: same page (5/4, 'limping' waltz)
            2: [N("A waltz with five beats to the bar, described as 'limping': graceful, but never "
                  "quite settling.")],
            # src: same page (scherzo, march-like)
            3: [N("A playful scherzo that turns into a march and drives to a triumphant close.",
                  at="frac:0.6")],
            # src: same page (ends very quietly)
            4: [N("Instead of a fast finale, an Adagio lamentoso. The symphony ends very quietly, "
                  "sinking into the low strings.", at="end")],
        }),

    "String Quartet No. 6 in B-flat major, Op. 18 No. 6": dict(
        # src: W+"String_Quartet_No._6_(Beethoven)"; W+"String_Quartets,_Op._18_(Beethoven)"
        work=N("Written 1798–1800 on a commission from Prince Lobkowitz and published in 1801: the last "
               "of Beethoven's first six quartets, composed in his late twenties in Vienna."),
        movements={
            1: [N("Allegro con brio: a quick, bright conversation tossed between first violin and cello.")],
            2: [N("A gentle Adagio in E-flat major, the quartet's quietest movement.")],
            # src: same page ('tour de force of syncopation')
            3: [N("A 'tour de force of syncopation': listen for accents that keep landing where the "
                  "beat isn't.")],
            # src: same page ('La Malinconia', delicacy marking)
            4: [N("'La Malinconia', melancholy. Beethoven marked it to be played 'with the greatest "
                  "delicacy'. It alternates with a carefree dance until the two collide.")],
        }),

    "String Quartet No. 1 in A major": dict(
        # src: imslp.org String_Quartet_No.1_(Borodin,_Aleksandr) (dates, dedication, premiere, Beethoven link)
        work=N("Composed 1874–79 and first played in Saint Petersburg on 30 December 1880. Its subtitle, "
               "'On a theme of Beethoven', comes from borrowings from the finale of Beethoven's Op. 130."),
        movements={
            # src: W+"Alexander_Borodin" (professor of chemistry; composed in his spare time)
            1: [N("Borodin was a professor of chemistry who composed in his spare time; this movement "
                  "weaves in Beethoven's theme.")],
            # src: IMSLP (Andante con moto, F-sharp minor, fugato)
            2: [N("Andante con moto in F-sharp minor, with a fugato at its heart.")],
            # src: IMSLP (file description: Scherzo abridged)
            3: [N("Scherzo: Prestissimo. This recording plays it abridged.")],
            # src: IMSLP (Andante – Allegro risoluto, A minor; Op. 130 elements)
            4: [N("A slow Andante opening, then Allegro risoluto, returning to the Beethoven-derived "
                  "material.")],
        }),

    "String Quartet No. 2 in D major": dict(
        # src: W+"String_Quartet_No._2_(Borodin)" (1881, Zhitovo, dedication, Dianin)
        work=N("Written in 1881 at a friend's estate at Zhitovo and dedicated to his wife, Ekaterina "
               "Protopopova. It may be a 20th-anniversary gift recalling how they met in Heidelberg."),
        movements={
            # src: same page (cello opens with a lyrical melody in high register)
            1: [N("The cello opens with a lyrical melody high in its register.")],
            2: [N("Scherzo: Allegro, light and quick, a brief breath before the famous Notturno.")],
            # src: same page (Notturno the most famous movement)
            3: [N("The Notturno, the quartet's most famous movement: the cello sings the long melody, "
                  "later answered by the first violin.")],
            4: [N("Finale: a slow question-and-answer opening, then off at a Vivace.")],
        }),

    "String Quartet No. 12 in F major, Op. 96": dict(
        # src: W+"String_Quartet_No._12_(Dvořák)" (Spillville, 10 June 1893, Haydn quote)
        work=N("Written in 1893 in Spillville, a Czech community in Iowa, on a summer break from New York. "
               "'Dear Papa Haydn kept appearing before my eyes,' Dvořák said, 'so it turned out so simple.'"),
        movements={
            # src: same page (pentatonic scale)
            1: [N("The viola opens with the main theme over shimmering violins. The pentatonic scale, "
                  "used throughout, gives the quartet its open sound.",
                  unsure="the viola opening is not stated on the fetched page")],
            2: [N("Lento: a long, aching melody for the first violin, later taken by the cello.")],
            # src: same page (bird song transcription; tanager questioned)
            3: [N("Listen for a high, interrupting strain in the first violin: a bird Dvořák heard in "
                  "Spillville. He thought it a scarlet tanager; it may have been a vireo.", at="frac:0.4")],
            4: [N("Finale: a steady, chugging rhythm drives it. Dvořák was a lifelong railway enthusiast.",
                  unsure="the railway link is only a page category on the fetched page")],
        }),

    "String Quartet No. 10 in E-flat major, Op. 51": dict(
        # src: W+"String_Quartet_No._10_(Dvořák)" (Becker, 'Slavonic', Joachim Quartet 1879)
        work=N("Written in 1879 for Jean Becker of the Florentine Quartet, who asked for a 'Slavonic' "
               "quartet after the success of the Slavonic Dances. The Joachim Quartet first played it in Berlin."),
        movements={
            1: [N("Allegro ma non troppo: a relaxed opening with a rocking, dance-like lilt.")],
            # src: same page (dumka gives the Slavonic character)
            2: [N("A dumka, the Slavonic lament that turns from sorrow to quick dance and back. It gives "
                  "the quartet its Slavonic character.")],
            3: [N("Romanza: a warm, song-like slow movement.")],
            # src: same page (Šourek: stylisation of the Czech skočná)
            4: [N("A stylisation of the Czech skočná, a fast leaping dance.")],
        }),

    "String Quartet in D major, Op. 64 No. 5, Hob. III:63": dict(
        # src: W+"String_Quartets,_Op._64_(Haydn)" (1790; Tost quartets)
        work=N("One of six quartets composed in 1790, known as the Tost quartets after the violinist "
               "Johann Tost, who helped Haydn find a publisher."),
        movements={
            1: [N("The nickname comes from the first violin's melody, which soars high above the others "
                  "like a lark.", at="after:12")],   # nickname origin: well established (confirmed by Jeem)
            # src: same page (Adagio cantabile in A major)
            2: [N("Adagio cantabile, in A major: a simple, singing melody, ornamented by the first violin.")],
            3: [N("Menuetto: Allegretto, a courtly dance with a darker trio.",
                  unsure="the trio's character is not described on the fetched page")],
            4: [N("Finale: a perpetual motion of rapid notes, with a fugal passage in the middle.",
                  unsure="the fugal middle is not described on the fetched page")],
        }),

    "String Quartet No. 6 in F minor, Op. 80": dict(
        # src: W+"String_Quartet_No._6_(Mendelssohn)" (1847; Fanny; last major work)
        work=N("Composed in 1847 after his sister Fanny died on 14 May, as a homage to her. It was the "
               "last major work he completed. He died two months later, on 4 November."),
        movements={
            1: [N("Allegro vivace assai: tremolos and shuddering accents, grief without consolation.")],
            2: [N("Allegro assai: an obsessive, syncopated scherzo that never relaxes.")],
            3: [N("Adagio: the one place of consolation in the quartet.")],
            4: [N("Finale: restless to the end, with no turn to the major.")],
        }),

    "String Quartet No. 15 in D minor, K. 421": dict(
        # src: W+"String_Quartet_No._15_(Mozart)" (c. June 1783; Constanze's account to the Novellos,
        # 1829; "the only one of the set in a minor key")
        work=N("Completed in 1783. In 1829 Constanze told the Novellos he wrote it while she was in "
               "labour with their first child, Raimund. The only minor-key quartet of the six for Haydn."),
        movements={
            1: [N("Allegro moderato: a quiet, troubled opening in D minor.")],
            2: [N("Andante, in F major: calm, but broken by sudden sighing pauses.")],
            # src: same page (Irving on the trio)
            3: [N("A dark Menuetto. Its major-key trio is almost lightweight, 'a wonderful foil' to the "
                  "minuet.", at="frac:0.45")],
            # src: same page (variations; Picardy third)
            4: [N("A set of variations, ending on a Picardy third: a final D-major chord after a "
                  "D-minor journey.", at="end")],
        }),

    "String Quartet No. 19 in C major, K. 465": dict(
        # src: W+"String_Quartet_No._19_(Mozart)" (14 Jan 1785; Haydn set; 1787 complaint)
        work=N("Completed on 14 January 1785, the last of the six quartets Mozart dedicated to Joseph "
               "Haydn."),
        movements={
            # src: same page (22-bar Adagio; quiet Cs in the cello)
            1: [N("The 22-bar slow introduction gave the 'Dissonance' its name: quiet repeated Cs in the "
                  "cello, then harmonies strange enough that a critic complained in print in 1787."),
                N("Then the Allegro breaks into clear C major.", at="frac:0.22")],
            2: [N("Andante cantabile, in F major: a singing, unhurried slow movement.")],
            # src: same page (trio in C minor)
            3: [N("Menuetto: Allegro. Its trio turns to C minor.", at="frac:0.5")],
            4: [N("Allegro molto: a quick-witted finale.")],
        }),

    "Meditation on the Old Czech Chorale 'St. Wenceslas', Op. 35a": dict(
        # src: imslp.org Meditation_on_the_Old_Czech_Chorale_..._(Suk,_Josef) (dedication; scoring);
        # 1914, patriotic purpose and wartime meaning confirmed by Jeem
        work=N("Written in 1914 as a patriotic piece on the old Czech chorale 'St Wenceslas', for string "
               "quartet or string orchestra. It became a wartime symbol of hope. Dedicated to Ferdinand Pečírka."),
        movements={
            1: [N("The chorale to the Czech patron saint builds to its fullest sound: in the war years, "
                  "a hymn of hope.", at="climax")],
        }),

    "Piano Sonata in E-flat major, D. 568": dict(
        # src: W+"Piano_Sonata_in_E-flat_major,_D_568_(Schubert)" (D-flat version 1817; E-flat published 1829)
        work=N("First drafted in D-flat major in June 1817, when Schubert was 20. He revised and finished "
               "it in E-flat; it was published in 1829, the year after his death."),
        movements={
            1: [N("Allegro moderato: a gentle, singing opening theme, unhurried even when it develops.")],
            2: [N("Andante molto: a slow, sorrowful song in G minor.")],   # key confirmed by Jeem
            3: [N("Menuetto: a graceful dance with a contrasting trio.")],
            4: [N("Allegro moderato: a relaxed, flowing finale.")],
        }),

    "Piano Sonata in A major, D. 664": dict(
        # src: W+"Piano_Sonata_in_A_major,_D_664_(Schubert)" (summer 1819; Josephine von Koller)
        work=N("Written in summer 1819 in Steyr, Upper Austria, and dedicated to 18-year-old Josephine von "
               "Koller, whom Schubert thought 'very pretty' and 'a good pianist'."),
        movements={
            1: [N("Allegro moderato: one of Schubert's most lyrical openings, a melody that seems to "
                  "sing itself.")],
            # src: same page (Andante in D major)
            2: [N("Andante, in D major: quiet and inward.")],
            3: [N("Allegro: a light, dancing finale.")],
        }),

    "Piano Sonata in A minor, D. 784": dict(
        # src: W+"Piano_Sonata_in_A_minor,_D_784_(Schubert)" (Feb 1823; illness; published 1839)
        work=N("Composed in February 1823, perhaps in response to the serious illness of the year before. "
               "It was not published until 1839, eleven years after his death."),
        movements={
            1: [N("Allegro giusto: bare octaves, stark and spacious, unlike the songful Schubert of earlier "
                  "sonatas.")],
            # src: same page (Andante in F major)
            2: [N("Andante, in F major: a hushed hymn interrupted by murmuring figures.")],
            3: [N("Allegro vivace: a fierce, driving finale.")],
        }),

    "Piano Sonata in A minor, D. 845": dict(
        # src: W+"Piano_Sonata_in_A_minor,_D_845_(Schubert)" (May 1825; Première Grande Sonate)
        work=N("Composed in May 1825 and published as his 'Première Grande Sonate', the first of only "
               "three Schubert sonatas printed in his lifetime."),
        movements={
            1: [N("Moderato: it opens with a soft, questioning unison phrase.")],
            # src: same page (five variations on a 32-bar theme)
            2: [N("Five variations on a simple 32-bar theme.")],
            3: [N("Scherzo: Allegro vivace, with a slower trio, 'un poco più lento'.")],
            4: [N("Rondo: Allegro vivace, a restless finale.")],
        }),

    "Piano Sonata in D major, D. 850": dict(
        # src: W+"Piano_Sonata_in_D_major,_D_850_(Schubert)" (August 1825, Bad Gastein)
        work=N("Written in August 1825 at the spa town of Bad Gastein, hence its nickname, the 'Gasteiner'."),
        movements={
            1: [N("Allegro vivace: big, bright chords that fill the piano.")],
            2: [N("Con moto: a long, slow-walking movement.")],
            3: [N("Scherzo: Allegro vivace, full of rhythmic energy.")],
            # src: same page (march-like rondo theme with stormy episodes)
            4: [N("A playful, march-like rondo theme, repeated with ever finer decoration and "
                  "interrupted by stormier episodes.")],
        }),

    "Piano Sonata in C minor, D. 958": dict(
        # src: W+"Piano_Sonata_in_C_minor,_D_958_(Schubert)" (last three sonatas, 1828)
        work=N("One of three sonatas written in the last months of Schubert's life, finished in "
               "September 1828. He died that November, at 31."),
        movements={
            # src: same page (quotes Beethoven's 32 Variations in C minor)
            1: [N("The opening bars quote the theme of Beethoven's 32 Variations in C minor. Schubert "
                  "deeply admired Beethoven.")],
            # src: same page (ABABA slow movement)
            2: [N("Adagio, in A-flat major: two ideas alternate, five sections in all.")],
            # src: same page (subdued minuet in place of a scherzo)
            3: [N("Instead of a scherzo, a subdued minuet.")],
            # src: same page (tarantella)
            4: [N("A relentless tarantella, galloping with hand-crossings and leaps across the keyboard.")],
        }),

    "Piano Sonata in A major, D. 959": dict(
        # src: same Wikipedia article as D 958 (1828; published 1839, dedicated to Schumann)
        work=N("Written in 1828, the last year of Schubert's life. When it was finally published in 1839, "
               "the dedication went to Robert Schumann, who had championed his music."),
        movements={
            1: [N("Allegro: a grand opening of full chords.")],
            # src: same article (F-sharp minor, ABA; improvisatory middle)
            2: [N("Andantino, in F-sharp minor: a quiet, rocking song.", at="start"),
                N("The middle section erupts: improvisatory, with harsh modulations, peaking in "
                  "fortissimo chords.", at="climax")],
            3: [N("Scherzo: Allegro vivace, with a gentler trio.")],
            4: [N("Rondo: Allegretto. The broad, singing theme returns again and again.")],
        }),

    "Goldberg Variations in G major, BWV 988": dict(
        # src: W+"Goldberg_Variations" (1741; Forkel's account, questioned)
        work=N("Published in 1741. Forkel's 1802 biography says Bach wrote it for Count Kaiserling, whose "
               "insomnia young Goldberg soothed from an antechamber. Historians question the story."),
        movements={
            # src: same page (1725 notebook; ground bass)
            1: [N("The Aria also survives in the 1725 notebook for Anna Magdalena Bach. Its bass line, "
                  "not its melody, carries all thirty variations.", at="after:20")],
            # src: same page (every third variation is a canon)
            4: [N("Every third variation is a canon, the interval widening each time. This first one is "
                  "at the unison.")],
            # src: same page (Variation 16 is headed Ouverture)
            17: [N("Halfway through, Variation 16 begins the second half as a French overture.")],
            # src: same page (Landowska's 'black pearl')
            26: [N("Wanda Landowska called this slow G-minor variation 'the black pearl' of the set.")],
            # src: same page (Quodlibet instead of a canon at the tenth)
            31: [N("Instead of a canon at the tenth, a quodlibet: popular tunes woven together over "
                   "the bass.")],
            32: [N("The Aria returns unchanged, but it sounds different after everything in between.")],
        }),

    # ---- From other sources (see the licence notes above WORKS += [...]) --------
    "Piano Sonata No. 14 'Moonlight' in C-sharp minor, Op. 27 No. 2": dict(
        # src: W+"Piano_Sonata_No._14_(Beethoven)" (1801; dedication 1802; Rellstab; quasi una fantasia)
        work=N("Completed in 1801 and dedicated to his pupil Countess Julie 'Giulietta' Guicciardi. "
               "Beethoven titled it Sonata quasi una fantasia; 'Moonlight' came later, from the poet "
               "Ludwig Rellstab's imagery."),
        movements={
            # src: same page (I.; the pedal direction; pp throughout, never above p)
            1: [N("Beethoven asked for the whole movement to be played 'with the utmost delicacy and "
                  "without dampers'. It never rises above piano."),
                # src: same page (Czerny's description; "Surely I've written better things")
                N("Czerny heard 'a mournful ghostly voice' from the distance. Beethoven, tired of this "
                  "movement's popularity, told him: 'Surely I've written better things'.", at="frac:0.55")],
            # src: same page (II. minuet, D-flat major, shortest; Liszt "is said to have")
            2: [N("A minuet in D-flat major, the shortest movement. Liszt is said to have called it 'a "
                  "flower between two abysses'.")],
            # src: same page (III. the weightiest movement, placed last; Rosen)
            3: [N("Presto agitato: the stormy finale, the weightiest of the three. Beethoven held the "
                  "fast music back until the end."),
                # (fixed time: the movement is loud throughout, so there is no single climax)
                N("Charles Rosen: 'Even today, two hundred years later, its ferocity is astonishing.'",
                  at="after:120")],
        }),

    "Suite bergamasque: Clair de lune in D-flat major, L. 75": dict(
        # src: W+"Suite_bergamasque" (begun c. 1890, revised for 1905; Promenade sentimentale; Verlaine)
        work=N("The third of four pieces in Debussy's Suite bergamasque, begun around 1890 and revised "
               "before publication in 1905. It was first called 'Promenade sentimentale'."),
        movements={
            # src: same page (title from Verlaine's poem; andante très expressif; 9/8)
            1: [N("Its title is that of a poem by Paul Verlaine. Marked andante très expressif, in "
                  "D-flat major, nine quavers to the bar."),
                # src: same page (Fantasia: cut for runtime; footage reused for "Blue Bayou")
                N("Disney planned it for Fantasia (1940) but cut it for length. Its heron footage became "
                  "'Blue Bayou' in Make Mine Music.", at="frac:0.6")],
        }),

    "Nocturnes, Op. 9 Nos. 1–3, Op. 27 No. 2, Op. 48 No. 1": dict(
        # src: W+"Nocturnes_(Chopin)" (21 nocturnes; Field), W+"Nocturnes,_Op._9_(Chopin)" (first set; Pleyel)
        work=N("Chopin wrote 21 nocturnes, taking the form from the Irish composer John Field. Op. 9, "
               "dedicated to Marie Pleyel, was his first published set."),
        movements={
            # src: W+"Nocturnes,_Op._9_(Chopin)" (No. 1: free right hand; groups of 7, 11, 20, 22)
            1: [N("Olga Gurevich plays. The left hand rolls steady arpeggios while the right hand floats "
                  "free, in runs of seven, eleven, even twenty-two notes."),
                # src: same page (melody over 17 bars of D-flat major chords; Picardy third)
                N("Before the return, the melody floats over seventeen bars of D-flat major chords. The "
                  "close turns to major.", at="frac:0.72")],
            # src: same page (No. 2: often called his most famous piece; about twenty; ornamented returns)
            2: [N("Frank Levy plays the nocturne often called Chopin's most famous piece, written when he "
                  "was about twenty. Each return of the melody is more ornamented."),
                # src: same page (penultimate bar: senza tempo)
                N("Near the end, a passage marked senza tempo: 'without tempo'.", at="end")],
            # src: same page (No. 3: Allegretto, chromatic; Agitato in B minor)
            3: [N("Xuan He plays. Allegretto: a chromatic theme with a nostalgic energy, full of "
                  "coloratura ornaments."),
                N("The agitato in B minor: melody and counter-melody in the right hand over running "
                  "left-hand arpeggios.", at="surge")],
            # src: W+"Nocturnes,_Op._27_(Chopin)" (1836; Countess d'Appony; two strophes; second voice)
            4: [N("Frank Levy plays. Composed in 1836 and dedicated to Countess d'Appony: two strophes in "
                  "ever more elaborate variations, often with a second voice under the melody."),
                # src: same page (Blair Johnston on the main cadence near the end)
                N("The cadence near the end: 'one of the most glorious moments in Chopin's entire output', "
                  "wrote Blair Johnston.", at="end")],
            # src: W+"Nocturnes,_Op._48_(Chopin)" (1841; lento; chorale; doppio movimento; Huneker)
            5: [N("Luke Faulkner plays. Written in 1841: James Huneker called it 'the noblest nocturne of "
                  "them all'."),
                N("The middle begins as a chorale in C major, then breaks into doppio movimento agitato, "
                  "with thundering octaves.", at="surge")],
        }),
}


# ---- Movement keys, for the engraved fragments' key signatures ---------------
# Keyed by album(w), then track number. Movements not listed use the work's home
# key if they are first or last, and no key signature otherwise. Written from the
# movement tables of each work's "ref" page and confirmed by Jeem, Oct 2026.
# Goldberg variations 15, 21 and 25 are in G minor.
MKEYS = {
    "Symphony No. 3 in E-flat major, Op. 55": {2: "C minor", 3: "E-flat major"},
    "Symphony No. 1 in C minor, Op. 68": {2: "E major", 3: "A-flat major"},
    "Symphony No. 2 in D major, Op. 73": {2: "B major", 3: "G major"},
    "Symphony No. 3 in F major, Op. 90": {2: "C major", 3: "C minor"},
    "Symphony No. 4 in E minor, Op. 98": {2: "E major", 3: "C major"},
    "Symphony No. 6 in B minor, Op. 74": {2: "D major", 3: "G major"},
    "String Quartet No. 6 in B-flat major, Op. 18 No. 6": {2: "E-flat major", 3: "B-flat major"},
    "String Quartet No. 2 in D major": {2: "F major", 3: "A major"},
    "String Quartet No. 12 in F major, Op. 96": {2: "D minor", 3: "F major"},
    "String Quartet No. 10 in E-flat major, Op. 51": {2: "G minor", 3: "B-flat major"},
    "String Quartet in D major, Op. 64 No. 5, Hob. III:63": {2: "A major", 3: "D major"},
    "String Quartet No. 6 in F minor, Op. 80": {2: "F minor", 3: "A-flat major"},
    "String Quartet No. 15 in D minor, K. 421": {2: "F major", 3: "D minor"},
    "String Quartet No. 19 in C major, K. 465": {2: "F major", 3: "C major"},
    "Piano Sonata in E-flat major, D. 568": {2: "G minor", 3: "E-flat major"},
    "Piano Sonata in A major, D. 664": {2: "D major"},
    "Piano Sonata in A minor, D. 784": {2: "F major"},
    "Piano Sonata in A minor, D. 845": {2: "C major", 3: "A minor"},
    "Piano Sonata in D major, D. 850": {2: "A major", 3: "D major"},
    "Piano Sonata in C minor, D. 958": {2: "A-flat major", 3: "C minor"},
    "Piano Sonata in A major, D. 959": {2: "F-sharp minor", 3: "A major"},
    "Goldberg Variations in G major, BWV 988": {16: "G minor", 22: "G minor", 26: "G minor"},
    # Keys given by Jeem; the nocturnes' keys also match their titles (Wikipedia, IMSLP).
    "Piano Sonata No. 14 'Moonlight' in C-sharp minor, Op. 27 No. 2": {2: "D-flat major"},
    "Nocturnes, Op. 9 Nos. 1–3, Op. 27 No. 2, Op. 48 No. 1": {
        1: "B-flat minor", 2: "E-flat major", 3: "B major", 4: "D-flat major", 5: "C minor"},
}
