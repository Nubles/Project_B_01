import json
import re

# The full raw text data provided by the user.
full_raw_data = """
Catalyst League Tasks
Easy Tasks (10 Points each)
Task ID	Locality	Task	Information	Requirements
462	Anachronia	Complete the base camp tutorial on Anachronia.	Complete the Anachronia base camp tutorial.	N/A
463	Anachronia	Observe all the large dragonkin statues around Anachronia.	Observe all the large dragonkin statues around Anachronia.	N/A
464	Anachronia	Surge under the spine on Anachronia.	Complete Spinal Surgery.	5 Agility
461	Anachronia	Set sail for Anachronia.	Set sail for Anachronia on The Stormbreaker docked at Varrock Dig Site.	N/A
465	Anachronia	Complete the quest: Helping Laniakea (miniquest).	Complete the Helping Laniakea miniquest.	See quest page
466	Anachronia	Complete the quest: Raksha, the Shadow Colossus.	Complete Raksha, the Shadow Colossus quest.	See quest page
467	Anachronia	Obtain 100 potent herbs from Herby Werby.	Obtain 100 potent herbs from Herby Werby.	1 Herblore
217	Burthorpe	Complete a lap of the Burthorpe Agility course.	Complete a lap of the Burthorpe Agility Course.	1 Agility
221	Falador	Kill a goblin raider boss in the Goblin Village.	Kill 15 goblins in the Goblin Village to spawn a Goblin raider boss.	N/A
222	Falador	Complete the quest: Witch's House.	Complete Witch's House.	See quest page
223	Falador	Sit down with Tiffy in Falador park.	Sit on the bench with Sir Tiffy Cashien in Falador Park.	N/A
224	Falador	Pray to Bandos's remains.	Pray to Bandos's remains (just south-east of Goblin Village).	N/A
225	Falador	Dance in the Falador party room.	Dance in the Falador party room.	N/A
263	Port Sarim	Give Thurgo a redberry pie.	Give Thurgo a redberry pie.	10 Cooking, Partial completion of The Knight's Sword
268	Taverley	Build a God statue in Taverley.	Build a God statue in Taverley.	N/A
271	Menaphos	Enter Menaphos.	Enter Menaphos.	N/A
272	Desert	Catch a whirligig at Het's Oasis.	Catch a whirligig at Het's Oasis.	1 Hunter
274	Desert	Search the Grand Gold Chest in room 1 of Pyramid Plunder in Sophanem.	Search the grand gold chest in room 1 of Pyramid Plunder in Sophanem.	21 Thieving, Partial completion of Icthlarin's Little Helper
275	Desert	Search the Grand Gold Chest in room 2 of Pyramid Plunder in Sophanem.	Search the grand gold chest in room 2 of Pyramid Plunder in Sophanem.	31 Thieving, Partial completion of Icthlarin's Little Helper
276	Desert	Search the Grand Gold Chest in room 3 of Pyramid Plunder in Sophanem.	Search the grand gold chest in room 3 of Pyramid Plunder in Sophanem.	41 Thieving, Partial completion of Icthlarin's Little Helper
277	Desert	Mine a gem rock at the Al Kharid mine.	Mine a gem rock at the Al Kharid mine. A common gem rock can be mined with level 1 Mining.	1 Mining
279	Desert	Kill a crocodile.	Kill a crocodile.	N/A
280	Desert	Create a spirit kalphite pouch at the obelisk south west of Pollnivneach.	Create a spirit kalphite pouch at the obelisk south west of Pollnivneach.	25 Summoning, A pouch, 51 spirit shards, a blue charm, and a potato cactus
281	Menaphos	Squish 10 corrupted scarabs.	Squish 10 corrupted scarabs.	N/A
282	Desert	Sell a pyramid top to Simon.	Hand Simon Templeton a pyramid top.	30 Agility
283	Desert	Use any of the magic carpets in the desert.	Use any of the magic carpets in the desert.	1,000 coins
284	Desert	Harvest a rose at Het's Oasis.	Harvest a rose at Het's Oasis.	30 Farming
339	Lunar Isles	Switch to the Lunar Spellbook at the astral altar.	Switch to the Lunar Spellbook at the astral altar.	Completion of Lunar Diplomacy
340	Fremennik	Defeat a Rock Crab in the Fremennik Province.	Defeat a Rock Crab in the Fremennik Province.	N/A
341	Fremennik	Defeat a Cockatrice in the Fremennik Province.	Defeat a cockatrice in the Fremennik Province.	25 Slayer, A mirror shield
342	Fremennik	Defeat a Troll in the Fremennik Province.	Defeat a troll in the Fremennik Province.	N/A
343	Fremennik	Deposit an item with Peer the Seer.	Deposit an item with Peer the Seer.	Completion of the easy Fremennik achievements
344	Fremennik	Use the Bank on Jatizso or Neitiznot.	Use the Bank on Jatizso or Neitiznot.	Partial completion of The Fremennik Isles
346	Fremennik	Catch a Sapphire Glacialis.	Catch a Sapphire Glacialis.	25 Hunter, A butterfly net and jar
127	Global	Level up any of your skills for the first time.	Level up any of your skills for the first time.	N/A
128	Global	Reach level 5 in any skill.	Reach level 5 in any skill.	N/A
129	Global	Reach level 10 in any skill.	Reach level 10 in any skill.	N/A
130	Global	Reach level 20 in any skill.	Reach level 20 in any skill.	N/A
136	Global	Reach combat level 5.	Reach combat level 5.	N/A
137	Global	Reach combat level 10.	Reach combat level 10.	N/A
141	Global	Reach total level 50.	Reach total level 50.	N/A
142	Global	Reach total level 100.	Reach total level 100.	N/A
147	Global	Mine a copper ore.	Mine copper ore from a copper rock.	1 Mining
148	Global	Mine 10 copper ore.	Mine 10 copper ore.	1 Mining
149	Global	Mine a tin ore.	Mine tin ore from a tin rock.	1 Mining
150	Global	Mine 10 tin ore.	Mine 10 tin ore.	1 Mining
151	Global	Smelt a bronze bar.	Smelt a bronze bar.	1 Smithing
152	Global	Smelt 10 bronze bars.	Smelt 10 bronze bars.	1 Smithing
153	Global	Smith any bronze item.	Smith any bronze item.	1 Smithing
154	Global	Mine clay.	Mine clay.	1 Mining
155	Global	Make some soft clay.	Make soft clay by using clay on a water source or with a container of water.	N/A
156	Global	Mine any ore 5 times.	Mine any ore 5 times.	1 Mining
159	Global	Chop any tree 5 times.	Chop any tree 5 times.	1 Woodcutting
162	Global	Chop a basic tree.	Chop a basic tree.	1 Woodcutting
163	Global	Chop 10 basic trees.	Chop 10 basic trees.	1 Woodcutting
164	Global	Chop an oak tree.	Chop an oak tree.	10 Woodcutting
166	Global	Burn any logs.	Burn any logs.	1 Firemaking
167	Global	Burn any logs 5 times.	Burn any logs 5 times.	1 Firemaking
170	Global	Catch a shrimp.	Catch a raw shrimp.	1 Fishing
171	Global	Catch 10 shrimp.	Catch 10 raw shrimps.	1 Fishing
172	Global	Catch an anchovy.	Catch a raw anchovy.	15 Fishing
173	Global	Catch a herring.	Catch a raw herring.	10 Fishing
174	Global	Cook shrimp, meat, or chicken.	Cook raw shrimps, raw meat, or raw chicken.	1 Cooking
175	Global	Cook 10 shrimp, meat, or chicken.	Cook 10 raw shrimps, raw meat, or raw chicken.	1 Cooking
176	Global	Burn any food.	Burn any food.	1 Cooking
177	Global	Catch any fish 5 times.	Catch any fish 5 times.	1 Fishing
180	Global	Bury any bones.	Bury any bones.	1 Prayer
181	Global	Bury any bones 10 times.	Bury any bones 10 times.	1 Prayer
182	Global	Activate the thick skin, rock skin, or steel skin Prayer.	Activate the Thick Skin, Rock Skin, or Steel Skin prayer.	1 Prayer
183	Global	Run out of Prayer points.	Run out of Prayer points.	1 Prayer
184	Draynor	Harvest a memory from a pale wisp.	Harvest a pale memory from a pale wisp.	1 Divination
185	Draynor	Harvest 10 memories from a pale wisp.	Harvest 10 pale memories from a pale wisp.	1 Divination
186	Global	Harvest any memory from a wisp 5 times.	Harvest any memory from a wisp 5 times.	1 Divination
189	Global	Pickpocket from a man or woman.	Pickpocket from a man or woman.	1 Thieving
190	Global	Pickpocket from a man or woman 10 times.	Pickpocket from a man or woman 10 times.	1 Thieving
191	Global	Steal from any stall.	Steal from any stall.	2 Thieving for Vegetable Stalls
192	Global	Steal from any stall 10 times.	Steal from any stall 10 times.	2 Thieving for Vegetable Stalls
193	Global	Pickpocket anyone 5 times.	Pickpocket anyone 5 times.	1 Thieving
196	Global	Rake any farming patch.	Rake any farming patch.	1 Farming
197	Global	Plant seeds in any farming patch.	Plant seeds in any farming patch.	1 Farming
198	Global	Plant seeds in any farming patch 10 times.	Plant seeds in any farming patch 10 times.	1 Farming
200	Global	Add any compostable item to a compost bin.	Add any compostable item to a compost bin.	N/A
201	Global	Have a tool leprechaun note any produce.	Have a tool leprechaun note any produce.	N/A
204	Global	Use the Home Teleport spell to return to Lumbridge.	Use the Home Teleport spell to return to Lumbridge.	N/A
205	Global	Eat a cabbage.	Eat a cabbage.	N/A
206	Global	Eat a baked potato.	Eat a baked potato.	7 Cooking
207	Global	Eat an onion.	Eat an onion.	N/A
208	Global	Kill an imp.	Kill an imp.	N/A
209	Global	Kill a chicken.	Kill a chicken.	N/A
210	Global	Claim a free item from any store.	Claim a free item from any store e.g. a tinderbox from Lumbridge General Store.	N/A
211	Global	Return a free item to any store.	Return a free item to any store e.g. a tinderbox from Lumbridge General Store.	N/A
212	Global	Sell an item to any store.	Sell an item to any store.	N/A
213	Global	Listen to any musician.	Listen to any musician.	N/A
214	Global	Pick wheat from a field.	Pick wheat from a field.	N/A
215	Global	Prospect any rock.	Prospect any rock.	1 Mining
216	Global	View the skillguide.	View the skill guide.	N/A
345	Global	Create a Guthix Rest Potion.	Create a Guthix rest potion.	18 Herblore, Partial completion of One Small Favour
770	Global	Make 5 potions of any kind.	Make 5 potions of any kind.	1 Herblore
773	Global	Drink a Strength Potion.	Drink a Strength Potion.	Giving a limpwurt root and red spiders' eggs to the Apothecary
774	Global	Make an Attack Potion.	Make an Attack potion.	1 Herblore, A clean guam and an eye of newt
775	Global	Make a Necromancy Potion.	Make a Necromancy potion.	11 Herblore, A clean marrentill and cadava berries
776	Global	Clean 5 Grimy Guam.	Clean 5 grimy guam.	1 Herblore, 5 grimy guam
777	Global	Clean 15 Grimy Tarromin.	Clean 15 grimy tarromin.	5 Herblore, 15 grimy tarromin
778	Global	Clean 5 of any herb.	Clean 5 of any herb.	1 Herblore, 5 of any grimy herb
779	Global	Clean 10 of any herb	Clean 10 of any herb	1 Herblore, 10 of any grimy herb
782	Global	Fletch an Oak Shortbow (unstrung).	Fletch an unstrung oak shortbow.	20 Fletching, Oak logs
783	Global	Fletch some arrow shafts.	Fletch some arrow shafts.	1 Fletching, Logs of any kind
785	Global	Fletch 50 Bronze bolts.	Fletch 50 bronze bolts.	9 Fletching, A bronze bar and 50 feathers
786	Global	Complete 10 laps of any Agility course.	Complete 10 laps of any Agility course.	1 Agility
790	Global	Smith 10 of any metal weapon or armour piece.	Smith 10 of any metal weapon or armour piece.	1 Smithing, 10 of any metal bar
794	Global	Open 30 Sedimentary Geodes.	Open 30 sedimentary geodes. These are found randomly while mining.	1 Mining
795	Global	Maintain nearly maximum stamina when mining for 60 seconds.	Maintain nearly maximum stamina when mining for 60 seconds.	1 Mining
796	Global	Harvest a Grimy Marrentill.	Harvest a grimy marrentill.	9 Farming, Marrentill seed
797	Global	Harvest 10 Grimy Tarromin.	Harvest 10 grimy tarromin.	19 Farming, Tarromin seeds
798	Global	Cook 5 fish.	Cook 5 fish.	1 Cooking, 5 of any raw fish
801	Global	Make some Bread.	Make some bread. Bread dough can be created by using a pot of flour with water, it must be cooked at a range.	1 Cooking, Bread dough
802	Global	Make some flour.	Make a pot of flour by grinding wheat at a windmill and collecting the flour in an empty pot.	Wheat and an empty pot
803	Global	Offer 5 bones of any kind to an altar.	Offer 5 bones (ashes also work) at the chaos altar in the Wilderness, the altar in Fort Forinthry, or an altar in the player-owned house chapel.	1 Prayer
804	Global	Offer 25 bones of any kind to an altar.	Offer 25 bones (ashes also work) at the chaos altar in the Wilderness, the altar in Fort Forinthry, or an altar in the player-owned house chapel.	1 Prayer
806	Global	Scatter some Ashes.	Scatter some ashes.	1 Prayer, Any demonic ashes
807	Global	Scatter 25 ashes of any kind.	Scatter 25 ashes of any kind.	1 Prayer, 25 of any demonic ashes
809	Global	Restore 50 Prayer Points at an Altar at once.	Restore 50 Prayer Points at an Altar at once.	5 Prayer
811	Global	Activate Superhuman or Ultimate Strength and Improved or Incredible Reflexes prayers at the same time.	Activate Superhuman or Ultimate Strength and Improved or Incredible Reflexes prayers at the same time.	16 Prayer
812	Global	Catch a Baby Impling.	Catch a baby impling. Cannot be completed in Puro-Puro.	17 Hunter
813	Global	Catch 10 Implings of any kind.	Catch 10 implings. Cannot be completed in Puro-Puro.	N/A
816	Global	Catch 5 Hunter creatures.	Catch 5 Hunter creatures.	1 Hunter
819	Global	Complete 5 Slayer tasks.	Complete 5 Slayer assignments.	1 Slayer
823	Global	Pick 5 Flax.	Pick 5 flax from flax fields.	N/A
824	Global	Spin 5 bowstring.	Spin 5 bowstrings by using flax on a spinning wheel.	1 Fletching, 5 flax
825	Global	Surge a distance of one tile.	Surge a distance of one tile.	5 Agility
826	Global	Spin a Ball of Wool.	Spin a ball of wool by using wool at a spinning wheel.	1 Fletching, Wool
827	Global	Equip a full set of Iron armour without any upgrades.	Equip an iron full helm, iron platebody, iron platelegs / iron plateskirt, iron gauntlets, iron armoured boots, and an iron kiteshield. Substitutes for pieces will work.	10 Defence
828	Global	Equip a full set of Green Dragonhide armour.	Equip a full set of green dragonhide armour.	40 Defence
829	Global	Equip a full set of Imphide robes.	Equip a full set of imphide robes.	10 Defence
830	Global	Equip a full set of Spider silk robes.	Equip a full set of spider silk robes.	20 Defence
831	Global	Store the items required for an emote clue in a Treasure Trail hidey-hole.	Store the items required for an emote clue in a Treasure Trail hidey-hole.	27 Construction, 4 planks and 10 of any nails for an easy hidey-hole
832	Global	Complete an Easy clue scroll.	Complete an easy clue scroll.	N/A
836	Global	Collect 10 unique items for the General clue rewards collection log.	Collect 10 unique items for the general clue rewards collection log.	N/A
403	Gnomes	Complete the Gnome Stronghold Agility Course.	Complete the Gnome Stronghold Agility Course.	1 Agility
404	Feldip	Catch a Crimson Swift in the Feldip Hills.	Catch a crimson swift in the Feldip Hills.	1 Hunter, A bird snare
405	Ardougne	Defeat a Tortoise with riders in Kandarin.	Defeat a tortoise with riders in Kandarin.	N/A
406	Seers	Complete the quest: You Are It.	Complete You Are It.	See quest page
407	Gnomes	Let Brimstail teleport you to the Rune Essence mine.	Let Brimstail teleport you to the Rune Essence mine.	N/A
408	Feldip	Equip a Marksman hat.	Equip a marksman hat.	125 chompy bird kills
409	Piscatoris	Obtain a Naragi engram from Orla Fairweather.	Obtain a Naragi engram from Orla Fairweather. The engram is given to the player during the tutorial for Memorial to Guthix.	1 Divination
410	Ardougne	Learn how many beans make five (complete the Player Owned Farm tutorial).	Complete the player-owned farm tutorial at Manor Farm.	17 Farming, 20 Construction
411	Piscatoris	Catch a Wild Kebbit.	Catch a wild kebbit.	23 Hunter, Logs of any kind
412	Ardougne	Teleport to the Wilderness using the lever in Ardougne.	Pull the lever in Ardougne.	N/A
413	Yanille	Use a ring of duelling to teleport to Castle Wars.	Teleport to Castle Wars with a ring of duelling.	27 Magic, 27 Crafting, Materials to make a ring of duelling
414	Gnomes	Make a Pineapple Punch cocktail.	Make a pineapple punch cocktail.	8 Cooking, See pineapple punch for ingredients
572	Karamja	Collect 5 seaweed from anywhere on Karamja.	Collect 5 seaweed from anywhere on Karamja.	N/A
573	Karamja	Fill up Luthas' crate near the Musa Point plantation with bananas and receive 30 coins for your work.	Fill up Luthas' crate near the Banana plantation with bananas and talk to him to receive 30 coins for your work.	N/A
574	Karamja	Claim a ticket from Brimhaven Agility Arena.	Claim a ticket from Brimhaven Agility Arena.	1 Agility
575	Karamja	Kill a snake.	Kill a snake.	N/A
576	Karamja	Catch a Karambwanji.	Catch a raw karambwanji.	5 Fishing
577	Karamja	Be assigned a Slayer task in Shilo Village.	Be assigned a Slayer task in Shilo Village.	100 Combat, 50 Slayer, Completion of Shilo Village
578	Karamja	Defeat a Greater Demon on Karamja.	Defeat a greater demon on Karamja.	N/A
579	Karamja	Pick a pineapple on Karamja.	Pick a pineapple on Karamja from the pineapple plants near the lodestone.	N/A
580	Karamja	Enter the Brimhaven Dungeon.	Enter the Brimhaven Dungeon.	875 coins
581	Karamja	Cross the spiky pit using the stepping stones within Brimhaven Dungeon.	Cross the spiky pit using the stepping stones within Brimhaven Dungeon.	12 Agility
0	Lumbridge	Progress through the Leagues tutorial to unlock your first relic.	Progress through the Leagues tutorial to unlock your first relic.	N/A
2	Draynor	Climb to the top of the Wizards' Tower.	Climb to the top of the Wizards' Tower.	N/A
3	Draynor	Have Ned make you some rope from balls of wool.	Have Ned make you some rope from 4 balls of wool.	N/A
4	Draynor	Siphon from a fire essling in the Runespan.	Siphon from a fire essling in the Runespan.	14 Runecrafting
5	Draynor	Convert at least one pale memory into energy.	Convert at least one pale memory into energy.	1 Divination
15	Edgeville	Kill a mugger near the Edgeville lodestone.	Kill a mugger near the Edgeville lodestone.	N/A
16	Edgeville	Mine some coal in the centre of Barbarian village.	Mine some coal in the centre of Barbarian Village.	20 Mining
22	Fort Forinthry	Use the bank in the workshop at Fort Forinthry.	Use the bank in the workshop at Fort Forinthry.	N/A
27	Lumbridge	Kill a giant rat in Lumbridge Swamp.	Kill a giant rat in Lumbridge Swamp.	N/A
28	Lumbridge	Kill a goblin in Lumbridge.	Kill a goblin in Lumbridge.	N/A
29	Lumbridge	Kill a giant spider in Lumbridge or Lumbridge Swamp.	Kill a giant spider in Lumbridge or Lumbridge Swamp.	N/A
30	Lumbridge	Milk a cow.	Milk a cow.	A bucket
32	Lumbridge	Talk to Hans and find out how old you are.	Talk to Hans and find out how old you are.	N/A
33	Lumbridge	Complete the quest: The Blood Pact.	Complete The Blood Pact.	See quest page
35	Draynor	Catch some shrimp in the fishing spot to the east of Lumbridge Swamp.	Catch some shrimp in the fishing spot to the east of Lumbridge Swamp.	1 Fishing
36	Lumbridge	Smelt a steel bar in the furnace in Lumbridge.	Smelt a steel bar in the furnace in Lumbridge.	20 Smithing
37	Lumbridge	Cook some rat meat on a fire in Lumbridge Swamp.	Cook some rat meat on a campfire in Lumbridge Swamp.	1 Cooking
38	Lumbridge	Mine iron ore from the mining site south-west of Lumbridge Swamp.	Mine iron ore from the mining site south-west of Lumbridge Swamp.	10 Mining
39	Lumbridge	Craft a water rune at the Water Altar.	Craft a water rune at the Water altar.	5 Runecrafting
40	Lumbridge	Complete a task from Jacquelyn, the Lumbridge Slayer master.	Complete a task from Jacquelyn, the Lumbridge Slayer master.	1 Slayer
41	Lumbridge	Fill a Charmed Sack with corruption at the Nexus in Lumbridge Swamp.	Fill a charmed sack with corruption at the Nexus in Lumbridge Swamp.	1 Prayer
61	Draynor	Complete the quest: Necromancy!.	Complete Necromancy!	See quest page
62	City of Um	Upgrade a piece of Death Skull or Deathwarden equipment to tier 20.	Upgrade a piece of death skull or deathwarden equipment to tier 20.	20 Necromancy, 15 Smithing (death skull) OR 15 Crafting (Deathwarden), Completion of Kili Row
63	City of Um	Craft some spirit or bone runes.	Craft some spirit or bone runes.	1 Runecrafting, Partial completion of Rune Mythos
64	City of Um	Complete a Lesser Necroplasm ritual.	Complete a Lesser Necroplasm ritual.	5 Necromancy
65	City of Um	Conjure a skeleton at the City of Um ritual site.	Conjure a Skeleton Warrior at the Um ritual site.	2 Necromancy, Conjure Skeleton Warrior unlocked at the Well of Souls
66	City of Um	Conjure a zombie at the City of Um ritual site.	Conjure a Putrid Zombie at the Um ritual site.	40 Necromancy, Conjure Putrid Zombie unlocked at the Well of Souls
67	City of Um	Conjure a ghost at the City of Um ritual site.	Conjure a Vengeful Ghost at the Um ritual site.	40 Necromancy, Conjure Vengeful Ghost unlocked at the Well of Souls
94	Varrock	Kill a dark wizard.	Kill a dark wizard.	N/A
95	Varrock	Enter the Earth Altar using an earth tiara or talisman.	Enter the earth altar using an earth tiara or talisman.	1 Runecrafting
96	Varrock	Have Elsie tell you a story.	Have Elsie tell you a story, she is found upstairs in the church in Varrock. You must give her a cup of tea.	A cup of tea
97	Varrock	Give a bone to one of Varrock's stray dogs (or to your pet stray dog if you have one).	Use some bones on one of Varrock's stray dogs (or to your pet stray dog if you have one).	N/A
98	Varrock	Claim a free clue scroll from Zaida at the Grand Exchange.	Claim a free clue scroll from Zaida at the Grand Exchange.	N/A
99	Fort Forinthry	Give Bill a beer in Fort Forinthry.	Give Bill a beer in Fort Forinthry.	A beer, partial completion of New Foundations
100	Varrock	Complete the Archaeology tutorial.	Complete the Archaeology tutorial.	1 Archaeology
101	Fort Forinthry	Make a plank yourself on the sawmill in Fort Forinthry.	Make a plank yourself on the sawmill in Fort Forinthry.	1 Construction, Partial completion of New Foundations
102	Varrock	Mine some iron ore in the mining spot south-west of Varrock.	Mine some iron ore in the mining spot south-west of Varrock.	10 Mining
103	Varrock	Steal from the Varrock tea stall.	Steal from the Varrock tea stall.	5 Thieving
104	Varrock	Pan in the river at the Digsite.	This can only be completed after the point during The Dig Site quest where the panning guide teaches you how to pan for gold. You can then use the panning point. If you complete the quest without completing this achievement the task will be completed by attempting to pan with a panning tray in your inventory.	Partial completion of The Dig Site
693	Morytania	Take an easy companion through an easy route of Temple Trekking.	Complete an Easy Temple Trek.	Completion of In Aid of the Myreque
694	Morytania	Craft your own snelm in Morytania.	Craft a snelm.	15 Crafting, Any blamish shell
695	Morytania	Defeat a Werewolf in Morytania.	Defeat a Werewolf in Morytania.	N/A
696	Morytania	Pass through the Holy barrier.	Pass through the Holy barrier.	Defeat a Ghoul (Paterdomus)
697	Morytania	Enter through the western gate of Port Phasmatys.	Pass through the western gate of Port Phasmatys.	N/A
698	Morytania	Activate the lodestone in Canifis.	Activate the Canifis lodestone.	Access to Morytania
699	Morytania	Kill anything on the ground floor of the Slayer Tower.	Kill anything on the ground floor of the Slayer Tower.	1 Slayer, Access to Morytania
700	Morytania	Using either a Silver Sickle or the Ivandis Flail, grow some fungus in the swamp using Bloom.	Cast Bloom using a blessed sickle or the Ivandis flail in Mort Myre Swamp.	18 Crafting, Completion of Nature Spirit
701	Morytania	Defeat 5 Feral Vampyres in the Haunted Woods.	Defeat 5 feral vampyres in the Haunted Woods.	Access to Morytania
702	Morytania	Use an ectophial to return to Port Phasmatys.	Use an ectophial to return to Port Phasmatys.	Completion of Ghosts Ahoy
703	Morytania	Visit Dragontooth Island by boat.	Visit Dragontooth Island by boat.	Ghostspeak amulet
514	Elven Lands	Cook a Rabbit in Tirannwn.	Cook a raw rabbit in Tirannwn.	1 Cooking
515	Elven Lands	Attempt to pass a leaf trap.	Attempt to pass a leaf trap.	N/A
516	Elven Lands	Use the Bank in Lletya.	Use the bank in Lletya.	N/A
517	Elven Lands	Charter a ship from Port Tyras.	Charter a ship from Port Tyras.	N/A
518	Elven Lands	Climb the Tower of Voices.	Climb the Tower of Voices.	N/A
519	Elven Lands	Burn some logs using the everlasting bonfire in the Tower of Voices.	Burn some logs using the everlasting bonfire in the Tower of Voices.	1 Firemaking
520	Elven Lands	Activate the lodestone in Prifddinas.	Activate the Prifddinas lodestone.	N/A
521	Elven Lands	Activate the lodestone in Tirannwn.	Activate the Tirannwn lodestone.	N/A
522	Elven Lands	Restore your prayer using the altar in Lletya.	Restore your prayer using the altar in Lletya.	1 Prayer
630	Wilderness	Use the bank at the Mage Arena.	Use the Mage Arena bank.	N/A
631	Wilderness	Defeat the Chaos Elemental.	Defeat the Chaos Elemental once.	N/A
632	Wilderness	Defeat the Chaos Elemental. (100 times)	Defeat the Chaos Elemental 100 times.	N/A
633	Wilderness	Reach a score of 10 using the strange switches in the Wilderness.	Reach a score of 10 using the strange switches in the Wilderness.	N/A
634	Wilderness	Jump over the Wilderness wall.	Jump over the Wilderness wall.	N/A
635	Wilderness	Activate the lodestone near the Wilderness Crater.	Activate the Wilderness Crater lodestone.	N/A
636	Daemonheim	Complete a Frozen floor in Daemonheim.	Complete a Frozen floor in Daemonheim.	1 Dungeoneering
637	Daemonheim	Make use of either an autoheater, gem bag, herbicide, bonecrusher or charming imp.	Make use of either an autoheater, gem bag, herbicide, bonecrusher or charming imp.	The gem bag is the cheapest reward at 2000 dungeoneering token, and upgrading it is required for a later task.
638	Wilderness	Enter the chaos tunnels from an entrance in the Wilderness.	Enter the Chaos Tunnels from an entrance in the Wilderness.	N/A
639	Wilderness	Defeat a Black Unicorn in the Wilderness.	Defeat a black unicorn in the Wilderness.	N/A
Medium Tasks (30 Points each)
Task ID	Locality	Task	Information	Requirements
468	Anachronia	Build your Player Lodge on Anachronia.	Build your Player Lodge on Anachronia.	40 Construction
469	Anachronia	Purchase the herb bag and the herb bag upgrade from the Herby Werby reward shop.	Purchase the herb bag and the herb bag upgrade from the Herby Werby reward shop.	1 Herblore, Requires 4 weeks worth of potent herbs
470	Anachronia	Give Snoop some clean Dwarf weed.	Give Snoop some clean dwarf weed.	70 Herblore if cleaning the herb yourself
471	Anachronia	Harvest produce from 5 animals on Anachronia farm.	Harvest produce from 5 animals on Anachronia farm.	42 Farming, 45 Construction
473	Anachronia	Complete the beginner sections of the Anachronia agility course.	Complete the beginner sections of the Anachronia agility course.	30 Agility
474	Anachronia	Complete the novice sections of the Anachronia agility course.	Complete the novice sections of the Anachronia agility course.	50 Agility
218	Burthorpe	Enter the Warriors Guild.	Enter the Warriors Guild.	Combined Attack and Strength level of 130, or 99 Attack, or 99 Strength
219	Burthorpe	Equip a defender.	Equip a defender.	Combined Attack and Strength level of 130, or 99 Attack, or 99 Strength
220	Burthorpe	Charge an Amulet of Glory in the Heroes' Guild.	Charge an amulet of glory in the Heroes' Guild.	80 Crafting and 68 Magic to make it from scratch, or 83 Hunter to catch dragon implings, Completion of Heroes' Quest
226	Falador	Enter the Crafting Guild.	Enter the Crafting Guild.	40 Crafting
227	Falador	Complete the task set: Easy Falador.		See Easy Falador achievements page
228	Falador	Complete the task set: Medium Falador.		See Medium Falador achievements page
229	Falador	Defeat the Giant Mole.	Kill the giant mole.	N/A
230	Falador	Defeat the Giant Mole. (50 times)	Kill the giant mole 50 times.	N/A
231	Falador	Steal some Wine of Zamorak from the Captured Temple, south of Goblin Village.	Steal some wine of Zamorak from the Captured Temple, south of Goblin Village.	33 Magic for Telekinetic Grab
232	Falador	Set up a dwarf cannon.	Set up a dwarf multicannon.	Completion of Dwarf Cannon
233	Falador	Complete a ceremonial sword at the Artisans' Workshop.	Complete a ceremonial sword at the Artisans' Workshop.	1 Smithing
234	Falador	Mine some orichalcite in the Mining Guild.	Mine some orichalcite ore in the Mining Guild.	60 Mining
235	Burthorpe	Harvest a herb from the troll stronghold herb patch.	Harvest a herb from the troll stronghold herb patch.	9 Farming to plant the lowest Herb seed, Completion of My Arm's Big Adventure
269	Taverley	Kill a blue dragon in Taverley dungeon.	Kill a blue dragon in Taverley dungeon.	Dusty key or 70 Agility
270	Taverley	Open the crystal chest in Taverley.	Open the crystal chest in Taverley.	A crystal key
273	Desert	Clear the Fort debris at the Kharid-et Dig Site.	Clear the fort debris at the Kharid-et Dig Site.	12 Archaeology
278	Desert	Complete the quest: One Piercing Note.	Complete One Piercing Note.	See quest page
285	Desert	Complete a lap of the Het's Oasis agility course.	Complete a lap of the Het's Oasis agility course.	65 Agility
286	Desert	Defeat the Kalphite Queen.	Defeat the Kalphite Queen.	N/A
287	Desert	Defeat the Kalphite Queen. (100 times)	Defeat the Kalphite Queen 100 times.	N/A
288	Desert	Defeat 100 bosses in the Dominion Tower.	Defeat 100 bosses in the Dominion Tower.	Completion of at least 20 various quests
289	Desert	Complete the task set: Easy Desert.	Easy desert tasks.	See Easy Desert achievements page
290	Desert	Complete the task set: Medium Desert.	Medium desert tasks.	See Medium Desert achievements page
291	Menaphos	Steal from the lamp stall in Menaphos.	Steal from the lamp stall in Menaphos.	46 Thieving
292	Desert	Buy some runes from Ali Morrisane.	Buy some runes from Ali Morrisane.	Completion of the runes portion of Ali the Trader
293	Menaphos	Catch a catfish.	Catch a raw catfish.	60 Fishing
294	Desert	Restore a Pontifex signet ring.	Restore a pontifex signet ring.	58 Archaeology, A cut dragonstone, which may require 55 Crafting
295	Desert	Search the Grand Gold Chest in room 4 of Pyramid Plunder in Sophanem.	Search the Grand Gold Chest in room 4 of Pyramid Plunder in Sophanem.	51 Thieving
296	Desert	Search the Grand Gold Chest in room 5 of Pyramid Plunder in Sophanem.	Search the Grand Gold Chest in room 5 of Pyramid Plunder in Sophanem.	61 Thieving
297	Desert	Search the Grand Gold Chest in room 6 of Pyramid Plunder in Sophanem.	Search the Grand Gold Chest in room 6 of Pyramid Plunder in Sophanem.	71 Thieving
298	Desert	Complete the quest: Smoking Kills.	Complete Smoking Kills.	See quest page
299	Desert	Complete the quest: Desert Treasure.	Complete Desert Treasure.	See quest page
300	Desert	Fully repair the statue of Het.	Repair the statue of Het at Het's Oasis.	200 pieces of Het
347	Lunar Isles	Cast Moonclan Teleport.	Cast Moonclan Teleport.	69 Magic
348	Fremennik	Move Your House to Rellekka.	Move your player-owned house's location to Rellekka by speaking to an estate agent.	30 Construction, 10,000 coins
349	Lunar Isles	Craft 50 Astral Runes.	Craft 50 astral runes.	40 Runecrafting, Completion of Lunar Diplomacy
350	Fremennik	Complete the Penguin Agility Course.	Complete the Penguin Agility Course.	30 Agility, Completion of Cold War
351	Fremennik	Catch a Snowy Knight.	Catch a Snowy Knight.	35 Hunter, A butterfly net and jar
352	Fremennik	Defeat a Kurask in the Fremennik Province.	Defeat a Kurask in the Fremennik Province.	70 Slayer, Leaf-bladed spear or other special weapon
353	Fremennik	Defeat a Dagannoth in the Fremennik Province.	Defeat a dagannoth in the Fremennik Province.	N/A
354	Fremennik	Equip a Helm of Neitiznot.	Equip a Helm of Neitiznot.	55 Defence, Completion of The Fremennik Isles
355	Fremennik	Defeat a Jelly in the Fremennik Province.	Defeat a jelly in the Fremennik Province.	52 Slayer
356	Fremennik	Complete the quest: Throne of Miscellania.	Complete Throne of Miscellania.	See quest page
357	Fremennik	Complete the quest: Royal Trouble.	Complete Royal Trouble.	See quest page
358	Fremennik	Equip a Granite Shield.	Equip a granite shield.	55 Defence, 55 Strength, Either completion of Eadgar's Ruse or partial completion of The Fremennik Isles
359	Fremennik	Equip a full set of Graahk, Larupia or Kyatt hunter gear.	Equip a full set of graahk, larupia or kyatt hunter gear.	31 Hunter to hunt spined larupia
360	Fremennik	Defeat any of the Dagannoth Kings.	Defeat any of the Dagannoth Kings 1 time.	N/A
361	Fremennik	Defeat any of the Dagannoth Kings.	Defeat any of the Dagannoth Kings 100 times.	N/A
362	Fremennik	Complete the task set: Easy Fremennik.		N/A
363	Fremennik	Ride a mine cart into Keldagrim.	Ride a mine cart into Keldagrim.	Completion of The Giant Dwarf
364	Fremennik	Travel to the Mammoth Iceberg.	Travel to the Mammoth Iceberg (must travel by boat, Skull of Slaying teleport does not work but can be used to take the boat back and forth).	N/A
365	Fremennik	Steal from the fish stall in Rellekka.	Steal from the fish stall in Rellekka.	42 Thieving, Completion of The Fremennik Trials
366	Fremennik	Harvest 100 sparkling energy from Sparkling Wisps.	Harvest 100 sparkling energy from sparkling wisps.	40 Divination
367	Fremennik	Climb to the top of the lighthouse.	Climb to the top of the lighthouse.	Completion of Horror from the Deep
368	Fremennik	Chop 10 Artic Pine trees.	Chop 10 arctic pine trees.	54 Woodcutting, Partial completion of The Fremennik Isles
369	Fremennik	Kill 25 Yaks.	Kill 25 yaks.	Partial completion of The Fremennik Isles
370	Fremennik	Interact with a pet rock.	Interact with a pet rock.	Partial completion of The Fremennik Trials
383	Fremennik	Complete the task set: Medium Fremennik.	Complete the Medium Fremennik achievements.	See Medium Fremennik achievements page
131	Global	Reach level 50 in any skill.	Reach level 50 in any skill.	Any skill at level 50
132	Global	Reach at least level 5 in all non-elite skills.	Reach at least level 5 in all non-elite skills.	All skills except Invention at level 5
133	Global	Reach at least level 10 in all non-elite skills.	Reach at least level 10 in all non-elite skills.	All skills except Invention at level 10
134	Global	Reach at least level 20 in all non-elite skills.	Reach at least level 20 in all non-elite skills.	All skills except Invention at level 20
138	Global	Reach combat level 50.	Reach combat level 50.	50 Combat level
143	Global	Reach total level 500.	Reach total level 500. This task is currently bugged and may complete before you have reached 500 total levels.	500 Total level
157	Global	Mine any ore 200 times.	Mine any ore 200 times.	1 Mining
160	Global	Chop any tree 200 times.	Chop any tree 200 times.	1 Woodcutting
165	Global	Chop a willow tree.	Chop a willow tree.	20 Woodcutting
168	Global	Burn any logs 200 times.	Burn any logs 200 times.	1 Firemaking
178	Global	Catch any fish 200 times.	Catch any fish 200 times.	1 Fishing
187	Global	Harvest any memory from a wisp 200 times.	Harvest any memory from a wisp 200 times.	1 Divination
194	Global	Pickpocket anyone 200 times.	Pickpocket anyone 200 times.	1 Thieving
199	Global	Plant seeds in any farming patch 100 times.	Plant seeds in any farming patch 100 times.	1 Farming
202	Global	Unlock all of the Free to Play Lodestones.	Unlock all of the Free to Play Lodestones.	N/A
771	Global	Make 200 potions of any kind.	Make 200 potions of any kind.	1 Herblore
780	Global	Clean 200 of any herb.	Clean 200 of any herb.	1 Herblore
784	Global	Fletch 1,000 arrow shafts.	Fletch 1,000 Arrow Shafts.	1 Fletching
787	Global	Complete 25 laps of any Agility course.	Complete 25 laps of any Agility course.	1 Agility
791	Global	Smith 25 of any metal weapon or armour piece.	Smith 25 of any metal weapon or armour piece.	1 Smithing
799	Global	Cook 200 fish.	Cook 200 fish.	1 Cooking
805	Global	Offer 100 bones of any kind to an altar.	Offer 100 bones (ashes also work) at the chaos altar in the Wilderness, the altar in Fort Forinthry, or an altar in the player-owned house chapel.	1 Prayer
808	Global	Scatter 100 ashes of any kind.	Scatter 100 ashes of any kind.	1 Prayer
810	Global	Restore 500 Prayer Points at an Altar at once.	Restore 500 Prayer Points at an Altar at once.	50 Prayer
814	Global	Catch 25 Implings of any kind.	Catch 25 implings of any kind. Cannot be completed in Puro-Puro.	17 Hunter
815	Global	Catch 35 Implings of any kind.	Catch 35 Implings of any kind. Cannot be completed in Puro-Puro.	17 Hunter
817	Global	Catch 200 Hunter creatures.	Catch 200 Hunter creatures.	1 Hunter
833	Global	Complete 25 Easy clue scrolls.	Complete 25 easy clue scrolls.	N/A
834	Global	Complete 75 Easy clue scrolls.	Complete 75 easy clue scrolls.	N/A
837	Global	Collect 25 unique items for the General clue rewards collection log.	Collect 25 unique items for the general clue rewards collection log.	N/A
839	Global	Make 30 Prayer Potions.	Make 30 prayer potions.	38 Herblore
840	Global	Make a 4-dose Potion.	Make a 4-dose potion.	1 Herblore, A botanist's amulet, Morytania legs 4, Underworld Grimoire 1, or a Varanusaur pen with a farm totem at the Anachronia Dinosaur Farm
841	Global	Make 20 Super Attack Potions.	Make 20 super attack potions.	45 Herblore
842	Global	Clean 50 Grimy Ranarr.	Clean 50 grimy ranarr.	25 Herblore
843	Global	Clean 50 Grimy Avantoe.	Clean 50 grimy avantoe.	48 Herblore
844	Global	Harvest 5 Grimy Ranarr.	Harvest 5 grimy ranarr.	32 Farming
845	Global	Equip an Iron Crossbow.	Equip an iron crossbow.	10 Ranged
846	Global	Equip a Maple shieldbow.	Equip a maple shieldbow.	30 Ranged, 30 Defence
847	Global	Fletch 50 Maple shieldbow (unstrung).	Fletch 50 unstrung maple shieldbows.	55 Fletching
848	Global	Fletch 400 Steel arrows.	Fletch 400 steel arrows.	30 Fletching
849	Global	Fletch 100 Iron bolts.	Fletch 100 iron bolts.	39 Fletching
850	Global	Mine some Ore With a Rune Pickaxe.	Mine some ore with a rune pickaxe.	50 Mining
851	Global	Mine 20 Mithril Ore.	Mine 20 mithril ore.	30 Mining
852	Global	Mine 30 Adamant Ore.	Mine 30 adamantite ore.	40 Mining
853	Global	Mine 40 Runite Ore.	Mine 40 runite ore.	50 Mining
854	Global	Open 20 Igenous Geodes.	Open 20 igneous geodes. These are found randomly while mining from rocks which require at least level 60 Mining.	60 Mining
855	Global	Check a grown Fruit Tree.	Check a tree grown in a fruit tree patch.	27 Farming
856	Global	Catch 100 Lobsters.	Catch 100 lobsters.	40 Fishing (or 68 Fishing via swarm fishing)
857	Global	Catch 50 Swordfish.	Catch 50 swordfish.	50 Fishing
858	Global	Catch 50 Salmon.	Catch 50 salmon.	30 Fishing
859	Global	Catch 10 Pike.	Catch 10 pike.	25 Fishing
860	Global	Make a Pineapple pizza.	Make a pineapple pizza by adding pineapple chunks or a pineapple ring to a plain pizza.	65 Cooking, Plain pizza and pineapple
861	Global	Make a Stew.	Make a stew: add a raw potato to a bowl of water, then add either cooked meat or chicken, and cook the stew at a range.	25 Cooking
862	Global	Make a Chocolate Cake.	Make a chocolate cake by adding a chocolate bar to a cooked cake.	50 Cooking, Cake and chocolate bar
863	Global	Bury some Baby Dragon bones.	Bury some baby dragon bones.	N/A
864	Global	Bury 5 Dragon bones.	Bury 5 dragon bones.	1 Prayer
865	Global	Activate Protect from Melee prayer.	Activate the Protect from Melee prayer.	43 Prayer
866	Global	Catch a Gourmet Impling.	Catch a gourmet impling. Cannot be completed in Puro-Puro.	28 Hunter
867	Global	Light a Bullseye Lantern.	Light a bullseye lantern.	49 Firemaking, Either 36 Thieving and completion of Death to the Dorgeshuun; or 50 Quest points and the Lorehound pet unlocked; or 20 Smithing and 49 Crafting to create from scratch
868	Global	Teleport using Law runes.	Teleport using law runes. The lowest level teleport spell is South Feldip Hills Teleport which also requires one air and one water rune.	10 Magic, A law rune
869	Global	Craft some Combination runes.	Craft some combination runes: mist runes have the lowest level requirement.	6 Runecrafting, A pure essence
870	Global	Craft 100 runes.	Craft 100 runes.	1 Runecrafting
871	Global	Craft 1,000 runes.	Craft 1,000 runes.	1 Runecrafting
874	Global	Equip a full set of Steel armour.	Equip a full set of steel armour (helm, body, legs, boots, and gauntlets).	20 Defence
875	Global	Equip a full set of Mithril armour.	Equip a full set of mithril armour (full helm, platebody, legs, boots, and gauntlets).	30 Defence
876	Global	Equip a full set of Adamant armour.	Equip a full set of adamant armour (full helm, platebody, legs, boots, and gauntlets).	40 Defence
877	Global	Equip a full set of Rune armour.	Equip a full set of rune armour (full helm, platebody, legs, boots, and gauntlets).	50 Defence
878	Global	Equip a full set of Blue Dragonhide armour.	Equip a full set of blue dragonhide armour.	50 Defence
879	Global	Equip a full set of Red Dragonhide armour.	Equip a full set of red Dragonhide armour.	55 Defence
880	Global	Equip a full set of Batwing robes.	Equip a full set of batwing robes.	30 Defence
881	Global	Equip a full set of Mystic robes.	Equip a full set of mystic robes.	50 Defence
882	Global	Create a Mithril Grapple.	Create a mithril grapple.	59 Fletching, 30 Smithing
883	Global	Burn 25 Willow logs.	Burn 25 willow logs.	30 Firemaking
884	Global	Burn 50 Maple logs.	Burn 50 maple logs.	45 Firemaking
885	Global	Equip any elemental battlestaff.	Equip any elemental battlestaff.	30 Magic
886	Global	Equip a mystic staff.	Equip a mystic staff.	40 Magic
887	Global	Obtain 50 Quest Points.	Obtain 50 quest points.	50 Quest points
891	Global	Complete 100 clues of any tier.	Complete 100 clues of any tier.	N/A
892	Global	Complete a Medium clue scroll.	Complete a medium clue scroll.	N/A
893	Global	Complete 25 Medium clue scrolls.	Complete 25 medium clue scrolls.	N/A
894	Global	Complete 75 Medium clue scrolls.	Complete 75 medium clue scrolls.	N/A
896	Global	Complete a Hard clue scroll.	Complete a hard clue scroll.	N/A
897	Global	Complete 25 Hard clue scrolls.	Complete 25 hard clue scrolls.	N/A
900	Global	Collect 5 unique items for the Easy clue rewards collection log.	Collect 5 unique items for the easy clue rewards collection log.	N/A
901	Global	Collect 10 unique items for the Easy clue rewards collection log.	Collect 10 unique items for the easy clue rewards collection log.	N/A
904	Global	Collect 5 unique items for the Medium clue rewards collection log.	Collect 5 unique items for the medium clue rewards collection log.	N/A
905	Global	Collect 10 unique items for the Medium clue rewards collection log.	Collect 10 unique items for the Medium clue rewards collection log.	N/A
908	Global	Collect 5 unique items for the Hard clue rewards collection log.	Collect 5 unique items for the hard clue rewards collection log.	N/A
912	Global	Equip any 2 pieces of an Elegant outfit.	Equip any 2 pieces of an elegant outfit.	N/A
913	Global	Equip a composite bow of any kind.	Equip a composite bow of any kind.	20 Ranged
943	Global	Perform a Special Attack.	Perform a special attack.	5 Attack or 5 Ranged or 5 Magic (claimed from Gudrik in Port Sarim)
1098	Global	Reach level 30 in any skill.	Reach level 30 in any skill.	N/A
1099	Global	Reach level 40 in any skill.	Reach level 40 in any skill.	N/A
1100	Global	Reach level 60 in any skill.	Reach level 60 in any skill.	N/A
1105	Global	Reach at least level 30 in all non-elite skills.	Reach at least level 30 in all non-elite skills.	All skills except Invention at level 30
415	Ardougne	Fletch 50 Maple shieldbow (unstrung) in Kandarin.	Fletch 50 unstrung maple shieldbows in Kandarin.	55 Fletching
416	Ardougne	Pickpocket a Knight of Ardougne 50 times.	Pickpocket a knight of Ardougne 50 times.	55 Thieving
417	Ardougne	Complete the Barbarian Outpost Agility Course.	Complete the Barbarian Outpost Agility Course.	35 Agility, Completion of Bar Crawl (miniquest)
418	Piscatoris	Equip a Spottier Cape.	Equip a spottier cape.	66 Hunter
419	Ardougne	Catch a red salamander from the Hunter area outside of Ourania Altar.	Catch a red salamander.	59 Hunter
420	Ardougne	Enter the Fishing Guild.	Enter the Fishing Guild.	68 Fishing
421	Gnomes	Check a grown Papaya Tree inside Tree Gnome Stronghold.	Check a grown papaya tree inside Tree Gnome Stronghold.	57 Farming
422	Ardougne	Kill a mithril dragon.	Defeat a mithril dragon.	N/A
423	Yanille	Enter the Magic Guild in Yanille.	Enter the Wizards' Guild.	66 Magic
424	Ardougne	Defeat a Fire Giant in Kandarin.	Defeat a fire giant in Kandarin.	N/A
425	Seers	Use the Chivalry Prayer.	Use the Chivalry prayer.	60 Prayer, 65 Defence, Completion of Knight Waves training ground
426	Yanille	Be on the winning side in a game of Castle Wars.	Win a game of Castle Wars.	N/A
427	Seers	Complete the quest: Elemental Workshop II.	Complete Elemental Workshop II.	See quest page
428	Feldip	Equip an Ogre Expert hat.	Equip an ogre expert hat.	300 chompy bird kills
429	Ardougne	Complete the task set: Easy Ardougne.	Complete the Easy Ardougne achievements.	See Easy Ardougne achievements page
430	Gnomes	Create the listed gnome cocktails.	Complete The Great Gnomish Shake Off achievement.	37 Cooking
431	Ardougne	Earn a total amount of 10,000 beans.	Earn a total of 10,000 beans from selling animals in player-owned farm.	17 Farming
432	Piscatoris	Hunt 10 Spotted Kebbits with the help of a falcon.	Hunt 10 spotted kebbits with using falconry.	43 Hunter
433	Piscatoris	Complete the quest: The Needle Skips.	Complete The Needle Skips.	See quest page
434	Ardougne	Complete the task set: Medium Ardougne.	Complete the Medium Ardougne achievements.	See Medium Ardougne achievements page
582	Karamja	Complete the task set: Easy Karamja.	Complete the Easy Karamja achievements.	See Easy Karamja achievements page
583	Karamja	Craft 50 Nature runes.	Craft 50 nature runes.	44 Runecrafting
584	Karamja	Catch a salmon on Karamja.	Catch a salmon on Karamja.	30 Fishing, Completion of Shilo Village
585	Karamja	Get Stiles to exchange some of your fish for bank notes.	Get Stiles to exchange some of your fish for bank notes.	N/A
586	Karamja	Convert 100 gleaming memories in an energy rift.	Convert 100 gleaming memories in an energy rift.	50 Divination
587	Karamja	Mine a drakolith rock in the Tai Bwo Wannai mine.	Mine a drakolith rock in the Tai Bwo Wannai mine.	60 Mining
588	Karamja	Mine a ruby from a gem rock in Shilo Village.	Mine a ruby from a gem rock in Shilo Village.	30 Mining, Completion of Shilo Village
589	Karamja	Enter the Hardwood Grove in Tai Bwo Wannai.	Enter the Hardwood Grove in Tai Bwo Wannai.	Completion of Jungle Potion
590	Karamja	Complete the quest: Dragon Slayer.	Complete Dragon Slayer.	See quest page
591	Karamja	Check a grown banana tree on Karamja.	Check a grown banana tree on Karamja.	33 Farming
592	Karamja	Defeat a TzHaar.	Defeat a TzHaar.	N/A
593	Karamja	Equip an Obsidian cape.	Equip an obsidian cape.	N/A
594	Karamja	Kill a metal dragon in Brimhaven Dungeon.	Kill a metal dragon in Brimhaven Dungeon.	N/A
595	Karamja	Catch 25 lobsters on Karamja.	Catch 25 lobsters on Karamja.	40 Fishing
596	Karamja	Equip a Toktz-Ket-Xil.	Equip a Toktz-Ket-Xil.	60 Defence
597	Karamja	Equip a Tzhaar-Ket-Om.	Equip a Tzhaar-Ket-Om.	60 Strength
598	Karamja	Equip a Toktz-Xil-Ak.	Equip a Toktz-Xil-Ak.	60 Attack
599	Karamja	Equip a Toktz-Xil-Ek.	Equip a Toktz-Xil-Ek.	60 Attack
600	Karamja	Complete the task set: Medium Karamja.	Complete the Medium Karamja achievements.	See Medium Karamja achievements page
1	Draynor	Kill the lesser demon in the Wizards' Tower.	Kill the lesser demon in the Wizards' Tower.	Cannot be attacked with short-range melee
6	Draynor	Hunt a yellow wizard in the RuneSpan and give them some items.	Hunt a yellow wizard in the Runespan and give them some items.	1 Runecrafting
7	Draynor	Use the Rune Goldberg Machine to create Vis wax.	Use the Rune Goldberg Machine to create vis wax.	50 Runecrafting
8	Draynor	Siphon from a nature esshound in the Runespan.	Siphon from a nature esshound in the Runespan.	44 Runecrafting
9	Draynor	Siphon Rune dust from a RuneSphere in the RuneSpan.	Siphon rune dust from a Runesphere in the RuneSpan.	1 Runecrafting
17	Edgeville	Fully complete the Stronghold of Player Safety.	Fully complete the Stronghold of Player Safety by pulling an old lever on the upper floor and then opening the treasure chest in the secure sector.	N/A
23	Fort Forinthry	Complete the quest: New Foundations.	Complete New Foundations.	See quest page
26	Lumbridge	Complete the task set: Beginner Lumbridge.	Given by Explorer Jack in Lumbridge for completing all Beginner Tasks in Lumbridge.	See Beginner Lumbridge achievements page
34	Draynor	Complete the quest: Duck Quest.	Complete Duck Quest.	See quest page
42	Lumbridge	Complete the task set: Easy Lumbridge.	Given by Bob, the axe seller in Lumbridge, for completing all Easy Tasks in Lumbridge.	See Easy Lumbridge achievements page
43	Lumbridge	Complete the task set: Medium Lumbridge.	Given by Ned in Draynor Village for completing all Medium Tasks in Lumbridge.	See Medium Lumbridge achievements page
44	Lumbridge	Drink from the Tears of Guthix.	Drink from the Tears of Guthix.	Completion of Tears of Guthix (quest)
45	Lumbridge	Complete world 25 in Shattered Worlds.	Reach world 25 in Shattered Worlds.	N/A
46	Lumbridge	Catch 20 implings in Puro-Puro.	Catch 20 implings in Puro-Puro.	17 Hunter
47	Lumbridge	Complete the quest: Sheep Shearer (miniquest).	Complete Sheep Shearer miniquest.	N/A
48	Lumbridge	Cut a willow tree east of Lumbridge Castle.	Cut the willow tree east of Lumbridge Castle, by the bridge across the River Lum.	20 Woodcutting
49	Lumbridge	Craft 50 Water Runes.	Craft 50 water runes.	5 Runecrafting, Water talisman or equivalent
50	Lumbridge	Pickpocket a H.A.M. member.	Pickpocket a H.A.M. member.	15 Thieving
51	Lumbridge	Churn some butter.	Make a pat of butter by using a bucket of milk at a dairy churn.	38 Cooking, Bucket of milk
52	Lumbridge	Craft 50 cosmic runes.	Craft 50 cosmic runes.	27 Runecrafting, Cosmic talisman or equivalent (or access through the Abyss), completion of Lost City quest
53	Lumbridge	Steal a lantern from a cave goblin.	Steal a lantern from a cave goblin (only the ones in Dorgesh-Kaan have the lantern as a possible loot from pickpocketting).	36 Thieving, Completion of Death to the Dorgeshuun quest
54	Lumbridge	Use the range in Lumbridge Castle to bake a cake.	Use the range in Lumbridge Castle to bake a cake.	40 Cooking, Completion of Cook's Assistant quest
68	City of Um	Have either a Putrid Zombie or Vengeful Ghost conjured while fighting the matching creature.	Have either a Putrid Zombie or Vengeful Ghost conjured while fighting the matching creature.	40 Necromancy, Unlock the ability to conjure at tier 3 of talents, conduit, ectoplasm?
69	City of Um	Learn how to craft moonstone jewellery.	Learn how to craft moonstone jewellery.	50 Necromancy, Brown apron or keepsaked override
70	City of Um	Disgruntle an inhabitant of Um by wearing a bedsheet.	Disgruntle an inhabitant of Um by wearing a bedsheet, see Poor Imitation for NPCs which can be disgruntled.	Completion of Ghosts Ahoy quest, bedsheet
71	City of Um	Upgrade a piece of Death Skull or Deathwarden equipment to tier 50.	Upgrade a piece of Death Skull or Deathwarden equipment to tier 50.	20 Necromancy, Completion of Necromancy! and Kili Row. See also Kili's Knowledge III.
72	City of Um	Complete a communion ritual using a memento.	Complete a communion ritual using a memento.	5 Necromancy, Completion of Necromancy!
73	City of Um	Conjure a Phantom Guardian at the City of Um ritual site.	Conjure a Phantom Guardian at the Um ritual site.	70 Necromancy, Conjure Phantom Guardian unlocked from the Well of Souls
74	City of Um	Complete the task set: Easy Underworld.	Complete the Easy Underworld achievements.	See Easy Underworld achievements page
84	City of Um	Complete the task set: Medium Underworld.	Complete the Medium Underworld achievements.	See Medium Underworld achievements page
105	Varrock	Complete the task set: Easy Varrock.	Given by Rat Burgiss south of Varrock for completing all Easy Tasks in Varrock.	See Easy Varrock achievements page
106	Varrock	Complete the task set: Medium Varrock.	Given by Reldo in Varrock Palace's library for completing all Medium Tasks in Varrock.	See Medium Varrock achievements page
107	Edgeville	Browse through Oziach's Armour Shop.	Browse through Oziach's Armour Shop.	Completion of Dragon Slayer quest
108	Varrock	Enter the Cooks' Guild.	Enter the Cooks' Guild.	32 Cooking, Chef's hat of equivalent
109	Varrock	Complete the quest: Demon Slayer.	Complete Demon Slayer.	See quest page
110	Varrock	Complete the quest: Vampyre Slayer.	Complete Vampyre Slayer.	See quest page
111	Varrock	Mine 50 pure essence.	Mine 50 pure essence.	30 Mining
112	Varrock	Pickpocket a guard in Varrock Palace's courtyard.	Pickpocket a Varrock guard.	40 Thieving
113	Varrock	Gather and convert 50 bright memories.	Gather and convert 50 bright memories.	20 Divination
704	Morytania	Complete the task set: Easy Morytania.	Complete the Easy Morytania achievements.	See Easy Morytania achievements page
705	Morytania	Take a medium companion through a medium route of Temple Trekking.	Take a medium companion through a medium route of Temple Trekking.	Completion of In Aid of the Myreque
706	Morytania	Visit Mos Le'Harmless.	Visit Mos Le'Harmless.	Partial completion of Cabin Fever
707	Morytania	Visit Harmony Island.	Visit Harmony Island.	Partial completion of The Great Brain Robbery
708	Morytania	Visit the Everlight dig site.	Visit the Everlight dig site.	42 Archaeology
709	Morytania	Finish a game of Werewolf Skullball.	Finish a game of Werewolf Skullball.	25 Agility, Completion of Creature of Fenkenstrain
710	Morytania	Defeat the six Barrows Brothers and loot their chest.	Defeat the six Barrows Brothers and loot their chest once.	N/A
711	Morytania	Defeat the six Barrows Brothers and loot their chest. (100 times)	Defeat the six Barrows Brothers and loot their chest 100 times.	N/A
712	Morytania	Equip a Barrows weapon.	Equip a barrows weapon.	70 Magic, 70 Attack, or 70 Ranged
713	Morytania	Equip a piece of Barrows armour.	Equip a piece of barrows armour.	70 Defence
714	Morytania	Equip a Salve Amulet (e).	Equip a salve amulet (e).	Completion of Lair of Tarn Razorlor (miniquest)
715	Morytania	Make a batch of cannonballs in Port Phasmatys.	Make a batch of cannonballs in Port Phasmatys.	35 Smithing, Completion of Dwarf Cannon
716	Morytania	Catch 10 Green salamanders.	Catch 10 Green salamanders.	29 Hunter
717	Morytania	Complete the quest: Haunted Mine.	Complete Haunted Mine.	See quest page
718	Morytania	Harvest bittercap mushrooms in the farming patch near Canifis.	Harvest bittercap mushrooms in the farming patch near Canifis.	53 Farming
719	Morytania	Complete the task set: Medium Morytania.		N/A
523	Elven Lands	Complete the task set: Easy Tirannwn.	Complete the Easy Tirannwn achievements.	See Easy Tirannwn achievements page
524	Elven Lands	Check a grown Papaya Tree in Lletya.	Check a grown papaya tree in Lletya.	57 Farming
525	Elven Lands	Craft 50 Death Runes.	Craft 50 death runes.	65 Runecrafting
526	Elven Lands	Move your house to Prifddinas.	Move your player-owned house's location to Prifddinas by speaking to an estate agent.	75 Construction, 50,000 coins
527	Elven Lands	Use an Elven Teleport Crystal.	Use a crystal teleport seed.	N/A
528	Elven Lands	Equip Iban's staff.	Equip Iban's staff.	50 Magic
529	Elven Lands	Catch 10 Pawyas in Isafdar.	Catch 10 pawyas in Isafdar.	66 Hunter
530	Elven Lands	Mine 200 soft clay in Prifddinas.	Mine 200 soft clay in Prifddinas.	75 Mining
531	Elven Lands	Use the fairy ring in the Amlodd district.	Use the fairy ring in the Amlodd district.	Partial completion of A Fairy Tale II - Cure a Queen
532	Elven Lands	Complete the task set: Medium Tirannwn.	Complete the Medium Tirannwn achievements.	See Medium Tirannwn achievements page
640	Wilderness	Complete the task set: Easy Wilderness.	Complete the Easy Wilderness achievements.	See Easy Wilderness achievements page
641	Wilderness	Defeat the King Black Dragon.	Defeat the King Black Dragon once.	N/A
642	Wilderness	Defeat the King Black Dragon. (100 times)	Defeat the King Black Dragon 100 times.	N/A
643	Wilderness	Sacrifice Dragon bones on the Chaos Altar.	Sacrifice dragon bones on the chaos altar in the Wilderness.	1 Prayer
644	Wilderness	Cast the Claws of Guthix special attack.	Cast the Claws of Guthix special attack.	60 Magic, Completion of Mage Arena, Guthix staff
645	Wilderness	Defeat 5 Green dragons.	Defeat 5 green dragons.	N/A
646	Wilderness	Complete 10 laps of the Wilderness agility course.	Complete 10 laps of the Wilderness agility course.	52 Agility
647	Wilderness	Equip a Saradomin, Zamorak, or Guthix cape.	Equip a Saradomin, Zamorak, or Guthix cape.	60 Magic, Completion of Mage Arena
648	Wilderness	Visit any Runecrafting altar through the Abyss.	Visit any Runecrafting altar through the Abyss.	Completion of Enter the Abyss (miniquest)
649	Wilderness	Defeat 10 Fetid Zombies.	Defeat 10 fetid zombies.	N/A
650	Wilderness	Defeat 20 Bound Skeletons.	Defeat 20 bound skeletons.	N/A
651	Daemonheim	Defeat the Rammernaut.	Defeat the Rammernaut.	35 Dungeoneering
652	Wilderness	Defeat Bossy McBoss Face.	Defeat Bossy McBoss Face.	N/A
653	Wilderness	Activate and teleport from each of the Wilderness teleport obelisks.	Activate and teleport from each of the Wilderness teleport obelisks.	N/A
654	Wilderness	Defeat Bossy McBossface's first mate.	Defeat Bossy McBossface's first mate.	N/A
655	Wilderness	Complete the task set: Medium Wilderness.	Complete the Medium Wilderness achievements.	See Medium Wilderness achievements page
Hard Tasks (80 Points each)
Task ID	Locality	Task	Information	Requirements
472	Anachronia	Harvest produce from 25 animals on Anachronia farm.	Harvest produce from 25 animals on Anachronia farm.	42 Farming, 45 Construction
475	Anachronia	Complete the ritual to activate a totem on Anachronia.	Complete the ritual to activate a totem on Anachronia.	N/A
476	Anachronia	Complete the Anachronia agility course in under 7 minutes.	Complete the Anachronia agility course in under 7 minutes.	85 Agility
477	Anachronia	Complete all frog breeds.	Complete all frog breeds.	42 Farming, 45 Construction
478	Anachronia	Purchase the Quick Traps upgrade from Irwinsson's Hunter Mark shop.	Purchase the quick traps upgrade from the Hunter Mark Shop.	50 Hunter marks
479	Anachronia	Complete the quest: Osseous Rex.	Complete the Osseous Rex quest.	See quest page
480	Anachronia	Clear an Overgrown idol on Anachronia.	Clear an overgrown idol on Anachronia.	81 Woodcutting
481	Anachronia	Defeat any of the Rex Matriarchs.	Defeat any of the Rex Matriarchs once.	N/A
482	Anachronia	Defeat any of the Rex Matriarchs. (100 times)	Defeat any of the Rex Matriarchs 100 times.	N/A
483	Anachronia	Complete the quest: Desperate Times.	Complete the Desperate Times quest.	See quest page
484	Anachronia	Find all the hidden Zygomites on Anachronia.	Find all of the ancient zygomites on Anachronia. See the page for a route.	85 Agility
485	Anachronia	Equip Laniakea's spear.	Equip Laniakea's spear.	82 Attack
486	Anachronia	Harvest an Arbuck herb.	Harvest an arbuck herb.	77 Farming
487	Anachronia	Complete the advanced sections of the Anachronia agility course.	Complete the advanced sections of the Anachronia agility course.	70 Agility
488	Anachronia	Equip a Dragon Mattock.	Equip a dragon mattock.	60 Archaeology, (optional) 75 Hunter
490	Anachronia	Take down each dinosaur in Big Game Hunter.	Take down each dinosaur in Big Game Hunter.	96 Hunter, 76 Slayer
492	Anachronia	Get caught by each of the big game creatures once.	Get caught by each of the Big Game Hunter creatures once.	96 Hunter, 76 Slayer
493	Anachronia	Complete a big game encounter without using movement abilities.	Complete a Big Game Hunter encounter without using movement abilities.	75 Hunter, 55 Slayer
500	Anachronia	Defeat Raksha, the Shadow Colossus.	Defeat Raksha, the Shadow Colossus once.	Completion of Raksha, the Shadow Colossus (quest)
236	Falador	Reach 100% respect at the Artisans' Workshop.	Reach 100% respect at the Artisans' Workshop.	1 Smithing
237	Falador	Complete the task set: Hard Falador.	Complete the Hard Falador achievements.	See Hard Falador achievements page
246	Burthorpe	Defeat any God Wars Dungeon boss 100 times.	Defeat any God Wars Dungeon boss 100 times.	Partial completion of Troll Stronghold
247	Burthorpe	Defeat any God Wars Dungeon boss 250 times.	Defeat any God Wars Dungeon boss 250 times.	Partial completion of Troll Stronghold
248	Burthorpe	Defeat Commander Zilyana.	Defeat Commander Zilyana.	70 Agility, Partial completion of Troll Stronghold
249	Burthorpe	Defeat General Graardor.	Defeat General Graardor.	70 Strength, Partial completion of Troll Stronghold
250	Burthorpe	Defeat K'ril Tsutsaroth.	Defeat K'ril Tsutsaroth.	70 Constitution, Partial completion of Troll Stronghold
251	Burthorpe	Defeat Kree'arra.	Defeat Kree'arra.	70 Ranged, Partial completion of Troll Stronghold
252	Burthorpe	Defeat Nex.	Defeat Nex.	70 Agility, 70 Strength, 70 Constitution, 70 Ranged, Partial completion of Troll Stronghold, completion of The Dig Site, frozen key
253	Burthorpe	Defeat Kree'arra. (100 times)	Defeat Kree'arra 100 times.	70 Ranged, Partial completion of Troll Stronghold
254	Burthorpe	Assemble any godsword from the God Wars Dungeon.	Assemble any godsword from the God Wars Dungeon.	80 Smithing and one of 70 Agility, 70 Strength, 70 Constitution, or 70 Ranged
264	Port Sarim	Defeat the Queen Black Dragon.	Defeat the Queen Black Dragon.	60 Summoning
265	Port Sarim	Defeat the Queen Black Dragon. (100 times)	Defeat the Queen Black Dragon 100 times.	60 Summoning
266	Port Sarim	Bury some frost dragon bones.	Bury some frost dragon bones.	85 Dungeoneering
301	Desert	Defeat the Kalphite King.	Defeat the Kalphite King.	N/A
302	Desert	Defeat the Kalphite King. (100 times)	Defeat the Kalphite King 100 times.	N/A
303	Desert	Equip a drygore weapon.	Equip a drygore weapon.	90 Attack
304	Desert	Become an honorary druid at the Garden of Kharid.	Purchase the Druid/Druidess title for 50,000 Crux Eqal favour.	50 Farming
305	Desert	Deploy a dreadnip.	Deploy a dreadnip.	20 of a collection of quests (see Dominion Tower#Requirements), 450 Dominion Tower kills
306	Desert	Complete the task set: Hard Desert.	Complete the Hard Desert achievements.	See Hard Desert achievements page
307	Desert	Defeat Avaryss and Nymora.	Defeat the Twin Furies.	80 Ranged
308	Desert	Defeat Gregorovic.	Defeat Gregorovic.	80 Prayer
309	Desert	Defeat Vindicta and Gorvek.	Defeat Vindicta.	80 Attack
310	Desert	Defeat Helwyr.	Defeat Helwyr.	80 Magic
311	Desert	Defeat Avaryss and Nymora. (100 times)	Defeat the Twin Furies 100 times.	80 Ranged
312	Desert	Defeat Gregorovic. (100 times)	Defeat Gregorovic 100 times.	80 Prayer
313	Desert	Defeat Vindicta and Gorvek. (100 times)	Defeat Vindicta 100 times.	80 Attack
314	Desert	Defeat Helwyr. (100 times)	Defeat Helwyr 100 times.	80 Magic
315	Desert	Equip a Dragon Rider lance.	Equip a Dragon Rider lance.	85 Attack
316	Desert	Equip a wand or orb of the Cywir elders.	Equip a wand or orb of the Cywir elders.	85 Magic
317	Desert	Equip a shadow glaive.	Equip a shadow glaive.	85 Ranged
318	Desert	Equip a blade of Nymora or Avaryss.	Equip a blade of Nymora or Avaryss.	85 Attack
319	Menaphos	Slay a combination of 500 corrupted or devourer creatures.	Slay a combination of 500 corrupted creatures or soul devourers.	88 Slayer, Completion of Icthlarin's Little Helper
320	Desert	Defeat the Magister.	Defeat the Magister.	115 Slayer, Key to the Crossing
321	Desert	Defeat the Magister. (50 times)	Defeat the Magister 50 times.	115 Slayer, Key to the Crossing
322	Menaphos	Find an Off-hand khopesh of the Kharidian in Shifting Tombs.	Find an off-hand khopesh of the Kharidian in Shifting Tombs.	At least one of 50 Dungeoneering, 50 Agility, 50 Thieving, or 50 Construction
323	Desert	Search the Grand Gold Chest in room 7 of Pyramid Plunder in Sophanem.	Search the Grand Gold Chest in room 7 of Pyramid Plunder in Sophanem.	81 Thieving, Partial completion of Icthlarin's Little Helper
324	Desert	Search the Grand Gold Chest in room 8 of Pyramid Plunder in Sophanem.	Search the Grand Gold Chest in room 8 of Pyramid Plunder in Sophanem.	91 Thieving, Partial completion of Icthlarin's Little Helper
325	Menaphos	Complete the quest: Beneath Scabaras' Sands.	Complete Beneath Scabaras' Sands.	See quest page
326	Desert	Kill a desert strykewyrm wearing a Full Slayer Helm and wielding an ancient staff.	Kill a desert strykewyrm wearing a full Slayer helm and wielding an ancient staff.	77 Slayer, 50 Magic, 20 Defence, 55 Crafting, Completion of Desert Treasure and Smoking Kills, 400 slayer points to unlock crafting slayer helmets.
328	Desert	Defeat Telos, the Warden.	Defeat Telos, the Warden.	80 Attack, 80 Prayer, 80 Magic, 80 Ranged
371	Lunar Isles	Cast Fertile Soil.	Cast Fertile Soil.	83 Magic, Completion of Lunar Diplomacy unless tier 6 reached
372	Fremennik	Build a Gilded Altar.	Build a gilded altar in your player-owned house's chapel.	75 Construction
373	Fremennik	Trap a Sabre-Toothed Kyatt.	Trap a sabre-toothed kyatt.	55 Hunter
374	Fremennik	Defeat all the Dagannoth Kings without leaving a solo boss instance.	Defeat all the Dagannoth Kings without leaving a solo boss instance.	N/A
375	Fremennik	Equip a Berserker, Warrior, Seers, or Archers Ring.	Equip a Berserker, Warrior, Seers, or Archers Ring.	N/A
376	Fremennik	Use the Special Attack of a Dragon Axe.	Use the special attack of a dragon hatchet.	60 Attack
377	Fremennik	Defeat a Dagannoth King solo whilst wearing full yak-hide armour and a Fremennik round shield.	Defeat a Dagannoth King solo whilst wearing full yak-hide armour and a Fremennik round shield.	25 Defence, Partial completion of The Fremennik Isles
378	Fremennik	Equip a full set of Skeletal, Spined, or Rockshell armour.	Equip a full skeletal, spined, or rock-shell armour set.	50 Defence, Completion of The Fremennik Trials
379	Fremennik	Collect Miscellania Resources at Full Approval.	Collect from Managing Miscellania with a 100% approval rating.	Completion of Throne of Miscellania
380	Fremennik	Travel to the island of Ungael.	Travel to the island of Ungael.	Partial completion of Ancient Awakening
381	Fremennik	Adopt a baby yak.	Obtain an unchecked/baby Fremennik yak.	71 Farming, Partial completion of The Fremennik Isles
382	Fremennik	Catch 50 Azure Skillchompas.	Catch 50 azure skillchompas.	68 Hunter
384	Fremennik	Mine 10 Banite Ore north of Rellekka.	Mine 10 Banite ore in the arctic (azure) habitat mine. Only the western section works.	80 Mining
385	Fremennik	Smith a piece of Bane equipment to +4 in Rellekka.	Upgrade a piece of bane equipment to +4 in Rellekka.	80 Smithing, Completion of The Fremennik Trials
386	Fremennik	Use a Crystal triskelion key to obtain some treasures.	Use a crystal triskelion to obtain some treasures.	N/A
388	Fremennik	Create a Catherby Teleport Tablet.	Create a Catherby teleport tablet.	87 Magic, 67 Construction, Completion of Lunar Diplomacy. Even with Tier 6 unlocked, the option to create tablets is locked without quest completion.
392	Fremennik	Gather a seed from an Aquanite using Seedicide.	Gather a seed from an aquanite using Seedicide.	78 Slayer, 2,200 renown, 10,000 beans, 360 thaler, or tier 4 reached
393	Fremennik	Complete the task set: Hard Fremennik.	Complete the Hard Fremennik achievements.	See Hard Fremennik achievements page
135	Global	Reach at least level 50 in all non-elite skills.	Reach at least level 50 in all non-elite skills.	All skills except Invention at level 50
139	Global	Reach combat level 100.	Reach combat level 100.	100 Combat
144	Global	Reach total level 1000.	Reach total level 1000. This task is currently bugged and may complete before you have reached 1000 total levels.	1000 Total level
158	Global	Mine any ore 1000 times.	Mine any ore 1000 times.	1 Mining
161	Global	Chop any tree 1000 times.	Chop any tree 1000 times.	1 Woodcutting
169	Global	Burn any logs 1000 times.	Burn any logs 1000 times.	1 Firemaking
179	Global	Catch any fish 1000 times.	Catch any fish 1000 times.	1 Fishing
188	Global	Harvest any memory from a wisp 1000 times.	Harvest any memory from a wisp 1000 times.	1 Divination
195	Global	Pickpocket anyone 1000 times.	Pickpocket anyone 1000 times.	1 Thieving
203	Global	Unlock all of the Lodestones.	Unlock all of the Lodestones.	N/A
772	Global	Make 1,000 potions of any kind.	Make 1,000 potions of any kind.	1 Herblore
781	Global	Clean 1,000 of any herb.	Clean 1,000 of any herb.	1 Herblore
788	Global	Complete 50 laps of any Agility course.	Complete 50 laps of any Agility course.	1 Agility
789	Global	Complete 100 laps of any Agility course.	Complete 100 laps of any Agility course.	1 Agility
792	Global	Smith 50 of any metal weapon or armour piece.	Smith 50 of any metal weapon or armour piece.	1 Smithing
793	Global	Smith 100 of any metal weapon or armour piece.	Smith 100 of any metal weapon or armour piece.	1 Smithing
800	Global	Cook 1,000 fish.	Cook 1,000 fish.	1 Cooking
818	Global	Catch 1,000 Hunter creatures.	Catch 1,000 Hunter creatures.	1 Hunter
820	Global	Complete 15 Slayer tasks.	Complete 15 Slayer tasks.	1 Slayer
835	Global	Complete 150 Easy clue scrolls.	Complete 150 easy clue scrolls.	N/A
838	Global	Collect 50 unique items for the General clue rewards collection log.	Collect 50 unique items for the general clue rewards collection log.	N/A
872	Global	Craft 10,000 runes.	Craft 10,000 runes.	1 Runecrafting
873	Global	Craft 20,000 runes.	Craft 20,000 runes.	1 Runecrafting
888	Global	Obtain 75 Quest Points.	Obtain 75 quest points.	75 Quest points
889	Global	Obtain 100 Quest Points.	Obtain 100 quest points.	100 Quest points
895	Global	Complete 150 Medium clue scrolls.	Complete 150 medium clue scrolls.	N/A
898	Global	Complete 75 Hard clue scrolls.	Complete 75 hard clue scrolls.	N/A
899	Global	Complete 150 Hard clue scrolls.	Complete 150 hard clue scrolls.	N/A
902	Global	Collect 25 unique items for the Easy clue rewards collection log.	Collect 25 unique items for the easy clue rewards collection log.	N/A
903	Global	Collect 50 unique items for the Easy clue rewards collection log.	Collect 50 unique items for the easy clue rewards collection log.	N/A
906	Global	Collect 25 unique items for the Medium clue rewards collection log.	Collect 25 unique items for the medium clue rewards collection log.	N/A
907	Global	Collect 50 unique items for the Medium clue rewards collection log.	Collect 50 unique items for the Medium clue rewards collection log.	N/A
909	Global	Collect 10 unique items for the Hard clue rewards collection log.	Collect 10 unique items for the hard clue rewards collection log.	N/A
910	Global	Collect 25 unique items for the Hard clue rewards collection log.	Collect 25 unique items for the easy clue rewards collection log.	N/A
914	Global	Equip any Dragon mask.	Equip any dragon mask.	N/A
915	Global	Make any Perfect Juju Potion.	Make any perfect juju potion.	75 Herblore
916	Global	Make 15 Antifire Potions.	Make 15 antifire potions.	69 Herblore
917	Global	Clean 50 Grimy Cadantine.	Clean 50 grimy cadantine.	65 Herblore
918	Global	Clean 100 Grimy Lantadyme.	Clean 100 grimy lantadyme.	67 Herblore
919	Global	Clean 100 Dwarf Weed.	Clean 100 grimy dwarf weed.	70 Herblore
920	Global	Clean 100 Arbuck.	Clean 100 grimy arbuck.	77 Herblore, 77 Farming
921	Global	Equip a Yew shortbow.	Equip a yew shortbow.	40 Ranged
922	Global	Equip a Magic shortbow.	Equip a magic shortbow.	50 Ranged
923	Global	Fletch some Broad Arrows or Bolts.	Fletch some broad arrows or bolts.	52 Fletching, Completion of Smoking Kills, 300 slayer points
924	Global	Fletch 100 Yew shortbows (unstrung).	Fletch 100 Yew shortbows (unstrung).	65 Fletching
925	Global	Fletch 100 Yew stocks.	Fletch 100 yew stocks.	69 Fletching
926	Global	Fletch a Rune Crossbow.	Fletch a rune crossbow.	69 Fletching
927	Global	Fletch 35 or more arrow shafts from a single log.	Fletch 35 or more arrow shafts from a single log.	60 Fletching, Yew logs or higher
928	Global	Fletch 500 Adamant arrows.	Fletch 500 adamant arrows.	60 Fletching
929	Global	Fletch 750 Rune arrows.	Fletch 750 rune arrows.	75 Fletching
930	Global	Fletch 75 Onyx bolts.	Fletch 75 onyx bolts.	73 Fletching
931	Global	Equip a Rune Ceremonial Sword.	Equip a rune ceremonial sword.	N/A
932	Global	Equip a full set of the Blacksmith's outfit.	Equip a full set of the blacksmith's outfit.	1 Smithing, Total of 250% Artisans' Workshop respect
933	Global	Power up the Artisan's Workshop with a Luminite Injector.	Power up the Artisan's Workshop with a luminite Injector.	1 Smithing, 100% Artisans' Workshop respect
934	Global	Mine 50 Orichalcite Ore.	Mine 50 orichalcite ore.	60 Mining
935	Global	Mine 50 Drakolith.	Mine 50 drakolith.	60 Mining
936	Global	Mine 60 Necrite Ore.	Mine 60 necrite ore.	70 Mining
937	Global	Mine 60 Phasmatite.	Mine 60 phasmatite.	70 Mining
938	Global	Harvest 20 Grimy Kwuarm.	Harvest 20 grimy kwuarm.	56 Farming
939	Global	Catch 100 Shark.	Catch 100 raw sharks.	76 Fishing (or 68 Fishing via swarm fishing)
940	Global	Catch 100 Green Blubber Jellyfish.	Catch 100 raw green blubber jellyfish.	68 Fishing
941	Global	Catch a Spirit Impling.	Catch a spirit impling. Cannot be completed in Puro-Puro.	54 Hunter
942	Global	Equip a Slayer helmet.	Equip a Slayer helmet.	55 Crafting, 35 Slayer, Completion of Smoking Kills, 400 slayer points. Note: This task requires the Full slayer helmet and therefore has an implicit requirement of 77 Slayer for Desert Strykewyrms.
944	Global	Complete a Soul Reaper task.	Complete a Soul Reaper task.	N/A
945	Global	Complete 5 Soul Reaper tasks.	Complete 5 Soul Reaper tasks.	N/A
947	Global	Equip a full set of Orikalkum armour.	Equip a full set of orikalkum armour.	60 Smithing, 60 Defence
948	Global	Equip a full set of Necronium armour.	Equip a full set of necronium armour.	70 Smithing, 70 Defence
949	Global	Equip a full set of Black Dragonhide armour.	Equip a full set of black dragonhide armour.	60 Defence, 60 Crafting unless getting the pieces as a drop
950	Global	Equip a full set of Royal Dragonhide armour.	Equip a full set of royal dragonhide armour.	65 Defence, 65 Crafting
951	Global	Cast a Wave spell.	Cast a wave spell.	62 Magic
952	Global	Burn 75 Yew logs.	Burn 75 yew logs.	60 Firemaking
953	Global	Unlock the Ring of Quests from May's Quest Caravan.	Unlock the Ring of Quests from May's Quest Caravan.	75 Quest points
954	Global	Complete 250 clues of any tier.	Complete 250 clues of any tier.	N/A
955	Global	Complete 500 clues of any tier.	Complete 500 clues of any tier.	N/A
956	Global	Complete an Elite clue scroll.	Complete an elite clue scroll.	N/A
957	Global	Complete 25 Elite clue scrolls.	Complete 25 elite clue scrolls.	N/A
960	Global	Complete a Master clue scroll.	Complete a master clue scroll.	N/A
964	Global	Collect 5 unique items for the Elite clue rewards collection log.	Collect 5 unique items for the elite clue rewards collection log.	N/A
965	Global	Collect 10 unique items for the Elite clue rewards collection log.	Collect 10 unique items for the elite clue rewards collection log.	N/A
966	Global	Collect 20 unique items for the Elite clue rewards collection log.	Collect 20 unique items for the elite clue rewards collection log.	N/A
968	Global	Collect 5 unique items for the Master clue rewards collection log.	Collect 5 unique items for the master clue rewards collection log.	N/A
1002	Global	Catch a Manta ray.	Catch a raw manta ray.	81 Fishing (or 68 Fishing via swarm fishing)
1101	Global	Reach level 70 in any skill.	Reach level 70 in any skill.	Any skill at level 70
1102	Global	Reach level 80 in any skill.	Reach level 80 in any skill.	Any skill at level 80
1106	Global	Reach at least level 40 in all non-elite skills.	Reach at least level 40 in all non-elite skills.	All skills except Invention at level 40
1107	Global	Reach at least level 60 in all non-elite skills.	Reach at least level 60 in all non-elite skills.	All skills except Invention at level 60
1108	Global	Reach at least level 70 in all non-elite skills.	Reach at least level 70 in all non-elite skills.	All skills except Invention at level 70
435	Ardougne	Throw coins into the deep sea whirlpool.	Throw some gold coins into the whirlpool at the Deep Sea Fishing platform.	68 Fishing
436	Ardougne	Solve the Archaeology mystery: Leap of Faith.	Solve the Leap of Faith Archaeology mystery.	70 Archaeology
437	Ardougne	Collect all breeds of chinchompa at the Player Owned Farm.	Breed all types of chinchompas.	54 Farming, 20 Construction, 97 Hunter to catch crystal chinchompas.
438	Ardougne	Equip one piece of the Fishing outfit.	Equip one piece of the fishing outfit.	1 Fishing, 140 fishing tokens
439	Ardougne	Defeat the Penance Queen.	Defeat the Penance Queen.	N/A
440	Ardougne	Pickpocket a Hero.	Pickpocket a hero.	80 Thieving
441	Ardougne	Catch 50 Red Chinchompas in Kandarin.	Catch 50 carnivorous chinchompas in Kandarin.	63 Hunter
442	Feldip	Equip an Ogre Expert hat.	Equip an ogre expert hat.	1,000 chompy bird kills
443	Piscatoris	Catch a Monkfish.	Catch a raw monkfish.	62 Fishing (or 68 Fishing via swarm fishing)
444	Piscatoris	Recover all data for one memory-storage bot in the Hall of Memories.	Recover all data for memory-storage bot (Aagi) in the Hall of Memories.	70 Divination
445	Seers	Use the Piety Prayer.	Use the Piety prayer.	60 Prayer, 65 Defence, Completion of Knight Waves training ground
446	Ardougne	Complete the task set: Hard Ardougne.	Complete the Hard Ardougne achievements.	See Hard Ardougne achievements page
601	Karamja	Use the stepping stone across the river in Shilo village.	Use the stepping stones Agility Shortcut in Shilo Village.	74 Agility, Completion of Shilo Village
602	Karamja	Equip a full set of Obsidian armour.	Equip a full set of obsidian armour.	60 Defence, Completion of The Brink of Extinction, 80 Smithing
603	Karamja	Equip a Red Topaz Machete.	Equip a red topaz machete.	N/A
604	Karamja	Find a Gout Tuber.	Find a gout tuber.	10 Woodcutting, Completion of Jungle Potion
605	Karamja	Defeat TzTok-Jad.	Defeat TzTok-Jad once.	N/A
606	Karamja	Defeat TzTok-Jad. (25 times)	Defeat TzTok-Jad 25 times.	N/A
607	Karamja	Use your fire cape on TzTok-Jad before defeating them.	Use your fire cape on TzTok-Jad before defeating them.	N/A
608	Karamja	Equip a Fire Cape.	Equip a fire cape.	N/A
609	Karamja	Defeat TokHaar-Hok in the Fight Cauldron minigame using only obsidian equipment.	Defeat TokHaar-Hok in the Fight Cauldron minigame using only obsidian equipment.	60 Defence and one of 60 Attack, 60 Strength, 60 Magic, or 60 Ranged, Completion of The Brink of Extinction
610	Karamja	Repair the fairy ring inside the Kharazi jungle.	Repair the fairy ring inside the Kharazi jungle.	Partial completion of Legends' Quest, 5 bittercap mushrooms
611	Karamja	Access the Gemstone cavern.	Access the gemstone cavern.	Hard Karamja achievements and either an uncut dragonstone or a gemstone dragon Slayer task (requires 95 Slayer)
612	Karamja	Catch a Draconic jadinko at Herblore Habitat.	Catch a draconic jadinko at Herblore Habitat.	80 Hunter
613	Karamja	Craft a Bolas.	Craft a bolas.	87 Fletching, 80 Slayer
614	Karamja	Complete the task set: Hard Karamja.	Complete the Hard Karamja achievements.	See Hard Karamja achievements page
615	Karamja	Collect 60 Agility Arena tickets from the Brimhaven Agility Arena.	Receive 60 Agility Arena tickets.	1 Agility
617	Karamja	Defeat TzTok-Jad in less than 45:00.	Defeat TzTok-Jad in less than 45:00.	N/A
618	Karamja	Complete the Fight Kiln.	Complete the Fight Kiln.	Completion of The Elder Kiln, hand in a fire cape
620	Karamja	Equip a TokHaar-Kal-Ket.	Equip a TokHaar-Kal-Ket.	Completion of The Elder Kiln, hand in a fire cape (once)
621	Karamja	Equip a TokHaar-Kal-Xil.	Equip a TokHaar-Kal-Xil.	Completion of The Elder Kiln, hand in a fire cape (once)
622	Karamja	Equip a TokHaar-Kal-Mej.	Equip a TokHaar-Kal-Mej.	Completion of The Elder Kiln, hand in a fire cape (once)
623	Karamja	Equip a TokHaar-Kal-Mor.	Equip a TokHaar-Kal-Mor.	Completion of The Elder Kiln, hand in a fire cape (once)
624	Karamja	Complete the Fight Kiln and collect an uncut onyx.	Complete the Fight Kiln and collect an uncut onyx.	Completion of The Elder Kiln, hand in a fire cape (once)
629	Karamja	Complete all TzTok-Jad combat achievements.	Complete all TzTok-Jad combat achievements.	See TzTok-Jad achievements page
10	Draynor	Siphon from a death esswraith in the RuneSpan.	Siphon from a death esswraith in the RuneSpan.	66 Runecrafting
12	Draynor	Obtain the Massive Pouch from the RuneSpan.	Obtain the massive pouch from the RuneSpan.	90 Runecrafting, 1,000 Runespan points
14	Draynor	Equip the full Master Runecrafter skilling outfit.	Equip the full master runecrafter robes set.	50 Runecrafting, 60,000 Runecrafting guild tokens, 16,000 Runespan points, or 2,000 thaler
18	Edgeville	Complete the task set: Hard Varrock.	Complete all of the Hard Varrock achievements and claim rewards from Vannaka in Edgeville.	See Hard Varrock achievements page
19	Edgeville	Make a waka canoe near Edgeville.	Make a waka canoe near Edgeville.	57 Woodcutting
20	Edgeville	Chop down the Edgeville elder tree.	Chop down the Edgeville elder tree.	90 Woodcutting
24	Fort Forinthry	Upgrade the workshop in Fort Forinthry to Tier 3.	Upgrade the workshop in Fort Forinthry to tier 3.	75 Construction, Completion of New Foundations
31	Lumbridge	Enter Zanaris via Lumbridge Swamp.	Enter Zanaris via Lumbridge Swamp.	Partial completion of Lost City
55	Lumbridge	Complete the task set: Hard Lumbridge.	Complete all Hard Tasks in Lumbridge and claim rewards from Ned in Draynor Village.	See Hard Lumbridge achievements page
56	Lumbridge	Unlock the Bladed Dive ability from Shattered Worlds.	Unlock the Bladed Dive ability from Shattered Worlds.	63,000,000 shattered anima
57	Lumbridge	Smith a mithril platebody on the anvil in the jailhouse sewers.	Smith a mithril platebody on the anvil in Draynor Sewers.	30 Smithing
58	Lumbridge	Fully grow a magic tree in Lumbridge.	Fully grow a magic tree in Lumbridge.	75 Farming
75	City of Um	Defeat Hermod, the Spirit of War.	Defeat Hermod, the Spirit of War once.	Completion of The Spirit of War
76	City of Um	Defeat Hermod, the Spirit of War. (100 times)	Defeat Hermod, the Spirit of War 100 times.	Completion of The Spirit of War
77	City of Um	Rest whilst listening to the Dead Beats in the City of Um.	Rest whilst listening to the Dead Beats in the City of Um.	Completion of That Old Black Magic
78	City of Um	Smelt a necronium bar at the smithy in the City of Um.	Smelt a necronium bar at the smithy in the City of Um.	70 Smithing, Partial completion of Necromancy!
79	City of Um	Create a passing bracelet, performing each step in the City of Um.	Create a passing bracelet, performing each step in the City of Um.	60 Necromancy for bar, 79 Crafting, 68 Magic, Ensouled bar, moonstone, runes for Lvl-5 Enchant.
80	City of Um	Catch a ghostly impling while wearing a full set of ghostly robes.	Catch a ghostly impling while wearing a full set of ghostly robes.	68 Hunter, Completion of The Curse of Zaros (miniquest)
81	City of Um	Upgrade a set of Death Skull equipment to tier 70.	Upgrade a set of Death Skull equipment to tier 70.	70 Necromancy, Completion of The Spirit of War. See also Kili's Knowledge V.
82	City of Um	Complete a Powerful Communion ritual.	Complete a powerful communion ritual.	90 Necromancy
83	City of Um	Conjure an undead army at the City of Um ritual site.	Conjure an undead army at the Um ritual site.	99 Necromancy, Conjure Undead Army unlocked in the Well of Souls.
Elite Tasks (200 Points each)
Task ID	Locality	Task	Information	Requirements
489	Anachronia	Discover all the totem pieces on Anachronia.	Discover all the totem pieces on Anachronia.	90 Slayer, 81 Woodcutting, 75 Hunter, 55 Slayer, 45 Construction, 42 Farming, 40 Mining, 30 Agility, Completion of Desperate Measures, Completion of Helping Laniakea (miniquest)
491	Anachronia	Unlock the double Surge or double Escape ability upgrade.	Unlock the double Surge or double Escape ability upgrade.	30 Agility (minimum, 85 Agility for best efficiency by running laps)
494	Anachronia	Harvest a Dragonfruit plant in the cactus patch in the north of Anachronia.	Harvest a dragonfruit cactus in the cactus patch in the north of Anachronia.	95 Farming
495	Anachronia	Kill 50 Dinosaurs.	Kill 50 dinosaurs.	90 Slayer
496	Anachronia	Kill 50 Vile Blooms.	Kill 50 vile blooms.	90 Slayer
497	Anachronia	Solve the Archaeology mystery: Teleport Node On.	Activate all Orthen teleportation devices on Anachronia.	90 Archaeology, 70 Runecrafting, 70 Crafting, 70 Divination, Completion of the Incomplete Portal Network III research
498	Anachronia	Use Potterington Blend #102 Fertiliser or dinosaur 'propellant' on Prehistoric Potterington.	Use Potterington blend 102 fertiliser or dinosaur 'propellant' on Prehistoric Potterington.	95 Firemaking
499	Anachronia	Find an unchecked egg in the pile of dinosaur eggs south of Anachronia dinosaur farm.	Find a dinosaur egg in the pile of dinosaur eggs on Anachronia Farm.	87 Firemaking
501	Anachronia	Defeat Raksha, the Shadow Colossus. (100 times)	Defeat Raksha, the Shadow Colossus 100 times.	Completion of Raksha, the Shadow Colossus (quest)
502	Anachronia	Complete the quest: Desperate Measures.	Complete the Desperate Measures quest.	See quest page
503	Anachronia	Equip a Terrasaur maul.	Equip a terrasaur maul.	80 Strength, 96 Hunter, 76 Slayer
505	Anachronia	Complete a big game encounter without stepping into the creature's vision ring.	Complete a Big Game Hunter encounter without stepping into the creature's vision ring.	75 Hunter, 55 Slayer
508	Anachronia	Craft 500 Time Runes.	Craft 500 time runes.	100 Runecrafting (unless bypassed via Ourania Altar or wild runes)
509	Anachronia	Solve the Archaeology mystery: Fragmented Memories.	Complete the Fragmented Memories Archaeology mystery.	108 Archaeology, 86 Hunter
512	Anachronia	Fletch any type of Elder God arrow.	Fletch any type of Elder God arrow.	95 Fletching, 95 Firemaking
513	Anachronia	Cast the Crumble Undead spell.	Cast the Crumble Undead spell.	78 Magic
238	Falador	Complete the task set: Elite Falador.	Complete the Elite Falador achievements.	See Elite Falador achievements page
239	Falador	Complete the Invention tutorial.	Complete the Invention tutorial.	80 Smithing, 80 Crafting, 80 Divination
240	Falador	Defeat Vorago, if you think you're hard enough.	Defeat Vorago.	N/A
241	Falador	Defeat Vorago, if you think you're hard enough. (50 times)	Defeat Vorago 50 times.	N/A
242	Falador	Equip a seismic wand or seismic singularity.	Equip a seismic wand or singularity.	90 Magic
243	Falador	Harvest some starbloom flowers from the flower patch south of Falador.	Harvest some starbloom flowers from the flower patch south of Falador.	100 Farming
244	Falador	Unlock the Royale Cannon from the Artisans' Workshop reward shop.	Unlock the royale dwarf multicannon from the Artisans' Workshop Reward Shop.	1 Smithing, 150% cumulative Artisans' Workshop respect
245	Falador	Equip a piece of masterwork melee armour.	Equip a piece of masterwork melee armour.	99 Smithing, 90 Defence, Completion of It Should Have Been Called Aetherium
255	Burthorpe	Equip a full set of Bandos armour.	Equip a full set of Bandos armour.	70 Defence, 70 Strength, Partial completion of Troll Stronghold
256	Burthorpe	Equip a full set of Armadyl armour.	Equip a full set of Armadyl armour.	70 Defence, 70 Ranged, Partial completion of Troll Stronghold
257	Burthorpe	Equip a full set of subjugation armour.	Equip a full set of subjugation armour.	70 Defence, 70 Constitution, Partial completion of Troll Stronghold
258	Burthorpe	Equip a piece of Torva, Pernix or Virtus armour.	Equip a piece of Torva, Pernix or Virtus armour.	80 Constitution, 80 Defence, 70 Ranged, 70 Strength, 70 Agility, Partial completion of Troll Stronghold
259	Burthorpe	Defeat Nex, the Angel of Death.	Kill Nex: Angel of Death.	70 Constitution, 70 Ranged, 70 Strength, 70 Agility, Partial completion of Troll Stronghold
260	Burthorpe	Defeat Nex, the Angel of Death. (50 times)	Kill Nex: Angel of Death 50 times.	70 Constitution, 70 Ranged, 70 Strength, 70 Agility, Partial completion of Troll Stronghold
267	Port Sarim	Kill a living wyvern.	Kill a wyvern.	96 Slayer
327	Desert	Complete the task set: Elite Desert.	Complete the Elite Desert achievements.	See Elite Desert achievements page
329	Desert	Defeat Telos, the Warden at 100% enrage.	Defeat Telos, the Warden at 100% enrage.	80 Attack, 80 Prayer, 80 Magic, 80 Ranged
330	Desert	Defeat Telos, the Warden at 500% enrage.	Defeat Telos, the Warden at 500% enrage.	80 Attack, 80 Prayer, 80 Magic, 80 Ranged
331	Menaphos	Craft some Soul runes.	Craft some soul runes.	90 Runecrafting, Completion of 'Phite Club
332	Desert	Defeat a Camel Warrior.	Defeat a camel warrior.	96 Slayer
333	Desert	Escape Kharid-et by boat.	Complete the Aquatic Escape achievement.	86 Archaeology, Partial completion of The Vault of Shadows quest or mystery
334	Desert	Defeat the Kalphite King solo.	Kill the Kalphite King solo.	N/A
335	Desert	Cast Ice Barrage in the desert.	Cast Ice Barrage in the desert.	94 Magic, Completion of Desert Treasure unless tier 6 reached
337	Desert	Craft a Zaros godsword, Seren godbow or staff of Sliske.	Craft a Zaros godsword, Seren godbow or staff of Sliske.	92 Crafting, 80 Attack, 80 Prayer, 80 Magic, 80 Ranged
1112	Menaphos	Defeat Amascut, the Devourer.	Defeat Amascut, the Devourer.	Completion of Eclipse of the Heart unless tier 5 reached
387	Lunar Isles	Cast Spellbook Swap from the Lunar spellbook.	Cast Spellbook Swap from the lunar spellbook.	96 Magic, Completion of Dream Mentor unless tier 6 reached
389	Fremennik	Equip Every Dagannoth King Ring.	Equip every Dagannoth King ring.	N/A
390	Fremennik	Equip a Completed God Book.	Equip a completed god book.	Completion of Horror from the Deep
391	Fremennik	Defeat 20 Acheron Mammoths.	Defeat 20 acheron mammoths.	96 Slayer
394	Fremennik	Cast the Paradox spell on any tree, rock, fishing spot, or box trap.	Cast the Paradox spell on any tree, rock, fishing spot, or box trap.	88 Magic, 100 Runecrafting (unless bypassed via Ourania Altar or Wild Runes)
395	Fremennik	Build a Demonic Throne.	Build a demonic throne.	99 Construction
397	Lunar Isles	Perform a Powerful Necroplasm ritual at the Ungael ritual site.	Perform a powerful necroplasm ritual at the Ungael ritual site.	90 Necromancy, Completion of Requiem for a Dragon
398	Fremennik	Defeat the Abomination once after Hero's Welcome.	Defeat the Abomination once after Hero's Welcome.	Completion of Hero's Welcome
399	Fremennik	Summon a Pack Mammoth.	Summon a pack mammoth.	96 Slayer, 99 Summoning
400	Fremennik	Complete the task set: Elite Fremennik.	Complete the Elite Fremennik achievements.	See Elite Fremennik achievements page
401	Fremennik	Complete the Ungael combat activity on hard mode.	Complete the Ungael combat activity on hard mode.	Completion of Ancient Awakening
402	Fremennik	Use the Trap Telekinesis spell to catch Azure Skillchompas 25 times.	Use the Trap Telekinesis spell to catch azure skillchompas 25 times.	97 Magic, 68 Hunter, Completion of Lunar Diplomacy unless tier 6 reached
140	Global	Reach maximum combat level.	Reach maximum combat level.	152 Combat
145	Global	Reach total level 2000.	Reach total level 2000.	2000 Total level
821	Global	Complete 50 Slayer tasks.	Complete 50 Slayer tasks.	1 Slayer
822	Global	Complete 75 Slayer tasks.	Complete 75 Slayer tasks.	1 Slayer
890	Global	Obtain 125 Quest Points.	Obtain 125 quest points.	125 Quest points
911	Global	Collect 75 unique items for the Hard clue rewards collection log.	Collect 75 unique items for the hard clue rewards collection log.	N/A
946	Global	Complete 10 Soul Reaper tasks.	Complete 10 Soul Reaper tasks.	N/A
958	Global	Complete 75 Elite clue scrolls.	Complete 75 elite clue scrolls.	N/A
959	Global	Complete 150 Elite clue scrolls.	Complete 150 elite clue scrolls.	N/A
961	Global	Complete 25 Master clue scrolls.	Complete 25 master clue scrolls.	N/A
962	Global	Complete 75 Master clue scrolls.	Complete 75 master clue scrolls.	N/A
967	Global	Collect 35 unique items for the Elite clue rewards collection log.	Collect 35 unique items for the elite clue rewards collection log.	N/A
969	Global	Collect 10 unique items for the Master clue rewards collection log.	Collect 10 unique items for the master clue rewards collection log.	N/A
970	Global	Collect 15 unique items for the Master clue rewards collection log.	Collect 15 unique items for the master clue rewards collection log.	N/A
971	Global	Collect 30 unique items for the Master clue rewards collection log.	Collect 30 unique items for the master clue rewards collection log.	N/A
972	Global	Make 25 Powerburst Potions.	Make 25 powerbursts.	103 Herblore, 95 Farming
973	Global	Make 25 Bomb Potions.	Make 25 bomb potions.	99 Herblore, 95 Farming
974	Global	Make 5 Perfect Plus Potions.	Make 5 perfect plus potions.	99 Herblore, 94 Farming, 89 Crafting, 81 Mining, Completion of As a First Resort
975	Global	Make 15 Overload Potions.	Make 15 overloads.	96 Herblore
976	Global	Make a Spiritual Prayer Potion.	Make a spiritual prayer potion.	110 Herblore, 95 Farming, 89 Crafting, 81 Mining, Completion of As a First Resort
977	Global	Fletch 200 Magic stocks.	Fletch 200 magic stocks.	92 Fletching
978	Global	Fletch 750 Elder arrow shafts.	Fletch 750 elder arrow shafts.	90 Fletching, 90 Woodcutting
979	Global	Fletch 20 Elder shortbow (unstrung)	Fletch 20 unstrung elder shortbows.	90 Fletching, 90 Woodcutting
980	Global	Fletch an Eternal magic shortbow (Martial) or Primal crossbow (martial).	Fletch an eternal magic shortbow (martial) or primal crossbow (martial).	100 Fletching, 100 Woodcutting
981	Global	Fletch 1,000 Eternal magic shafts.	Fletch 1,000 eternal magic shafts.	100 Fletching, 100 Woodcutting
982	Global	Fletch 1,500 Primal arrows.	Fletch 1,500 primal arrows.	100 Fletching, 100 Woodcutting, 100 Smithing
983	Global	Fletch an Eternal Magic Wood Box.	Fletch an eternal magic wood box.	100 Fletching
984	Global	Fletch 350 Rune darts.	Fletch 350 rune darts.	81 Fletching, 50 Smithing, Completion of The Tourist Trap
985	Global	Smith a Primal Ore Box.	Smith a primal ore box.	100 Smithing
986	Global	Smith 10,000 Armour Spikes.	Smith 10,000 armour spikes.	90 Smithing
987	Global	Smith 10,000 Primal Armour Spikes.	Smith 10,000 primal armour spikes.	100 Smithing
988	Global	Mine each of the 10 ores on the surface of the Daemonheim peninsula in under 5 minutes.	Mine each of the 10 ores on the surface of the Daemonheim peninsula in under 5 minutes.	100 Mining
989	Global	Mine 70 Banite Ore.	Mine 70 banite ore.	80 Mining
990	Global	Mine 100 Dark or Light Animica.	Mine 100 dark or light animica.	90 Mining
991	Global	Open 10 Metamorphic Geodes.	Open 10 metamorphic geodes. These are found randomly while mining from rocks which require at least level 60 Mining.	60 Mining
992	Global	Harvest 20 Grimy Kwuarm.	Harvest 20 grimy kwuarm.	56 Farming
993	Global	Harvest 50 Grimy Fellstalk.	Harvest 50 grimy fellstalk.	91 Farming
994	Global	Plant an Avocado seed in a bush patch.	Plant an avocado seed in a bush patch.	99 Farming
995	Global	Harvest 20 Lychee.	Harvest 20 lychee.	111 Farming
996	Global	Harvest 24 Starbloom Flowers.	Harvest 24 starbloom flowers.	100 Farming
997	Global	Catch 150 Rocktail.	Catch 150 raw rocktails.	90 Fishing (or 79 Fishing via swarm fishing)
998	Global	Catch 200 Sailfish.	Catch 200 raw sailfish.	97 Fishing (or 81 Fishing via swarm fishing)
999	Global	Catch 150 Blue Blubber Jellyfish.	Catch 150 raw blue blubber jellyfish.	91 Fishing (or 80 Fishing via swarm fishing)
1000	Global	Obtain the highest boost available in the 'Fishing Frenzy' activity.	Obtain the highest boost available in the 'Fishing Frenzy' activity at Deep Sea Fishing.	94 Fishing
1001	Global	Catch a Cavefish.	Catch a raw cavefish.	85 Fishing (or 75 Fishing via swarm fishing)
1003	Global	Manually bury or scatter each of the listed bones and ashes.	Complete the Bury All achievement.	94 Slayer, Completion of Zogre Flesh Eaters, Ritual of the Mahjarrat, Fate of the Gods, and partial completion of Tai Bwo Wannai Trio
1004	Global	Activate Soul Split prayer.	Activate Soul Split prayer.	92 Prayer, Tier 5 passive effect or completion of The Temple at Senntisten
1005	Global	Catch a Dragon Impling.	Catch a dragon impling. Cannot be completed in Puro-Puro.	83 Hunter
1006	Global	Catch a Kingly Impling.	Catch a kingly impling. Cannot be completed in Puro-Puro.	91 Hunter
1007	Global	Equip a full set of Bane armour.	Equip a full set of bane armour.	80 Smithing, 80 Mining, 80 Defence
1008	Global	Equip a full set of Elder Rune armour.	Equip a full set of elder rune armour.	90 Smithing, 90 Mining, 90 Defence
1009	Global	Cast a Surge spell.	Cast a Surge spell.	81 Magic
1010	Global	Burn 100 Magic Logs	Burn 100 magic logs	75 Firemaking
1011	Global	Burn 10 Elder logs.	Burn 10 elder logs.	90 Firemaking
1012	Global	Reach level 99 in the Agility skill.	Reach level 99 Agility.	99 Agility
1013	Global	Reach level 99 in the Archaeology skill.	Reach level 99 Archaeology.	99 Archaeology
1014	Global	Reach level 99 in the Attack skill.	Reach level 99 Attack.	99 Attack
1015	Global	Reach level 99 in the Construction skill.	Reach level 99 Construction.	99 Construction
1016	Global	Reach level 99 in the Cooking skill.	Reach level 99 Cooking.	99 Cooking
1017	Global	Reach level 99 in the Crafting skill.	Reach level 99 Crafting.	99 Crafting
1018	Global	Reach level 99 in the Defence skill.	Reach level 99 Defence.	99 Defence
1019	Global	Reach level 99 in the Divination skill.	Reach level 99 Divination.	99 Divination
1020	Global	Reach level 99 in the Dungeoneering skill.	Reach level 99 Dungeoneering.	99 Dungeoneering
1021	Global	Reach level 99 in the Farming skill.	Reach level 99 Farming.	99 Farming
1022	Global	Reach level 99 in the Firemaking skill. (Where arson is its own reward.)	Reach level 99 Firemaking.	99 Firemaking
1023	Global	Reach level 99 in the Fishing skill.	Reach level 99 Fishing.	99 Fishing
1024	Global	Reach level 99 in the Fletching skill.	Reach level 99 Fletching.	99 Fletching
1025	Global	Reach level 99 in the Herblore skill.	Reach level 99 Herblore.	99 Herblore
1026	Global	Reach level 99 in the Constitution skill.	Reach level 99 Constitution.	99 Constitution
1027	Global	Reach level 99 in the Hunter skill.	Reach level 99 Hunter.	99 Hunter
1028	Global	Reach level 99 in the Invention skill.	Reach level 99 Invention.	99 Invention
1029	Global	Reach level 99 in the Magic skill.	Reach level 99 Magic.	99 Magic
1030	Global	Reach level 99 in the Mining skill.	Reach level 99 Mining.	99 Mining
1031	Global	Reach level 99 in the Necromancy skill.	Reach level 99 Necromancy.	99 Necromancy
1032	Global	Reach level 99 in the Prayer skill.	Reach level 99 Prayer.	99 Prayer
1033	Global	Reach level 99 in the Ranged skill.	Reach level 99 Ranged.	99 Ranged
1034	Global	Reach level 99 in the Runecrafting skill.	Reach level 99 Runecrafting.	99 Runecrafting
1035	Global	Reach level 99 in the Slayer skill.	Reach level 99 Slayer.	99 Slayer
1036	Global	Reach level 99 in the Smithing skill.	Reach level 99 Smithing.	99 Smithing
1037	Global	Reach level 99 in the Strength skill.	Reach level 99 Strength.	99 Strength
1038	Global	Reach level 99 in the Summoning skill.	Reach level 99 Summoning.	99 Summoning
1039	Global	Reach level 99 in the Thieving skill.	Reach level 99 Thieving.	99 Thieving
1040	Global	Reach level 99 in the Woodcutting skill.	Reach level 99 Woodcutting.	99 Woodcutting
1041	Global	Reach level 110 in the Mining skill.	Reach level 110 Mining.	110 Mining
1042	Global	Reach level 110 in the Smithing skill.	Reach level 110 Smithing.	110 Smithing
1043	Global	Reach level 110 in the Crafting skill.	Reach level 110 Crafting	110 Crafting
1044	Global	Reach level 110 in the Firemaking skill.	Reach level 110 Firemaking.	110 Firemaking
1045	Global	Reach level 110 in the Fletching skill.	Reach level 110 Fletching.	110 Fletching
1046	Global	Reach level 110 in the Woodcutting skill.	Reach level 110 Woodcutting.	110 Woodcutting
1047	Global	Reach level 110 in the Runecrafting skill.	Reach level 110 Runecrafting.	110 Runecrafting
1048	Global	Reach level 120 in the Dungeoneering skill.	Reach level 120 Dungeoneering.	120 Dungeoneering
1049	Global	Reach level 120 in the Farming skill.	Reach level 120 Farming.	120 Farming
1050	Global	Reach level 120 in the Herblore skill.	Reach level 120 Herblore.	120 Herblore
1051	Global	Reach level 120 in the Slayer skill.	Reach level 120 Slayer.	120 Slayer
1052	Global	Reach level 120 in the Invention skill.	Reach level 120 Invention.	120 Invention
1053	Global	Reach level 120 in the Archaeology skill.	Reach level 120 Archaeology	120 Archaeology
1054	Global	Reach level 120 in the Necromancy skill.	Reach level 120 Necromancy.	120 Necromancy
1055	Global	Obtain 50 Million Agility XP.	Obtain 50 million Agility XP.	112 Agility
1056	Global	Obtain 50 Million Construction XP.	Obtain 50 million Construction XP.	112 Construction
1057	Global	Obtain 50 Million Cooking XP.	Obtain 50 million Cooking XP.	112 Cooking
1058	Global	Obtain 50 Million Crafting XP.	Obtain 50 million Crafting XP.	112 Crafting
1059	Global	Obtain 50 Million Farming XP.	Obtain 50 million Farming XP.	112 Farming
1060	Global	Obtain 50 Million Firemaking XP.	Obtain 50 million Firemaking XP.	112 Firemaking
1061	Global	Obtain 50 Million Fishing XP.	Obtain 50 million Fishing XP.	112 Fishing
1062	Global	Obtain 50 Million Fletching XP.	Obtain 50 million Fletching XP.	112 Fletching
1063	Global	Obtain 50 Million Herblore XP.	Obtain 50 million Herblore XP.	112 Herblore
1064	Global	Obtain 50 Million Hunter XP.	Obtain 50 million Hunter XP.	112 Hunter
1065	Global	Obtain 50 Million Mining XP.	Obtain 50 million Mining XP.	112 Mining
1066	Global	Obtain 50 Million Prayer XP.	Obtain 50 million Prayer XP.	112 Prayer
1067	Global	Obtain 50 Million Runecrafting XP.	Obtain 50 million Runecrafting XP.	112 Runecrafting
1068	Global	Obtain 50 Million Slayer XP.	Obtain 50 million Slayer XP.	112 Slayer
1069	Global	Obtain 50 Million Smithing XP.	Obtain 50 million Smithing XP.	112 Smithing
1070	Global	Obtain 50 Million Thieving XP.	Obtain 50 million Thieving XP.	112 Thieving
1071	Global	Obtain 50 Million Woodcutting XP.	Obtain 50 million Woodcutting XP.	112 Woodcutting
1072	Global	Obtain 50 Million Dungeoneering XP.	Obtain 50 million Dungeoneering XP.	112 Dungeoneering
1073	Global	Obtain 50 Million Invention XP.	Obtain 50 million Invention XP.	112 Invention
1074	Global	Obtain 50 Million Divination XP.	Obtain 50 million Divination XP.	112 Divination
1075	Global	Obtain 50 Million Archaeology XP.	Obtain 50 million Archaeology XP.	112 Archaeology
1076	Global	Obtain 50 Million Attack XP.	Obtain 50 million Attack XP.	112 Attack
1077	Global	Obtain 50 Million Constitution XP.	Obtain 50 million Constitution XP.	112 Constitution
1078	Global	Obtain 50 Million Strength XP.	Obtain 50 million Strength XP.	112 Strength
1079	Global	Obtain 50 Million Defence XP.	Obtain 50 million Defence XP.	112 Defence
1080	Global	Obtain 50 Million Ranged XP.	Obtain 50 million Ranged XP.	112 Ranged
1081	Global	Obtain 50 Million Magic XP.	Obtain 50 million Magic XP.	112 Magic
1082	Global	Obtain 50 Million Summoning XP.	Obtain 50 million Summoning XP.	112 Summoning
1083	Global	Obtain 50 Million Necromancy XP.	Obtain 50 million Necromancy XP.	112 Necromancy
1084	Global	Complete 750 clues of any tier.	Complete 750 clues of any tier.	N/A
1085	Global	Complete 1000 clues of any tier.	Complete 1000 clues of any tier.	N/A
1086	Global	Make 5 Elder Overload Salve Potions.	Make 5 elder overload salves.	107 Herblore, 89 Crafting, 81 Mining
1087	Global	Equip an Eternal Magic shortbow.	Equip an eternal magic shortbow.	100 Woodcutting, 100 Fletching
1094	Global	Equip a full set of Primal armour.	Equip a full set of primal armour.	100 Mining, 100 Smithing, 99 Defence
1103	Global	Reach level 90 in any skill.	Reach level 90 in any skill.	Any skill at level 90
1104	Global	Reach level 95 in any skill.	Reach level 95 in any skill.	Any skill at level 95
1109	Global	Reach at least level 80 in all non-elite skills.	Reach at least level 80 in all non-elite skills.	All skills except Invention at level 80
1110	Global	Reach at least level 90 in all non-elite skills.	Reach at least level 90 in all non-elite skills.	All skills except Invention at level 90
447	Piscatoris	Help the Archivist recover all core memory data in the Hall of Memories.	Recover all core memory data in the Hall of Memories.	95 Divination
448	Piscatoris	Attune and hand all engrams in to the Memorial to Guthix.	Hand all engrams in to the Memorial to Guthix.	95 Divination, Completion of Lost City
449	Ardougne	Equip a dragon full helm.	Equip a dragon full helm.	60 Defence
450	Ardougne	Chop an Elder Tree until it no longer has logs remaining.	Chop an elder tree until it no longer has logs remaining.	90 Woodcutting
451	Ardougne	Obtain a Crystal Geode from a Crystal Tree.	Obtain a crystal geode from a crystal tree.	94 Woodcutting
452	Ardougne	Reach Howl's Workshop in the Stormguard Citadel.	Partial completion of the Howl's Floating Workshop mystery.	95 Archaeology or tier 4 reached
453	Feldip	Equip an Expert Dragon Archer hat.	Equip an Expert Dragon Archer hat.	2,250 chompy bird kills
454	Ardougne	Complete the task set: Elite Ardougne.	Complete the Elite Ardougne achievements.	See Elite Ardougne achievements page
455	Ardougne	Successfully breed a royal dragon.	Breed a royal dragon.	92 Farming
457	Ardougne	Defeat an Automaton after 'The World Wakes'.	Defeat an automaton after The World Wakes.	67 Slayer, Completion of The World Wakes, Ritual of the Mahjarrat, The Firemaker's Curse, The Branches of Darkmeyer, The Void Stares Back, and The Chosen Commander
459	Piscatoris	Mine 25 Platinum Ore south of Piscatoris Fishing Colony.	Mine 25 platinum ores south of Piscatoris Fishing Colony.	104 Mining
460	Piscatoris	Chop 50 Eternal Magic logs.	Chop 50 eternal magic logs.	100 Woodcutting
616	Karamja	Purchase an uncut onyx from Tzhaar-Hur-Lek's ore and gem store.	Purchase an uncut onyx from TzHaar-Hur-Lek's Ore and Gem Store.	2,700,000 Tokkul
619	Karamja	Defeat the Har-Aken. (10 times)	Defeat Har-Aken 10 times.	Completion of The Elder Kiln, hand in a fire cape (once)
625	Karamja	Defeat 10 gemstone dragons inside the Gemstone cavern.	Defeat 10 gemstone dragons inside the Gemstone cavern.	95 Slayer, Completion of the Hard Karamja achievements
626	Karamja	Equip a piece of Gemstone armour.	Equip a piece of gemstone armour.	95 Slayer, Completion of the Hard Karamja achievements
627	Karamja	Complete the task set: Elite Karamja.	Complete the Elite Karamja achievements.	See Elite Karamja achievements page
628	Karamja	Complete all Har-Aken combat achievements.	Complete all Har-Aken combat achievements.	Completion of The Elder Kiln
11	Draynor	Navigate the RuneSpan using a Greater Conjuration Platorm.	Navigate the RuneSpan using a greater conjuration platform.	95 Runecrafting
13	Draynor	Obtain the Greater Runic Staff from the RuneSpan.	Obtain the greater runic staff from the RuneSpan.	90 Runecrafting, 75 Magic
21	Edgeville	Complete the task set: Elite Varrock.	Given by Vannaka in Edgeville for completing all of the Elite Varrock achievements.	See Elite Varrock achievements page
25	Fort Forinthry	Upgrade the guardhouse in Fort Forinthry to Tier 3.	Upgrade the guardhouse in Fort Forinthry to tier 3.	95 Construction, Completion of Unwelcome Guests
59	Lumbridge	Defeat 150 tormented demons.	Defeat 150 tormented demons.	Completion of While Guthix Sleeps
60	Lumbridge	Equip a dragon crossbow.	Equip a dragon crossbow.	60 Ranged, 94 Fletching, Completion of While Guthix Sleeps
85	City of Um	Defeat Rasial, the First Necromancer.	Defeat Rasial, the First Necromancer once.	Completion of Alpha vs Omega
86	City of Um	Defeat Rasial, the First Necromancer. (100 times)	Defeat Rasial, the First Necromancer 100 times.	Completion of Alpha vs Omega
87	City of Um	Equip an Omni guard.	Equip an omni guard.	95 Necromancy, Completion of Alpha vs Omega
88	City of Um	Equip a Soulbound lantern.	Equip a soulbound lantern.	95 Necromancy, Alpha vs Omega
89	City of Um	Equip a full set of Robes of the First Necromancer.	Equip a full set of First Necromancer's equipment.	95 Necromancy, 95 Defence, Completion of Alpha vs Omega
90	City of Um	Give a blueberry pie to Thalmund in the City of Um.	Give a blueberry pie to Thalmund in the City of Um.	10 Cooking, 90 Defence, Completion of Kili's Knowledge VII, partial completion of A Fairy Tale II - Cure a Queen, completion of The Fremennik Trials
91	City of Um	Track 8 of the owls in the City of Um.	Track 8 of the owls in the City of Um. See Birds of Prey for details.	90 Necromancy, Completion of Housing of Parliament
92	Varrock	Defeat Croesus.	Defeat Croesus 1 time.	N/A
93	Varrock	Defeat Croesus. (100 times)	Defeat Croesus 100 times.	N/A
119	Varrock	Defeat Kerapac, the bound. (100 times)	Defeat Kerapac, the bound 100 times.	N/A
121	Varrock	Defeat the Arch-Glacor in hard mode. (100 times)	Defeat the Arch-Glacor in hard mode 100 times.	N/A
124	Varrock	Equip either a Dark Shard of Leng or a Dark Sliver of Leng.	Equip either a Dark Shard of Leng or a Dark Sliver of Leng.	95 Attack, 95 Smithing, 95 Crafting
125	Varrock	Craft 100 earth runes simultaneously without aid from an explorer's ring, pouches or familiars.	Craft 100 earth runes simultaneously without aid from an explorer's ring, pouches or familiars.	78 Runecrafting (As low as 26 Runecrafting if using elemental anima stones)
126	Varrock	Bake a summer pie in the Cooking Guild from scratch.	Bake a summer pie in the Cooking Guild from scratch.	95 Cooking
758	Varrock	Defeat TzKal-Zuk.	Defeat TzKal-Zuk once.	N/A
759	Varrock	Defeat TzKal-Zuk. (10 times)	Defeat TzKal-Zuk 10 times.	N/A
760	City of Um	Craft a soul rune at the soul altar with a soul cape equipped.	Craft a soul rune at the soul altar with a soul cape equipped.	90 Runecrafting, Completion of 'Phite Club, completion of Nomad's Elegy
761	City of Um	Upgrade a set of Death Skull equipment to tier 90.	Upgrade a set of Death Skull equipment to tier 90.	10 Cooking, 90 Defence, 90 Necromancy
763	City of Um	Defeat Nakatra, Devourer Eternal. (100 times)	Defeat Nakatra, Devourer Eternal 100 times.	Completion of Necromancy!, completion of Soul Searching
765	City of Um	Cleanse the Gate of Elidinis. (100 times)	Cleanse The Gate of Elidinis 100 times.	Completion of Ode of the Devourer (or Soul Searching if tier 4 reached)
769	City of Um	Complete the task set: Elite Underworld.	Complete the Elite Underworld achievements.	See Elite Underworld achievements page
735	Morytania	Defeat 30 Abyssal Demons.	Defeat 30 abyssal demons.	85 Slayer
736	Morytania	Harvest 200 radiant energy from Radiant Wisps.	Harvest 200 radiant energy from radiant wisps.	85 Divination
737	Morytania	Defeat 20 Celestial Dragons.	Defeat 20 celestial dragons.	Completion of One of a Kind. They can also be killed during the Dragonkin Laboratory without the quest requirement.
738	Morytania	Defeat Araxxi.	Defeat Araxxi once.	N/A
739	Morytania	Defeat Araxxi. (100 times)	Defeat Araxxi 100 times.	N/A
740	Morytania	Defeat the empowered Barrows Brothers.	Complete one Rise of the Six encounter.	N/A
741	Morytania	Defeat the empowered Barrows Brothers.	Complete 100 Rise of the Six encounters.	N/A
742	Morytania	Equip a Noxious Scythe.	Equip a noxious scythe.	90 Crafting, 90 Attack
743	Morytania	Equip a Noxious Staff.	Equip a noxious staff.	90 Crafting, 90 Magic
744	Morytania	Equip a Noxious Bow.	Equip a noxious bow.	90 Crafting, 90 Ranged
745	Morytania	Equip a full set of Linza's equipment, including the hammer and shield.	Equip a full set of Linza the Disgraced's equipment, including the hammer and shield.	80 Attack, 80 Defence, Completion of Kindred Spirits
746	Morytania	Equip a full set of Akrisae's equipment, including the war mace.	Equip a full set of Akrisae the Doomed's equipment, including the war mace.	70 Attack, 70 Ranged, 70 Magic, 70 Defence, Completion of Ritual of the Mahjarrat
747	Morytania	Equip a Malevolent Kiteshield.	Equip a malevolent kiteshield.	90 Defence
748	Morytania	Equip a Merciless Kiteshield.	Equip a merciless kiteshield.	90 Defence
749	Morytania	Equip a Vengeful Kiteshield.	Equip a vengeful kiteshield.	90 Defence
750	Morytania	Complete all the Everlight mysteries.	Complete all of the Everlight Dig Site mysteries.	105 Archaeology, 40 Construction, 6 Hunter
751	Morytania	Obtain an Araxyte Pheremone drop.	Obtain an araxyte pheremone drop.	N/A
752	Morytania	Complete the task set: Elite Morytania.	Complete the Elite Morytania achievements.	See Elite Morytania achievements page
753	Morytania	Enter the Morytania Slayer Tower resource dungeon.	Enter the Morytania Slayer Tower dungeon.	100 Dungeoneering
757	Morytania	Read the book acquired from Roberta outside the Everlight porcelain clay mine.	Read On the Origin of Centaurs.	102 Mining
551	Elven Lands	Enter the Gorajo Hoardstalker resource dungeon.	Enter the Gorajo Hoardstalker Dungeon.	95 Dungeoneering
552	Elven Lands	Have Lady Ithell create a crystal pickaxe, hatchet, or mattock.	Have Lady Ithell create a crystal pickaxe, hatchet, or mattock.	N/A
553	Elven Lands	Find all of the memoriam crystals in Prifddinas.	Find all of the memoriam crystals in Prifddinas.	77 Agility, 75 Farming, 50 Thieving, Completion of Fate of the Gods, partial completion of A Fairy Tale II - Cure a Queen
554	Elven Lands	Aid Lord Amlodd in cleansing shadow cores.	Complete the I'm Forever Washing Shadows achievement.	91 Divination
555	Elven Lands	Help Lady Ithell with crystal singing research.	Complete the Sing for the Lady achievement.	75 Smithing, 75 Magic
556	Elven Lands	Aid Lady Trahaearn in removing some corruption by smelting 100 corrupted ore.	Complete the Uncorrupted Ore achievement.	89 Mining, 89 Smithing
557	Elven Lands	Check a grown Crystal Tree in the Tower of Voices.	Check a grown crystal tree in the Tower of Voices.	94 Farming
558	Elven Lands	Have 4 elven clans suspect you of thieving at the same time.	Have 4 elven clans suspect you of thieving at the same time. If you have the Five Finger Discount relic this task is completed when pickpocketing an elf.	94 Thieving
559	Elven Lands	Chop a log from an elder tree you have grown in the Prifddinas farming patch, then fletch it into a shortbow.	Chop a log from an elder tree you have grown in the Prifddinas farming patch, then fletch it into an elder shortbow.	90 Farming, 90 Woodcutting, 90 Fletching
560	Elven Lands	Catch a Crystal impling.	Catch a crystal impling. Cannot be completed in Puro-Puro.	95 Hunter
561	Elven Lands	Craft an Attuned crystal teleport seed.	Craft an attuned crystal teleport seed.	85 Smithing, Completion of The Eyes of Glouphrie
562	Elven Lands	Mine 50 Light animica in Isafdar.	Mine 50 light animica in Isafdar.	90 Mining
563	Elven Lands	Chop 25 Elder logs in Tirannwn.	Chop 25 elder logs in Tirannwn.	90 Woodcutting
564	Elven Lands	Catch 75 Crystal skillchompas in Isafdar.	Catch 75 crystal skillchompas in Isafdar.	97 Hunter
565	Elven Lands	Complete the task set: Elite Tirannwn.	Complete the Elite Tirannwn achievements.	See Elite Tirannwn achievements page
566	Elven Lands	Complete a Seren symbol.	Create a Seren's symbol.	98 Thieving or 77 Agility
567	Elven Lands	Obtain the titles of the elven clans.	Obtain the titles of the elven clans.	89 Mining, 90 Slayer, 120 Combat, 90 Farming, 88 Summoning, 71 Divination, 89 Crafting, 77 Agility, Completion of all quests
568	Elven Lands	Perform well enough in Rush of Blood to impress Morvran.	Complete the Make Them Bleed achievement.	85 Slayer
569	Elven Lands	Reach inside the Motherlode Maw 5 times.	Reach inside the Motherlode Maw 5 times.	115 Dungeoneering and level 95 in all other skills
570	Elven Lands	Obtain 'the Elven' title by purchasing each of the elven clan capes.	Obtain the Elven title by purchasing each of the elven clan capes.	8,000,000 coins
669	Wilderness	Equip the Hellfire bow.	Equip the hellfire bow.	90 Ranged
670	Wilderness	Complete a slayer task from Mandrith.	Complete a slayer task from Mandrith.	95 Slayer, 120 Combat
671	Wilderness	Chop 20 Bloodwood logs in the Wilderness.	Chop 20 bloodwood logs in the Wilderness.	85 Woodcutting
672	Wilderness	Unlock the Greater Flurry, Barge, and Fury abilities.	Unlock the Greater Flurry, Barge, and Fury abilities.	N/A
673	Wilderness	Crack 6 safes inside the Rogues' Castle.	Crack 6 safes inside the Rogues' Castle.	90 Thieving
674	Wilderness	Defeat 5 Ripper Demons.	Defeat 5 ripper demons.	96 Slayer
675	Wilderness	Defeat 10 Lava Strykewyrms in the Wilderness, south of the Lava Maze.	Defeat 10 lava strykewyrms in the Wilderness, south of the Lava Maze.	94 Slayer
676	Wilderness	Equip Annihilation, Decimation, or Obliteration.	Equip Annihilation, Decimation, or Obliteration.	87 Attack OR 87 Ranged OR 87 Magic
677	Daemonheim	Kill Blink in a solo Dungeoneering instance, without dying.	Kill Blink in a solo Dungeoneering instance without dying.	95 Dungeoneering
679	Wilderness	Defeat every miniboss inside the Dragonkin Laboratory.	Defeat every miniboss inside the Dragonkin Laboratory.	N/A
680	Wilderness	Defeat the Black Stone Dragon.	Defeat the black stone dragon once.	N/A
681	Wilderness	Defeat the Black Stone Dragon. (25 times)	Defeat the black stone dragon 25 times.	N/A
682	Wilderness	Complete the task set: Elite Wilderness.	Complete the Elite Wilderness achievements.	See Elite Wilderness achievements page
683	Wilderness	Defeat 25 Hydrix dragons in the Wilderness.	Defeat 25 hydrix dragons in the Wilderness.	101 Slayer
684	Wilderness	Defeat 10 Abyssal lords in the Wilderness.	Defeat 10 abyssal lords in the Wilderness.	115 Slayer
685	Daemonheim	Mine 30 Primal ores.	Mine 30 primal ores.	100 Mining
686	Daemonheim	Smelt 150 Primal bars.	Smelt 150 primal bars.	100 Mining, 100 Smithing
687	Daemonheim	Defeat Kal'Ger the Warmonger.	Defeat Kal'Ger the Warmonger.	113 Dungeoneering
689	Wilderness	Defeat the Ambassador.	Defeat the Ambassador once.	N/A
690	Wilderness	Defeat the Ambassador. (25 times)	Defeat the Ambassador 25 times.	N/A
691	Wilderness	Equip a Spectral, Arcane, Elysian, or Divine spirit shield.	Equip a spectral, arcane, Elysian, or divine spirit shield.	75 Defence, 75 Prayer, Completion of Summer's End
692	Wilderness	Defeat the Ambassador after allowing 4 unstable black holes to explode.	Defeat the Ambassador after allowing 4 unstable black holes to explode.	N/A
1114	Fort Forinthry	Defeat Zemouregal & Vorkath.	Defeat Zemouregal & Vorkath.	Completion of Battle of Forinthry unless tier 5 reached
1115	Fort Forinthry	Defeat Zemouregal & Vorkath. (100 times)	Defeat Zemouregal & Vorkath 100 times.	Completion of Battle of Forinthry unless tier 5 reached
Master Tasks (400 Points each)
Task ID	Locality	Task	Information	Requirements
504	Anachronia	Fully upgrade the Town Hall in the base camp on Anachronia.	Fully upgrade the town hall in the base camp on Anachronia.	N/A
506	Anachronia	Complete a big game encounter with 3 creatures active.	Complete a Big Game Hunter encounter with 3 creatures active.	75 Hunter, 55 Slayer
507	Anachronia	Breed a shiny dinosaur.	Breed a shiny dinosaur.	97 Farming
510	Anachronia	Equip Skeka's hypnowand.	Equip Skeka's hypnowand.	103 Archaeology, 95 Dungeoneering, 80 Hunter
511	Anachronia	Complete the quest: Extinction.	Complete the Extinction quest.	See quest page
261	Burthorpe	Complete all of the Combat Achievements for God Wars Dungeon bosses, including Nex.	Complete all of the Combat Achievements for God Wars Dungeon bosses, including Nex.	70 Agility, 70 Strength, 70 Ranged, 70 Constitution, 87 Summoning, Partial completion of Troll Stronghold, completion of The Slug Menace, completion of Fate of the Gods
262	Burthorpe	Unlock all the prayers from the Praesul Codex.	Unlock all the prayers from the Praesul codex.	70 Agility, 70 Strength, 70 Ranged, 70 Constitution, Partial completion of Troll Stronghold
336	Desert	Defeat Telos, the Warden at 1,000% enrage.	Defeat Telos, the Warden at 1000% enrage.	80 Attack, 80 Prayer, 80 Magic, 80 Ranged
338	Desert	Complete all of the Combat Achievements for the Heart of Gielinor bosses (excluding Telos).	Complete all of the Combat Achievements for the Heart of Gielinor bosses (excluding Telos).	85 Attack, 80 Prayer, 80 Magic, 80 Ranged, 77 Agility
1113	Menaphos	Defeat Amascut, the Devourer. (100 times)	Defeat Amascut, the Devourer 100 times.	Completion of Eclipse of the Heart unless tier 5 reached
396	Fremennik	Equip every completed God Book.	Equip every completed god book.	30 Prayer, Completion of Horror from the Deep
146	Global	Reach maximum total level.	Reach maximum total level.	3095 Total level
963	Global	Complete 150 Master clue scrolls.	Complete 150 master clue scrolls.	N/A
1088	Global	Work with Ramarno (in Camdozaal) to obtain a pickaxe of life and death.	Create a pickaxe of life and death.	100 Mining, 100 Smithing, 90 Necromancy, Completion of Birthright of the Dwarves, While Guthix Sleeps, Defender of Varrock, Kili Row, and Cabin Fever
1089	Global	Have something planted and living in every farming patch.	Have something planted and living in every farming patch.	119 Farming, 70 Magic, 60 Agility, 60 Crafting, 50 Construction, Completion of The Great Brain Robbery, Lunar Diplomacy, My Arm's Big Adventure, The Fremennik Trials, Unwelcome Guests, Necromancy!, and Back to my Roots
1090	Global	Work with Ramarno (in Camdozaal) to obtain a hatchet of bloom and blight.	Create a hatchet of bloom and blight.	100 Smithing, 100 Woodcutting, 100 Fletching, 90 Necromancy, Completion of Kili Row and Pieces of Hate
1091	Global	Equip any Masterwork weapon.	Equip any masterwork weapon.	See Masterwork bow#Full process, Masterwork 2h sword#Full process, Masterwork staff#Full process, or Masterwork Spear of Annihilation#Raw materials required for full requirements.
1092	Global	Equip a full set of Masterwork armour.	Equip a full set of masterwork armour.	Either of the following combinations: 90 Mining, 99 Smithing, and 90 Defence; OR 110 Crafting, 104 Smithing, 100 Farming, 90 Defence, 90 Runecrafting, and 90 Magic
1093	Global	Unlock the Richie pet from helping Richie accumulate wealth at the Grand Exchange.	Donate 100,000,000 GP to Richie.	N/A
1095	Global	Obtain 200 Million XP in any single skill.	Obtain 200 Million XP in any single skill.	N/A
1096	Global	Fill all of the Treasure Trail hidey-holes. You can find a complete list of hidey-holes at the noticeboard by Zaida.	Fill all of the Treasure Trail hidey-holes.	88 Construction, Numerous other requirements; see Fill Them All! for a complete list
1097	Global	Obtain a dye, or a piece of Third-age or Second-age gear from a clue scroll.	Obtain a dye, or a piece of Third-age or Second-age gear from a clue scroll.	Good luck!
1111	Global	Reach at least level 95 in all non-elite skills.	Reach at least level 95 in all non-elite skills.	All skills except Invention at level 95
456	Feldip	Equip an Expert Dragon Archer hat.	Equip an Expert Dragon Archer hat.	4,000 chompy bird kills
458	Ardougne	Throw 100,000,000 gold coins into the Whirlpool at the Deep Sea Fishing platform.	Throw 100,000,000 gold coins into the Whirlpool at the Deep Sea Fishing platform.	68 Fishing
122	Varrock	Equip an Ek-ZekKil.	Equip an Ek-ZekKil.	95 Strength, 95 Smithing
123	Varrock	Equip a Fractured Staff of Armadyl.	Equip a Fractured Staff of Armadyl.	95 Magic, 95 Crafting
767	City of Um	Complete all Sanctum of Rebirth combat achievements.	Complete all Sanctum of Rebirth combat achievements.	Completion of Soul Searching
768	City of Um	Complete all of Rasial, the First Necromancer's combat achievements.	Complete all of Rasial, the First Necromancer's combat achievements.	Completion of Alpha vs Omega
754	Morytania	Fully explore the history of the Everlight Dig Site.	Complete the Mastery - Everlight achievements.	105 Archaeology, 40 Construction, 6 Hunter
755	Morytania	Complete all Araxxor and Araxxi combat achievements.	Complete all Araxxor and Araxxi combat achievements.	N/A
756	Morytania	Complete the quest: River of Blood.	Complete River of Blood.	See quest page
571	Elven Lands	Obtain the 'Dark Lord' title by unlocking a selection of titles from Prifddinas.	Obtain the Dark Lord title by completing the Sort of Crystally achievement.	89 Mining, 90 Slayer, 120 Combat, 90 Farming, 88 Summoning, 71 Divination, 89 Crafting, 77 Agility, Completion of all quests
688	Wilderness	Equip an Eldritch Crossbow.	Equip an eldritch crossbow.	92 Ranged, 96 Fletching
1116	Varrock	Equip an igneous Kal-Zuk cape.	Equip an igneous Kal-Zuk cape.	90 Crafting, Completion of the Excuse Me, That's My Seat achievement
"""

def parse_tasks(raw_text):
    tasks = {"Easy": [], "Medium": [], "Hard": [], "Elite": [], "Master": []}
    current_tier = None
    points = 0

    lines = raw_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        tier_match = re.match(r'(\w+) Tasks \((\d+) Points each\)', line)
        if tier_match:
            current_tier = tier_match.group(1)
            points = int(tier_match.group(2))
            continue

        if line.startswith("Task ID"):
            continue

        parts = line.split('\t')

        if len(parts) == 5 and current_tier:
            try:
                task_id = int(parts[0])
                task_data = {
                    "id": task_id,
                    "locality": parts[1],
                    "task": parts[2],
                    "information": parts[3],
                    "requirements": parts[4],
                    "tier": current_tier,
                    "points": points
                }
                # A task with a null requirement was causing issues
                if task_data["requirements"] == "null":
                    task_data["requirements"] = "N/A"

                tasks[current_tier].append(task_data)
            except (ValueError, IndexError):
                # Ignore lines that don't parse correctly
                continue

    return tasks

if __name__ == "__main__":
    parsed_tasks = parse_tasks(full_raw_data)
    with open('tasks.json', 'w') as f:
        json.dump(parsed_tasks, f, indent=2)
    print("tasks.json file has been created successfully.")