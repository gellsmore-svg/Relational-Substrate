# Chapter 5: Constrained Chance

Take a lump of carbon from an old campfire and consider a single atom of radioactive carbon-14 inside it. When will that atom decay? On the standard understanding of quantum physics, nobody can say, and not because we lack information. (Some interpretations dispute this; the chapter returns to them below.) The atom has no internal clock counting down. It might decay in the next second or in fifty thousand years. Yet take a sample of many trillions of such atoms, and half of them will have decayed in about 5,730 years, with a precision that lets archaeologists date the campfire. The individual event is open. The collective behaviour is as reliable as a law.

This pairing, open in the particular and exact in the aggregate, is one of the most important facts in this book. It also requires one of the most easily misunderstood words in the English language. This chapter is about chance: what it is, what it is not, and what the Relational Substrate project proposes about it.

## Three meanings of "random"

When people say that something happened "at random", they can mean at least three different things.

They might mean that it was **lawless or arbitrary**: anything could have happened, with no pattern and no reason. They might mean that it was **unpredictable to us**: there was a cause, but we did not know enough to foresee the result. Or they might mean that it was **probabilistic**: governed by definite chances over a definite set of possibilities, so that individual outcomes are open while their frequencies are fixed.

The third meaning is the one that matters here, and it is precisely not the first. A fair die is the simplest example. Each throw is open: any face can come up. But it cannot come up seven, and over thousands of throws each face appears very close to one time in six. The die is not lawless. It is governed by a probability distribution, and the distribution is exact.

To keep this meaning clear, the book uses the word **stochastic**, from a Greek word for aiming at a target. A stochastic process is one whose outcomes are governed by probabilities over defined possibilities. Stochastic does not mean lawless. It does not mean that anything at all can happen. And it does not mean chaotic, which is a different idea again. A *chaotic* system, in the technical sense, is fully deterministic: each state follows from the last by fixed rules, but the system is so sensitive to its starting point that tiny differences grow into large ones, as in the weather. Chaos makes the future hard to predict even though nothing in it is chancy. A stochastic description makes the future a matter of definite probabilities, without being lawless.

Notice what the word does not yet say. Calling a process stochastic says how it is *described*: by probabilities over defined possibilities. It does not by itself say why. The probabilities might express our ignorance of hidden details in a process that is deterministic underneath. Or they might express genuine openness in the world itself, so that the outcome is not fixed until it occurs. The first is called *epistemic* probability, the second *ontic* indeterminacy. The same stochastic description fits both.

## Chance in physics

Radioactive decay is not an isolated curiosity. At the scale of atoms, quantum theory, the most precisely tested theory in physics, gives its predictions as probabilities. It does not say where an electron will be found. It says how likely each place is, and the frequencies of repeated measurements match those probabilities with great precision.

Whether this means nature itself is fundamentally chancy is a different question, and a contested one. On several interpretations of quantum theory, the probabilities express genuine openness in the world: until an outcome occurs, it is not fixed. On others, the probabilities express our ignorance of hidden details, or reflect the way a single deterministic universe looks from inside one of its branches, and the underlying reality is fully determined. These interpretations agree about every measurement made so far. They disagree about what is there. (A different family of theories, which modify the quantum dynamics with spontaneous collapse, make slightly different predictions, and experiments are now testing them.) This is exactly the situation Chapter 2 described: a superbly successful description joined to more than one ontology.

So the book must be careful. It is scientific consensus that quantum predictions are probabilistic. It is not settled whether nature is fundamentally indeterministic.

## The proposal: constrained stochastic actualisation

Into this open question, the Relational Substrate project puts a definite hypothesis. Recall the question left by the previous chapter: if nothing inside the substrate chooses which admissible transition becomes actual, what makes one rather than another actual? The proposal is that **actualisation is fundamentally stochastic** in the ontic sense. Among the transitions that are admissible, which one occurs is genuinely open until it occurs, a matter of chance weighted by tendency. The future, on this hypothesis, is really open within constrained possibility. That openness belongs to the Relational Substrate hypothesis, not to the meaning of the word "stochastic".

The word *constrained* carries most of the weight in that sentence. **Unconstrained** stochasticity, where every conceivable outcome is equally open, would produce a world without stable form: a static of meaningless flicker. **Constrained** stochasticity is chance operating inside the shape of the possible. Admissibility rules out whole regions of possibility entirely. Tendency weights what remains. And, as the next chapters will show, what has already happened can change what is admissible or likely next. Chance, on this proposal, never acts on an open field. It acts within a structure that was there before it.

This is an **RS working hypothesis**, and the book holds it at that strength. It is consistent with the probabilistic character of quantum theory. It does not follow from it, since deterministic interpretations remain viable, and it has not been tested against them. Its value, if it has any, will lie in how much it helps everything else hang together. One piece of that value is already visible. Stable, exact, law-like behaviour does not require that every underlying event be determined in advance. The carbon-14 atoms show this in nature. The project's own experiments showed it in a different and more surprising way.

