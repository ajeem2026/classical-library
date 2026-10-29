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
            1: [N("Borodin was a professor of chemistry who composed in his spare time; this movement "
                  "weaves in Beethoven's theme.", unsure="Borodin's chemistry career is not on the fetched IMSLP page")],
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
               "Protopova. It may be a 20th-anniversary gift recalling how they met in Heidelberg."),
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
                  "like a lark.", at="after:12", unsure="the origin of the nickname is not on the fetched page")],
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
        # src: W+"String_Quartet_No._15_(Mozart)" (1783; Constanze in labour)
        work=N("Completed in 1783, while his wife Constanze was in labour with their first child, "
               "Raimund. The only minor-key quartet in the set of six Mozart dedicated to Haydn.",
               unsure="'only minor-key quartet of the set' is not on the fetched page"),
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
        # src: imslp.org Meditation_on_the_Old_Czech_Chorale_..._(Suk,_Josef) (1914; dedication; scoring)
        work=N("A meditation on the old Czech chorale 'St Wenceslas', for string quartet or string "
               "orchestra, first published in 1914 and dedicated to Ferdinand Pečírka."),
        movements={
            1: [N("Published in the first year of the First World War, the chorale to the Czech patron "
                  "saint here builds to its fullest sound.", at="climax",
                  unsure="any wartime meaning is inferred from the date, not stated on IMSLP")],
        }),

    "Piano Sonata in E-flat major, D. 568": dict(
        # src: W+"Piano_Sonata_in_E-flat_major,_D_568_(Schubert)" (D-flat version 1817; E-flat published 1829)
        work=N("First drafted in D-flat major in June 1817, when Schubert was 20. He revised and finished "
               "it in E-flat; it was published in 1829, the year after his death."),
        movements={
            1: [N("Allegro moderato: a gentle, singing opening theme, unhurried even when it develops.")],
            2: [N("Andante molto: a slow, sorrowful song in a minor key.",
                  unsure="the minor key is not stated on the fetched page")],
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
}


# ---- Dream conversations (imagined; shown labelled "Imagined conversation") --
# Keyed by album(w). Lines alternate: "me" (Jeem, first person) and "them" (the
# composer, in character). Each composer line rests on a fact from the work's
# NOTES sources unless flagged with unsure=.

def L(who, text, unsure=None):
    return dict(who=who, text=text, unsure=unsure)


DREAMS = {
    "Symphony No. 3 in E-flat major, Op. 55": [
        # src: W+"Symphony_No._3_(Beethoven)" (Ries on the title page; Ries on the horn entrance)
        L("me", "You wrote Bonaparte's name on the title page. What happened?"),
        L("them", "He made himself emperor. Now he will trample the rights of man. I tore the page in two."),
        L("me", "And the horn that comes in early?"),
        L("them", "At the first rehearsal Ries thought the player was wrong, and said so. He nearly had his ears boxed."),
    ],
    "Symphony No. 1 in C minor, Op. 68": [
        # src: W+"Symphony_No._1_(Brahms)" (1855–1876; Beethoven's reputation; card to Clara, 1868)
        L("me", "Twenty-one years on one symphony?"),
        L("them", "After Beethoven, a symphony had to carry real weight. I was not going to hurry it."),
        L("me", "And the horn tune in the finale?"),
        L("them", "I sent it to Clara on a card in 1868. 'Thus blew the shepherd's horn today.'"),
    ],
    "Symphony No. 2 in D major, Op. 73": [
        # src: W+"Symphony_No._2_(Brahms)" (Pörtschach, 1877; letter to the publisher)
        L("me", "You told your publisher this one was unbearably melancholy."),
        L("them", "I did. Then he heard it. A summer by the lake at Pörtschach does not make a sad symphony."),
    ],
    "Symphony No. 3 in F major, Op. 90": [
        # src: W+"Symphony_No._3_(Brahms)" (F–A–F; Joachim's F–A–E; quiet ending)
        L("me", "F, A, F. What does it mean?"),
        L("them", "Frei aber froh. Free, but happy. Joachim's motto was 'free but lonely'. At fifty, I chose mine."),
        L("me", "Why let it end so quietly?"),
        L("them", "Everyone expects thunder at the end of a symphony. I let the motto settle instead.",
          unsure="Brahms's reason for the quiet ending is imagined"),
    ],
    "Symphony No. 4 in E minor, Op. 98": [
        # src: W+"Symphony_No._4_(Brahms)" (BWV 150 chaconne; triangle)
        L("me", "The finale goes back to Bach."),
        L("them", "A chaconne from his cantata 'Nach dir, Herr, verlanget mich'. My last symphony ends on his ground."),
        L("me", "And the triangle?"),
        L("them", "Once, in four symphonies. Let it ring."),
    ],
    "Symphony No. 6 in B minor, Op. 74": [
        # src: W+"Symphony_No._6_(Tchaikovsky)" (letter to his brother; premiere nine days before his death)
        L("me", "You conducted this nine days before you died."),
        L("them", "I did not know that. I only wrote to my brother that I believed it the best of my works."),
        L("me", "Why end slowly?"),
        L("them", "Symphonies end in triumph. This one ends very quietly, in the low strings."),
    ],
    "String Quartet No. 6 in B-flat major, Op. 18 No. 6": [
        # src: W+"String_Quartet_No._6_(Beethoven)" ('La Malinconia'; delicacy marking)
        L("me", "Why call the last movement 'melancholy'?"),
        L("them", "Because it is. I wrote that it must be played with the greatest delicacy."),
        L("me", "Then a dance breaks in."),
        L("them", "The dance tries to forget. The melancholy keeps coming back."),
    ],
    "String Quartet No. 1 in A major": [
        # src: imslp.org String_Quartet_No.1_(Borodin,_Aleksandr) (Op. 130 borrowing; 1874–79)
        L("me", "Five years on one quartet?"),
        L("them", "1874 to 1879. I was a chemist first; music had to wait for my free hours.",
          unsure="Borodin's chemistry career is not on the fetched IMSLP page"),
        L("me", "Why borrow from Beethoven?"),
        L("them", "A phrase from the finale of his Op. 130 stayed with me. My quartet answers it."),
    ],
    "String Quartet No. 2 in D major": [
        # src: W+"String_Quartet_No._2_(Borodin)" (dedication; Dianin's anniversary reading; Heidelberg)
        L("me", "Who is this for?"),
        L("them", "For Ekaterina, my wife. Twenty years since we met in Heidelberg, some say."),
        L("me", "And the Notturno?"),
        L("them", "The cello sings first, then the violin answers. You may guess who is who.",
          unsure="the cello/violin as the couple is a popular reading, not a documented one"),
    ],
    "String Quartet No. 12 in F major, Op. 96": [
        # src: W+"String_Quartet_No._12_(Dvořák)" (Spillville; the bird; the Haydn quotation)
        L("me", "What did you hear in Spillville?"),
        L("them", "A bird, high in the trees. I wrote its song down and gave it to the first violin."),
        L("me", "People argue about which bird."),
        L("them", "A scarlet tanager, I thought. Perhaps a vireo. I wanted something simple, like dear Papa Haydn."),
    ],
    "String Quartet No. 10 in E-flat major, Op. 51": [
        # src: W+"String_Quartet_No._10_(Dvořák)" (Becker's request; dumka; skočná)
        L("me", "Becker asked you for something Slavonic?"),
        L("them", "After the Slavonic Dances, everyone did. So: a dumka in the middle, and a skočná to finish."),
    ],
    "String Quartet in D major, Op. 64 No. 5, Hob. III:63": [
        # src: W+"String_Quartets,_Op._64_(Haydn)" (Tost)
        L("me", "Who was Tost?"),
        L("them", "A violinist, later a merchant. He helped me find a publisher for these."),
        L("me", "Do you mind them calling it 'The Lark'?"),
        L("them", "Others named it, not I. The first violin does fly high.",
          unsure="the origin of the nickname is not on the fetched page"),
    ],
    "String Quartet No. 6 in F minor, Op. 80": [
        # src: W+"String_Quartet_No._6_(Mendelssohn)" (Fanny, 14 May 1847; homage)
        L("me", "This came after Fanny died."),
        L("them", "In May she was gone. I could not write anything gentle. This is what came."),
        L("me", "There is no turn to the major at the end."),
        L("them", "No. I could not find one.", unsure="Mendelssohn's own view of the ending is imagined"),
    ],
    "String Quartet No. 15 in D minor, K. 421": [
        # src: W+"String_Quartet_No._15_(Mozart)" (1783; Constanze in labour); Haydn dedication
        L("me", "Is it true you wrote this while Constanze was in labour?"),
        L("them", "So it is told. Our first child, Raimund, in 1783. I was at my desk; she was in the next room.",
          unsure="the 'next room' detail is imagined"),
        L("me", "And it is for Haydn."),
        L("them", "Six quartets for the man who showed us all how quartets are written."),
    ],
    "String Quartet No. 19 in C major, K. 465": [
        # src: W+"String_Quartet_No._19_(Mozart)" (22-bar Adagio; 1787 printed complaint; Haydn set)
        L("me", "Your opening sounds wrong on purpose."),
        L("them", "Twenty-two bars of fog before the sun comes out. A critic complained in print."),
        L("me", "Did it bother you?"),
        L("them", "I had dedicated it to Haydn. His ears were the ones I wrote for.",
          unsure="Mozart's reaction to criticism is imagined"),
    ],
    "Meditation on the Old Czech Chorale 'St. Wenceslas', Op. 35a": [
        # src: imslp.org Meditation_..._(Suk,_Josef) (1914; dedication; chorale)
        L("me", "Why the St Wenceslas chorale?"),
        L("them", "It is our oldest hymn to our patron saint. In 1914, people needed something to hold on to.",
          unsure="the wartime motive is inferred from the date"),
    ],
    "Piano Sonata in E-flat major, D. 568": [
        # src: W+"Piano_Sonata_in_E-flat_major,_D_568_(Schubert)"
        L("me", "You began this in D-flat?"),
        L("them", "At twenty, in 1817. Later I moved it to E-flat and finished it. I never saw it printed."),
    ],
    "Piano Sonata in A major, D. 664": [
        # src: W+"Piano_Sonata_in_A_major,_D_664_(Schubert)"
        L("me", "Who was Josephine?"),
        L("them", "Josephine von Koller, in Steyr. Eighteen, very pretty, and a good pianist. The sonata is hers."),
    ],
    "Piano Sonata in A minor, D. 784": [
        # src: W+"Piano_Sonata_in_A_minor,_D_784_(Schubert)" (Feb 1823; illness the year before)
        L("me", "What happened the year before?"),
        L("them", "I was seriously ill. When I wrote this in February, I wanted nothing decorative. Bare octaves.",
          unsure="the link between illness and the stark style is a suggestion on the page, not certain"),
    ],
    "Piano Sonata in A minor, D. 845": [
        # src: W+"Piano_Sonata_in_A_minor,_D_845_(Schubert)"
        L("me", "This one was printed while you lived."),
        L("them", "My first grand sonata in print. Only three ever were, in my lifetime."),
    ],
    "Piano Sonata in D major, D. 850": [
        # src: W+"Piano_Sonata_in_D_major,_D_850_(Schubert)"
        L("me", "Gastein?"),
        L("them", "A spa in the mountains, August 1825. The mountain air made me write big chords.",
          unsure="the 'mountain air' remark is imagined"),
    ],
    "Piano Sonata in C minor, D. 958": [
        # src: W+"Piano_Sonata_in_C_minor,_D_958_(Schubert)" (Beethoven quote; 1828)
        L("me", "The opening sounds like Beethoven."),
        L("them", "His C minor Variations. I admired him more than anyone."),
        L("me", "You finished this in September 1828."),
        L("them", "And by November I was gone. I did not know there would be no time."),
    ],
    "Piano Sonata in A major, D. 959": [
        # src: same article (Andantino middle section; 1839 dedication to Schumann)
        L("me", "What happens in the middle of the Andantino?"),
        L("them", "The song breaks. Everything I had kept quiet comes out at once, then the song returns."),
        L("me", "It is dedicated to Schumann."),
        L("them", "After my death, by the publisher. He loved my music, so it is right."),
    ],
    "Goldberg Variations in G major, BWV 988": [
        # src: W+"Goldberg_Variations" (Forkel 1802; 1741; canons; quodlibet)
        L("me", "Did you really write this for a count who couldn't sleep?"),
        L("them", "Forkel tells it so, sixty years later. I published it in 1741, as keyboard practice."),
        L("me", "Thirty variations on one tune?"),
        L("them", "On one bass. Every third a canon, each a step wider. And at the end, a joke: a quodlibet."),
    ],
}
