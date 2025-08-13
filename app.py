from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# --- Game Data (Expanded List) ---
PROMPTS = [
    {"prompt": "Donald Duck's middle name.", "answer": "Fauntleroy"},
    {"prompt": "A study published in the journal Anthrozoo reported that cows produce 5% more milk when they are given _____.", "answer": "Names"},
    {"prompt": "In 2002, Bruce Willis sent 12,000 boxes of _____ to U.S. soldiers in Afghanistan.", "answer": "Girl Scout Cookies"},
    {"prompt": "The original name for the search engine Google was _____.", "answer": "Backrub"},
    {"prompt": "In the 19th century, it was fashionable for wealthy Europeans to have _____ as pets.", "answer": "Hermits"},
    {"prompt": "In Switzerland, it is illegal to own just one _____.", "answer": "Guinea pig"},
    {"prompt": "A group of flamingos is called a _____.", "answer": "Flamboyance"},
    {"prompt": "The tiny plastic or metal tube at the end of a shoelace is called an _____.", "answer": "Aglet"},
    {"prompt": "The Roman emperor Caligula once declared war on _____.", "answer": "The sea"},
    {"prompt": "Before the 17th century, carrots were _____.", "answer": "Purple"},
    {"prompt": "The dot over the letter 'i' and 'j' is called a _____.", "answer": "Tittle"},
    {"prompt": "The _____ is the national animal of Scotland.", "answer": "Unicorn"},
    {"prompt": "On November 12, 1970, George Thornton, a highwat engineer in Oregon, had the unusual job of blowing up a _____.", "answer": "Dead Whale"},
    {"prompt": "People in Damariscotta, Maine hold an annual race where they use _____ as boats.", "answer": "Pumpkins"},
    {"prompt": "As a young student in Buenos Aires, Pope Francis worked as a _____.", "answer": "Bouncer"},
    {"prompt": "A woman in Muncie, Indiana was hospitalized after trying to remove a callus on her foot with a _____.", "answer": "Shotgun"},
    {"prompt": "Jacobite Cruises purchased unusual insurance to protect it from damage caused by _____.", "answer": "The Loch Ness Monster"},
    {"prompt": "El Colacho is a Spanish festival where people dress up like the devil and jump over _____.", "answer": "Babies"},
    {"prompt": "Cheap Chic Weddings is an annual contest in which participants make wedding dresses out of _____.", "answer": "Toilet Paper"},
    {"prompt": "Marcella Hazan is the culinary guru who pioneered the unusual technique of cooking duck with a _____.", "answer": "Hair Dryer"},
    {"prompt": "The sound of E.T. walking was made by someone squishing _____.", "answer": "Jell-O"},
    {"prompt": "The first item listed on eBay was a broken _____.", "answer": "Laser Pointer"},
    {"prompt": "Oddly enough, Albert Einstein's eyeballs can be found in a _____ in New York City.", "answer": "Safe Deposit Box"},
    {"prompt": "In 2013, a wealthy Michagan man bought the house next to his ex -wife and erected a giant bronze statue of a _____.", "answer": "Middle Finger"},
    {"prompt": "The name of the first chimp sent into space.", "answer": "Ham"},
    {"prompt": "The name for a group of porcupines", "answer": "Prickle"},
    {"prompt": "The name of the dog that won the 2012 World's Ugliest Dog Competition.", "answer": "Mugly"},
    {"prompt": "Dr. Seuss is credit with coining this common derogatory term in his 1950 book If I Ran the Zoo.", "answer": "Nerd"},
    {"prompt": "The name of the man on the Quaker Oats label.", "answer": "Larry"},
    {"prompt": "During a famous fire in 1567, a Norwegian man named Hans Steininger died after tripping over a _____.", "answer": "Beard"},
    {"prompt": "The fishing company E21 makes a very peculiar fishing rod that is composed of 70% _____.", "answer": "Carrots"},
    {"prompt": "On January 13, 2014, U.S. Secretary of State John Kerry presented to Russian Foreign Minister Sergei Lavrow the odd gift of two very large _____.", "answer": "Potatoes"},
    {"prompt": "During the mid to late-nineties, the English town of Glastonbury was on a manhunt for the old house intruder known as 'The _____.'", "answer": "Tickler"},
    {"prompt": "Suffering from an extremely rare side effect after getting hip surgery in 2010, a Dutch man has alienated his family because he cannot stop _____.", "answer": "Laughing"},
    {"prompt": "It's weird work but Jackie Samuel charges $60 an hour to _____.", "answer": "Snuggle"},
    {"prompt": "Huggies Brazil developed a phone app that tells you when a baby's diaper is wet. It's called _____.", "answer": "Tweetpee"},
    {"prompt": "Ben and Jerry only started making ice cream because it was too expensive to make _____.", "answer": "Bagels"},
    {"prompt": "Tashirojima is an island off of Japan that is complete overrun by _____.", "answer": "Cats"},
    {"prompt": "While president of the United States, John Adams had a dog named Juno and a dog named _____.", "answer": "Satan"},
    {"prompt": "In 2012, a 26-year-old man from London went on a mission to lick every _____ in the United Kingdom.", "answer": "Cathedral"},
    {"prompt": "In 2003, Morocco made the highly unusual offer to send 2,000 _____ to assist the United States' war efforts in Iraq.", "answer": "Monkeys"},
    {"prompt": "Romano Mussolini, son of the fascist dictator Benito Mussolini, did not follow in his father's footsteps. Instead, he made his living as a _____.", "answer": "Jazz Musician"},
    {"prompt": "ROAD TRIP! When in Nepal, visit the village of Parsawa and Laxmipur, where you can enjoy the slightly off-putting 10 day _____ Festival.", "answer": "Cursing"},
    {"prompt": "A group known as the 'Robin Hooders' in Keene, New Hampshire pay for other people's _____.", "answer": "Parking Meters"},
    {"prompt": "In an effort to push 'slow TV,' Norway had a 12-hour block of programming in 2013 dedicated to _____.", "answer": "Knitting"},
    {"prompt": "Belmont University in Nashville has offered a class called 'Oh, Look, a _____.'", "answer": "Chicken"},
    {"prompt": "The area in the Pacific Ocean where great white sharks congregate every spring is called the White Shark _____.", "answer": "Cafe"},
    {"prompt": "Reg Mellor is the reigning champion of a sport that just involves keeping a _____ in your pants.", "answer": "Ferret"},
    {"prompt": "Although very unconventional, farmer William von Schneidau feeds his pigs _____.", "answer": "Marijuana"},
    {"prompt": "When Paul Nelson and Andrew Hunter climbed Britain's highest mountain in 2006, they made an unusual discovery hidden behind a pile of stones. It was a _____.", "answer": "Piano"},
    {"prompt": "At 2:45 a.m. one day in June 2013, a man in Orlando, Florida was arrested for walking up to a police officer and punching his _____.", "answer": "Horse"},
    {"prompt": "A 2013 Pakistani game show caused a controversy when their grand prize was a _____.", "answer": "Baby"},
    {"prompt": "In 2013, two teens from Sequoyah High Sxhool near Atlanta, Georgia won $5,0000 scholarships for wearing _____ to prom", "answer": "Duct Tape"},
    {"prompt": "Since 2000, a couple in Queens, New York has been living rent-free in a _____ in exchange for taking care of it.", "answer": "Cemetery"},
    {"prompt": "In 2013, a 51-year-old Swedish inmate broke out of prison a day before his scheduled release so he could go see a _____.", "answer": "Dentist"},
    {"prompt": "In 2010, Customs officers on the Norway-Sweden border intercepted a truck trying to smuggle 28 tons of _____ from China.", "answer": "Garlic"},
    {"prompt": "In 2012, a teenager from Weslaco, Texas claimed the reason he stabbed his friend was because a _____ made him do it.", "answer": "Ouija Board"},
    {"prompt": "ROADTRIP! When on a spring break trip to Dongyang, China, be sure to try their eggs cooked in ______.", "answer": "Young Boy Urine"},
    {"prompt": "A man in Milford, Iowa got fired from his job after he used a ____ to dislodge his Twix bar from the office vending machine.", "answer": "Forklift"},
    {"prompt": "According to a Chinese myth, if a vampire comes across a sack of rice, he must ____", "answer": "Count Each Grain"},
    {"prompt": "When soccer player Stefan Schwarz signed with Sunderland in 1999, the team made sure that his contract specifically prohibited him from traveling to ___.", "answer": "Outer Space"},
    {"prompt": "What Dr. Edgar Parker legally changed his name to, in order to help his dental practice", "answer": "Painless"},
    {"prompt": "After an allergic reaction to steroids used to treat asthma, a 28-year old woman started growing ____ on her head instead of hair.", "answer": "Fingernails"},
    {"prompt": "PETA has asked officials in Punxsutawney Phil, the Groundhog Day groundhog, with ______.", "answer": "An Animatronic Groundhog"},
    {"prompt": "In 2004, the CEO of Blockbuster mailed Reed Hastings, the CEO of Netflix, an odd package. He sent him a ___.", "answer": "Kitchen Sink"},
    {"prompt": "According to a 2010 study, one child in the U.S. was injured every 46 minutes by a ___.", "answer": "Bounce House"},
    {"prompt": "In October of 2013, eight sixth-graders from a New York college prep school were hospitalized after someone released _____ in a classroom.", "answer": "Axe Body Spray"},
    {"prompt": "In 2013, Dell issued a recall after customers complained their laptops smelled like ____.", "answer": "Cat Urine"},
    {"prompt": "The Kila Raipur Sports Festival, held annually in Punjab, India, has many odd and dangerous events, including one where the participants lay on the ground and get _______.", "answer": "Run Over By A Tractor"},
    {"prompt": "The city of Olney, Illinois organizes an annual event in order to ______ squirrels.", "answer": "Count"},
    {"prompt": "While in Florence, New Jersey be sure to check out the auto repair shop which, according to its owner, has an operational toilet once owned by _____.", "answer": "Hitler"},
    {"prompt": "Amerigo Vespucci, the man for whom America was named, was a _____ dealer.", "answer": "Pickle"},
    {"prompt": "Walter Arnold received the world's first speeding ticket in 1896 for going _____ miles per hour.", "answer": "8"},
    {"prompt": "Edgar Valdez Villarreal, a notorious Mexican drug cartel leader, had the not-so-scary nickname \"La ______\".", "answer": "Barbie"},
    {"prompt": "Frank Hayes is the first jockey to win a race while ______.", "answer": "Dead"},
    {"prompt": "In 1967, a small town in Ecuador elected an inanimate object mayor. The elected mayor was a ______.", "answer": "Foot Powder"},
    {"prompt": "As a way to protest Belarus' police state, a Swedish group dropped hundreds of ________ from an airplane.", "answer": "Teddy Bears"},
    {"prompt": "A man in western Pennsylvania got a DUI for having an open can of beer while riding a ____.", "answer": "Lawn Mower"},
    {"prompt": "Anatidaephobia is the fear that somewhere in the world a _______ is watching you.", "answer": "Duck"},
    {"prompt": "According to a Logitech study, 49% of lost remote controls are found in the couch, while 4% are found in the ____.", "answer": "Fridge"},
    {"prompt": "The French have a pastry called \"Nun's ___\".", "answer": "Fart"},
    {"prompt": "Alexander the Great made his men ________ before a battle.", "answer": "Shave"},
    {"prompt": "Freddie Mercury backed out of a duet with Michael Jackson because Jackson brought a _____ to the recording studio", "answer": "Llama"},
    {"prompt": "An Indiana woman sued a church cemetery because they refused to install her late husband's tombstone shaped like a _____.", "answer": "Couch"},
    {"prompt": "While in Alliance, Nebraska, you can visit the Stonehenge replica made out of ____.", "answer": "Cars"},
    {"prompt": "A Florida man choked to death on cockroaches he ate while trying to win a ___.", "answer": "Python"},
    {"prompt": "For one day in 1998, Topeka, Kansas renamed itself ______.", "answer": "Topikachu"},
    {"prompt": "There was once a fourth member of Kellogg's Rice Krispies mascot gang. Originally it was Snap, Crackle, Pop and ____,", "answer": "Pow"},
    {"prompt": "In 2006, the wax museum Madame Tussaud's in New York City introduced its first wax ____.", "answer": "Baby"},
    {"prompt": "In 2007, a woman with a rare disorder that causes her to be sexually attracted to inanimate objects married ______.", "answer": "Eiffel Tower"},
    {"prompt": "On his own website, magician David Blaine once wrote, \"The most courageous act a man can do is _____.\"", "answer": "Cry"},
    {"prompt": "The University of Victoria offers a physical education class called The Science of ________.", "answer": "Batman"},
    {"prompt": "The Lehigh Valley IronPigs, a minor league baseball team, held a contest where the prize was a voucher for a ______.", "answer": "Funeral"},
    {"prompt": "Every year residents in Ivrea, Italy reenact a historical battle of their region, and instead of replica weapons, they use ____.", "answer": "Oranges"},
    {"prompt": "Nigeria's version of Cookie Monster can't stop eating _____.", "answer": "Yams"},
    {"prompt": "Advanced Comfort Technology makes waterbeds for _____.", "answer": "Cows"},
    {"prompt": "Mexico's Isla de las Munecas is an attraction known for having hundreds of ________ hanging in its trees.", "answer": "Dolls"},
    {"prompt": "In 2013, a U.S. Customs and Border Protection Officer was found guilty of granting citizenship in exchange for 200 ____.", "answer": "Egg Rolls"},
    {"prompt": "A British woman was arrested for hijacking a British ferry and yelling, \"________!\"", "answer": "I'm Jack Sparrow"},
    {"prompt": "In 2013, the Rethink ad agency placed red beer fridges throughout Europe that could only be opened by _______.", "answer": "Canadians"},
    {"prompt": "According to Forbes, the average income for an \"ice cream taster\" is $______ a year.", "answer": "56000"},
    {"prompt": "Located near the town of Stanley, there's a small village in England called No _____.", "answer": "Place"},
    {"prompt": "Edwin E. Holmes, a man with very specific interests, wrote the 254-page book \"A History of _______\".", "answer": "Thimbles"},
    {"prompt": "Haribo sells a gummi in Germany that depicts a human butt with _______ growing out of it.", "answer": "Ears"},
    {"prompt": "@blakeshelton, the country singer and judge on The Voice, tweeted, \"Just fell down and gashed my hand open while running from ______... Don't ask.\"", "answer": "An Ostrich"},
    {"prompt": "Over the course of 35 years, artist Scott Weaver has built a replica of the city of San Francisco using over 100,000 ______.", "answer": "Toothpicks"},
    {"prompt": "On October 24th, 2013 a man in Columbus, Georgia ran into his burning home in order to save his ____.", "answer": "Beer"},
    {"prompt": "Unagi Travel is an unusual Japanese travel agency that sends your ______ on vacations.", "answer": "Stuffed Animals"},
    {"prompt": "Scottsdale Community College's sports teams are oddly named the Fighting _____.", "answer": "Artichokes"},
    {"prompt": "Because he found Chinese food to be odd, during the 2008 Beijing Olympics, sprinter Usain Bolt said that he ended up eating 1,000 _______.", "answer": "McNuggets"},
    {"prompt": "With 88 catches, Canadian Aaron Gregg holds the Guinness World Record for _______ juggling.", "answer": "Chainsaw"},
    {"prompt": "In 1977, Simulations Publications, Inc. published a strangely named board game called After The ______.", "answer": "Holocaust"},
    {"prompt": "Actual warning on Vidal Sassoon hair dryer: \"Do not use while ______.\"", "answer": "Sleeping"},
    {"prompt": "Phil Shaw is the founder of the bizarre sport called Extreme _________.", "answer": "Ironing"},
    {"prompt": "On November 25, 2013, a 16-month-old Chinese girl underwent surgery to remove the unusual growth of a _____ in her ear canal.", "answer": "Dandelion"},
    {"prompt": "According to the nonfiction book The Man-Eating Tigers of Sundarbans, tiger urine \"smells sort of like _____.\"", "answer": "Buttered Popcorn"},
    {"prompt": "@taylorswift13 Tweeted \"Thank you for tonight, Des Moines. I found endless amounts of _____ on my arms from hugging lots of you tonight.\"", "answer": "Glitter"},
    {"prompt": "In 2000, Australia had its largest ever online petition, which called for an end to rising _____ prices.", "answer": "Beer"},
    {"prompt": "The App of Icelanders is a phone app that warns you if the person you're romantically interested in is a ____.", "answer": "Relative"},
    {"prompt": "In school, Sylvester Stallone was voted by his teachers as Most Likely to Go To _____.", "answer": "The Electric Chair"},
    {"prompt": "Although gross, chemist Sir Robert Cheseborough claimed he ate a spoonful of his invention, ______, every day", "answer": "Vaseline"},
    {"prompt": "The first thing eaten in outer space was ____", "answer": "Applesauce"},
    {"prompt": "According to the International Code of Disease, the code Y92250 is the code for \"when a patient is injured in an ____.\"", "answer": "Art Gallery"},
    {"prompt": "The rare condition known as \"argyria\" causes people's skin to _____.", "answer": "Turn Blue"},
    {"prompt": "In India you can buy a cola named Gau Jal that includes the bizarre ingredient _______.", "answer": "Cow Urine"},
    {"prompt": "In a study done by author Stefan Gates, 44% of adults admitted to eating _____.", "answer": "Boogers"},
    {"prompt": "In 2000, a mafia boss in an Italian prison escaped his cell using only _____.", "answer": "Dental Floss"},
    {"prompt": "Located within the municipal boundaries of Kirkland Lake, Ontario, there lies the controversially named village of ____.", "answer": "Swastika"},
    {"prompt": "In the late 17th century, London was victimized by a man named Whipping Tom, who would randomly spank people and scream \"______!\"", "answer": "Spanko"},
    {"prompt": "Famed film director Alfred Hitchcock - the \"Master of Suspense\" - claimed, \"I'm frightened of ______, worse than frightened, they revolt me.\"", "answer": "Eggs"},
    {"prompt": "Ruppy the beagle is a very unusual dog because he can ____.", "answer": "Glow In The Dark"},
    {"prompt": "The Snickers candy bar was named after its creator's _____.", "answer": "Horse"},
    {"prompt": "After consuming antifreeze, a Maltese terrier in Australia had his life saved when vets then gave him ____ to drink.", "answer": "Vodka"},
    {"prompt": "A Brazillian environmental group launched a campaign in 2009 to save the rainforest by urging people to pee in ____.", "answer": "The Shower"},
    {"prompt": "In 2009, a Russian man shocked the medical world when it was discovered he had a 5 centimeter long _____ growing in his lung.", "answer": "Tree Branch"},
    {"prompt": "The Backyard Brains company sells a device that lets you control _____ with your mobile phone.", "answer": "Cockroaches"},
    {"prompt": "On the northwest tower of the Washington National Cathedral, there hangs a gargoyle made to resemble _____.", "answer": "Darth Vader"},
    {"prompt": "Lake Superior State University offers a bizarre license. The license entitles you to hunt ____.", "answer": "Unicorns"},
    {"prompt": "A man from Enniskillen, Northern Ireland was sentenced to three months in prison for a fire he started while trying to turn _____ into gold.", "answer": "His Poop"},
    {"prompt": "A study conducted at Tufts University by psychology grad student Nicholas Rule found that people have the ability to point out _____ in a crowd.", "answer": "Mormons"},
    {"prompt": "Cambridge University economist Ha-Joon Chang holds an unpopular opinion. He insists that the _____ changed the world more than the Internet.", "answer": "Washing Machine"},
    {"prompt": "A man in Watertown, New York, claims to have been happily married for over 25 years to his wife Teagan, who strangely is a ____.", "answer": "Mannequin In A Wheelchair"},
    {"prompt": "New Mexico state senator Duncan Scott successfully got a bill passed in the New Mexico senate requiring psychiatrists testifying in court to wear a ____.", "answer": "Wizard's Hat"},
    {"prompt": "UC Irvine brought 6,084 students together in 2012 to break the world record for largest _____ ever.", "answer": "Dodgeball Game"},
    {"prompt": "Highway construction in Iceland was delayed in 2013 after advocates claimed the project would destroy the natural land where _____ live and thrive.", "answer": "Elves"},
    {"prompt": "When in the North Shore Mountains near Vancouver, British Columbia, be sure to climb the unusually named peak called _______ Mountain.", "answer": "Unnecessary"},
    {"prompt": "According to a University of Barcelona study, surprisingly, 5% of people have absolutely no emotional response when they ______.", "answer": "Listen To Music"},
    {"prompt": "In 1726, a British woman named Mary Toft convinced doctors that she had given birth to _____.", "answer": "Rabbits"},
    {"prompt": "Mohammed Khurshid Hussain is in the Guinness Book of World Records because he is able to ______ very quickly with his nose.", "answer": "Type"},
    {"prompt": "Ward Shelley and Alex Schweder's art piece \"In Orbit,\" which was on display at a gallery in New York, featured two men living in a giant _____ for 10 days.", "answer": "Hamster Wheel"},
    {"prompt": "@SimonCowell Tweeted: \"Still not sure what a ____ is.\"", "answer": "Baby Shower"},
    {"prompt": "In 1518, hundreds of people in Strasbourg became afflicted with a bizarre condition that rendered them unable to stop _____.", "answer": "Dancing"},
    {"prompt": "In 2013 a zoo in China attempted to pass off a _____ as an African lion.", "answer": "Large Dog"},
    {"prompt": "A Swedish man who works as a dishwasher receives disability benefits due to his unusual addiction to _____.", "answer": "Heavy Metal Music"},
    {"prompt": "Bill Bennett made news in 2004 when he was able to sell just a single, ordinary ______ on eBay", "answer": "Corn Flake"},
    {"prompt": "During the 1990s, teachers in North Korea were, oddly enough, required to know how to ____.", "answer": "Play The Accordion"},
    {"prompt": "Instead of having guard dogs, police in rural parts of China's Xinjiang Province use ___.", "answer": "Geese"},
    {"prompt": "In 2013, the Romanian government, facing financial hardships, started taxing a group of people they had never taxed before. They started taxing ____.", "answer": "Witches"},
    {"prompt": "In 2013, researchers at the University of Tokyo developed the incendiary reflection, a mirror that makes it look like you're _____.", "answer": "Smiling"},
    {"prompt": "Pam Anderson wrote a book of recipes with the title How to Cook Without a ____.", "answer": "Book"},
    {"prompt": "In 2004, the Trane Corporation sold pillows in Japan that were designed to combat loneliness. They were shaped like a _____.", "answer": "Woman's Lap"},
    {"prompt": "Actor Eddie Murphy released a dance song in 1982 titled \"Boogie in _____.\"", "answer": "Your Butt"},
    {"prompt": "When in Laza, Spain, be sure to check out the annual festival where participants pelt each other with muddy rags full of _____.", "answer": "Fire Ants"},
    {"prompt": "When visiting Christchurch, New Zealand, check out the $6 million cathedral made out of ____.", "answer": "Cardboard"},
    {"prompt": "The mountain logo on a package of Toblerone chocolate contains a hidden image of a _____.", "answer": "Bear"},
    {"prompt": "Ahlgrim Acres is a nine hole miniature golf course oddly located in an Illinois _____.", "answer": "Funeral Home"},
    {"prompt": "Psycho was the first American movie to show a ____.", "answer": "Toilet Flushing"},
    {"prompt": "One of Kim Jong Il's many titles was \"Invicible and Ever-Triumphant General and Highest Incarnation of the Revolutionary Comradely ____.\"", "answer": "Love"},
    {"prompt": "Pentheraphobia is the constant fear of your ______.", "answer": "Mother-In-Law"},
    {"prompt": "The real name of the Internet's famous Grumpy Cat is ___.", "answer": "Tardar Sauce"},
    {"prompt": "In autumn 2013, a company that owns parking lots in England temporarily allowed drivers to pay for parking not with money, but with _____.", "answer": "Chestnuts"},
    {"prompt": "Gloucestershire, England is home to the Cotswold Olimpicks, the highlight of which is the traditional _____-kicking competition.", "answer": "Shin"},
    {"prompt": "Moviegoers who use their cell phones at the Prince Charles Cinema in London are escorted out by people dressed as ____.", "answer": "Ninjas"},
    {"prompt": "Used in medical studies, a robot at the UK's Health and Safety Laboratory goes by the name _____ Larry.", "answer": "Vomiting"},
    {"prompt": "In 1988, George H. W. Bush celebrated Halloween by dressing up as _____.", "answer": "Himself"},
    {"prompt": "The unusual Chick and Sophie Major memorial scholarships are awarded to high school students who are good at _____.", "answer": "Duck Calls"},
    {"prompt": "Chad Orzel wrote the book How to Teach _____ to Your Dog.", "answer": "Physics"},
    {"prompt": "A Florida woman returned home one day in 2012 to discover that, strangely, her ______ had been stolen while neighbors just watched it happen.", "answer": "Driveway"},
    {"prompt": "On December 3, 2009, and March 30, 2010, rapper Eminem Tweeted a photo proving he was surprisingly really good at ____.", "answer": "Donkey Kong"},
    {"prompt": "The first and only dog to be given rank in the United States Armed Forces was named Sergeant _____.", "answer": "Stubby"},
    {"prompt": "The lead singer of the heavy metal band Hatebeak is ____.", "answer": "A Parrot"},
    {"prompt": "You are experiencing the Mariko Aoki phenomenon when you have the urge to poop while _____.", "answer": "In A Bookstore"},
    {"prompt": "Metrophilia is sexual arousal caused by ___", "answer": "Poetry"},
    {"prompt": "The secret code name for the project to invent the first microwave oven in the 1940s.", "answer": "Speedy Weenie"},
    {"prompt": "The original name for Pepsi.", "answer": "Brad's Drink"},
    {"prompt": "About 180 miles south of New Zealand, at the coordinates 50'36.25'S 165'58.38'E, lies this oddly named island.", "answer": "Disappointment Island"},
    {"prompt": "In the U.S., the original name of the game bingo.", "answer": "Beano"},
    {"prompt": "Strange brand name for the cigarettes sold by The Enlightened Tobacco Company in the 1990s.", "answer": "Death"},
    {"prompt": "The name for the random symbols used to indicate swearing in comic strips.", "answer": "Grawlix"},
    {"prompt": "Item that teachers at Mounts Bay Academy in England were banned from using in 2014.", "answer": "Red Pens"},
    {"prompt": "The Michelin Man's strange, official name.", "answer": "Bibendum"},
    {"prompt": "Former first lady Barbara Bush wrote an official apology letter to this fictional character in 1990.", "answer": "Marge Simpson"},
    {"prompt": "What South Africans call traffic lights.", "answer": "Robots"},
    {"prompt": "Samsung started out as a company that made this completely low-tech product.", "answer": "Noodles"},
    {"prompt": "The U.S. occupation with the highest percentage of white people.", "answer": "Veterinarian"},
    {"prompt": "The fastest-growing baby name for girls in 2012.", "answer": "Arya"},
    {"prompt": "Cap'n Crunch's first name.", "answer": "Horatio"},
    {"prompt": "Occupation with the highest divorce rate, according to the 2000 U.S. Census.", "answer": "Dancer"},
    {"prompt": "The original brand name for Kool-Aid.", "answer": "Fruit Smack"},
    {"prompt": "The Oxford Dictionaries' \"word of the year\" for 2013.", "answer": "Selfie"},
    {"prompt": "When Milton Bradley first acquired the rights to it, the game Twister was called this.", "answer": "Pretzel"},
    {"prompt": "Because of his ability to stay on-air for hours, NBC newsman Lester Holt has earned the nickname ____ from his colleagues.", "answer": "Iron Pants"},
    {"prompt": "Strangely, a 2015 study conducted by professors in Finland and California came to the conclusion that there are too many ____.", "answer": "Studies"},
    {"prompt": "The patent shown here is for Paul R. Harriss's invention, the ____. It features a belt around a father with two straps for a child's feet.", "answer": "Dad Saddle"},
    {"prompt": "According to Civil War historian Alfred Jay Bollet, there was an unwritten code among soldiers that they would not shoot each other while _____.", "answer": "Pooping"},
    {"prompt": "Princess Olga of 10th Century Russia had a nasty reputation for killing anyone who suggested she ____.", "answer": "Get Married"},
    {"prompt": "As France has begun growing more corn, they've noticed a shocking side effect: Their cornfields are full of _____.", "answer": "Cannibal Hamsters"},
    {"prompt": "Despite it being a crime for the last 38 years, in 2014 Grand Rapids officially made it legal to _____ another's person.", "answer": "Annoy"},
    {"prompt": "Donald Rogers wrote a book in the '50s called Teach Your Wife To Be a ____.", "answer": "Widow"},
    {"prompt": "There's a Russian saying about needing to finish what you start. It translates to \"If you called yourself a ____, get into the basket!\"", "answer": "Mushroom"},
    {"prompt": "Dr. Elena Bodnar invented a bra that can also be used as a ____.", "answer": "Gas Mask"},
    {"prompt": "DSM, a company from the Netherlands, invented a new product that could help save the environment by stopping ____.", "answer": "Cow Burps"},
    {"prompt": "The police department of the Canadian town of Kensington publicly apologized for their 2016 announcement that the new punishment for driving drunk would be _____.", "answer": "Listening To Nickelback"},
    {"prompt": "Entrepreneur Leo De Watts has made a hefty sum selling $115 bottles of ____ to China.", "answer": "British Air"},
    {"prompt": "In 2013, police in the Maldives detained a suspect for loitering near an election polling place on suspicion of black magic. the suspect in question was ____.", "answer": "A Coconut"},
    {"prompt": "\"Sphenopalatine ganglioneuralgia\" may sound like a life-threatening affliction, but you've probably already had it if you've ever ____.", "answer": "Eaten Ice Cream"},

]

