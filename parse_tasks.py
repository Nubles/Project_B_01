import json
import re

# The full, corrected raw text data provided by the user.
full_raw_data = """
Task ID	Tier	Locality	Task	Information / Requirements	Pts	Comp%
462	Easy	Anachronia	Complete the base camp tutorial on Anachronia.	Complete the Anachronia base camp tutorial.	10	52.1%
463	Easy	Anachronia	Observe all the large dragonkin statues around Anachronia.	Observe all the large dragonkin statues around Anachronia.	10	3.2%
464	Easy	Anachronia	Surge under the spine on Anachronia.	Complete Spinal Surgery. (5 Agility)	10	30.4%
461	Easy	Anachronia	Set sail for Anachronia.	Set sail for Anachronia on The Stormbreaker docked at Varrock Dig Site.	10	53.1%
465	Easy	Anachronia	Complete the quest: Helping Laniakea (miniquest).	Complete the Helping Laniakea miniquest.	10	0.2%
466	Easy	Anachronia	Complete the quest: Raksha, the Shadow Colossus.	Complete Raksha, the Shadow Colossus quest.	10	7.7%
467	Easy	Anachronia	Obtain 100 potent herbs from Herby Werby.	Obtain 100 potent herbs from Herby Werby. (1 Herblore)	10	35.9%
217	Easy	Asgarnia: Burthorpe	Complete a lap of the Burthorpe Agility course.	Complete a lap of the Burthorpe Agility Course. (1 Agility)	10	77.8%
221	Easy	Asgarnia: Falador	Kill a goblin raider boss in the Goblin Village.	Kill 15 goblins in the Goblin Village to spawn a goblin raider boss.	10	49.5%
222	Easy	Asgarnia: Falador	Complete the quest: Witch's House.	Complete Witch's House.	10	36.4%
223	Easy	Asgarnia: Falador	Sit down with Tiffy in Falador park.	Sit on the bench with Sir Tiffy Cashien in Falador Park.	10	74.5%
224	Easy	Asgarnia: Falador	Pray to Bandos's remains.	Pray to Bandos's remains (just south-east of Goblin Village).	10	62.6%
225	Easy	Asgarnia: Falador	Dance in the Falador party room.	Dance in the Falador party room.	10	71.3%
263	Easy	Asgarnia: Port Sarim	Give Thurgo a redberry pie.	Give Thurgo a redberry pie. (10 Cooking, Partial completion of The Knight's Sword)	10	32.7%
268	Easy	Asgarnia: Taverley	Build a God statue in Taverley.	Build a God statue in Taverley.	10	60.8%
271	Easy	Desert: Menaphos	Enter Menaphos.	Enter Menaphos.	10	54.4%
272	Easy	Desert: General	Catch a whirligig at Het's Oasis.	Catch a whirligig at Het's Oasis. (1 Hunter)	10	49.5%
274	Easy	Desert: General	Search the Grand Gold Chest in room 1 of Pyramid Plunder.	Search the grand gold chest in room 1 of Pyramid Plunder in Sophanem. (21 Thieving, Partial completion of Icthlarin's Little Helper)	10	5.3%
275	Easy	Desert: General	Search the Grand Gold Chest in room 2 of Pyramid Plunder.	Search the grand gold chest in room 2 of Pyramid Plunder in Sophanem. (31 Thieving, Partial completion of Icthlarin's Little Helper)	10	5.2%
276	Easy	Desert: General	Search the Grand Gold Chest in room 3 of Pyramid Plunder.	Search the grand gold chest in room 3 of Pyramid Plunder in Sophanem. (41 Thieving, Partial completion of Icthlarin's Little Helper)	10	5.2%
277	Easy	Desert: General	Mine a gem rock at the Al Kharid mine.	Mine a gem rock at the Al Kharid mine. A common gem rock can be mined with level 1 Mining.	10	74%
279	Easy	Desert: General	Kill a crocodile.	Kill a crocodile.	10	40.1%
280	Easy	Desert: General	Create a spirit kalphite pouch.	Create a spirit kalphite pouch at the obelisk south west of Pollnivneach. (25 Summoning, A pouch, 51 spirit shards, a blue charm, and a potato cactus)	10	1.9%
281	Easy	Desert: Menaphos	Squish 10 corrupted scarabs.	Squish 10 corrupted scarabs.	10	15.2%
282	Easy	Desert: General	Sell a pyramid top to Simon.	Hand Simon Templeton a pyramid top. (30 Agility)	10	13.6%
283	Easy	Desert: General	Use any of the magic carpets in the desert.	Use any of the magic carpets in the desert. (1,000 coins)	10	53.3%
284	Easy	Desert: General	Harvest a rose at Het's Oasis.	Harvest a rose at Het's Oasis. (30 Farming)	10	29.3%
339	Easy	Fremennik: Lunar Isles	Switch to the Lunar Spellbook at the astral altar.	Switch to the Lunar Spellbook at the astral altar. (Completion of Lunar Diplomacy)	10	1%
340	Easy	Fremennik: Mainland	Defeat a Rock Crab in the Fremennik Province.	Defeat a Rock Crab in the Fremennik Province.	10	41.6%
341	Easy	Fremennik: Mainland	Defeat a Cockatrice in the Fremennik Province.	Defeat a cockatrice in the Fremennik Province. (25 Slayer, A mirror shield)	10	23.2%
342	Easy	Fremennik: Mainland	Defeat a Troll in the Fremennik Province.	Defeat a troll in the Fremennik Province.	10	12.6%
343	Easy	Fremennik: Mainland	Deposit an item with Peer the Seer.	Deposit an item with Peer the Seer. (Completion of the easy Fremennik achievements)	10	0.9%
344	Easy	Fremennik: Mainland	Use the Bank on Jatizso or Neitiznot.	Use the Bank on Jatizso or Neitiznot. (Partial completion of The Fremennik Isles)	10	2.4%
346	Easy	Fremennik: Mainland	Catch a Sapphire Glacialis.	Catch a Sapphire Glacialis. (25 Hunter, A butterfly net and jar)	10	8.4%
127	Easy	Global	Level up any of your skills for the first time.	Level up any of your skills for the first time.	10	98.3%
128	Easy	Global	Reach level 5 in any skill.	Reach level 5 in any skill.	10	97.7%
129	Easy	Global	Reach level 10 in any skill.	Reach level 10 in any skill.	10	97%
130	Easy	Global	Reach level 20 in any skill.	Reach level 20 in any skill.	10	95.5%
136	Easy	Global	Reach combat level 5.	Reach combat level 5.	10	94.4%
137	Easy	Global	Reach combat level 10.	Reach combat level 10.	10	91.5%
141	Easy	Global	Reach total level 50.	Reach total level 50.	10	97.3%
142	Easy	Global	Reach total level 100.	Reach total level 100.	10	94.5%
147	Easy	Global	Mine a copper ore.	Mine copper ore from a copper rock. (1 Mining)	10	93.2%
148	Easy	Global	Mine 10 copper ore.	Mine 10 copper ore. (1 Mining)	10	92.4%
149	Easy	Global	Mine a tin ore.	Mine tin ore from a tin rock. (1 Mining)	10	91.4%
150	Easy	Global	Mine 10 tin ore.	Mine 10 tin ore. (1 Mining)	10	90.2%
151	Easy	Global	Smelt a bronze bar.	Smelt a bronze bar. (1 Smithing)	10	92.8%
152	Easy	Global	Smelt 10 bronze bars.	Smelt 10 bronze bars. (1 Smithing)	10	92.4%
153	Easy	Global	Smith any bronze item.	Smith any bronze item. (1 Smithing)	10	87.9%
154	Easy	Global	Mine clay.	Mine clay. (1 Mining)	10	87.6%
155	Easy	Global	Make some soft clay.	Make soft clay by using clay on a water source or with a container of water.	10	78.3%
156	Easy	Global	Mine any ore 5 times.	Mine any ore 5 times. (1 Mining)	10	93.5%
159	Easy	Global	Chop any tree 5 times.	Chop any tree 5 times. (1 Woodcutting)	10	90.4%
162	Easy	Global	Chop a basic tree.	Chop a basic tree. (1 Woodcutting)	10	93.4%
163	Easy	Global	Chop 10 basic trees.	Chop 10 basic trees. (1 Woodcutting)	10	88.8%
164	Easy	Global	Chop an oak tree.	Chop an oak tree. (10 Woodcutting)	10	84.5%
166	Easy	Global	Burn any logs.	Burn any logs. (1 Firemaking)	10	92%
167	Easy	Global	Burn any logs 5 times.	Burn any logs 5 times. (1 Firemaking)	10	87.6%
170	Easy	Global	Catch a shrimp.	Catch a raw shrimp. (1 Fishing)	10	88.1%
171	Easy	Global	Catch 10 shrimp.	Catch 10 raw shrimps. (1 Fishing)	10	87.2%
172	Easy	Global	Catch an anchovy.	Catch a raw anchovy. (15 Fishing)	10	73.9%
173	Easy	Global	Catch a herring.	Catch a raw herring. (10 Fishing)	10	68%
174	Easy	Global	Cook shrimp, meat, or chicken.	Cook raw shrimps, raw meat, or raw chicken. (1 Cooking)	10	92.3%
175	Easy	Global	Cook 10 shrimp, meat, or chicken.	Cook 10 raw shrimps, raw meat, or raw chicken. (1 Cooking)	10	87.2%
176	Easy	Global	Burn any food.	Burn any food. (1 Cooking)	10	86.7%
177	Easy	Global	Catch any fish 5 times.	Catch any fish 5 times. (1 Fishing)	10	89.1%
180	Easy	Global	Bury any bones.	Bury any bones. (1 Prayer)	10	94.5%
181	Easy	Global	Bury any bones 10 times.	Bury any bones 10 times. (1 Prayer)	10	87.3%
182	Easy	Global	Activate the thick skin, rock skin, or steel skin Prayer.	Activate the Thick Skin, Rock Skin, or Steel Skin prayer. (1 Prayer)	10	86.5%
183	Easy	Global	Run out of Prayer points.	Run out of Prayer points. (1 Prayer)	10	85.6%
184	Easy	Misthalin: Draynor Village	Harvest a memory from a pale wisp.	Harvest a pale memory from a pale wisp. (1 Divination)	10	83.2%
185	Easy	Misthalin: Draynor Village	Harvest 10 memories from a pale wisp.	Harvest 10 pale memories from a pale wisp. (1 Divination)	10	82.5%
186	Easy	Global	Harvest any memory from a wisp 5 times.	Harvest any memory from a wisp 5 times. (1 Divination)	10	83.2%
189	Easy	Global	Pickpocket from a man or woman.	Pickpocket from a man or woman. (1 Thieving)	10	89.4%
190	Easy	Global	Pickpocket from a man or woman 10 times.	Pickpocket from a man or woman 10 times. (1 Thieving)	10	86.7%
191	Easy	Global	Steal from any stall.	Steal from any stall. (2 Thieving for Vegetable Stalls)	10	86.7%
192	Easy	Global	Steal from any stall 10 times.	Steal from any stall 10 times. (2 Thieving for Vegetable Stalls)	10	85.3%
193	Easy	Global	Pickpocket anyone 5 times.	Pickpocket anyone 5 times. (1 Thieving)	10	88.4%
196	Easy	Global	Rake any farming patch.	Rake any farming patch. (1 Farming)	10	82.4%
197	Easy	Global	Plant seeds in any farming patch.	Plant seeds in any farming patch. (1 Farming)	10	74%
198	Easy	Global	Plant seeds in any farming patch 10 times.	Plant seeds in any farming patch 10 times. (1 Farming)	10	61.1%
200	Easy	Global	Add any compostable item to a compost bin.	Add any compostable item to a compost bin.	10	68.3%
201	Easy	Global	Have a tool leprechaun note any produce.	Have a tool leprechaun note any produce.	10	61.4%
204	Easy	Global	Use the Home Teleport spell to return to Lumbridge.	Use the Home Teleport spell to return to Lumbridge.	10	91.4%
205	Easy	Global	Eat a cabbage.	Eat a cabbage.	10	84%
206	Easy	Global	Eat a baked potato.	Eat a baked potato. (7 Cooking)	10	61.8%
207	Easy	Global	Eat an onion.	Eat an onion.	10	76.4%
208	Easy	Global	Kill an imp.	Kill an imp.	10	82%
209	Easy	Global	Kill a chicken.	Kill a chicken.	10	85.7%
210	Easy	Global	Claim a free item from any store.	Claim a free item from any store e.g. a tinderbox from Lumbridge General Store.	10	86.9%
211	Easy	Global	Return a free item to any store.	Return a free item to any store e.g. a tinderbox from Lumbridge General Store.	10	75.3%
212	Easy	Global	Sell an item to any store.	Sell an item to any store.	10	86.8%
213	Easy	Global	Listen to any musician.	Listen to any musician.	10	80.1%
214	Easy	Global	Pick wheat from a field.	Pick wheat from a field.	10	83.9%
215	Easy	Global	Prospect any rock.	Prospect any rock. (1 Mining)	10	77.8%
216	Easy	Global	View the skillguide.	View the skill guide.	10	95%
345	Easy	Global	Create a Guthix Rest Potion.	Create a Guthix rest potion. (18 Herblore, Partial completion of One Small Favour)	10	2%
770	Easy	Global	Make 5 potions of any kind.	Make 5 potions of any kind. (1 Herblore)	10	57.9%
773	Easy	Global	Drink a Strength Potion.	Drink a strength potion. (Giving a limpwurt root and red spiders' eggs to the Apothecary)	10	37.3%
774	Easy	Global	Make an Attack Potion.	Make an attack potion. (1 Herblore, A clean guam and an eye of newt)	10	65.3%
775	Easy	Global	Make a Necromancy Potion.	Make a necromancy potion. (11 Herblore, A clean marrentill and cadava berries)	10	22.8%
776	Easy	Global	Clean 5 Grimy Guam.	Clean 5 grimy guam. (1 Herblore, 5 grimy guam)	10	64.6%
777	Easy	Global	Clean 15 Grimy Tarromin.	Clean 15 grimy tarromin. (5 Herblore, 15 grimy tarromin)	10	41%
778	Easy	Global	Clean 5 of any herb.	Clean 5 of any herb. (1 Herblore, 5 of any grimy herb)	10	67.3%
779	Easy	Global	Clean 10 of any herb	Clean 10 of any herb. (1 Herblore, 10 of any grimy herb)	10	64.3%
782	Easy	Global	Fletch an Oak Shortbow (unstrung).	Fletch an unstrung oak shortbow. (20 Fletching, Oak logs)	10	55.8%
783	Easy	Global	Fletch some arrow shafts.	Fletch some arrow shafts. (1 Fletching, Logs of any kind)	10	81.9%
785	Easy	Global	Fletch 50 Bronze bolts.	Fletch 50 bronze bolts. (9 Fletching, A bronze bar and 50 feathers)	10	55.5%
786	Easy	Global	Complete 10 laps of any Agility course.	Complete 10 laps of any Agility course. (1 Agility)	10	69.1%
790	Easy	Global	Smith 10 of any metal weapon or armour piece.	Smith 10 of any metal weapon or armour piece. (1 Smithing, 10 of any metal bar)	10	82.5%
794	Easy	Global	Open 30 Sedimentary Geodes.	Open 30 sedimentary geodes. These are found randomly while mining. (1 Mining)	10	72.5%
795	Easy	Global	Maintain nearly maximum stamina when mining for 60 seconds.	Maintain nearly maximum stamina when mining for 60 seconds. (1 Mining)	10	71.1%
796	Easy	Global	Harvest a Grimy Marrentill.	Harvest a grimy marrentill. (9 Farming, Marrentill seed)	10	42.9%
797	Easy	Global	Harvest 10 Grimy Tarromin.	Harvest 10 grimy tarromin. (19 Farming, Tarromin seeds)	10	41.7%
798	Easy	Global	Cook 5 fish.	Cook 5 fish. (1 Cooking, 5 of any raw fish)	10	87.8%
801	Easy	Global	Make some Bread.	Make some bread. Bread dough can be created by using a pot of flour with water, it must be cooked at a range. (1 Cooking, Bread dough)	10	56.9%
802	Easy	Global	Make some flour.	Make a pot of flour by grinding wheat at a windmill and collecting the flour in an empty pot. (Wheat and an empty pot)	10	78.6%
803	Easy	Global	Offer 5 bones of any kind to an altar.	Offer 5 bones (ashes also work) at the chaos altar in the Wilderness, the altar in Fort Forinthry, or an altar in the player-owned house chapel. (1 Prayer)	10	55.7%
804	Easy	Global	Offer 25 bones of any kind to an altar.	Offer 25 bones (ashes also work) at the chaos altar in the Wilderness, the altar in Fort Forinthry, or an altar in the player-owned house chapel. (1 Prayer)	10	52.9%
806	Easy	Global	Scatter some Ashes.	Scatter some ashes. (1 Prayer, Any demonic ashes)	10	75.7%
807	Easy	Global	Scatter 25 ashes of any kind.	Scatter 25 ashes of any kind. (1 Prayer, 25 of any demonic ashes)	10	43.7%
809	Easy	Global	Restore 50 Prayer Points at an Altar at once.	Restore 50 Prayer Points at an Altar at once. (5 Prayer)	10	75%
811	Easy	Global	Activate Superhuman/Ultimate Strength & Improved/Incredible Reflexes.	Activate Superhuman or Ultimate Strength and Improved or Incredible Reflexes prayers at the same time. (16 Prayer)	10	64.2%
812	Easy	Global	Catch a Baby Impling.	Catch a baby impling. Cannot be completed in Puro-Puro. (17 Hunter)	10	30%
813	Easy	Global	Catch 10 Implings of any kind.	Catch 10 implings. Cannot be completed in Puro-Puro.	10	13.1%
816	Easy	Global	Catch 5 Hunter creatures.	Catch 5 Hunter creatures. (1 Hunter)	10	58.7%
819	Easy	Global	Complete 5 Slayer tasks.	Complete 5 Slayer assignments. (1 Slayer)	10	50.8%
823	Easy	Global	Pick 5 Flax.	Pick 5 flax from flax fields.	10	71.8%
824	Easy	Global	Spin 5 bowstring.	Spin 5 bowstrings by using flax on a spinning wheel. (1 Fletching, 5 flax)	10	69.9%
825	Easy	Global	Surge a distance of one tile.	Surge a distance of one tile. (5 Agility)	10	70.2%
826	Easy	Global	Spin a Ball of Wool.	Spin a ball of wool by using wool at a spinning wheel. (1 Fletching, Wool)	10	75.5%
827	Easy	Global	Equip a full set of Iron armour without any upgrades.	Equip an iron full helm, iron platebody, iron platelegs/iron plateskirt, iron gauntlets, iron armoured boots, and an iron kiteshield. (10 Defence)	10	60.8%
828	Easy	Global	Equip a full set of Green Dragonhide armour.	Equip a full set of green dragonhide armour. (40 Defence)	10	29.7%
829	Easy	Global	Equip a full set of Imphide robes.	Equip a full set of imphide robes. (10 Defence)	10	52.8%
830	Easy	Global	Equip a full set of Spider silk robes.	Equip a full set of spider silk robes. (20 Defence)	10	53.2%
831	Easy	Global	Store emote clue items in a Treasure Trail hidey-hole.	Store the items required for an emote clue in a Treasure Trail hidey-hole. (27 Construction, 4 planks and 10 of any nails for an easy hidey-hole)	10	11%
832	Easy	Global	Complete an Easy clue scroll.	Complete an easy clue scroll.	10	47.4%
836	Easy	Global	Collect 10 unique items for the General clue rewards log.	Collect 10 unique items for the general clue rewards collection log.	10	33.8%
403	Easy	Kandarin: Gnomes	Complete the Gnome Stronghold Agility Course.	Complete the Gnome Stronghold Agility Course. (1 Agility)	10	43%
404	Easy	Kandarin: Feldip Hills	Catch a Crimson Swift in the Feldip Hills.	Catch a crimson swift in the Feldip Hills. (1 Hunter, A bird snare)	10	8.5%
405	Easy	Kandarin: Ardougne	Defeat a Tortoise with riders in Kandarin.	Defeat a tortoise with riders in Kandarin.	10	32.6%
406	Easy	Kandarin: Seers Village	Complete the quest: You Are It.	Complete You Are It.	10	18.7%
407	Easy	Kandarin: Gnomes	Let Brimstail teleport you to the Rune Essence mine.	Let Brimstail teleport you to the Rune Essence mine.	10	21.6%
408	Easy	Kandarin: Feldip Hills	Equip a Marksman hat.	Equip a marksman hat. (125 chompy bird kills)	10	<0.1%
409	Easy	Global	Obtain a Naragi engram from Orla Fairweather.	Obtain a Naragi engram from Orla Fairweather. The engram is given to the player during the tutorial for Memorial to Guthix. (1 Divination)	10	26.4%
410	Easy	Kandarin: Ardougne	Learn how many beans make five.	Complete the player-owned farm tutorial at Manor Farm. (17 Farming, 20 Construction)	10	41.9%
411	Easy	Global	Catch a Wild Kebbit.	Catch a wild kebbit. (23 Hunter, Logs of any kind)	10	6.3%
412	Easy	Kandarin: Ardougne	Teleport to the Wilderness using the lever in Ardougne.	Pull the lever in Ardougne.	10	51.6%
413	Easy	Kandarin: Yanille	Use a ring of duelling to teleport to Castle Wars.	Teleport to Castle Wars with a ring of duelling. (27 Magic, 27 Crafting, Materials to make a ring of duelling)	10	17.4%
414	Easy	Kandarin: Gnomes	Make a Pineapple Punch cocktail.	Make a pineapple punch cocktail. (8 Cooking)	10	8.4%
572	Easy	Karamja	Collect 5 seaweed from anywhere on Karamja.	Collect 5 seaweed from anywhere on Karamja.	10	46.4%
573	Easy	Karamja	Fill up Luthas' crate with bananas.	Fill up Luthas' crate near the Musa Point plantation with bananas and receive 30 coins for your work.	10	42.2%
574	Easy	Karamja	Claim a ticket from Brimhaven Agility Arena.	Claim a ticket from Brimhaven Agility Arena. (1 Agility)	10	26.3%
575	Easy	Karamja	Kill a snake.	Kill a snake.	10	52.3%
576	Easy	Karamja	Catch a Karambwanji.	Catch a raw karambwanji. (5 Fishing)	10	23.3%
577	Easy	Karamja	Be assigned a Slayer task in Shilo Village.	Be assigned a Slayer task in Shilo Village. (100 Combat, 50 Slayer, Completion of Shilo Village)	10	6.3%
578	Easy	Karamja	Defeat a Greater Demon on Karamja.	Defeat a greater demon on Karamja.	10	31%
579	Easy	Karamja	Pick a pineapple on Karamja.	Pick a pineapple on Karamja from the pineapple plants near the lodestone.	10	46.2%
580	Easy	Karamja	Enter the Brimhaven Dungeon.	Enter the Brimhaven Dungeon. (875 coins)	10	51.7%
581	Easy	Karamja	Cross the spiky pit in Brimhaven Dungeon.	Cross the spiky pit using the stepping stones within Brimhaven Dungeon. (12 Agility)	10	41.2%
0	Easy	Misthalin: Lumbridge	Progress through the Leagues tutorial to unlock your first relic.	Progress through the Leagues tutorial to unlock your first relic.	10	100%
2	Easy	Misthalin: Draynor Village	Climb to the top of the Wizards' Tower.	Climb to the top of the Wizards' Tower.	10	79.6%
3	Easy	Misthalin: Draynor Village	Have Ned make you some rope from balls of wool.	Have Ned make you some rope from 4 balls of wool.	10	54.8%
4	Easy	Misthalin: Draynor Village	Siphon from a fire essling in the Runespan.	Siphon from a fire essling in the Runespan. (14 Runecrafting)	10	47.6%
5	Easy	Misthalin: Draynor Village	Convert at least one pale memory into energy.	Convert at least one pale memory into energy. (1 Divination)	10	69.8%
15	Easy	Misthalin: Edgeville	Kill a mugger near the Edgeville lodestone.	Kill a mugger near the Edgeville lodestone.	10	73.2%
16	Easy	Misthalin: Edgeville	Mine some coal in the centre of Barbarian village.	Mine some coal in the centre of Barbarian Village. (20 Mining)	10	70.7%
22	Easy	Misthalin: Fort Forinthry	Use the bank in the workshop at Fort Forinthry.	Use the bank in the workshop at Fort Forinthry.	10	54.9%
27	Easy	Misthalin: Lumbridge	Kill a giant rat in Lumbridge Swamp.	Kill a giant rat in Lumbridge Swamp.	10	91.1%
28	Easy	Misthalin: Lumbridge	Kill a goblin in Lumbridge.	Kill a goblin in Lumbridge.	10	94.8%
29	Easy	Misthalin: Lumbridge	Kill a giant spider in Lumbridge or Lumbridge Swamp.	Kill a giant spider in Lumbridge or Lumbridge Swamp.	10	91.1%
30	Easy	Misthalin: Lumbridge	Milk a cow.	Milk a cow. (A bucket)	10	88.5%
32	Easy	Misthalin: Lumbridge	Talk to Hans and find out how old you are.	Talk to Hans and find out how old you are.	10	90.9%
33	Easy	Misthalin: Lumbridge	Complete the quest: The Blood Pact.	Complete The Blood Pact.	10	79.6%
35	Easy	Misthalin: Draynor Village	Catch shrimp east of Lumbridge Swamp.	Catch some shrimp in the fishing spot to the east of Lumbridge Swamp. (1 Fishing)	10	85.2%
36	Easy	Misthalin: Lumbridge	Smelt a steel bar in the furnace in Lumbridge.	Smelt a steel bar in the furnace in Lumbridge. (20 Smithing)	10	64.6%
37	Easy	Misthalin: Lumbridge	Cook some rat meat on a fire in Lumbridge Swamp.	Cook some rat meat on a fire in Lumbridge Swamp. (1 Cooking)	10	87.5%
38	Easy	Misthalin: Lumbridge	Mine iron ore south-west of Lumbridge Swamp.	Mine iron ore from the mining site south-west of Lumbridge Swamp. (10 Mining)	10	85.1%
39	Easy	Misthalin: Lumbridge	Craft a water rune at the Water Altar.	Craft a water rune at the Water Altar. (5 Runecrafting)	10	48.2%
40	Easy	Misthalin: Lumbridge	Complete a task from Jacquelyn.	Complete a task from Jacquelyn, the Lumbridge Slayer master. (1 Slayer)	10	79.8%
41	Easy	Misthalin: Lumbridge	Fill a Charmed Sack with corruption.	Fill a Charmed Sack with corruption at the Nexus in Lumbridge Swamp. (1 Prayer)	10	78.9%
61	Easy	Misthalin: Draynor Village	Complete the quest: Necromancy!.	Complete Necromancy!.	10	71.6%
62	Easy	Misthalin: City of Um	Upgrade Death Skull or Deathwarden equipment to tier 20.	Upgrade a piece of Death Skull or Deathwarden equipment to tier 20. (20 Necromancy, 15 Smithing/Crafting, Completion of Kili Row)	10	29.3%
63	Easy	Misthalin: City of Um	Craft some spirit or bone runes.	Craft some spirit or bone runes. (1 Runecrafting, Partial completion of Rune Mythos)	10	26.3%
64	Easy	Misthalin: City of Um	Complete a Lesser Necroplasm ritual.	Complete a Lesser Necroplasm ritual. (5 Necromancy)	10	49.2%
65	Easy	Misthalin: City of Um	Conjure a skeleton at the City of Um ritual site.	Conjure a Skeleton Warrior at the Um ritual site. (2 Necromancy)	10	46.8%
66	Easy	Misthalin: City of Um	Conjure a zombie at the City of Um ritual site.	Conjure a Putrid Zombie at the Um ritual site. (40 Necromancy)	10	9.3%
67	Easy	Misthalin: City of Um	Conjure a ghost at the City of Um ritual site.	Conjure a Vengeful Ghost at the Um ritual site. (40 Necromancy)	10	10.8%
94	Easy	Misthalin: Varrock	Kill a dark wizard.	Kill a dark wizard.	10	80%
95	Easy	Misthalin: Varrock	Enter the Earth Altar using an earth tiara or talisman.	Enter the Earth Altar using an earth tiara or talisman. (1 Runecrafting)	10	39.4%
96	Easy	Misthalin: Varrock	Have Elsie tell you a story.	Have Elsie tell you a story. (A cup of tea)	10	61.7%
97	Easy	Misthalin: Varrock	Give a bone to one of Varrock's stray dogs.	Give a bone to one of Varrock's stray dogs (or to your pet stray dog if you have one).	10	71%
98	Easy	Misthalin: Varrock	Claim a free clue scroll from Zaida at the Grand Exchange.	Claim a free clue scroll from Zaida at the Grand Exchange.	10	70.4%
99	Easy	Misthalin: Fort Forinthry	Give Bill a beer in Fort Forinthry.	Give Bill a beer in Fort Forinthry. (A beer, partial completion of New Foundations)	10	31.1%
100	Easy	Misthalin: Varrock	Complete the Archaeology tutorial.	Complete the Archaeology tutorial. (1 Archaeology)	10	73.4%
101	Easy	Misthalin: Fort Forinthry	Make a plank yourself on the sawmill in Fort Forinthry.	Make a plank yourself on the sawmill in Fort Forinthry. (1 Construction, Partial completion of New Foundations)	10	47.4%
102	Easy	Misthalin: Varrock	Mine iron ore south-west of Varrock.	Mine some iron ore in the mining spot south-west of Varrock. (10 Mining)	10	79.1%
103	Easy	Misthalin: Varrock	Steal from the Varrock tea stall.	Steal from the Varrock tea stall. (5 Thieving)	10	70.5%
104	Easy	Misthalin: Varrock	Pan in the river at the Digsite.	Pan in the river at the Digsite. (Partial completion of The Dig Site)	10	17.4%
693	Easy	Morytania	Take an easy companion through an easy route of Temple Trekking.	Complete an easy Temple Trek. (Completion of In Aid of the Myreque)	10	0.8%
694	Easy	Morytania	Craft your own snelm in Morytania.	Craft a snelm. (15 Crafting, Any blamish shell)	10	28.3%
695	Easy	Morytania	Defeat a Werewolf in Morytania.	Defeat a Werewolf in Morytania.	10	45.5%
696	Easy	Morytania	Pass through the Holy barrier.	Pass through the Holy barrier. (Defeat a Ghoul)	10	61.2%
697	Easy	Morytania	Enter through the western gate of Port Phasmatys.	Enter through the western gate of Port Phasmatys.	10	11.8%
698	Easy	Morytania	Activate the lodestone in Canifis.	Activate the Canifis lodestone. (Access to Morytania)	10	60.8%
699	Easy	Morytania	Kill anything on the ground floor of the Slayer Tower.	Kill anything on the ground floor of the Slayer Tower. (1 Slayer, Access to Morytania)	10	44.8%
700	Easy	Morytania	Grow some fungus in the swamp using Bloom.	Cast Bloom using a blessed sickle or the Ivandis flail in Mort Myre Swamp. (18 Crafting, Completion of Nature Spirit)	10	15.7%
701	Easy	Morytania	Defeat 5 Feral Vampyres in the Haunted Woods.	Defeat 5 feral vampyres in the Haunted Woods. (Access to Morytania)	10	39.9%
702	Easy	Morytania	Use an ectophial to return to Port Phasmatys.	Use an ectophial to return to Port Phasmatys. (Completion of Ghosts Ahoy)	10	15.5%
703	Easy	Morytania	Visit Dragontooth Island by boat.	Visit Dragontooth Island by boat. (Ghostspeak amulet)	10	19.2%
514	Easy	Elven Lands: Tirranwn	Cook a Rabbit in Tirannwn.	Cook a raw rabbit in Tirannwn. (1 Cooking)	10	31%
515	Easy	Elven Lands: Tirranwn	Attempt to pass a leaf trap.	Attempt to pass a leaf trap.	10	41.1%
516	Easy	Elven Lands: Tirranwn	Use the Bank in Lletya.	Use the bank in Lletya.	10	37.4%
517	Easy	Elven Lands: Tirranwn	Charter a ship from Port Tyras.	Charter a ship from Port Tyras.	10	28.2%
518	Easy	Elven Lands: Tirranwn	Climb the Tower of Voices.	Climb the Tower of Voices.	10	37.3%
519	Easy	Elven Lands: Tirranwn	Burn logs using the everlasting bonfire in the Tower of Voices.	Burn some logs using the everlasting bonfire in the Tower of Voices. (1 Firemaking)	10	41.8%
520	Easy	Elven Lands: Tirranwn	Activate the lodestone in Prifddinas.	Activate the Prifddinas lodestone.	10	63.1%
521	Easy	Elven Lands: Tirranwn	Activate the lodestone in Tirannwn.	Activate the Tirannwn lodestone.	10	42.1%
522	Easy	Elven Lands: Tirranwn	Restore your prayer using the altar in Lletya.	Restore your prayer using the altar in Lletya. (1 Prayer)	10	32.4%
630	Easy	Wilderness: General	Use the bank at the Mage Arena.	Use the Mage Arena bank.	10	48.7%
631	Easy	Wilderness: General	Defeat the Chaos Elemental.	Defeat the Chaos Elemental once.	10	23.7%
632	Easy	Wilderness: General	Defeat the Chaos Elemental. (100 times)	Defeat the Chaos Elemental 100 times.	10	2%
633	Easy	Wilderness: General	Reach a score of 10 using the strange switches in the Wilderness.	Reach a score of 10 using the strange switches in the Wilderness.	10	13.1%
634	Easy	Wilderness: General	Jump over the Wilderness wall.	Jump over the Wilderness wall.	10	75.4%
635	Easy	Wilderness: General	Activate the lodestone near the Wilderness Crater.	Activate the Wilderness Crater lodestone.	10	71.4%
636	Easy	Wilderness: Daemonheim	Complete a Frozen floor in Daemonheim.	Complete a Frozen floor in Daemonheim. (1 Dungeoneering)	10	37.8%
637	Easy	Wilderness: Daemonheim	Make use of an autoheater, gem bag, herbicide, bonecrusher or charming imp.	Make use of either an autoheater, gem bag, herbicide, bonecrusher or charming imp.	10	55.1%
638	Easy	Wilderness: General	Enter the chaos tunnels from an entrance in the Wilderness.	Enter the Chaos Tunnels from an entrance in the Wilderness.	10	45.7%
639	Easy	Wilderness: General	Defeat a Black Unicorn in the Wilderness.	Defeat a black unicorn in the Wilderness.	10	57.1%
904	Easy	Global	Collect 5 unique items for the Medium clue rewards log.	Collect 5 unique items for the medium clue rewards collection log.	10	35.1%
468	Medium	Anachronia	Build your Player Lodge on Anachronia.	Build your Player Lodge on Anachronia. (40 Construction)	30	1.5%
469	Medium	Anachronia	Purchase the herb bag and the herb bag upgrade.	Purchase the herb bag and the herb bag upgrade from the Herby Werby reward shop. (1 Herblore)	30	0.1%
470	Medium	Anachronia	Give Snoop some clean Dwarf weed.	Give Snoop some clean dwarf weed. (70 Herblore)	30	0.7%
471	Medium	Anachronia	Harvest produce from 5 animals on Anachronia farm.	Harvest produce from 5 animals on Anachronia farm. (42 Farming, 45 Construction)	30	0.5%
473	Medium	Anachronia	Complete the beginner sections of the Anachronia agility course.	Complete the beginner sections of the Anachronia agility course. (30 Agility)	30	17.4%
474	Medium	Anachronia	Complete the novice sections of the Anachronia agility course.	Complete the novice sections of the Anachronia agility course. (50 Agility)	30	11.6%
218	Medium	Asgarnia: Burthorpe	Enter the Warriors Guild.	Enter the Warriors Guild. (Combined Attack and Strength level of 130)	30	23.2%
219	Medium	Asgarnia: Burthorpe	Equip a defender.	Equip a defender. (Combined Attack and Strength level of 130)	30	10.5%
220	Medium	Asgarnia: Burthorpe	Charge an Amulet of Glory in the Heroes' Guild.	Charge an amulet of glory in the Heroes' Guild. (Completion of Heroes' Quest)	30	0.6%
226	Medium	Asgarnia: Falador	Enter the Crafting Guild.	Enter the Crafting Guild. (40 Crafting)	30	45.2%
227	Medium	Asgarnia: Falador	Complete the task set: Easy Falador.	Complete the Easy Falador achievements.	30	3.5%
228	Medium	Asgarnia: Falador	Complete the task set: Medium Falador.	Complete the Medium Falador achievements.	30	0.1%
229	Medium	Asgarnia: Falador	Defeat the Giant Mole.	Kill the giant mole.	30	36.2%
230	Medium	Asgarnia: Falador	Defeat the Giant Mole. (50 times)	Kill the giant mole 50 times.	30	0.2%
231	Medium	Asgarnia: Falador	Steal some Wine of Zamorak from the Captured Temple.	Steal some wine of Zamorak from the Captured Temple, south of Goblin Village. (33 Magic for Telekinetic Grab)	30	22%
232	Medium	Asgarnia: Falador	Set up a dwarf cannon.	Set up a dwarf multicannon. (Completion of Dwarf Cannon)	30	2.2%
233	Medium	Asgarnia: Falador	Complete a ceremonial sword at the Artisans' Workshop.	Complete a ceremonial sword at the Artisans' Workshop. (1 Smithing)	30	29.2%
234	Medium	Asgarnia: Falador	Mine some orichalcite in the Mining Guild.	Mine some orichalcite ore in the Mining Guild. (60 Mining)	30	64.7%
235	Medium	Asgarnia: Burthorpe	Harvest a herb from the troll stronghold herb patch.	Harvest a herb from the troll stronghold herb patch. (9 Farming, Completion of My Arm's Big Adventure)	30	0.1%
269	Medium	Asgarnia: Taverley	Kill a blue dragon in Taverley dungeon.	Kill a blue dragon in Taverley dungeon. (Dusty key or 70 Agility)	30	24.7%
270	Medium	Asgarnia: Taverley	Open the crystal chest in Taverley.	Open the crystal chest in Taverley. (A crystal key)	30	19.1%
273	Medium	Desert: General	Clear the Fort debris at the Kharid-et Dig Site.	Clear the fort debris at the Kharid-et Dig Site. (12 Archaeology)	30	62.2%
278	Medium	Desert: General	Complete the quest: One Piercing Note.	Complete One Piercing Note.	30	23.4%
285	Medium	Desert: General	Complete a lap of the Het's Oasis agility course.	Complete a lap of the Het's Oasis agility course. (65 Agility)	30	11.2%
286	Medium	Desert: General	Defeat the Kalphite Queen.	Defeat the Kalphite Queen.	30	9.5%
287	Medium	Desert: General	Defeat the Kalphite Queen. (100 times)	Defeat the Kalphite Queen 100 times.	30	<0.1%
288	Medium	Desert: General	Defeat 100 bosses in the Dominion Tower.	Defeat 100 bosses in the Dominion Tower. (Completion of at least 20 various quests)	30	<0.1%
289	Medium	Desert: General	Complete the task set: Easy Desert.	Complete the Easy Desert achievements.	30	0.4%
290	Medium	Desert: General	Complete the task set: Medium Desert.	Complete the Medium Desert achievements.	30	<0.1%
291	Medium	Desert: Menaphos	Steal from the lamp stall in Menaphos.	Steal from the lamp stall in Menaphos. (46 Thieving)	30	11.7%
292	Medium	Desert: General	Buy some runes from Ali Morrisane.	Buy some runes from Ali Morrisane. (Completion of the runes portion of Ali the Trader)	30	0.6%
293	Medium	Desert: Menaphos	Catch a catfish.	Catch a raw catfish. (60 Fishing)	30	16.7%
294	Medium	Desert: General	Restore a Pontifex signet ring.	Restore a pontifex signet ring. (58 Archaeology, A cut dragonstone)	30	3.4%
295	Medium	Desert: General	Search the Grand Gold Chest in room 4 of Pyramid Plunder.	Search the Grand Gold Chest in room 4 of Pyramid Plunder in Sophanem. (51 Thieving)	30	4.5%
296	Medium	Desert: General	Search the Grand Gold Chest in room 5 of Pyramid Plunder.	Search the Grand Gold Chest in room 5 of Pyramid Plunder in Sophanem. (61 Thieving)	30	3.2%
297	Medium	Desert: General	Search the Grand Gold Chest in room 6 of Pyramid Plunder.	Search the Grand Gold Chest in room 6 of Pyramid Plunder in Sophanem. (71 Thieving)	30	2.3%
298	Medium	Desert: General	Complete the quest: Smoking Kills.	Complete Smoking Kills.	30	6.1%
299	Medium	Desert: General	Complete the quest: Desert Treasure.	Complete Desert Treasure.	30	0.8%
300	Medium	Desert: General	Fully repair the statue of Het.	Repair the statue of Het at Het's Oasis. (200 pieces of Het)	30	1.4%
347	Medium	Fremennik: Lunar Isles	Cast Moonclan Teleport.	Cast Moonclan Teleport. (69 Magic)	30	1.4%
348	Medium	Fremennik: Mainland	Move Your House to Rellekka.	Move your player-owned house's location to Rellekka. (30 Construction, 10,000 coins)	30	16.4%
349	Medium	Fremennik: Lunar Isles	Craft 50 Astral Runes.	Craft 50 astral runes. (40 Runecrafting, Completion of Lunar Diplomacy)	30	0.5%
350	Medium	Fremennik: Mainland	Complete the Penguin Agility Course.	Complete the Penguin Agility Course. (30 Agility, Completion of Cold War)	30	0.5%
351	Medium	Fremennik: Mainland	Catch a Snowy Knight.	Catch a Snowy Knight. (35 Hunter, A butterfly net and jar)	30	7.6%
352	Medium	Fremennik: Mainland	Defeat a Kurask in the Fremennik Province.	Defeat a Kurask in the Fremennik Province. (70 Slayer, Leaf-bladed spear or other special weapon)	30	8.6%
353	Medium	Fremennik: Mainland	Defeat a Dagannoth in the Fremennik Province.	Defeat a dagannoth in the Fremennik Province.	30	27.7%
354	Medium	Fremennik: Mainland	Equip a Helm of Neitiznot.	Equip a Helm of Neitiznot. (55 Defence, Completion of The Fremennik Isles)	30	1.6%
355	Medium	Fremennik: Mainland	Defeat a Jelly in the Fremennik Province.	Defeat a jelly in the Fremennik Province. (52 Slayer)	30	22.6%
356	Medium	Fremennik: Mainland	Complete the quest: Throne of Miscellania.	Complete Throne of Miscellania.	30	2.4%
357	Medium	Fremennik: Mainland	Complete the quest: Royal Trouble.	Complete Royal Trouble.	30	1.9%
358	Medium	Fremennik: Mainland	Equip a Granite Shield.	Equip a granite shield. (55 Defence, 55 Strength)	30	0.7%
359	Medium	Fremennik: Mainland	Equip a full set of Graahk, Larupia or Kyatt hunter gear.	Equip a full set of graahk, larupia or kyatt hunter gear. (31 Hunter)	30	2.3%
360	Medium	Fremennik: Mainland	Defeat any of the Dagannoth Kings.	Defeat any of the Dagannoth Kings 1 time.	30	9.9%
361	Medium	Fremennik: Mainland	Defeat any of the Dagannoth Kings.	Defeat any of the Dagannoth Kings 100 times.	30	1.1%
362	Medium	Fremennik: Mainland	Complete the task set: Easy Fremennik.	Complete the Easy Fremennik achievements.	30	1.3%
363	Medium	Fremennik: Mainland	Ride a mine cart into Keldagrim.	Ride a mine cart into Keldagrim. (Completion of The Giant Dwarf)	30	3.4%
364	Medium	Fremennik: Mainland	Travel to the Mammoth Iceberg.	Travel to the Mammoth Iceberg.	30	13.9%
365	Medium	Fremennik: Mainland	Steal from the fish stall in Rellekka.	Steal from the fish stall in Rellekka. (42 Thieving, Completion of The Fremennik Trials)	30	3%
366	Medium	Fremennik: Mainland	Harvest 100 sparkling energy from Sparkling Wisps.	Harvest 100 sparkling energy from sparkling wisps. (40 Divination)	30	32.2%
367	Medium	Fremennik: Mainland	Climb to the top of the lighthouse.	Climb to the top of the lighthouse. (Completion of Horror from the Deep)	30	2%
368	Medium	Fremennik: Mainland	Chop 10 Artic Pine trees.	Chop 10 arctic pine trees. (54 Woodcutting, Partial completion of The Fremennik Isles)	30	2.3%
369	Medium	Fremennik: Mainland	Kill 25 Yaks.	Kill 25 yaks. (Partial completion of The Fremennik Isles)	30	1.7%
370	Medium	Fremennik: Mainland	Interact with a pet rock.	Interact with a pet rock. (Partial completion of The Fremennik Trials)	30	3.3%
383	Medium	Fremennik: Mainland	Complete the task set: Medium Fremennik.	Complete the Medium Fremennik achievements.	30	<0.1%
131	Medium	Global	Reach level 50 in any skill.	Reach level 50 in any skill.	30	85.4%
132	Medium	Global	Reach at least level 5 in all non-elite skills.	Reach at least level 5 in all non-elite skills.	30	46.3%
133	Medium	Global	Reach at least level 10 in all non-elite skills.	Reach at least level 10 in all non-elite skills.	30	41.8%
134	Medium	Global	Reach at least level 20 in all non-elite skills.	Reach at least level 20 in all non-elite skills.	30	30.1%
138	Medium	Global	Reach combat level 50.	Reach combat level 50.	30	67.7%
143	Medium	Global	Reach total level 500.	Reach total level 500.	30	78%
157	Medium	Global	Mine any ore 200 times.	Mine any ore 200 times. (1 Mining)	30	86.8%
160	Medium	Global	Chop any tree 200 times.	Chop any tree 200 times. (1 Woodcutting)	30	66.2%
165	Medium	Global	Chop a willow tree.	Chop a willow tree. (20 Woodcutting)	30	76.9%
168	Medium	Global	Burn any logs 200 times.	Burn any logs 200 times. (1 Firemaking)	30	39.8%
178	Medium	Global	Catch any fish 200 times.	Catch any fish 200 times. (1 Fishing)	30	66.7%
187	Medium	Global	Harvest any memory from a wisp 200 times.	Harvest any memory from a wisp 200 times. (1 Divination)	30	63.3%
194	Medium	Global	Pickpocket anyone 200 times.	Pickpocket anyone 200 times. (1 Thieving)	30	44.7%
199	Medium	Global	Plant seeds in any farming patch 100 times.	Plant seeds in any farming patch 100 times. (1 Farming)	30	28.9%
202	Medium	Global	Unlock all of the Free to Play Lodestones.	Unlock all of the Free to Play Lodestones.	30	45.3%
771	Medium	Global	Make 200 potions of any kind.	Make 200 potions of any kind. (1 Herblore)	30	17.1%
780	Medium	Global	Clean 200 of any herb.	Clean 200 of any herb. (1 Herblore)	30	40%
784	Medium	Global	Fletch 1,000 arrow shafts.	Fletch 1,000 Arrow Shafts. (1 Fletching)	30	69.1%
787	Medium	Global	Complete 25 laps of any Agility course.	Complete 25 laps of any Agility course. (1 Agility)	30	44.2%
791	Medium	Global	Smith 25 of any metal weapon or armour piece.	Smith 25 of any metal weapon or armour piece. (1 Smithing)	30	72.6%
799	Medium	Global	Cook 200 fish.	Cook 200 fish. (1 Cooking)	30	55.1%
805	Medium	Global	Offer 100 bones of any kind to an altar.	Offer 100 bones (ashes also work) at the chaos altar in the Wilderness, the altar in Fort Forinthry, or an altar in the player-owned house chapel. (1 Prayer)	30	42.8%
808	Medium	Global	Scatter 100 ashes of any kind.	Scatter 100 ashes of any kind. (1 Prayer)	30	26.3%
810	Medium	Global	Restore 500 Prayer Points at an Altar at once.	Restore 500 Prayer Points at an Altar at once. (50 Prayer)	30	42.3%
814	Medium	Global	Catch 25 Implings of any kind.	Catch 25 implings of any kind. Cannot be completed in Puro-Puro. (17 Hunter)	30	5.2%
815	Medium	Global	Catch 35 Implings of any kind.	Catch 35 Implings of any kind. Cannot be completed in Puro-Puro. (17 Hunter)	30	3.5%
817	Medium	Global	Catch 200 Hunter creatures.	Catch 200 Hunter creatures. (1 Hunter)	30	14.6%
833	Medium	Global	Complete 25 Easy clue scrolls.	Complete 25 easy clue scrolls.	30	4.9%
834	Medium	Global	Complete 75 Easy clue scrolls.	Complete 75 easy clue scrolls.	30	0.4%
837	Medium	Global	Collect 25 unique items for the General clue rewards log.	Collect 25 unique items for the general clue rewards collection log.	30	15.3%
839	Medium	Global	Make 30 Prayer Potions.	Make 30 prayer potions. (38 Herblore)	30	20.9%
840	Medium	Global	Make a 4-dose Potion.	Make a 4-dose potion. (1 Herblore, A botanist's amulet, Morytania legs 4, Underworld Grimoire 1, or a varanusaur pen with a farm totem)	30	4.8%
841	Medium	Global	Make 20 Super Attack Potions.	Make 20 super attack potions. (45 Herblore)	30	13.8%
842	Medium	Global	Clean 50 Grimy Ranarr.	Clean 50 grimy ranarr. (25 Herblore)	30	27%
843	Medium	Global	Clean 50 Grimy Avantoe.	Clean 50 grimy avantoe. (48 Herblore)	30	9.5%
844	Medium	Global	Harvest 5 Grimy Ranarr.	Harvest 5 grimy ranarr. (32 Farming)	30	36.1%
845	Medium	Global	Equip an Iron Crossbow.	Equip an iron crossbow. (10 Ranged)	30	29.2%
846	Medium	Global	Equip a Maple shieldbow.	Equip a maple shieldbow. (30 Ranged, 30 Defence)	30	22.7%
847	Medium	Global	Fletch 50 Maple shieldbow (unstrung).	Fletch 50 unstrung maple shieldbows. (55 Fletching)	30	21.6%
848	Medium	Global	Fletch 400 Steel arrows.	Fletch 400 steel arrows. (30 Fletching)	30	39.5%
849	Medium	Global	Fletch 100 Iron bolts.	Fletch 100 iron bolts. (39 Fletching)	30	32%
850	Medium	Global	Mine Ore With a Rune Pickaxe.	Mine some ore with a rune pickaxe. (50 Mining)	30	53.6%
851	Medium	Global	Mine 20 Mithril Ore.	Mine 20 mithril ore. (30 Mining)	30	80%
852	Medium	Global	Mine 30 Adamant Ore.	Mine 30 adamantite ore. (40 Mining)	30	75.7%
853	Medium	Global	Mine 40 Runite Ore.	Mine 40 runite ore. (50 Mining)	30	70.6%
854	Medium	Global	Open 20 Igneous Geodes.	Open 20 igneous geodes. (60 Mining)	30	47.3%
855	Medium	Global	Check a grown Fruit Tree.	Check a tree grown in a fruit tree patch. (27 Farming)	30	32%
856	Medium	Global	Catch 100 Lobsters.	Catch 100 lobsters. (40 Fishing)	30	48.2%
857	Medium	Global	Catch 50 Swordfish.	Catch 50 swordfish. (50 Fishing)	30	36.6%
858	Medium	Global	Catch 50 Salmon.	Catch 50 salmon. (30 Fishing)	30	56.8%
859	Medium	Global	Catch 10 Pike.	Catch 10 pike. (25 Fishing)	30	54.9%
860	Medium	Global	Make a Pineapple pizza.	Make a pineapple pizza. (65 Cooking, Plain pizza and pineapple)	30	2.5%
861	Medium	Global	Make a Stew.	Make a stew. (25 Cooking)	30	11.9%
862	Medium	Global	Make a Chocolate Cake.	Make a chocolate cake. (50 Cooking, Cake and chocolate bar)	30	13.3%
863	Medium	Global	Bury some Baby Dragon bones.	Bury some baby dragon bones.	30	29.2%
864	Medium	Global	Bury 5 Dragon bones.	Bury 5 dragon bones. (1 Prayer)	30	36.5%
865	Medium	Global	Activate Protect from Melee prayer.	Activate the Protect from Melee prayer. (43 Prayer)	30	52.8%
866	Medium	Global	Catch a Gourmet Impling.	Catch a gourmet impling. Cannot be completed in Puro-Puro. (28 Hunter)	30	26.7%
867	Medium	Global	Light a Bullseye Lantern.	Light a bullseye lantern. (49 Firemaking)	30	10.5%
868	Medium	Global	Teleport using Law runes.	Teleport using law runes. (10 Magic)	30	49.8%
869	Medium	Global	Craft some Combination runes.	Craft some combination runes. (6 Runecrafting, A pure essence)	30	23.1%
870	Medium	Global	Craft 100 runes.	Craft 100 runes. (1 Runecrafting)	30	52.7%
871	Medium	Global	Craft 1,000 runes.	Craft 1,000 runes. (1 Runecrafting)	30	18.3%
874	Medium	Global	Equip a full set of Steel armour.	Equip a full set of steel armour. (20 Defence)	30	57.3%
875	Medium	Global	Equip a full set of Mithril armour.	Equip a full set of mithril armour. (30 Defence)	30	55%
876	Medium	Global	Equip a full set of Adamant armour.	Equip a full set of adamant armour. (40 Defence)	30	50.1%
877	Medium	Global	Equip a full set of Rune armour.	Equip a full set of rune armour. (50 Defence)	30	43.8%
878	Medium	Global	Equip a full set of Blue Dragonhide armour.	Equip a full set of blue dragonhide armour. (50 Defence)	30	18.3%
879	Medium	Global	Equip a full set of Red Dragonhide armour.	Equip a full set of red Dragonhide armour. (55 Defence)	30	6.5%
880	Medium	Global	Equip a full set of Batwing robes.	Equip a full set of batwing robes. (30 Defence)	30	47.5%
881	Medium	Global	Equip a full set of Mystic robes.	Equip a full set of mystic robes. (50 Defence)	30	21.3%
882	Medium	Global	Create a Mithril Grapple.	Create a mithril grapple. (59 Fletching, 30 Smithing)	30	9.1%
883	Medium	Global	Burn 25 Willow logs.	Burn 25 willow logs. (30 Firemaking)	30	60.9%
884	Medium	Global	Burn 50 Maple logs.	Burn 50 maple logs. (45 Firemaking)	30	34.7%
885	Medium	Global	Equip any elemental battlestaff.	Equip any elemental battlestaff. (30 Magic)	30	37.7%
886	Medium	Global	Equip a mystic staff.	Equip a mystic staff. (40 Magic)	30	27.7%
887	Medium	Global	Obtain 50 Quest Points.	Obtain 50 quest points.	30	59.5%
891	Medium	Global	Complete 100 clues of any tier.	Complete 100 clues of any tier.	30	6.7%
892	Medium	Global	Complete a Medium clue scroll.	Complete a medium clue scroll.	30	39.8%
893	Medium	Global	Complete 25 Medium clue scrolls.	Complete 25 medium clue scrolls.	30	8.1%
894	Medium	Global	Complete 75 Medium clue scrolls.	Complete 75 medium clue scrolls.	30	0.7%
896	Medium	Global	Complete a Hard clue scroll.	Complete a hard clue scroll.	30	36.1%
897	Medium	Global	Complete 25 Hard clue scrolls.	Complete 25 hard clue scrolls.	30	13.3%
900	Medium	Global	Collect 5 unique items for the Easy clue rewards log.	Collect 5 unique items for the easy clue rewards collection log.	30	37.8%
901	Medium	Global	Collect 10 unique items for the Easy clue rewards log.	Collect 10 unique items for the easy clue rewards collection log.	30	31.6%
905	Medium	Global	Collect 10 unique items for the Medium clue rewards log.	Collect 10 unique items for the Medium clue rewards collection log.	30	30.4%
908	Medium	Global	Collect 5 unique items for the Hard clue rewards log.	Collect 5 unique items for the hard clue rewards collection log.	30	32%
912	Medium	Global	Equip any 2 pieces of an Elegant outfit.	Equip any 2 pieces of an elegant outfit.	30	18.6%
913	Medium	Global	Equip a composite bow of any kind.	Equip a composite bow of any kind. (20 Ranged)	30	23.7%
943	Medium	Global	Perform a Special Attack.	Perform a special attack. (5 Attack or 5 Ranged or 5 Magic)	30	39.8%
1098	Medium	Global	Reach level 30 in any skill.	Reach level 30 in any skill.	30	93.6%
1099	Medium	Global	Reach level 40 in any skill.	Reach level 40 in any skill.	30	90.2%
1100	Medium	Global	Reach level 60 in any skill.	Reach level 60 in any skill.	30	79.7%
1105	Medium	Global	Reach at least level 30 in all non-elite skills.	Reach at least level 30 in all non-elite skills.	30	20.4%
415	Medium	Kandarin: Ardougne	Fletch 50 Maple shieldbow (unstrung) in Kandarin.	Fletch 50 unstrung maple shieldbows in Kandarin. (55 Fletching)	30	20.4%
416	Medium	Kandarin: Ardougne	Pickpocket a Knight of Ardougne 50 times.	Pickpocket a knight of Ardougne 50 times. (55 Thieving)	30	15.1%
417	Medium	Kandarin: Ardougne	Complete the Barbarian Outpost Agility Course.	Complete the Barbarian Outpost Agility Course. (35 Agility, Completion of Bar Crawl (miniquest))	30	7.1%
418	Medium	Global	Equip a Spottier Cape.	Equip a spottier cape. (66 Hunter)	30	1%
419	Medium	Kandarin: Ardougne	Catch a red salamander outside of Ourania Altar.	Catch a red salamander. (59 Hunter)	30	2.9%
420	Medium	Kandarin: Ardougne	Enter the Fishing Guild.	Enter the Fishing Guild. (68 Fishing)	30	16.1%
421	Medium	Kandarin: Gnomes	Check a grown Papaya Tree inside Tree Gnome Stronghold.	Check a grown papaya tree inside Tree Gnome Stronghold. (57 Farming)	30	4%
422	Medium	Kandarin: Ardougne	Kill a mithril dragon.	Defeat a mithril dragon.	30	4.6%
423	Medium	Kandarin: Yanille	Enter the Magic Guild in Yanille.	Enter the Wizards' Guild. (66 Magic)	30	16.4%
424	Medium	Kandarin: Ardougne	Defeat a Fire Giant in Kandarin.	Defeat a fire giant in Kandarin.	30	21.9%
425	Medium	Kandarin: Seers Village	Use the Chivalry Prayer.	Use the Chivalry prayer. (60 Prayer, 65 Defence, Completion of Knight Waves training ground)	30	1.1%
426	Medium	Kandarin: Yanille	Be on the winning side in a game of Castle Wars.	Win a game of Castle Wars.	30	0.2%
427	Medium	Kandarin: Seers Village	Complete the quest: Elemental Workshop II.	Complete Elemental Workshop II.	30	4.3%
428	Medium	Kandarin: Feldip Hills	Equip an Ogre Forester Hat.	Equip an ogre forester hat. (300 chompy bird kills)	30	<0.1%
429	Medium	Kandarin: Ardougne	Complete the task set: Easy Ardougne.	Complete the Easy Ardougne achievements.	30	0.9%
430	Medium	Kandarin: Gnomes	Create the listed gnome cocktails.	Complete The Great Gnomish Shake Off achievement. (37 Cooking)	30	3.9%
431	Medium	Kandarin: Ardougne	Earn a total amount of 10,000 beans.	Earn a total of 10,000 beans from selling animals in player-owned farm. (17 Farming)	30	0.2%
432	Medium	Global	Hunt 10 Spotted Kebbits with the help of a falcon.	Hunt 10 spotted kebbits using falconry. (43 Hunter)	30	4.1%
433	Medium	Global	Complete the quest: The Needle Skips.	Complete The Needle Skips.	30	3.6%
434	Medium	Kandarin: Ardougne	Complete the task set: Medium Ardougne.	Complete the Medium Ardougne achievements.	30	<0.1%
582	Medium	Karamja	Complete the task set: Easy Karamja.	Complete the Easy Karamja achievements.	30	10.1%
583	Medium	Karamja	Craft 50 Nature runes.	Craft 50 nature runes. (44 Runecrafting)	30	13%
584	Medium	Karamja	Catch a salmon on Karamja.	Catch a salmon on Karamja. (30 Fishing, Completion of Shilo Village)	30	5.7%
585	Medium	Karamja	Get Stiles to exchange fish for bank notes.	Get Stiles to exchange some of your fish for bank notes.	30	26.3%
586	Medium	Karamja	Convert 100 gleaming memories in an energy rift.	Convert 100 gleaming memories in an energy rift. (50 Divination)	30	26.5%
587	Medium	Karamja	Mine a drakolith rock in the Tai Bwo Wannai mine.	Mine a drakolith rock in the Tai Bwo Wannai mine. (60 Mining)	30	37.7%
588	Medium	Karamja	Mine a ruby from a gem rock in Shilo Village.	Mine a ruby from a gem rock in Shilo Village. (30 Mining, Completion of Shilo Village)	30	6.9%
589	Medium	Karamja	Enter the Hardwood Grove in Tai Bwo Wannai.	Enter the Hardwood Grove in Tai Bwo Wannai. (Completion of Jungle Potion)	30	4.7%
590	Medium	Karamja	Complete the quest: Dragon Slayer.	Complete Dragon Slayer.	30	25.8%
591	Medium	Karamja	Check a grown banana tree on Karamja.	Check a grown banana tree on Karamja. (33 Farming)	30	10.8%
592	Medium	Karamja	Defeat a TzHaar.	Defeat a TzHaar.	30	40.4%
593	Medium	Karamja	Equip an Obsidian cape.	Equip an obsidian cape.	30	2.8%
594	Medium	Karamja	Kill a metal dragon in Brimhaven Dungeon.	Kill a metal dragon in Brimhaven Dungeon.	30	16.9%
595	Medium	Karamja	Catch 25 lobsters on Karamja.	Catch 25 lobsters on Karamja. (40 Fishing)	30	42.9%
596	Medium	Karamja	Equip a Toktz-Ket-Xil.	Equip a Toktz-Ket-Xil. (60 Defence)	30	1.2%
597	Medium	Karamja	Equip a Tzhaar-Ket-Om.	Equip a Tzhaar-Ket-Om. (60 Strength)	30	1%
598	Medium	Karamja	Equip a Toktz-Xil-Ak.	Equip a Toktz-Xil-Ak. (60 Attack)	30	0.5%
599	Medium	Karamja	Equip a Toktz-Xil-Ek.	Equip a Toktz-Xil-Ek. (60 Attack)	30	0.6%
600	Medium	Karamja	Complete the task set: Medium Karamja.	Complete the Medium Karamja achievements.	30	<0.1%
1	Medium	Misthalin: Draynor Village	Kill the lesser demon in the Wizards' Tower.	Kill the lesser demon in the Wizards' Tower.	30	59.9%
6	Medium	Misthalin: Draynor Village	Hunt a yellow wizard in the RuneSpan.	Hunt a yellow wizard in the Runespan and give them some items. (1 Runecrafting)	30	31.2%
7	Medium	Misthalin: Draynor Village	Use the Rune Goldberg Machine to create Vis wax.	Use the Rune Goldberg Machine to create vis wax. (50 Runecrafting)	30	22.7%
8	Medium	Misthalin: Draynor Village	Siphon from a nature esshound in the Runespan.	Siphon from a nature esshound in the Runespan. (44 Runecrafting)	30	32.1%
9	Medium	Misthalin: Draynor Village	Siphon Rune dust from a RuneSphere in the RuneSpan.	Siphon rune dust from a Runesphere in the RuneSpan. (1 Runecrafting)	30	12.9%
17	Medium	Misthalin: Edgeville	Fully complete the Stronghold of Player Safety.	Fully complete the Stronghold of Player Safety.	30	39.8%
23	Medium	Misthalin: Fort Forinthry	Complete the quest: New Foundations.	Complete New Foundations.	30	38.2%
26	Medium	Misthalin: Lumbridge	Complete the task set: Beginner Lumbridge.	Complete all Beginner Tasks in Lumbridge.	30	48%
34	Medium	Misthalin: Draynor Village	Complete the quest: Duck Quest.	Complete Duck Quest.	30	27.6%
42	Medium	Misthalin: Lumbridge	Complete the task set: Easy Lumbridge.	Complete all Easy Tasks in Lumbridge.	30	22.4%
43	Medium	Misthalin: Lumbridge	Complete the task set: Medium Lumbridge.	Complete all Medium Tasks in Lumbridge.	30	7.3%
44	Medium	Misthalin: Lumbridge	Drink from the Tears of Guthix.	Drink from the Tears of Guthix. (Completion of Tears of Guthix (quest))	30	5.4%
45	Medium	Misthalin: Lumbridge	Complete world 25 in Shattered Worlds.	Reach world 25 in Shattered Worlds.	30	13.8%
46	Medium	Misthalin: Lumbridge	Catch 20 implings in Puro-Puro.	Catch 20 implings in Puro-Puro. (17 Hunter)	30	7.5%
47	Medium	Misthalin: Lumbridge	Complete the quest: Sheep Shearer (miniquest).	Complete Sheep Shearer miniquest.	30	63%
48	Medium	Misthalin: Lumbridge	Cut a willow tree east of Lumbridge Castle.	Cut the willow tree east of Lumbridge Castle, by the bridge across the River Lum. (20 Woodcutting)	30	66.3%
49	Medium	Misthalin: Lumbridge	Craft 50 Water Runes.	Craft 50 water runes. (5 Runecrafting, Water talisman or equivalent)	30	46.8%
50	Medium	Misthalin: Lumbridge	Pickpocket a H.A.M. member.	Pickpocket a H.A.M. member. (15 Thieving)	30	62.5%
51	Medium	Misthalin: Lumbridge	Churn some butter.	Make a pat of butter. (38 Cooking, Bucket of milk)	30	28%
52	Medium	Misthalin: Lumbridge	Craft 50 cosmic runes.	Craft 50 cosmic runes. (27 Runecrafting, Cosmic talisman or equivalent, completion of Lost City quest)	30	10.3%
53	Medium	Misthalin: Lumbridge	Steal a lantern from a cave goblin.	Steal a lantern from a cave goblin. (36 Thieving, Completion of Death to the Dorgeshuun quest)	30	0.9%
54	Medium	Misthalin: Lumbridge	Use the range in Lumbridge Castle to bake a cake.	Use the range in Lumbridge Castle to bake a cake. (40 Cooking, Completion of Cook's Assistant quest)	30	23.1%
68	Medium	Misthalin: City of Um	Have a conjured creature fight its matching creature.	Have either a Putrid Zombie or Vengeful Ghost conjured while fighting the matching creature. (40 Necromancy)	30	11.4%
69	Medium	Misthalin: City of Um	Learn how to craft moonstone jewellery.	Learn how to craft moonstone jewellery. (50 Necromancy, Brown apron or keepsaked override)	30	4.6%
70	Medium	Misthalin: City of Um	Disgruntle an inhabitant of Um by wearing a bedsheet.	Disgruntle an inhabitant of Um by wearing a bedsheet. (Completion of Ghosts Ahoy quest, bedsheet)	30	4.1%
71	Medium	Misthalin: City of Um	Upgrade Death Skull or Deathwarden equipment to tier 50.	Upgrade a piece of Death Skull or Deathwarden equipment to tier 50. (20 Necromancy, Completion of Necromancy! and Kili Row)	30	14.4%
72	Medium	Misthalin: City of Um	Complete a communion ritual using a memento.	Complete a communion ritual using a memento. (5 Necromancy, Completion of Necromancy!)	30	30.7%
73	Medium	Misthalin: City of Um	Conjure a Phantom Guardian at the City of Um ritual site.	Conjure a Phantom Guardian at the Um ritual site. (70 Necromancy)	30	5.6%
74	Medium	Misthalin: City of Um	Complete the task set: Easy Underworld.	Complete the Easy Underworld achievements.	30	21.4%
84	Medium	Misthalin: City of Um	Complete the task set: Medium Underworld.	Complete the Medium Underworld achievements.	30	5.8%
105	Medium	Misthalin: Varrock	Complete the task set: Easy Varrock.	Complete all Easy Tasks in Varrock.	30	4.4%
106	Medium	Misthalin: Varrock	Complete the task set: Medium Varrock.	Complete all Medium Tasks in Varrock.	30	<0.1%
107	Medium	Misthalin: Edgeville	Browse through Oziach's Armour Shop.	Browse through Oziach's Armour Shop. (Completion of Dragon Slayer quest)	30	23.3%
108	Medium	Misthalin: Varrock	Enter the Cooks' Guild.	Enter the Cooks' Guild. (32 Cooking, Chef's hat)	30	42.1%
109	Medium	Misthalin: Varrock	Complete the quest: Demon Slayer.	Complete Demon Slayer.	30	43%
110	Medium	Misthalin: Varrock	Complete the quest: Vampyre Slayer.	Complete Vampyre Slayer.	30	47.3%
111	Medium	Misthalin: Varrock	Mine 50 pure essence.	Mine 50 pure essence. (30 Mining)	30	68.2%
112	Medium	Misthalin: Varrock	Pickpocket a guard in Varrock Palace's courtyard.	Pickpocket a Varrock guard. (40 Thieving)	30	35%
113	Medium	Misthalin: Varrock	Gather and convert 50 bright memories.	Gather and convert 50 bright memories. (20 Divination)	30	48.8%
704	Medium	Morytania	Complete the task set: Easy Morytania.	Complete the Easy Morytania achievements.	30	0.2%
705	Medium	Morytania	Take a medium companion through a medium route of Temple Trekking.	Take a medium companion through a medium route of Temple Trekking. (Completion of In Aid of the Myreque)	30	0.5%
706	Medium	Morytania	Visit Mos Le'Harmless.	Visit Mos Le'Harmless. (Partial completion of Cabin Fever)	30	2.3%
707	Medium	Morytania	Visit Harmony Island.	Visit Harmony Island. (Partial completion of The Great Brain Robbery)	30	0.1%
708	Medium	Morytania	Visit the Everlight dig site.	Visit the Everlight dig site. (42 Archaeology)	30	22.4%
709	Medium	Morytania	Finish a game of Werewolf Skullball.	Finish a game of Werewolf Skullball. (25 Agility, Completion of Creature of Fenkenstrain)	30	0.6%
710	Medium	Morytania	Defeat the six Barrows Brothers and loot their chest.	Defeat the six Barrows Brothers and loot their chest once.	30	22.3%
711	Medium	Morytania	Defeat the six Barrows Brothers and loot their chest. (100 times)	Defeat the six Barrows Brothers and loot their chest 100 times.	30	0.1%
712	Medium	Morytania	Equip a Barrows weapon.	Equip a barrows weapon. (70 Magic, 70 Attack, or 70 Ranged)	30	4.6%
713	Medium	Morytania	Equip a piece of Barrows armour.	Equip a piece of barrows armour. (70 Defence)	30	10.5%
714	Medium	Morytania	Equip a Salve Amulet (e).	Equip a salve amulet (e). (Completion of Lair of Tarn Razorlor (miniquest))	30	7.8%
715	Medium	Morytania	Make a batch of cannonballs in Port Phasmatys.	Make a batch of cannonballs in Port Phasmatys. (35 Smithing, Completion of Dwarf Cannon)	30	1.5%
716	Medium	Morytania	Catch 10 Green salamanders.	Catch 10 Green salamanders. (29 Hunter)	30	10.5%
717	Medium	Morytania	Complete the quest: Haunted Mine.	Complete Haunted Mine.	30	15.5%
718	Medium	Morytania	Harvest bittercap mushrooms near Canifis.	Harvest bittercap mushrooms in the farming patch near Canifis. (53 Farming)	30	7.6%
719	Medium	Morytania	Complete the task set: Medium Morytania.	Complete the Medium Morytania achievements.	30	<0.1%
523	Medium	Elven Lands: Tirranwn	Complete the task set: Easy Tirannwn.	Complete the Easy Tirannwn achievements.	30	0.1%
524	Medium	Elven Lands: Tirranwn	Check a grown Papaya Tree in Lletya.	Check a grown papaya tree in Lletya. (57 Farming)	30	5.1%
525	Medium	Elven Lands: Tirranwn	Craft 50 Death Runes.	Craft 50 death runes. (65 Runecrafting)	30	2.4%
526	Medium	Elven Lands: Tirranwn	Move your house to Prifddinas.	Move your player-owned house's location to Prifddinas. (75 Construction, 50,000 coins)	30	2.3%
527	Medium	Elven Lands: Tirranwn	Use an Elven Teleport Crystal.	Use a crystal teleport seed.	30	18.7%
528	Medium	Elven Lands: Tirranwn	Equip Iban's staff.	Equip Iban's staff. (50 Magic)	30	2.8%
529	Medium	Elven Lands: Tirranwn	Catch 10 Pawyas in Isafdar.	Catch 10 pawyas in Isafdar. (66 Hunter)	30	0.3%
530	Medium	Elven Lands: Tirranwn	Mine 200 soft clay in Prifddinas.	Mine 200 soft clay in Prifddinas. (75 Mining)	30	27.6%
531	Medium	Elven Lands: Tirranwn	Use the fairy ring in the Amlodd district.	Use the fairy ring in the Amlodd district. (Partial completion of A Fairy Tale II - Cure a Queen)	30	4.3%
532	Medium	Elven Lands: Tirranwn	Complete the task set: Medium Tirannwn.	Complete the Medium Tirannwn achievements.	30	<0.1%
640	Medium	Wilderness: General	Complete the task set: Easy Wilderness.	Complete the Easy Wilderness achievements.	30	10.5%
641	Medium	Wilderness: General	Defeat the King Black Dragon.	Defeat the King Black Dragon once.	30	29.8%
642	Medium	Wilderness: General	Defeat the King Black Dragon. (100 times)	Defeat the King Black Dragon 100 times.	30	0.6%
643	Medium	Wilderness: General	Sacrifice Dragon bones on the Chaos Altar.	Sacrifice dragon bones on the chaos altar in the Wilderness. (1 Prayer)	30	37.1%
644	Medium	Wilderness: General	Cast the Claws of Guthix special attack.	Cast the Claws of Guthix special attack. (60 Magic, Completion of Mage Arena, Guthix staff)	30	6.1%
645	Medium	Wilderness: General	Defeat 5 Green dragons.	Defeat 5 green dragons.	30	36.9%
646	Medium	Wilderness: General	Complete 10 laps of the Wilderness agility course.	Complete 10 laps of the Wilderness agility course. (52 Agility)	30	21.6%
647	Medium	Wilderness: General	Equip a Saradomin, Zamorak, or Guthix cape.	Equip a Saradomin, Zamorak, or Guthix cape. (60 Magic, Completion of Mage Arena)	30	10.8%
648	Medium	Wilderness: General	Visit any Runecrafting altar through the Abyss.	Visit any Runecrafting altar through the Abyss. (Completion of Enter the Abyss (miniquest))	30	32.7%
649	Medium	Wilderness: General	Defeat 10 Fetid Zombies.	Defeat 10 fetid zombies.	30	31.6%
650	Medium	Wilderness: General	Defeat 20 Bound Skeletons.	Defeat 20 bound skeletons.	30	17.7%
651	Medium	Wilderness: Daemonheim	Defeat the Rammernaut.	Defeat the Rammernaut. (35 Dungeoneering)	30	2.3%
652	Medium	Wilderness: General	Defeat Bossy McBoss Face.	Defeat Bossy McBoss Face.	30	2.9%
653	Medium	Wilderness: General	Activate and teleport from each Wilderness obelisk.	Activate and teleport from each of the Wilderness teleport obelisks.	30	12.5%
654	Medium	Wilderness: General	Defeat Bossy McBossface's first mate.	Defeat Bossy McBossface's first mate.	30	1.4%
655	Medium	Wilderness: General	Complete the task set: Medium Wilderness.	Complete the Medium Wilderness achievements.	30	1.2%
472	Hard	Anachronia	Harvest produce from 25 animals on Anachronia farm.	Harvest produce from 25 animals on Anachronia farm. (42 Farming, 45 Construction)	80	0.1%
475	Hard	Anachronia	Complete the ritual to activate a totem on Anachronia.	Complete the ritual to activate a totem on Anachronia.	80	0.1%
476	Hard	Anachronia	Complete the Anachronia agility course in under 7 minutes.	Complete the Anachronia agility course in under 7 minutes. (85 Agility)	80	1.5%
477	Hard	Anachronia	Complete all frog breeds.	Complete all frog breeds. (42 Farming, 45 Construction)	80	<0.1%
478	Hard	Anachronia	Purchase the Quick Traps upgrade from Irwinsson's Hunter Mark shop.	Purchase the quick traps upgrade from the Hunter Mark Shop. (50 hunter marks)	80	0.1%
479	Hard	Anachronia	Complete the quest: Osseous Rex.	Complete the Osseous Rex quest.	80	1.2%
480	Hard	Anachronia	Clear an Overgrown idol on Anachronia.	Clear an overgrown idol on Anachronia. (81 Woodcutting)	80	0.6%
481	Hard	Anachronia	Defeat any of the Rex Matriarchs.	Defeat any of the Rex Matriarchs once.	80	9.1%
482	Hard	Anachronia	Defeat any of the Rex Matriarchs. (100 times)	Defeat any of the Rex Matriarchs 100 times.	80	2.3%
483	Hard	Anachronia	Complete the quest: Desperate Times.	Complete the Desperate Times quest.	80	1.7%
484	Hard	Anachronia	Find all the hidden Zygomites on Anachronia.	Find all of the ancient zygomites on Anachronia. (85 Agility)	80	0.1%
485	Hard	Anachronia	Equip Laniakea's spear.	Equip Laniakea's spear. (82 Attack)	80	2.2%
486	Hard	Anachronia	Harvest an Arbuck herb.	Harvest an arbuck herb. (77 Farming)	80	5.6%
487	Hard	Anachronia	Complete the advanced sections of the Anachronia agility course.	Complete the advanced sections of the Anachronia agility course. (70 Agility)	80	6.3%
488	Hard	Anachronia	Equip a Dragon Mattock.	Equip a dragon mattock. (60 Archaeology, (optional) 75 Hunter)	80	0.1%
490	Hard	Anachronia	Take down each dinosaur in Big Game Hunter.	Take down each dinosaur in Big Game Hunter. (96 Hunter, 76 Slayer)	80	<0.1%
492	Hard	Anachronia	Get caught by each of the big game creatures once.	Get caught by each of the Big Game Hunter creatures once. (96 Hunter, 76 Slayer)	80	<0.1%
493	Hard	Anachronia	Complete a big game encounter without using movement abilities.	Complete a Big Game Hunter encounter without using movement abilities. (75 Hunter, 55 Slayer)	80	0.4%
500	Hard	Anachronia	Defeat Raksha, the Shadow Colossus.	Defeat Raksha, the Shadow Colossus once. (Completion of Raksha, the Shadow Colossus (quest))	80	0.5%
236	Hard	Asgarnia: Falador	Reach 100% respect at the Artisans' Workshop.	Reach 100% respect at the Artisans' Workshop. (1 Smithing)	80	30.1%
237	Hard	Asgarnia: Falador	Complete the task set: Hard Falador.	Complete the Hard Falador achievements.	80	<0.1%
246	Hard	Asgarnia: Burthorpe	Defeat any God Wars Dungeon boss 100 times.	Defeat any God Wars Dungeon boss 100 times. (Partial completion of Troll Stronghold)	80	17.5%
247	Hard	Asgarnia: Burthorpe	Defeat any God Wars Dungeon boss 250 times.	Defeat any God Wars Dungeon boss 250 times. (Partial completion of Troll Stronghold)	80	7.1%
248	Hard	Asgarnia: Burthorpe	Defeat Commander Zilyana.	Defeat Commander Zilyana. (70 Agility, Partial completion of Troll Stronghold)	80	5.5%
249	Hard	Asgarnia: Burthorpe	Defeat General Graardor.	Defeat General Graardor. (70 Strength, Partial completion of Troll Stronghold)	80	16.1%
250	Hard	Asgarnia: Burthorpe	Defeat K'ril Tsutsaroth.	Defeat K'ril Tsutsaroth. (70 Constitution, Partial completion of Troll Stronghold)	80	12.6%
251	Hard	Asgarnia: Burthorpe	Defeat Kree'arra.	Defeat Kree'arra. (70 Ranged, Partial completion of Troll Stronghold)	80	3.1%
252	Hard	Asgarnia: Burthorpe	Defeat Nex.	Defeat Nex. (70 Agility, 70 Strength, 70 Constitution, 70 Ranged, Partial completion of Troll Stronghold, completion of The Dig Site, frozen key)	80	1.2%
253	Hard	Asgarnia: Burthorpe	Defeat Kree'arra. (100 times)	Defeat Kree'arra 100 times. (70 Ranged, Partial completion of Troll Stronghold)	80	0.2%
254	Hard	Asgarnia: Burthorpe	Assemble any godsword from the God Wars Dungeon.	Assemble any godsword from the God Wars Dungeon. (80 Smithing and one of 70 Agility, 70 Strength, 70 Constitution, or 70 Ranged)	80	1.4%
264	Hard	Asgarnia: Port Sarim	Defeat the Queen Black Dragon.	Defeat the Queen Black Dragon. (60 Summoning)	80	4.3%
265	Hard	Asgarnia: Port Sarim	Defeat the Queen Black Dragon. (100 times)	Defeat the Queen Black Dragon 100 times. (60 Summoning)	80	0.1%
266	Hard	Asgarnia: Port Sarim	Bury some frost dragon bones.	Bury some frost dragon bones. (85 Dungeoneering)	80	1%
301	Hard	Desert: General	Defeat the Kalphite King.	Defeat the Kalphite King.	80	6.5%
302	Hard	Desert: General	Defeat the Kalphite King. (100 times)	Defeat the Kalphite King 100 times.	80	0.2%
303	Hard	Desert: General	Equip a drygore weapon.	Equip a drygore weapon. (90 Attack)	80	2.3%
304	Hard	Desert: General	Become an honorary druid at the Garden of Kharid.	Purchase the Druid/Druidess title for 50,000 Crux Eqal favour. (50 Farming)	80	1.3%
305	Hard	Desert: General	Deploy a dreadnip.	Deploy a dreadnip. (20 of a collection of quests, 450 Dominion Tower kills)	80	<0.1%
306	Hard	Desert: General	Complete the task set: Hard Desert.	Complete the Hard Desert achievements.	80	<0.1%
307	Hard	Desert: General	Defeat Avaryss and Nymora.	Defeat the Twin Furies. (80 Ranged)	80	2.2%
308	Hard	Desert: General	Defeat Gregorovic.	Defeat Gregorovic. (80 Prayer)	80	4.9%
309	Hard	Desert: General	Defeat Vindicta and Gorvek.	Defeat Vindicta. (80 Attack)	80	15.2%
310	Hard	Desert: General	Defeat Helwyr.	Defeat Helwyr. (80 Magic)	80	4.3%
311	Hard	Desert: General	Defeat Avaryss and Nymora. (100 times)	Defeat the Twin Furies 100 times. (80 Ranged)	80	0.1%
312	Hard	Desert: General	Defeat Gregorovic. (100 times)	Defeat Gregorovic 100 times. (80 Prayer)	80	0.1%
313	Hard	Desert: General	Defeat Vindicta and Gorvek. (100 times)	Defeat Vindicta 100 times. (80 Attack)	80	2.6%
314	Hard	Desert: General	Defeat Helwyr. (100 times)	Defeat Helwyr 100 times. (80 Magic)	80	0.2%
315	Hard	Desert: General	Equip a Dragon Rider lance.	Equip a Dragon Rider lance. (85 Attack)	80	6%
316	Hard	Desert: General	Equip a wand or orb of the Cywir elders.	Equip a wand or orb of the Cywir elders. (85 Magic)	80	0.6%
317	Hard	Desert: General	Equip a shadow glaive.	Equip a shadow glaive. (85 Ranged)	80	0.1%
318	Hard	Desert: General	Equip a blade of Nymora or Avaryss.	Equip a blade of Nymora or Avaryss. (85 Attack)	80	0.3%
319	Hard	Desert: Menaphos	Slay 500 corrupted or devourer creatures.	Slay a combination of 500 corrupted creatures or soul devourers. (88 Slayer, Completion of Icthlarin's Little Helper)	80	0.3%
320	Hard	Desert: General	Defeat the Magister.	Defeat the Magister. (115 Slayer, Key to the Crossing)	80	0.1%
321	Hard	Desert: General	Defeat the Magister. (50 times)	Defeat the Magister 50 times. (115 Slayer, Key to the Crossing)	80	<0.1%
322	Hard	Desert: Menaphos	Find an Off-hand khopesh of the Kharidian in Shifting Tombs.	Find an off-hand khopesh of the Kharidian in Shifting Tombs. (At least one of 50 Dungeoneering, 50 Agility, 50 Thieving, or 50 Construction)	80	<0.1%
323	Hard	Desert: General	Search the Grand Gold Chest in room 7 of Pyramid Plunder.	Search the Grand Gold Chest in room 7 of Pyramid Plunder in Sophanem. (81 Thieving, Partial completion of Icthlarin's Little Helper)	80	2%
324	Hard	Desert: General	Search the Grand Gold Chest in room 8 of Pyramid Plunder.	Search the Grand Gold Chest in room 8 of Pyramid Plunder in Sophanem. (91 Thieving, Partial completion of Icthlarin's Little Helper)	80	1.8%
325	Hard	Desert: Menaphos	Complete the quest: Beneath Scabaras' Sands.	Complete Beneath Scabaras' Sands.	80	<0.1%
326	Hard	Desert: General	Kill a desert strykewyrm with specific gear.	Kill a desert strykewyrm wearing a full Slayer helm and wielding an ancient staff. (77 Slayer, 50 Magic, 20 Defence, 55 Crafting)	80	<0.1%
328	Hard	Desert: General	Defeat Telos, the Warden.	Defeat Telos, the Warden. (80 Attack, 80 Prayer, 80 Magic, 80 Ranged)	80	1.2%
371	Hard	Fremennik: Lunar Isles	Cast Fertile Soil.	Cast Fertile Soil. (83 Magic, Completion of Lunar Diplomacy)	80	1%
372	Hard	Fremennik: Mainland	Build a Gilded Altar.	Build a gilded altar in your player-owned house's chapel. (75 Construction)	80	1%
373	Hard	Fremennik: Mainland	Trap a Sabre-Toothed Kyatt.	Trap a sabre-toothed kyatt. (55 Hunter)	80	5.1%
374	Hard	Fremennik: Mainland	Defeat all Dagannoth Kings without leaving a solo instance.	Defeat all the Dagannoth Kings without leaving a solo boss instance.	80	1.2%
375	Hard	Fremennik: Mainland	Equip a Berserker, Warrior, Seers, or Archers Ring.	Equip a Berserker, Warrior, Seers, or Archers Ring.	80	4.3%
376	Hard	Fremennik: Mainland	Use the Special Attack of a Dragon Axe.	Use the special attack of a dragon hatchet. (60 Attack)	80	2.1%
377	Hard	Fremennik: Mainland	Defeat a Dagannoth King solo with specific gear.	Defeat a Dagannoth King solo whilst wearing full yak-hide armour and a Fremennik round shield. (25 Defence, Partial completion of The Fremennik Isles)	80	0.2%
378	Hard	Fremennik: Mainland	Equip a full set of Skeletal, Spined, or Rockshell armour.	Equip a full skeletal, spined, or rock-shell armour set. (50 Defence, Completion of The Fremennik Trials)	80	0.2%
379	Hard	Fremennik: Mainland	Collect Miscellania Resources at Full Approval.	Collect from Managing Miscellania with a 100% approval rating. (Completion of Throne of Miscellania)	80	0.9%
380	Hard	Fremennik: Mainland	Travel to the island of Ungael.	Travel to the island of Ungael. (Partial completion of Ancient Awakening)	80	0.3%
381	Hard	Fremennik: Mainland	Adopt a baby yak.	Obtain an unchecked/baby Fremennik yak. (71 Farming, Partial completion of The Fremennik Isles)	80	0.1%
382	Hard	Fremennik: Mainland	Catch 50 Azure Skillchompas.	Catch 50 azure skillchompas. (68 Hunter)	80	0.9%
384	Hard	Fremennik: Mainland	Mine 10 Banite Ore north of Rellekka.	Mine 10 Banite ore in the arctic (azure) habitat mine. (80 Mining)	80	37.2%
385	Hard	Fremennik: Mainland	Smith a piece of Bane equipment to +4 in Rellekka.	Upgrade a piece of bane equipment to +4 in Rellekka. (80 Smithing, Completion of The Fremennik Trials)	80	3%
386	Hard	Fremennik: Mainland	Use a Crystal triskelion key to obtain some treasures.	Use a crystal triskelion to obtain some treasures.	80	9.9%
388	Hard	Fremennik: Mainland	Create a Catherby Teleport Tablet.	Create a Catherby teleport tablet. (87 Magic, 67 Construction, Completion of Lunar Diplomacy)	80	0.1%
392	Hard	Fremennik: Mainland	Gather a seed from an Aquanite using Seedicide.	Gather a seed from an aquanite using Seedicide. (78 Slayer)	80	3.8%
393	Hard	Fremennik: Mainland	Complete the task set: Hard Fremennik.	Complete the Hard Fremennik achievements.	80	<0.1%
135	Hard	Global	Reach at least level 50 in all non-elite skills.	Reach at least level 50 in all non-elite skills.	80	8.2%
139	Hard	Global	Reach combat level 100.	Reach combat level 100.	80	34%
144	Hard	Global	Reach total level 1000.	Reach total level 1000.	80	60.1%
158	Hard	Global	Mine any ore 1000 times.	Mine any ore 1000 times. (1 Mining)	80	72.7%
161	Hard	Global	Chop any tree 1000 times.	Chop any tree 1000 times. (1 Woodcutting)	80	20.7%
169	Hard	Global	Burn any logs 1000 times.	Burn any logs 1000 times. (1 Firemaking)	80	5.9%
179	Hard	Global	Catch any fish 1000 times.	Catch any fish 1000 times. (1 Fishing)	80	19.6%
188	Hard	Global	Harvest any memory from a wisp 1000 times.	Harvest any memory from a wisp 1000 times. (1 Divination)	80	22.9%
195	Hard	Global	Pickpocket anyone 1000 times.	Pickpocket anyone 1000 times. (1 Thieving)	80	12.8%
203	Hard	Global	Unlock all of the Lodestones.	Unlock all of the lodestones.	80	0.2%
772	Hard	Global	Make 1,000 potions of any kind.	Make 1,000 potions of any kind. (1 Herblore)	80	3%
781	Hard	Global	Clean 1,000 of any herb.	Clean 1,000 of any herb. (1 Herblore)	80	20%
788	Hard	Global	Complete 50 laps of any Agility course.	Complete 50 laps of any Agility course. (1 Agility)	80	23.9%
789	Hard	Global	Complete 100 laps of any Agility course.	Complete 100 laps of any Agility course. (1 Agility)	80	7.8%
792	Hard	Global	Smith 50 of any metal weapon or armour piece.	Smith 50 of any metal weapon or armour piece. (1 Smithing)	80	63.3%
793	Hard	Global	Smith 100 of any metal weapon or armour piece.	Smith 100 of any metal weapon or armour piece. (1 Smithing)	80	50.3%
800	Hard	Global	Cook 1,000 fish.	Cook 1,000 fish. (1 Cooking)	80	10.7%
818	Hard	Global	Catch 1,000 Hunter creatures.	Catch 1,000 Hunter creatures. (1 Hunter)	80	2%
820	Hard	Global	Complete 15 Slayer tasks.	Complete 15 Slayer tasks. (1 Slayer)	80	18.7%
835	Hard	Global	Complete 150 Easy clue scrolls.	Complete 150 easy clue scrolls.	80	0.2%
838	Hard	Global	Collect 50 unique items for the General clue rewards log.	Collect 50 unique items for the general clue rewards collection log.	80	0.1%
872	Hard	Global	Craft 10,000 runes.	Craft 10,000 runes. (1 Runecrafting)	80	0.4%
873	Hard	Global	Craft 20,000 runes.	Craft 20,000 runes. (1 Runecrafting)	80	0.2%
888	Hard	Global	Obtain 75 Quest Points.	Obtain 75 quest points.	80	30.1%
889	Hard	Global	Obtain 100 Quest Points.	Obtain 100 quest points.	80	11.4%
895	Hard	Global	Complete 150 Medium clue scrolls.	Complete 150 medium clue scrolls.	80	0.2%
898	Hard	Global	Complete 75 Hard clue scrolls.	Complete 75 hard clue scrolls.	80	2%
899	Hard	Global	Complete 150 Hard clue scrolls.	Complete 150 hard clue scrolls.	80	0.3%
902	Hard	Global	Collect 25 unique items for the Easy clue rewards log.	Collect 25 unique items for the easy clue rewards collection log.	80	15.5%
903	Hard	Global	Collect 50 unique items for the Easy clue rewards log.	Collect 50 unique items for the easy clue rewards collection log.	80	2.7%
906	Hard	Global	Collect 25 unique items for the Medium clue rewards log.	Collect 25 unique items for the medium clue rewards collection log.	80	20.3%
907	Hard	Global	Collect 50 unique items for the Medium clue rewards log.	Collect 50 unique items for the medium clue rewards collection log.	80	8.9%
909	Hard	Global	Collect 10 unique items for the Hard clue rewards log.	Collect 10 unique items for the hard clue rewards collection log.	80	28.9%
910	Hard	Global	Collect 25 unique items for the Hard clue rewards log.	Collect 25 unique items for the hard clue rewards collection log.	80	22.9%
914	Hard	Global	Equip any Dragon mask.	Equip any dragon mask.	80	24.2%
915	Hard	Global	Make any Perfect Juju Potion.	Make any perfect juju potion. (75 Herblore)	80	0.1%
916	Hard	Global	Make 15 Antifire Potions.	Make 15 antifire potions. (69 Herblore)	80	3%
917	Hard	Global	Clean 50 Grimy Cadantine.	Clean 50 grimy cadantine. (65 Herblore)	80	3.7%
918	Hard	Global	Clean 100 Grimy Lantadyme.	Clean 100 grimy lantadyme. (67 Herblore)	80	5.5%
919	Hard	Global	Clean 100 Dwarf Weed.	Clean 100 grimy dwarf weed. (70 Herblore)	80	4%
920	Hard	Global	Clean 100 Arbuck.	Clean 100 grimy arbuck. (77 Herblore, 77 Farming)	80	1%
921	Hard	Global	Equip a Yew shortbow.	Equip a yew shortbow. (40 Ranged)	80	21.5%
922	Hard	Global	Equip a Magic shortbow.	Equip a magic shortbow. (50 Ranged)	80	14.6%
923	Hard	Global	Fletch some Broad Arrows or Bolts.	Fletch some broad arrows or bolts. (52 Fletching, Completion of Smoking Kills, 300 slayer points)	80	4.6%
924	Hard	Global	Fletch 100 Yew shortbows (unstrung).	Fletch 100 Yew shortbows (unstrung). (65 Fletching)	80	8.1%
925	Hard	Global	Fletch 100 Yew stocks.	Fletch 100 yew stocks. (69 Fletching)	80	6.7%
926	Hard	Global	Fletch a Rune Crossbow.	Fletch a rune crossbow. (69 Fletching)	80	7.3%
927	Hard	Global	Fletch 35 or more arrow shafts from a single log.	Fletch 35 or more arrow shafts from a single log. (60 Fletching, Yew logs or higher)	80	13.8%
928	Hard	Global	Fletch 500 Adamant arrows.	Fletch 500 adamant arrows. (60 Fletching)	80	20.9%
929	Hard	Global	Fletch 750 Rune arrows.	Fletch 750 rune arrows. (75 Fletching)	80	11.8%
930	Hard	Global	Fletch 75 Onyx bolts.	Fletch 75 onyx bolts. (73 Fletching)	80	2.8%
931	Hard	Global	Equip a Rune Ceremonial Sword.	Equip a rune ceremonial sword.	80	0.8%
932	Hard	Global	Equip a full set of the Blacksmith's outfit.	Equip a full set of the blacksmith's outfit. (1 Smithing, Total of 250% Artisans' Workshop respect)	80	8.8%
933	Hard	Global	Power up the Artisan's Workshop with a Luminite Injector.	Power up the Artisan's Workshop with a luminite Injector. (1 Smithing, 100% Artisans' Workshop respect)	80	9.6%
934	Hard	Global	Mine 50 Orichalcite Ore.	Mine 50 orichalcite ore. (60 Mining)	80	63.4%
935	Hard	Global	Mine 50 Drakolith.	Mine 50 drakolith. (60 Mining)	80	52.2%
936	Hard	Global	Mine 60 Necrite Ore.	Mine 60 necrite ore. (70 Mining)	80	50.6%
937	Hard	Global	Mine 60 Phasmatite.	Mine 60 phasmatite. (70 Mining)	80	46%
938	Hard	Global	Harvest 20 Grimy Kwuarm.	Harvest 20 grimy kwuarm. (56 Farming)	80	16.9%
939	Hard	Global	Catch 100 Shark.	Catch 100 raw sharks. (76 Fishing)	80	4.8%
940	Hard	Global	Catch 100 Green Blubber Jellyfish.	Catch 100 green blubber jellyfish. (68 Fishing)	80	7.5%
941	Hard	Global	Catch a Spirit Impling.	Catch a spirit impling. Cannot be completed in Puro-Puro. (54 Hunter)	80	6.2%
942	Hard	Global	Equip a Slayer helmet.	Equip a Slayer helmet. (55 Crafting, 35 Slayer, Completion of Smoking Kills, 400 slayer points)	80	0.7%
944	Hard	Global	Complete a Soul Reaper task.	Complete a Soul Reaper task.	80	34.2%
945	Hard	Global	Complete 5 Soul Reaper tasks.	Complete 5 Soul Reaper tasks.	80	13.1%
947	Hard	Global	Equip a full set of Orikalkum armour.	Equip a full set of orikalkum armour. (60 Smithing, 60 Defence)	80	39%
948	Hard	Global	Equip a full set of Necronium armour.	Equip a full set of necronium armour. (70 Smithing, 70 Defence)	80	28.3%
949	Hard	Global	Equip a full set of Black Dragonhide armour.	Equip a full set of black dragonhide armour. (60 Defence, 60 Crafting)	80	14.3%
950	Hard	Global	Equip a full set of Royal Dragonhide armour.	Equip a full set of royal dragonhide armour. (65 Defence, 65 Crafting)	80	8.5%
951	Hard	Global	Cast a Wave spell.	Cast a wave spell. (62 Magic)	80	23.6%
952	Hard	Global	Burn 75 Yew logs.	Burn 75 yew logs. (60 Firemaking)	80	11.2%
953	Hard	Global	Unlock the Ring of Quests from May's Quest Caravan.	Unlock the Ring of Quests from May's Quest Caravan. (75 Quest points)	80	11.2%
954	Hard	Global	Complete 250 clues of any tier.	Complete 250 clues of any tier.	80	0.4%
955	Hard	Global	Complete 500 clues of any tier.	Complete 500 clues of any tier.	80	<0.1%
956	Hard	Global	Complete an Elite clue scroll.	Complete an elite clue scroll.	80	29.1%
957	Hard	Global	Complete 25 Elite clue scrolls.	Complete 25 elite clue scrolls.	80	4%
960	Hard	Global	Complete a Master clue scroll.	Complete a master clue scroll.	80	30.7%
964	Hard	Global	Collect 5 unique items for the Elite clue rewards log.	Collect 5 unique items for the elite clue rewards collection log.	80	24%
965	Hard	Global	Collect 10 unique items for the Elite clue rewards log.	Collect 10 unique items for the elite clue rewards collection log.	80	19.8%
966	Hard	Global	Collect 20 unique items for the Elite clue rewards log.	Collect 20 unique items for the elite clue rewards collection log.	80	14.6%
968	Hard	Global	Collect 5 unique items for the Master clue rewards log.	Collect 5 unique items for the master clue rewards collection log.	80	25.9%
1002	Hard	Global	Catch a Manta ray.	Catch a raw manta ray. (81 Fishing)	80	5.7%
1101	Hard	Global	Reach level 70 in any skill.	Reach level 70 in any skill.	80	70.4%
1102	Hard	Global	Reach level 80 in any skill.	Reach level 80 in any skill.	80	59.2%
1106	Hard	Global	Reach at least level 40 in all non-elite skills.	Reach at least level 40 in all non-elite skills.	80	13.9%
1107	Hard	Global	Reach at least level 60 in all non-elite skills.	Reach at least level 60 in all non-elite skills.	80	2.9%
1108	Hard	Global	Reach at least level 70 in all non-elite skills.	Reach at least level 70 in all non-elite skills.	80	0.7%
435	Hard	Kandarin: Ardougne	Throw coins into the deep sea whirlpool.	Throw some gold coins into the whirlpool at the Deep Sea Fishing platform. (68 Fishing)	80	6.5%
436	Hard	Kandarin: Ardougne	Solve the Archaeology mystery: Leap of Faith.	Solve the Leap of Faith Archaeology mystery. (70 Archaeology)	80	5.2%
437	Hard	Kandarin: Ardougne	Collect all breeds of chinchompa at Player Owned Farm.	Breed all types of chinchompas. (54 Farming, 97 Hunter)	80	<0.1%
438	Hard	Kandarin: Ardougne	Equip one piece of the Fishing outfit.	Equip one piece of the fishing outfit. (1 Fishing, 140 fishing tokens)	80	0.1%
439	Hard	Kandarin: Ardougne	Defeat the Penance Queen.	Defeat the Penance Queen.	80	<0.1%
440	Hard	Kandarin: Ardougne	Pickpocket a Hero.	Pickpocket a hero. (80 Thieving)	80	25.8%
441	Hard	Kandarin: Ardougne	Catch 50 Red Chinchompas in Kandarin.	Catch 50 carnivorous chinchompas in Kandarin. (63 Hunter)	80	1.2%
442	Hard	Kandarin: Feldip Hills	Equip an Ogre Expert hat.	Equip an ogre expert hat. (1,000 chompy bird kills)	80	<0.1%
443	Hard	Global	Catch a Monkfish.	Catch a raw monkfish. (62 Fishing, Completion of Swan Song)	80	8.5%
444	Hard	Global	Recover all data for one memory-storage bot.	Recover all data for memory-storage bot (Aagi) in the Hall of Memories. (70 Divination)	80	6.8%
445	Hard	Kandarin: Seers Village	Use the Piety Prayer.	Use the Piety Prayer. (70 Prayer, 70 Defence, Completion of Knight Waves training ground)	80	1.2%
446	Hard	Kandarin: Ardougne	Complete the task set: Hard Ardougne.	Complete the Hard Ardougne achievements.	80	<0.1%
601	Hard	Karamja	Use the stepping stone across the river in Shilo village.	Use the stepping stones Agility Shortcut in Shilo Village. (74 Agility, Completion of Shilo Village)	80	1.1%
602	Hard	Karamja	Equip a full set of Obsidian armour.	Equip a full set of obsidian armour. (60 Defence, Completion of The Brink of Extinction, 80 Smithing)	80	0.3%
603	Hard	Karamja	Equip a Red Topaz Machete.	Equip a red topaz machete.	80	1.7%
604	Hard	Karamja	Find a Gout Tuber.	Find a gout tuber. (10 Woodcutting, Completion of Jungle Potion)	80	0.4%
605	Hard	Karamja	Defeat TzTok-Jad.	Defeat TzTok-Jad once.	80	18.4%
606	Hard	Karamja	Defeat TzTok-Jad. (25 times)	Defeat TzTok-Jad 25 times.	80	1.3%
607	Hard	Karamja	Use your fire cape on TzTok-Jad before defeating them.	Use your fire cape on TzTok-Jad before defeating them.	80	2.1%
608	Hard	Karamja	Equip a Fire Cape.	Equip a fire cape.	80	18.1%
609	Hard	Karamja	Defeat TokHaar-Hok with only obsidian equipment.	Defeat TokHaar-Hok in the Fight Cauldron minigame using only obsidian equipment. (60 Defence and one of 60 Attack, 60 Strength, 60 Magic, or 60 Ranged, Completion of The Brink of Extinction)	80	<0.1%
610	Hard	Karamja	Repair the fairy ring inside the Kharazi jungle.	Repair the fairy ring inside the Kharazi jungle. (Partial completion of Legends' Quest, 5 bittercap mushrooms)	80	0.2%
611	Hard	Karamja	Access the Gemstone cavern.	Access the gemstone cavern. (Hard Karamja achievements and either an uncut dragonstone or a gemstone dragon Slayer task)	80	0.3%
612	Hard	Karamja	Catch a Draconic jadinko at Herblore Habitat.	Catch a draconic jadinko at Herblore Habitat. (80 Hunter)	80	0.1%
613	Hard	Karamja	Craft a Bolas.	Craft a bolas. (87 Fletching, 80 Slayer)	80	0.5%
614	Hard	Karamja	Complete the task set: Hard Karamja.	Complete the Hard Karamja achievements.	80	<0.1%
615	Hard	Karamja	Collect 60 Agility Arena tickets from Brimhaven Agility Arena.	Receive 60 Agility Arena tickets. (1 Agility)	80	1.1%
617	Hard	Karamja	Defeat TzTok-Jad in less than 45:00.	Defeat TzTok-Jad in less than 45:00.	80	17.6%
618	Hard	Karamja	Complete the Fight Kiln.	Complete the Fight Kiln. (Completion of The Elder Kiln, hand in a fire cape)	80	5.3%
620	Hard	Karamja	Equip a TokHaar-Kal-Ket.	Equip a TokHaar-Kal-Ket. (Completion of The Elder Kiln, hand in a fire cape (once))	80	4%
621	Hard	Karamja	Equip a TokHaar-Kal-Xil.	Equip a TokHaar-Kal-Xil. (Completion of The Elder Kiln, hand in a fire cape (once))	80	0.1%
622	Hard	Karamja	Equip a TokHaar-Kal-Mej.	Equip a TokHaar-Kal-Mej. (Completion of The Elder Kiln, hand in a fire cape (once))	80	0.3%
623	Hard	Karamja	Equip a TokHaar-Kal-Mor.	Equip a TokHaar-Kal-Mor. (Completion of The Elder Kiln, hand in a fire cape (once))	80	0.9%
624	Hard	Karamja	Complete the Fight Kiln and collect an uncut onyx.	Complete the Fight Kiln and collect an uncut onyx. (Completion of The Elder Kiln, hand in a fire cape (once))	80	0.9%
629	Hard	Karamja	Complete all TzTok-Jad combat achievements.	Complete all TzTok-Jad combat achievements.	80	<0.1%
10	Hard	Misthalin: Draynor Village	Siphon from a death esswraith in the RuneSpan.	Siphon from a death esswraith in the RuneSpan. (66 Runecrafting)	80	7.3%
12	Hard	Misthalin: Draynor Village	Obtain the Massive Pouch from the RuneSpan.	Obtain the massive pouch from the RuneSpan. (90 Runecrafting, 1,000 Runespan points)	80	0.4%
14	Hard	Misthalin: Draynor Village	Equip the full Master Runecrafter skilling outfit.	Equip the full master runecrafter robes set. (50 Runecrafting, 60,000 Runecrafting guild tokens, 16,000 Runespan points, or 2,000 thaler)	80	<0.1%
18	Hard	Misthalin: Edgeville	Complete the task set: Hard Varrock.	Complete all of the Hard Varrock achievements.	80	<0.1%
19	Hard	Misthalin: Edgeville	Make a waka canoe near Edgeville.	Make a waka canoe near Edgeville. (57 Woodcutting)	80	27.1%
20	Hard	Misthalin: Edgeville	Chop down the Edgeville elder tree.	Chop down the Edgeville elder tree. (90 Woodcutting)	80	0.9%
24	Hard	Misthalin: Fort Forinthry	Upgrade the workshop in Fort Forinthry to Tier 3.	Upgrade the workshop in Fort Forinthry to tier 3. (75 Construction, Completion of New Foundations)	80	0.5%
31	Hard	Misthalin: Lumbridge	Enter Zanaris via Lumbridge Swamp.	Enter Zanaris via Lumbridge Swamp. (Partial completion of Lost City)	80	29.9%
55	Hard	Misthalin: Lumbridge	Complete the task set: Hard Lumbridge.	Complete all Hard Tasks in Lumbridge.	80	2.1%
56	Hard	Misthalin: Lumbridge	Unlock the Bladed Dive ability from Shattered Worlds.	Unlock the Bladed Dive ability from Shattered Worlds. (63,000,000 shattered anima)	80	0.6%
57	Hard	Misthalin: Lumbridge	Smith a mithril platebody in the Draynor Sewers.	Smith a mithril platebody on the anvil in Draynor Sewers. (30 Smithing)	80	46.6%
58	Hard	Misthalin: Lumbridge	Fully grow a magic tree in Lumbridge.	Fully grow a magic tree in Lumbridge. (75 Farming)	80	2.8%
75	Hard	Misthalin: City of Um	Defeat Hermod, the Spirit of War.	Defeat Hermod, the Spirit of War once. (Completion of The Spirit of War)	80	<0.1%
76	Hard	Misthalin: City of Um	Defeat Hermod, the Spirit of War. (100 times)	Defeat Hermod, the Spirit of War 100 times. (Completion of The Spirit of War)	80	0.2%
77	Hard	Misthalin: City of Um	Rest whilst listening to the Dead Beats in the City of Um.	Rest whilst listening to the Dead Beats in the City of Um. (Completion of That Old Black Magic)	80	0.1%
78	Hard	Misthalin: City of Um	Smelt a necronium bar at the smithy in the City of Um.	Smelt a necronium bar at the smithy in the City of Um. (70 Smithing, Partial completion of Necromancy!)	80	11.5%
79	Hard	Misthalin: City of Um	Create a passing bracelet in the City of Um.	Create a passing bracelet, performing each step in the City of Um. (60 Necromancy, 79 Crafting, 68 Magic)	80	0.9%
80	Hard	Misthalin: City of Um	Catch a ghostly impling while wearing ghostly robes.	Catch a ghostly impling while wearing a full set of ghostly robes. (68 Hunter, Completion of The Curse of Zaros (miniquest))	80	<0.1%
81	Hard	Misthalin: City of Um	Upgrade a set of Death Skull equipment to tier 70.	Upgrade a set of Death Skull equipment to tier 70. (70 Necromancy, Completion of The Spirit of War)	80	5.4%
82	Hard	Misthalin: City of Um	Complete a Powerful Communion ritual.	Complete a powerful communion ritual. (90 Necromancy)	80	0.7%
83	Hard	Misthalin: City of Um	Conjure an undead army at the City of Um ritual site.	Conjure an undead army at the Um ritual site. (99 Necromancy)	80	1.4%
114	Hard	Misthalin: Varrock	Obtain a new set of Family Crest gauntlets from Dimintheis.	Obtain a new set of family gauntlets from Dimintheis. (Completion of Family Crest)	80	0.9%
115	Hard	Misthalin: Varrock	Talk to Romily Weaklax and give him a wild pie.	Talk to Romily Weaklax and give him a wild pie. (85 Cooking or 50 Hunter)	80	0.2%
116	Hard	Misthalin: Varrock	Harness the power of three relics at once.	Activate 3 Archaeology relics at once. (25 Archaeology, A ring of luck)	80	3.9%
117	Hard	Misthalin: Varrock	Mine 50 Dark Animica from the Empty Throne Room.	Mine 50 dark animica from the Empty Throne Room. (90 Mining)	80	15.2%
118	Hard	Misthalin: Varrock	Defeat Kerapac, the bound.	Defeat Kerapac, the bound once.	80	4.7%
120	Hard	Misthalin: Varrock	Defeat the Arch-Glacor.	Defeat the Arch-Glacor.	80	23.2%
762	Hard	Misthalin: City of Um	Defeat Nakatra, Devourer Eternal.	Defeat Nakatra, Devourer Eternal. (Completion of Necromancy!, completion of Soul Searching)	80	0.7%
764	Hard	Misthalin: City of Um	Cleanse the Gate of Elidinis.	Cleanse the Gate of Elidinis. (Completion of Ode of the Devourer or Soul Searching)	80	17%
766	Hard	Misthalin: City of Um	Complete the task set: Hard Underworld.	Complete the Hard Underworld achievements.	80	<0.1%
720	Hard	Morytania	Take a hard companion through a hard route of Temple Trekking.	Take a hard companion through a hard route of Temple Trekking. (Completion of In Aid of the Myreque)	80	0.4%
721	Hard	Morytania	Mine 30 Phasmatite.	Mine 30 phasmatite at Port Phasmatys south mine. (70 Mining)	80	42.6%
722	Hard	Morytania	Defeat 25 Gargoyles.	Defeat 25 gargoyles. (75 Slayer)	80	9.4%
723	Hard	Morytania	Defeat 35 Aberrant Spectres.	Defeat 35 aberrant spectres. (60 Slayer)	80	19.4%
724	Hard	Morytania	Equip a full set of Ahrim's equipment, including the staff.	Equip a full set of Ahrim's equipment. (70 Defence, 70 Magic)	80	<0.1%
725	Hard	Morytania	Equip a full set of Dharok's equipment, including the greataxe.	Equip a full set of Dharok's equipment. (70 Defence, 70 Attack)	80	0.1%
726	Hard	Morytania	Equip a full set of Guthan's equipment, including the warspear.	Equip a full set of Guthan's equipment. (70 Defence, 70 Attack)	80	0.1%
727	Hard	Morytania	Equip a full set of Torag's equipment, including the hammer.	Equip a full set of Torag's equipment. (70 Defence, 70 Attack)	80	0.1%
728	Hard	Morytania	Equip a full set of Verac's equipment, including the flail.	Equip a full set of Verac's equipment. (70 Defence, 70 Attack)	80	0.1%
729	Hard	Morytania	Equip a full set of Karil's equipment, including the 2h crossbow.	Equip a full set of Karil's equipment. (70 Defence, 70 Ranged)	80	<0.1%
730	Hard	Morytania	Complete the quest: The Branches of Darkmeyer.	Complete The Branches of Darkmeyer.	80	0.3%
731	Hard	Morytania	Burn 20 Blisterwood logs.	Burn 20 blisterwood logs. (76 Woodcutting, 76 Firemaking, Partial completion of The Branches of Darkmeyer)	80	0.1%
732	Hard	Morytania	Fully level up all Temple Trekking companions.	Fully level up all Temple Trekking companions. (Completion of In Aid of the Myreque)	80	<0.1%
733	Hard	Morytania	Catch 5 sharks in Burgh de Rott.	Catch 5 raw sharks in Burgh de Rott. (76 Fishing, Partial completion of In Aid of the Myreque)	80	0.1%
734	Hard	Morytania	Complete the task set: Hard Morytania.	Complete the Hard Morytania achievements.	80	<0.1%
533	Hard	Elven Lands: Tirranwn	Plant a mushroom seed in the mushroom patch in Isafdar.	Plant a mushroom seed in the mushroom patch in Isafdar. (53 Farming, Completion of the medium Tirannwn achievements)	80	<0.1%
534	Hard	Elven Lands: Tirranwn	Defeat 30 Cadarn warriors in Prifddinas.	Defeat 30 Cadarn warriors in Prifddinas.	80	13.3%
535	Hard	Elven Lands: Tirranwn	Harvest some harmony moss from a harmony pillar.	Harvest some harmony moss from a harmony pillar. (75 Farming)	80	4.6%
536	Hard	Elven Lands: Tirranwn	Complete the Hefin Agility course with a light creature familiar.	Complete the Hefin Agility Course with a light creature familiar summoned. (77 Agility, 88 Summoning, 71 Divination)	80	0.1%
537	Hard	Elven Lands: Tirranwn	Cleanse the Corrupted Seren stone with 5 cleansing crystals.	Cleanse the corrupted Seren stone with 5 cleansing crystals. (75 Prayer)	80	15.4%
538	Hard	Elven Lands: Tirranwn	Complete 10 laps of the Hefin agility course.	Complete 10 laps of the Hefin Agility Course. (77 Agility)	80	6.7%
539	Hard	Elven Lands: Tirranwn	Harvest 100 Incandescent energy from Incandescent Wisps.	Harvest 100 incandescent energy from incandescent wisps. (95 Divination)	80	1.3%
540	Hard	Elven Lands: Tirranwn	Equip a Dark bow.	Equip a dark bow. (90 Slayer, 70 Ranged, 70 Defence)	80	1.2%
541	Hard	Elven Lands: Tirranwn	Defeat 30 Dark beasts in Tirannwn.	Defeat 30 dark beasts in Tirannwn. (90 Slayer)	80	3.3%
542	Hard	Elven Lands: Tirranwn	Equip a Crystal halberd.	Equip a crystal halberd. (50 Agility, 70 Attack)	80	14%
543	Hard	Elven Lands: Tirranwn	Equip a Crystal shield.	Equip a crystal shield. (50 Agility, 70 Defence)	80	5.8%
544	Hard	Elven Lands: Tirranwn	Equip a Crystal bow.	Equip a crystal bow. (50 Agility, 70 Ranged)	80	4.9%
545	Hard	Elven Lands: Tirranwn	Catch 25 Grenwalls in Isafdar.	Catch 25 grenwalls in Isafdar. (77 Hunter)	80	0.1%
546	Hard	Elven Lands: Tirranwn	Defeat 10 Elf warriors in Lletya.	Defeat 10 elf warriors in Lletya.	80	25.2%
547	Hard	Elven Lands: Tirranwn	Chop 50 Magic logs in Tirannwn.	Chop 50 magic logs in Tirannwn. (80 Woodcutting)	80	3.1%
548	Hard	Elven Lands: Tirranwn	Open the crystal chest in Prifddinas 10 times.	Open the crystal chest in Prifddinas 10 times.	80	10.6%
549	Hard	Elven Lands: Tirranwn	Charge Dragonstone jewellery using the Tears of Seren.	Charge a piece of dragonstone jewellery using the Tears of Seren. (Completion of Legends' Quest)	80	0.1%
550	Hard	Elven Lands: Tirranwn	Complete the task set: Hard Tirannwn.	Complete the Hard Tirannwn achievements.	80	<0.1%
656	Hard	Wilderness: General	Defeat the KBD while wearing black dragonhide.	Defeat the King Black Dragon while wearing black dragonhide armour in six equipment slots. (60 Defence)	80	6.3%
657	Hard	Wilderness: General	Defeat one of each revenant creature.	Defeat one of each revenant creature in the Forinthry dungeon.	80	6.1%
658	Hard	Wilderness: General	Equip a Statius's warhammer.	Equip a Statius's warhammer. (78 Attack)	80	<0.1%
659	Hard	Wilderness: General	Catch 25 Black Salamanders.	Catch 25 black salamanders. (67 Hunter)	80	1.7%
660	Hard	Wilderness: Daemonheim	Restore an artefact from the Daemonheim digsite.	Restore an artefact from the Daemonheim Dig Site. (73 Archaeology)	80	2.8%
661	Hard	Wilderness: General	Defeat the Corporeal Beast.	Defeat the Corporeal Beast once. (Completion of Summer's End)	80	0.2%
662	Hard	Wilderness: General	Defeat the Corporeal Beast. (100 times)	Defeat the Corporeal Beast 100 times. (Completion of Summer's End)	80	<0.1%
663	Hard	Wilderness: Daemonheim	Defeat the Skeletal Trio.	Defeat the Skeletal Trio. (71 Dungeoneering)	80	0.8%
664	Hard	Wilderness: Daemonheim	Upgrade your Gem bag.	Upgrade your gem bag. (40 Dungeoneering, 45 Crafting, 20,000 dungeoneering tokens)	80	1.2%
665	Hard	Wilderness: General	Equip a pair of Steadfast boots.	Equip a pair of steadfast boots. (85 Defence)	80	<0.1%
666	Hard	Wilderness: General	Equip a pair of Glaiven boots.	Equip a pair of glaiven boots. (85 Defence)	80	<0.1%
667	Hard	Wilderness: General	Equip a pair of Ragefire boots.	Equip a pair of ragefire boots. (85 Defence)	80	<0.1%
668	Hard	Wilderness: General	Complete the task set: Hard Wilderness.	Complete the Hard Wilderness achievements.	80	0.4%
678	Hard	Wilderness: Daemonheim	Equip a Chaotic weapon or kiteshield.	Equip a chaotic weapon or kiteshield. (80 Dungeoneering, 80 Attack OR 80 Ranged OR 80 Magic OR 80 Defence)	80	0.3%
489	Elite	Anachronia	Discover all the totem pieces on Anachronia.	Discover all the totem pieces on Anachronia.	200	<0.1%
491	Elite	Anachronia	Unlock the double Surge or double Escape ability upgrade.	Unlock the double Surge or double Escape ability upgrade. (30 Agility)	200	0.2%
494	Elite	Anachronia	Harvest a Dragonfruit plant on Anachronia.	Harvest a dragonfruit cactus in the cactus patch in the north of Anachronia. (95 Farming)	200	2.8%
495	Elite	Anachronia	Kill 50 Dinosaurs.	Kill 50 dinosaurs. (90 Slayer)	200	4.3%
496	Elite	Anachronia	Kill 50 Vile Blooms.	Kill 50 vile blooms. (90 Slayer)	200	4%
497	Elite	Anachronia	Solve the Archaeology mystery: Teleport Node On.	Activate all Orthen teleportation devices on Anachronia. (90 Archaeology, 70 Runecrafting, 70 Crafting, 70 Divination)	200	<0.1%
498	Elite	Anachronia	Use special fertiliser on Prehistoric Potterington.	Use Potterington Blend #102 Fertiliser or dinosaur 'propellant' on Prehistoric Potterington. (95 Firemaking)	200	<0.1%
499	Elite	Anachronia	Find an unchecked egg in the pile of dinosaur eggs.	Find a dinosaur egg in the pile of dinosaur eggs on Anachronia Farm. (87 Firemaking)	200	0.3%
501	Elite	Anachronia	Defeat Raksha, the Shadow Colossus. (100 times)	Defeat Raksha, the Shadow Colossus 100 times.	200	<0.1%
502	Elite	Anachronia	Complete the quest: Desperate Measures.	Complete the Desperate Measures quest.	200	1%
503	Elite	Anachronia	Equip a Terrasaur maul.	Equip a terrasaur maul. (80 Strength, 96 Hunter, 76 Slayer)	200	<0.1%
505	Elite	Anachronia	Complete a big game encounter without being seen.	Complete a Big Game Hunter encounter without stepping into the creature's vision ring. (75 Hunter, 55 Slayer)	200	0.5%
508	Elite	Anachronia	Craft 500 Time Runes.	Craft 500 time runes. (100 Runecrafting)	200	0.5%
509	Elite	Anachronia	Solve the Archaeology mystery: Fragmented Memories.	Complete the Fragmented Memories Archaeology mystery. (108 Archaeology, 86 Hunter)	200	<0.1%
512	Elite	Anachronia	Fletch any type of Elder God arrow.	Fletch any type of Elder God arrow. (95 Fletching, 95 Firemaking)	200	0.1%
513	Elite	Anachronia	Cast the Crumble Undead spell.	Cast the Crumble Undead spell. (78 Magic)	200	5%
238	Elite	Asgarnia: Falador	Complete the task set: Elite Falador.	Complete the Elite Falador achievements.	200	<0.1%
239	Elite	Asgarnia: Falador	Complete the Invention tutorial.	Complete the Invention tutorial. (80 Smithing, 80 Crafting, 80 Divination)	200	20%
240	Elite	Asgarnia: Falador	Defeat Vorago.	Defeat Vorago.	200	0.8%
241	Elite	Asgarnia: Falador	Defeat Vorago. (50 times)	Defeat Vorago 50 times.	200	<0.1%
242	Elite	Asgarnia: Falador	Equip a seismic wand or seismic singularity.	Equip a seismic wand or singularity. (90 Magic)	200	<0.1%
243	Elite	Asgarnia: Falador	Harvest some starbloom flowers south of Falador.	Harvest some starbloom flowers from the flower patch south of Falador. (100 Farming)	200	3.1%
244	Elite	Asgarnia: Falador	Unlock the Royale Cannon from the Artisans' Workshop.	Unlock the royale dwarf multicannon from the Artisans' Workshop Reward Shop.	200	14.7%
245	Elite	Asgarnia: Falador	Equip a piece of masterwork melee armour.	Equip a piece of masterwork melee armour. (99 Smithing, 90 Defence, Completion of It Should Have Been Called Aetherium)	200	0.3%
255	Elite	Asgarnia: Burthorpe	Equip a full set of Bandos armour.	Equip a full set of Bandos armour. (70 Defence, 70 Strength, Partial completion of Troll Stronghold)	200	10.6%
256	Elite	Asgarnia: Burthorpe	Equip a full set of Armadyl armour.	Equip a full set of Armadyl armour. (70 Defence, 70 Ranged, Partial completion of Troll Stronghold)	200	0.1%
257	Elite	Asgarnia: Burthorpe	Equip a full set of subjugation armour.	Equip a full set of subjugation armour. (70 Defence, 70 Constitution, Partial completion of Troll Stronghold)	200	1.8%
258	Elite	Asgarnia: Burthorpe	Equip a piece of Torva, Pernix or Virtus armour.	Equip a piece of Torva, Pernix or Virtus armour. (80 Constitution, 80 Defence, 70 Ranged, 70 Strength, 70 Agility, Partial completion of Troll Stronghold)	200	0.4%
259	Elite	Asgarnia: Burthorpe	Defeat Nex, the Angel of Death.	Kill Nex: Angel of Death. (70 Constitution, 70 Ranged, 70 Strength, 70 Agility, Partial completion of Troll Stronghold)	200	<0.1%
260	Elite	Asgarnia: Burthorpe	Defeat Nex, the Angel of Death. (50 times)	Kill Nex: Angel of Death 50 times. (70 Constitution, 70 Ranged, 70 Strength, 70 Agility, Partial completion of Troll Stronghold)	200	<0.1%
267	Elite	Asgarnia: Port Sarim	Kill a living wyvern.	Kill a wyvern. (96 Slayer)	200	4.8%
327	Elite	Desert: General	Complete the task set: Elite Desert.	Complete the Elite Desert achievements.	200	<0.1%
329	Elite	Desert: General	Defeat Telos, the Warden at 100% enrage.	Defeat Telos, the Warden at 100% enrage. (80 Attack, 80 Prayer, 80 Magic, 80 Ranged)	200	0.5%
330	Elite	Desert: General	Defeat Telos, the Warden at 500% enrage.	Defeat Telos, the Warden at 500% enrage. (80 Attack, 80 Prayer, 80 Magic, 80 Ranged)	200	0.1%
331	Elite	Desert: Menaphos	Craft some Soul runes.	Craft some soul runes. (90 Runecrafting, Completion of 'Phite Club)	200	<0.1%
332	Elite	Desert: General	Defeat a Camel Warrior.	Defeat a camel warrior. (96 Slayer)	200	5%
333	Elite	Desert: General	Escape Kharid-et by boat.	Complete the Aquatic Escape achievement. (86 Archaeology, Partial completion of The Vault of Shadows)	200	0.4%
334	Elite	Desert: General	Defeat the Kalphite King solo.	Kill the Kalphite King solo.	200	2.2%
335	Elite	Desert: General	Cast Ice Barrage in the desert.	Cast Ice Barrage in the desert. (94 Magic, Completion of Desert Treasure)	200	1.9%
337	Elite	Desert: General	Craft a Zaros godsword, Seren godbow or staff of Sliske.	Craft a Zaros godsword, Seren godbow or staff of Sliske. (92 Crafting, 80 Attack, 80 Prayer, 80 Magic, 80 Ranged)	200	<0.1%
1112	Elite	Desert: Menaphos	Defeat Amascut, the Devourer.	Defeat Amascut, the Devourer. (Completion of Eclipse of the Heart)	200	0.3%
387	Elite	Fremennik: Lunar Isles	Cast Spellbook Swap from the Lunar spellbook.	Cast Spellbook Swap from the lunar spellbook. (96 Magic, Completion of Dream Mentor)	200	1.1%
389	Elite	Fremennik: Mainland	Equip Every Dagannoth King Ring.	Equip every Dagannoth King ring.	200	0.2%
390	Elite	Fremennik: Mainland	Equip a Completed God Book.	Equip a completed god book. (Completion of Horror from the Deep)	200	<0.1%
391	Elite	Fremennik: Mainland	Defeat 20 Acheron Mammoths.	Defeat 20 acheron mammoths. (96 Slayer)	200	4.8%
394	Elite	Fremennik: Mainland	Cast the Paradox spell.	Cast the Paradox spell on any tree, rock, fishing spot, or box trap. (88 Magic, 100 Runecrafting)	200	0.4%
395	Elite	Fremennik: Mainland	Build a Demonic Throne.	Build a demonic throne. (99 Construction)	200	0.1%
397	Elite	Fremennik: Lunar Isles	Perform a Powerful Necroplasm ritual at Ungael.	Perform a powerful necroplasm ritual at the Ungael ritual site. (90 Necromancy, Completion of Requiem for a Dragon)	200	<0.1%
398	Elite	Fremennik: Mainland	Defeat the Abomination once after Hero's Welcome.	Defeat the Abomination once after Hero's Welcome. (Completion of Hero's Welcome)	200	<0.1%
399	Elite	Fremennik: Mainland	Summon a Pack Mammoth.	Summon a pack mammoth. (96 Slayer, 99 Summoning)	200	0.2%
400	Elite	Fremennik: Mainland	Complete the task set: Elite Fremennik.	Complete the Elite Fremennik achievements.	200	<0.1%
401	Elite	Fremennik: Mainland	Complete the Ungael combat activity on hard mode.	Complete the Ungael combat activity on hard mode. (Completion of Ancient Awakening)	200	<0.1%
402	Elite	Fremennik: Mainland	Use Trap Telekinesis to catch Azure Skillchompas 25 times.	Use the Trap Telekinesis spell to catch azure skillchompas 25 times. (97 Magic, 68 Hunter, Completion of Lunar Diplomacy)	200	0.2%
140	Elite	Global	Reach maximum combat level.	Reach maximum combat level. (152 Combat)	200	<0.1%
145	Elite	Global	Reach total level 2000.	Reach total level 2000.	200	15.8%
821	Elite	Global	Complete 50 Slayer tasks.	Complete 50 Slayer tasks. (1 Slayer)	200	1.5%
822	Elite	Global	Complete 75 Slayer tasks.	Complete 75 Slayer tasks. (1 Slayer)	200	0.6%
890	Elite	Global	Obtain 125 Quest Points.	Obtain 125 quest points.	200	3.9%
911	Elite	Global	Collect 75 unique items for the Hard clue rewards log.	Collect 75 unique items for the hard clue rewards collection log.	200	6.7%
946	Elite	Global	Complete 10 Soul Reaper tasks.	Complete 10 Soul Reaper tasks.	200	1.3%
958	Elite	Global	Complete 75 Elite clue scrolls.	Complete 75 elite clue scrolls.	200	0.2%
959	Elite	Global	Complete 150 Elite clue scrolls.	Complete 150 elite clue scrolls.	200	<0.1%
961	Elite	Global	Complete 25 Master clue scrolls.	Complete 25 master clue scrolls.	200	1.9%
962	Elite	Global	Complete 75 Master clue scrolls.	Complete 75 master clue scrolls.	200	<0.1%
967	Elite	Global	Collect 35 unique items for the Elite clue rewards log.	Collect 35 unique items for the elite clue rewards collection log.	200	8.8%
969	Elite	Global	Collect 10 unique items for the Master clue rewards log.	Collect 10 unique items for the master clue rewards collection log.	200	21.4%
970	Elite	Global	Collect 15 unique items for the Master clue rewards log.	Collect 15 unique items for the master clue rewards collection log.	200	17.4%
971	Elite	Global	Collect 30 unique items for the Master clue rewards log.	Collect 30 unique items for the master clue rewards collection log.	200	6.9%
972	Elite	Global	Make 25 Powerburst Potions.	Make 25 powerbursts. (103 Herblore, 95 Farming)	200	<0.1%
973	Elite	Global	Make 25 Bomb Potions.	Make 25 bomb potions. (99 Herblore, 95 Farming)	200	<0.1%
974	Elite	Global	Make 5 Perfect Plus Potions.	Make 5 perfect plus potions. (99 Herblore)	200	<0.1%
975	Elite	Global	Make 15 Overload Potions.	Make 15 overloads. (96 Herblore)	200	0.8%
976	Elite	Global	Make a Spiritual Prayer Potion.	Make a spiritual prayer potion. (110 Herblore)	200	<0.1%
977	Elite	Global	Fletch 200 Magic stocks.	Fletch 200 magic stocks. (92 Fletching)	200	2.7%
978	Elite	Global	Fletch 750 Elder arrow shafts.	Fletch 750 elder arrow shafts. (90 Fletching, 90 Woodcutting)	200	0.4%
979	Elite	Global	Fletch 20 Elder shortbow (unstrung).	Fletch 20 unstrung elder shortbows. (90 Fletching, 90 Woodcutting)	200	0.5%
980	Elite	Global	Fletch an Eternal magic shortbow or Primal crossbow.	Fletch an eternal magic shortbow (martial) or primal crossbow (martial). (100 Fletching)	200	0.1%
981	Elite	Global	Fletch 1,000 Eternal magic shafts.	Fletch 1,000 eternal magic shafts. (100 Fletching, 100 Woodcutting)	200	0.1%
982	Elite	Global	Fletch 1,500 Primal arrows.	Fletch 1,500 primal arrows. (100 Fletching, 100 Woodcutting, 100 Smithing)	200	0.1%
983	Elite	Global	Fletch an Eternal Magic Wood Box.	Fletch an eternal magic wood box. (100 Fletching)	200	0.1%
984	Elite	Global	Fletch 350 Rune darts.	Fletch 350 rune darts. (81 Fletching, 50 Smithing, Completion of The Tourist Trap)	200	2.3%
985	Elite	Global	Smith a Primal Ore Box.	Smith a primal ore box. (100 Smithing)	200	2.1%
986	Elite	Global	Smith 10,000 Armour Spikes.	Smith 10,000 armour spikes. (90 Smithing)	200	6%
987	Elite	Global	Smith 10,000 Primal Armour Spikes.	Smith 10,000 primal armour spikes. (100 Smithing)	200	2.1%
988	Elite	Global	Mine 10 ores on Daemonheim peninsula in under 5 minutes.	Mine each of the 10 ores on the surface of the Daemonheim peninsula in under 5 minutes. (100 Mining)	200	2.1%
989	Elite	Global	Mine 70 Banite Ore.	Mine 70 banite ore. (80 Mining)	200	42.6%
990	Elite	Global	Mine 100 Dark or Light Animica.	Mine 100 dark or light animica. (90 Mining)	200	20.7%
991	Elite	Global	Open 10 Metamorphic Geodes.	Open 10 metamorphic geodes. (60 Mining)	200	0.1%
992	Elite	Global	Harvest 40 Grimy Lantadyme.	Harvest 40 grimy lantadyme. (73 Farming)	200	15.9%
993	Elite	Global	Harvest 50 Grimy Fellstalk.	Harvest 50 grimy fellstalk. (91 Farming)	200	7.4%
994	Elite	Global	Plant an Avocado seed in a bush patch.	Plant an avocado seed in a bush patch. (99 Farming)	200	1%
995	Elite	Global	Harvest 20 Lychee.	Harvest 20 lychee. (111 Farming)	200	0.2%
996	Elite	Global	Harvest 24 Starbloom Flowers.	Harvest 24 starbloom flowers. (100 Farming)	200	3.2%
997	Elite	Global	Catch 150 Rocktail.	Catch 150 raw rocktails. (90 Fishing)	200	0.8%
998	Elite	Global	Catch 200 Sailfish.	Catch 200 raw sailfish. (97 Fishing)	200	0.6%
999	Elite	Global	Catch 150 Blue Blubber Jellyfish.	Catch 150 raw blue blubber jellyfish. (91 Fishing)	200	0.7%
1000	Elite	Global	Obtain the highest boost in 'Fishing Frenzy'.	Obtain the highest boost available in the 'Fishing Frenzy' activity at Deep Sea Fishing. (94 Fishing)	200	0.2%
1001	Elite	Global	Catch a Cavefish.	Catch a raw cavefish. (85 Fishing)	200	3.1%
1003	Elite	Global	Manually bury or scatter each of the listed bones and ashes.	Complete the Bury All achievement.	200	<0.1%
1004	Elite	Global	Activate Soul Split prayer.	Activate Soul Split prayer. (92 Prayer, Completion of The Temple at Senntisten)	200	21.6%
1005	Elite	Global	Catch a Dragon Impling.	Catch a dragon impling. Cannot be completed in Puro-Puro. (83 Hunter)	200	0.2%
1006	Elite	Global	Catch a Kingly Impling.	Catch a kingly impling. Cannot be completed in Puro-Puro. (91 Hunter)	200	0.1%
1007	Elite	Global	Equip a full set of Bane armour.	Equip a full set of bane armour. (80 Smithing, 80 Mining, 80 Defence)	200	19.3%
1008	Elite	Global	Equip a full set of Elder Rune armour.	Equip a full set of elder rune armour. (90 Smithing, 90 Mining, 90 Defence)	200	6.5%
1009	Elite	Global	Cast a Surge spell.	Cast a Surge spell. (81 Magic)	200	8.5%
1010	Elite	Global	Burn 100 Magic Logs.	Burn 100 magic logs. (75 Firemaking)	200	5.7%
1011	Elite	Global	Burn 10 Elder logs.	Burn 10 elder logs. (90 Firemaking)	200	0.6%
1012	Elite	Global	Reach level 99 in the Agility skill.	Reach level 99 Agility.	200	5.9%
1013	Elite	Global	Reach level 99 in the Archaeology skill.	Reach level 99 Archaeology.	200	3.2%
1014	Elite	Global	Reach level 99 in the Attack skill.	Reach level 99 Attack.	200	7.4%
1015	Elite	Global	Reach level 99 in the Construction skill.	Reach level 99 Construction.	200	0.2%
1016	Elite	Global	Reach level 99 in the Cooking skill.	Reach level 99 Cooking.	200	0.5%
1017	Elite	Global	Reach level 99 in the Crafting skill.	Reach level 99 Crafting.	200	2.6%
1018	Elite	Global	Reach level 99 in the Defence skill.	Reach level 99 Defence.	200	9.1%
1019	Elite	Global	Reach level 99 in the Divination skill.	Reach level 99 Divination.	200	1.1%
1020	Elite	Global	Reach level 99 in the Dungeoneering skill.	Reach level 99 Dungeoneering.	200	0.4%
1021	Elite	Global	Reach level 99 in the Farming skill.	Reach level 99 Farming.	200	6.8%
1022	Elite	Global	Reach level 99 in the Firemaking skill.	Reach level 99 Firemaking.	200	0.4%
1023	Elite	Global	Reach level 99 in the Fishing skill.	Reach level 99 Fishing.	200	0.5%
1024	Elite	Global	Reach level 99 in the Fletching skill.	Reach level 99 Fletching.	200	3.2%
1025	Elite	Global	Reach level 99 in the Herblore skill.	Reach level 99 Herblore.	200	0.6%
1026	Elite	Global	Reach level 99 in the Constitution skill.	Reach level 99 Constitution.	200	7.7%
1027	Elite	Global	Reach level 99 in the Hunter skill.	Reach level 99 Hunter.	200	0.2%
1028	Elite	Global	Reach level 99 in the Invention skill.	Reach level 99 Invention.	200	15.2%
1029	Elite	Global	Reach level 99 in the Magic skill.	Reach level 99 Magic.	200	1.3%
1030	Elite	Global	Reach level 99 in the Mining skill.	Reach level 99 Mining.	200	10.1%
1031	Elite	Global	Reach level 99 in the Necromancy skill.	Reach level 99 Necromancy.	200	3.2%
1032	Elite	Global	Reach level 99 in the Prayer skill.	Reach level 99 Prayer.	200	12%
1033	Elite	Global	Reach level 99 in the Ranged skill.	Reach level 99 Ranged.	200	0.4%
1034	Elite	Global	Reach level 99 in the Runecrafting skill.	Reach level 99 Runecrafting.	200	0.6%
1035	Elite	Global	Reach level 99 in the Slayer skill.	Reach level 99 Slayer.	200	4.9%
1036	Elite	Global	Reach level 99 in the Smithing skill.	Reach level 99 Smithing.	200	4.7%
1037	Elite	Global	Reach level 99 in the Strength skill.	Reach level 99 Strength.	200	8.7%
1038	Elite	Global	Reach level 99 in the Summoning skill.	Reach level 99 Summoning.	200	0.5%
1039	Elite	Global	Reach level 99 in the Thieving skill.	Reach level 99 Thieving.	200	6.3%
1040	Elite	Global	Reach level 99 in the Woodcutting skill.	Reach level 99 Woodcutting.	200	0.4%
1041	Elite	Global	Reach level 110 in the Mining skill.	Reach level 110 Mining.	200	0.7%
1042	Elite	Global	Reach level 110 in the Smithing skill.	Reach level 110 Smithing.	200	0.1%
1043	Elite	Global	Reach level 110 in the Crafting skill.	Reach level 110 Crafting.	200	<0.1%
1044	Elite	Global	Reach level 110 in the Firemaking skill.	Reach level 110 Firemaking.	200	<0.1%
1045	Elite	Global	Reach level 110 in the Fletching skill.	Reach level 110 Fletching.	200	0.8%
1046	Elite	Global	Reach level 110 in the Woodcutting skill.	Reach level 110 Woodcutting.	200	<0.1%
1047	Elite	Global	Reach level 110 in the Runecrafting skill.	Reach level 110 Runecrafting.	200	<0.1%
1048	Elite	Global	Reach level 120 in the Dungeoneering skill.	Reach level 120 Dungeoneering.	200	<0.1%
1049	Elite	Global	Reach level 120 in the Farming skill.	Reach level 120 Farming.	200	0.1%
1050	Elite	Global	Reach level 120 in the Herblore skill.	Reach level 120 Herblore.	200	<0.1%
1051	Elite	Global	Reach level 120 in the Slayer skill.	Reach level 120 Slayer.	200	0.2%
1052	Elite	Global	Reach level 120 in the Invention skill.	Reach level 120 Invention.	200	14.8%
1053	Elite	Global	Reach level 120 in the Archaeology skill.	Reach level 120 Archaeology.	200	0.2%
1054	Elite	Global	Reach level 120 in the Necromancy skill.	Reach level 120 Necromancy.	200	0.1%
1055	Elite	Global	Obtain 50 Million Agility XP.	Obtain 50 million Agility XP. (112 Agility)	200	0.5%
1056	Elite	Global	Obtain 50 Million Construction XP.	Obtain 50 million Construction XP. (112 Construction)	200	<0.1%
1057	Elite	Global	Obtain 50 Million Cooking XP.	Obtain 50 million Cooking XP. (112 Cooking)	200	<0.1%
1058	Elite	Global	Obtain 50 Million Crafting XP.	Obtain 50 million Crafting XP. (112 Crafting)	200	<0.1%
1059	Elite	Global	Obtain 50 Million Farming XP.	Obtain 50 million Farming XP. (112 Farming)	200	0.3%
1060	Elite	Global	Obtain 50 Million Firemaking XP.	Obtain 50 million Firemaking XP. (112 Firemaking)	200	<0.1%
1061	Elite	Global	Obtain 50 Million Fishing XP.	Obtain 50 million Fishing XP. (112 Fishing)	200	<0.1%
1062	Elite	Global	Obtain 50 Million Fletching XP.	Obtain 50 million Fletching XP. (112 Fletching)	200	0.7%
1063	Elite	Global	Obtain 50 Million Herblore XP.	Obtain 50 million Herblore XP. (112 Herblore)	200	<0.1%
1064	Elite	Global	Obtain 50 Million Hunter XP.	Obtain 50 million Hunter XP. (112 Hunter)	200	<0.1%
1065	Elite	Global	Obtain 50 Million Mining XP.	Obtain 50 million Mining XP. (112 Mining)	200	0.3%
1066	Elite	Global	Obtain 50 Million Prayer XP.	Obtain 50 million Prayer XP. (112 Prayer)	200	0.5%
1067	Elite	Global	Obtain 50 Million Runecrafting XP.	Obtain 50 million Runecrafting XP. (112 Runecrafting)	200	<0.1%
1068	Elite	Global	Obtain 50 Million Slayer XP.	Obtain 50 million Slayer XP. (112 Slayer)	200	0.8%
1069	Elite	Global	Obtain 50 Million Smithing XP.	Obtain 50 million Smithing XP. (112 Smithing)	200	<0.1%
1070	Elite	Global	Obtain 50 Million Thieving XP.	Obtain 50 million Thieving XP. (112 Thieving)	200	1%
1071	Elite	Global	Obtain 50 Million Woodcutting XP.	Obtain 50 million Woodcutting XP. (112 Woodcutting)	200	<0.1%
1072	Elite	Global	Obtain 50 Million Dungeoneering XP.	Obtain 50 million Dungeoneering XP. (112 Dungeoneering)	200	<0.1%
1073	Elite	Global	Obtain 50 Million Invention XP.	Obtain 50 million Invention XP. (112 Invention)	200	15%
1074	Elite	Global	Obtain 50 Million Divination XP.	Obtain 50 million Divination XP. (112 Divination)	200	<0.1%
1075	Elite	Global	Obtain 50 Million Archaeology XP.	Obtain 50 million Archaeology XP. (112 Archaeology)	200	0.4%
1076	Elite	Global	Obtain 50 Million Attack XP.	Obtain 50 million Attack XP. (112 Attack)	200	0.8%
1077	Elite	Global	Obtain 50 Million Constitution XP.	Obtain 50 million Constitution XP. (112 Constitution)	200	0.6%
1078	Elite	Global	Obtain 50 Million Strength XP.	Obtain 50 million Strength XP. (112 Strength)	200	0.8%
1079	Elite	Global	Obtain 50 Million Defence XP.	Obtain 50 million Defence XP. (112 Defence)	200	0.9%
1080	Elite	Global	Obtain 50 Million Ranged XP.	Obtain 50 million Ranged XP. (112 Ranged)	200	<0.1%
1081	Elite	Global	Obtain 50 Million Magic XP.	Obtain 50 million Magic XP. (112 Magic)	200	0.1%
1082	Elite	Global	Obtain 50 Million Summoning XP.	Obtain 50 million Summoning XP. (112 Summoning)	200	<0.1%
1083	Elite	Global	Obtain 50 Million Necromancy XP.	Obtain 50 million Necromancy XP. (112 Necromancy)	200	0.5%
1084	Elite	Global	Complete 750 clues of any tier.	Complete 750 clues of any tier.	200	<0.1%
1085	Elite	Global	Complete 1000 clues of any tier.	Complete 1000 clues of any tier.	200	<0.1%
1086	Elite	Global	Make 5 Elder Overload Salve Potions.	Make 5 elder overload salves. (107 Herblore, 89 Crafting, 81 Mining)	200	<0.1%
1087	Elite	Global	Equip an Eternal Magic shortbow.	Equip an eternal magic shortbow. (100 Woodcutting, 100 Fletching)	200	<0.1%
1094	Elite	Global	Equip a full set of Primal armour.	Equip a full set of primal armour. (100 Mining, 100 Smithing, 99 Defence)	200	1.1%
1103	Elite	Global	Reach level 90 in any skill.	Reach level 90 in any skill.	200	43.5%
1104	Elite	Global	Reach level 95 in any skill.	Reach level 95 in any skill.	200	35.2%
1109	Elite	Global	Reach at least level 80 in all non-elite skills.	Reach at least level 80 in all non-elite skills.	200	0.1%
1110	Elite	Global	Reach at least level 90 in all non-elite skills.	Reach at least level 90 in all non-elite skills.	200	<0.1%
447	Elite	Global	Help the Archivist recover all core memory data.	Recover all core memory data in the Hall of Memories. (95 Divination)	200	0.5%
448	Elite	Global	Attune and hand all engrams in to the Memorial to Guthix.	Hand all engrams in to the Memorial to Guthix. (95 Divination, Completion of Lost City)	200	0.1%
449	Elite	Kandarin: Ardougne	Equip a dragon full helm.	Equip a dragon full helm. (60 Defence)	200	0.1%
450	Elite	Kandarin: Ardougne	Chop an Elder Tree until it is depleted.	Chop an elder tree until it no longer has logs remaining. (90 Woodcutting)	200	61.2%
451	Elite	Kandarin: Ardougne	Obtain a Crystal Geode from a Crystal Tree.	Obtain a crystal geode from a crystal tree. (94 Woodcutting)	200	3.4%
452	Elite	Kandarin: Ardougne	Reach Howl's Workshop in the Stormguard Citadel.	Partial completion of the Howl's Floating Workshop mystery. (95 Archaeology)	200	6.1%
453	Elite	Kandarin: Feldip Hills	Equip a Dragon Archer hat.	Equip a Dragon Archer hat. (2,250 chompy bird kills)	200	<0.1%
454	Elite	Kandarin: Ardougne	Complete the task set: Elite Ardougne.	Complete the Elite Ardougne achievements.	200	<0.1%
455	Elite	Kandarin: Ardougne	Successfully breed a royal dragon.	Breed a royal dragon. (92 Farming)	200	<0.1%
457	Elite	Kandarin: Ardougne	Defeat an Automaton after 'The World Wakes'.	Defeat an automaton after The World Wakes. (67 Slayer, Completion of multiple quests)	200	0.7%
459	Elite	Global	Mine 25 Platinum Ore south of Piscatoris Fishing Colony.	Mine 25 platinum ores south of Piscatoris Fishing Colony. (104 Mining)	200	1.6%
460	Elite	Global	Chop 50 Eternal Magic logs.	Chop 50 eternal magic logs. (100 Woodcutting)	200	0.2%
616	Elite	Karamja	Purchase an uncut onyx from Tzhaar-Hur-Lek's store.	Purchase an uncut onyx from TzHaar-Hur-Lek's Ore and Gem Store. (2,700,000 Tokkul)	200	<0.1%
619	Elite	Karamja	Defeat the Har-Aken. (10 times)	Defeat Har-Aken 10 times. (Completion of The Elder Kiln, hand in a fire cape (once))	200	0.1%
625	Elite	Karamja	Defeat 10 gemstone dragons.	Defeat 10 gemstone dragons inside the Gemstone cavern. (95 Slayer, Completion of the Hard Karamja achievements)	200	4.2%
626	Elite	Karamja	Equip a piece of Gemstone armour.	Equip a piece of gemstone armour. (95 Slayer, Completion of the Hard Karamja achievements)	200	<0.1%
627	Elite	Karamja	Complete the task set: Elite Karamja.	Complete the Elite Karamja achievements.	200	<0.1%
628	Elite	Karamja	Complete all Har-Aken combat achievements.	Complete all Har-Aken combat achievements. (Completion of The Elder Kiln)	200	<0.1%
11	Elite	Misthalin: Draynor Village	Navigate the RuneSpan using a Greater Conjuration Platform.	Navigate the RuneSpan using a greater conjuration platform. (95 Runecrafting)	200	0.3%
13	Elite	Misthalin: Draynor Village	Obtain the Greater Runic Staff from the RuneSpan.	Obtain the greater runic staff from the RuneSpan. (90 Runecrafting, 75 Magic)	200	<0.1%
21	Elite	Misthalin: Edgeville	Complete the task set: Elite Varrock.	Complete all of the Elite Varrock achievements.	200	<0.1%
25	Elite	Misthalin: Fort Forinthry	Upgrade the guardhouse in Fort Forinthry to Tier 3.	Upgrade the guardhouse in Fort Forinthry to tier 3. (95 Construction, Completion of Unwelcome Guests)	200	<0.1%
59	Elite	Misthalin: Lumbridge	Defeat 150 tormented demons.	Defeat 150 tormented demons. (Completion of While Guthix Sleeps)	200	<0.1%
60	Elite	Misthalin: Lumbridge	Equip a dragon crossbow.	Equip a dragon crossbow. (60 Ranged, 94 Fletching, Completion of While Guthix Sleeps)	200	<0.1%
85	Elite	Misthalin: City of Um	Defeat Rasial, the First Necromancer.	Defeat Rasial, the First Necromancer once. (Completion of Alpha vs Omega)	200	<0.1%
86	Elite	Misthalin: City of Um	Defeat Rasial, the First Necromancer. (100 times)	Defeat Rasial, the First Necromancer 100 times. (Completion of Alpha vs Omega)	200	0.1%
87	Elite	Misthalin: City of Um	Equip an Omni guard.	Equip an omni guard. (95 Necromancy, Completion of Alpha vs Omega)	200	0.1%
88	Elite	Misthalin: City of Um	Equip a Soulbound lantern.	Equip a soulbound lantern. (95 Necromancy, Alpha vs Omega)	200	0.1%
89	Elite	Misthalin: City of Um	Equip a full set of Robes of the First Necromancer.	Equip a full set of First Necromancer's equipment. (95 Necromancy, 95 Defence, Completion of Alpha vs Omega)	200	<0.1%
90	Elite	Misthalin: City of Um	Give a blueberry pie to Thalmund in the City of Um.	Give a blueberry pie to Thalmund in the City of Um. (10 Cooking, 90 Defence, Completion of Kili's Knowledge VII, partial completion of A Fairy Tale II - Cure a Queen, completion of The Fremennik Trials)	200	0.1%
91	Elite	Misthalin: City of Um	Track 8 of the owls in the City of Um.	Track 8 of the owls in the City of Um. (90 Necromancy, Completion of Housing of Parliament)	200	0.3%
92	Elite	Misthalin: Varrock	Defeat Croesus.	Defeat Croesus 1 time.	200	1%
93	Elite	Misthalin: Varrock	Defeat Croesus. (100 times)	Defeat Croesus 100 times.	200	<0.1%
119	Elite	Misthalin: Varrock	Defeat Kerapac, the bound. (100 times)	Defeat Kerapac, the bound 100 times.	200	0.1%
121	Elite	Misthalin: Varrock	Defeat the Arch-Glacor in hard mode. (100 times)	Defeat the Arch-Glacor in hard mode 100 times.	200	<0.1%
124	Elite	Misthalin: Varrock	Equip a Dark Shard or Sliver of Leng.	Equip either a Dark Shard of Leng or a Dark Sliver of Leng. (95 Attack, 95 Smithing, 95 Crafting)	200	<0.1%
125	Elite	Misthalin: Varrock	Craft 100 earth runes simultaneously without aid.	Craft 100 earth runes simultaneously without aid from an explorer's ring, pouches or familiars. (78 Runecrafting)	200	13.2%
126	Elite	Misthalin: Varrock	Bake a summer pie in the Cooking Guild from scratch.	Bake a summer pie in the Cooking Guild from scratch. (95 Cooking)	200	0.1%
758	Elite	Misthalin: Varrock	Defeat TzKal-Zuk.	Defeat TzKal-Zuk once.	200	2.6%
759	Elite	Misthalin: Varrock	Defeat TzKal-Zuk. (10 times)	Defeat TzKal-Zuk 10 times.	200	0.1%
760	Elite	Misthalin: City of Um	Craft a soul rune at the soul altar with a soul cape.	Craft a soul rune at the soul altar with a soul cape equipped. (90 Runecrafting, Completion of 'Phite Club, completion of Nomad's Elegy)	200	<0.1%
761	Elite	Misthalin: City of Um	Upgrade a set of Death Skull equipment to tier 90.	Upgrade a set of Death Skull equipment to tier 90. (10 Cooking, 90 Defence, 90 Necromancy)	200	0.5%
763	Elite	Misthalin: City of Um	Defeat Nakatra, Devourer Eternal. (100 times)	Defeat Nakatra, Devourer Eternal 100 times. (Completion of Necromancy!, completion of Soul Searching)	200	<0.1%
765	Elite	Misthalin: City of Um	Cleanse the Gate of Elidinis. (100 times)	Cleanse The Gate of Elidinis 100 times. (Completion of Ode of the Devourer or Soul Searching)	200	0.1%
769	Elite	Misthalin: City of Um	Complete the task set: Elite Underworld.	Complete the Elite Underworld achievements.	200	<0.1%
735	Elite	Morytania	Defeat 30 Abyssal Demons.	Defeat 30 abyssal demons. (85 Slayer)	200	9.9%
736	Elite	Morytania	Harvest 200 radiant energy from Radiant Wisps.	Harvest 200 radiant energy from radiant wisps. (85 Divination)	200	3.4%
737	Elite	Morytania	Defeat 20 Celestial Dragons.	Defeat 20 celestial dragons. (Completion of One of a Kind)	200	2.6%
738	Elite	Morytania	Defeat Araxxi.	Defeat Araxxi once.	200	8.4%
739	Elite	Morytania	Defeat Araxxi. (100 times)	Defeat Araxxi 100 times.	200	<0.1%
740	Elite	Morytania	Defeat the empowered Barrows Brothers.	Complete one Rise of the Six encounter.	200	1.7%
741	Elite	Morytania	Defeat the empowered Barrows Brothers.	Complete 100 Rise of the Six encounters.	200	<0.1%
742	Elite	Morytania	Equip a Noxious Scythe.	Equip a noxious scythe. (90 Crafting, 90 Attack)	200	0.5%
743	Elite	Morytania	Equip a Noxious Staff.	Equip a noxious staff. (90 Crafting, 90 Magic)	200	0.1%
744	Elite	Morytania	Equip a Noxious Bow.	Equip a noxious bow. (90 Crafting, 90 Ranged)	200	0.1%
745	Elite	Morytania	Equip a full set of Linza's equipment.	Equip a full set of Linza the Disgraced's equipment. (80 Attack, 80 Defence, Completion of Kindred Spirits)	200	<0.1%
746	Elite	Morytania	Equip a full set of Akrisae's equipment.	Equip a full set of Akrisae the Doomed's equipment. (70 Attack, 70 Ranged, 70 Magic, 70 Defence, Completion of Ritual of the Mahjarrat)	200	<0.1%
747	Elite	Morytania	Equip a Malevolent Kiteshield.	Equip a malevolent kiteshield. (90 Defence)	200	0.2%
748	Elite	Morytania	Equip a Merciless Kiteshield.	Equip a merciless kiteshield. (90 Defence)	200	0.2%
749	Elite	Morytania	Equip a Vengeful Kiteshield.	Equip a vengeful kiteshield. (90 Defence)	200	0.2%
750	Elite	Morytania	Complete all the Everlight mysteries.	Complete all of the Everlight Dig Site mysteries. (105 Archaeology, 40 Construction, 6 Hunter)	200	0.1%
751	Elite	Morytania	Obtain an Araxyte Pheremone drop.	Obtain an araxyte pheremone drop.	200	1.5%
752	Elite	Morytania	Complete the task set: Elite Morytania.	Complete the Elite Morytania achievements.	200	<0.1%
753	Elite	Morytania	Enter the Morytania Slayer Tower resource dungeon.	Enter the Morytania Slayer Tower dungeon. (100 Dungeoneering)	200	0.2%
757	Elite	Morytania	Read the book from Roberta outside the Everlight mine.	Read On the Origin of Centaurs. (102 Mining)	200	0.9%
551	Elite	Elven Lands: Tirranwn	Enter the Gorajo Hoardstalker resource dungeon.	Enter the Gorajo Hoardstalker Dungeon. (95 Dungeoneering)	200	0.4%
552	Elite	Elven Lands: Tirranwn	Have Lady Ithell create a crystal tool.	Have Lady Ithell create a crystal pickaxe, hatchet, or mattock.	200	<0.1%
553	Elite	Elven Lands: Tirranwn	Find all of the memoriam crystals in Prifddinas.	Find all of the memoriam crystals in Prifddinas. (77 Agility, 75 Farming, 50 Thieving, Completion of Fate of the Gods, partial completion of A Fairy Tale II - Cure a Queen)	200	<0.1%
554	Elite	Elven Lands: Tirranwn	Aid Lord Amlodd in cleansing shadow cores.	Complete the I'm Forever Washing Shadows achievement. (91 Divination)	200	0.2%
555	Elite	Elven Lands: Tirranwn	Help Lady Ithell with crystal singing research.	Complete the Sing for the Lady achievement. (75 Smithing, 75 Magic)	200	2%
556	Elite	Elven Lands: Tirranwn	Aid Lady Trahaearn by smelting 100 corrupted ore.	Complete the Uncorrupted Ore achievement. (89 Mining, 89 Smithing)	200	5.8%
557	Elite	Elven Lands: Tirranwn	Check a grown Crystal Tree in the Tower of Voices.	Check a grown crystal tree in the Tower of Voices. (94 Farming)	200	<0.1%
558	Elite	Elven Lands: Tirranwn	Have 4 elven clans suspect you of thieving.	Have 4 elven clans suspect you of thieving at the same time. (94 Thieving)	200	5.4%
559	Elite	Elven Lands: Tirranwn	Chop and fletch a log from your own elder tree in Prifddinas.	Chop a log from an elder tree you have grown in the Prifddinas farming patch, then fletch it into an elder shortbow. (90 Farming, 90 Woodcutting, 90 Fletching)	200	0.1%
560	Elite	Elven Lands: Tirranwn	Catch a Crystal impling.	Catch a crystal impling. Cannot be completed in Puro-Puro. (95 Hunter)	200	0.1%
561	Elite	Elven Lands: Tirranwn	Craft an Attuned crystal teleport seed.	Craft an attuned crystal teleport seed. (85 Smithing, Completion of The Eyes of Glouphrie)	200	<0.1%
562	Elite	Elven Lands: Tirranwn	Mine 50 Light animica in Isafdar.	Mine 50 light animica in Isafdar. (90 Mining)	200	18.3%
563	Elite	Elven Lands: Tirranwn	Chop 25 Elder logs in Tirannwn.	Chop 25 elder logs in Tirannwn. (90 Woodcutting)	200	0.6%
564	Elite	Elven Lands: Tirranwn	Catch 75 Crystal skillchompas in Isafdar.	Catch 75 crystal skillchompas in Isafdar. (97 Hunter)	200	<0.1%
565	Elite	Elven Lands: Tirranwn	Complete the task set: Elite Tirannwn.	Complete the Elite Tirannwn achievements.	200	<0.1%
566	Elite	Elven Lands: Tirranwn	Complete a Seren symbol.	Create a Seren's symbol. (98 Thieving or 77 Agility)	200	0.2%
567	Elite	Elven Lands: Tirranwn	Obtain the titles of the elven clans.	Obtain the titles of the elven clans.	200	<0.1%
568	Elite	Elven Lands: Tirranwn	Perform well in Rush of Blood to impress Morvran.	Complete the Make Them Bleed achievement. (85 Slayer)	200	<0.1%
569	Elite	Elven Lands: Tirranwn	Reach inside the Motherlode Maw 5 times.	Reach inside the Motherlode Maw 5 times. (115 Dungeoneering and level 95 in all other skills)	200	<0.1%
570	Elite	Elven Lands: Tirranwn	Obtain 'the Elven' title by purchasing all elven clan capes.	Obtain the Elven title by purchasing each of the elven clan capes. (8,000,000 coins)	200	7.4%
669	Elite	Wilderness: General	Equip the Hellfire bow.	Equip the hellfire bow. (90 Ranged)	200	0.2%
670	Elite	Wilderness: General	Complete a slayer task from Mandrith.	Complete a slayer task from Mandrith. (95 Slayer, 120 Combat)	200	3.7%
671	Elite	Wilderness: General	Chop 20 Bloodwood logs in the Wilderness.	Chop 20 bloodwood logs in the Wilderness. (85 Woodcutting)	200	0.8%
672	Elite	Wilderness: General	Unlock Greater Flurry, Barge, and Fury abilities.	Unlock the Greater Flurry, Barge, and Fury abilities.	200	0.2%
673	Elite	Wilderness: General	Crack 6 safes inside the Rogues' Castle.	Crack 6 safes inside the Rogues' Castle. (90 Thieving)	200	3.1%
674	Elite	Wilderness: General	Defeat 5 Ripper Demons.	Defeat 5 ripper demons. (96 Slayer)	200	4.2%
675	Elite	Wilderness: General	Defeat 10 Lava Strykewyrms in the Wilderness.	Defeat 10 lava strykewyrms in the Wilderness, south of the Lava Maze. (94 Slayer)	200	5.4%
676	Elite	Wilderness: General	Equip Annihilation, Decimation, or Obliteration.	Equip Annihilation, Decimation, or Obliteration. (87 Attack OR 87 Ranged OR 87 Magic)	200	0.1%
677	Elite	Wilderness: Daemonheim	Kill Blink in a solo Dungeoneering instance, without dying.	Kill Blink in a solo Dungeoneering instance without dying. (95 Dungeoneering)	200	0.1%
678	Elite	Wilderness: Daemonheim	Complete a solo Dungeoneering floor without dying.	Complete a solo Dungeoneering floor without dying. (1 Dungeoneering)	200	37.8%
679	Elite	Wilderness: General	Defeat every miniboss inside the Dragonkin Laboratory.	Defeat every miniboss inside the Dragonkin Laboratory.	200	0.1%
680	Elite	Wilderness: General	Defeat the Black Stone Dragon.	Defeat the black stone dragon once.	200	2.9%
681	Elite	Wilderness: General	Defeat the Black Stone Dragon. (25 times)	Defeat the black stone dragon 25 times.	200	<0.1%
682	Elite	Wilderness: General	Complete the task set: Elite Wilderness.	Complete the Elite Wilderness achievements.	200	0.1%
683	Elite	Wilderness: General	Defeat 25 Hydrix dragons in the Wilderness.	Defeat 25 hydrix dragons in the Wilderness. (101 Slayer)	200	1.1%
684	Elite	Wilderness: General	Defeat 10 Abyssal lords in the Wilderness.	Defeat 10 abyssal lords in the Wilderness. (115 Slayer)	200	0.3%
685	Elite	Wilderness: Daemonheim	Mine 30 Primal ores.	Mine 30 primal ores. (100 Mining)	200	5.5%
686	Elite	Wilderness: Daemonheim	Smelt 150 Primal bars.	Smelt 150 primal bars. (100 Mining, 100 Smithing)	200	3%
687	Elite	Wilderness: Daemonheim	Defeat Kal'Ger the Warmonger.	Defeat Kal'Ger the Warmonger. (113 Dungeoneering)	200	<0.1%
689	Elite	Wilderness: General	Defeat the Ambassador.	Defeat the Ambassador once.	200	1.4%
690	Elite	Wilderness: General	Defeat the Ambassador. (25 times)	Defeat the Ambassador 25 times.	200	<0.1%
691	Elite	Wilderness: General	Equip a Spectral, Arcane, Elysian, or Divine spirit shield.	Equip a spectral, arcane, Elysian, or divine spirit shield. (75 Defence, 75 Prayer, Completion of Summer's End)	200	<0.1%
692	Elite	Wilderness: General	Defeat the Ambassador after 4 unstable black holes explode.	Defeat the Ambassador after allowing 4 unstable black holes to explode.	200	0.2%
768	Elite	Misthalin: City of Um	Complete all of Rasial, the First Necromancer's combat achievements.	Complete all of Rasial, the First Necromancer's combat achievements. (Completion of Alpha vs Omega)	200	<0.1%
1114	Elite	Misthalin: Fort Forinthry	Defeat Zemouregal & Vorkath.	Defeat Zemouregal & Vorkath. (Completion of Battle of Forinthry)	200	0.9%
1115	Elite	Misthalin: Fort Forinthry	Defeat Zemouregal & Vorkath. (100 times)	Defeat Zemouregal & Vorkath 100 times. (Completion of Battle of Forinthry)	200	<0.1%
504	Master	Anachronia	Fully upgrade the Town Hall in the base camp on Anachronia.	Fully upgrade the town hall in the base camp on Anachronia.	400	0.4%
506	Master	Anachronia	Complete a big game encounter with 3 creatures active.	Complete a Big Game Hunter encounter with 3 creatures active. (75 Hunter, 55 Slayer)	400	<0.1%
507	Master	Anachronia	Breed a shiny dinosaur.	Breed a shiny dinosaur. (97 Farming)	400	<0.1%
510	Master	Anachronia	Equip Skeka's hypnowand.	Equip Skeka's hypnowand. (103 Archaeology, 95 Dungeoneering, 80 Hunter)	400	<0.1%
511	Master	Anachronia	Complete the quest: Extinction.	Complete the Extinction quest.	400	0.3%
261	Master	Asgarnia: Burthorpe	Complete all Combat Achievements for God Wars Dungeon bosses.	Complete all of the Combat Achievements for God Wars Dungeon bosses, including Nex.	400	<0.1%
262	Master	Asgarnia: Burthorpe	Unlock all the prayers from the Praesul Codex.	Unlock all the prayers from the Praesul codex.	400	<0.1%
336	Master	Desert: General	Defeat Telos, the Warden at 1,000% enrage.	Defeat Telos, the Warden at 1000% enrage. (80 Attack, 80 Prayer, 80 Magic, 80 Ranged)	400	<0.1%
338	Master	Desert: General	Complete all Combat Achievements for Heart of Gielinor bosses.	Complete all of the Combat Achievements for the Heart of Gielinor bosses (excluding Telos).	400	<0.1%
1113	Master	Desert: Menaphos	Defeat Amascut, the Devourer. (100 times)	Defeat Amascut, the Devourer 100 times. (Completion of Eclipse of the Heart)	400	<0.1%
396	Master	Fremennik: Mainland	Equip every completed God Book.	Equip every completed god book. (30 Prayer, Completion of Horror from the Deep)	400	<0.1%
146	Master	Global	Reach maximum total level.	Reach maximum total level. (3095)	400	<0.1%
963	Master	Global	Complete 150 Master clue scrolls.	Complete 150 master clue scrolls.	400	<0.1%
1088	Master	Global	Obtain a pickaxe of life and death.	Create a pickaxe of life and death. (100 Mining, 100 Smithing, 90 Necromancy, Completion of multiple quests)	400	<0.1%
1089	Master	Global	Have something planted and living in every farming patch.	Have something planted and living in every farming patch. (119 Farming, Completion of multiple quests)	400	<0.1%
1090	Master	Global	Obtain a hatchet of bloom and blight.	Create a hatchet of bloom and blight. (100 Smithing, 100 Woodcutting, 100 Fletching, 90 Necromancy, Completion of Kili Row and Pieces of Hate)	400	<0.1%
1091	Master	Global	Equip any Masterwork weapon.	Equip any masterwork weapon.	400	<0.1%
1092	Master	Global	Equip a full set of Masterwork armour.	Equip a full set of masterwork armour. (99 Smithing, 90 Defence)	400	0.2%
1093	Master	Global	Unlock the Richie pet.	Donate 100,000,000 GP to Richie.	400	9.7%
1095	Master	Global	Obtain 200 Million XP in any single skill.	Obtain 200 Million XP in any single skill.	400	11.1%
1096	Master	Global	Fill all of the Treasure Trail hidey-holes.	Fill all of the Treasure Trail hidey-holes. (88 Construction)	400	<0.1%
1097	Master	Global	Obtain a dye, Third-age, or Second-age gear.	Obtain a dye, or a piece of Third-age or Second-age gear from a clue scroll.	400	14.2%
1111	Master	Global	Reach at least level 95 in all non-elite skills.	Reach at least level 95 in all non-elite skills.	400	<0.1%
456	Master	Kandarin: Feldip Hills	Equip an Expert Dragon Archer hat.	Equip an Expert Dragon Archer hat. (4,000 chompy bird kills)	400	<0.1%
458	Master	Kandarin: Ardougne	Throw 100,000,000 gold coins into the Whirlpool.	Throw 100,000,000 gold coins into the Whirlpool at the Deep Sea Fishing platform. (68 Fishing)	400	5.7%
122	Master	Misthalin: Varrock	Equip an Ek-ZekKil.	Equip an Ek-ZekKil. (95 Strength, 95 Smithing)	400	0.1%
123	Master	Misthalin: Varrock	Equip a Fractured Staff of Armadyl.	Equip a Fractured Staff of Armadyl. (95 Magic, 95 Crafting)	400	<0.1%
767	Master	Misthalin: City of Um	Complete all Sanctum of Rebirth combat achievements.	Complete all Sanctum of Rebirth combat achievements. (Completion of Soul Searching)	400	<0.1%
768	Master	Misthalin: City of Um	Complete all of Rasial, the First Necromancer's combat achievements.	Complete all of Rasial, the First Necromancer's combat achievements. (Completion of Alpha vs Omega)	400	<0.1%
754	Master	Morytania	Fully explore the history of the Everlight Dig Site.	Complete the Mastery - Everlight achievements. (105 Archaeology, 40 Construction, 6 Hunter)	400	0.1%
755	Master	Morytania	Complete all Araxxor and Araxxi combat achievements.	Complete all Araxxor and Araxxi combat achievements.	400	<0.1%
756	Master	Morytania	Complete the quest: River of Blood.	Complete River of Blood.	400	0.2%
571	Master	Elven Lands: Tirranwn	Obtain the 'Dark Lord' title.	Obtain the Dark Lord title by completing the Sort of Crystally achievement.	400	<0.1%
688	Master	Wilderness: General	Equip an Eldritch Crossbow.	Equip an eldritch crossbow. (92 Ranged, 96 Fletching)	400	<0.1%
1116	Master	Misthalin: Varrock	Equip an igneous Kal-Zuk cape.	Equip an igneous Kal-Zuk cape. (90 Crafting, Completion of the Excuse Me, That's My Seat achievement)	400	<0.1%
"""