## Exact answers from chance: the stochastic calculator

In September 2026, the project built a calculator that does arithmetic without ever calculating. To add 17 and 28, it does not apply the rules of addition. It builds two small populations of relations, one standing for 17 and one for 28, each relation carrying a positive or negative orientation. It pours them together and lets them change at random according to a few local rules. Any relation may be re-attached to a different place. A pair of opposite relations may cancel each other out. A neutral pair (one positive and one negative together) may appear or disappear without changing the total. At each step the program chooses at random which allowed change to make. Eventually no further cancellation is possible, the population settles, and the number of surviving relations is read off. A separate, ordinary calculator then checks the answer.

The calculator was run 40,000 times on additions and subtractions, and it gave the correct answer every time. In a sharper test the researchers fixed the entire starting arrangement, every relation in exactly the same place, and ran it 4,000 times with different random choices. All 4,000 runs followed different paths through the space of possible arrangements: no two histories were alike. All 4,000 arrived at the correct answer.

The lesson is precise. **An exact, stable outcome can coexist with a great diversity of chance-driven paths.** Deterministic-looking results at the level of the answer do not require deterministic processes underneath. Every run wandered differently. The number never wavered.

The researchers were scrupulous about the limits of this result, and the book follows them closely. The exactness did not arise from chance. It arose from rules that were built in: the cancellation rule conserves the total, and the starting populations were encoded so that the total was the right answer. Chance supplied the variety of paths; the constraint supplied the identity of the result. When the same rules were run in a fixed order instead of a random one, the answers were also exact, so randomness was compatible with the result but not necessary for it. Multiplication and division needed whole-system bookkeeping that is not purely local. Ordinary computer science explains everything the calculator did. Systems of this broad kind are already studied as chemical reaction networks and population protocols. The researchers concluded that the experiment establishes no new physical law and no unique Relational Substrate mechanism. What it supplies is a concrete, reproducible example of the pattern the project proposes, and a test bench for its vocabulary.

That example is worth having. It is one thing to say in the abstract that chance and exactness can coexist. It is another to watch four thousand different histories, from one identical starting point, arrive at the same number.

## How strict must the constraint be?

The calculator also answered a question about constraint itself. What happens if the rules are not perfectly enforced, if some forbidden changes are occasionally allowed through?

The researchers added a fault: now and then, a relation could be deleted outright, destroying part of the total. They then varied how strictly the rules rejected such faults. With perfect enforcement the answers stayed exact. As enforcement weakened, accuracy fell, smoothly and predictably. There was no sudden collapse at some magic threshold, and no mysterious "deepening well" that drew the system toward the right answer. The falling accuracy was predicted, before the decisive runs, by a simple formula from ordinary probability: the chance that each of the necessary steps survives the faults, multiplied together. Reliability also depended on how long the system was watched. A rule enforced 99.9 per cent of the time still held the right answer in about half of the runs after two thousand steps; given long enough, ordinary probability says it would lose it in all of them.

The modest lesson is that stability is always stability *of something*, *against some kind of disturbance*, *over some length of time*. When later chapters speak of things persisting, the book will try to keep those three qualifiers in view.

## Chance and providence

A Christian reader may feel uneasy at this point. If actualisation is at bottom a matter of chance, is the world slipping out of God's hands? Scripture speaks to this directly, and its answer is unexpectedly calm:

> `The lot is cast into the lap; but the whole disposing thereof is of the LORD.`
> *Proverbs 16:33*

The casting of lots was the ancient world's paradigm of a chance event, and Israel used it in matters as weighty as the division of the land. Scripture does not deny that the lot falls by chance, as far as anything within the lap and the hand can tell. It says that the whole disposing of it belongs to the Lord. Chance is a real feature of how created events unfold, and it is not outside God's governance. Elsewhere the Preacher observes plainly that "time and chance happeneth to them all" (Ecclesiastes 9:11), and the observation is not treated as a threat to God's rule.

The book draws a theological inference here, and it marks it as one. If created actualisation is constrained-stochastic, then chance is a *created mode of actualisation*. It is part of how a non-agentic creation unfolds within possibilities God has shaped. It is not a rival power, and it is not God's uncertainty. God is not waiting to see how the dice fall. He is the Creator of the dice, of the table, of the probabilities, and of the purposes the whole serves. How divine sovereignty relates in detail to created chance is a question Christian thinkers have pondered for centuries, and this book does not claim to settle it. It claims only that constrained chance does not compete with the God of Proverbs 16:33.

## What chance leaves unexplained

The stone on the path has a history in which chance played a part: the settling of grains, the paths of eroding water, the cracks that happened to open. Its present form is one actual history among many admissible ones. Yet it is not a flicker of static. It is a stone, and it will be the same stone tomorrow. If the history beneath it is open at every step, what keeps it the same? The calculator gave a hint: the number survived every path because something was preserved by every allowed change. The next chapter asks what that something is, and proposes that identity itself is best understood in the same way.
