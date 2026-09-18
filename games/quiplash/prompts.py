import os
import random
from typing import List, Dict, Any, Optional, Set

STATIC_QUIPLASH_PROMPTS = [
    "The worst thing to find in your burrito.",
    "A terrible slogan for a funeral home.",
    "Something you shouldn't say to your mother-in-law.",
    "A surprising new feature for the next iPhone.",
    "A bad first line for your presidential inauguration speech.",
    "A bad thing to say to a cop as he writes you a speeding ticket.",
    "A good fake name to use when checking into a hotel.",
    "A good sign that your house is haunted.",
    "A good way to get fired on your very first day.",
    "A great name to have on a fake I.D.",
    'A great new invention that starts with "Automatic".',
    "A great opening line to start a conversation with a stranger at a party.",
    "A name for a brand of designer adult diapers.",
    "A not-very-scary name for a pirate captain.",
    "A rejected crayon color from Crayola.",
    "A terrible name for a 1930s mobster.",
    "A terrifying fortune cookie fortune.",
    "A Tweet from a confused caveman.",
    "The #1 tourist attraction in Hell.",
    "An angry 1-star Yelp review you'd give this game.",
    "Come up with the name of a country that definitely doesn't exist.",
    "A fun thing to do if locked in the mall overnight.",
    "Graffiti you might find in a kindergarten classroom.",
    "If animals took over, an exhibit you'd see at the human zoo.",
    "Name a new movie starring a talking goat who is president.",
    "One thing you should never do on a first date.",
    'Really awful cheerleaders would yell "_____!"',
    "Something you can only do in a Walmart if no one is looking.",
    "Something you probably shouldn't pack for a trip to the Sahara Desert.",
    "Something you shouldn't wear to a job interview.",
    "Something you'd be alarmed to see a donkey do.",
    "The best thing about living in an igloo.",
    "The best (or worst) way to start your Monday morning.",
    "The crime you would commit if you knew you'd get away with it.",
    "The last person you'd ever invite to your birthday party.",
    "The most ridiculous Guinness World Record to break.",
    "The name of a clothing store for oversized leprechauns.",
    "The name of a font that should be outlawed.",
    "The sound a tree actually makes when it falls in an empty forest.",
    "The worst Halloween costume for a young toddler.",
    "The worst stage name for a rap artist.",
    "The worst name for a home assistant robot.",
    "The worst words to begin a wedding toast with.",
    "The worst words for the priest to say at a funeral.",
    "Something you'd be horrified to hear a pilot say over the intercom.",
    "The secret ingredient in grandma's mystery soup.",
    "A new Olympic sport that anyone could win with zero training.",
    "The weirdest reason to break up with someone via text.",
    "A secret room inside the White House that nobody talks about.",
    "What dogs would say if they could speak human for 5 minutes.",
    "What kittens are really thinking when they stare into space."
]

ACRONYMS = (
    "A.P.C. H.N.G. T.F.J. R.M.C. F.G.O. P.P.P. S.W.D. G.D.W. C.A.L. U.B.M. "
    "R.D.S. W.H.F. B.O.P. N.J.C. D.Y.S. B.B.L. U.H.I. S.K.E. O.P.F. M.E.M. "
    "G.S.D. K.P.L. Q.C.B. S.H.N. D.P.D. W.A.W. J.M.T. K.L.C. R.T.O. G.O.R."
).split()

WORDS = (
    "PORK MULE PANTS TAINT DUMP PUMP LICK DUCK WART NUN BEARD OINK NUT CORN "
    "BUNS TROUT BUMP CLOWN APE FLOP SCREW TUB CHEEK SCAB SQUEEZE PUKE FUDGE "
    "BREAD FORK KILL GREASE GAS ZIT WIG SQUID HONK CHUNK SQUIRT DORK TOOTH "
    "MOIST SPANK ITCH SLIME"
).split()

TEMPLATES = [
    "Come up with a new hilarious sitcom with this word in the title: {}",
    "Come up with a new TV show with this word in the title: {}",
    "Come up with a hit song with this word in the title: {}",
    "Come up with a romantic comedy film with this word in the title: {}",
    "Come up with a classic novel with this word in the title: {}",
    "Come up with a new sport with this word in its name: {}",
    "Come up with an award-winning movie with this word in its title: {}",
    "Come up with a shocking newspaper headline with this word in its title: {}",
    "Come up with a new cartoon character with this word in their name: {}",
    "Come up with a hot new Broadway musical with this word in its name: {}",
    "Come up with a fast food restaurant with this word in its name: {}",
    "Come up with a hit new video game with this word in its title: {}",
    "Come up with a music group with this word in their name: {}",
    "Come up with a clever insult using this word: {}",
    "Come up with a flashy wrestling move with this word in its name: {}",
    "Come up with a new snack food with this word in its name: {}",
    "Come up with a hot new website with this word in its name: {}"
]

def load_quiplash_prompts() -> List[Dict[str, Any]]:
    prompts: List[Dict[str, Any]] = []
    seen = set()

    # 1. Static prompts
    for p in STATIC_QUIPLASH_PROMPTS:
        if p not in seen:
            seen.add(p)
            prompts.append({"prompt": p, "image": None})

    # 2. Acronym prompts
    for acro in ACRONYMS:
        p_text = f"Come up with a funny meaning for the acronym: {acro}"
        if p_text not in seen:
            seen.add(p_text)
            prompts.append({"prompt": p_text, "image": None})

    # 3. Template generated unique prompts
    for t in TEMPLATES:
        for w in WORDS[:4]:  # Deterministic combinations
            p_text = t.format(w)
            if p_text not in seen:
                seen.add(p_text)
                prompts.append({"prompt": p_text, "image": None})

    # 4. Image comic strip prompts
    image_dir = './static/images'
    if os.path.exists(image_dir):
        comic_idx = 1
        for filename in sorted(os.listdir(image_dir)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                p_text = f"Fill in the empty dialogue for Comic #{comic_idx}:"
                if p_text not in seen:
                    seen.add(p_text)
                    prompts.append({
                        "prompt": p_text,
                        "image": f"/static/images/{filename}"
                    })
                    comic_idx += 1

    return prompts

_CACHED_QUIPLASH_PROMPTS: Optional[List[Dict[str, Any]]] = None

def get_random_quiplash_prompts(count: int = 10, used_prompts=None) -> List[Dict[str, Any]]:
    global _CACHED_QUIPLASH_PROMPTS
    if _CACHED_QUIPLASH_PROMPTS is None:
        _CACHED_QUIPLASH_PROMPTS = load_quiplash_prompts()
    if used_prompts is None:
        used_prompts = set()
    available = [p for p in _CACHED_QUIPLASH_PROMPTS if p.get("prompt") not in used_prompts]
    if len(available) < count:
        used_prompts.clear()
        available = list(_CACHED_QUIPLASH_PROMPTS)
    random.shuffle(available)
    selected = available[:count]
    for p in selected:
        used_prompts.add(p.get("prompt", ""))
    return selected
