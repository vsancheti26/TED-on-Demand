**Our goal is to develop a software solution that, given a user generated prompt, produces infotainment-type content. The idea is that upon receiving a prompt, the
software will produce a video of educational value on the topic (image and audio).**

**Approach:**
- Build a front end for the user to interact with our website (flask)
- Prompt from our user for a subject for the TED talk.
- Generate a script on the subject that follows the structure of a TED talkb(keytotext, wikipedia).
- The script generation is done in three parts:
  - Firstly, a language model trained on only introductions generates only the introduction for the script.
  - Next, identify a Wikipedia article on the subject and summarize it, making up the body of the text.
  - Lastly, a language model trained on only conclusion paragraphs generates only the conclusion of the script.
- Find relevant images related to the prompt (keybert, icrawler).
- Generate a voiceover using the keywords (gtts).
- Overlay the intro and outro with a video of an animated person talking (moviepy).
- Combine the images and the voice-over into a single video (moviepy).

**Final output:**
- We built the front end using html, css, and flask.
- Models for generating the introduction and conclusion of the script were made using the t5 encoder-decoder using the keytotext library.
- The Wikipedia summary was generated using the python Wikipedia library.
- Relevant images were found using the keybert model to find the correct keywords to google and retrieving images was found using icrawler.
- Voiceovers were generated using the gtts library.
- The images and videos were combined and the final output was generated using the moviepy library.

**Screen recording of a sample run:**
https://www.loom.com/share/3a53151a62db496abff1d4785eea89ce
