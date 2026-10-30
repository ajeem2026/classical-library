"""Dream material: imagined conversations between me (Jeem) and each composer.

Keyed by album(w). Each work has 4 openings (the composer greets me), 8 questions
(mine) with 3 short in-character answers each, and 4 closings (the dream fades).
At runtime the player assembles one dream: an opening, 2–3 question/answer pairs
and a closing, never repeating a pair within a session. Scenes are labelled
"An imagined conversation" on screen.

Every line is under 25 words. A source comment marks each line that states a
fact; lines with none voice feeling or imagery, not fact. unsure= marks a claim
the source did not confirm (listed in data/dreams_to_check.md).

Brahms was written first to set the voice; the other works follow it.
"""


def L(text, unsure=None, who="them"):
    return dict(who=who, text=text, unsure=unsure)


def me(text):
    return L(text, who="me")


def Q(ask, *answers):
    return dict(ask=ask, answers=list(answers))


W = "https://en.wikipedia.org/wiki/"
BRAHMS = W + "Johannes_Brahms"   # composer pages for life facts, fetched Oct 2026

DREAMS = {
    # ---- Brahms ----------------------------------------------------------------
    "Symphony No. 1 in C minor, Op. 68": dict(
        # src: W+"Symphony_No._1_(Brahms)" unless noted
        open=[
            L("Come in, mind the sketches on the floor. Some of them are older than you'd think."),
            # premiere: Karlsruhe, conducted by his friend Felix Otto Dessoff
            L("You found me in Karlsruhe. Dessoff is about to begin, and my hands are cold."),
            # 21 years, 1855–1876
            L("Good evening. You've heard it, then? Twenty-one years, and I'm still not sure of it."),
            L("Sit down. They are tuning the timpani, and I can't bear to watch."),
        ],
        qa=[
            Q("Why did this symphony take you twenty-one years?",
              # 21 years from first sketches to the premiere
              L("A symphony after Beethoven can't be dashed off. Twenty-one years, from first sketch to Karlsruhe."),
              # BRAHMS: perfectionist, destroyed many works
              L("I write slowly, and I burn more than I keep."),
              # the finale may not have taken shape until 1868 (hedged on the page)
              L("Sketches, doubts, more doubts. The finale only found its shape years later, around 1868.")),
            Q("Bülow called it Beethoven's Tenth. Were you flattered?",
              L("Flattered, and cornered. Now every critic holds me up against him."),
              # Bülow, 1877
              L("Bülow said it in 1877. He means well. I wrote my First, not anybody's Tenth."),
              L("I'd rather they listened than counted.")),
            Q("The big tune in the finale sounds like the Ode to Joy.",
              # reply quoted on the page
              L("Any ass can see that."),
              L("Yes, yes, Beethoven's Ninth. Everyone points it out, as if I hadn't noticed."),
              # BRAHMS: kept a marble bust of Beethoven where he composed
              L("Of course it does. His bust watches me while I work. I'm not hiding anything.")),
            Q("Tell me about the horn call in the finale.",
              # card to Clara Schumann, September 1868
              L("I sent it to Clara on a card in September 1868. 'Thus blew the shepherd's horn today!'"),
              # a birthday card: sent 12 September 1868, Clara's birthday the 13th (confirmed by Jeem);
              # in the symphony by its 1876 premiere
              L("An alphorn tune, for Clara's birthday. Eight years later it was in the symphony."),
              L("It breaks through the dark like sunlight on a mountain. After that, the strings may sing.")),
            Q("Why does it open with that pounding timpani?",
              # "pulsating timpani" under the opening
              L("The timpani throb under everything, like a heartbeat you can't ignore."),
              # introduction written after the rest of the movement
              L("I wrote the introduction last, after the Allegro. The house needed a gate."),
              # BRAHMS: "long and in C minor", pointing to Beethoven's Fifth
              L("It is long, and in C minor. You know which other symphony that is.")),
            Q("Where was it first played?",
              # 4 November 1876, Karlsruhe, Dessoff
              L("Karlsruhe, on 4 November 1876. My friend Dessoff conducted."),
              L("In Karlsruhe. Better to stumble in a small court town than in Vienna.",
                unsure="his reason for choosing Karlsruhe is imagined"),
              # Simrock got the score only after performances in three cities
              L("Karlsruhe first. Simrock only got the score after three cities had heard it.")),
            Q("What is the slow movement saying?",
              # Andante sostenuto in E major
              L("It's in E major, a long way from C minor. Somewhere to breathe."),
              # long violin solo near the end
              L("Near the end the solo violin sings. Let it, and don't talk over it."),
              # BRAHMS: replaced the original slow movement before publication
              L("This is my second try. I replaced the first slow movement before it was published.")),
            Q("Did you ever think of giving up on it?",
              # BRAHMS: claimed to have destroyed 20 string quartets before Op. 51 No. 1
              L("Give up? I destroyed twenty quartets before I let one out. This one I kept."),
              # BRAHMS: a D minor symphony project became the First Piano Concerto
              L("An early D minor symphony became my First Piano Concerto. Nothing is wasted."),
              L("Every summer I doubted it. Every autumn I went back to it.")),
        ],
        close=[
            L("The horn is calling again. Go and listen. I'll stay in the shadows."),
            L("The finale is starting. I must go and worry somewhere quietly."),
            L("Enough talk. The music says it better. Goodnight."),
            me("His voice thins into the strings, and the room goes dark."),
        ]),

    "Symphony No. 2 in D major, Op. 73": dict(
        # src: W+"Symphony_No._2_(Brahms)" unless noted
        open=[
            # summer 1877 at Pörtschach am Wörthersee
            L("Ah, you've found the lake. Pörtschach in summer. Sit, the light on the water is free."),
            # letter of 22 Nov 1877
            L("Welcome. I'm writing something cheerful, though I'll tell my publisher otherwise."),
            # composition brief next to the First's 21 years
            L("After twenty-one years on the First, this one came in a single summer. Don't tell anyone."),
            # premiere postponed while the players learned Das Rheingold
            L("Good evening. Richter has it on the stands at last. The orchestra was busy with Wagner."),
        ],
        qa=[
            Q("You told your publisher it was so melancholy he couldn't bear it. Really?",
              L("A joke. Listen to it. It's a summer by a lake."),
              # quoted from the letter
              L("My words: 'so melancholy that you will not be able to bear it.' I enjoyed writing them."),
              L("He believed me for a week. Then he heard it.",
                unsure="the publisher's reaction is imagined")),
            Q("Where did you write it?",
              # Pörtschach am Wörthersee, Carinthia, summer 1877
              L("Pörtschach, on the Wörthersee, in the summer of 1877."),
              L("In Carinthia, by a lake. It took one summer, not twenty-one years."),
              L("At Pörtschach. The water, the hills, the light: they are all in there.")),
            Q("Is that your Lullaby in the first movement?",
              # second theme (bar 82) resembles the Wiegenlied, Op. 49 No. 4, then is reshaped
              L("Its cousin. Violas and cellos sing it, and then I bend it out of shape."),
              L("Only for a few bars. Then it grows up and goes its own way."),
              L("You noticed. I never throw a good tune away.")),
            Q("Why trombones and tuba in such a sunny piece?",
              # letter to Vinzenz Lachner: the shadow "perhaps accounts for those timpani and trombones"
              L("Even summer has a shadow. Perhaps that accounts for the timpani and trombones."),
              # same letter: "a severely melancholic person"
              L("I told Lachner I am a severely melancholic person. The trombones know it."),
              L("So the ending can blaze. Wait for the last bars.")),
            Q("What happens in the slow movement?",
              # Adagio non troppo in B major; the cello melody is from NOTES
              L("B major, and a long cello melody that wanders and won't say where it's going."),
              L("This is where the summer clouds over. Don't hurry it."),
              # comparisons with Beethoven's Sixth
              L("It's the serious part. People forget that when they call this my Pastoral.")),
            Q("Who played it first?",
              # 30 December 1877, Vienna Philharmonic, Hans Richter
              L("The Vienna Philharmonic under Richter, on 30 December 1877."),
              # postponed while the players learned Das Rheingold
              L("Richter, in Vienna. It was postponed; the orchestra was busy learning Wagner's Rheingold."),
              L("Vienna, just before the new year. A good way to end one.")),
            Q("Is the third movement a dance?",
              # G major, interrupted by quicker Presto episodes built on the same tune (NOTES)
              L("A gentle one in G major, twice interrupted by something quicker made of the same tune."),
              L("Yes. Then it trips into a Presto and comes back as if nothing happened."),
              L("Think of a country dance, played by people in their good shoes.")),
            Q("Is it really like Beethoven's Pastoral?",
              L("People say so. I wrote what the lake gave me."),
              L("Every symphony of mine is held against Beethoven. At least this time it's the kind one."),
              # letter to Vinzenz Lachner, quoted on the page: the symphony "is followed by a little
              # essay about the great 'Why'"
              L("Cheerful, yes. But I told Lachner it is followed by a little essay about the great 'Why'.")),
        ],
        close=[
            L("The trombones are coming. I'll leave before they arrive."),
            L("The lake is going dark. Listen to the end. It's louder than I let on."),
            L("Go on. And never believe what I write in letters."),
            me("The water takes his voice. Only the horns are left."),
        ]),

    "Symphony No. 3 in F major, Op. 90": dict(
        # src: W+"Symphony_No._3_(Brahms)" unless noted
        open=[
            # summer 1883, Wiesbaden; Brahms was 50
            L("Welcome to Wiesbaden. Summer 1883. I'm fifty and, as you see, still free."),
            L("F, A, F. You heard it already, didn't you? Sit down."),
            # premiere at the Musikverein; Wagner enthusiasts tried to interfere
            L("Richter is rehearsing in the Musikverein. Let's talk before the Wagnerians arrive."),
            # nearly six years after No. 2
            L("Come in. Six years since my Second. I wasn't idle, only careful."),
        ],
        qa=[
            Q("What does F–A–F mean?",
              # widely assumed to be "frei aber froh"; Brahms said nothing about it
              L("Frei aber froh. Free, but happy. At least, that's what people say I meant."),
              # echoes Joachim's F–A–E, "frei aber einsam"
              L("Joachim's motto was F–A–E, free but lonely. Mine answers his."),
              # Brahms often said he spoke "through my music"
              L("I speak through my music. Ask the notes, not me.")),
            Q("Did Richter like it?",
              # Richter called it Brahms's "Eroica"
              L("He called it my Eroica. I let him."),
              # 2 December 1883, Vienna
              L("Richter conducted it in Vienna on 2 December 1883 and called it my Eroica."),
              # better received than the Second
              L("Very much. It went down better than my Second, Wagner crowd or no.")),
            Q("Was the premiere peaceful?",
              # Wagner enthusiasts tried to interfere
              L("Wagner's admirers tried to spoil it. The music won."),
              # the Brahms–Wagner quarrel nearly led to a duel
              L("Almost a duel, between my friends and Wagner's. Over a symphony!"),
              L("Noisy outside the score, quiet inside it. I prefer the inside.")),
            Q("That melody in the third movement...",
              # Poco allegretto, C minor, 3/8, lyrical, not a fast scherzo
              L("C minor, in three-eight, and not a scherzo. Let it sing."),
              L("Everyone hums that one. I never know whether to be pleased."),
              # moderate in tempo, intensely lyrical
              L("Not fast. Moderate, and as tender as I dared.")),
            Q("Why does it end so quietly?",
              L("Everyone expects thunder at the end of a symphony. I let it fade instead.",
                unsure="Brahms's reason for the quiet ending is imagined"),
              # finale in F minor, ending quietly in F major
              L("The storm in F minor burns out, and the motto settles into F major."),
              L("I'm fifty. I know how to leave a room.")),
            Q("What did Hanslick write?",
              # "artistically the most nearly perfect"
              L("That it was artistically the most nearly perfect of my symphonies. He is kind to me."),
              L("'Artistically the most nearly perfect.' From a critic, I'll take it."),
              L("Praise, of course. Wagner's people say he'd praise my laundry list.",
                unsure="the jibe is imagined")),
            Q("Do I hear Schumann in the opening?",
              # opening theme resembles a phrase of Schumann's "Rhenish" Symphony
              L("His Rhenish Symphony, yes. A phrase I carry with me."),
              # BRAHMS: Schumann's "Neue Bahnen", 28 October 1853
              L("Robert wrote 'New Paths' about me in 1853. His music never left me."),
              # a transition alludes to the Siren's Chorus from Tannhäuser
              L("And a little Wagner too, in one passage. Don't tell anyone.")),
            Q("What is the Andante like?",
              # C major; the melody first on solo clarinet, then passed round the orchestra
              L("C major. A quiet clarinet tune that the whole orchestra passes round."),
              L("Simple, like a hymn at evening. Don't look for drama here."),
              L("The clarinet begins alone. Then everyone wants a turn.")),
        ],
        close=[
            L("Listen: the motto again, quietly now. That's how I want to leave."),
            L("It ends softly. So do I. Goodnight."),
            L("No applause, please. Just let the last chord settle."),
            me("He hums F, A, F, and the room dissolves into the strings."),
        ]),

    "Symphony No. 4 in E minor, Op. 98": dict(
        # src: W+"Symphony_No._4_(Brahms)" unless noted
        open=[
            # begun at Mürzzuschlag, 1884
            L("Welcome to Mürzzuschlag. Mountains, and a symphony that won't leave me alone."),
            # private two-piano preview with Ignaz Brüll
            L("You've come for the last one. Sit. Brüll and I are at the two pianos."),
            # premiere: Meiningen, 25 October 1885, Brahms conducting
            L("Meiningen, October 1885. I'm conducting it myself tonight. Wish me luck."),
            # begun 1884, a year after the Third
            L("Come in. I began this in the Alps, a year after the Third."),
        ],
        qa=[
            Q("Why do the violins open with falling thirds?",
              # chain of falling thirds (NOTES)
              L("Two notes at a time, sighing. A chain that keeps falling."),
              L("Falling thirds. The whole movement hangs from them."),
              L("Because it's simple. A child could play the outline. The rest is work.")),
            Q("Where does the finale come from?",
              # theme adapted from the closing chaconne of BWV 150
              L("Bach's cantata 'Nach dir, Herr, verlanget mich'. I borrowed his chaconne theme."),
              # passacaglia: variations over a repeating theme
              L("A passacaglia: one theme, again and again, and everything changes over it."),
              L("From Bach. When in doubt, go back to Bach.")),
            Q("What did your friends say at the piano preview?",
              # Hanslick, page-turning, per Kalbeck
              L("Hanslick turned pages and said he felt beaten by two incredibly intelligent people."),
              L("Brüll and I played it on two pianos. Then a long silence.",
                unsure="the silence is imagined"),
              L("Hanslick felt he was being given a beating. I took it as a compliment.")),
            Q("Why a triangle?",
              # triangle only in the third movement
              L("Only in the third movement. One glint of metal in a serious symphony."),
              # the only scherzo-like movement in his symphonies (NOTES)
              L("It's the nearest I come to a scherzo. Even I can be loud."),
              # NOTES: the only Brahms symphony movement with a triangle
              L("Listen for it. I use it nowhere else in my symphonies.")),
            Q("What are the horns playing at the start of the slow movement?",
              # E Phrygian theme, warmed into E major (NOTES)
              L("Phrygian, the old church mode. Then the strings warm it into E major."),
              L("Something old, from the church. I like old things that still work."),
              L("Horns first, in an ancient mode. Like a ballad before anyone sings it.")),
            Q("Who played it first?",
              # Meiningen Court Orchestra, 25 October 1885, Brahms conducting
              L("The Meiningen Court Orchestra, on 25 October 1885. I conducted."),
              L("I conducted, in Meiningen. A small court with a fine orchestra."),
              L("Meiningen. I stood in front of it myself, with my heart in my mouth.")),
            Q("Why end your last symphony so darkly?",
              L("The passacaglia goes where it must. I won't force a happy ending on it."),
              L("I knew it would be dark. I wrote it anyway."),
              L("Did I know it was my last? I'm not telling you.")),
            Q("Do you still think about Beethoven?",
              # BRAHMS: marble bust of Beethoven in his composing space
              L("His bust watches me compose. I think of him every day."),
              L("Less now. In this one I talked with Bach instead."),
              L("Always. But by the Fourth, I'm no longer afraid of him.")),
        ],
        close=[
            L("The passacaglia is turning. Let it carry you down."),
            L("My last symphony. Listen to it, then let me go."),
            L("Bach would have finished it better. Goodnight."),
            me("The bass line keeps repeating, and he walks away along it."),
        ]),

    # ---- Beethoven, Eroica -------------------------------------------------------
    "Symphony No. 3 in E-flat major, Op. 55": dict(
        # src: W+"Symphony_No._3_(Beethoven)" and its NOTES unless noted (fetched Oct 2026);
        # LvB = W+"Ludwig_van_Beethoven"
        open=[
            # composed mainly in 1803–04, with Napoleon in mind
            L("Come in. Mind the ink. I'm writing a symphony for a great man. Possibly."),
            # first private performance at Prince Lobkowitz's palace, with extra players hired
            L("Welcome to the Lobkowitz palace. The prince hired extra players. Even a third horn."),
            # public premiere at the Theater an der Wien
            L("Sit. Tonight Vienna hears it at the Theater an der Wien. They'll complain it's long."),
            # LvB: the Heiligenstadt Testament; "seize Fate by the throat"
            L("You've found me. Last year I thought of giving up. Now I've seized Fate by the throat."),
        ],
        qa=[
            Q("You wrote Bonaparte's name on the title page. What happened?",
              # Ries: Beethoven tore the title page in half on hearing Napoleon had made himself emperor
              L("He made himself emperor. I tore the page in two."),
              # Ries: "So he is no more than a common mortal!"
              L("So he is no more than a common mortal! Now he'll trample on everyone."),
              # the 1806 title: "to celebrate the memory of a great man"
              L("Now it celebrates the memory of a great man. Which man, I no longer say.")),
            Q("Who is it dedicated to now?",
              # re-dedicated to Prince Lobkowitz in autumn 1804
              L("Prince Lobkowitz. He pays for the rehearsals; he gets the dedication."),
              L("Not to an emperor. Never to an emperor."),
              L("A prince who loves music more than conquest. That will do.")),
            Q("And the horn that comes in early?",
              # Ries complained at the first rehearsal; Beethoven did not forgive him for a long time
              L("At the first rehearsal Ries said the player couldn't count. I haven't forgiven him."),
              # the horn's apparent early entrance near the end of the development
              L("Early? It's exactly where I wrote it. The violins are late."),
              L("A horn sees the theme coming before anyone else. Let it speak.")),
            Q("Why is it so long?",
              # about twice as long as symphonies by Haydn and Mozart
              L("Twice as long as Haydn's, they say. The subject needed room."),
              # a reviewer said it "would improve immeasurably" if shorter
              L("A critic says it would improve immeasurably if it were shorter. So would he."),
              # the first movement is nearly as long as a whole Classical symphony
              L("The first movement alone is nearly a whole symphony. I had a lot to say.")),
            Q("How does it begin?",
              # two sharp chords, then the cellos' rising arpeggio theme
              L("Two blows, then the cellos. Everything grows from that plain tune."),
              L("No introduction. Two chords, like a door kicked open."),
              L("A simple arpeggio. Simple things grow the furthest.")),
            Q("Why a funeral march?",
              # Marcia funebre in C minor
              L("A hero's symphony needs a grave. The march is in C minor."),
              L("Because heroes die, and everyone walks behind them."),
              L("It keeps coming back, like grief does.")),
            Q("Three horns in the trio?",
              # three horns in the trio, a first for a symphony
              L("Three. No symphony has had three before. Now one does."),
              L("The prince hired a third horn for the rehearsals. I made him earn it."),
              L("Listen to them call to each other. Hunting horns, almost.")),
            Q("Where does the finale's theme come from?",
              # a bass theme also used in The Creatures of Prometheus, the Contredanses and the Op. 35 Variations
              L("From my ballet, The Creatures of Prometheus. The Titan who brought fire."),
              L("I've used it before, in dances and piano variations. It wasn't finished with me."),
              L("A good bass line deserves more than one life.")),
        ],
        close=[
            L("The finale is starting. Long, yes. Stay anyway."),
            L("Go. And don't tell me about emperors."),
            L("The horns are calling. That one is not early."),
            me("He scowls, then laughs, and the funeral march carries him off."),
        ]),

    # ---- Tchaikovsky -------------------------------------------------------------
    "Symphony No. 6 in B minor, Op. 74": dict(
        # src: W+"Symphony_No._6_(Tchaikovsky)" and its NOTES unless noted;
        # TR = "https://en.tchaikovsky-research.net/pages/Symphony_No._6" (letters, fetched Oct 2026);
        # TCH = W+"Pyotr_Ilyich_Tchaikovsky"
        open=[
            # written in a small house in Klin
            L("Come in, quietly. Klin is small, and so is my house. The symphony is not."),
            # the players showed little admiration at rehearsals
            L("Forgive me, I'm nervous. The orchestra didn't seem to like it at rehearsal."),
            # the first movement was ready in under four days
            L("Sit. The first movement came in under four days. After that, I couldn't stop."),
            # premiere in Saint Petersburg, conducted by Tchaikovsky
            L("Good evening. Petersburg is cold, and tonight I conduct my own symphony. Pray for me."),
        ],
        qa=[
            Q("Is it true you think this is your best work?",
              # TR: letter to his nephew Vladimir ("Bob") Davydov, 2/14 August 1893
              L("I wrote to Bob that it's the best, and the most sincere, of all my creations."),
              # TR: same letter
              L("I love it as I have never loved any of my other musical offspring."),
              L("Best? Tomorrow I may hate it. Tonight, yes, I love it.")),
            Q("Is there a secret programme?",
              # TR: letter to Davydov, February 1893: "a programme that will remain an enigma to everyone"
              L("Yes. A programme that will remain an enigma to everyone. Let them guess."),
              # at the premiere he told Rimsky-Korsakov there was one, and would not reveal it
              L("Rimsky asked me at the premiere. I said there was one, and told him nothing."),
              # he had considered calling it "Programme Symphony"
              L("I thought of calling it the Programme Symphony. Then everyone would ask what the programme was.")),
            Q("Who gave it the name Pathétique?",
              # Modest claimed he suggested it the day after the premiere; doubted (TR)
              L("Modest says he did, the day after the premiere. My brother likes a good story."),
              # the Russian title means "passionate" or "emotional"
              L("In Russian it means passionate, emotional. Not pitiful. Remember that."),
              # the publisher kept the title
              L("My publisher kept the name. I've stopped arguing with publishers.")),
            Q("Why does the second movement limp?",
              # a waltz in 5/4, described as "limping"
              L("Five beats to the bar. A waltz that can't quite stand on both feet."),
              L("Graceful, but never settling. Like a man dancing with a stone in his shoe."),
              L("Count it: one-two, one-two-three. It almost waltzes.")),
            Q("The third movement sounds like a victory.",
              # scherzo that turns into a march, to a triumphant close
              L("A scherzo that turns into a march and drives to a triumphant close."),
              L("Enjoy it. What comes after is not a march."),
              L("A triumph in the third movement is not the end of the story.")),
            Q("Why end slowly, and so quietly?",
              # Adagio lamentoso; ends very quietly in the low strings
              L("Symphonies end in triumph. Mine sinks into the low strings: Adagio lamentoso."),
              L("Because that is how the story ends. I won't say whose story."),
              L("I wanted the last sound to be almost nothing.")),
            Q("Did you throw away another symphony before this one?",
              # the Symphony in E-flat, 1891–92, found unsatisfactory; its first movement became the Third Piano Concerto
              L("One in E-flat. I found it unsatisfactory, and its first movement became a piano concerto."),
              L("Yes. It was empty. This one came from somewhere deeper."),
              L("I put the rest of it in a drawer and started again.")),
            Q("Were you frightened to conduct it?",
              # TCH: conducting from 1887 helped him overcome lifelong stage fright
              L("Always. For years I couldn't face an orchestra. Conducting cured me, almost."),
              L("The players were polite and unimpressed. I went home and worried."),
              # TCH: trained in law; worked at the Ministry of Justice
              L("I was a clerk at the Ministry of Justice once. Orchestras frighten me more than judges.")),
        ],
        close=[
            L("The basses are going down. Let me go down with them, quietly."),
            L("Don't clap at the march. Wait for the end."),
            L("Write to me, if you can. I am a great writer of letters."),
            me("The last chord thins to nothing, and so does he."),
        ]),

    # ---- Beethoven ---------------------------------------------------------------
    "String Quartet No. 6 in B-flat major, Op. 18 No. 6": dict(
        # src: W+"String_Quartet_No._6_(Beethoven)" and its NOTES unless noted;
        # LvB = W+"Ludwig_van_Beethoven"
        open=[
            # commissioned by Prince Lobkowitz
            L("Yes? Speak up. Come in, I'm copying parts for Prince Lobkowitz."),
            # LvB: piano duels with Wölfl (1799) and Steibelt (1800)
            L("You've caught me between duels. Steibelt thinks he can play the piano. Sit."),
            # LvB: came to Vienna and studied counterpoint with Haydn
            L("Welcome to Vienna. I came to learn counterpoint from Haydn. Now I write quartets."),
            # the last of the six Op. 18 quartets
            L("Six quartets. This is the last, and the strangest. Sit down."),
        ],
        qa=[
            Q("Why call the last movement 'melancholy'?",
              # 'La Malinconia', marked to be played with the greatest delicacy
              L("Because it is. I wrote that it must be played with the greatest delicacy."),
              L("La Malinconia. I put the word on the page so no one could pretend otherwise."),
              # it alternates with a carefree dance until the two collide
              L("Melancholy, then a dance that tries to forget. They collide. That's the truth of it.")),
            Q("Who were these quartets for?",
              # commissioned by, and dedicated to, Prince Lobkowitz
              L("Prince Lobkowitz commissioned all six. He gets the dedication, and the bill."),
              L("For Vienna, which thinks it knows quartets because of Haydn and Mozart."),
              # published in 1801
              L("Published in 1801, all six at once, so no one could say the first was luck.")),
            Q("The scherzo keeps tripping me up.",
              # "a tour de force of syncopation"
              L("Good. Accents where the beat isn't. Let the players sweat."),
              L("A tour de force of syncopation, they'll say. I call it a joke on the foot-tappers."),
              L("Count, if you like. You'll lose.")),
            Q("Your hearing. Is it...?",
              # LvB: told Neate in 1815 that his hearing loss began in 1798, in a quarrel with a singer
              L("Don't. Since a quarrel with a singer, there's a noise in my ears. Tell no one."),
              # LvB: by 1801 he was writing to friends about his symptoms
              L("Some days, worse. I write to my friends about it. Not to princes."),
              L("The music is in here, not in the ears. Ask me something else.")),
            Q("Did Haydn teach you?",
              # LvB: studied composition with Haydn, mastering counterpoint
              L("Counterpoint, when I first came to Vienna. I learned more than I admit."),
              L("He taught me counterpoint. I taught myself the rest, mostly by arguing."),
              L("A great man. But a quartet of mine must not sound like a quartet of his.")),
            Q("What happens in the first movement?",
              # a quick, bright conversation between first violin and cello
              L("Allegro con brio. The violin says something, the cello answers back. Quickly."),
              L("A conversation, tossed back and forth. Nobody waits politely."),
              L("Bright and quick. Save your sighs for the finale.")),
            Q("And the Adagio?",
              # a gentle Adagio in E-flat major, the quietest movement
              L("E-flat major, the quietest place in the quartet. Rest there."),
              L("Gentle, yes. I can be gentle. Don't spread it around."),
              L("A song without words, for four people who can listen.")),
            Q("You play in the salons, they say. Do you win?",
              # LvB: performer and improviser in noble salons; won duels against Wölfl and Steibelt
              L("Wölfl, Steibelt, I've played them all. Improvising, I don't lose."),
              L("Steibelt played a showpiece. I turned his cello part upside down and improvised on it.",
                unsure="the upside-down cello part (Ries's account) is not on the fetched pages"),
              # LvB: Prince Lichnowsky was among his patrons
              L("The princes listen when I improvise. Even Lichnowsky stops talking.")),
        ],
        close=[
            L("The dance is coming back. Go, before the melancholy catches you."),
            L("Enough. I have parts to copy and a prince to pay me."),
            L("Delicately, I said. Delicately! Goodbye."),
            me("He turns back to the desk, humming too loud, and the room goes quiet."),
        ]),

    # ---- Borodin -----------------------------------------------------------------
    "String Quartet No. 1 in A major": dict(
        # src: imslp.org String_Quartet_No.1_(Borodin,_Aleksandr) and its NOTES unless noted;
        # AB = W+"Alexander_Borodin"
        open=[
            # AB: professor of chemistry
            L("Welcome to my laboratory. Mind the flasks. The quartet is on the piano, under my notes."),
            L("Ah, a visitor. I've a lecture at nine, but sit. Music first, for once."),
            # composed over five years
            L("Come in. Five years on one quartet. Chemists are patient people."),
            # AB: composed in his spare time or when ill
            L("Good evening. I compose best when I'm ill. Today I'm quite ill."),
        ],
        qa=[
            Q("Why did this quartet take five years?",
              # AB: medicine and science came first; he composed in his spare time or when ill
              L("Chemistry first. Music had to wait for my free hours, or a good fever."),
              L("Between lectures and experiments, a few bars a week."),
              # AB: studied composition with Balakirev
              L("Balakirev scolds me for being slow. Balakirev scolds everyone.")),
            Q("Why borrow from Beethoven?",
              # borrowings from the finale of Beethoven's Op. 130
              L("A phrase from the finale of his Op. 130 stayed with me. My quartet answers it."),
              # subtitle "On a theme of Beethoven"
              L("'On a theme of Beethoven', the title says. I wanted to be honest about it."),
              L("Even a Russian may learn from a German. Especially a chemist.")),
            Q("You're a professor of chemistry?",
              # AB: professor at the Medical-Surgical Academy; known for work on aldehydes
              L("At the Medical-Surgical Academy. Aldehydes are my speciality. Very fragrant."),
              L("Science is my profession. Music is my joy. Joy gets the evenings."),
              # AB: founded medical courses for women in 1872
              L("I also teach medicine to women. Someone has to begin.")),
            Q("What happens in the slow movement?",
              # Andante con moto in F-sharp minor, with a fugato
              L("Andante con moto, in F-sharp minor, with a little fugue at its heart."),
              L("A fugato: one voice begins, the others follow, like students into a lecture."),
              L("It's sad, but it keeps walking. Con moto.")),
            Q("Why is the scherzo so short here?",
              # this recording plays it abridged
              L("This recording cuts it. Prestissimo is fast enough already."),
              L("Prestissimo! Like a reaction too quick to watch."),
              L("Blink and you've missed it. That's the point of a scherzo.")),
            Q("Where was it first played?",
              # Saint Petersburg, 30 December 1880
              L("In Saint Petersburg, on 30 December 1880. A good way to end a year."),
              L("At home in Petersburg. My friends came, and some critics, unfortunately."),
              L("Petersburg. I was nervous. Chemistry never makes me nervous.")),
            Q("Who were your parents?",
              # AB: illegitimate son of a Georgian nobleman, registered as the son of a serf
              L("My father was a Georgian nobleman. On paper I was the son of his serf."),
              L("I was registered as a serf's son. Paper is not the truth."),
              # AB: born in Saint Petersburg; in Heidelberg 1859–62
              L("I grew up in Petersburg and have hardly left it, except for Heidelberg.")),
            Q("How does the finale go?",
              # Andante opening, then Allegro risoluto, returning to the Beethoven material
              L("An Andante first, then Allegro risoluto, and Beethoven's phrase comes back."),
              L("Resolutely. I wrote risoluto so no one would dawdle."),
              L("It balances at the end, like a good equation.")),
        ],
        close=[
            L("My lecture is in an hour. I'll go and smell aldehydes."),
            L("Tell Beethoven I meant it kindly, if you see him."),
            L("The quartet is ending. Somewhere, a flask is boiling over."),
            me("He hums the finale, and the laboratory blurs into the strings."),
        ]),

    "String Quartet No. 2 in D major": dict(
        # src: W+"String_Quartet_No._2_(Borodin)" and its NOTES unless noted; AB = W+"Alexander_Borodin"
        open=[
            # written in 1881 at a friend's estate at Zhitovo, dedicated to his wife
            L("Welcome to Zhitovo. A friend's estate, a summer, and a quartet for my wife."),
            L("Come in. Ekaterina is resting. Speak softly; this one is hers."),
            # the Notturno, the most famous movement
            L("Ah, you've come for the Notturno. Everyone does. Sit."),
            # possibly a 20th-anniversary gift recalling how they met in Heidelberg
            L("Good evening. Twenty years ago I met a pianist in Heidelberg. Guess the rest."),
        ],
        qa=[
            Q("Who is this for?",
              # dedicated to his wife, Ekaterina Protopopova
              L("For Ekaterina, my wife. That's all a dedication needs to say."),
              # Dianin's reading: a 20th-anniversary gift
              L("Twenty years since we met in Heidelberg, some say. I'm not saying."),
              # AB: Protopopova was a pianist
              L("She's a pianist. I wrote it for strings, so she could simply listen.")),
            Q("How did you meet her?",
              # AB: in Heidelberg 1859–62, studying chemistry
              L("In Heidelberg, while I was studying chemistry. She played; I listened."),
              # AB: married in 1863
              L("Heidelberg. We married in 1863, and I've been late for dinner ever since."),
              L("That's a story for her to tell. She tells it better.")),
            Q("Why does the cello begin?",
              # the cello opens with a lyrical melody high in its register
              L("Because it can sing high, like a tenor. Listen to it reach."),
              L("The cello opens, high in its register. A man's voice, trying hard."),
              L("I play the cello myself, a little. So I gave it the best tune.",
                unsure="Borodin playing the cello is well known but not on the fetched pages")),
            Q("Tell me about the Notturno.",
              # the cello sings the long melody, later answered by the first violin
              L("The cello sings the long melody, and then the first violin answers it."),
              L("It's the movement everyone remembers. I didn't plan that."),
              L("A night piece. Two voices, one melody. You may guess who is who.",
                unsure="the cello and violin as the couple is a popular reading, not a documented one")),
            Q("What is the scherzo doing?",
              # light and quick, a breath before the Notturno
              L("Being light and quick. A breath before the Notturno."),
              L("Allegro, and over before you notice. Like a summer evening."),
              L("Even a chemist can be frivolous for a few minutes.")),
            Q("Where did you write it?",
              # Zhitovo, 1881
              L("At Zhitovo, a friend's country estate, in the summer of 1881."),
              L("In the country, away from the laboratory. My students think I'm working."),
              L("Zhitovo. Fields, quiet, and no lectures. The music came quickly.")),
            Q("How does the finale start?",
              # a slow question-and-answer opening, then Vivace
              L("With a slow question and an answer. Then off at a Vivace."),
              L("Two instruments ask, two reply. Then everyone runs."),
              L("Like talk at dinner before the vodka arrives.")),
            Q("Is it hard, being a composer and a chemist?",
              # AB: composed in his spare time or when ill
              L("I compose in my spare time, or when I'm ill. I'm often ill."),
              L("Science is my work. This is my rest. Some rest!"),
              # AB: medical courses for women, taught until 1885
              L("My students come first. Women studying medicine, in Petersburg. Imagine.")),
        ],
        close=[
            L("Ekaterina is calling. I must go. Listen to the cello for me."),
            L("The Notturno again? Everyone wants it again. Go on."),
            L("Summer is ending at Zhitovo. Back to the laboratory."),
            me("The cello's melody hangs in the air after he has gone."),
        ]),

    # ---- Dvořák ------------------------------------------------------------------
    "String Quartet No. 12 in F major, Op. 96": dict(
        # src: W+"String_Quartet_No._12_(Dvořák)" and its NOTES unless noted;
        # AD = W+"Antonín_Dvořák"
        open=[
            # Spillville, a Czech community in Iowa
            L("Welcome to Spillville. Czech voices, a Czech church, and Iowa all around. Sit."),
            # AD: a lifelong passion for trains
            L("Come in. I've just walked back from watching the trains. I always watch the trains."),
            # a summer break from New York
            L("A visitor from New York? No, no, I'm on holiday. Mostly."),
            # the bird song in the third movement
            L("Good morning. The birds here sing differently. I've been writing them down."),
        ],
        qa=[
            Q("What did you hear in Spillville?",
              # bird song transcribed in the third movement
              L("A bird, high in the trees. I wrote its song down and gave it to the first violin."),
              # a Czech community in Iowa
              L("Czech spoken in Iowa. After New York, it was like coming home."),
              L("Quiet. In New York there's never quiet.")),
            Q("Which bird was it?",
              # he thought a scarlet tanager; it may have been a vireo
              L("A scarlet tanager, I thought. Others say a vireo. The bird didn't say."),
              L("A red one, very proud of its song. I stole it."),
              L("Listen in the third movement, high in the first violin. That's him.")),
            Q("Why does it sound so simple?",
              # "Dear Papa Haydn kept appearing before my eyes ... so it turned out so simple"
              L("Dear Papa Haydn kept appearing before my eyes. So it turned out simple."),
              L("I wanted it clear, like the air here. No knots."),
              # the pentatonic scale, used throughout
              L("Five notes do a great deal of work. The pentatonic scale is very generous.")),
            Q("Who plays first?",
              L("The viola, over the violins' shimmer. Nobody expects it, so everybody listens.",
                unsure="the viola opening is not stated on the fetched page"),
              # AD: viola in the Provisional Theatre orchestra, 1862–71
              L("I sat among the violas in a theatre orchestra for nine years. They deserve a tune."),
              L("The quiet one in the middle. It has a lot to say.")),
            Q("Is the finale a train?",
              # AD: lifelong passion for trains (the link to the finale is a reading)
              L("You hear it too? A steady rhythm, chugging along. I love trains."),
              # AD: the Nelahozeves station was built in his childhood
              L("As a boy I watched them build the station in our village. I never got over it."),
              L("I won't say it's a train. I won't say it isn't.")),
            Q("Why are you in America?",
              # AD: director of the National Conservatory, New York, under Jeannette Thurber
              L("Mrs Thurber asked me to direct her conservatory in New York. I said yes."),
              L("To help Americans find their own music. I think they will."),
              # AD: salary $15,000, paid irregularly
              L("Money, partly. Fifteen thousand dollars a year, when they pay it.")),
            Q("What is the slow movement about?",
              # Lento: a long melody for the first violin, later the cello
              L("Lento. A long melody for the first violin, then the cello takes it."),
              L("Homesickness, maybe. I miss Bohemia, even in a Czech village."),
              L("It aches. I let it.")),
            Q("Who helped you most?",
              # AD: Brahms, on the State Prize jury, recommended him to Simrock
              L("Brahms. He sat on a prize jury and sent me to his publisher, Simrock."),
              # AD: Simrock commissioned the Slavonic Dances
              L("Simrock asked for Slavonic Dances, and suddenly the world knew my name."),
              L("God, my father, and Brahms. In that order, most days.")),
        ],
        close=[
            L("The evening train is due. Excuse me, I must go and watch it."),
            L("The bird is singing again. Go on, I'll write it down."),
            L("Back to New York soon. Let me have one more quiet day."),
            me("The chugging rhythm carries him off down the line."),
        ]),

    "String Quartet No. 10 in E-flat major, Op. 51": dict(
        # src: W+"String_Quartet_No._10_(Dvořák)" and its NOTES unless noted; AD = W+"Antonín_Dvořák"
        open=[
            # requested after the success of the Slavonic Dances
            L("Ah, you've come because of the Slavonic Dances, like everyone. Sit, sit."),
            # Jean Becker asked for a "Slavonic" quartet
            L("Welcome to Prague. Becker wants something Slavonic. I can do Slavonic."),
            # first played by the Joachim Quartet in Berlin
            L("Good day. Joachim's quartet will play my music in Berlin. Berlin! Imagine."),
            # AD: Simrock, after the Slavonic Dances
            L("Come in. Mind the scores. Simrock wants everything at once now."),
        ],
        qa=[
            Q("Becker asked you for something Slavonic?",
              # Becker's request; dumka; skočná
              L("After the Slavonic Dances, everyone did. So: a dumka in the middle, a skočná to finish."),
              # Jean Becker of the Florentine Quartet
              L("Jean Becker, of the Florentine Quartet. A polite request, with a clear order."),
              L("Slavonic, he said. As if I could write anything else.")),
            Q("What is a dumka?",
              # a Slavonic lament that turns from sorrow to quick dance and back
              L("A lament that suddenly dances, and then remembers it was sad."),
              L("Sorrow, then quick feet, then sorrow again. Very Slavonic."),
              # the dumka gives the quartet its Slavonic character
              L("It gives the whole quartet its character. Becker got what he asked for.")),
            Q("And a skočná?",
              # finale: a stylisation of the Czech skočná, a fast leaping dance
              L("A Czech leaping dance. In the finale I dress it up, but you can still jump."),
              # AD: his father was a zither player who earned a living as a musician
              L("A village dance. My father played for dancers, you know."),
              L("Fast and leaping. Don't sit too still.")),
            Q("Who played it first?",
              # the Joachim Quartet, Berlin
              L("Joachim's quartet, in Berlin. Germans playing Czech dances. Wonderful."),
              # BRAHMS: Joachim, Brahms's friend since 1853
              L("Joachim himself. A great violinist, and Brahms's friend."),
              L("Berlin heard it first. Prague will forgive me.")),
            Q("How did Brahms help you?",
              # AD: Brahms, on the State Prize jury, recommended him to Simrock
              L("He judged a state prize and told Simrock to publish me. I owe him much."),
              L("He said little and did a great deal. That's Brahms."),
              # AD: Simrock commissioned the Slavonic Dances
              L("Simrock asked me for Slavonic Dances because Brahms said so.")),
            Q("Why does the first movement rock like that?",
              # a relaxed opening with a rocking, dance-like lilt
              L("A relaxed lilt, a little dance in the walk. No hurry."),
              L("Like a cradle, or a cart on a country road."),
              L("Allegro ma non troppo. Not too fast. I mean it.")),
            Q("Tell me about the Romanza.",
              # a warm, song-like slow movement
              L("A warm song, for the evening. Nothing clever."),
              L("Every Czech knows how to sing. The Romanza simply sings."),
              L("After the dumka's tears, something kind.")),
            Q("Did you always want to be a composer?",
              # AD: his father was an innkeeper and musician
              L("I grew up in an inn, among village musicians. Music was always in the house."),
              # AD: viola in the Provisional Theatre orchestra
              L("I played viola in a theatre orchestra for years and composed at night."),
              # AD: born 1841 in Nelahozeves
              L("I was born in Nelahozeves, in 1841. Try saying it quickly.")),
        ],
        close=[
            L("The skočná is starting. You'll want to stand up."),
            L("Tell Becker it's finished. Slavonic enough, I hope."),
            L("I must write to Simrock. He's always waiting."),
            me("The leaping dance fades into the noise of a Prague street."),
        ]),

    # ---- Haydn -------------------------------------------------------------------
    "String Quartet in D major, Op. 64 No. 5, Hob. III:63": dict(
        # src: W+"String_Quartets,_Op._64_(Haydn)" and its NOTES unless noted; JH = W+"Joseph_Haydn"
        open=[
            # JH: Eszterháza's isolation; "forced to become original"
            L("Welcome to Eszterháza. Far from everything. That's how I learned to be original."),
            # JH: music director for the Esterházy family
            L("Ah, a guest! Sit. The Prince keeps me busy, but there's always time for a quartet."),
            # Johann Tost helped Haydn find a publisher
            L("Good day. Tost is here about the publisher again. Business, business."),
            # Dvořák's "dear Papa Haydn" (Op. 96 page)
            L("Come in, come in. They call me Papa. You may too."),
        ],
        qa=[
            Q("Do you mind them calling it 'The Lark'?",
              # the nickname from the first violin's soaring melody (confirmed by Jeem)
              L("Others named it, not I. But the first violin does fly high."),
              L("A lark is a fine bird. Let them call it that; it sells copies."),
              L("Listen to the violin climb over the others. Yes, a lark.")),
            Q("Who was Tost?",
              # a violinist, later a merchant, who helped Haydn find a publisher
              L("A violinist, later a merchant. He helped me find a publisher for these."),
              L("Johann Tost. A good violinist, and a better businessman."),
              # the Tost quartets
              L("To me they're just six quartets. Others call them the Tost quartets.")),
            Q("How did you learn to write quartets?",
              # JH: "forced to become original"
              L("Alone, at Eszterháza. Cut off from the world, I was forced to become original."),
              L("By trying things on my own players. No one could stop me."),
              # JH: nearly thirty years with the Esterházy family
              L("Thirty years of practice. Ask me again in thirty more.")),
            Q("Do you know Mozart?",
              # Leopold Mozart's letter of 16 February 1785, quoting Haydn (well documented)
              L("I told his father he's the greatest composer I know, in person or by name."),
              # Mozart's six quartets dedicated to Haydn (K. 421, K. 465 pages)
              L("Wolfgang dedicated six quartets to me. I'm still blushing."),
              # JH: joined the same Masonic lodge as Mozart
              L("We are brothers in the same lodge. Don't ask what happens there.")),
            Q("What is the slow movement like?",
              # Adagio cantabile in A major, ornamented by the first violin
              L("Adagio cantabile, in A major. A simple song, and the violin decorates it."),
              L("Cantabile means it sings. So let it sing, and don't hurry."),
              L("Simple things are the hardest. Anyone can be complicated.")),
            Q("And the finale?",
              # a perpetual motion of rapid notes
              L("Notes running and running, never stopping. A perpetual motion."),
              L("In the middle the voices chase each other, like a little fugue.",
                unsure="the fugal middle is not described on the fetched page"),
              L("Fast. The players will hate me, then love me.")),
            Q("What will you do, now the Prince has died?",
              # JH: Prince Nikolaus died in 1790; his successor dismissed most musicians
              L("Prince Nikolaus is gone, and the new one sent the musicians home. I'm free."),
              # JH: two visits to London with the impresario Salomon
              L("Travel! A man called Salomon wants me in London."),
              L("They say the English pay well and clap loudly. We'll see.")),
            Q("Where did you begin?",
              # JH: chorister at St Stephen's, dismissed in 1749, then freelance
              L("As a choirboy at St Stephen's in Vienna. Then dismissed, and scraping a living."),
              # JH: born 1732 in Rohrau
              L("In Rohrau, in 1732. A village with more geese than musicians."),
              L("From nothing. Hard work and good luck, mostly hard work.")),
        ],
        close=[
            L("The lark is climbing again. Go and listen."),
            L("Excuse me. The Prince's orchestra is waiting. Or it was."),
            L("Goodbye, my friend. Write to me if you get to London."),
            me("The first violin rises out of sight, and he is gone with it."),
        ]),

    # ---- Mendelssohn -------------------------------------------------------------
    "String Quartet No. 6 in F minor, Op. 80": dict(
        # src: W+"String_Quartet_No._6_(Mendelssohn)" and its NOTES unless noted;
        # FM = W+"Felix_Mendelssohn"
        open=[
            # Fanny died on 14 May 1847
            L("Forgive the quiet. Since May, the house has been very quiet."),
            # FM: a watercolour of Lucerne dated 1847; an enthusiastic painter
            L("Come in. I've been painting watercolours at Lucerne. My hands needed something gentle."),
            # a homage to Fanny
            L("Sit with me. I can't speak about her yet, but the quartet can."),
            L("Welcome. You've come at a hard time. Stay a little anyway."),
        ],
        qa=[
            Q("This came after Fanny died.",
              # Fanny died on 14 May 1847
              L("She died on 14 May. I couldn't write anything gentle. This is what came."),
              # FM: Fanny Hensel, a gifted composer and pianist
              L("Fanny was the better musician of us two, some days. Now there's only me."),
              # composed as a homage to her
              L("A homage to her. I have no other way to say it.")),
            Q("Why does it shake so at the start?",
              # tremolos and shuddering accents
              L("Tremolos, shuddering accents. Grief doesn't let you sit still."),
              L("I didn't want it beautiful. I wanted it true."),
              L("There's no comfort in the first movement. Not yet.")),
            Q("The scherzo never relaxes.",
              # an obsessive, syncopated scherzo
              L("No. It goes round and round, syncopated, like a thought you can't put down."),
              L("Obsessive, yes. I couldn't stop it, so I wrote it down."),
              L("My scherzos used to be fairies and moonlight. Not this one.")),
            Q("Is there any consolation in it?",
              # the Adagio, the one place of consolation
              L("The Adagio. One place to rest. Only one."),
              L("In the slow movement I let myself remember her kindly."),
              L("A little. Don't expect it to last.")),
            Q("There is no turn to the major at the end.",
              # the finale stays restless, with no turn to the major
              L("No. I couldn't find one."),
              L("Restless to the end. I won't lie to her memory with a happy chord."),
              L("F minor, start to finish. Some things don't resolve.")),
            Q("What was Fanny like?",
              # FM: a talented composer and pianist
              L("A composer and pianist, as gifted as anyone I knew."),
              # FM: Fanny Hensel
              L("Fanny Hensel, after her marriage. To me, always just Fanny."),
              L("I always wanted her to hear things first. Who will I play to now?")),
            Q("You brought Bach back to life, they say.",
              # FM: conducted the St Matthew Passion in Berlin, 1829, first outside Leipzig since Bach's death
              L("The St Matthew Passion, in Berlin, in 1829. Its first time outside Leipzig since Bach died."),
              L("I only conducted it. Bach did the rest."),
              # FM: grandson of the philosopher Moses Mendelssohn
              L("My grandfather Moses was a philosopher. I suppose I like bringing old things back.")),
            Q("Did you love Scotland?",
              # FM: the trip inspired The Hebrides and the Scottish Symphony
              L("The Hebrides gave me an overture, and Scotland a symphony. And rain."),
              # FM: worked in pencil and watercolour
              L("I drew and painted everywhere I went. Scotland too."),
              L("Today I can't think of Scotland. Ask me another year.")),
        ],
        close=[
            L("I'm tired. The strings can finish without me."),
            L("Go gently. Tell no one I wept."),
            L("The finale won't rest. Neither will I. Goodnight."),
            me("The shuddering strings fade, and he is only a shape at the window."),
        ]),

    # ---- Mozart ------------------------------------------------------------------
    "String Quartet No. 15 in D minor, K. 421": dict(
        # src: W+"String_Quartet_No._15_(Mozart)" and its NOTES unless noted (fetched Oct 2026)
        open=[
            # Constanze in labour in the other room (her account to the Novellos)
            L("Shh. Constanze is in the next room, and I'm writing in D minor. Sit, quietly."),
            L("Welcome. A child is coming any hour. My hands wanted something to do."),
            # the only minor-key quartet of the six dedicated to Haydn
            L("You're here for the quartets for Haydn? This is the dark one."),
            L("Come in! Excuse the noise. Everything in this house is happening at once."),
        ],
        qa=[
            Q("Is it true you wrote this while Constanze was in labour?",
              # Constanze's account to Vincent and Mary Novello, 1829
              L("So she told the Novellos, in 1829. Who am I to argue with my wife?"),
              # first child, Raimund; she was in the other room
              L("Our first child, Raimund. She was in the next room. I had a quartet to finish."),
              L("Constanze tells it so, years later. She remembers it better than I do.")),
            Q("Are her cries really in the music?",
              # Constanze said the rising string figures matched her cries from the other room
              L("She said the rising figures were her cries. Perhaps they are."),
              L("She says so. I say a composer listens to everything."),
              L("Ask her. I'm not brave enough to contradict her.")),
            Q("Why D minor?",
              # the only one of the set in a minor key
              L("Five of the six are in major keys. One needed shadows."),
              L("D minor is a serious key. Today was a serious day."),
              L("Haydn would expect variety. I gave him a storm.")),
            Q("Who are these quartets for?",
              # dedicated to Haydn; the second of the set
              L("For Haydn. He showed us all how quartets are written."),
              L("Six for Haydn. This is the second, and the only one in a minor key."),
              L("For Haydn, with love and some fear. He'll notice everything.")),
            Q("The minuet is dark, but the trio...?",
              # the trio "almost embarrassingly lightweight on its own", "a wonderful foil"
              L("Light as anything. A wonderful foil, someone will say."),
              L("After the shadows, a little dance in the major. One must breathe."),
              L("Almost too light on its own. Next to the minuet, exactly right.")),
            Q("How does it end?",
              # variations ending on a Picardy third
              L("Variations, and then the last chord turns to D major. A Picardy third."),
              L("In the minor, nearly. At the last moment, a little light."),
              L("With a set of variations. I can never resist variations.")),
            Q("What happens in the Andante?",
              # Andante in F major, calm, broken by sighing pauses
              L("F major, calm, and then sudden pauses, like sighs."),
              L("It's peaceful until it isn't. Listen for the breaths."),
              L("A lullaby, perhaps, for someone not yet born.")),
            Q("How does the first movement begin?",
              # a quiet, troubled opening in D minor
              L("Quietly, troubled, in D minor. The cello knows something the others don't."),
              L("Softly, as if everyone in the house were listening."),
              L("Allegro moderato. Not too fast; I was distracted.")),
        ],
        close=[
            L("I'm needed in the next room. Forgive me!"),
            L("Listen for the last chord. A little light, at the very end."),
            L("A baby is crying somewhere. Goodbye, goodbye!"),
            me("The D-minor shadows thin, and the last chord turns to light."),
        ]),

    "String Quartet No. 19 in C major, K. 465": dict(
        # src: W+"String_Quartet_No._19_(Mozart)" and its NOTES unless noted
        open=[
            # the last of the six dedicated to Haydn
            L("Ah, welcome! The ink's still wet. Haydn is coming to hear these."),
            L("Come in. You've heard the opening? Don't worry, it gets better. Much better."),
            L("The last of the six for Haydn. Sit, before I change something."),
            L("Good evening! Let me finish this bar, then I'm all yours."),
        ],
        qa=[
            Q("Your opening sounds wrong on purpose.",
              # the 22-bar slow introduction
              L("Twenty-two bars of fog before the sun comes out."),
              # quiet repeated Cs in the cello, strange harmonies
              L("On purpose, yes. Quiet Cs in the cello, and the harmonies wander."),
              L("Wrong? No. Strange. There's a difference.")),
            Q("A critic complained in print.",
              # a critic complained in print in 1787
              L("In 1787, yes. Complaints mean people listened."),
              L("Let him. I wrote it for Haydn's ears, not his."),
              L("Critics like everything in its place. I like surprises.")),
            Q("Then the Allegro arrives.",
              # the Allegro breaks into clear C major
              L("In clear C major, like opening the shutters."),
              L("After the fog, sunlight. That's the whole joke."),
              L("You see? You needed the fog to enjoy the sun.")),
            Q("What did Haydn say about you?",
              # Leopold Mozart's letter of 16 February 1785, quoting Haydn (well documented)
              L("He told my father I'm the greatest composer he knows, in person or by name."),
              L("Kind things, to my father. Father nearly smiled."),
              # same letter: "taste and ... the most profound knowledge of composition"
              L("That I have taste, and the deepest knowledge of composition. I may frame it.")),
            Q("Why dedicate six quartets to Haydn?",
              L("He taught us all how quartets are written. These are my thanks."),
              # Mozart's dedication calls the quartets his six children (well documented)
              L("My six children, I call them in the dedication. I hand them to him."),
              # completed on 14 January 1785, the last of the six
              L("This is the last of the six. I finished it in January 1785.")),
            Q("What is the Andante like?",
              # Andante cantabile in F major
              L("Cantabile, in F major. Singing and unhurried. After the fog, a song."),
              L("Unhurried. I'm always in a hurry; the music needn't be."),
              L("Let the first violin sing, and the others hold their breath.")),
            Q("And the minuet?",
              # Menuetto: Allegro; its trio turns to C minor
              L("A brisk minuet, and then the trio turns to C minor, just for a moment."),
              L("A dance with a frown in the middle. That's the trio."),
              L("Even dances need a shadow, or they're only exercise.")),
            Q("How does the finale feel?",
              # Allegro molto: a quick-witted finale
              L("Allegro molto. Quick-witted. The players had better be awake."),
              L("Like a good supper: fast, and everyone talking at once."),
              L("Fun. After the fog, I owe you some fun.")),
        ],
        close=[
            L("Haydn's at the door! Go, go, I must play him the opening."),
            L("The finale's running away with us. Goodbye!"),
            L("Twenty-two bars of fog, and then the sun. Remember that."),
            me("His laughter outruns the finale, and the room brightens and is gone."),
        ]),

    # ---- Suk ---------------------------------------------------------------------
    "Meditation on the Old Czech Chorale 'St. Wenceslas', Op. 35a": dict(
        # src: imslp.org Meditation_..._(Suk,_Josef) and its NOTES unless noted; 1914, patriotic,
        # a wartime symbol of hope (confirmed by Jeem); JS = W+"Josef_Suk_(composer)"
        open=[
            # written in 1914 as a patriotic piece
            L("Welcome. It's 1914, and Bohemia needs its old hymns. Sit and listen."),
            # JS: played with the Czech Quartet until 1933
            L("Come in. I'm a quartet player first. This piece is for my own kind."),
            # the old chorale to Saint Wenceslas, the Czech patron saint
            L("Good evening. Saint Wenceslas has watched over us for centuries."),
            L("Ah, you found me. Quietly, please. This is a prayer, not a concert."),
        ],
        qa=[
            Q("Why the St Wenceslas chorale?",
              # the old Czech chorale; 1914
              L("It's the old hymn to our patron saint. In 1914, we needed something to hold."),
              L("Every Czech knows it by heart. That was the point."),
              L("Wenceslas is our patron. I asked him, in music, to look after us.")),
            Q("Was it meant as a patriotic piece?",
              # patriotic, at the start of the war
              L("Yes. A Czech hymn, played as the war began. Everyone understood."),
              # it became a wartime symbol of hope
              L("It became a symbol of hope in the war. I only wrote the notes."),
              L("Patriotic, quietly. No drums. Just strings and a hymn.")),
            Q("Who taught you?",
              # JS: one of Dvořák's favourite pupils
              L("Dvořák. I was one of his favourite pupils, they say."),
              # JS: married Dvořák's daughter Otilie in 1898
              L("Dvořák taught me, and then I married his daughter Otilie."),
              L("Master Dvořák. Everything I know, I learned in his classroom or at his table.")),
            Q("You lost them both, didn't you?",
              # JS: Dvořák died 1904; Otilie a year later; they inspired the Asrael Symphony
              L("Dvořák in 1904, and Otilie a year later. I wrote Asrael for them."),
              L("Asrael is the angel of death. I gave him a whole symphony."),
              L("Yes. Some of my music since has been for them, whatever its title.")),
            Q("Why for string quartet?",
              # JS: the Czech Quartet
              L("I play in a quartet. I know what four strings can carry."),
              # for string quartet or string orchestra
              L("Quartet or string orchestra, either. A hymn should fit any church."),
              L("Four players can be as loud as a crowd, if they mean it.")),
            Q("Who is it dedicated to?",
              # dedicated to Ferdinand Pečírka
              L("To Ferdinand Pečírka. A friend, and he knows why."),
              L("Pečírka's name is on the page. The music is for everyone."),
              L("To a friend. Hymns are always for more than one person.")),
            Q("What happens at the climax?",
              # the chorale builds to its fullest sound
              L("The chorale rises to its fullest sound. Then it bows its head again."),
              L("Everything I have, in four parts. Then quiet."),
              L("It swells like a congregation finding its voice.")),
            Q("Do you still play in the quartet?",
              # JS: played with the Czech Quartet until he retired in 1933
              L("The Czech Quartet, yes, for most of my life. I'll retire when my fingers ask."),
              L("Every evening a different hall, the same four chairs."),
              L("Yes. Composing is lonely. A quartet never is.")),
        ],
        close=[
            L("The hymn is ending. Let it end quietly; that's how prayers end."),
            L("Go home safely. These are hard years."),
            L("Saint Wenceslas, look after this one too."),
            me("The chorale fades, and I hear only my own breath, steadier."),
        ]),

    # ---- Schubert ----------------------------------------------------------------
    # FS = W+"Franz_Schubert" (fetched Oct 2026)
    "Piano Sonata in E-flat major, D. 568": dict(
        # src: W+"Piano_Sonata_in_E-flat_major,_D_568_(Schubert)" and its NOTES unless noted
        open=[
            # drafted in June 1817, at 20
            L("Come in, come in. I'm twenty, and I've written too many songs today."),
            # FS: Joseph von Spaun, a friend who promoted his work
            L("A friend of Spaun's? Sit. There's wine, and a piano with most of its keys working."),
            # FS: born in Himmelpfortgrund, Vienna
            L("Welcome to Himmelpfortgrund. Heaven's Gate, the name means. The rent is less heavenly."),
            # FS: worked at his father's school
            L("Good evening. Father thinks I'm marking schoolwork. I'm not."),
        ],
        qa=[
            Q("You began this in D-flat?",
              # first drafted in D-flat major, June 1817; revised and finished in E-flat
              L("In June 1817. Later I moved it to E-flat and finished it."),
              L("D-flat felt too soft. E-flat stands up straighter."),
              L("I changed the key and kept the heart.")),
            Q("Did you see it published?",
              # published in 1829, the year after his death
              L("No. They printed it the year after I died."),
              L("No. Most of my sonatas waited in drawers."),
              L("Not in my lifetime. Music is patient. I wasn't given the time.")),
            Q("What is the slow movement?",
              # Andante molto in G minor (key confirmed by Jeem)
              L("Andante molto, in G minor. A sad little song, walking slowly."),
              L("A song without a singer. I write songs all day; some escape into sonatas."),
              L("Sorrowful, yes. I'm twenty. Twenty-year-olds are very sorrowful.")),
            Q("Who taught you?",
              # FS: Salieri taught composition; his father violin; his brother Ignaz piano
              L("Salieri taught me composition. Father the violin, and my brother the piano."),
              # FS: at the Stadtkonvikt he encountered Haydn, Mozart and Beethoven
              L("At the Stadtkonvikt I heard Haydn, Mozart and Beethoven. That was my real school."),
              # FS: he soon surpassed Ignaz at the piano
              L("Ignaz taught me piano until I overtook him. He forgave me, mostly.")),
            Q("Do you like teaching at your father's school?",
              # FS: teaching at his father's school, which he found unfulfilling
              L("No. Children and arithmetic. I'd rather write a song."),
              L("Father wants a schoolmaster. I want an evening free."),
              L("I teach in the mornings and write the rest of the time. Badly arranged.")),
            Q("How does the sonata open?",
              # a gentle, singing opening theme, unhurried
              L("With a gentle, singing theme. It never rushes, even when it develops."),
              L("Allegro moderato. Moderate. I'm a moderate man, except at parties."),
              L("Like a song with the words taken away.")),
            Q("What is the minuet like?",
              # a graceful dance with a contrasting trio
              L("Graceful, with a contrasting trio. A dance for a Viennese evening."),
              L("Light. My friends dance badly to it."),
              L("A minuet for people who'd rather be waltzing.")),
            Q("And the finale?",
              # a relaxed, flowing finale
              L("Relaxed and flowing. No storms tonight."),
              L("Allegro moderato again. I like to end where I began, more or less."),
              L("It wanders home, the way I do after an evening with friends.")),
        ],
        close=[
            L("My friends are calling from the street. I must go."),
            L("Back to the schoolroom tomorrow. Let me have tonight."),
            L("Play it gently. Everything I write wants to be sung."),
            me("He smiles behind his spectacles and fades into the flowing finale."),
        ]),

    "Piano Sonata in A major, D. 664": dict(
        # src: W+"Piano_Sonata_in_A_major,_D_664_(Schubert)" and its NOTES unless noted
        open=[
            # written in summer 1819 in Steyr, Upper Austria
            L("Welcome to Steyr! Mountains, fresh air, and very kind people."),
            L("Come in. It's summer, and I'm on holiday. Even my sonatas are smiling."),
            # dedicated to Josephine von Koller
            L("Ah, you've met Josephine? Then you know why this sonata sings."),
            L("Good evening. Upper Austria agrees with me. Vienna can wait."),
        ],
        qa=[
            Q("Who was Josephine?",
              # Josephine von Koller, 18; "very pretty", "a good pianist"
              L("Josephine von Koller, in Steyr. Eighteen, very pretty, and a good pianist."),
              L("A good pianist. That's the first thing, of course. The second too."),
              L("A young pianist in Steyr. I wrote it for her hands.")),
            Q("When did you write it?",
              # summer 1819, Steyr
              L("In the summer of 1819, on holiday in Upper Austria."),
              L("On a summer holiday. You can hear it, can't you?"),
              L("Between walks. Sonatas come easier with fresh air.")),
            Q("Why is the opening so lyrical?",
              # one of his most lyrical openings, a melody that seems to sing itself
              L("It's a song, really. The melody sings itself; I just wrote it down."),
              L("I write songs all the time. My piano music can't help it."),
              L("Allegro moderato. Unhurried. It's summer.")),
            Q("What is the Andante like?",
              # Andante in D major, quiet and inward
              L("D major, quiet and inward. Someone thinking aloud at dusk."),
              L("Short. A sigh between two smiles."),
              L("Andante. Walking pace. Holiday pace.")),
            Q("And the finale?",
              # a light, dancing finale
              L("Light and dancing. Let your hands enjoy it."),
              L("A dance for a summer evening. Nothing heavy."),
              L("Quick fingers, light heart.")),
            Q("Who brings you to Upper Austria?",
              # FS: the baritone Johann Michael Vogl promoted his work
              L("My friend Vogl, the baritone. He sings my songs to anyone who'll listen."),
              L("Friends. I have the best friends. They feed me and find me pianos."),
              L("Summer, and a reason to leave Vienna.")),
            Q("What do you think of Beethoven?",
              # FS: admired Beethoven throughout his life
              L("I admire him more than anyone. Meeting him is another matter."),
              L("Beethoven? I'd sooner talk to a mountain. It's less frightening."),
              L("Not here. Here there's only Josephine, and the hills.")),
            Q("Do you have many friends?",
              # FS: Spaun, Schober and Vogl promoted his work
              L("Spaun, Schober, Vogl. They push my music into every drawing room."),
              # FS: their gatherings became known as "Schubertiads"
              L("Enough for a party every week. They call them Schubertiads. I'm embarrassed."),
              L("More friends than money. A good bargain.")),
        ],
        close=[
            L("The holiday's ending. I'll miss these hills."),
            L("Josephine is at the piano. I should go and turn pages."),
            L("Back to Vienna. Back to work. Goodbye!"),
            me("The finale skips away, and the summer light goes with it."),
        ]),

    "Piano Sonata in A minor, D. 784": dict(
        # src: W+"Piano_Sonata_in_A_minor,_D_784_(Schubert)" and its NOTES unless noted
        open=[
            L("Come in. Forgive the cold; I don't go out much this winter."),
            # perhaps a response to the serious illness of the year before
            L("Welcome. I'm not well. The piano doesn't mind."),
            # unlike the songful Schubert of earlier sonatas
            L("Sit. This one is not a song. Don't expect me to smile."),
            # composed in February 1823
            L("Good evening. February in Vienna. Grey outside, grey in here."),
        ],
        qa=[
            Q("What happened the year before?",
              # composed perhaps in response to the serious illness of the year before (hedged on the page)
              L("I was seriously ill. Perhaps that's why there's nothing decorative here."),
              L("Illness. Let's leave it there."),
              L("Something changed. The music stopped wanting to please.")),
            Q("Why bare octaves at the start?",
              # bare octaves, stark and spacious
              L("Stark and spacious. I didn't want decoration, only bones."),
              L("Two hands saying the same thing. Sometimes that's all there is."),
              L("Allegro giusto. Strict time. No sighing allowed.")),
            Q("This isn't the songful Schubert people know.",
              # unlike the songful Schubert of earlier sonatas
              L("No. My earlier sonatas sing. This one stares."),
              L("I can't write sweetly all the time. Not this winter."),
              L("Even a songwriter has days without words.")),
            Q("What is the slow movement?",
              # Andante in F major: a hushed hymn interrupted by murmuring figures
              L("F major, a hushed hymn, with murmuring underneath."),
              L("Quiet, like someone praying without wanting to be heard."),
              L("A short rest before the storm.")),
            Q("And the finale?",
              # a fierce, driving finale
              L("Fierce. It drives on and won't stop for anyone."),
              L("Allegro vivace. Anger, maybe. I don't know."),
              L("Run with it. I couldn't hold it back.")),
            Q("When was it published?",
              # published in 1839, eleven years after his death
              L("In 1839, eleven years after I died."),
              L("Long after me. Nobody was waiting for my sonatas."),
              L("Not in my life. Perhaps it's better heard later.")),
            Q("Who keeps you company now?",
              # FS: Spaun and Schober, friends who promoted his work
              L("My friends. Spaun and Schober still come, even when I'm poor company."),
              # FS: Vogl promoted his songs
              L("Vogl sings my songs to people who've never heard of me."),
              L("The piano. It's patient with me.")),
            Q("Do you still hope?",
              L("Every morning. By evening I've written something, and that's hope enough."),
              L("Yes. Next year will be better. It usually isn't, but I say it."),
              L("Ask me after the finale.")),
        ],
        close=[
            L("I'm tired. Go, and come back in the spring."),
            L("The finale's running. Let it run me out of the room."),
            L("Thank you for sitting with me. Not many do, this winter."),
            me("The bare octaves sound again in my head as he fades."),
        ]),

    "Piano Sonata in A minor, D. 845": dict(
        # src: W+"Piano_Sonata_in_A_minor,_D_845_(Schubert)" and its NOTES unless noted
        open=[
            # published as his "Première Grande Sonate"
            L("Welcome! A publisher wants a grand sonata from me. A grand one!"),
            # composed in May 1825
            L("Come in. It's May, and for once things are going well."),
            # the first of only three sonatas printed in his lifetime
            L("Sit. You're about to hear my first grand sonata in print. My first!"),
            # FS: a summer holiday in Upper Austria in 1825
            L("Good day. Soon I'm off to Upper Austria for the summer. First, this."),
        ],
        qa=[
            Q("This one was printed while you lived.",
              # the first of only three Schubert sonatas printed in his lifetime
              L("My first grand sonata in print. Only three ever were, in my lifetime."),
              # "Première Grande Sonate"
              L("'Première Grande Sonate', it says on the title page. Very grand."),
              L("Printed! I held a copy. You have no idea.")),
            Q("How does it open?",
              # a soft, questioning unison phrase
              L("Softly, with both hands in unison, asking a question."),
              L("Moderato. A question first. The answers take the rest of the sonata."),
              L("Quietly. Grand doesn't have to mean loud.")),
            Q("What is in the slow movement?",
              # five variations on a 32-bar theme
              L("Five variations on a simple theme of thirty-two bars."),
              L("A plain tune, then five ways of looking at it."),
              L("Variations. I like to turn a melody over in my hands.")),
            Q("The scherzo has a slower trio.",
              # trio marked "un poco più lento"
              L("Un poco più lento. A little slower, a little sadder."),
              L("Fast, then the trio takes a breath."),
              L("Every busy house needs a quieter room.")),
            Q("How does it end?",
              # Rondo: Allegro vivace, a restless finale
              L("A restless rondo. It keeps coming back, still unsettled."),
              # finale in A minor (key confirmed by Jeem)
              L("Allegro vivace, and no peace. A minor all the way."),
              L("Restless. Like me before a journey.")),
            Q("When did you write it?",
              # May 1825
              L("In May 1825, before a summer in Upper Austria."),
              L("In spring. Things were going well. That doesn't happen often."),
              L("Quickly, once I knew someone would print it.")),
            Q("Are you known in Vienna now?",
              # FS: admitted to the Gesellschaft der Musikfreunde as a performing member
              L("The Gesellschaft der Musikfreunde made me a member. That's something."),
              L("My songs are known. My sonatas, less. This one may help."),
              # FS: his only public concert came in 1828
              L("In some drawing rooms. Not yet in the concert halls.")),
            Q("Will you go to the mountains?",
              # FS: a summer in Upper Austria in 1825, warmly welcomed
              L("Upper Austria this summer. They're very kind to me there."),
              # FS: visited Gastein that year
              L("Yes. Gastein too, perhaps. I'll take paper."),
              L("Anywhere with a piano and a friend.")),
        ],
        close=[
            L("The rondo won't settle. Neither will I. Goodbye!"),
            L("Go and buy a copy! It's printed, you know."),
            L("Summer's coming. Wish me good weather."),
            me("The questioning unison returns, and he slips away before the answer."),
        ]),

    "Piano Sonata in D major, D. 850": dict(
        # src: W+"Piano_Sonata_in_D_major,_D_850_(Schubert)" and its NOTES unless noted
        open=[
            # written at the spa town of Bad Gastein
            L("Welcome to Gastein! Mountains everywhere. Even the piano feels taller."),
            # August 1825
            L("Come in. It's August, and I'm happier than I've been for years."),
            L("You've climbed all this way? Sit, have some water. Spa water."),
            # nickname: the "Gasteiner"
            L("Good day. They call this my Gasteiner. I call it my holiday."),
        ],
        qa=[
            Q("Gastein?",
              # Bad Gastein, August 1825
              L("A spa in the mountains. I wrote this there, in August 1825."),
              L("A spa town. People come to bathe. I came to write."),
              # the nickname "Gasteiner"
              L("Hence the nickname, the Gasteiner. I like being named for a place.")),
            Q("Why such big chords?",
              # big, bright chords that fill the piano
              L("Allegro vivace. I wanted to fill the whole piano."),
              L("The mountain air made me write big chords."),
              L("Sometimes a man wants to be loud. Today is one of those days.")),
            Q("What is the slow movement like?",
              # Con moto: a long, slow-walking movement
              L("Con moto. A long walk, slow and steady, through the valley."),
              L("Long, yes. I like long walks. My friends complain."),
              L("With movement, it says. Not too slow. Keep walking.")),
            Q("The scherzo is so rhythmic.",
              # full of rhythmic energy
              L("Full of energy. You can't sit still for it."),
              L("Rhythm is the mountain stream. It doesn't stop."),
              L("Allegro vivace. Lively. I'm lively this summer.")),
            Q("The finale sounds like a toy march.",
              # a march-like rondo theme, repeated with finer decoration
              L("A playful march, decorated more finely each time it comes back."),
              # interrupted by stormier episodes
              L("And then storms interrupt it. Mountain weather."),
              L("A march for small soldiers. I was a child once too.")),
            Q("Are you well?",
              # FS: illness from 1823
              L("Better. The illness of the last years is quieter now."),
              L("This summer, yes. Ask me in winter."),
              L("Well enough to climb a hill and write a sonata.")),
            Q("Who's with you?",
              L("Friends. I have good friends; they take me everywhere."),
              # FS: warmly welcomed in Upper Austria in 1825
              L("Kind people in Upper Austria. They welcomed me like family."),
              L("My music paper. The best companion; it never complains.")),
            Q("What do you think of Beethoven?",
              # FS: admired Beethoven throughout his life
              L("I admire him more than anyone alive. I hardly dare write sonatas."),
              L("He makes sonatas into mountains. I make mine into valleys."),
              L("Ask me something easier.")),
        ],
        close=[
            L("The march is coming round again. Listen to the decorations."),
            L("I'm off for a walk. Mountains don't wait."),
            L("Thank you for climbing up. Go down carefully."),
            me("The toy march ticks on, and he is a small figure far up the path."),
        ]),

    "Piano Sonata in C minor, D. 958": dict(
        # src: W+"Piano_Sonata_in_C_minor,_D_958_(Schubert)" and its NOTES unless noted
        open=[
            # one of three sonatas written in the last months of his life
            L("Come in. Three sonatas this summer. This is the first, and the stormiest."),
            # FS: torchbearer at Beethoven's funeral in 1827
            L("Welcome. Beethoven has been gone a year. I carried a torch at his funeral."),
            # FS: his only public concert, 26 March 1828, a success
            L("A visitor! I gave a concert of my own this spring. My only one."),
            L("Good evening. I'm tired, but the music isn't."),
        ],
        qa=[
            Q("The opening sounds like Beethoven.",
              # quotes the theme of Beethoven's 32 Variations in C minor
              L("His C minor Variations. I admire him more than anyone."),
              L("Yes. I borrowed his theme to begin. A greeting to him."),
              L("Every pianist knows those variations. I wanted them to hear him in me.")),
            Q("You finished this in September 1828.",
              # he died that November, at 31
              L("And by November I was gone. I didn't know there'd be no time."),
              L("Three sonatas in one summer. I was in a hurry, and didn't know why."),
              L("I was thirty-one. There was so much still to write.")),
            Q("What is the Adagio like?",
              # Adagio in A-flat major, ABABA
              L("A-flat major. Two ideas taking turns, five sections in all."),
              L("One song, then another, then the first again. Patient."),
              L("Slow, because some things shouldn't be hurried.")),
            Q("Why a minuet instead of a scherzo?",
              # a subdued minuet in place of a scherzo
              L("A subdued minuet. I didn't want to joke in this sonata."),
              L("Old-fashioned, yes. Quiet, too."),
              L("Haydn would approve. Beethoven would scowl.")),
            Q("The finale gallops.",
              # a relentless tarantella, hand-crossings and leaps
              L("A tarantella. Hand-crossings, leaps, no rest."),
              L("Relentless. The pianist must survive it."),
              L("It's a dance you dance until you drop.")),
            Q("Tell me about your concert.",
              # FS: 26 March 1828, his only public concert of his own works, a success
              L("My only public concert of my own music, on 26 March 1828. It went well!"),
              L("Friends filled the hall. For one night, Vienna listened."),
              L("A success. I wish Beethoven had been there.")),
            Q("You were at Beethoven's funeral.",
              # FS: a torchbearer at Beethoven's funeral
              L("I carried a torch beside his coffin."),
              L("Half of Vienna was there. I walked and said nothing."),
              # FS: at his own request, buried near Beethoven's grave
              L("I've asked to be buried near him, when my time comes.")),
            Q("Are you afraid?",
              L("Of what? I have three sonatas to finish. There's no time for fear."),
              L("A little. The finale isn't afraid; I wrote it that way."),
              L("Ask me in November.")),
        ],
        close=[
            L("The tarantella's starting. Don't try to keep up."),
            L("Two more sonatas to finish. Excuse me."),
            L("Tell Beethoven, if you see him, I tried."),
            me("The gallop thins to silence, and his chair is empty."),
        ]),

    "Piano Sonata in A major, D. 959": dict(
        # src: the same Wikipedia article as D. 958 and the NOTES unless noted
        open=[
            # the second of the last three sonatas, 1828
            L("Welcome. The second of my three. Sit; this one sings."),
            L("Come in. Autumn's coming. I'm writing as fast as I can."),
            # the Andantino's eruption
            L("You've heard the Andantino? Then you know what's in me."),
            # published in 1839, dedicated to Schumann
            L("Good evening. A man called Schumann will love this one day. Strange to think."),
        ],
        qa=[
            Q("What happens in the middle of the Andantino?",
              # the middle section erupts, improvisatory, harsh modulations, fortissimo chords
              L("The song breaks. Everything I kept quiet comes out at once, then the song returns."),
              L("Harsh modulations, fortissimo chords. It sounds improvised because it nearly was."),
              L("A storm in a lullaby. Don't ask me where it came from.")),
            Q("It's dedicated to Schumann.",
              # the dedication to Robert Schumann on publication in 1839, after his death
              L("After my death, by the publisher. He loved my music, so it's right."),
              # Schumann had championed his music
              L("Robert Schumann. A young man who fought for my music when I couldn't."),
              L("I never met him. He knew me better than some who did.")),
            Q("How does it open?",
              # a grand opening of full chords
              L("With grand, full chords. Like a door thrown open."),
              L("Allegro. Big. Then softer, as if surprised at itself."),
              L("Grandly. I'm allowed to be grand sometimes.")),
            Q("What is the Andantino, before the storm?",
              # F-sharp minor, a quiet, rocking song
              L("F-sharp minor, a quiet rocking song. Like a boat at night."),
              L("Rocking, rocking. Then the storm."),
              L("A song with no words, for someone very tired.")),
            Q("And the scherzo?",
              # Allegro vivace, with a gentler trio
              L("Quick and bright, with a gentler trio. A little laughter."),
              L("Allegro vivace. After that storm, I owed you a joke."),
              L("Light fingers. The pianist deserves a rest.")),
            Q("The finale's tune keeps coming back.",
              # Rondo: the broad, singing theme returns again and again
              L("A rondo. The broad, singing theme returns again and again."),
              L("It's a song I couldn't let go of."),
              L("I like my friends to come back. Tunes too.")),
            Q("When was it published?",
              # 1839
              L("In 1839, more than ten years after me."),
              L("Too late for me to hold a copy."),
              L("Long after. Music waits more patiently than men.")),
            Q("Do you know how little time you have?",
              L("No. I only know there's too much music and not enough candles."),
              L("I don't count days. I count bars."),
              L("Don't tell me. Let me finish the rondo.")),
        ],
        close=[
            L("The rondo's tune again. Hum it on your way home."),
            L("One more sonata to write. Good night."),
            L("Thank Schumann for me, when you meet him."),
            me("The singing theme returns once more, and he does not."),
        ]),

    # ---- Bach --------------------------------------------------------------------
    "Goldberg Variations in G major, BWV 988": dict(
        # src: W+"Goldberg_Variations" and its NOTES unless noted; JSB = W+"Johann_Sebastian_Bach"
        open=[
            # JSB: Thomaskantor in Leipzig, with the St Thomas School
            L("Welcome to Leipzig. Mind the choirboys on the stairs."),
            # JSB: twenty children
            L("Sit, quietly. Somewhere in this house a child is always practising."),
            # the Aria survives in the 1725 notebook for Anna Magdalena Bach
            L("You've come about the Aria? Anna Magdalena has it in her book."),
            L("Come in. Thirty variations, and you want to talk? Very well."),
        ],
        qa=[
            Q("Did you really write this for a count who couldn't sleep?",
              # Forkel's 1802 biography; historians question the story
              L("Forkel tells it so, sixty years later. Historians doubt him. So may you."),
              # published as keyboard practice, the fourth Clavier-Übung (JSB)
              L("Count Kaiserling and his insomnia? A good story. I published it as keyboard practice."),
              L("If it put anyone to sleep, Goldberg was playing it too slowly.")),
            Q("Thirty variations on one tune?",
              # the bass line, not the melody, carries all thirty variations
              L("On one bass. The melody may wander; the bass line holds everything."),
              L("Not the tune. The ground under it. Listen to the bass."),
              L("Thirty, and then the Aria again. A circle.")),
            Q("What about the canons?",
              # every third variation is a canon, the interval widening each time
              L("Every third variation is a canon, each a step wider than the last."),
              L("The first at the unison, then the second, then the third, and onwards."),
              L("Counting keeps the mind honest. A canon is counting that sings.")),
            Q("Why a joke at the end?",
              # a quodlibet of popular tunes instead of a canon at the tenth
              L("A quodlibet: popular tunes woven together over the bass, where a canon should be."),
              L("After so much learning, a little laughter. Even cantors laugh."),
              L("Where you expect a canon at the tenth, you get songs from the street.")),
            Q("Wanda Landowska called one variation the black pearl.",
              # Landowska's "black pearl": the slow G-minor variation
              L("The slow one in G minor. I'm glad someone found it in the dark."),
              L("A pearl? It's a lament. Take it slowly."),
              L("Whoever she is, I hope she plays it slowly.")),
            Q("How did you become cantor here?",
              # JSB: Thomaskantor, responsible for four churches and the St Thomas School
              L("Leipzig made me Thomaskantor. Four churches and a school to feed with music."),
              # JSB: "the leading cantorate in Protestant Germany"
              L("The leading post in Protestant Germany, they say. The pay is less leading."),
              L("Hard work, and a little stubbornness. A little more than a little.")),
            Q("Is it true you were once jailed?",
              # JSB: jailed for almost a month in Weimar for "too stubbornly forcing the issue of his dismissal"
              L("In Weimar, almost a month. I pressed too stubbornly for my dismissal."),
              L("The Duke didn't want to let me go. I didn't want to stay."),
              L("A month to think. I thought mostly about leaving.")),
            Q("Did you really walk to Lübeck?",
              # JSB: an extended leave to hear Buxtehude, about 450 km each way, reportedly on foot
              L("To hear Buxtehude play. Hundreds of kilometres, and I stayed far too long."),
              L("On foot, they say. My boots say so too."),
              L("My employers were not pleased. Buxtehude was worth it.")),
        ],
        close=[
            L("The Aria again. Nothing has changed, and everything has."),
            L("Sleep well. If you can't, Goldberg will play."),
            L("The choir needs me. Go, and practise your counterpoint."),
            me("The Aria returns, and the room settles back into its first shape."),
        ]),

    # ---- Beethoven, Moonlight ------------------------------------------------------
    "Piano Sonata No. 14 'Moonlight' in C-sharp minor, Op. 27 No. 2": dict(
        # src: W+"Piano_Sonata_No._14_(Beethoven)" and its NOTES unless noted (fetched Oct 2026);
        # LvB = W+"Ludwig_van_Beethoven"
        open=[
            L("Come in, quietly. The candles are low and the piano is still warm."),
            # dedicated in 1802 to his pupil Countess Julie "Giulietta" Guicciardi
            L("Welcome. I'm copying out a sonata for my pupil, the young Countess Guicciardi."),
            # LvB: hearing loss from 1798, with severe tinnitus
            L("Speak up a little, will you? My ears have been ringing for some time."),
            # LvB: reputation as an improviser in the salons of the Viennese nobility
            L("Sit. Vienna knows me for improvising. Tonight I'll play something already written down."),
        ],
        qa=[
            Q("Did you call it the Moonlight Sonata?",
              # the nickname came from Rellstab's imagery, not from Beethoven
              L("Never. I wrote 'Sonata quasi una fantasia'. The moonlight belongs to a poet."),
              # Rellstab's story Theodor, 1824: a lake in moon-shimmer
              L("A poet called Rellstab saw moonlight on a lake in it, in 1824. A pretty picture."),
              # critics called the title misleading, the movement almost a funeral march
              L("Moonlight? Some hear a funeral march. Let them argue.")),
            Q("Why 'quasi una fantasia'?",
              # end-weighted: the fast music held off until the third movement
              L("Because it breaks the usual order. The fast music waits until the end."),
              # the companion Op. 27 No. 1 has the same title
              L("Its twin, the other sonata of Op. 27, has the same title. Both wander."),
              # Grove: "sonata in the manner of a fantasy", suggestive of improvisation
              L("A sonata that sounds as if I'm making it up as I go.")),
            Q("Who was Giulietta?",
              # dedicatee, his pupil
              L("My pupil, Countess Julie Guicciardi. The sonata carries her name."),
              L("A pupil. Leave it there."),
              L("Someone I taught, and thought about more than I should have.",
                unsure="his feelings for Guicciardi are not in the fetched sources")),
            Q("How should the first movement be played?",
              # "Si deve suonare tutto questo pezzo delicatissimamente e senza sordino"
              L("With the utmost delicacy, and without dampers. I wrote it at the top."),
              # played pianissimo; the loudest it gets is piano
              L("Softly. It never rises above piano. If you play it loud, you've misread me."),
              # a modern piano sustains much longer than the pianos of Beethoven's time
              L("On my piano the pedal can stay down. Yours rings far longer, so be careful.")),
            Q("Everyone wants the first movement. Does that annoy you?",
              # remark to Czerny: "Surely I've written better things"
              L("Surely I've written better things. I told Czerny so."),
              # very popular in his day, to the point of exasperating him
              L("It was popular even in my day. Popularity is a strange reward."),
              L("They stop listening after the first page. The storm is at the end.")),
            Q("What is the middle movement?",
              # Allegretto: a minuet in D-flat major, the shortest movement
              L("A little minuet in D-flat major. The shortest of the three."),
              # Liszt is said to have called it "a flower between two abysses"
              L("Liszt is said to call it a flower between two abysses. Rather good, for Liszt."),
              L("A breath between the night and the storm.")),
            Q("Why is the finale so violent?",
              # the weightiest movement, placed last
              L("Because the weight belongs at the end. Here the storm comes last."),
              # mostly marked piano; sforzandos and a few fortissimos make the power
              L("Most of it is marked piano. The sforzandos do the shouting."),
              # Rosen: "its ferocity is astonishing"
              L("Two hundred years on, someone will still call its ferocity astonishing. Good.")),
            Q("Were you already losing your hearing?",
              # LvB: told Neate it began in 1798; severe tinnitus
              L("It began a few years before this, with a ringing that never stops."),
              # LvB: letters to Wegeler and Amenda describing the symptoms
              L("I've written to Wegeler and Amenda about it. Few others know."),
              # LvB: on his doctor's advice, Heiligenstadt from April 1802
              L("My doctor wants me in Heiligenstadt next spring. I don't know yet what I'll write there.")),
        ],
        close=[
            L("The candle's nearly out. Let the triplets carry you home."),
            L("The Presto is coming. Hold on to something."),
            L("Go now. And play it softly, whatever they tell you."),
            me("The triplets keep turning, and his voice sinks under them."),
        ]),

    # ---- Debussy, Clair de lune ----------------------------------------------------
    "Suite bergamasque: Clair de lune in D-flat major, L. 75": dict(
        # src: W+"Suite_bergamasque" and its NOTES unless noted (fetched Oct 2026);
        # CD = W+"Claude_Debussy"
        open=[
            # begun around 1890
            L("Come in. It's 1890, or near it. I'm writing pieces I won't let anyone print for years."),
            # revised just before the 1905 publication
            L("Welcome. My publisher wants my old suite back. I'm correcting it, and wincing."),
            L("Shh. Listen to the arpeggios first. We can talk when the moon comes up."),
            L("Good evening. Sit by the window. The light there is better than the lamp."),
        ],
        qa=[
            Q("Where does the title come from?",
              # from Verlaine's poem "Clair de lune"
              L("From Verlaine's poem. His moonlight is sad and beautiful, like this."),
              # originally entitled "Promenade sentimentale", also a Verlaine title
              L("I first called it 'Promenade sentimentale'. Also Verlaine. Moonlight was better."),
              # Verlaine's poem refers to bergamasks in its opening stanza
              L("Verlaine's poem mentions bergamasques. So the whole suite took the name.")),
            Q("Why did you wait so long to publish it?",
              # unwilling: early pieces not in his mature style
              L("They were young pieces, not in my later style. I didn't want them seen."),
              # in 1905 he accepted a publisher's offer, given his fame
              L("A publisher thought my name would sell them by 1905. He was right, irritatingly."),
              # not known how much was written in 1890 and how much in 1905
              L("Nobody knows how much I rewrote. I prefer it that way.")),
            Q("Are you an Impressionist?",
              # CD: said anyone using the term was an imbecile
              L("Anyone who uses that word is an imbecile. I've said so."),
              # CD: the Conservatoire's assessors first applied it, disapprovingly, to Printemps
              L("The Conservatoire used it as an insult first, about my Printemps."),
              L("I write music. Leave the brushstrokes to the painters.")),
            Q("What do you think of Chopin?",
              # CD: "the greatest of them all, for through the piano he discovered everything"
              L("The greatest of them all. Through the piano he discovered everything."),
              # CD: from 1914 supervised the editing of Durand's Chopin edition
              L("One day I'll edit his music for Durand. I owe him respectful gratitude."),
              # CD: he took lessons from Antoinette Mauté de Fleurville
              L("My first real teacher, Madame Mauté, said she'd been his pupil.",
                unsure="Mauté's claim to have studied with Chopin is not in the fetched source")),
            Q("How did you start playing?",
              # CD: first lessons at seven in Cannes, with Jean Cerutti, paid by his aunt
              L("In Cannes, at seven, with an Italian called Cerutti. My aunt paid."),
              # CD: admitted to the Conservatoire at ten
              L("The Conservatoire took me at ten. I was going to be a pianist."),
              # CD: studied piano first, then found his vocation in composition
              L("Then I found I'd rather invent the music than practise it.")),
            Q("How should it be played?",
              # marked andante très expressif, in 9/8
              L("Andante, très expressif. Slowly, but never heavy."),
              # D-flat major
              L("In D-flat major, mostly on the black keys. Let it float."),
              L("As if you were remembering it, not reading it.")),
            Q("Did you know it would become so famous?",
              L("Famous? It was a small piece in a suite I nearly hid."),
              # planned for Fantasia (1940), cut for running time
              L("Disney nearly put it in Fantasia, with herons. They ran out of time."),
              L("I'd have chosen something later. Nobody asks the composer.")),
            Q("Does it belong with the other movements?",
              # Prélude, Menuet, Clair de lune, Passepied
              L("It sits between a Menuet and a Passepied. Old dances, and then this."),
              # the Passepied was first composed as a Pavane
              L("Even the Passepied changed its name. It was a Pavane once."),
              L("Play the whole suite once. Then you may play this alone forever.")),
        ],
        close=[
            L("The moon is behind the clouds again. Goodnight."),
            L("Listen to the last chords. They're the part I like best."),
            L("Go quietly. Verlaine would have walked you home."),
            me("The arpeggios dissolve, and the window goes dark."),
        ]),

    # ---- Chopin, Nocturnes ---------------------------------------------------------
    "Nocturnes, Op. 9 Nos. 1–3, Op. 27 No. 2, Op. 48 No. 1": dict(
        # src: W+"Nocturnes_(Chopin)", W+"Nocturnes,_Op._9_(Chopin)", W+"Nocturnes,_Op._27_(Chopin)",
        # W+"Nocturnes,_Op._48_(Chopin)" and the NOTES unless noted (fetched Oct 2026);
        # FC = W+"Frédéric_Chopin"
        open=[
            # FC: preferred playing in his own apartment for small groups of friends
            L("Come in, but only you. I play best for a few friends, in my own rooms."),
            # FC: he meant to go to Italy; unrest sent him to Paris
            L("Welcome to Paris. I meant to go to Italy, you know."),
            # FC: an annual concert at the Salle Pleyel, which seated three hundred
            L("Sit near the piano. The Salle Pleyel holds three hundred. This room holds us."),
            L("Shh. The lamp is low. Nocturnes don't like bright rooms."),
        ],
        qa=[
            Q("Did you invent the nocturne?",
              # the form was developed by the Irish composer John Field
              L("No, John Field did. I only took it further."),
              # Field is said to have called him a "sickroom talent"
              L("Field heard mine and called me a sickroom talent. I still admire him."),
              # FC: more structured and deeper than Field's; agitated middle sections
              L("His were lovely songs. I gave mine storms in the middle.")),
            Q("Why do the nocturnes sound like singing?",
              # Liszt insisted they were influenced by Bellini's bel canto arias
              L("Liszt says I learned it from Bellini's arias. He isn't wrong."),
              # FC: Friederike Müller: "does not know how to join two notes together"
              L("The worst thing a pupil can do is not know how to join two notes together."),
              # song-like right-hand melody over left-hand broken chords
              L("The right hand sings. The left hand breathes for it.")),
            Q("Who was Op. 9 for?",
              # dedicated to Madame Marie Pleyel; his first published set
              L("Madame Marie Pleyel. It's my first set of nocturnes in print."),
              L("A Pleyel, like my pianos. Paris is a small town.",
                unsure="Marie Pleyel's link to the Pleyel piano firm is not in the fetched sources"),
              L("Three nocturnes, three moods. She may choose her favourite.")),
            Q("Is the E-flat nocturne your favourite?",
              # often regarded as his most famous piece; written at about twenty
              L("Everyone else's favourite. I wrote it at about twenty."),
              # the melody returns three times, more ornamented each time
              L("The melody comes back three times, dressed more richly each time."),
              # senza tempo in the penultimate bar
              L("Wait for the bar near the end marked senza tempo. Then I let go of time.")),
            Q("How much rubato should I use?",
              L("The left hand keeps time. The right hand may borrow, then pay back.",
                unsure="the borrow-and-repay image is not in the fetched sources"),
              # FC: Müller: he hated lingering, dragging and misplaced rubato; strict rhythm
              L("I hate dragging and misplaced rubato. Rhythm first."),
              L("Steal a little time, never the whole bar.")),
            Q("Op. 27 No. 2 has two voices singing together. Who are they?",
              # Huneker: "a song of the sweet summer of two souls"
              L("A critic will call it a song of two souls. I give no names."),
              # FC: he never named an instrumental work beyond genre and number (bar the Funeral March)
              L("I don't name my pieces. Genre and number; the rest is yours."),
              # Johnston on the main cadence near the end
              L("Wait for the cadence near the end. That's where they meet.")),
            Q("The C minor nocturne is so heavy. What happened?",
              # Op. 48 written in 1841; FC: summers at Nohant with Sand, 1839–1846
              L("It's 1841, and the summers at Nohant are long. Let the music say the rest.",
                unsure="that Op. 48 was written at Nohant is not confirmed"),
              # middle section a chorale in C major, then doppio movimento agitato
              L("A chorale in the middle, in C major. Then it breaks into double speed."),
              # Huneker: "the noblest nocturne of them all"; Niecks and Willeby thought it overrated
              L("Someone will call it the noblest of them all. Others will say it's overrated.")),
            Q("Do you miss Poland?",
              # FC: left Warsaw less than a month before the November 1830 Uprising
              L("I left Warsaw less than a month before the uprising. I think of it every day."),
              # FC: his sister Ludwika took his heart to Warsaw
              L("My sister will carry my heart back to Warsaw. The rest of me stays in Paris."),
              # FC: born in Żelazowa Wola, west of Warsaw
              L("I was born in Żelazowa Wola, west of Warsaw. The nights there were quiet like this.")),
        ],
        close=[
            L("The candle is guttering. One more nocturne, then sleep."),
            L("Don't applaud. Just stay a moment in the quiet."),
            L("Go home softly. The night is a better title than any I could give."),
            me("The last chord hangs in the air, and he is gone before it fades."),
        ]),
}
