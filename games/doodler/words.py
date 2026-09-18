import random
from typing import List, Optional, Set

DOODLE_PROMPTS = [
    "Alien eating a taco",
    "Flamingo on a skateboard",
    "Haunted toaster",
    "Cat driving a racecar",
    "Dinosaur at a birthday party",
    "Penguin DJ at a nightclub",
    "Shark wearing sunglasses",
    "Wizard doing laundry",
    "Octopus playing the drums",
    "Sneezing dragon",
    "Gorilla drinking boba tea",
    "Astronaut walking a dog",
    "Robot weeping over spilled milk",
    "Cow jumping over the moon",
    "Ninja baking a cake",
    "Pirate parrot captain",
    "Teddy bear in an epic sword fight",
    "Superhero squirrel saving an acorn",
    "Hamster trapped in a bubble",
    "Angry cactus giving hugs",
    "Sloth running a marathon",
    "Giraffe trying to hide behind a pole",
    "Cheeseburger wearing a crown",
    "Dancing mushroom with maracas",
    "Bear riding a unicycle",
    "Chameleon failing to blend in",
    "T-Rex trying to make a bed",
    "Duck wearing roller skates",
    "Llama wearing a winter scarf",
    "Pug lifting heavy dumbbells",
    "Kangaroo boxing a punching bag",
    "Vampire brushing his fangs",
    "Zombie eating an ice cream cone",
    "Yeti sunbathing on a tropical beach",
    "Snail breaking the sound barrier",
    "Walrus balancing a ball on its nose",
    "Koala playing an electric guitar",
    "Mermaid ordering coffee",
    "Chicken piloting an airplane",
    "Owl wearing glasses reading a book",
    "Fox playing chess",
    "Frog meditating on a lily pad",
    "Hippo in a ballet tutu",
    "Raccoon rummaging through outer space",
    "Banana slipping on a human",
    "Pizza slice surfing a tidal wave",
    "Cupcake lifting weights",
    "Mouse wearing a suit of armor",
    "Lion getting a haircut",
    "Elephant painting a self portrait"
]

def get_random_doodle_prompts(count: int = 5, used_prompts: Optional[Set[str]] = None) -> List[str]:
    """Returns unique doodle prompts, persisting across rounds until the library is exhausted."""
    if used_prompts is None:
        used_prompts = set()
    available = [p for p in DOODLE_PROMPTS if p not in used_prompts]
    if len(available) < count:
        used_prompts.clear()
        available = list(DOODLE_PROMPTS)
    random.shuffle(available)
    selected = available[:count]
    for p in selected:
        used_prompts.add(p)
    return selected
