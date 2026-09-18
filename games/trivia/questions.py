import random
from typing import List, Dict, Any

TRIVIA_QUESTIONS: List[Dict[str, Any]] = [
    # =========================================================================
    # MULTIPLE CHOICE (Classic 4 choices)
    # =========================================================================
    {
        "type": "multiple_choice",
        "question": "Which planet in our solar system rotates clockwise (retrograde)?",
        "category": "Science & Space",
        "options": ["Venus", "Mars", "Jupiter", "Neptune"],
        "answer": "Venus",
        "explanation": "Venus rotates east-to-west (clockwise), unlike most other planets."
    },
    {
        "type": "multiple_choice",
        "question": "What is the collective noun for a group of flamingos?",
        "category": "Nature & Animals",
        "options": ["A Flamboyance", "A Sparkle", "A Parade", "A Squadron"],
        "answer": "A Flamboyance",
        "explanation": "A group of flamingos is officially known as a flamboyance."
    },
    {
        "type": "multiple_choice",
        "question": "Which video game character made his first appearance as 'Jumpman' in 1981?",
        "category": "Video Games",
        "options": ["Mario", "Sonic", "Mega Man", "Pac-Man"],
        "answer": "Mario",
        "explanation": "Mario was originally named Jumpman in the arcade classic Donkey Kong."
    },
    {
        "type": "multiple_choice",
        "question": "What is the only letter that does not appear anywhere on the Periodic Table?",
        "category": "Chemistry & Science",
        "options": ["J", "Q", "X", "Z"],
        "answer": "J",
        "explanation": "The letter J does not appear in any chemical element symbol or name."
    },
    {
        "type": "multiple_choice",
        "question": "In what country was the Hawaiian pizza invented?",
        "category": "Food & Culture",
        "options": ["Canada", "United States", "Italy", "Australia"],
        "answer": "Canada",
        "explanation": "Hawaiian pizza was invented in 1962 by Sam Panopoulos in Chatham, Ontario, Canada."
    },
    {
        "type": "multiple_choice",
        "question": "Which animal produces cube-shaped poop?",
        "category": "Absurd Nature",
        "options": ["Wombat", "Platypus", "Koala", "Tasmanian Devil"],
        "answer": "Wombat",
        "explanation": "Wombats produce cubic scat to mark territory without it rolling away."
    },
    {
        "type": "multiple_choice",
        "question": "What was the first feature-length animated movie ever released?",
        "category": "Movies & Entertainment",
        "options": ["Snow White and the Seven Dwarfs", "Pinocchio", "Fantasia", "Bambi"],
        "answer": "Snow White and the Seven Dwarfs",
        "explanation": "Disney released Snow White in December 1937."
    },
    {
        "type": "multiple_choice",
        "question": "How many hearts does an octopus have?",
        "category": "Nature & Animals",
        "options": ["3", "1", "2", "4"],
        "answer": "3",
        "explanation": "An octopus has three hearts: two pump blood to the gills, one to the body."
    },
    {
        "type": "multiple_choice",
        "question": "In Minecraft, what monster was created from a coding glitch on a pig model?",
        "category": "Video Games",
        "options": ["Creeper", "Enderman", "Zombie Pigman", "Ghast"],
        "answer": "Creeper",
        "explanation": "Notch accidentally swapped height and length on a pig model, creating the Creeper!"
    },
    {
        "type": "multiple_choice",
        "question": "Which human bone is the longest and strongest?",
        "category": "Human Anatomy",
        "options": ["Femur (Thighbone)", "Tibia (Shinbone)", "Humerus (Upper Arm)", "Fibula"],
        "answer": "Femur (Thighbone)",
        "explanation": "The femur is both the longest and strongest bone in the human skeleton."
    },
    {
        "type": "multiple_choice",
        "question": "What is the name of the dot over the lowercase letter 'i' or 'j'?",
        "category": "Language & Trivia",
        "options": ["Tittle", "Pip", "Dotlet", "Jot"],
        "answer": "Tittle",
        "explanation": "The small dot above lowercase i and j is called a tittle."
    },
    {
        "type": "multiple_choice",
        "question": "What color is the 'black box' flight recorder on commercial airplanes?",
        "category": "Aviation & Tech",
        "options": ["Bright Orange", "Pitch Black", "Neon Yellow", "Red"],
        "answer": "Bright Orange",
        "explanation": "Flight recorders are painted bright orange with reflective tape to aid ocean recovery."
    },
    {
        "type": "multiple_choice",
        "question": "Which famous artist co-designed the Chupa Chups lollipop logo in 1969?",
        "category": "Art & History",
        "options": ["Salvador Dalí", "Pablo Picasso", "Andy Warhol", "Claude Monet"],
        "answer": "Salvador Dalí",
        "explanation": "Salvador Dalí drew the iconic daisy logo on a newspaper napkin in a cafe."
    },
    {
        "type": "multiple_choice",
        "question": "What was Google's original search engine project name in 1996?",
        "category": "Tech History",
        "options": ["BackRub", "Googol", "WebCrawler", "PageRank"],
        "answer": "BackRub",
        "explanation": "Larry Page and Sergey Brin originally called their search algorithm BackRub."
    },
    {
        "type": "multiple_choice",
        "question": "What flavor is the liqueur Cointreau?",
        "category": "Food & Drink",
        "options": ["Orange", "Almond", "Anise", "Coffee"],
        "answer": "Orange",
        "explanation": "Cointreau is a clear, orange-flavored triple sec liqueur from France."
    },
    {
        "type": "multiple_choice",
        "question": "Which mammal is the only one capable of sustained, powered flight?",
        "category": "Nature & Animals",
        "options": ["Bat", "Flying Squirrel", "Sugar Glider", "Colugo"],
        "answer": "Bat",
        "explanation": "Bats are true flying mammals; flying squirrels and gliders merely glide."
    },
    {
        "type": "multiple_choice",
        "question": "What is the speed of sound at sea level in dry air at 20°C?",
        "category": "Physics",
        "options": ["343 m/s (767 mph)", "299 m/s (670 mph)", "450 m/s (1006 mph)", "512 m/s (1145 mph)"],
        "answer": "343 m/s (767 mph)",
        "explanation": "Sound travels through room-temperature air at approximately 343 meters per second (Mach 1)."
    },

    # =========================================================================
    # SLIDER QUESTIONS (Guess the number / range)
    # =========================================================================
    {
        "type": "slider",
        "question": "In what year did the RMS Titanic sink after hitting an iceberg?",
        "category": "History Slider",
        "min": 1900,
        "max": 1930,
        "step": 1,
        "unit": "",
        "answer": 1912,
        "explanation": "The Titanic sank on the night of April 14-15, 1912."
    },
    {
        "type": "slider",
        "question": "What percentage of the Earth's surface is covered by water?",
        "category": "Earth Science Slider",
        "min": 0,
        "max": 100,
        "step": 1,
        "unit": "%",
        "answer": 71,
        "explanation": "Oceans and waterways cover about 71% of Earth's surface."
    },
    {
        "type": "slider",
        "question": "In what year was the very first Apple iPhone released by Steve Jobs?",
        "category": "Tech Slider",
        "min": 2000,
        "max": 2015,
        "step": 1,
        "unit": "",
        "answer": 2007,
        "explanation": "Steve Jobs introduced the original iPhone in January 2007."
    },
    {
        "type": "slider",
        "question": "How many keys are on a standard modern acoustic piano?",
        "category": "Music Slider",
        "min": 50,
        "max": 120,
        "step": 1,
        "unit": "keys",
        "answer": 88,
        "explanation": "A standard piano features 88 keys: 52 white keys and 36 black keys."
    },
    {
        "type": "slider",
        "question": "How many bones does a shark's skeleton contain?",
        "category": "Nature Trick Slider",
        "min": 0,
        "max": 300,
        "step": 1,
        "unit": "bones",
        "answer": 0,
        "explanation": "Sharks have 0 bones! Their skeletons are made entirely of cartilage."
    },
    {
        "type": "slider",
        "question": "How many teeth does an adult human normally have (including wisdom teeth)?",
        "category": "Anatomy Slider",
        "min": 16,
        "max": 48,
        "step": 1,
        "unit": "teeth",
        "answer": 32,
        "explanation": "A full adult set consists of 32 teeth (8 incisors, 4 canines, 8 premolars, 12 molars)."
    },
    {
        "type": "slider",
        "question": "How many muscles does a domestic cat have in each individual ear?",
        "category": "Animal Slider",
        "min": 5,
        "max": 60,
        "step": 1,
        "unit": "muscles",
        "answer": 32,
        "explanation": "Cats have 32 separate muscles controlling each outer ear pinna."
    },
    {
        "type": "slider",
        "question": "What is the top recorded sprinting speed of a wild cheetah in mph?",
        "category": "Wildlife Slider",
        "min": 30,
        "max": 100,
        "step": 1,
        "unit": "mph",
        "answer": 70,
        "explanation": "Cheetahs can accelerate up to 70-75 mph in short bursts."
    },
    {
        "type": "slider",
        "question": "In what year did Neil Armstrong walk on the Moon during Apollo 11?",
        "category": "Space Slider",
        "min": 1955,
        "max": 1980,
        "step": 1,
        "unit": "",
        "answer": 1969,
        "explanation": "Apollo 11 landed on the Moon on July 20, 1969."
    },
    {
        "type": "slider",
        "question": "How many yards long is an American football field including both endzones?",
        "category": "Sports Slider",
        "min": 80,
        "max": 160,
        "step": 5,
        "unit": "yards",
        "answer": 120,
        "explanation": "The field is 100 yards of playing area plus two 10-yard endzones = 120 yards."
    },
    {
        "type": "slider",
        "question": "How many seconds are in one single standard hour?",
        "category": "Math Slider",
        "min": 1000,
        "max": 6000,
        "step": 100,
        "unit": "seconds",
        "answer": 3600,
        "explanation": "60 seconds × 60 minutes = 3,600 seconds in an hour."
    },

    # =========================================================================
    # MULTI-SELECT ("Select All That Apply")
    # =========================================================================
    {
        "type": "multi_select",
        "question": "Select all mammals that lay eggs (monotremes):",
        "category": "Bizarre Biology",
        "options": ["Platypus", "Echidna", "Kangaroo", "Fruit Bat", "Koala"],
        "answer": ["Platypus", "Echidna"],
        "explanation": "Only platypuses and echidnas are living egg-laying mammals (monotremes)."
    },
    {
        "type": "multi_select",
        "question": "Select all fruits that are botanically classified as BERRIES:",
        "category": "Botanical Facts",
        "options": ["Banana", "Watermelon", "Tomato", "Strawberry", "Raspberry"],
        "answer": ["Banana", "Watermelon", "Tomato"],
        "explanation": "Botanically, bananas, watermelons, and tomatoes are berries! Strawberries and raspberries are aggregate fruits."
    },
    {
        "type": "multi_select",
        "question": "Select all original founding Avengers in the 2012 MCU film:",
        "category": "Marvel Movies",
        "options": ["Iron Man", "Thor", "Captain America", "Black Widow", "Spider-Man", "Wolverine"],
        "answer": ["Iron Man", "Thor", "Captain America", "Black Widow"],
        "explanation": "The 2012 team was Iron Man, Captain America, Thor, Hulk, Black Widow, and Hawkeye."
    },
    {
        "type": "multi_select",
        "question": "Select all countries that share an active land border with France:",
        "category": "World Geography",
        "options": ["Spain", "Germany", "Belgium", "Italy", "Portugal", "Austria"],
        "answer": ["Spain", "Germany", "Belgium", "Italy"],
        "explanation": "France borders Spain, Germany, Belgium, Italy, Switzerland, Monaco, Luxembourg, and Andorra. Not Portugal or Austria!"
    },
    {
        "type": "multi_select",
        "question": "Select all primary colors in the additive RGB light spectrum:",
        "category": "Science & Light",
        "options": ["Red", "Green", "Blue", "Yellow", "Cyan"],
        "answer": ["Red", "Green", "Blue"],
        "explanation": "RGB (Red, Green, Blue) are the primary colors of light and digital screens."
    },
    {
        "type": "multi_select",
        "question": "Select all metals that are liquid at or near room temperature (25°C to 30°C):",
        "category": "Chemistry",
        "options": ["Mercury", "Gallium", "Lead", "Titanium", "Copper"],
        "answer": ["Mercury", "Gallium"],
        "explanation": "Mercury is liquid at room temp (-38°C melting point), and Gallium melts in your hand at 29.7°C!"
    },
    {
        "type": "multi_select",
        "question": "Select all planets in our solar system that have rings:",
        "category": "Astronomy",
        "options": ["Saturn", "Jupiter", "Uranus", "Neptune", "Mars"],
        "answer": ["Saturn", "Jupiter", "Uranus", "Neptune"],
        "explanation": "All four giant gas planets (Saturn, Jupiter, Uranus, Neptune) have ring systems."
    },
    {
        "type": "multi_select",
        "question": "Select all creatures that are invertebrates (have no backbone):",
        "category": "Animal Kingdom",
        "options": ["Jellyfish", "Octopus", "Earthworm", "Snake", "Chameleon"],
        "answer": ["Jellyfish", "Octopus", "Earthworm"],
        "explanation": "Jellyfish, octopuses, and worms lack backbones. Snakes and chameleons are vertebrates."
    },

    # =========================================================================
    # TRUE OR FALSE (Fact or Fiction)
    # =========================================================================
    {
        "type": "true_false",
        "question": "Bananas share roughly 50% of their DNA with human beings.",
        "category": "Genetics: Fact or Fiction",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "True! About 50% of the genes in humans have recognizable counterparts in bananas for cellular function."
    },
    {
        "type": "true_false",
        "question": "Napoleon Bonaparte was famously short compared to average French men of his time.",
        "category": "History Myths",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "False! At 5 feet 7 inches (170 cm), Napoleon was actually slightly above average French male height."
    },
    {
        "type": "true_false",
        "question": "A flock or gathering of crows is officially referred to as a 'Murder'.",
        "category": "Nature Trivia",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "True! A group of crows is called a Murder of Crows."
    },
    {
        "type": "true_false",
        "question": "Common goldfish have a memory span of only 3 seconds.",
        "category": "Animal Myths",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "False! Scientific studies show goldfish have memory spans lasting up to 5 months."
    },
    {
        "type": "true_false",
        "question": "Lightning never strikes the exact same location on Earth twice.",
        "category": "Weather Myths",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "False! The Empire State Building is struck by lightning about 25 times every single year."
    },
    {
        "type": "true_false",
        "question": "The Eiffel Tower can grow over 15 cm (6 inches) taller during hot summer days.",
        "category": "Architecture & Physics",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "True! Thermal expansion of iron in summer heat makes the Eiffel Tower expand upward."
    },
    {
        "type": "true_false",
        "question": "Humans only use 10% of their brain capacity at any given time.",
        "category": "Brain Myths",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "False! Brain scans show virtually all parts of the brain are active throughout the day."
    },
    {
        "type": "true_false",
        "question": "Oxford University is older than the Aztec Empire.",
        "category": "Timeline Trivia",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "True! Oxford was teaching by 1096; the Aztec Empire was founded centuries later around 1428."
    }
]

def get_random_trivia_questions(count: int = 5, used_prompts=None) -> List[Dict[str, Any]]:
    """Returns a shuffled deck with a balanced mix of question types, persisting across rounds."""
    if used_prompts is None:
        used_prompts = set()
    available = [q for q in TRIVIA_QUESTIONS if q.get("question") not in used_prompts]
    if len(available) < count:
        used_prompts.clear()
        available = list(TRIVIA_QUESTIONS)
    random.shuffle(available)
    selected = available[:count]
    for q in selected:
        used_prompts.add(q.get("question", ""))
    return selected
