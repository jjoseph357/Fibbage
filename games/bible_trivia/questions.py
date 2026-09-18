import random
from typing import List, Dict, Any

BIBLE_TRIVIA_QUESTIONS: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. SLIDER QUESTIONS (Old & New Testament Numerical & Chronological Estimations)
    # =========================================================================
    # --- Old Testament Sliders ---
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Wisdom & Psalms",
        "question": "How many total chapters / psalms are in the Book of Psalms?",
        "min": 50,
        "max": 200,
        "step": 5,
        "unit": "psalms",
        "answer": 150,
        "verse_ref": "Psa. 150:1-6",
        "explanation": "The Book of Psalms contains exactly 150 psalms divided into five distinct books."
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Pentateuch & Wilderness",
        "question": "How many years did the children of Israel wander in the wilderness before crossing into Canaan?",
        "min": 10,
        "max": 80,
        "step": 1,
        "unit": "years",
        "answer": 40,
        "verse_ref": "Num. 14:34",
        "explanation": "According to Numbers 14:34, Israel wandered 40 years, one year for each of the 40 days the spies searched Canaan."
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Patriarchs",
        "question": "How old was Methuselah when he died, making him the longest-lived man in Scripture?",
        "min": 750,
        "max": 1050,
        "step": 1,
        "unit": "years old",
        "answer": 969,
        "verse_ref": "Gen. 5:27",
        "explanation": "Genesis 5:27 records: 'And all the days of Methuselah were nine hundred sixty-nine years, and he died.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Early Earth",
        "question": "How many total people were saved aboard Noah's ark during the Great Flood?",
        "min": 2,
        "max": 30,
        "step": 1,
        "unit": "souls",
        "answer": 8,
        "verse_ref": "1 Pet. 3:20; Gen. 7:13",
        "explanation": "Eight souls were saved: Noah, his wife, his three sons (Shem, Ham, Japheth), and their three wives."
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Flood",
        "question": "How many days did the waters prevail upon the earth during Noah's Flood before abating (Genesis 7:24)?",
        "min": 50,
        "max": 250,
        "step": 25,
        "unit": "days",
        "answer": 150,
        "verse_ref": "Gen. 7:24; 8:3",
        "explanation": "Genesis 7:24: 'And the waters prevailed upon the earth a hundred and fifty days.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Major Prophets & Exile",
        "question": "According to Jeremiah 29:10, how many years was the Babylonian captivity prophesied to last?",
        "min": 20,
        "max": 120,
        "step": 5,
        "unit": "years",
        "answer": 70,
        "verse_ref": "Jer. 29:10; Dan. 9:2",
        "explanation": "Jeremiah 29:10 declares: 'When seventy years are completed for Babylon, I will visit you and perform My good word toward you.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Pentateuch & Moses",
        "question": "How old was Moses when he died on Mount Nebo with his eyesight undimmed?",
        "min": 70,
        "max": 150,
        "step": 5,
        "unit": "years old",
        "answer": 120,
        "verse_ref": "Deut. 34:7",
        "explanation": "Deuteronomy 34:7: 'Moses was a hundred and twenty years old when he died; his eye was not dim, nor his natural force abated.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Major Prophets",
        "question": "How many chapters are in the Book of Isaiah, matching the total number of books in the Bible?",
        "min": 30,
        "max": 90,
        "step": 1,
        "unit": "chapters",
        "answer": 66,
        "verse_ref": "Isa. 66:1-24",
        "explanation": "Isaiah has 66 chapters (often called a 'miniature Bible', with 39 chapters on judgment and 27 on comfort and grace)."
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Noah",
        "question": "According to Genesis 6:15, what was the length of Noah's ark in ancient cubits?",
        "min": 100,
        "max": 600,
        "step": 25,
        "unit": "cubits",
        "answer": 300,
        "verse_ref": "Gen. 6:15",
        "explanation": "Genesis 6:15 specifies: 'The length of the ark shall be three hundred cubits, its breadth fifty cubits, and its height thirty cubits.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Kings of Israel",
        "question": "How many total years did King David reign over Israel (7 years in Hebron and 33 in Jerusalem)?",
        "min": 15,
        "max": 70,
        "step": 1,
        "unit": "years",
        "answer": 40,
        "verse_ref": "2 Sam. 5:4-5",
        "explanation": "2 Samuel 5:4: 'David was thirty years old when he became king, and he reigned forty years.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Joshua & Land Division",
        "question": "How many designated Cities of Refuge were established in Israel for unintentional manslaughter?",
        "min": 2,
        "max": 20,
        "step": 1,
        "unit": "cities",
        "answer": 6,
        "verse_ref": "Josh. 20:7-8; Num. 35:13",
        "explanation": "Six cities of refuge were appointed: three on the west side of the Jordan and three on the east side."
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Abraham",
        "question": "How old was Abraham when his miracle son Isaac was born to ninety-year-old Sarah?",
        "min": 60,
        "max": 140,
        "step": 5,
        "unit": "years old",
        "answer": 100,
        "verse_ref": "Gen. 21:5",
        "explanation": "Genesis 21:5: 'And Abraham was a hundred years old when Isaac his son was born to him.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Sodom",
        "question": "In Genesis 18, what was the lowest number of righteous people for which God agreed to spare Sodom?",
        "min": 5,
        "max": 50,
        "step": 5,
        "unit": "people",
        "answer": 10,
        "verse_ref": "Gen. 18:32",
        "explanation": "Genesis 18:32: 'And He said, I will not destroy it for the sake of the ten.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Jacob",
        "question": "How many total years did Jacob serve Laban in Haran for his wives and his flocks?",
        "min": 7,
        "max": 40,
        "step": 1,
        "unit": "years",
        "answer": 20,
        "verse_ref": "Gen. 31:38-41",
        "explanation": "Jacob served Laban 14 years for his two daughters (Leah and Rachel) and 6 years for his flock, totaling 20 years."
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Numbers & Spies",
        "question": "How many days did the twelve tribal leaders explore the Promised Land of Canaan in Numbers 13?",
        "min": 10,
        "max": 80,
        "step": 5,
        "unit": "days",
        "answer": 40,
        "verse_ref": "Num. 13:25",
        "explanation": "Numbers 13:25: 'And they returned from spying out the land at the end of forty days.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "1 Samuel & David",
        "question": "How many smooth stones did young David choose from the brook before running to face Goliath?",
        "min": 1,
        "max": 12,
        "step": 1,
        "unit": "stones",
        "answer": 5,
        "verse_ref": "1 Sam. 17:40",
        "explanation": "1 Samuel 17:40: 'And he took his staff in his hand and chose for himself five smooth stones from the brook.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Genesis & Joseph",
        "question": "How many pieces of silver did the brothers of Joseph sell him for to the Midianite/Ishmaelite traders?",
        "min": 10,
        "max": 50,
        "step": 5,
        "unit": "pieces of silver",
        "answer": 20,
        "verse_ref": "Gen. 37:28",
        "explanation": "Genesis 37:28: 'And they sold Joseph to the Ishmaelites for twenty pieces of silver.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Kings of Judah",
        "question": "How many years did the faithful young King Josiah reign in Jerusalem before his death (2 Kings 22:1)?",
        "min": 10,
        "max": 50,
        "step": 1,
        "unit": "years",
        "answer": 31,
        "verse_ref": "2 Kings 22:1",
        "explanation": "2 Kings 22:1: 'Josiah was eight years old when he began to reign, and he reigned thirty-one years in Jerusalem.'"
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Historical Books & Esther",
        "question": "In Esther 4:16, how many days and nights did Esther and the Jews in Susa fast before she went into the inner court?",
        "min": 1,
        "max": 10,
        "step": 1,
        "unit": "days",
        "answer": 3,
        "verse_ref": "Esth. 4:16",
        "explanation": "Esther 4:16: 'Hold a fast on my behalf, and neither eat nor drink for three days, night or day.'"
    },

    # --- New Testament Sliders ---
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Canon of Scripture",
        "question": "How many total inspired books make up the New Testament canon (from Matthew to Revelation)?",
        "min": 15,
        "max": 45,
        "step": 1,
        "unit": "books",
        "answer": 27,
        "verse_ref": "2 Tim. 3:16; 2 Pet. 3:16",
        "explanation": "The New Testament contains exactly 27 books: 4 Gospels, 1 historical book (Acts), 21 epistles, and 1 book of prophecy (Revelation)."
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Ministry",
        "question": "How many days and nights did Jesus fast in the wilderness before being tempted by Satan?",
        "min": 7,
        "max": 70,
        "step": 1,
        "unit": "days",
        "answer": 40,
        "verse_ref": "Matt. 4:2",
        "explanation": "Matthew 4:2 records that Jesus fasted forty days and forty nights in the Judean wilderness."
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Passion of Christ",
        "question": "How many pieces of silver was Judas Iscariot paid by the chief priests to betray Jesus?",
        "min": 10,
        "max": 100,
        "step": 5,
        "unit": "pieces",
        "answer": 30,
        "verse_ref": "Matt. 26:15; Zech. 11:12",
        "explanation": "Judas was paid thirty pieces of silver, fulfilling the prophetic price of a slave in Zechariah 11:12."
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Miracles",
        "question": "In Luke 17, how many lepers called out to Jesus and were cleansed as they went to show themselves to the priests?",
        "min": 2,
        "max": 25,
        "step": 1,
        "unit": "lepers",
        "answer": 10,
        "verse_ref": "Luke 17:12-14",
        "explanation": "Luke 17:12-14: 'Ten leprous men met Him... and as they went, they were cleansed.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Parables",
        "question": "In Matthew 25, how many total virgins took their lamps to go forth and meet the bridegroom?",
        "min": 4,
        "max": 24,
        "step": 2,
        "unit": "virgins",
        "answer": 10,
        "verse_ref": "Matt. 25:1-2",
        "explanation": "Matthew 25:1-2 describes ten virgins: five prudent virgins who took oil in their vessels, and five foolish virgins."
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Forgiveness",
        "question": "In Matthew 18:22, how many times did Jesus tell Peter to forgive a sinning brother ('seventy times seven')?",
        "min": 7,
        "max": 700,
        "step": 7,
        "unit": "times",
        "answer": 490,
        "verse_ref": "Matt. 18:21-22",
        "explanation": "Matthew 18:22: 'Jesus said to him, I do not say to you, Up to seven times, but, Up to seventy times seven' (490 times, symbolizing limitless grace)."
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Resurrection",
        "question": "How many days was Jesus seen alive by His disciples after His resurrection before ascending to heaven (Acts 1:3)?",
        "min": 10,
        "max": 80,
        "step": 5,
        "unit": "days",
        "answer": 40,
        "verse_ref": "Acts 1:3",
        "explanation": "Acts 1:3: 'To whom He also presented Himself alive after His suffering by many irrefutable proofs, appearing to them through forty days.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Acts & Paul's Trials",
        "question": "In 2 Corinthians 11:25, how many times did the Apostle Paul state he suffered shipwreck in his travels?",
        "min": 1,
        "max": 10,
        "step": 1,
        "unit": "times",
        "answer": 3,
        "verse_ref": "2 Cor. 11:25",
        "explanation": "2 Corinthians 11:25: 'Three times I was shipwrecked; a night and a day I have spent in the deep.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Acts & Saul's Conversion",
        "question": "How many days did Saul of Tarsus remain blind and fast without food or water in Damascus before Ananias arrived?",
        "min": 1,
        "max": 14,
        "step": 1,
        "unit": "days",
        "answer": 3,
        "verse_ref": "Acts 9:9",
        "explanation": "Acts 9:9: 'And he was three days without seeing, and neither ate nor drank.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Miracles",
        "question": "How many days had Lazarus already been in the tomb when Jesus arrived at Bethany to raise him?",
        "min": 1,
        "max": 10,
        "step": 1,
        "unit": "days",
        "answer": 4,
        "verse_ref": "John 11:17",
        "explanation": "John 11:17 notes that Lazarus had already been in the tomb four days, demonstrating divine resurrection power."
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Miracles",
        "question": "How many baskets full of broken leftover pieces did the disciples gather after Jesus fed the 5,000?",
        "min": 3,
        "max": 24,
        "step": 1,
        "unit": "baskets",
        "answer": 12,
        "verse_ref": "Matt. 14:20",
        "explanation": "Matthew 14:20 records: 'And they took up what was left over of the broken pieces, twelve handbaskets full.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Gospels & Resurrection",
        "question": "In John 21, how many large fish were counted in the disciples' unbroken net on the Sea of Tiberias?",
        "min": 50,
        "max": 250,
        "step": 1,
        "unit": "large fish",
        "answer": 153,
        "verse_ref": "John 21:11",
        "explanation": "John 21:11: 'Simon Peter went up and drew the net to the land, full of great fishes, a hundred and fifty-three.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Acts & Early Church",
        "question": "How many souls were baptized and added to the church on the day of Pentecost in Acts 2?",
        "min": 500,
        "max": 6000,
        "step": 500,
        "unit": "souls",
        "answer": 3000,
        "verse_ref": "Acts 2:41",
        "explanation": "Acts 2:41: 'Those therefore who received his word were baptized; and there were added in that day about three thousand souls.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Revelation & Throne Room",
        "question": "In Revelation 4:4, how many crowned elders were seated upon thrones surrounding the throne of God?",
        "min": 6,
        "max": 48,
        "step": 2,
        "unit": "elders",
        "answer": 24,
        "verse_ref": "Rev. 4:4",
        "explanation": "Revelation 4:4: 'And around the throne were twenty-four thrones, and upon the thrones twenty-four elders sitting, clothed in white garments.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Revelation & New Jerusalem",
        "question": "In Revelation 21, how many giant gates made of a single pearl each enter into the New Jerusalem?",
        "min": 4,
        "max": 24,
        "step": 1,
        "unit": "pearl gates",
        "answer": 12,
        "verse_ref": "Rev. 21:12, 21",
        "explanation": "Revelation 21:21: 'And the twelve gates were twelve pearls; each one of the gates respectively was of one pearl.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Revelation & Prophecy",
        "question": "In Revelation 5:1, how many seals sealed the sacred scroll in the right hand of Him who sat on the throne?",
        "min": 3,
        "max": 14,
        "step": 1,
        "unit": "seals",
        "answer": 7,
        "verse_ref": "Rev. 5:1",
        "explanation": "Revelation 5:1: 'And I saw in the right hand of Him who sat upon the throne a scroll written within and on the back, sealed with seven seals.'"
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Revelation & Millennium",
        "question": "In Revelation 20:4, how many years is the reign of Christ with His saints upon the earth during the Millennium?",
        "min": 100,
        "max": 5000,
        "step": 100,
        "unit": "years",
        "answer": 1000,
        "verse_ref": "Rev. 20:4",
        "explanation": "Revelation 20:4 states that the saints lived and reigned with Christ for a thousand years."
    },
    {
        "type": "slider",
        "testament": "Both Testaments",
        "category": "Canon of Scripture",
        "question": "How many total inspired books make up the standard Protestant / Christian Bible canon?",
        "min": 40,
        "max": 90,
        "step": 1,
        "unit": "books",
        "answer": 66,
        "verse_ref": "2 Tim. 3:16",
        "explanation": "The Bible contains 66 books: 39 books in the Old Testament and 27 books in the New Testament."
    },

    # =========================================================================
    # 2. MULTI-SELECT QUESTIONS (Select All That Apply)
    # =========================================================================
    # --- Old Testament Multi-Select ---
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Genesis & Tribes",
        "question": "Select all sons of Jacob who were born to his beloved wife RACHEL:",
        "options": ["Joseph", "Benjamin", "Judah", "Reuben", "Dan", "Levi"],
        "answer": ["Joseph", "Benjamin"],
        "verse_ref": "Gen. 35:24",
        "explanation": "Rachel gave birth to only two sons: Joseph and Benjamin (at whose birth she passed away near Bethlehem)."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Tabernacle & Priesthood",
        "question": "Select all three items preserved INSIDE the Ark of the Covenant (Hebrews 9:4):",
        "options": [
            "Golden pot holding the manna",
            "Aaron's rod that budded",
            "Tablets of the covenant (Ten Commandments)",
            "Bronze serpent of Moses",
            "Urim and Thummim",
            "Gideon's golden ephod"
        ],
        "answer": [
            "Golden pot holding the manna",
            "Aaron's rod that budded",
            "Tablets of the covenant (Ten Commandments)"
        ],
        "verse_ref": "Heb. 9:4; Exo. 16:33; Num. 17:10",
        "explanation": "Hebrews 9:4 specifies the Ark contained the golden pot of manna, Aaron's budded rod, and the stone tablets."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Genesis & Early Earth",
        "question": "Select all three sons of Noah who boarded the ark and repopulated the earth:",
        "options": ["Shem", "Ham", "Japheth", "Canaan", "Nimrod", "Methuselah"],
        "answer": ["Shem", "Ham", "Japheth"],
        "verse_ref": "Gen. 9:18-19",
        "explanation": "Genesis 9:18-19: 'And the sons of Noah who went forth from the ark were Shem and Ham and Japheth... from these the whole earth was overspread.'"
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Genesis & Patriarchs",
        "question": "Select all three patriarchs with whom God established His covenant (God of...):",
        "options": ["Abraham", "Isaac", "Jacob (Israel)", "Joseph", "Moses", "David"],
        "answer": ["Abraham", "Isaac", "Jacob (Israel)"],
        "verse_ref": "Exo. 3:6; Matt. 22:32",
        "explanation": "God is repeatedly revealed as 'the God of Abraham, the God of Isaac, and the God of Jacob.'"
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Exodus & Plagues",
        "question": "Select all plagues brought upon the land of Egypt through Moses in Exodus:",
        "options": [
            "Water turned to blood",
            "Swarm of frogs",
            "Dense plague of locusts",
            "Fiery hail mixed with fire",
            "Massive earthquake",
            "Blinding solar eclipse"
        ],
        "answer": [
            "Water turned to blood",
            "Swarm of frogs",
            "Dense plague of locusts",
            "Fiery hail mixed with fire"
        ],
        "verse_ref": "Exo. 7:20; 8:6; 9:23; 10:14",
        "explanation": "The ten plagues included blood, frogs, gnats, flies, livestock disease, boils, hail, locusts, darkness, and death of the firstborn."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Torah & Pentateuch",
        "question": "Select all five books of the Pentateuch (the Law of Moses):",
        "options": ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges"],
        "answer": ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"],
        "verse_ref": "Luke 24:44",
        "explanation": "The Torah / Pentateuch comprises the first five books of the Bible written by Moses."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Judges of Israel",
        "question": "Select all individuals who served as judges in the Book of Judges:",
        "options": ["Deborah", "Gideon", "Samson", "Ehud", "Aaron", "David"],
        "answer": ["Deborah", "Gideon", "Samson", "Ehud"],
        "verse_ref": "Judg. 3:15; 4:4; 6:11; 13:24",
        "explanation": "Deborah, Gideon, Samson, and Ehud were leaders raised up to deliver Israel in the Book of Judges."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Priesthood & Aaron",
        "question": "Select all four sons of Aaron who were ordained to serve in the priesthood (Exodus 28:1):",
        "options": ["Nadab", "Abihu", "Eleazar", "Ithamar", "Phinehas", "Gershom"],
        "answer": ["Nadab", "Abihu", "Eleazar", "Ithamar"],
        "verse_ref": "Exo. 28:1; Num. 3:2",
        "explanation": "Aaron's four sons were Nadab, Abihu, Eleazar, and Ithamar."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Wisdom & Job",
        "question": "Select all three friends of Job who initially sat in silence and debated him in his suffering:",
        "options": ["Eliphaz the Temanite", "Bildad the Shuhite", "Zophar the Naamathite", "Elihu", "Balaam", "Ahithophel"],
        "answer": ["Eliphaz the Temanite", "Bildad the Shuhite", "Zophar the Naamathite"],
        "verse_ref": "Job 2:11",
        "explanation": "Job 2:11 names Job's three original friends: Eliphaz, Bildad, and Zophar."
    },

    # --- New Testament Multi-Select ---
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "The Gospels",
        "question": "Select all three SYNOPTIC Gospels (Gospels sharing a similar viewpoint and narrative outline):",
        "options": ["Matthew", "Mark", "Luke", "John", "Acts", "Romans"],
        "answer": ["Matthew", "Mark", "Luke"],
        "verse_ref": "Luke 1:1-4",
        "explanation": "Matthew, Mark, and Luke are called the synoptic Gospels ('seeing together'); John presents a uniquely theological perspective."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Genealogy of Christ",
        "question": "Select all women explicitly named in the genealogy of Jesus in Matthew chapter 1:",
        "options": ["Tamar", "Rahab", "Ruth", "Mary", "Sarah", "Esther"],
        "answer": ["Tamar", "Rahab", "Ruth", "Mary"],
        "verse_ref": "Matt. 1:3, 5, 6, 16",
        "explanation": "Matthew 1 uniquely highlights Tamar, Rahab, Ruth, 'the wife of Uriah' (Bathsheba), and Mary."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Nativity of Christ",
        "question": "Select all three distinct treasures presented by the magi to the young child Jesus in Bethlehem:",
        "options": ["Gold", "Frankincense", "Myrrh", "Silver", "Fine linen", "Spices of Lebanon"],
        "answer": ["Gold", "Frankincense", "Myrrh"],
        "verse_ref": "Matt. 2:11",
        "explanation": "Matthew 2:11 records they offered gifts of gold (His kingship), frankincense (His divine priesthood), and myrrh (His redemptive death)."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Gospels & Parables of Luke",
        "question": "Select all famous parables recorded EXCLUSIVELY in the Gospel of Luke:",
        "options": [
            "The Good Samaritan",
            "The Prodigal Son",
            "The Rich Man and Lazarus",
            "The Sower and the Soils",
            "The Ten Virgins",
            "The Mustard Seed"
        ],
        "answer": [
            "The Good Samaritan",
            "The Prodigal Son",
            "The Rich Man and Lazarus"
        ],
        "verse_ref": "Luke 10:30; 15:11; 16:19",
        "explanation": "Luke uniquely includes the Good Samaritan, the Prodigal Son, the Rich Man and Lazarus, and the Pharisee and the Tax Collector."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Gospels & Resurrections",
        "question": "Select all three individuals explicitly recorded in the Gospels as being raised from the dead by Jesus:",
        "options": [
            "Lazarus of Bethany",
            "The widow of Nain's son",
            "Jairus's 12-year-old daughter",
            "John the Baptist",
            "Stephen the Martyr",
            "Nicodemus"
        ],
        "answer": [
            "Lazarus of Bethany",
            "The widow of Nain's son",
            "Jairus's 12-year-old daughter"
        ],
        "verse_ref": "John 11:43-44; Luke 7:14-15; Mark 5:41-42",
        "explanation": "Jesus raised Jairus's daughter from her deathbed, the widow of Nain's son from his open coffin, and Lazarus from the 4-day-old tomb."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Epistles of Paul",
        "question": "Select all fruits of the Holy Spirit explicitly listed in Galatians 5:22-23:",
        "options": ["Love", "Joy", "Peace", "Longsuffering", "Courage", "Prosperity", "Ambition"],
        "answer": ["Love", "Joy", "Peace", "Longsuffering"],
        "verse_ref": "Gal. 5:22-23",
        "explanation": "Galatians 5:22-23 lists: love, joy, peace, longsuffering, kindness, goodness, faithfulness, meekness, self-control."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Epistles of Paul",
        "question": "Select all components of the whole Armor of God described in Ephesians 6:14-17:",
        "options": [
            "Belt of truth",
            "Breastplate of righteousness",
            "Shield of faith",
            "Helmet of salvation",
            "Staff of authority",
            "Chariot of fire"
        ],
        "answer": [
            "Belt of truth",
            "Breastplate of righteousness",
            "Shield of faith",
            "Helmet of salvation"
        ],
        "verse_ref": "Eph. 6:14-17",
        "explanation": "Ephesians 6 outlines the belt of truth, breastplate of righteousness, gospel shoes, shield of faith, helmet of salvation, and sword of the Spirit."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Paul's Prison Epistles",
        "question": "Select all four epistles written by the Apostle Paul while imprisoned in Rome (The Prison Epistles):",
        "options": ["Ephesians", "Philippians", "Colossians", "Philemon", "Romans", "Galatians", "1 Thessalonians"],
        "answer": ["Ephesians", "Philippians", "Colossians", "Philemon"],
        "verse_ref": "Eph. 3:1; Phil. 1:13; Col. 4:18; Philem. 1:1",
        "explanation": "Paul composed Ephesians, Philippians, Colossians, and Philemon during his Roman house arrest."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Paul's Pastoral Epistles",
        "question": "Select all three 'Pastoral Epistles' written by Paul to guide church leadership and pastoral care:",
        "options": ["1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James"],
        "answer": ["1 Timothy", "2 Timothy", "Titus"],
        "verse_ref": "1 Tim. 1:1; 2 Tim. 1:1; Titus 1:1",
        "explanation": "1 Timothy, 2 Timothy, and Titus are collectively designated the Pastoral Epistles."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Gospels & Apostles",
        "question": "Select the three disciples comprising Jesus's inner circle (present at the Transfiguration & Gethsemane):",
        "options": ["Peter", "James (son of Zebedee)", "John", "Andrew", "Philip", "Thomas"],
        "answer": ["Peter", "James (son of Zebedee)", "John"],
        "verse_ref": "Matt. 17:1; 26:37; Mark 5:37",
        "explanation": "Peter, James, and John were uniquely brought along by Jesus to Jairus's daughter's raising, the Transfiguration, and Gethsemane."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Gospels & 'I AM' Statements",
        "question": "Select all divine 'I AM' declarations made by Jesus in the Gospel of John:",
        "options": [
            "I am the Bread of Life",
            "I am the Light of the World",
            "I am the Good Shepherd",
            "I am the True Vine",
            "I am the Sword of Justice",
            "I am the Golden Temple"
        ],
        "answer": [
            "I am the Bread of Life",
            "I am the Light of the World",
            "I am the Good Shepherd",
            "I am the True Vine"
        ],
        "verse_ref": "John 6:35; 8:12; 10:11; 15:1",
        "explanation": "John records seven profound 'I AM' metaphors: Bread of Life, Light of the World, Door, Good Shepherd, Resurrection and Life, Way/Truth/Life, True Vine."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Revelation & The Seven Churches",
        "question": "Select all of the seven historic churches in Asia addressed by the Lord in Revelation 2-3:",
        "options": ["Ephesus", "Smyrna", "Sardis", "Laodicea", "Antioch", "Corinth", "Rome"],
        "answer": ["Ephesus", "Smyrna", "Sardis", "Laodicea"],
        "verse_ref": "Rev. 1:11; 2:1-3:22",
        "explanation": "The seven churches were Ephesus, Smyrna, Pergamum, Thyatira, Sardis, Philadelphia, and Laodicea."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Acts & Leadership",
        "question": "Select all seven men appointed in Acts 6 to oversee the daily distribution of food to widows in Jerusalem:",
        "options": ["Stephen", "Philip", "Prochorus", "Nicanor", "Cornelius", "Silas"],
        "answer": ["Stephen", "Philip", "Prochorus", "Nicanor"],
        "verse_ref": "Acts 6:5",
        "explanation": "Acts 6:5 lists the seven: Stephen, Philip, Prochorus, Nicanor, Timon, Parmenas, and Nicolas."
    },

    # =========================================================================
    # 3. MULTIPLE CHOICE (Deep Theological & Historical Scriptural Questions)
    # =========================================================================
    # --- Old Testament Multiple Choice ---
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Eden",
        "question": "What was the name of the garden in Genesis where Adam and Eve walked with God before the Fall?",
        "options": ["Garden of Eden", "Garden of Gethsemane", "Garden of Uzza", "Mount Moriah"],
        "answer": "Garden of Eden",
        "verse_ref": "Gen. 2:8",
        "explanation": "Genesis 2:8: 'And Jehovah God planted a garden eastward, in Eden; and there He put the man whom He had formed.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Priesthood",
        "question": "In Genesis 14, who was the mysterious King of Salem and Priest of God Most High who brought bread and wine to Abraham?",
        "options": ["Melchizedek", "Abimelech", "Jethro", "Balaam"],
        "answer": "Melchizedek",
        "verse_ref": "Gen. 14:18; Heb. 7:1-3",
        "explanation": "Melchizedek, King of Salem and priest of the Most High God, is a profound type of Christ in Hebrews 7."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Tower of Babel",
        "question": "In Genesis 11, what ancient city was the site of the tower built to make a name for mankind, where God scattered their languages?",
        "options": ["Babel (Babylon)", "Nineveh", "Ur of the Chaldees", "Sodom"],
        "answer": "Babel (Babylon)",
        "verse_ref": "Gen. 11:9",
        "explanation": "Genesis 11:9: 'Therefore its name was called Babel, because there Jehovah confounded the language of all the earth.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Exodus & Midian",
        "question": "What was the name of the priest of Midian whose daughter Zipporah married Moses in the wilderness?",
        "options": ["Jethro (Reuel)", "Melchizedek", "Balaam", "Abimelech"],
        "answer": "Jethro (Reuel)",
        "verse_ref": "Exo. 2:18; 3:1",
        "explanation": "Exodus 3:1: 'Now Moses was shepherding the flock of Jethro his father-in-law, the priest of Midian.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Minor Prophets",
        "question": "Which prophet was commanded by the Lord to marry Gomer as a living portrait of God's unfaithful covenant people?",
        "options": ["Hosea", "Amos", "Micah", "Habakkuk"],
        "answer": "Hosea",
        "verse_ref": "Hosea 1:2",
        "explanation": "Hosea married Gomer, and his redeeming love for her reflected Yahweh's unfailing, redeeming love for wayward Israel."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Judges & Conquest",
        "question": "Which judge of Israel routed a massive Midianite host with only 300 men carrying trumpets and torches inside clay pitchers?",
        "options": ["Gideon (Jerubbaal)", "Samson", "Jephthah", "Barak"],
        "answer": "Gideon (Jerubbaal)",
        "verse_ref": "Judg. 7:7, 19-22",
        "explanation": "The Lord reduced Gideon's army from 32,000 to 300 so Israel could not boast that their own strength saved them."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Kings & Prophets",
        "question": "On which mountain summit did Elijah challenge the 450 prophets of Baal to a showdown of fire from heaven?",
        "options": ["Mount Carmel", "Mount Sinai / Horeb", "Mount Nebo", "Mount Hermon"],
        "answer": "Mount Carmel",
        "verse_ref": "1 Kings 18:19-38",
        "explanation": "Elijah confronted Ahab and the false prophets on Mount Carmel, where God answered with consuming fire."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Kings & Prophets",
        "question": "In 2 Kings 2, what heavenly vehicle appeared with a whirlwind to take the prophet Elijah alive into heaven?",
        "options": ["Chariot and horses of fire", "A pillar of cloud", "A flying scroll", "A fiery cloud of angels"],
        "answer": "Chariot and horses of fire",
        "verse_ref": "2 Kings 2:11",
        "explanation": "2 Kings 2:11: 'There appeared a chariot of fire and horses of fire... and Elijah went up by a whirlwind into heaven.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Major Prophets & Visions",
        "question": "Which prophet was set down in the midst of a valley full of dry bones and commanded to prophesy life to them?",
        "options": ["Ezekiel", "Jeremiah", "Isaiah", "Daniel"],
        "answer": "Ezekiel",
        "verse_ref": "Ezek. 37:1-10",
        "explanation": "Ezekiel 37 depicts the breath of God entering the slain dry bones of Israel to form an exceedingly great army."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Daniel & Prophecy",
        "question": "During King Belshazzar's banquet, what divine words were inscribed by a mysterious hand upon the palace wall?",
        "options": ["MENE, MENE, TEKEL, UPHARSIN", "ICHABOD, ICHABOD", "MARANATHA, ELOI", "TALITHA CUMI"],
        "answer": "MENE, MENE, TEKEL, UPHARSIN",
        "verse_ref": "Dan. 5:25-28",
        "explanation": "Daniel interpreted: God has numbered your kingdom, you are weighed in the balances and found lacking, and your kingdom is divided."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Historical Books",
        "question": "Which Jewish cupbearer to King Artaxerxes of Persia wept and returned to rebuild the broken walls of Jerusalem in 52 days?",
        "options": ["Nehemiah", "Ezra", "Zerubbabel", "Mordecai"],
        "answer": "Nehemiah",
        "verse_ref": "Neh. 1:11; 6:15",
        "explanation": "Nehemiah led the remnant with a trowel in one hand and a weapon in the other, finishing the wall in 52 days."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Kings & Miracles",
        "question": "In which river did the prophet Elisha instruct Naaman the Syrian commander to dip seven times to heal his leprosy?",
        "options": ["Jordan River", "Nile River", "Euphrates River", "Abana River"],
        "answer": "Jordan River",
        "verse_ref": "2 Kings 5:10-14",
        "explanation": "Naaman humbled himself and dipped seven times in the Jordan, and his flesh was restored like the flesh of a little child."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Samuel & David",
        "question": "Which prophet confronted King David regarding Bathsheba using the heart-rending parable of the poor man's ewe lamb?",
        "options": ["Nathan", "Gad", "Samuel", "Ahijah"],
        "answer": "Nathan",
        "verse_ref": "2 Sam. 12:1-7",
        "explanation": "Nathan declared to David: 'You are the man!', bringing King David to deep repentance expressed in Psalm 51."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Historical Books & Ruth",
        "question": "What was the name of the wealthy landowner of Bethlehem who served as the faithful kinsman-redeemer for Ruth?",
        "options": ["Boaz", "Elimelech", "Mahlon", "Chilion"],
        "answer": "Boaz",
        "verse_ref": "Ruth 4:9-10",
        "explanation": "Boaz redeemed the land and married Ruth; their son Obed became the grandfather of King David."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Samuel & Ark of God",
        "question": "What Philistine idol fell face down on the ground and had its head and hands broken off before the Ark of the Lord in Ashdod?",
        "options": ["Dagon", "Baal-Zebub", "Ashtoreth", "Molech"],
        "answer": "Dagon",
        "verse_ref": "1 Sam. 5:2-4",
        "explanation": "1 Samuel 5 records that the statue of the fish-god Dagon collapsed in pieces before the holy Ark of God."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Historical Books & Esther",
        "question": "Who was the wicked Persian royal official who plotted genocide against the Jews and built a 50-cubit gallows, on which he was hanged?",
        "options": ["Haman", "Sanballat", "Tobiah", "Bigthan"],
        "answer": "Haman",
        "verse_ref": "Esth. 7:9-10",
        "explanation": "Haman the Agagite's conspiracy was exposed by Queen Esther, and he was hanged on his own gallows."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Kings of Judah",
        "question": "Which King of Judah was struck with leprosy in his forehead when he entered the holy temple to unlawfully burn incense?",
        "options": ["Uzziah (Azariah)", "Hezekiah", "Josiah", "Jehoshaphat"],
        "answer": "Uzziah (Azariah)",
        "verse_ref": "2 Chron. 26:16-21",
        "explanation": "2 Chronicles 26:19 notes that while Uzziah was raging against the priests with a censer in his hand, leprosy broke out on his forehead."
    },

    # --- New Testament Multiple Choice ---
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Passion",
        "question": "In Matthew 27:32, who was the man from Cyrene compelled by Roman soldiers to carry Jesus's cross?",
        "options": ["Simon of Cyrene", "Joseph of Arimathea", "Barabbas", "Nicodemus"],
        "answer": "Simon of Cyrene",
        "verse_ref": "Matt. 27:32; Mark 15:21",
        "explanation": "Simon of Cyrene was seized as he was coming from the country to carry the cross beam behind Jesus."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Nicodemus",
        "question": "What prominent Pharisee and ruler of the Jews came to Jesus by night, to whom Jesus said 'You must be born anew'?",
        "options": ["Nicodemus", "Gamaliel", "Joseph of Arimathea", "Simon the Leper"],
        "answer": "Nicodemus",
        "verse_ref": "John 3:1-7",
        "explanation": "Nicodemus came by night; Jesus revealed to him the necessity of regeneration by the Spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Miracles",
        "question": "In John 2, in which Galilean village did Jesus perform His first miraculous sign by turning water into wine at a wedding?",
        "options": ["Cana", "Capernaum", "Nazareth", "Bethsaida"],
        "answer": "Cana",
        "verse_ref": "John 2:1-11",
        "explanation": "John 2:11: 'This beginning of signs Jesus did in Cana of Galilee and manifested His glory, and His disciples believed into Him.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Burial of Jesus",
        "question": "Who was the wealthy council member who boldly went to Pilate, requested Jesus's body, and wrapped Him in linen in his own new tomb?",
        "options": ["Joseph of Arimathea", "Nicodemus", "Lazarus", "Simon of Cyrene"],
        "answer": "Joseph of Arimathea",
        "verse_ref": "Matt. 27:57-60",
        "explanation": "Joseph of Arimathea, a disciple of Jesus in secret, placed Jesus's body in his own freshly hewn tomb in fulfillment of Isaiah 53:9."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Living Water",
        "question": "In John 4, at which historic well in Samaria did Jesus converse with the Samaritan woman concerning living water?",
        "options": ["Jacob's Well", "Abraham's Well", "Beer-sheba", "Pool of Bethesda"],
        "answer": "Jacob's Well",
        "verse_ref": "John 4:5-6",
        "explanation": "John 4:6: 'And Jacob's spring was there. Jesus therefore, being wearied from the journey, sat thus by the spring.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Bethesda",
        "question": "What pool in Jerusalem with five porches was the site where Jesus healed a man who had been sick for thirty-eight years?",
        "options": ["Pool of Bethesda", "Pool of Siloam", "Sea of Galilee", "River Jordan"],
        "answer": "Pool of Bethesda",
        "verse_ref": "John 5:2-9",
        "explanation": "John 5:2: 'Now there is in Jerusalem near the Sheep Gate a pool, which is called in Hebrew Bethesda, having five porches.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Miracles",
        "question": "In Troas, what young man sank into a deep sleep during Paul's midnight sermon and fell out of a third-story window to his death, but was restored by Paul?",
        "options": ["Eutychus", "Trophimus", "Onesimus", "Epaphras"],
        "answer": "Eutychus",
        "verse_ref": "Acts 20:9-10",
        "explanation": "Acts 20:9-10 records that Paul went down, fell upon Eutychus, embraced him, and said 'Do not make a commotion, for his life is in him.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Imprisonment",
        "question": "In which Macedonian city were Paul and Silas singing hymns at midnight in the inner prison when an earthquake loosed their chains?",
        "options": ["Philippi", "Thessalonica", "Berea", "Corinth"],
        "answer": "Philippi",
        "verse_ref": "Acts 16:25-26",
        "explanation": "In Philippi, the prison earthquake led directly to the salvation and baptism of the Philippian jailer and his entire household."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Athens",
        "question": "On which rocky promontory in Athens did the Apostle Paul deliver his address to the Greek philosophers regarding the 'UNKNOWN GOD'?",
        "options": ["The Areopagus (Mars Hill)", "The Acropolis", "Mount Hermon", "Mount Moriah"],
        "answer": "The Areopagus (Mars Hill)",
        "verse_ref": "Acts 17:19, 22-23",
        "explanation": "Paul stood in the midst of the Areopagus and proclaimed God who made the world and does not dwell in temples made with hands."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Philip",
        "question": "On the desert road from Jerusalem to Gaza, what high official was reading Isaiah in his chariot when evangelist Philip climbed in to preach Christ?",
        "options": ["The Ethiopian Eunuch", "Cornelius the Centurion", "Sergius Paulus", "The Jailer of Philippi"],
        "answer": "The Ethiopian Eunuch",
        "verse_ref": "Acts 8:27-38",
        "explanation": "The treasurer of Queen Candace of Ethiopia asked 'Of whom does the prophet say this?' and Philip baptized him in water on the road."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Early Church",
        "question": "Who was the eloquent Jewish teacher from Alexandria, mighty in Scriptures, who was mentored privately in Ephesus by Priscilla and Aquila?",
        "options": ["Apollos", "Barnabas", "Stephen", "Silas"],
        "answer": "Apollos",
        "verse_ref": "Acts 18:24-26",
        "explanation": "Acts 18:26: 'Priscilla and Aquila took him to them and expounded the way of God to him more accurately.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Peter's Release",
        "question": "In Acts 12, what servant girl was so overjoyed to hear Peter's voice at the gate after an angel broke him out of prison that she forgot to open it?",
        "options": ["Rhoda", "Tabitha", "Lydia", "Phoebe"],
        "answer": "Rhoda",
        "verse_ref": "Acts 12:13-14",
        "explanation": "Acts 12:14: 'And recognizing Peter's voice, from joy she did not open the gate, but ran in and announced that Peter was standing before the gate.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Converts",
        "question": "In Philippi, who was the merchant woman and seller of purple dye from Thyatira whose heart the Lord opened to receive the gospel?",
        "options": ["Lydia", "Phoebe", "Dorcas", "Chloe"],
        "answer": "Lydia",
        "verse_ref": "Acts 16:14-15",
        "explanation": "Lydia became the first recorded Christian convert in Europe and hosted the apostles in her home."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Bartimaeus",
        "question": "What was the name of the blind beggar who threw off his cloak and cried out 'Son of David, have mercy on me!' outside Jericho?",
        "options": ["Bartimaeus", "Zacchaeus", "Malchus", "Simon of Cyrene"],
        "answer": "Bartimaeus",
        "verse_ref": "Mark 10:46-52",
        "explanation": "Mark 10:46 identifies the blind beggar as Bartimaeus, the son of Timaeus, who received his sight and followed Jesus."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Gethsemane",
        "question": "In the Garden of Gethsemane, what was the name of the high priest's slave whose right ear was sliced off by Simon Peter?",
        "options": ["Malchus", "Barabbas", "Caiaphas", "Alexander"],
        "answer": "Malchus",
        "verse_ref": "John 18:10; Luke 22:51",
        "explanation": "John 18:10 notes the slave's name was Malchus; Luke records that Jesus touched his ear and healed him instantly."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Thomas",
        "question": "Which apostle famously doubted Christ's physical resurrection until he could see the nail prints and touch His pierced side?",
        "options": ["Thomas (Didymus)", "Philip", "Bartholomew", "Thaddaeus"],
        "answer": "Thomas (Didymus)",
        "verse_ref": "John 20:24-28",
        "explanation": "When Jesus appeared, Thomas exclaimed the highest confession of faith in the Gospels: 'My Lord and my God!'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Epistles & Hall of Faith",
        "question": "Which New Testament epistle contains the famous chapter 11 'Hall of Faith', recounting heroes from Abel to the prophets?",
        "options": ["Hebrews", "Romans", "James", "1 Peter"],
        "answer": "Hebrews",
        "verse_ref": "Heb. 11:1-40",
        "explanation": "Hebrews 11 defines faith as 'the substantiation of things hoped for, the conviction of things not seen', recounting the faithful cloud of witnesses."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & Patmos",
        "question": "On which Aegean island was the Apostle John in exile 'for the word of God and the testimony of Jesus' when he received Revelation?",
        "options": ["Patmos", "Crete", "Cyprus", "Rhodes"],
        "answer": "Patmos",
        "verse_ref": "Rev. 1:9",
        "explanation": "Revelation 1:9: 'I John... was on the island called Patmos for the word of God and the testimony of Jesus.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Epistles of Paul",
        "question": "What was the name of the runaway slave in Philemon whom Paul led to Christ and sent back as a beloved brother?",
        "options": ["Onesimus", "Tychicus", "Epaphras", "Aristarchus"],
        "answer": "Onesimus",
        "verse_ref": "Philem. 10-16",
        "explanation": "Paul appealed for Onesimus (whose name means 'profitable'), urging Philemon to receive him no longer as a slave, but as a brother."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Early Church",
        "question": "What was the name of the Roman centurion of the Italian cohort in Caesarea whose conversion opened the door of the gospel to the Gentiles?",
        "options": ["Cornelius", "Julius", "Claudius Lysias", "Longinus"],
        "answer": "Cornelius",
        "verse_ref": "Acts 10:1-2, 44-48",
        "explanation": "Cornelius was a devout, God-fearing centurion whom Peter visited after receiving the vision of the descending sheet."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Christology",
        "question": "According to John 11:35 in English translations, what is celebrated as the shortest verse in the Bible?",
        "options": ["'Jesus wept.'", "'Rejoice always.'", "'Pray without ceasing.'", "'Remember Lot's wife.'"],
        "answer": "'Jesus wept.'",
        "verse_ref": "John 11:35",
        "explanation": "John 11:35 consists of just two words ('Jesus wept'), revealing the Lord's deep human compassion at Lazarus's tomb."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Martyrs",
        "question": "Who was the first Christian martyr recorded in the Book of Acts, who saw Jesus standing at the right hand of God as he was stoned?",
        "options": ["Stephen", "James the brother of John", "Barnabas", "Philip the Evangelist"],
        "answer": "Stephen",
        "verse_ref": "Acts 7:55-60",
        "explanation": "Stephen was full of faith and the Holy Spirit, crying out 'Lord, do not hold this sin against them!' as he died."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Epistles of Paul",
        "question": "In Romans 16, what female servant (deaconess) of the church in Cenchrea was commended by Paul to carry his master epistle to Rome?",
        "options": ["Phoebe", "Priscilla", "Junia", "Chloe"],
        "answer": "Phoebe",
        "verse_ref": "Rom. 16:1-2",
        "explanation": "Romans 16:1 commends Phoebe, a deaconess of the church in Cenchrea and a patroness of many including Paul."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Early Church",
        "question": "In which cosmopolitan Syrian city were the disciples of Jesus first called 'Christians'?",
        "options": ["Antioch", "Jerusalem", "Alexandria", "Ephesus"],
        "answer": "Antioch",
        "verse_ref": "Acts 11:26",
        "explanation": "Acts 11:26: 'And the disciples were first called Christians in Antioch.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Shipwreck",
        "question": "On which Mediterranean island was Paul shipwrecked for three months on his voyage to Rome, where he was bitten by a viper unharmed?",
        "options": ["Malta (Melita)", "Crete", "Cyprus", "Patmos"],
        "answer": "Malta (Melita)",
        "verse_ref": "Acts 28:1-6",
        "explanation": "Acts 28:1 records they learned the island was Malta, where the natives showed unusual kindness and saw Paul shake off the snake into the fire."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Zacchaeus",
        "question": "In Luke 19, what kind of tree did the short tax collector Zacchaeus climb in Jericho so he could see Jesus pass by?",
        "options": ["Sycamore tree", "Olive tree", "Fig tree", "Cedar of Lebanon"],
        "answer": "Sycamore tree",
        "verse_ref": "Luke 19:4",
        "explanation": "Luke 19:4: 'And running on before, he climbed up into a sycamore tree to see Him, for He was about to pass through that way.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Trial of Jesus",
        "question": "Who was the Jewish high priest who presided over Jesus's Sanhedrin trial and tore his robes claiming Jesus committed blasphemy?",
        "options": ["Caiaphas", "Annas", "Gamaliel", "Nicodemus"],
        "answer": "Caiaphas",
        "verse_ref": "Matt. 26:57, 65",
        "explanation": "Matthew 26:65: 'Then the high priest tore his garments, saying, He has blasphemed! What further need do we have of witnesses?'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & Christology",
        "question": "In Revelation 19:16, what majestic title is written upon the garment and thigh of the Rider on the white horse?",
        "options": ["KING OF KINGS AND LORD OF LORDS", "ALPHA AND OMEGA", "LION OF THE TRIBE OF JUDAH", "PRINCE OF PEACE"],
        "answer": "KING OF KINGS AND LORD OF LORDS",
        "verse_ref": "Rev. 19:16",
        "explanation": "Revelation 19:16: 'And He has on His garment and on His thigh a name written: KING OF KINGS AND LORD OF LORDS.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Epistles & Scribes",
        "question": "In Romans 16:22, who was the faithful scribe / amanuensis who wrote down the Epistle to the Romans from Paul's dictation?",
        "options": ["Tertius", "Timothy", "Luke", "Tychicus"],
        "answer": "Tertius",
        "verse_ref": "Rom. 16:22",
        "explanation": "Romans 16:22: 'I, Tertius, who write this epistle, greet you in the Lord.'"
    },

    # =========================================================================
    # 4. TRUE OR FALSE (New & Old Testament Scriptural Facts vs Common Myths)
    # =========================================================================
    # --- New Testament True / False ---
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Crucifixion of Christ",
        "question": "Jesus spoke seven distinct recorded sayings while hanging upon the cross at Calvary.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Luke 23:34; John 19:30",
        "explanation": "True! The Seven Last Words from the cross are recorded across the four Gospels (including 'Father, forgive them' and 'It is finished')."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Gospels & Parables",
        "question": "The Gospel of John contains the parable of the Good Samaritan and the parable of the Prodigal Son.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Luke 10:30-37; 15:11-32",
        "explanation": "False! Both parables are found exclusively in the Gospel of Luke; John contains zero traditional narrative parables."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Nativity of Christ",
        "question": "The Gospel of Matthew explicitly states that exactly THREE wise men (magi) visited the young child Jesus in Bethlehem.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Matt. 2:1-11",
        "explanation": "False! Matthew mentions three gifts (gold, frankincense, myrrh), but the Bible never specifies the exact number of magi."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Acts & Paul",
        "question": "Apostle Paul was a Roman citizen by birth, which gave him the legal right to appeal his capital trial to Caesar in Rome.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Acts 22:28; 25:11",
        "explanation": "True! When the commander noted he bought his citizenship for a large sum, Paul replied: 'But I was born a citizen.'"
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Gospels & Miracles",
        "question": "Simon Peter successfully stepped out of the boat and walked on water toward Jesus before beginning to sink in the strong wind.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Matt. 14:29-30",
        "explanation": "True! Matthew 14:29: 'And Peter got down from the boat and walked on the water and came toward Jesus.'"
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Acts & Bereans",
        "question": "The believers in Berea were commended in Acts 17 as more noble because they examined the Scriptures daily to verify Paul's teachings.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Acts 17:11",
        "explanation": "True! Acts 17:11: 'Now these were more noble... examining the Scriptures daily to see whether these things were so.'"
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Epistle of James",
        "question": "The Epistle of James compares the uncontrolled tongue to a tiny rudder that steers a mighty ship and a spark that ignites a whole forest.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "James 3:4-5",
        "explanation": "True! James 3 illustrates how a tiny member like the tongue boasts great things and sets on fire the course of life."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Crucifixion of Christ",
        "question": "The Apostle John was the only one of the twelve male apostles explicitly recorded as standing near the cross at Jesus's death.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "John 19:26-27",
        "explanation": "True! Jesus looked down from the cross and entrusted His mother Mary to the beloved disciple John."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Gospels & Apostles",
        "question": "Apostle Matthew worked as a fisherman on the Sea of Galilee before Jesus called him to follow Him.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Matt. 9:9",
        "explanation": "False! Matthew (Levi) was a tax collector sitting at the tax collection booth in Capernaum when Jesus called him."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Doctrine & Scripture",
        "question": "The English theological word 'Trinity' appears explicitly as a written term in the New Testament manuscripts.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Matt. 28:19; 2 Cor. 13:14",
        "explanation": "False! While the Triune nature of God (Father, Son, and Holy Spirit) is profoundly revealed throughout Scripture, the word 'Trinity' itself is not in the biblical text."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "New Testament Canon",
        "question": "The word 'Christian' is used only three times in the entire New Testament text.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Acts 11:26; 26:28; 1 Pet. 4:16",
        "explanation": "True! The term appears only three times: in Acts 11:26 (Antioch), Acts 26:28 (King Agrippa), and 1 Peter 4:16."
    },
    {
        "type": "true_false",
        "testament": "New Testament",
        "category": "Epistles & Love",
        "question": "The famous 'Love Chapter' of the Bible is 1 Corinthians chapter 13.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "1 Cor. 13:1-13",
        "explanation": "True! 1 Corinthians 13 describes the surpassing way of divine love that never fails."
    },

    # --- Old Testament True / False ---
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Popular Bible Myths",
        "question": "The phrase 'God helps those who help themselves' is a literal verse found in the Book of Proverbs.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Prov. 3:5-6; Jer. 17:5-7",
        "explanation": "False! The phrase originated from ancient Greek fables and was popularized by Benjamin Franklin. Scripture teaches absolute trust in the Lord!"
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Kings of Israel",
        "question": "King Solomon spoke over 3,000 proverbs and composed 1,005 songs according to 1 Kings 4:32.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "1 Kings 4:32",
        "explanation": "True! 1 Kings 4:32 states: 'And he spoke three thousand proverbs, and his songs were a thousand and five.'"
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Deuteronomy & Moses",
        "question": "Moses was permitted to cross the Jordan River and live in the Promised Land before his death.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Deut. 34:4-5",
        "explanation": "False! Moses climbed Mount Nebo and viewed the land from afar, but died in Moab without entering."
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Genesis & Eden",
        "question": "The forbidden fruit eaten by Adam and Eve in Genesis is explicitly identified as an apple.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Gen. 3:3-6",
        "explanation": "False! Genesis refers strictly to the 'fruit of the tree of the knowledge of good and evil'; the apple idea came from Latin wordplay (malum)."
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Genesis & Kings",
        "question": "Enoch and Elijah are the only two Old Testament figures explicitly recorded as being taken to God without experiencing physical death.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Gen. 5:24; 2 Kings 2:11; Heb. 11:5",
        "explanation": "True! Enoch walked with God and was not, for God took him; Elijah went up into heaven in a whirlwind."
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Historical Books",
        "question": "The entire Book of Esther never once directly contains the explicit Hebrew name for God (Yahweh or Elohim).",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Esth. 4:14",
        "explanation": "True! While God's sovereign hand and hidden providence saturate every chapter, God is not directly named in the text."
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "1 Samuel & David",
        "question": "Young David struck down and killed the giant Goliath using a sword in his initial attack.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "1 Sam. 17:50",
        "explanation": "False! 1 Samuel 17:50 emphasizes: 'So David prevailed over the Philistine with a sling and with a stone... and there was no sword in the hand of David.'"
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Exodus & Mount Sinai",
        "question": "The golden calf worshipped by Israel while Moses was on Mount Sinai was fashioned by Moses's brother Aaron.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Exo. 32:2-4",
        "explanation": "True! Aaron collected the gold rings from the people and fashioned a molten calf with a graving tool."
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Minor Prophets & Jonah",
        "question": "Prophet Jonah rejoiced and was happy when the city of Nineveh repented in sackcloth and God spared them from judgment.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Jonah 4:1-2",
        "explanation": "False! Jonah was exceedingly angry and complained to God because he wanted Nineveh destroyed."
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Joshua & Jericho",
        "question": "The fortified walls of Jericho collapsed after the Israelites marched around the city for seven days and sounded shofars.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Josh. 6:20",
        "explanation": "True! On the seventh day after seven circuits, the people shouted and the wall fell down flat."
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Daniel & Lions",
        "question": "Prophet Daniel was cast into the den of lions because he refused to cease praying three times a day to his God toward Jerusalem.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Dan. 6:10, 16",
        "explanation": "True! Daniel 6:10 records Daniel continued his custom of kneeling in prayer three times daily with windows opened toward Jerusalem."
    },
    # =========================================================================
    # OLD TESTAMENT - RECOVERY TRUTHS & TYPES
    # =========================================================================
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Two Trees",
        "question": "In Genesis 2:9, what was growing in the middle of the garden of Eden representing God wishing to impart Himself as eternal life to man?",
        "options": ["The tree of life", "The tree of the knowledge of good and evil", "The golden vine", "The tree of wisdom"],
        "answer": "The tree of life",
        "verse_ref": "Gen. 2:9",
        "explanation": "Genesis 2:9 shows the tree of life in the midst of the garden, typifying God in Christ as life in the form of food for man to receive."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Calling",
        "question": "During the generation of Seth's son Enosh (whose name means frail, mortal man), what crucial practice began among mankind (Genesis 4:26)?",
        "options": ["Calling upon the name of Jehovah", "Building walled cities", "Offering burnt incense on golden altars", "Writing sacred scrolls"],
        "answer": "Calling upon the name of Jehovah",
        "verse_ref": "Gen. 4:26",
        "explanation": "Genesis 4:26 declares: 'At that time men began to call upon the name of Jehovah.' When man realized his weakness and mortality, he began to call upon Jehovah."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Patriarchs",
        "question": "Who walked with God for three hundred years in oneness with God and was taken by God, so that he did not see death (Genesis 5:22, 24)?",
        "options": ["Enoch", "Methuselah", "Noah", "Melchizedek"],
        "answer": "Enoch",
        "verse_ref": "Gen. 5:22-24",
        "explanation": "Genesis 5:22 and 24 record that Enoch walked with God for 300 years after begetting Methuselah, and he was not, for God took him."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Bethel",
        "question": "When Jacob awoke from his dream of the heavenly ladder, what did he name that place, declaring it to be 'the house of God and gate of heaven'?",
        "options": ["Bethel", "Peniel", "Mahanaim", "Shechem"],
        "answer": "Bethel",
        "verse_ref": "Gen. 28:17-19",
        "explanation": "Genesis 28:19 records Jacob named the place Bethel ('Beth' = house, 'El' = God), setting up the stone pillar as the house of God."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Exodus & Moses",
        "question": "When Jehovah appeared to Moses on Mount Horeb in a flame of fire out of the midst of a thornbush (Exodus 3:2), what was remarkable about it?",
        "options": ["The thornbush burned with fire, but was not consumed", "The thornbush turned into pure gold", "The thornbush immediately sprouted sweet figs", "The thornbush vanished into thin air"],
        "answer": "The thornbush burned with fire, but was not consumed",
        "verse_ref": "Exo. 3:2",
        "explanation": "Exodus 3:2: 'And the thornbush burned with fire, yet the thornbush was not consumed,' signifying God shining through redeemed humanity without consuming human energy."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Exodus & Tabernacle",
        "question": "According to Exodus 30:23-25, which four principal spices were compounded with a hin of olive oil to prepare the holy anointing oil? (Select all 4)",
        "options": ["Flowing myrrh", "Sweet-smelling cinnamon", "Sweet-smelling calamus", "Cassia", "Frankincense", "Henna"],
        "answer": ["Flowing myrrh", "Sweet-smelling cinnamon", "Sweet-smelling calamus", "Cassia"],
        "verse_ref": "Exo. 30:23-25",
        "explanation": "Exodus 30:23-25 specifies 500 shekels of myrrh, 250 of cinnamon, 250 of calamus, and 500 of cassia with a hin of olive oil, typifying the compound Spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Exodus & Lampstand",
        "question": "In Exodus 25:31, what material was used to make the golden lampstand in the tabernacle, and how was it crafted?",
        "options": ["Pure beaten gold of one piece", "Acacia wood overlaid with brass", "Cast bronze with silver plating", "Carved cedarwood lined with gold"],
        "answer": "Pure beaten gold of one piece",
        "verse_ref": "Exo. 25:31",
        "explanation": "Exodus 25:31 specifies: 'You shall make a lampstand of pure gold; of beaten work shall the lampstand be made,' typifying the embodiment of the Triune God."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Exodus & Wilderness",
        "question": "At Rephidim (Horeb), what did God command Moses to strike so that living water would flow out for the thirsty people to drink (Exodus 17:6)?",
        "options": ["The rock", "The desert sands", "The dry riverbed", "The base of Mount Sinai"],
        "answer": "The rock",
        "verse_ref": "Exo. 17:6",
        "explanation": "Exodus 17:6: 'You shall strike the rock, and water will come out of it so that the people may drink.' 1 Corinthians 10:4 confirms 'the rock was Christ.'"
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Leviticus & Offerings",
        "question": "According to Leviticus 2:13, every meal offering offered to Jehovah was required to be seasoned with the salt of the covenant of God.",
        "options": ["True", "False"],
        "answer": "True",
        "verse_ref": "Lev. 2:13",
        "explanation": "True! Leviticus 2:13 commands: 'Every offering of your meal offering you shall season with salt... you shall not let the salt of the covenant of your God be lacking.'"
    },
    {
        "type": "true_false",
        "testament": "Old Testament",
        "category": "Leviticus & Priesthood",
        "question": "According to Leviticus 6:13, the fire on the bronze altar of burnt offering was allowed to go out each night after the evening sacrifice.",
        "options": ["True", "False"],
        "answer": "False",
        "verse_ref": "Lev. 6:13",
        "explanation": "False! Leviticus 6:13 commands: 'Fire shall be kept burning on the altar continually; it shall not go out.'"
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Numbers & Priesthood",
        "question": "According to Numbers 17:8, when Aaron's rod for the house of Levi budded overnight in the tent of the testimony, what three things did it put forth? (Select all 3)",
        "options": ["Buds", "Blossoms", "Ripe almonds", "Golden olives", "Sweet figs", "Pomegranates"],
        "answer": ["Buds", "Blossoms", "Ripe almonds"],
        "verse_ref": "Num. 17:8",
        "explanation": "Numbers 17:8 records: 'The rod of Aaron for the house of Levi had sprouted and put forth buds and produced blossoms and bore ripe almonds,' typifying resurrection life."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Numbers & Living Water",
        "question": "In Numbers 21:17-18, what did the children of Israel sing when water was given at the well dug by the leaders with their scepters?",
        "options": ["Spring up, O well! Sing to it!", "Flow, O mighty river of God!", "Shout for joy, O Israel!", "Rejoice in the living fountain!"],
        "answer": "Spring up, O well! Sing to it!",
        "verse_ref": "Num. 21:17-18",
        "explanation": "Numbers 21:17: 'Then Israel sang this song: Spring up, O well! Sing to it! The well which the leaders sank, which the nobles of the people dug...'"
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Deuteronomy & Good Land",
        "question": "Deuteronomy 8:7-8 portrays the all-inclusive good land as rich in which agricultural produce? (Select all that apply)",
        "options": ["Wheat and barley", "Vines and fig trees", "Pomegranates", "Olive trees and honey", "Apples and oranges", "Walnuts and dates"],
        "answer": ["Wheat and barley", "Vines and fig trees", "Pomegranates", "Olive trees and honey"],
        "verse_ref": "Deut. 8:7-8",
        "explanation": "Deuteronomy 8:8 lists: 'A land of wheat and barley and vines and fig trees and pomegranates; a land of olive trees with oil and of honey' - types of the unsearchable riches of Christ."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Deuteronomy & Oneness",
        "question": "In Deuteronomy 12:5, where did God command His people to bring their offerings rather than offering them in every place they chose?",
        "options": ["To the place which Jehovah your God chooses out of all your tribes to put His name there", "To the highest peak in each tribe's boundary", "At each family's private threshold", "In any walled city with twelve gates"],
        "answer": "To the place which Jehovah your God chooses out of all your tribes to put His name there",
        "verse_ref": "Deut. 12:5",
        "explanation": "Deuteronomy 12:5 preserves the oneness of God's people by designating one unique place of worship where Jehovah put His name and habitation."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "2 Samuel & Building",
        "question": "When King David wished to build a house for God (2 Samuel 7:12-13), what did God reveal to him through Nathan the prophet?",
        "options": ["God would first build David a house and raise up his seed to establish an eternal throne and build God's house", "David was commanded to cut down Lebanon's cedars immediately", "God preferred to live in tents forever with no temple", "David's general Joab was commissioned to build the house"],
        "answer": "God would first build David a house and raise up his seed to establish an eternal throne and build God's house",
        "verse_ref": "2 Sam. 7:12-13",
        "explanation": "2 Samuel 7:12-13 shows God's economy: before man can build for God, God must build Christ into man. God promised to build David a house and raise up his seed."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Psalms & Oneness",
        "question": "In Psalm 133:1-2, the pleasantness of brothers dwelling together in oneness is compared to what flowing down Aaron's beard?",
        "options": ["The fine oil upon the head", "Living spring water from Mount Zion", "Sweet frankincense smoke", "Golden honey from the rock"],
        "answer": "The fine oil upon the head",
        "verse_ref": "Psa. 133:1-2",
        "explanation": "Psalm 133:2: 'It is like the fine oil upon the head that ran down upon the beard, upon the beard of Aaron, that ran down upon the hem of his garments.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Psalms & Enjoyment",
        "question": "According to Psalm 36:8-9, with what are God's people saturated in His presence, and what is with God?",
        "options": ["Saturated with the fatness of Your house, for with You is the fountain of life", "Enriched with gold and silver from the temple vaults", "Adorned with royal crowns and purple robes", "Shielded by chariot legions from all enemies"],
        "answer": "Saturated with the fatness of Your house, for with You is the fountain of life",
        "verse_ref": "Psa. 36:8-9",
        "explanation": "Psalm 36:8-9: 'They are saturated with the fatness of Your house, and You cause them to drink of the river of Your pleasures. For with You is the fountain of life; in Your light we see light.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Isaiah & Salvation",
        "question": "According to Isaiah 12:3-4, how do God's people draw water out of the springs of salvation?",
        "options": ["With joy, praising Jehovah and calling upon His name", "With silent sorrow and heavy fasting", "By bringing costly silver vessels to the priests", "By digging deep physical irrigation wells"],
        "answer": "With joy, praising Jehovah and calling upon His name",
        "verse_ref": "Isa. 12:3-4",
        "explanation": "Isaiah 12:3-4: 'Therefore with joy shall you draw water out of the springs of salvation. And in that day you will say, Give thanks to Jehovah; call upon His name!'"
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Jeremiah & Evils",
        "question": "In Jeremiah 2:13, what two evils did God charge His people with committing? (Select both)",
        "options": ["Forsaking Jehovah, the fountain of living waters", "Hewing out for themselves broken cisterns that can hold no water", "Failing to pay tribute to the king of Babylon", "Refusing to build stone altars on mountaintops"],
        "answer": ["Forsaking Jehovah, the fountain of living waters", "Hewing out for themselves broken cisterns that can hold no water"],
        "verse_ref": "Jer. 2:13",
        "explanation": "Jeremiah 2:13: 'For My people have committed two evils: They have forsaken Me, the fountain of living waters, to hew out for themselves cisterns, broken cisterns, which can hold no water.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Jeremiah & Eating the Word",
        "question": "What did the prophet Jeremiah say took place when God's words were found (Jeremiah 15:16)?",
        "options": ["Your words were found and I ate them, and Your word became the gladness and joy of my heart", "Your words were found and carved onto two tables of stone", "Your words were placed into an ark and hidden in a cave", "Your words were sealed with seven seals until the end of time"],
        "answer": "Your words were found and I ate them, and Your word became the gladness and joy of my heart",
        "verse_ref": "Jer. 15:16",
        "explanation": "Jeremiah 15:16: 'Your words were found and I ate them, and Your word became to me the gladness and joy of my heart; for I am called by Your name, O Jehovah, God of hosts.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Ezekiel & River",
        "question": "In Ezekiel 47:3-5, as the man measured four distances of a thousand cubits into the river issuing from the house of God, what were the four depths of water?",
        "options": ["To the ankles, to the knees, to the loins, and waters to swim in", "To the soles, to the waist, to the neck, and over the head", "To the sandals, to the shoulders, to the crown, and a great flood", "To the stones, to the bushes, to the trees, and an ocean"],
        "answer": "To the ankles, to the knees, to the loins, and waters to swim in",
        "verse_ref": "Ezek. 47:3-5",
        "explanation": "Ezekiel 47:3-5 records the four stages of the river's depth: water to the ankles, water to the knees, water to the loins, and waters to swim in - a river that could not be passed over."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Zechariah & Spirit",
        "question": "What word of Jehovah was spoken to Zerubbabel regarding the rebuilding of the temple and lampstand in Zechariah 4:6?",
        "options": ["Not by might nor by power, but by My Spirit, says Jehovah of hosts", "By the strength of legions of chariots and horses", "By the wisdom and philosophies of the nations", "By abundant treasuries of silver and gold"],
        "answer": "Not by might nor by power, but by My Spirit, says Jehovah of hosts",
        "verse_ref": "Zech. 4:6",
        "explanation": "Zechariah 4:6: 'This is the word of Jehovah to Zerubbabel, saying, Not by might nor by power, but by My Spirit, says Jehovah of hosts.'"
    },

    # =========================================================================
    # NEW TESTAMENT - RECOVERY TRUTHS & SCRIPTURES
    # =========================================================================
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Incarnation",
        "question": "According to John 1:14, what did the eternal Word become, and what did He do among us?",
        "options": ["The Word became flesh and tabernacled among us, full of grace and reality", "The Word became an angel and delivered heavenly laws", "The Word remained in heaven and spoke through prophets", "The Word became a philosophy taught in academies"],
        "answer": "The Word became flesh and tabernacled among us, full of grace and reality",
        "verse_ref": "John 1:14",
        "explanation": "John 1:14: 'And the Word became flesh and tabernacled among us (and we beheld His glory, glory as of the only Begotten from the Father), full of grace and reality.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Regeneration",
        "question": "In John 3:6, how did the Lord Jesus describe the two distinct spirits in the mystery of regeneration?",
        "options": ["That which is born of the flesh is flesh, and that which is born of the Spirit is spirit", "The mind is educated and the emotions are purified", "The physical body is rejuvenated by divine power", "The soul becomes an angelic spirit after baptism"],
        "answer": "That which is born of the flesh is flesh, and that which is born of the Spirit is spirit",
        "verse_ref": "John 3:6",
        "explanation": "John 3:6 distinguishes the divine Spirit (capital S) from the human spirit (lowercase s): 'That which is born of the flesh is flesh, and that which is born of the Spirit is spirit.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Worship",
        "question": "According to John 4:24, what is God in His nature, and how must those who worship Him worship?",
        "options": ["God is Spirit, and those who worship Him must worship in spirit and truthfulness", "God is light, and worshippers must travel to Jerusalem on feast days", "God is a sovereign judge, and worshippers must recite formal creeds", "God is a consuming fire, and worshippers must burn animal sacrifices"],
        "answer": "God is Spirit, and those who worship Him must worship in spirit and truthfulness",
        "verse_ref": "John 4:24",
        "explanation": "John 4:24 reveals: 'God is Spirit, and those who worship Him must worship in spirit and truthfulness.' True worship is touching God the Spirit with the human spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Living Bread",
        "question": "In John 6:57, what did the Lord Jesus say would happen to the person who eats Him?",
        "options": ["He who eats Me, he also shall live because of Me", "He shall never require physical meals again", "He shall be crowned with earthly authority", "He shall be granted angelic visions daily"],
        "answer": "He who eats Me, he also shall live because of Me",
        "verse_ref": "John 6:57",
        "explanation": "John 6:57: 'As the living Father has sent Me and I live because of the Father, so he who eats Me, he also shall live because of Me.' Eating Christ as food is the way to live Him."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Spirit and Life",
        "question": "In John 6:63, what did the Lord Jesus declare gives life, and what are the words He has spoken?",
        "options": ["It is the Spirit who gives life; the flesh profits nothing; the words which I have spoken to you are spirit and are life", "It is the law that gives life through strict observance of rituals", "It is moral discipline that imparts divine righteousness", "Outward ceremonies cleanse the inward heart"],
        "answer": "It is the Spirit who gives life; the flesh profits nothing; the words which I have spoken to you are spirit and are life",
        "verse_ref": "John 6:63",
        "explanation": "John 6:63: 'It is the Spirit who gives life; the flesh profits nothing; the words which I have spoken to you are spirit and are life.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Living Water",
        "question": "In John 7:38-39, what did the Lord Jesus promise would flow out of the innermost being of him who believes into Him?",
        "options": ["Rivers of living water", "Fountains of fragrant oil", "Beams of heavenly lightning", "Streams of golden incense"],
        "answer": "Rivers of living water",
        "verse_ref": "John 7:38-39",
        "explanation": "John 7:38-39: 'He who believes into Me, as the Scripture said, out of his innermost being shall flow rivers of living water. But this He said concerning the Spirit...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Life Release",
        "question": "In John 12:24, what agricultural picture did Jesus use to describe His death and resurrection releasing divine life to produce many sons of God?",
        "options": ["A grain of wheat falling into the ground and dying to bear much fruit", "A mustard seed growing into a large garden tree", "A tender shoot sprouting from an olive root", "A fig branch putting forth early figs"],
        "answer": "A grain of wheat falling into the ground and dying to bear much fruit",
        "verse_ref": "John 12:24",
        "explanation": "John 12:24: 'Truly, truly, I say to you, Unless the grain of wheat falls into the ground and dies, it abides alone; but if it dies, it bears much fruit.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & The Vine",
        "question": "In John 15:5, how did Jesus describe the organic union and relationship between Himself and the believers?",
        "options": ["I am the vine; you are the branches. He who abides in Me and I in him, he bears much fruit", "I am the potter; you are the inert clay vessels", "I am the general; you are soldiers who follow orders", "I am the teacher; you are students in a lecture hall"],
        "answer": "I am the vine; you are the branches. He who abides in Me and I in him, he bears much fruit",
        "verse_ref": "John 15:5",
        "explanation": "John 15:5: 'I am the vine; you are the branches. He who abides in Me and I in him, he bears much fruit; for apart from Me you can do nothing.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Holy Breath",
        "question": "On the evening of His resurrection day (John 20:22), what did the Lord Jesus do into His disciples?",
        "options": ["He breathed into them and said, Receive the Holy Spirit", "He poured fragrant olive oil upon their heads", "He washed their feet with water in a basin", "He laid hands on them and appointed elders"],
        "answer": "He breathed into them and said, Receive the Holy Spirit",
        "verse_ref": "John 20:22",
        "explanation": "John 20:22 records the essential Spirit imparted into the disciples as holy breath: 'And when He had said this, He breathed into them and said to them, Receive the Holy Spirit.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Calling",
        "question": "In the book of Acts (Acts 9:14), what distinct practice was used to identify all Christians so that Saul of Tarsus had authority to bind them?",
        "options": ["All who call upon Your name", "All who wear white linen vestments", "All who speak Hebrew in the marketplace", "All who carry parchment scrolls"],
        "answer": "All who call upon Your name",
        "verse_ref": "Acts 9:14",
        "explanation": "Acts 9:14: 'And here he has authority from the chief priests to bind all who call upon Your name.' Calling on the name of the Lord was the audible hallmark of the early church."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Acts & Church Life",
        "question": "In Acts 2:42, in which four things did the early believers in Jerusalem continue steadfastly? (Select all 4)",
        "options": ["The teaching of the apostles", "The fellowship", "The breaking of bread", "The prayers", "The building of stone cathedrals", "The observing of Jewish Sabbath laws"],
        "answer": ["The teaching of the apostles", "The fellowship", "The breaking of bread", "The prayers"],
        "verse_ref": "Acts 2:42",
        "explanation": "Acts 2:42: 'And they continued steadfastly in the teaching and the fellowship of the apostles, in the breaking of bread and the prayers' - the fourfold practice of the church life."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Romans & Organic Salvation",
        "question": "In Romans 5:10, Paul reasons that if while being enemies we were reconciled to God through the death of His Son, much more we shall be what?",
        "options": ["Saved in His life", "Given immediate exemption from physical problems", "Transformed into disembodied angels", "Elevated to rule nations in this age"],
        "answer": "Saved in His life",
        "verse_ref": "Rom. 5:10",
        "explanation": "Romans 5:10 contrasts judicial redemption with organic salvation: 'much more we will be saved in His life, having been reconciled.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Romans & Spirit of Life",
        "question": "According to Romans 8:2, what has freed believers in Christ Jesus from the law of sin and of death?",
        "options": ["The law of the Spirit of life", "The Ten Commandments given to Moses", "Human willpower and strict self-control", "The traditions of the church fathers"],
        "answer": "The law of the Spirit of life",
        "verse_ref": "Rom. 8:2",
        "explanation": "Romans 8:2: 'For the law of the Spirit of life has freed me in Christ Jesus from the law of sin and of death.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Romans & The Mind",
        "question": "Romans 8:6 contrasts two states: 'The mind set on the flesh is death, but the mind set on the spirit is...' what?",
        "options": ["Life and peace", "Knowledge and influence", "Righteousness and wealth", "Glory and power"],
        "answer": "Life and peace",
        "verse_ref": "Rom. 8:6",
        "explanation": "Romans 8:6 reveals the key to daily Christian living: 'For the mind set on the flesh is death, but the mind set on the spirit is life and peace.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Romans & Mingled Spirit",
        "question": "According to Romans 8:16, who witnesses with our human spirit that we are children of God?",
        "options": ["The Spirit Himself", "The church leadership", "Our changing emotional feelings", "The guardian angels"],
        "answer": "The Spirit Himself",
        "verse_ref": "Rom. 8:16",
        "explanation": "Romans 8:16 demonstrates the two spirits witnessing together: 'The Spirit Himself witnesses with our spirit that we are children of God.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Romans & Rich Lord",
        "question": "According to Romans 10:12, how is the Lord Jesus toward all who call upon Him?",
        "options": ["The same Lord is Lord of all and rich to all who call upon Him", "He is distant and answers only high priests", "He requires elaborate rituals before drawing near", "He favors one particular nationality over others"],
        "answer": "The same Lord is Lord of all and rich to all who call upon Him",
        "verse_ref": "Rom. 10:12",
        "explanation": "Romans 10:12: 'For there is no distinction between Jew and Greek, for the same Lord is Lord of all and rich to all who call upon Him.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Corinthians & One Spirit",
        "question": "In 1 Corinthians 6:17, what foundational declaration does Paul make regarding the believer's organic union with the Lord?",
        "options": ["He who is joined to the Lord is one spirit", "He who is joined to the Lord is free from all physical sickness", "He who is joined to the Lord memorizes all biblical languages", "He who is joined to the Lord receives an earthly title"],
        "answer": "He who is joined to the Lord is one spirit",
        "verse_ref": "1 Cor. 6:17",
        "explanation": "1 Corinthians 6:17: 'But he who is joined to the Lord is one spirit' - revealing the deep truth of the mingled spirit, the divine Spirit mingled with our regenerated human spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Corinthians & Body and Spirit",
        "question": "According to 1 Corinthians 12:13, in what were we all baptized into one Body, and what were we all given to drink?",
        "options": ["In one Spirit were we all baptized into one Body, and were all given to drink one Spirit", "In water we were initiated, and given to drink wine with the elders", "In doctrine we were organized, and given to drink philosophical wisdom", "In religious laws we were disciplined, and given to drink solemn oaths"],
        "answer": "In one Spirit were we all baptized into one Body, and were all given to drink one Spirit",
        "verse_ref": "1 Cor. 12:13",
        "explanation": "1 Corinthians 12:13: 'For also in one Spirit we were all baptized into one Body... and were all given to drink one Spirit.' We are baptized outwardly into the Body and drink inwardly of the one Spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Corinthians & Life-Giving Spirit",
        "question": "In 1 Corinthians 15:45, what did the last Adam (Christ in resurrection) become?",
        "options": ["A life-giving Spirit", "A living soul", "An archangel in heaven", "A reigning political ruler"],
        "answer": "A life-giving Spirit",
        "verse_ref": "1 Cor. 15:45",
        "explanation": "1 Corinthians 15:45: 'So also it is written, \"The first man, Adam, became a living soul\"; the last Adam became a life-giving Spirit.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Corinthians & Transformation",
        "question": "According to 2 Corinthians 3:17-18, who is the Lord today, and what happens to believers who behold Him with unveiled face?",
        "options": ["The Lord is the Spirit, and we are being transformed into the same image from glory to glory", "The Lord is far off in heaven, and we wait passively without change", "The Lord is a historic figure, and we memorize His biography", "The Lord is a stern judge, and we tremble in fear of condemnation"],
        "answer": "The Lord is the Spirit, and we are being transformed into the same image from glory to glory",
        "verse_ref": "2 Cor. 3:17-18",
        "explanation": "2 Corinthians 3:17-18: 'Now the Lord is the Spirit... we all with unveiled face, beholding and reflecting like a mirror the glory of the Lord, are being transformed into the same image from glory to glory, even as from the Lord Spirit.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Corinthians & Earthen Vessels",
        "question": "In 2 Corinthians 4:7, where does Paul say believers have the marvelous treasure of the indwelling Christ?",
        "options": ["In earthen vessels, that the excellency of the power may be of God and not out of us", "In golden urns kept in the temple sanctuary", "In parchment scrolls preserved in jars of clay", "In heavenly storehouses beyond human reach"],
        "answer": "In earthen vessels, that the excellency of the power may be of God and not out of us",
        "verse_ref": "2 Cor. 4:7",
        "explanation": "2 Corinthians 4:7: 'But we have this treasure in earthen vessels that the excellency of the power may be of God and not out of us.' We are the earthen containers; Christ is the priceless treasure within."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Corinthians & Triune God Benediction",
        "question": "How does the benediction of 2 Corinthians 13:14 present the flow and transmission of the Triune God into believers?",
        "options": ["The grace of the Lord Jesus Christ and the love of God and the fellowship of the Holy Spirit be with you all", "The power of the Father, the wisdom of the Son, and the majesty of heaven be with you", "The peace of Jerusalem, the blessings of Aaron, and the law of Moses be with you", "The righteous judgment of God and the fear of the Lord be upon all assemblies"],
        "answer": "The grace of the Lord Jesus Christ and the love of God and the fellowship of the Holy Spirit be with you all",
        "verse_ref": "2 Cor. 13:14",
        "explanation": "2 Corinthians 13:14: 'The grace of the Lord Jesus Christ and the love of God and the fellowship of the Holy Spirit be with you all' - love is the source, grace the course, and fellowship the impartation."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Galatians & Christ Lives in Me",
        "question": "In Galatians 2:20, Paul declares: 'I am crucified with Christ; and it is no longer I who live, but...' who lives in me?",
        "options": ["It is Christ who lives in me", "It is the law that lives in me", "It is moral virtue that lives in me", "It is religious zeal that lives in me"],
        "answer": "It is Christ who lives in me",
        "verse_ref": "Gal. 2:20",
        "explanation": "Galatians 2:20: 'I am crucified with Christ; and it is no longer I who live, but it is Christ who lives in me; and the life which I now live in the flesh I live in faith, the faith of the Son of God...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & The Body",
        "question": "According to Ephesians 1:22-23, what is the church in relation to Christ who has been given to be Head over all things?",
        "options": ["His Body, the fullness of the One who fills all in all", "A voluntary association of religious clubs", "A charitable institution caring for civic needs", "A school of theology teaching sacred languages"],
        "answer": "His Body, the fullness of the One who fills all in all",
        "verse_ref": "Eph. 1:22-23",
        "explanation": "Ephesians 1:22-23: 'And He subjected all things under His feet and gave Him to be Head over all things to the church, which is His Body, the fullness of the One who fills all in all.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & One New Man",
        "question": "In Ephesians 2:15, what did Christ create in Himself of Jewish and Gentile believers by abolishing the law of commandments in ordinances?",
        "options": ["One new man, so making peace", "Two friendly denominations coexisting in harmony", "A federated league of distinct cultural traditions", "A renewed Aaronic priesthood with twelve orders"],
        "answer": "One new man, so making peace",
        "verse_ref": "Eph. 2:15",
        "explanation": "Ephesians 2:15: 'Abolishing in His flesh the enmity, the law of commandments in ordinances, that He might create the two in Himself into one new man, so making peace.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & Inner Man",
        "question": "In Paul's prayer in Ephesians 3:16-17, what does he petition that the Father would grant the believers through His Spirit?",
        "options": ["To be strengthened with power through His Spirit into the inner man, that Christ may make His home in your hearts through faith", "To be endowed with worldly honor, financial riches, and health", "To receive visions of angels visiting their gatherings", "To be exempted from persecution by the Roman empire"],
        "answer": "To be strengthened with power through His Spirit into the inner man, that Christ may make His home in your hearts through faith",
        "verse_ref": "Eph. 3:16-17",
        "explanation": "Ephesians 3:16-17: 'To be strengthened with power through His Spirit into the inner man, that Christ may make His home in your hearts through faith...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Philippians & Bountiful Supply",
        "question": "In Philippians 1:19, Paul was assured that his trials would turn out to salvation through the petition of the saints and what?",
        "options": ["The bountiful supply of the Spirit of Jesus Christ", "An emergency pardon signed by the Roman emperor", "His personal oratorical brilliance in the forum", "An earthquake opening the prison doors"],
        "answer": "The bountiful supply of the Spirit of Jesus Christ",
        "verse_ref": "Phil. 1:19",
        "explanation": "Philippians 1:19: 'For I know that for me this will turn out to salvation through your petition and the bountiful supply of the Spirit of Jesus Christ.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Colossians & The Mystery",
        "question": "In Colossians 1:27, what is revealed as the riches of the glory of the divine mystery among the Gentiles?",
        "options": ["Christ in you, the hope of glory", "A hidden philosophical system of ethics", "A calendar of prophetic end-time dates", "A restored earthly kingdom based in Jerusalem"],
        "answer": "Christ in you, the hope of glory",
        "verse_ref": "Col. 1:27",
        "explanation": "Colossians 1:27: 'To whom God willed to make known what are the riches of the glory of this mystery among the Gentiles, which is Christ in you, the hope of glory.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Colossians & New Man",
        "question": "According to Colossians 3:10-11, in the new man who is being renewed unto full knowledge, what is the ultimate reality?",
        "options": ["There cannot be Greek and Jew, circumcision and uncircumcision, barbarian, Scythian, slave, free man, but Christ is all and in all", "Every racial and national group maintains separate assemblies", "The clergy hold spiritual authority above ordinary members", "Only those circumcised in the flesh possess leadership"],
        "answer": "There cannot be Greek and Jew, circumcision and uncircumcision, barbarian, Scythian, slave, free man, but Christ is all and in all",
        "verse_ref": "Col. 3:10-11",
        "explanation": "Colossians 3:11: 'Where there cannot be Greek and Jew, circumcision and uncircumcision, barbarian, Scythian, slave, free man, but Christ is all and in all.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Thessalonians & Tripartite Man",
        "question": "In 1 Thessalonians 5:23, Paul prays that the God of peace would sanctify the believers wholly, preserving what three parts of their being complete?",
        "options": ["Your whole spirit and soul and body", "Your mind and emotion and will", "Your words and thoughts and actions", "Your church and family and community"],
        "answer": "Your whole spirit and soul and body",
        "verse_ref": "1 Thes. 5:23",
        "explanation": "1 Thessalonians 5:23 clearly shows man's three parts: 'And may your spirit and soul and body be preserved complete, without blame at the coming of our Lord Jesus Christ.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Hebrews & Soul and Spirit",
        "question": "According to Hebrews 4:12, why is the living and operative word of God sharper than any two-edged sword?",
        "options": ["It pierces to the dividing of soul and spirit and of joints and marrow, discerning the thoughts and intentions of the heart", "It strikes down enemies of the church in physical combat", "It provides intellectual ammunition to defeat debate opponents", "It dictates political laws to govern civic magistrates"],
        "answer": "It pierces to the dividing of soul and spirit and of joints and marrow, discerning the thoughts and intentions of the heart",
        "verse_ref": "Heb. 4:12",
        "explanation": "Hebrews 4:12: 'For the word of God is living and operative and sharper than any two-edged sword, and piercing even to the dividing of soul and spirit and of joints and marrow...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Hebrews & Throne of Grace",
        "question": "According to Hebrews 4:16, why are believers encouraged to come forward with boldness to the throne of grace in their spirit?",
        "options": ["That we may receive mercy and find grace for timely help", "That we may admire the golden cherubim from afar", "That we may petition for material earthly riches", "That we may escape all earthly responsibilities"],
        "answer": "That we may receive mercy and find grace for timely help",
        "verse_ref": "Heb. 4:16",
        "explanation": "Hebrews 4:16: 'Let us therefore come forward with boldness to the throne of grace that we may receive mercy and find grace for timely help.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & Lampstands",
        "question": "In Revelation 1:20, what is revealed to be the mystery of the seven golden lampstands seen by the Apostle John?",
        "options": ["The seven churches in seven cities of Asia Minor", "Seven archangels stationed at heaven's gates", "Seven spiritual virtues in the believer's heart", "Seven successive dispensations of human history"],
        "answer": "The seven churches in seven cities of Asia Minor",
        "verse_ref": "Rev. 1:20",
        "explanation": "Revelation 1:20: 'The seven lampstands are the seven churches' - showing the local churches as golden lampstands shining with the divine light in this dark age."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Revelation & Seven Spirits",
        "question": "In the book of Revelation, the sevenfold intensified Spirit of God is described under which of the following symbols? (Select all that apply)",
        "options": ["The seven Spirits who are before His throne", "Seven lamps of fire burning before the throne", "Seven eyes of the Lamb sent forth into all the earth", "Seven silver cups overflowing with wine", "Seven bronze crowns placed upon the elders"],
        "answer": ["The seven Spirits who are before His throne", "Seven lamps of fire burning before the throne", "Seven eyes of the Lamb sent forth into all the earth"],
        "verse_ref": "Rev. 4:5",
        "explanation": "Revelation portrays the sevenfold intensified Spirit as the seven Spirits before the throne (1:4), seven burning lamps of fire (4:5), and seven eyes of the Lamb (5:6)."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & New Jerusalem Bride",
        "question": "In Revelation 21:2 and 9-10, the holy city, New Jerusalem, coming down out of heaven from God, is declared by the angel to be what?",
        "options": ["The bride, the wife of the Lamb", "A literal physical mansion made of concrete and marble", "A golden planet floating in the solar system", "A private palace built for ancient patriarchs only"],
        "answer": "The bride, the wife of the Lamb",
        "verse_ref": "Rev. 21:2",
        "explanation": "Revelation 21:2 and 9-10 reveal the New Jerusalem is not a physical city, but the consummate corporate person: 'the bride, the wife of the Lamb,' prepared as a bride adorned for her husband."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & River and Tree of Life",
        "question": "In Revelation 22:1-2, what proceeds out of the throne of God and of the Lamb down the middle of the street of the New Jerusalem?",
        "options": ["A river of water of life, bright as crystal, and on both sides the tree of life", "A river of burning sulphur and the tree of knowledge", "A wide highway of gold flanked by statues of prophets", "A stone canal surrounded by dry desert sand"],
        "answer": "A river of water of life, bright as crystal, and on both sides the tree of life",
        "verse_ref": "Rev. 22:1-2",
        "explanation": "Revelation 22:1-2: 'And he showed me a river of water of life, bright as crystal, proceeding out of the throne of God and of the Lamb in the middle of its street. And on this side and on that side of the river was the tree of life...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & The Final Call",
        "question": "In the concluding chapter of the Bible (Revelation 22:17), who speaks together in complete oneness to invite anyone who is thirsty to take the water of life freely?",
        "options": ["The Spirit and the bride", "The cherubim and seraphim", "Moses and Elijah", "The kings and governors of the earth"],
        "answer": "The Spirit and the bride",
        "verse_ref": "Rev. 22:17",
        "explanation": "Revelation 22:17: 'And the Spirit and the bride say, Come! And let him who hears say, Come! And let him who is thirsty come; let him who wills take the water of life freely.'"
    },

    # =========================================================================
    # SLIDER QUESTIONS (Numerical Estimation - New Jerusalem Dimensions & Canon)
    # =========================================================================
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Revelation & Holy City",
        "question": "According to Revelation 21:12-13, how many total pearl gates does the wall of the New Jerusalem have (three on the east, three on the north, three on the south, and three on the west)?",
        "min": 4,
        "max": 24,
        "step": 1,
        "unit": "gates",
        "answer": 12,
        "verse_ref": "Rev. 21:12-13",
        "explanation": "Revelation 21:12-13 describes twelve gates of the holy city, each gate being one pearl, with three gates facing each of the four directions."
    },
    {
        "type": "slider",
        "testament": "New Testament",
        "category": "Revelation & Foundations",
        "question": "According to Revelation 21:14, how many foundations adorned with precious stones does the wall of the New Jerusalem have, bearing the names of the twelve apostles of the Lamb?",
        "min": 4,
        "max": 24,
        "step": 1,
        "unit": "foundations",
        "answer": 12,
        "verse_ref": "Rev. 21:14",
        "explanation": "Revelation 21:14 records: 'And the wall of the city had twelve foundations, and on them the twelve names of the twelve apostles of the Lamb.'"
    },
    # =========================================================================
    # WAVE 2: OLD TESTAMENT - RECOVERY TRUTHS & TYPES
    # =========================================================================
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Image",
        "question": "In Genesis 1:26-27, for what dual purpose did God create man in His image and according to His likeness?",
        "options": ["To express God with His image and represent Him with dominion over the earth", "To cultivate the soil and build earthly empires", "To serve angels as lesser celestial beings", "To offer physical animal sacrifices in a temple"],
        "answer": "To express God with His image and represent Him with dominion over the earth",
        "verse_ref": "Gen. 1:26-27",
        "explanation": "Genesis 1:26 reveals God's eternal purpose: man was made in God's image to be His corporate expression, and given dominion over all creation to represent His authority."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Human Spirit",
        "question": "According to Genesis 2:7, what did Jehovah God breathe into man's nostrils that formed the human spirit?",
        "options": ["The breath of life", "A measure of golden dust", "An angelic soul", "The dew of heaven"],
        "answer": "The breath of life",
        "verse_ref": "Gen. 2:7",
        "explanation": "Genesis 2:7: 'Jehovah God formed man from the dust of the ground and breathed into his nostrils the breath of life, and man became a living soul.' Proverbs 20:27 confirms: 'The spirit of man is the lamp of Jehovah.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Eve",
        "question": "In Genesis 2:21-23, how was Eve produced to be Adam's matching counterpart, typifying the church coming out of Christ's resurrection?",
        "options": ["Built from a rib taken out of Adam while in a deep sleep", "Formed separately from the red clay of the field", "Created by angelic decree in heaven", "Adopted from another tribe of living creatures"],
        "answer": "Built from a rib taken out of Adam while in a deep sleep",
        "verse_ref": "Gen. 2:21-23",
        "explanation": "Genesis 2:22: 'And Jehovah God built the rib, which He had taken from the man, into a woman and brought her to the man.' Eve typifies the church built purely out of Christ's resurrection life."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Melchizedek",
        "question": "When Melchizedek king of Salem met Abraham returning from the slaughter of the kings (Genesis 14:18), what did he bring out to minister to him?",
        "options": ["Bread and wine", "Gold and frankincense", "Roasted lamb and bitter herbs", "Fine linen and purple dye"],
        "answer": "Bread and wine",
        "verse_ref": "Gen. 14:18",
        "explanation": "Genesis 14:18 records: 'And Melchizedek the king of Salem brought out bread and wine; now he was priest of God the Most High,' prefiguring Christ ministering Himself as food and drink."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Isaac's Bride",
        "question": "In Genesis 24, whom did Abraham charge his oldest servant to take as a wife for his son Isaac, typifying the Holy Spirit securing the church as Christ's bride?",
        "options": ["A wife from his own country and relatives, Rebekah", "A daughter of the Canaanites living nearby", "An Egyptian princess from Pharaoh's court", "A maiden chosen by the elders of Salem"],
        "answer": "A wife from his own country and relatives, Rebekah",
        "verse_ref": "Gen. 24:2-4",
        "explanation": "Genesis 24 shows a complete type of the Divine Trinity: the Father sending the Holy Spirit to the world to find and betroth the church (Rebekah) as the bride for the Son (Isaac)."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Genesis & Transformation",
        "question": "At Peniel, when God touched the hollow of Jacob's thigh, what new name did He give him, changing him from a supplanter to a prince of God?",
        "options": ["Israel", "Abraham", "Ephraim", "Joshua"],
        "answer": "Israel",
        "verse_ref": "Gen. 32:28",
        "explanation": "Genesis 32:28: 'Your name shall no longer be called Jacob, but Israel; for you have striven with God and with men and have prevailed.' Jacob was transformed into Israel, a prince of God."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Exodus & Passover",
        "question": "According to Exodus 12:7-8, what two things were the children of Israel commanded to do with the Passover lamb on the night of redemption? (Select both)",
        "options": ["Put some of the blood on the two doorposts and on the lintel of the houses", "Eat the flesh roasted with fire, with unleavened bread and bitter herbs", "Bury the bones in the desert outside the camp", "Boil the meat in milk on an open hearth"],
        "answer": ["Put some of the blood on the two doorposts and on the lintel of the houses", "Eat the flesh roasted with fire, with unleavened bread and bitter herbs"],
        "verse_ref": "Exo. 12:7-8",
        "explanation": "Exodus 12:7-8 reveals both judicial redemption (blood on the doorposts for God to pass over) and organic life supply (eating the roasted lamb with unleavened bread and bitter herbs inside)."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Exodus & Manna",
        "question": "In Exodus 16:14 and 31, how is the miraculous wilderness manna described in appearance and taste?",
        "options": ["Like coriander seed, white, and its taste was like wafers made with honey", "Like golden grain, round, and its taste was like salted bread", "Like sweet grapes, purple, and its taste was like fresh wine", "Like crushed olives, green, and its taste was like bitter oil"],
        "answer": "Like coriander seed, white, and its taste was like wafers made with honey",
        "verse_ref": "Exo. 16:14, 31",
        "explanation": "Exodus 16:31: 'It was like coriander seed, white; and its taste was like wafers made with honey.' Manna is a type of Christ as our daily heavenly life supply."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Exodus & Priesthood",
        "question": "In Exodus 21:5-6, if a Hebrew slave plainly said, 'I love my master, my wife, and my children; I will not go out free,' how was he consecrated for lifelong service?",
        "options": ["His master brought him to the doorpost and pierced his ear through with an awl", "He was given a golden ring and a new tunic", "He offered two turtle doves on the bronze altar", "He swore a solemn oath before the twelve judges"],
        "answer": "His master brought him to the doorpost and pierced his ear through with an awl",
        "verse_ref": "Exo. 21:5-6",
        "explanation": "Exodus 21:5-6 typifies Christ as the willing, loving slave of God and the church, whose ear was bored at the doorpost to serve God forever in love."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Exodus & Priesthood",
        "question": "According to Exodus 28:15 and 30, what items were placed in the high priest's breastplate of judgment to obtain divine illumination and decisions?",
        "options": ["Twelve precious stones bearing the names of the twelve tribes of Israel", "The Urim and the Thummim", "The two stone tablets of the Ten Commandments", "A golden vial filled with hidden manna"],
        "answer": ["Twelve precious stones bearing the names of the twelve tribes of Israel", "The Urim and the Thummim"],
        "verse_ref": "Exo. 28:15, 30",
        "explanation": "Exodus 28:15, 30 describes the breastplate of judgment with twelve inscribed precious stones, containing the Urim (lights) and Thummim (perfections) for discerning God's leading."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Leviticus & Burnt Offering",
        "question": "In Leviticus 1:3-4, what did the offerer do to the burnt offering before it was slain, signifying his identification with Christ who lived absolutely for God?",
        "options": ["Lay his hand upon the head of the burnt offering", "Wash its feet seven times in the bronze laver", "Sprinkle oil upon its horns in the courtyard", "Place a wreath of olive branches around its neck"],
        "answer": "Lay his hand upon the head of the burnt offering",
        "verse_ref": "Lev. 1:3-4",
        "explanation": "Leviticus 1:4: 'And he shall lay his hand upon the head of the burnt offering, and it will be accepted for him to make expiation for him.' Laying on of hands signifies organic union and identification."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Leviticus & Discernment",
        "question": "In Leviticus 11:2-3, what two characteristics had to be present for a four-footed animal to be deemed clean for eating by God's people? (Select both)",
        "options": ["Parting the hoof and dividing the hoof completely", "Chewing the cud", "Having white fleece or hide", "Living solely in green pastures"],
        "answer": ["Parting the hoof and dividing the hoof completely", "Chewing the cud"],
        "verse_ref": "Lev. 11:2-3",
        "explanation": "Leviticus 11:3: 'Whatever parts the hoof and divides the hoof completely, chewing the cud among the beasts, that you may eat.' Typifies discerning walk and receiving/ruminating on the Word."
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Leviticus & Cleansing",
        "question": "In Leviticus 14:14 and 17, when a cleansed leper was consecrated, upon which three parts of his body were the blood and then the oil applied? (Select all 3)",
        "options": ["The tip of his right ear", "The thumb of his right hand", "The big toe of his right foot", "The center of his forehead", "The palm of his left hand"],
        "answer": ["The tip of his right ear", "The thumb of his right hand", "The big toe of his right foot"],
        "verse_ref": "Lev. 14:14, 17",
        "explanation": "Leviticus 14:14, 17 records applying blood and oil to the right ear (hearing), right thumb (action/working), and right toe (walk/living), typifying complete cleansing and anointing by the Spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Leviticus & Feasts",
        "question": "According to Leviticus 23:10-11, on what day was the sheaf of the firstfruits of the harvest waved before Jehovah, prefiguring Christ's resurrection on Sunday?",
        "options": ["On the day after the Sabbath", "On the seventh day of the feast", "On the day of the new moon", "On the evening of the Passover sacrifice"],
        "answer": "On the day after the Sabbath",
        "verse_ref": "Lev. 23:10-11",
        "explanation": "Leviticus 23:11: 'On the day after the Sabbath the priest shall wave it.' The day after the Sabbath is the first day of the week (Sunday), the exact day of Christ's resurrection (1 Cor. 15:20)."
    },
    {
        "type": "slider",
        "testament": "Old Testament",
        "category": "Leviticus & Jubilee",
        "question": "According to Leviticus 25:10, every how many years did the Year of Jubilee take place, when liberty was proclaimed and everyone returned to his lost possession?",
        "min": 10,
        "max": 100,
        "step": 5,
        "unit": "years",
        "answer": 50,
        "verse_ref": "Lev. 25:10",
        "explanation": "Leviticus 25:10: 'And you shall sanctify the fiftieth year, and proclaim liberty throughout the land to all its inhabitants; it shall be a jubilee for you; and you shall return every man to his possession...'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Numbers & Blessing",
        "question": "In Numbers 6:24-26, how does the threefold priestly blessing express the divine dispensing of the Triune God?",
        "options": ["Jehovah bless you and keep you (Father); Jehovah make His face shine upon you (Son); Jehovah lift up His countenance upon you and give you peace (Spirit)", "May your herds multiply, your fields flourish, and your storehouses overflow", "May the priests intercede, the levites sing, and the elders govern", "May the sun rise in peace, the moon shine with light, and the stars guide your journey"],
        "answer": "Jehovah bless you and keep you (Father); Jehovah make His face shine upon you (Son); Jehovah lift up His countenance upon you and give you peace (Spirit)",
        "verse_ref": "Num. 6:24-26",
        "explanation": "Numbers 6:24-26 is the Old Testament parallel of 2 Cor. 13:14: the Father keeps and blesses, the Son shines in grace, and the Spirit lifts up His face to impart peace."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Numbers & The Rock",
        "question": "In Numbers 20:8, what was Moses commanded to do to the rock at Kadesh to bring forth water, rather than striking it again?",
        "options": ["Speak to the rock before their eyes", "Strike the rock twice with Aaron's rod", "Dig a trench beneath the rock with scepters", "Pour olive oil over the top of the rock"],
        "answer": "Speak to the rock before their eyes",
        "verse_ref": "Num. 20:8",
        "explanation": "Numbers 20:8: 'Take the rod... and speak to the rock before their eyes, and it will give forth its water.' Christ was struck once for all on the cross; now we only need to speak to Him in prayer!"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Numbers & Bronze Serpent",
        "question": "In Numbers 21:8-9, when fiery serpents bit the people, what did Moses put on a pole so that anyone who looked upon it lived?",
        "options": ["A bronze serpent", "A golden lampstand", "A silver trumpet", "A budding almond rod"],
        "answer": "A bronze serpent",
        "verse_ref": "Num. 21:8-9",
        "explanation": "Numbers 21:8-9 typifies Christ who had the likeness of the flesh of sin (bronze serpent) but was without sin (no poison), as revealed by Jesus in John 3:14."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Song of Songs & Pursuit",
        "question": "What is the opening cry of longing for personal, intimate affection in Song of Songs 1:2?",
        "options": ["Let him kiss me with the kisses of his mouth! For your love is better than wine", "Teach me the mysteries of the heavenly kingdom", "Give me victory over the chariots of Pharaoh", "Build me a palace of cedar and fir"],
        "answer": "Let him kiss me with the kisses of his mouth! For your love is better than wine",
        "verse_ref": "Song of Songs 1:2",
        "explanation": "Song of Songs 1:2 expresses the seeker's pursuit of Christ in personal, affectionate, private, and spiritual fellowship: 'Let him kiss me with the kisses of his mouth!'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Song of Songs & The Cross",
        "question": "In Song of Songs 2:14, where does the Beloved call His seeker to abide, typifying the believer hiding in the cleft of the crucified and resurrected Christ?",
        "options": ["In the clefts of the rock, in the secret places of the steep ascent", "In the banquet hall drinking sweet spiced wine", "On the city walls watching the desert horizon", "In the garden gathering myrrh with balsam"],
        "answer": "In the clefts of the rock, in the secret places of the steep ascent",
        "verse_ref": "Song of Songs 2:14",
        "explanation": "Song of Songs 2:14: 'O my dove, in the clefts of the rock, in the secret places of the steep ascent, let me see your countenance, let me hear your voice...'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Song of Songs & The Shulammite",
        "question": "In Song of Songs 6:13, what is the lover called, representing the counterpart who has become the reproduction and duplicate of Solomon?",
        "options": ["The Shulammite", "The Queen of Sheba", "The Daughter of Zion", "The Rose of Sharon"],
        "answer": "The Shulammite",
        "verse_ref": "Song of Songs 6:13",
        "explanation": "Song of Songs 6:13: 'Return, return, O Shulammite!' Shulammite is the feminine form of Solomon, signifying the church becoming the exact duplicate of Christ in life, nature, and expression."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Isaiah & Prophecy",
        "question": "In Isaiah 7:14, what sign did the Lord give concerning the Messiah's birth?",
        "options": ["The virgin shall conceive and bear a son, and shall call His name Immanuel", "A great light will flash over the temple in Jerusalem", "A golden crown will descend from heaven upon Bethlehem", "The river Jordan will cease flowing for three days"],
        "answer": "The virgin shall conceive and bear a son, and shall call His name Immanuel",
        "verse_ref": "Isa. 7:14",
        "explanation": "Isaiah 7:14: 'Therefore the Lord Himself will give you a sign: Behold, the virgin shall conceive and bear a son, and she will call His name Immanuel (God with us).'"
    },
    {
        "type": "multi_select",
        "testament": "Old Testament",
        "category": "Isaiah & The Divine Son",
        "question": "In Isaiah 9:6, which four divine titles are given to the child born and the Son given to us? (Select all 4)",
        "options": ["Wonderful Counselor", "Mighty God", "Eternal Father", "Prince of Peace", "Ancient of Days", "Lion of Judah"],
        "answer": ["Wonderful Counselor", "Mighty God", "Eternal Father", "Prince of Peace"],
        "verse_ref": "Isa. 9:6",
        "explanation": "Isaiah 9:6: 'And His name will be called Wonderful Counselor, Mighty God, Eternal Father, Prince of Peace' - proving that the Son who is born is also the Mighty God and the Eternal Father."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Isaiah & Waiting on God",
        "question": "According to Isaiah 40:31, what happens to those who wait upon Jehovah?",
        "options": ["They will renew their strength and mount up with wings like eagles", "They will inherit vast cities and earthly kingdoms", "They will receive angelic chariots to escape battle", "They will be exempted from physical aging"],
        "answer": "They will renew their strength and mount up with wings like eagles",
        "verse_ref": "Isa. 40:31",
        "explanation": "Isaiah 40:31: 'Yet those who wait on Jehovah will renew their strength; they will mount up with wings like eagles; they will run and not be weary; they will walk and not faint.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Isaiah & Vicarious Suffering",
        "question": "In Isaiah 53:5, how does the prophet describe the substitutionary death of the Suffering Servant?",
        "options": ["He was pierced for our transgressions, crushed for our iniquities; and by His stripes we are healed", "He was exiled to distant lands for the sins of the priests", "He fell in battle defending the holy sanctuary", "He was vindicated before the earthly kings without suffering"],
        "answer": "He was pierced for our transgressions, crushed for our iniquities; and by His stripes we are healed",
        "verse_ref": "Isa. 53:5",
        "explanation": "Isaiah 53:5: 'He was pierced for our transgressions; He was crushed for our iniquities; the chastening for our peace was upon Him, and by His stripes we are healed.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Isaiah & Free Waters",
        "question": "What is the gracious invitation extended in Isaiah 55:1 to everyone who is thirsty and has no money?",
        "options": ["Come to the waters, and buy wine and milk without money and without price", "Go labor in the royal vineyards until wages are earned", "Offer seven heifers at the bronze altar before drinking", "Travel across the Great Sea to the distant isles"],
        "answer": "Come to the waters, and buy wine and milk without money and without price",
        "verse_ref": "Isa. 55:1",
        "explanation": "Isaiah 55:1: 'Ho! Everyone who thirsts, come to the waters; and he who has no money, come, buy and eat; yes, come, buy wine and milk without money and without price.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Ezekiel & Four Living Creatures",
        "question": "In Ezekiel 1:10 and 26, what was the likeness of the One seated upon the throne above the crystal clear expanse?",
        "options": ["The likeness of a man", "A burning pillar of brass", "A crowned cherub with outstretched wings", "An unapproachable storm cloud with lightning"],
        "answer": "The likeness of a man",
        "verse_ref": "Ezek. 1:10, 26",
        "explanation": "Ezekiel 1:26: 'And above the expanse that was over their heads was the likeness of a throne... and upon the likeness of the throne was the likeness as the appearance of a man upon it above' - Christ on the throne in resurrection!"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Ezekiel & New Heart and Spirit",
        "question": "In Ezekiel 36:26, what did God promise to do for His people regarding their inner being?",
        "options": ["A new heart also will I give you, and a new spirit will I put within you", "I will teach your mind the complete law of Moses", "I will grant you prophetic visions of the end times", "I will send angels to guard your thoughts"],
        "answer": "A new heart also will I give you, and a new spirit will I put within you",
        "verse_ref": "Ezek. 36:26",
        "explanation": "Ezekiel 36:26: 'A new heart also will I give you, and a new spirit will I put within you; and I will take away the stony heart out of your flesh, and I will give you a heart of flesh.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Ezekiel & Dry Bones",
        "question": "In Ezekiel 37:9-10, when the prophet prophesied to the breath (Ruach / Spirit) to breathe into the slain in the valley of dry bones, what did they become?",
        "options": ["They lived and stood up upon their feet, an exceedingly great army", "They wept in sackcloth and ashes before the altar", "They returned to their tombs until the final resurrection", "They scattered into the four corners of the wilderness"],
        "answer": "They lived and stood up upon their feet, an exceedingly great army",
        "verse_ref": "Ezek. 37:9-10",
        "explanation": "Ezekiel 37:10: 'And the breath came into them, and they lived and stood up upon their feet, an exceedingly great army' - typifying the Spirit forming the Body of Christ."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Daniel & The Stone",
        "question": "In Daniel 2:34-35, what struck the great human image upon its feet of iron and clay and then became a great mountain that filled the whole earth?",
        "options": ["A stone cut out without hands", "A flaming meteorite from the heavens", "A golden chariot with lightning wheels", "A roaring lion out of the forest"],
        "answer": "A stone cut out without hands",
        "verse_ref": "Dan. 2:34-35",
        "explanation": "Daniel 2:34-35 portrays Christ as the stone cut out without hands who smites the totality of human government and becomes a kingdom filling the whole earth."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Micah & Bethlehem",
        "question": "According to Micah 5:2, where was the Ruler in Israel prophesied to come forth from, whose goings forth have been from of old, from the days of eternity?",
        "options": ["Bethlehem Ephrathah", "Jerusalem the holy city", "Nazareth of Galilee", "Hebron in Judah"],
        "answer": "Bethlehem Ephrathah",
        "verse_ref": "Micah 5:2",
        "explanation": "Micah 5:2: 'You, Bethlehem Ephrathah... out of you shall come forth to Me One who is to be Ruler in Israel, whose goings forth have been from of old, from the days of eternity.'"
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Haggai & The Temple",
        "question": "In Haggai 2:7, who was prophesied to come when God shakes all nations, filling His house with glory?",
        "options": ["The Desire of all nations", "The conqueror of Babylon", "The king of Persia with gold", "The high priest of the line of Aaron"],
        "answer": "The Desire of all nations",
        "verse_ref": "Hag. 2:7",
        "explanation": "Haggai 2:7: 'And I will shake all nations, and the Desire of all nations shall come; and I will fill this house with glory, says Jehovah of hosts.' Christ is the Desire of all nations."
    },
    {
        "type": "multiple_choice",
        "testament": "Old Testament",
        "category": "Malachi & Healing",
        "question": "According to Malachi 4:2, what will arise for those who fear Jehovah's name, with healing in His wings?",
        "options": ["The Sun of righteousness", "The star of Jacob", "The morning dew of Hermon", "The cloud of incense"],
        "answer": "The Sun of righteousness",
        "verse_ref": "Mal. 4:2",
        "explanation": "Malachi 4:2: 'But unto you who fear My name will the Sun of righteousness arise with healing in His wings; and you will go forth and leap like well-fed calves.'"
    },

    # =========================================================================
    # WAVE 2: NEW TESTAMENT - RECOVERY TRUTHS & SCRIPTURES
    # =========================================================================
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Gospels & Matthew",
        "question": "In Matthew 1:21 and 23, what two names were announced for the incarnated Son of God? (Select both)",
        "options": ["Jesus (for He will save His people from their sins)", "Immanuel (which is interpreted, God with us)", "Shiloh (the bringer of peace)", "Melchizedek (the eternal priest)"],
        "answer": ["Jesus (for He will save His people from their sins)", "Immanuel (which is interpreted, God with us)"],
        "verse_ref": "Matt. 1:21, 23",
        "explanation": "Matthew 1:21, 23 presents Jesus (Jehovah the Savior) who saves us from sin, and Immanuel (God with us) who abides with us forever."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & The Rock",
        "question": "In Matthew 16:18, upon what foundation did the Lord Jesus declare He would build His church?",
        "options": ["Upon this rock (the revelation of Christ, the Son of the living God)", "Upon the temple Mount in Jerusalem", "Upon the imperial authority of Rome", "Upon the Mosaic law of the covenant"],
        "answer": "Upon this rock (the revelation of Christ, the Son of the living God)",
        "verse_ref": "Matt. 16:18",
        "explanation": "Matthew 16:18: 'Upon this rock I will build My church, and the gates of Hades shall not prevail against it.' The rock is the revelation concerning Christ and the church."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Gathering",
        "question": "According to Matthew 18:20, where is the Lord Jesus present in the midst of His believers?",
        "options": ["Where two or three are gathered into My name", "Only in cathedrals consecrated by archbishops", "Only in historical holy sites in Galilee", "Only during annual Passover feasts"],
        "answer": "Where two or three are gathered into My name",
        "verse_ref": "Matt. 18:20",
        "explanation": "Matthew 18:20 reveals the simplicity and reality of the church meeting: 'For where two or three are gathered into My name, there am I in their midst.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & The Virgins",
        "question": "In the parable of the ten virgins (Matthew 25:3-4), what did the prudent virgins take in their vessels that the foolish did not?",
        "options": ["Oil in their vessels with their lamps", "Golden wicks for their lamps", "Parchment scrolls of the law", "Costly garments for the wedding feast"],
        "answer": "Oil in their vessels with their lamps",
        "verse_ref": "Matt. 25:3-4",
        "explanation": "Matthew 25:4: 'The prudent took oil in their vessels with their lamps.' The lamp is the human spirit (Prov. 20:27); the vessel is the soul transformed by extra supply of the Holy Spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospels & Baptism",
        "question": "In the Great Commission of Matthew 28:19, into what are disciples to be baptized?",
        "options": ["Into the name (singular) of the Father and of the Son and of the Holy Spirit", "Into the names of the twelve apostles", "Into the membership rolls of the local synagogue", "Into the water of Jordan only"],
        "answer": "Into the name (singular) of the Father and of the Son and of the Holy Spirit",
        "verse_ref": "Matt. 28:19",
        "explanation": "Matthew 28:19: 'baptizing them into the name of the Father and of the Son and of the Holy Spirit' - 'name' is singular, denoting the one Divine Trinity, an immersion into the Triune God Himself."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Gospels & Luke 15",
        "question": "In Luke 15, which three parables work together to reveal the love of the Father, Son, and Spirit in recovering lost sinners? (Select all 3)",
        "options": ["The shepherd seeking the one lost sheep", "The woman with a lighted lamp sweeping the house for the lost coin", "The compassionate father running to receive the prodigal son", "The good Samaritan pouring oil and wine on the traveler", "The merchant seeking fine pearls"],
        "answer": ["The shepherd seeking the one lost sheep", "The woman with a lighted lamp sweeping the house for the lost coin", "The compassionate father running to receive the prodigal son"],
        "verse_ref": "Luke 15:4, 8, 20",
        "explanation": "Luke 15 shows the Trinity saving man: the Son as the Shepherd finding the sheep, the Spirit as the woman enlightening within the heart, and the Father receiving the son back into His embrace."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & The Lamb",
        "question": "What did John the Baptist proclaim when he saw Jesus coming toward him in John 1:29?",
        "options": ["Behold, the Lamb of God who takes away the sin of the world!", "Behold, the mighty king who will overthrow Caesar!", "Behold, the high priest who will reform the temple!", "Behold, the judge who brings the fire of judgment!"],
        "answer": "Behold, the Lamb of God who takes away the sin of the world!",
        "verse_ref": "John 1:29",
        "explanation": "John 1:29: 'Behold, the Lamb of God who takes away the sin of the world!' - Christ as the unique, all-inclusive sacrifice fulfilling all Old Testament offerings."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Abundant Life",
        "question": "In John 10:10-11, what did the Good Shepherd state as His supreme purpose in coming to earth?",
        "options": ["I have come that they may have life and may have it abundantly", "I have come to establish a political party in Judea", "I have come to teach philosophical ethics to scholars", "I have come to enforce legal penalties upon transgressors"],
        "answer": "I have come that they may have life and may have it abundantly",
        "verse_ref": "John 10:10-11",
        "explanation": "John 10:10: 'The thief does not come, except to steal and kill and destroy; I have come that they may have life and may have it abundantly.' Life (zoe) is God's eternal divine life."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Way, Reality, Life",
        "question": "In John 14:6, how did the Lord Jesus identify Himself as the exclusive path to God the Father?",
        "options": ["I am the way and the reality and the life; no one comes to the Father except through Me", "I am a helpful teacher and an inspiring example among many", "I am one of several valid spiritual pathways to heaven", "I am a prophet pointing you to the law of Sinai"],
        "answer": "I am the way and the reality and the life; no one comes to the Father except through Me",
        "verse_ref": "John 14:6",
        "explanation": "John 14:6: 'Jesus said to him, I am the way and the reality and the life; no one comes to the Father except through Me.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Spirit of Reality",
        "question": "In John 14:16-17, what did Jesus promise the Father would send to abide with the believers forever?",
        "options": ["Another Comforter, the Spirit of reality, who abides with you and shall be in you", "A company of twelve archangels to protect the disciples", "A written code of church bylaws carved on cedar boards", "An earthly sanctuary in Jerusalem to house the apostles"],
        "answer": "Another Comforter, the Spirit of reality, who abides with you and shall be in you",
        "verse_ref": "John 14:16-17",
        "explanation": "John 14:16-17 reveals the Holy Spirit as the Spirit of reality, the transfiguration of Christ coming into the believers to dwell within them forever."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & In That Day",
        "question": "In John 14:20, what marvelous mutual dwelling and coinherence did Jesus say believers would know in the day of resurrection?",
        "options": ["In that day you will know that I am in My Father, and you in Me, and I in you", "In that day you will leave all physical earth behind forever", "In that day you will understand all astronomy and mathematics", "In that day the temple of Herod will be enlarged tenfold"],
        "answer": "In that day you will know that I am in My Father, and you in Me, and I in you",
        "verse_ref": "John 14:20",
        "explanation": "John 14:20 is the profound truth of coinherence: 'In that day you will know that I am in My Father, and you in Me, and I in you' - believers incorporated into the Triune God."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Gospel of John & Oneness",
        "question": "In His high priestly prayer in John 17:21, what did the Lord Jesus pray for all who believe into Him?",
        "options": ["That they all may be one; even as You, Father, are in Me and I in You, that they also may be in Us", "That they may build separate denominations according to doctrine", "That they may establish worldly political influence across nations", "That they may achieve physical prosperity and earthly titles"],
        "answer": "That they all may be one; even as You, Father, are in Me and I in You, that they also may be in Us",
        "verse_ref": "John 17:21",
        "explanation": "John 17:21 is the Lord's heartfelt prayer for the divine oneness: 'That they all may be one; even as You, Father, are in Me and I in You, that they also may be in Us...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Power to Witness",
        "question": "In Acts 1:8, what did the resurrected Lord declare the disciples would receive when the Holy Spirit came upon them?",
        "options": ["Power, and you shall be My witnesses both in Jerusalem and in all Judea and Samaria and unto the uttermost part of the earth", "A royal charter from Caesar granting them tax exemption", "Secret wisdom to decode political revolutions in Rome", "Immunity from physical fatigue and aging"],
        "answer": "Power, and you shall be My witnesses both in Jerusalem and in all Judea and Samaria and unto the uttermost part of the earth",
        "verse_ref": "Acts 1:8",
        "explanation": "Acts 1:8: 'But you shall receive power when the Holy Spirit comes upon you, and you shall be My witnesses... unto the uttermost part of the earth.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Acts & Ministering to the Lord",
        "question": "In Acts 13:2, what were the prophets and teachers in Antioch doing when the Holy Spirit said, 'Set apart for Me now Barnabas and Saul'?",
        "options": ["Ministering to the Lord and fasting", "Drafting an organizational constitution for the province", "Petitioning the Roman senate for legal protections", "Conducting business investments for the church treasury"],
        "answer": "Ministering to the Lord and fasting",
        "verse_ref": "Acts 13:2",
        "explanation": "Acts 13:2 shows the sweet reality of the church life: 'And as they were ministering to the Lord and fasting, the Holy Spirit said, Set apart for Me now Barnabas and Saul...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Romans & Justification by Faith",
        "question": "According to Romans 1:17, what is revealed in the gospel from faith to faith?",
        "options": ["The righteousness of God... 'the righteous shall have life and live by faith'", "The secret penalties of purgatory", "The requirements of Mosaic ceremonial washings", "The historical genealogy of the Roman emperors"],
        "answer": "The righteousness of God... 'the righteous shall have life and live by faith'",
        "verse_ref": "Rom. 1:17",
        "explanation": "Romans 1:17: 'For the righteousness of God is revealed in it to faith from faith, as it is written, \"But the righteous shall have life and live by faith.\"'"
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Romans & Consecration",
        "question": "In Romans 12:1-2, what two practical actions does Paul urge believers to take regarding their bodies and minds? (Select both)",
        "options": ["Present your bodies a living sacrifice, holy, well pleasing to God", "Do not be fashioned according to this age, but be transformed by the renewing of the mind", "Withdraw into mountain monasteries away from society", "Undergo physical circumcision according to the flesh"],
        "answer": ["Present your bodies a living sacrifice, holy, well pleasing to God", "Do not be fashioned according to this age, but be transformed by the renewing of the mind"],
        "verse_ref": "Rom. 12:1-2",
        "explanation": "Romans 12:1-2: Present your bodies a living sacrifice for the church life, and be transformed by the renewing of the mind so that you may prove the good, well-pleasing, and perfect will of God."
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "1 Corinthians & Wisdom",
        "question": "According to 1 Corinthians 1:30, Christ became wisdom to us from God in which three sequential aspects? (Select all 3)",
        "options": ["Righteousness (for our past)", "Sanctification (for our present)", "Redemption (for our future)", "Eloquence in philosophy", "Worldly political influence"],
        "answer": ["Righteousness (for our past)", "Sanctification (for our present)", "Redemption (for our future)"],
        "verse_ref": "1 Cor. 1:30",
        "explanation": "1 Corinthians 1:30: 'Christ Jesus, who became wisdom to us from God: both righteousness and sanctification and redemption' - meeting all the needs of our spirit, soul, and body."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Corinthians & God's Building",
        "question": "In 1 Corinthians 3:9, what two agricultural and architectural terms does Paul use to describe the church?",
        "options": ["God's cultivated land, God's building", "God's political state, God's military camp", "God's commercial market, God's merchant ship", "God's lecture academy, God's library"],
        "answer": "God's cultivated land, God's building",
        "verse_ref": "1 Cor. 3:9",
        "explanation": "1 Corinthians 3:9: 'For we are God's fellow workers; you are God's cultivated land, God's building' - we grow in life as God's farm to be built up with precious materials as God's house."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Corinthians & One Bread",
        "question": "In 1 Corinthians 10:17, what truth does the single loaf of bread on the Lord's table signify?",
        "options": ["Seeing that there is one bread, we who are many are one Body; for we all partake of the one bread", "The bread represents our personal individual piety alone", "The bread is a memorial of the Old Testament Passover feast only", "The bread confers magical physical healing upon consumption"],
        "answer": "Seeing that there is one bread, we who are many are one Body; for we all partake of the one bread",
        "verse_ref": "1 Cor. 10:17",
        "explanation": "1 Corinthians 10:17: 'Seeing that there is one bread, we who are many are one Body; for we all partake of the one bread' - the physical loaf on the table represents the mystical corporate Body of Christ."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Corinthians & Prophesying",
        "question": "According to 1 Corinthians 14:3-4, what is the supreme value of prophesying (speaking for God and speaking forth Christ) in church meetings?",
        "options": ["He who prophesies speaks to men building up, and he builds up the church", "He who prophesies predicts secret future world events", "He who prophesies shows off his eloquence over others", "He who prophesies proves he is an ordained clergyman"],
        "answer": "He who prophesies speaks to men building up, and he builds up the church",
        "verse_ref": "1 Cor. 14:3-4",
        "explanation": "1 Corinthians 14:3-4 reveals: 'He who prophesies speaks to men building up and encouragement and consolation... he who prophesies builds up the church.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Corinthians & New Creation",
        "question": "In 2 Corinthians 5:17, what is declared concerning anyone who is organically in Christ?",
        "options": ["He is a new creation: the old things have passed away; behold, they have become new", "He becomes an angelic spirit without physical body", "He receives automatic exemption from all life struggles", "He is restored to the physical garden of Eden"],
        "answer": "He is a new creation: the old things have passed away; behold, they have become new",
        "verse_ref": "2 Cor. 5:17",
        "explanation": "2 Corinthians 5:17: 'So then if anyone is in Christ, he is a new creation. The old things have passed away; behold, they have become new.' In Christ, we possess God's uncreated divine life."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Corinthians & Righteousness",
        "question": "In 2 Corinthians 5:21, what did God do with Christ who knew no sin, and for what purpose?",
        "options": ["Him who did not know sin He made sin on our behalf that we might become the righteousness of God in Him", "He exempted Him from the cross so He could establish an earthly reign", "He made Him an angelic archangel to supervise human affairs", "He sent Him to condemn sinners to immediate judgment"],
        "answer": "Him who did not know sin He made sin on our behalf that we might become the righteousness of God in Him",
        "verse_ref": "2 Cor. 5:21",
        "explanation": "2 Corinthians 5:21: 'Him who did not know sin He made sin on our behalf that we might become the righteousness of God in Him.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Galatians & Blessing of Abraham",
        "question": "In Galatians 3:14, what is the ultimate blessing of Abraham that has come to the Gentiles through faith in Christ Jesus?",
        "options": ["The promise of the Spirit", "Physical real estate in the Middle East", "Large herds of cattle and sheep", "Earthly political crowns"],
        "answer": "The promise of the Spirit",
        "verse_ref": "Gal. 3:14",
        "explanation": "Galatians 3:14: 'In order that the blessing of Abraham might come to the Gentiles in Christ Jesus, that we might receive the promise of the Spirit through faith.' The all-inclusive Spirit is the blessing of Abraham!"
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Galatians & Fruit of the Spirit",
        "question": "In Galatians 5:22-23, which of the following virtues are listed as the ninefold fruit of the Spirit? (Select all that apply)",
        "options": ["Love, joy, and peace", "Long-suffering, kindness, and goodness", "Faithfulness, meekness, and self-control", "Financial wealth and worldly fame", "Military conquest and political dominance"],
        "answer": ["Love, joy, and peace", "Long-suffering, kindness, and goodness", "Faithfulness, meekness, and self-control"],
        "verse_ref": "Gal. 5:22-23",
        "explanation": "Galatians 5:22-23: 'The fruit of the Spirit is love, joy, peace, long-suffering, kindness, goodness, faithfulness, meekness, self-control.' The fruit of the Spirit is Christ expressed through our walk by the Spirit."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & The Sevenfold Oneness",
        "question": "In Ephesians 4:4-6, what seven elements constitute the divine oneness of the Body of Christ?",
        "options": ["One Body, one Spirit, one hope, one Lord, one faith, one baptism, one God and Father", "Seven denominational councils, seven creeds, seven sacraments", "Seven earthly bishops, seven cathedrals, seven apostolic sees", "Seven holy days, seven fasts, seven canonical liturgies"],
        "answer": "One Body, one Spirit, one hope, one Lord, one faith, one baptism, one God and Father",
        "verse_ref": "Eph. 4:4-6",
        "explanation": "Ephesians 4:4-6 reveals the seven onenesses: one Body and one Spirit, one hope, one Lord, one faith, one baptism, one God and Father of all, who is over all and through all and in all."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & Gifts for Building",
        "question": "According to Ephesians 4:11-12, why did the ascended Christ give apostles, prophets, evangelists, and shepherds and teachers to the church?",
        "options": ["For the perfecting of the saints unto the work of the ministry, unto the building up of the Body of Christ", "To perform all the church's service while the saints remain passive spectators", "To establish bureaucratic clerical hierarchies over congregations", "To collect tithes for constructing elaborate monuments"],
        "answer": "For the perfecting of the saints unto the work of the ministry, unto the building up of the Body of Christ",
        "verse_ref": "Eph. 4:11-12",
        "explanation": "Ephesians 4:11-12 shows that the gifted persons do not replace the saints; they perfect every saint to do the work of the ministry, which is to build up the Body of Christ directly."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & Filled in Spirit",
        "question": "In Ephesians 5:18-19, instead of being drunk with wine, what are believers charged to be, and how is it expressed?",
        "options": ["Be filled in spirit, speaking to one another in psalms and hymns and spiritual songs", "Be silent in church gatherings with heads bowed", "Engage in solemn ascetic fasts in isolated desert cells", "Memorize rabbinic commentaries without singing"],
        "answer": "Be filled in spirit, speaking to one another in psalms and hymns and spiritual songs",
        "verse_ref": "Eph. 5:18-19",
        "explanation": "Ephesians 5:18-19: 'Do not be drunk with wine, in which is dissoluteness, but be filled in spirit, speaking to one another in psalms and hymns and spiritual songs, singing and psalming with your heart to the Lord.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & Cleansing the Church",
        "question": "In Ephesians 5:26, how does Christ sanctify and cleanse the church that He might present her to Himself a glorious church without spot or wrinkle?",
        "options": ["By the washing of the water in the word", "By the enforcement of ecclesiastical penances", "By ceremonial washings with physical hyssop", "By lengthy fasting in seclusion"],
        "answer": "By the washing of the water in the word",
        "verse_ref": "Eph. 5:26",
        "explanation": "Ephesians 5:26: 'That He might sanctify her, cleansing her by the washing of the water in the word.' The water here is the washing of the living word (rhema) of Christ."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Ephesians & Spiritual Warfare",
        "question": "In Ephesians 6:17-18, how do believers receive the sword of the Spirit, which Spirit is the word of God?",
        "options": ["By means of all prayer and petition, praying at every time in spirit", "By manufacturing physical steel weapons for battle", "By memorizing philosophical debate techniques", "By demanding political authority in government"],
        "answer": "By means of all prayer and petition, praying at every time in spirit",
        "verse_ref": "Eph. 6:17-18",
        "explanation": "Ephesians 6:17-18 teaches pray-reading the Word: 'Receive the helmet of salvation and the sword of the Spirit, which Spirit is the word of God, by means of all prayer and petition, praying at every time in spirit.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Philippians & Inward Operation",
        "question": "In Philippians 2:13, who operates within the believer, and what does He operate?",
        "options": ["It is God who operates in you both the willing and the working for His good pleasure", "It is natural human willpower striving to keep the law", "It is angelic guardians moving our limbs", "It is ancestral memory guiding our choices"],
        "answer": "It is God who operates in you both the willing and the working for His good pleasure",
        "verse_ref": "Phil. 2:13",
        "explanation": "Philippians 2:13: 'For it is God who operates in you both the willing and the working for His good pleasure.' God is not outside demanding; He is inside operating!"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Philippians & Gaining Christ",
        "question": "In Philippians 3:8 and 10, what was Paul's single passionate ambition for which he counted all things as refuse?",
        "options": ["That I may gain Christ and know Him and the power of His resurrection and the fellowship of His sufferings", "That I may obtain the highest seat in the Jerusalem Sanhedrin", "That I may publish the largest library of philosophical scrolls", "That I may be recognized as chief apostle over all regions"],
        "answer": "That I may gain Christ and know Him and the power of His resurrection and the fellowship of His sufferings",
        "verse_ref": "Phil. 3:8, 10",
        "explanation": "Philippians 3:8, 10: Paul counted all things loss that he might gain Christ, be found in Him, and know Him, the power of His resurrection, and the fellowship of His sufferings, being conformed to His death."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Colossians & Inhabiting Word",
        "question": "According to Colossians 3:16, how should the word of Christ reside within the believers?",
        "options": ["Let the word of Christ dwell in you richly in all wisdom", "Keep the word of Christ locked in church vaults for scholars", "Read the word of Christ only on ceremonial feast days", "Treat the word of Christ as ancient historical myth"],
        "answer": "Let the word of Christ dwell in you richly in all wisdom",
        "verse_ref": "Col. 3:16",
        "explanation": "Colossians 3:16: 'Let the word of Christ dwell in you richly in all wisdom, teaching and admonishing one another with psalms and hymns and spiritual songs, singing with grace in your hearts to God.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Timothy & The Human Spirit",
        "question": "In 2 Timothy 1:7, what kind of spirit has God given to us, and what kind has He NOT given us?",
        "options": ["God has not given us a spirit of cowardice, but of power and of love and of sobermindedness", "God has given us a spirit of fear, trembling, and solemn gloom", "God has given us an intellectual spirit of debate and controversy", "God has given us a spirit of passive sleep"],
        "answer": "God has not given us a spirit of cowardice, but of power and of love and of sobermindedness",
        "verse_ref": "2 Tim. 1:7",
        "explanation": "2 Timothy 1:7: 'For God has not given us a spirit of cowardice, but of power (will) and of love (emotion) and of sobermindedness (mind).' The regenerated human spirit fans into flame!"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Timothy & Companions in Calling",
        "question": "In 2 Timothy 2:22, with whom is Timothy commanded to flee youthful lusts and pursue righteousness, faith, love, and peace?",
        "options": ["With those who call on the Lord out of a pure heart", "With isolated ascetics living alone in desert caves", "With prominent politicians and civic leaders", "With the religious scribes and Pharisees of Jerusalem"],
        "answer": "With those who call on the Lord out of a pure heart",
        "verse_ref": "2 Tim. 2:22",
        "explanation": "2 Timothy 2:22: 'Flee youthful lusts, and pursue righteousness, faith, love, peace with those who call on the Lord out of a pure heart.' Vital spiritual companions calling on the Lord together."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Hebrews & One Source",
        "question": "In Hebrews 2:11, what is the organic relationship between Christ the Sanctifier and the believers who are being sanctified?",
        "options": ["Both He who sanctifies and those who are being sanctified are all of One, for which cause He is not ashamed to call them brothers", "He is an unapproachable monarch and they are distant subjects", "He is the master and they are hired day-laborers", "He is the creator and they remain mere clay without His divine life"],
        "answer": "Both He who sanctifies and those who are being sanctified are all of One, for which cause He is not ashamed to call them brothers",
        "verse_ref": "Heb. 2:11",
        "explanation": "Hebrews 2:11 reveals the marvelous truth of sonship: 'For both He who sanctifies and those who are being sanctified are all of One, for which cause He is not ashamed to call them brothers.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Hebrews & Holy of Holies",
        "question": "According to Hebrews 10:19-20, by what new and living way do believers have boldness to enter into the Holy of Holies?",
        "options": ["In the blood of Jesus, through the veil, that is, His flesh", "By presenting animal sacrifices once a year on Yom Kippur", "By wearing Aaron's embroidered linen robes", "By climbing the slopes of Mount Sinai"],
        "answer": "In the blood of Jesus, through the veil, that is, His flesh",
        "verse_ref": "Heb. 10:19-20",
        "explanation": "Hebrews 10:19-20: 'Having therefore, brothers, boldness for entering the Holy of Holies in the blood of Jesus, which entrance He initiated for us as a new and living way through the veil, that is, His flesh.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Hebrews & Looking Away",
        "question": "In Hebrews 12:2, unto whom are believers urged to look away as they run the heavenly race with endurance?",
        "options": ["Looking away unto Jesus, the Author and Perfecter of our faith", "Looking unto our own failures and shortcomings", "Looking unto the opinions and praises of the world", "Looking unto historical monuments and ancient tombs"],
        "answer": "Looking away unto Jesus, the Author and Perfecter of our faith",
        "verse_ref": "Heb. 12:2",
        "explanation": "Hebrews 12:2: 'Looking away unto Jesus, the Author and Perfecter of our faith, who for the joy set before Him endured the cross, despising the shame, and has sat down on the right hand of the throne of God.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Hebrews & Outside the Camp",
        "question": "In Hebrews 13:13, where are believers exhorted to go forth unto Jesus, since He suffered outside the gate?",
        "options": ["Let us therefore go forth unto Him outside the camp, bearing His reproach", "Let us build a protective walled compound within the city", "Let us seek compromise with religious tradition", "Let us plead for acceptance from the high council"],
        "answer": "Let us therefore go forth unto Him outside the camp, bearing His reproach",
        "verse_ref": "Heb. 13:13",
        "explanation": "Hebrews 13:13: 'Let us therefore go forth unto Him outside the camp, bearing His reproach.' The camp typifies religious organizations and systems that reject the living Christ."
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 Peter & Living Stones",
        "question": "According to 1 Peter 2:5, what are believers as they come to Christ the living stone?",
        "options": ["You yourselves also, as living stones, are being built up a spiritual house into a holy priesthood", "Isolated gems stored separately in velvet boxes", "Inert bricks stacked in a monument", "Decorative carvings placed upon exterior walls"],
        "answer": "You yourselves also, as living stones, are being built up a spiritual house into a holy priesthood",
        "verse_ref": "1 Pet. 2:5",
        "explanation": "1 Peter 2:5: 'You yourselves also, as living stones, are being built up a spiritual house into a holy priesthood to offer up spiritual sacrifices acceptable to God through Jesus Christ.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "2 Peter & Divine Nature",
        "question": "According to 2 Peter 1:4, through God's precious and exceedingly great promises, what have believers become?",
        "options": ["Partakers of the divine nature", "Angelic messengers of the cosmos", "Sovereign rulers over physical planets", "Impassive observers of universe history"],
        "answer": "Partakers of the divine nature",
        "verse_ref": "2 Pet. 1:4",
        "explanation": "2 Peter 1:4 reveals deification in life and nature: 'through these you might become partakers of the divine nature, having escaped the corruption which is in the world by lust.'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "1 John & The Anointing",
        "question": "In 1 John 2:27, what divine provision abides within believers, teaching them concerning all things?",
        "options": ["The anointing which you have received from Him abides in you, and you have no need that anyone teach you", "A leather scroll of ecclesiastical canons", "An external council of scholars voting on truth", "A system of scholastic theology memorized by rote"],
        "answer": "The anointing which you have received from Him abides in you, and you have no need that anyone teach you",
        "verse_ref": "1 John 2:27",
        "explanation": "1 John 2:27 shows the moving and working of the indwelling compound Holy Spirit: 'And as for you, the anointing which you have received from Him abides in you, and you have no need that anyone teach you...'"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & Overcomers",
        "question": "In Revelation 2:7, what reward is promised to the overcomer in the church in Ephesus?",
        "options": ["To him who overcomes, to him I will give to eat of the tree of life, which is in the Paradise of God", "A golden sceptre to rule over Rome", "A marble statue erected in the city square", "A fleet of ships to sail across the Mediterranean"],
        "answer": "To him who overcomes, to him I will give to eat of the tree of life, which is in the Paradise of God",
        "verse_ref": "Rev. 2:7",
        "explanation": "Revelation 2:7: 'To him who overcomes, to him I will give to eat of the tree of life, which is in the Paradise of God' - returning to the central matter of eating Christ as life!"
    },
    {
        "type": "multiple_choice",
        "testament": "New Testament",
        "category": "Revelation & Pillar in the Temple",
        "question": "In Revelation 3:12, what promise is given to the overcomer in Philadelphia?",
        "options": ["He who overcomes, him I will make a pillar in the temple of My God... and I will write upon him the name of My God and the name of the city of My God, the New Jerusalem", "He will be exempted from physical mortality on earth", "He will receive an earthly army of ten thousand chariots", "He will sit upon an earthly throne in Antioch"],
        "answer": "He who overcomes, him I will make a pillar in the temple of My God... and I will write upon him the name of My God and the name of the city of My God, the New Jerusalem",
        "verse_ref": "Rev. 3:12",
        "explanation": "Revelation 3:12: 'He who overcomes, him I will make a pillar in the temple of My God, and he shall by no means go out anymore, and I will write upon him the name of My God and the name of the city of My God, the New Jerusalem...'"
    },
    {
        "type": "multi_select",
        "testament": "New Testament",
        "category": "Revelation & Marriage of the Lamb",
        "question": "In Revelation 19:7-8, how is the readiness of the Lamb's wife (the corporate church) described? (Select both)",
        "options": ["The marriage of the Lamb has come, and His wife has made herself ready", "It was given to her that she should be clothed in fine linen, bright and clean; for the fine linen is the righteousnesses of the saints", "She was crowned with pearls from the emperor's treasury", "She held a golden sceptre over the fallen nations"],
        "answer": ["The marriage of the Lamb has come, and His wife has made herself ready", "It was given to her that she should be clothed in fine linen, bright and clean; for the fine linen is the righteousnesses of the saints"],
        "verse_ref": "Rev. 19:7-8",
        "explanation": "Revelation 19:7-8: The bride is clothed in fine linen, bright and clean, which is the subjective righteousnesses (plural) of the saints - Christ lived out of the believers as their wedding garment."
    }
]

def get_random_bible_trivia_questions(count: int = 5, used_prompts=None) -> List[Dict[str, Any]]:
    """Returns a shuffled deck with a balanced mix of Old/New Testament questions, persisting across rounds."""
    if used_prompts is None:
        used_prompts = set()
    available = [q for q in BIBLE_TRIVIA_QUESTIONS if q.get("question") not in used_prompts]
    if len(available) < count:
        used_prompts.clear()
        available = list(BIBLE_TRIVIA_QUESTIONS)
    random.shuffle(available)
    selected = available[:count]
    for q in selected:
        used_prompts.add(q.get("question", ""))
    return selected