# --- Game State ---
game_state = {
    "prompt": "",
    "answer": "",
    "answers": [],
    "stage": "waiting"  # waiting -> answering -> voting
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@socketio.on('connect')
def handle_connect():
    # Send the current game state to a newly connected client
    emit('game_update', game_state)

@socketio.on('get_random_prompt')
def handle_get_random_prompt():
    selected = random.choice(PROMPTS)
    # Emit only to the admin who requested it
    emit('random_prompt_data', selected, room=request.sid)

@socketio.on('start_game')
def handle_start_game(data):
    game_state['prompt'] = data.get('prompt')
    game_state['answer'] = data.get('answer')
    game_state['stage'] = 'answering'
    game_state['answers'] = []
    socketio.emit('game_update', game_state)

@socketio.on('submit_answers')
def handle_submit_answers(data):
    player_answers = data.get('player_answers', [])
    
    # Add the real answer to the list of player answers
    all_answers = player_answers + [game_state['answer']]
    random.shuffle(all_answers)
    
    game_state['answers'] = all_answers
    game_state['stage'] = 'voting'
    socketio.emit('game_update', game_state)

@socketio.on('new_round')
def handle_new_round():
    game_state['stage'] = 'waiting'
    game_state['prompt'] = ''
    game_state['answer'] = ''
    game_state['answers'] = []
    socketio.emit('game_update', game_state)

if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible on your local network
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)