def parse_tasks(raw_text):
    tasks = {"Easy": [], "Medium": [], "Hard": [], "Elite": [], "Master": []}
    lines = raw_text.strip().split('\n')

    # Skip the header line
    for i, line in enumerate(lines[1:]):
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')

        if len(parts) != 7:
            print(f"WARNING: Line {i+2} has {len(parts)} parts, expected 7: {line}")
            continue

        try:
            task_id = int(parts[0])
            tier = parts[1].strip()
            locality = parts[2].strip()
            task_desc = parts[3].strip()
            information = parts[4].strip()
            points = int(parts[5])

            task_data = {
                "id": task_id,
                "locality": locality,
                "task": task_desc,
                "information": information,
                "requirements": "N/A",
                "tier": tier,
                "points": points
            }

            req_match = re.search(r'\((.*?)\)', information)
            if req_match:
                task_data["requirements"] = req_match.group(1)

            if tier in tasks:
                tasks[tier].append(task_data)
            else:
                print(f"WARNING: Unknown tier '{tier}' on line {i+2}: {line}")


        except (ValueError, IndexError) as e:
            print(f"ERROR: Could not parse line {i+2}: {line} -> {e}")
            continue

    return tasks

if __name__ == "__main__":
    parsed_tasks = parse_tasks(full_raw_data)

    print("\n--- Verification ---")
    total_tasks = 0
    total_points = 0
    for tier, task_list in parsed_tasks.items():
        unique_tasks_dict = {task['id']: task for task in task_list}
        unique_tasks_list = list(unique_tasks_dict.values())

        parsed_tasks[tier] = unique_tasks_list

        tier_points = sum(task['points'] for task in parsed_tasks[tier])
        total_tasks += len(parsed_tasks[tier])
        total_points += tier_points
        print(f"{tier}: {len(parsed_tasks[tier])} tasks, {tier_points} points")

    print("--------------------")
    print(f"Total Tasks: {total_tasks}")
    print(f"Total Points: {total_points}")
    print("--------------------")

    with open('tasks.json', 'w') as f:
        json.dump(parsed_tasks, f, indent=2)
    print("tasks.json file has been created successfully.")