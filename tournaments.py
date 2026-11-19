"""Tournaments: setup (basics, sports, interest, registration, review) and the organizer workspace.

Formats follow Regulars_Sports_Formats_and_Tags (v0.4) and Figma "21 · Tournaments" / "22 · Tournament module":
five format presets A–E; a sport lists the presets it allows and a default; formats attach to stages,
so a sport can mix them (pools A → bracket A, heats B → final B). Two or more sports = multi-sport (F).
Fees are a demo until Stripe is connected: nothing is charged.
Schema changes are additive only. Nothing here rewrites or deletes rows on boot.
"""
import datetime as dt
import re
import secrets

PRESETS = {
    # code: (name, one line, example sports, tone)
    "A": ("Head-to-head", "Two sides play. A score decides.", "Water polo · volleyball · tennis · basketball", "sun"),
    "B": ("Timed", "Fastest time wins.", "Swim · run · row · cycle", "sky"),
    "C": ("Measured", "Longest, highest, heaviest wins.", "Jumps · throws · lifts", "tangerine"),
    "D": ("Judged", "A panel scores a performance.", "Diving · gymnastics · surf · skate", "lavender"),
    "E": ("Scored rounds", "Points add up over rounds.", "Golf · bowling · archery · disc golf", "aqua"),
}
PRESET_DIMS = {
    "A": (("Entrant", "Team or individual"), ("Structure", "Pools → bracket"), ("Result", "Score"), ("Ranking", "Match points"), ("Progression", "Top N advance")),
    "B": (("Entrant", "Individual / relay"), ("Structure", "Heats & lanes"), ("Result", "Time"), ("Ranking", "Fastest"), ("Progression", "Prelims → final")),
    "C": (("Entrant", "Individual"), ("Structure", "Flights · 3 attempts"), ("Result", "Distance / height / kg"), ("Ranking", "Best mark"), ("Progression", "Top 8 get 3 more")),
    "D": (("Entrant", "Individual / pair"), ("Structure", "Start order · rounds"), ("Result", "Panel × DD"), ("Ranking", "Highest total"), ("Progression", "Semi → final")),
    "E": (("Entrant", "Individual / team"), ("Structure", "Rounds · holes · frames"), ("Result", "Strokes / pins"), ("Ranking", "Low or high total"), ("Progression", "Cut line")),
}

# key, name, discipline / family, default preset, allowed presets, typical stages, category, support tier
CATALOG = [
    ["swimming", "Swimming", "", "B", "BE", "Heats B → final B; swim-off B for ties; team points E", "olympic", "Supported"],
    ["water-polo", "Water polo", "", "A", "A", "Pools A (points table) → crossovers/knockout A → penalty shootout stage A", "olympic", "Supported"],
    ["open-water-swimming", "Open water swimming", "Marathon swimming / open water", "B", "BE", "Single B race; series totals E", "olympic", "Generic"],
    ["diving", "Diving", "", "D", "D", "Prelim D → final D", "olympic", "Generic – manual"],
    ["artistic-swimming", "Artistic swimming", "", "D", "DE", "Routines D; figures + routine combined (E) in youth", "olympic", "Generic – manual"],
    ["archery", "Archery", "", "C", "AC", "Ranking round C → elimination matches A; shoot-off for ties", "olympic", "Generic"],
    ["athletics", "Athletics", "Track, road, field, combined events", "B", "BCE", "Track: heats B → final B · Field: qualifying C → final C · Combined: E over B + C", "olympic", "Generic"],
    ["badminton", "Badminton", "", "A", "A", "Groups A → knockout A", "olympic", "Generic"],
    ["baseball-and-softball", "Baseball and softball", "Baseball, softball", "A", "A", "Pool play A → bracket A (often double elimination)", "olympic", "Generic"],
    ["basketball", "Basketball", "5x5, 3x3", "A", "A", "Pools/league A → bracket A; overtime per rule pack", "olympic", "Generic"],
    ["boxing", "Boxing", "", "A", "A", "Elimination bouts A (decision entered manually)", "olympic", "Generic"],
    ["canoe-sprint", "Canoe sprint", "Sprint", "B", "B", "Heats B → semis B → final B", "olympic", "Generic"],
    ["canoe-slalom", "Canoe slalom", "Slalom", "B", "B", "Heats B (time + penalties) → semi → final B", "olympic", "Generic"],
    ["cricket", "Cricket", "", "A", "A", "Group/league A → knockout A; tie-breaker (e.g. super over) per playing conditions (verify)", "olympic", "Generic"],
    ["road-cycling", "Road cycling", "Road", "B", "BE", "Road race / TT B; stage race E over B stages", "olympic", "Generic"],
    ["track-cycling", "Track cycling", "Track", "A", "ABE", "Sprint: B qualifier → A bracket · Pursuit/TT: B · Omnium/points: E", "olympic", "Generic"],
    ["mountain-bike-bmx-racing", "Mountain bike & BMX racing", "Mountain bike, BMX racing", "B", "B", "BMX: motos B → final B · MTB: single B race", "olympic", "Generic"],
    ["bmx-freestyle", "BMX freestyle", "", "D", "D", "Qualification D → final D", "olympic", "Generic – manual"],
    ["equestrian", "Equestrian", "Dressage, jumping, eventing", "C", "BCDE", "Dressage D · Jumping C/B (faults + time) → jump-off · Eventing E over D + C", "olympic", "Generic – manual"],
    ["fencing", "Fencing", "Fencing (foil, épée, sabre)", "A", "A", "Pools A → seeded direct elimination A", "olympic", "Generic"],
    ["field-hockey", "Field hockey", "", "A", "A", "Group/league A (points table) → knockout A; drawn knockout → extra time/shootout stage per rule pack", "olympic", "Generic"],
    ["flag-football", "Flag football", "", "A", "A", "Round robin/league A → playoff bracket A", "olympic", "Generic"],
    ["soccer", "Soccer", "Football (soccer)", "A", "A", "Group/league A (points table) → knockout A; drawn knockout → extra time/shootout stage per rule pack", "olympic", "Generic"],
    ["golf", "Golf", "", "C", "ACE", "Stroke play C, E over rounds → cut → playoff · Match play A", "olympic", "Generic"],
    ["gymnastics", "Gymnastics", "Artistic, rhythmic, trampoline", "D", "DE", "Qualification D → apparatus finals D; all-around E", "olympic", "Generic – manual"],
    ["handball", "Handball", "Indoor", "A", "A", "Group/league A (points table) → knockout A; drawn knockout → extra time/shootout stage per rule pack", "olympic", "Generic"],
    ["judo", "Judo", "", "A", "A", "Elimination A (+ repechage) → bronze bouts; golden score per rules", "olympic", "Generic"],
    ["lacrosse", "Lacrosse", "Sixes", "A", "A", "Round robin/league A → playoff bracket A", "olympic", "Generic"],
    ["modern-pentathlon", "Modern pentathlon", "", "E", "ABE", "E over A (fencing), B (swim, laser-run) and obstacle/riding", "olympic", "Generic – manual"],
    ["rowing", "Rowing", "Rowing, coastal", "B", "B", "Heats B → repechage B → final B", "olympic", "Generic"],
    ["rugby-sevens", "Rugby sevens", "Sevens", "A", "A", "Pools A → cup/placement brackets A", "olympic", "Generic"],
    ["sailing", "Sailing", "", "E", "BE", "Races B (finish order) → series E (low-point, discards) → medal race (verify)", "olympic", "Generic – manual"],
    ["shooting", "Shooting", "", "C", "C", "Qualification C → final C (elimination format; verify)", "olympic", "Generic – manual"],
    ["skateboarding", "Skateboarding", "Street, park", "D", "D", "Heats D → final D", "olympic", "Generic – manual"],
    ["sport-climbing", "Sport climbing", "Boulder, lead, speed", "C", "ABC", "Boulder/lead: qualification C → final C · Speed: B qualifier → A bracket", "olympic", "Generic – manual"],
    ["squash", "Squash", "", "A", "A", "Draws/ladders A", "olympic", "Generic"],
    ["surfing", "Surfing", "", "D", "D", "Heats D → elimination by heat place", "olympic", "Generic – manual"],
    ["table-tennis", "Table tennis", "", "A", "A", "Groups A → knockout A", "olympic", "Generic"],
    ["taekwondo", "Taekwondo", "", "A", "A", "Elimination A (+ repechage in some events; verify)", "olympic", "Generic"],
    ["tennis", "Tennis", "", "A", "A", "Round robin A → draw A; tiebreak games inside the match", "olympic", "Generic"],
    ["triathlon", "Triathlon", "", "B", "BE", "E over B legs; relays as relay entrants", "olympic", "Generic"],
    ["volleyball", "Volleyball", "Indoor, beach", "A", "A", "Pools A → bracket A", "olympic", "Generic"],
    ["weightlifting", "Weightlifting", "", "C", "CE", "Flights C per lift → total (E-like)", "olympic", "Generic"],
    ["wrestling", "Wrestling", "Freestyle, Greco-Roman", "A", "A", "Elimination A (+ repechage; verify)", "olympic", "Generic"],
    ["biathlon", "Biathlon", "", "B", "B", "Sprint B → pursuit B (start gaps from sprint)", "olympic", "Generic – manual"],
    ["bobsleigh-skeleton-luge", "Bobsleigh / skeleton / luge", "Bobsleigh, skeleton, luge", "B", "BE", "Runs B → E sum of runs", "olympic", "Generic – manual"],
    ["curling", "Curling", "", "A", "A", "Round robin A → playoffs A; extra end for ties", "olympic", "Generic"],
    ["ice-hockey", "Ice hockey", "", "A", "A", "Group/league A → knockout A; overtime/shootout stage per rule pack", "olympic", "Generic"],
    ["figure-skating", "Figure skating", "", "D", "DE", "Short program D + free D → E total", "olympic", "Generic – manual"],
    ["speed-skating", "Speed skating", "Speed skating, short track", "B", "AB", "Long track: pairs B · Short track: heats A (finish order) → final", "olympic", "Generic"],
    ["skiing-alpine-nordic", "Skiing (alpine & nordic)", "Alpine, cross-country, ski mountaineering", "B", "ABE", "Runs B → E combined time; sprint heats A in cross-country", "olympic", "Generic – manual"],
    ["freestyle-ski-snowboard", "Freestyle ski & snowboard", "Freestyle, freeride, snowboard park, ski jumping", "D", "CD", "Qualification D → final D; ski jumping D + C distance", "olympic", "Generic – manual"],
    ["ski-snowboard-cross", "Ski & snowboard cross", "Cross events (ski/snowboard cross), parallel snowboard", "A", "AB", "Seeding run B → heats/head-to-head A", "olympic", "Generic"],
    ["kickball", "Kickball", "Adult co-ed", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["dodgeball", "Dodgeball", "Foam / cloth", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["cornhole", "Cornhole", "Bags", "A", "A", "Round robin A → bracket A (often double elimination)", "adult_rec", "Generic"],
    ["bowling", "Bowling", "Ten-pin", "C", "ACE", "Qualifying C (pinfall) → match-play A; league totals E", "adult_rec", "Generic"],
    ["darts", "Darts", "Steel-tip / soft-tip", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["bocce-petanque", "Bocce / pétanque", "Bocce / pétanque / boule lyonnaise", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["disc-golf", "Disc golf", "", "C", "ACE", "Rounds C → E total; doubles; match play A", "adult_rec", "Generic"],
    ["ultimate-frisbee", "Ultimate frisbee", "Ultimate", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["pickleball", "Pickleball", "", "A", "A", "Round robin A → bracket A", "adult_rec", "Generic"],
    ["padel", "Padel", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["racquetball", "Racquetball", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["roundnet-spikeball", "Roundnet (Spikeball)", "Spikeball / roundnet", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["touch-rugby", "Touch rugby", "Touch rugby / touch football", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["rugby-league", "Rugby league", "Rugby league / nines / masters (modified)", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["netball", "Netball", "Netball / walking netball", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["futsal-small-sided-soccer", "Futsal & small-sided soccer", "Futsal, walking football, beach soccer", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["slow-pitch-softball", "Slow-pitch softball", "Slow-pitch", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["road-running", "Road running", "Run clubs / parkrun / road races", "B", "B", "Single B race", "adult_rec", "Generic"],
    ["gran-fondo", "Gran fondo", "Group rides / gran fondos", "B", "B", "Same format in every stage", "adult_rec", "Generic"],
    ["axe-throwing", "Axe throwing", "", "C", "AC", "League matches A scored by C target points", "adult_rec", "Generic"],
    ["billiards", "Billiards", "Pool / snooker / carom", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["roller-hockey", "Roller hockey", "Roller / inline hockey", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["broomball", "Broomball", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["underwater-hockey", "Underwater hockey", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["korfball", "Korfball", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["quadball", "Quadball", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["footvolley", "Footvolley", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["sepak-takraw", "Sepak takraw", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["dragon-boat-outrigger", "Dragon boat & outrigger", "Dragon boat, outrigger (va'a), SUP", "B", "B", "Heats B → final B", "adult_rec", "Generic"],
    ["canoe-polo", "Canoe polo", "Canoe polo (kayak polo)", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["functional-fitness", "Functional fitness", "Functional fitness (CrossFit-style)", "E", "BCE", "Workouts B (time), C (reps/load) → E overall points", "adult_rec", "Generic – manual"],
    ["fitness-racing-hyrox", "Fitness racing (HYROX)", "", "B", "B", "Same format in every stage", "adult_rec", "Generic"],
    ["obstacle-course-racing", "Obstacle course racing", "OCR", "B", "B", "Same format in every stage", "adult_rec", "Generic"],
    ["footgolf-mini-golf", "FootGolf & mini golf", "FootGolf, mini golf", "C", "CE", "Rounds C → E total", "adult_rec", "Generic"],
    ["gaelic-games", "Gaelic games", "Gaelic football / hurling / camogie", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["aussie-rules", "Aussie rules", "Aussie rules / AFL Masters", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["social-cricket", "Social cricket", "Indoor / social T20 / softball cricket", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["lawn-bowls", "Lawn bowls", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["shuffleboard", "Shuffleboard", "Court (deck), table", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["floorball", "Floorball", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["roller-derby", "Roller derby", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["wall-handball", "Wall handball", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["platform-tennis", "Platform tennis", "Platform tennis (paddle)", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["kickboxing-muay-thai", "Kickboxing & muay thai", "Kickboxing, muay thai", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["brazilian-jiu-jitsu", "Brazilian jiu-jitsu", "BJJ", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["powerlifting", "Powerlifting", "", "C", "CE", "Flights C per lift → total (E-like)", "adult_rec", "Generic"],
    ["orienteering", "Orienteering", "", "B", "B", "Single B course; relays", "adult_rec", "Generic"],
    ["surf-lifesaving", "Surf lifesaving", "", "B", "ABE", "Races B · Beach flags A elimination · Carnival points E", "adult_rec", "Generic"],
    ["trail-running", "Trail running", "Trail / ultra", "B", "B", "Same format in every stage", "adult_rec", "Generic"],
    ["box-lacrosse", "Box lacrosse", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["inner-tube-water-polo", "Inner-tube water polo", "", "A", "A", "Same format in every stage", "adult_rec", "Generic"],
    ["underwater-rugby", "Underwater rugby", "", "A", "A", "Head-to-head matches; tournaments typically use pools or round robin then a knockout. Two teams compete underwater with a ball and a heavy goal on the pool bottom.", "niche", "Generic"],
    ["underwater-torpedo", "Underwater torpedo", "", "A", "A", "Seeding games then a knockout (Aqua Bowl). Line changes mid-game are used like hockey. Safety referees in the water.", "niche", "Generic"],
    ["finswimming", "Finswimming", "", "B", "B", "Heats and finals by time, like pool swimming, across pool and open-water distances. Relays exist. Para finswimming is a CMAS parasport.", "niche", "Generic"],
    ["freediving", "Freediving", "", "B", "BE", "Ranked by time (static), distance (dynamic pool) or depth (open water). Series or combined-event totals can use E. Safety protocols are the organiser's responsibility, no", "niche", "Generic"],
    ["spearfishing", "Spearfishing", "", "C", "CE", "Competitors are ranked by catch points (species, size, count) over a timed session. Team totals possible (E). Local fishing law and safety are the organiser's responsibil", "niche", "Generic"],
    ["underwater-target-shooting", "Underwater target shooting", "", "C", "BCE", "Precision is measured target scores (C). Biathlon/super biathlon mix swimming (B) with target scores (C); combined ranking may use E.", "niche", "Generic"],
    ["aquathlon-cmas", "Aquathlon (CMAS)", "", "A", "A", "Head-to-head bouts, usually by weight class, with elimination or pool-to-bracket tournaments. Do not confuse with World Triathlon aquathlon.", "niche", "Generic"],
    ["mermaiding", "Mermaiding", "", "D", "D", "Judged skill and dance routines (solo, synchro, group). Scores entered by the organiser in v1; no panel engine.", "niche", "Generic – manual"],
    ["underwater-orienteering", "Underwater orienteering", "", "B", "BCE", "Courses are completed underwater with compass/distance; ranking by time and/or course accuracy (B and C). Team events can use E.", "niche", "Generic"],
    ["sport-diving", "Sport diving", "", "E", "BCE", "Mix of timed skills (B), measured tasks (C) and team totals (E). Organiser-entered results in v1; verify event list against current CMAS rules.", "niche", "Generic – manual"],
    ["high-diving", "High diving", "", "D", "D", "Judged dives (degree of difficulty x judges' awards), prelims to finals. v1: manual final scores only (same as Olympic diving).", "niche", "Generic – manual"],
    ["waterskiing", "Waterskiing", "", "C", "CDE", "Slalom and jump are measured (C); tricks are judged (D). Rankings can sum events (E). Barefoot, show ski and cable ski are other IWWF disciplines. Motorboat/cable venue a", "niche", "Generic – manual"],
    ["wakeboarding", "Wakeboarding", "", "D", "D", "Judged runs or heats to finals. v1: manual scores or placings. Cable wakeboard has its own IWWF rules.", "niche", "Generic – manual"],
    ["wakesurfing", "Wakesurfing", "", "D", "D", "Judged rides, typically heats to finals. v1: manual scores or placings.", "niche", "Generic – manual"],
    ["rafting", "Rafting", "", "B", "ABE", "Some events are pure timed races (B); head-to-head / knockout formats use A; a championship often combines several event types into an overall (E).", "niche", "Generic"],
    ["gig-rowing", "Gig rowing", "", "B", "BE", "Mass-start or timed races for six-person crews plus cox. Regattas may have several races; overall points can use E.", "niche", "Generic"],
    ["kabaddi", "Kabaddi", "", "A", "A", "Head-to-head matches, league seasons and knockout championships. Circle and standard rulesets differ (verify rule pack). Also in Demonstration tab.", "niche", "Generic"],
    ["kho-kho", "Kho kho", "", "A", "A", "Head-to-head innings matches; tournaments use pools and knockouts. Also appeared as an Olympic demonstration sport. Also in Demonstration tab.", "niche", "Generic"],
    ["shinty", "Shinty", "", "A", "A", "League season plus knockout cups. International shinty-hurling composites exist (verify).", "niche", "Generic"],
    ["teqball", "Teqball", "", "A", "A", "Sets and matches, typically groups then knockout. Played on a curved table, no hands.", "niche", "Generic"],
    ["padbol", "Padbol", "", "A", "A", "Doubles matches, sets, tournament brackets or short leagues.", "niche", "Generic"],
    ["kin-ball", "Kin-Ball", "", "A", "A", "Unusual three-team scoring (not two-sided). Tournaments still use match wins and tables. Regulars' default two-side head-to-head may need a three-side extension or manual", "niche", "Generic – manual"],
    ["fistball", "Fistball", "", "A", "A", "Sets like volleyball; league and championship structures, including indoor and outdoor seasons.", "niche", "Generic"],
    ["tchoukball", "Tchoukball", "", "A", "A", "Head-to-head matches, pools and knockouts. No blocking of shots, which is a rule-pack detail, not a format change.", "niche", "Generic"],
    ["hardcourt-bike-polo", "Hardcourt bike polo", "", "A", "A", "Round robin or pools to knockout; club club-nights and weekend tournaments. Typical format is first to a set number of goals in a short game.", "niche", "Generic"],
    ["unicycle-hockey", "Unicycle hockey", "", "A", "A", "Head-to-head matches, league or tournament brackets, similar to indoor hockey.", "niche", "Generic"],
    ["horseball", "Horseball", "", "A", "A", "Head-to-head matches, league and championships. Entrant is the rider; horse name is free text.", "niche", "Generic – manual"],
    ["cycle-ball", "Cycle-ball", "", "A", "AD", "Short two-half matches; championships and club competitions. Artistic cycling would use D if tagged later.", "niche", "Generic"],
    ["pesapallo", "Pesäpallo", "", "A", "A", "Innings-based matches; league season plus playoffs. Scoring and advancing rules differ from baseball (rule pack, not a new format). Also in Demonstration tab.", "niche", "Generic"],
    ["futnet", "Futnet", "", "A", "A", "Sets and matches, tournament brackets. Verify current IF name and ruleset before encoding a sport pack.", "niche", "Generic"],
    ["soft-tennis", "Soft tennis", "", "A", "A", "Sets and matches, singles and doubles, groups and knockouts — same shape as tennis.", "niche", "Generic"],
    ["gaelic-handball", "Gaelic handball", "", "A", "A", "Singles or doubles matches, championship brackets and graded adult competitions. Court codes differ (verify).", "niche", "Generic"],
    ["polocrosse", "Polocrosse", "", "A", "A", "Head-to-head chukkas/sections, tournament or carnival formats. Entrant is the rider; horse name is free text.", "niche", "Generic – manual"],
    ["intercrosse", "Intercrosse", "", "A", "A", "Head-to-head matches, leagues and tournaments.", "niche", "Generic"],
    ["slamball", "SlamBall", "", "A", "A", "Head-to-head games, typically a short season or showcase tournament. Scoring resembles basketball.", "niche", "Generic"],
    ["bossaball", "Bossaball", "", "A", "A", "Sets like volleyball, often event or exhibition brackets rather than national leagues.", "niche", "Generic"],
    ["schwingen", "Schwingen", "", "A", "A", "Bouts scored by throws; festivals use a bout/gang structure rather than a simple bracket (verify mapping). Enter winners and points; do not encode festival scoring in v1.", "niche", "Generic"],
    ["sumo", "Sumo", "", "A", "A", "Elimination bouts by weight class. Winner and method entered manually; no judges'-tab engine required for a basic tournament.", "niche", "Generic"],
    ["sambo", "Sambo", "", "A", "A", "Elimination or repechage by weight class. Combat sambo adds striking (sanctioning/medical are the organiser's). Enter winner and method.", "niche", "Generic"],
    ["kendo", "Kendo", "", "A", "AE", "Point-bout shiai, usually elimination by weight or open class, plus team matches (E of individual bouts). Point values come from a rule pack; v1 can record bout winners o", "niche", "Generic"],
    ["capoeira", "Capoeira", "", "D", "AD", "WCF events use judged bouts and/or match wins (A + D). v1: enter places or bout winners manually. Do not encode WCF scoring in v1.", "niche", "Generic – manual"],
    ["wushu", "Wushu", "", "A", "ADE", "Sanda: elimination bouts (A). Taolu: judged performances (D), prelims to finals. Combined team totals possible (E). v1: generic A for sanda; manual scores for taolu.", "niche", "Generic"],
    ["ju-jitsu-jjif", "Ju-jitsu (JJIF)", "", "A", "AD", "Fighting and ne-waza are head-to-head bouts by weight class (A). Duo is a judged pair demonstration (D). Do not merge this tag with BJJ.", "niche", "Generic"],
    ["arm-wrestling", "Arm wrestling", "", "A", "A", "Best-of series in a weight class, often a bracket or double-elimination. Left and right arms are usually separate events.", "niche", "Generic"],
    ["mixed-martial-arts", "Mixed martial arts", "", "A", "A", "Elimination bouts by weight class. Enter winner and method (decision/stoppage); no scorecard engine in v1.", "niche", "Generic"],
    ["molkky", "Mölkky", "", "C", "AC", "Players score by knocking numbered pins (C). Events often use pools or Swiss then a knockout (A stages around a measured score).", "niche", "Generic"],
    ["kubb", "Kubb", "", "A", "A", "Head-to-head matches (knock over the king to win) in brackets or pools; throwing accuracy is the skill, but the contest is match play (A), not a pure measured ranking.", "niche", "Generic"],
    ["crokinole", "Crokinole", "", "A", "AC", "Head-to-head or multi-player rounds scored by shots (C points inside A/Swiss or round-robin stages). Typical event is a points tour to a championship.", "niche", "Generic"],
    ["knife-throwing", "Knife throwing", "", "C", "AC", "Standard is points on a target (C), often in flights or rounds then a final. Some league nights use match play (A).", "niche", "Generic"],
    ["casting-sport", "Casting sport", "", "C", "CE", "Accuracy and distance events (C). Championships combine several events into an overall (E).", "niche", "Generic"],
    ["carrom", "Carrom", "", "A", "A", "Head-to-head boards/matches with point scores; tournament brackets or leagues.", "niche", "Generic"],
    ["ice-stock-sport", "Ice stock sport", "", "C", "AC", "Target and distance events are measured (C); team target play can feel like head-to-head curling-style matches (A). Also in Demonstration tab.", "niche", "Generic"],
    ["hornussen", "Hornussen", "", "A", "AC", "Team innings with measured placements/points (C inside A). Festival and championship structures; do not encode scoring in v1 (enter team scores or places).", "niche", "Generic – manual"],
    ["strongman", "Strongman", "", "C", "BCE", "Each contest is a series of measured, timed or max-load events (C and B) added into an overall (E). v1: enter event results or overall points; official scoring tables lat", "niche", "Generic"],
    ["highland-games", "Highland games", "", "C", "ACDE", "Most throws are measured (C); caber is judged for the angle of the toss (D). A games total across events is E. Track/pipe-band elements of a games are separate tags if ne", "niche", "Generic"],
    ["timbersports", "Timbersports", "", "C", "BCE", "Most disciplines are timed (B) or measured; a competition total is E. Heats to finals on some disciplines.", "niche", "Generic"],
    ["mallakhamb", "Mallakhamb", "", "D", "BD", "Judged routines and/or timed/held elements (D, sometimes B). v1: manual scores or placings. Also in Demonstration tab.", "niche", "Generic – manual"],
    ["pole-sports", "Pole sports", "", "D", "D", "Judged routines, often prelims to finals, sometimes with difficulty catalogues. v1: manual scores only; no panel engine.", "niche", "Generic – manual"],
    ["swimrun", "Swimrun", "", "B", "BE", "Mass-start endurance race ranked by time (B), usually pairs. Series rankings use E. Course and safety ops are the organiser's.", "niche", "Generic"],
    ["aquathlon-world-triathlon", "Aquathlon (World Triathlon)", "", "B", "BE", "Single continuous race ranked by time, or a series (E). Waves or mass start.", "niche", "Generic"],
    ["duathlon", "Duathlon", "", "B", "BE", "Single race by time, or series totals (E).", "niche", "Generic"],
    ["biathle-triathle", "Biathle / triathle", "", "B", "BE", "Continuous or heat format ranked by time (B), with shooting penalties in triathle. Series use E. Shooting is organiser-scored in v1.", "niche", "Generic"],
    ["rogaining", "Rogaining", "", "C", "BCE", "Score-orienteering: most points in a time window (C), ties broken by time (B). Overall is a single stage, sometimes with a series (E).", "niche", "Generic"],
    ["skyrunning", "Skyrunning", "", "B", "BE", "Mass-start races ranked by time; series rankings use E.", "niche", "Generic"],
    ["adventure-racing", "Adventure racing", "", "E", "BCE", "Overall ranking by time or official points across a course of mixed legs (E over B/C). v1: enter official team times or places; do not model the full expedition course.", "niche", "Generic – manual"],
    ["canicross", "Canicross", "", "B", "BE", "Timed individual (or sometimes mass-start) races; series use E. Entrant is the runner; dog name is free text.", "niche", "Generic – manual"],
    ["parkour", "Parkour", "", "B", "BD", "Speed is a timed run (B, heats/finals). Freestyle is judged (D). v1: generic timed ranking for speed; manual scores for freestyle.", "niche", "Generic"],
    ["ninja", "Ninja", "", "B", "BCE", "Usually timed runs (B), sometimes with stage clears or points (C/E), and finals. Manual or CSV times in v1.", "niche", "Generic"],
    ["sport-stacking", "Sport stacking", "", "B", "B", "Timed routines (individual and relays), often with heats or age/open divisions. Ranked by time.", "niche", "Generic"],
    ["drone-racing", "Drone racing", "", "B", "ABE", "Heats and finals ranked by time or by finish order / points (B, sometimes A race-head-to-head, series E). v1: manual or CSV times/places. Closer to motorsport than to ath", "niche", "Generic – manual"],
    ["inline-speed-skating", "Inline speed skating", "", "B", "B", "Time trials, pack races and relays; championships use heats and finals. Ranked by time or finish order.", "niche", "Generic"],
    ["ringette", "Ringette", "", "A", "A", "League season and championships, plus international tournaments. Head-to-head ice games.", "niche", "Generic"],
    ["bandy", "Bandy", "", "A", "A", "League season plus knockout cups and world championships. 11-a-side on ice (rink bandy is a smaller variant). Also in Demonstration tab.", "niche", "Generic"],
    ["rinkball", "Rinkball", "", "A", "A", "League and cup matches, plus an open SM tournament. Head-to-head ice games.", "niche", "Generic"],
    ["skijoring", "Skijoring", "", "B", "BE", "Timed races, often by class; series use E. Entrant is the skier; dog/horse name is free text. Also in Demonstration tab.", "niche", "Generic – manual"],
    ["sled-dog-racing", "Sled dog racing", "", "B", "BE", "Timed races, sometimes multi-stage (E for stage totals). Entrant is the musher. Also in Demonstration tab.", "niche", "Generic – manual"],
    ["yukigassen", "Yukigassen", "", "A", "A", "Timed team matches with eliminations of players and a flag/goal objective; tournament brackets. Rule pack is specialised but the format is head-to-head.", "niche", "Generic"],
    ["snow-volleyball", "Snow volleyball", "", "A", "A", "Sets and matches, usually 3-a-side, pools to knockout — same shape as beach volleyball.", "niche", "Generic"],
    ["beach-handball", "Beach handball", "", "A", "A", "Sets (often two sets plus a shootout or 'golden goal' tiebreak — verify current IHF rules). Tournaments use pools and knockouts. Spin-shot and spectacular-goal scoring is", "niche", "Generic"],
    ["beach-tennis", "Beach tennis", "", "A", "A", "Doubles (and some singles) sets, world-tour events and brackets — same shape as tennis.", "niche", "Generic"],
    ["bodyboarding", "Bodyboarding", "", "D", "D", "Judged waves/heats to finals, like surfing. v1: manual heat scores or placings. No surf-scoring engine.", "niche", "Generic – manual"],
    ["wife-carrying", "Wife carrying", "", "B", "B", "Timed pairs over an obstacle course; a sprint uses heats to a final; a team relay also exists. Ranked by time.", "niche", "Generic"],
    ["kokpar", "Kokpar", "", "A", "A", "Head-to-head team games to place an animal carcass or analogue in a goal (kazan). Festival and championship formats. Enter match scores only; no sport pack in v1.", "niche", "Generic – manual"],
    ["chess-boxing", "Chess boxing", "", "A", "A", "Each bout is a sequence of chess stages (timed board, not a Regulars chess engine) and boxing stages (A). Winner/method is entered manually. A full sport pack is later wo", "niche", "Generic – manual"],
    ["esports", "Esports", "", "A", "AE", "Most titles are head-to-head matches or series (A), with groups and brackets, or cumulative ladders (E). Regulars would only store match winners/scores entered by the org", "niche", "Generic – manual"],
    ["speedcubing", "Speedcubing", "", "B", "B", "Best-of or average-of times (B) in rounds that advance to finals. Multiple official events at one competition (a programme of events, like a swim meet). Manual or CSV tim", "niche", "Generic"],
]
SPORTS = {row[0]: row for row in CATALOG}
FIRST = ("water-polo", "swimming", "diving", "open-water-swimming", "volleyball", "pickleball", "soccer", "basketball", "road-running", "ultimate-frisbee")

STATUS = {"draft": ("Draft", "Not on the public page yet"), "interest": ("Gauging interest", "Share link is open"),
          "published": ("Published", "Registration is set")}
STEPS = (("basics", "Basics"), ("sports", "Sports"), ("interest", "Interest"), ("registration", "Registration"), ("review", "Review"))


def ensure(d):
    d.execute("""CREATE TABLE IF NOT EXISTS tournaments(id INTEGER PRIMARY KEY, name TEXT NOT NULL, summary TEXT,
        starts TEXT, ends TEXT, tz TEXT, hosting TEXT, host_org TEXT, cohosts TEXT, venue TEXT, city TEXT,
        status TEXT NOT NULL DEFAULT 'draft', token TEXT, created_by INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        base_cents INTEGER, opens TEXT, closes TEXT, channels TEXT, early_cents INTEGER, early_until TEXT,
        late_cents INTEGER, late_from TEXT, interest_note TEXT, interest_until TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS tournament_sports(id INTEGER PRIMARY KEY, tournament_id INTEGER NOT NULL,
        sport_key TEXT NOT NULL, preset TEXT NOT NULL, sort INTEGER DEFAULT 0, UNIQUE(tournament_id, sport_key))""")
    d.execute("""CREATE TABLE IF NOT EXISTS tournament_interest(id INTEGER PRIMARY KEY, tournament_id INTEGER NOT NULL,
        kind TEXT NOT NULL, name TEXT NOT NULL, team TEXT, email TEXT, players INTEGER, sports TEXT, note TEXT,
        member_id INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")


def sport(key):
    row = SPORTS.get(key)
    if not row: return None
    return {"key": row[0], "name": row[1], "sub": row[2], "default": row[3] or "A", "allowed": list(row[4] or row[3] or "A"),
            "stages": row[5], "category": row[6], "tier": row[7]}


def search(q, limit=12):
    q = re.sub(r"[^a-z0-9 ]+", " ", (q or "").lower()).strip()
    if not q:
        return [sport(k) for k in FIRST if k in SPORTS]
    words = q.split()
    def score(row):
        hay = re.sub(r"[^a-z0-9 ]+", " ", (row[1] + " " + row[2]).lower())
        if hay.startswith(q): return 0
        if all(w in hay for w in words): return 1
        return None
    hits = sorted((score(r), i, r[0]) for i, r in enumerate(CATALOG) if score(r) is not None)
    return [sport(k) for _s, _i, k in hits[:limit]]


def get(d, tid):
    return d.execute("SELECT * FROM tournaments WHERE id=?", (tid,)).fetchone()


def by_token(d, token):
    if not token: return None
    return d.execute("SELECT * FROM tournaments WHERE token=?", (token,)).fetchone()


def mine(d, member_id, is_admin=False):
    if is_admin:
        return d.execute("SELECT * FROM tournaments ORDER BY COALESCE(starts,'') DESC, id DESC").fetchall()
    return d.execute("SELECT * FROM tournaments WHERE created_by=? ORDER BY COALESCE(starts,'') DESC, id DESC", (member_id,)).fetchall()


def sports_of(d, tid):
    out = []
    for r in d.execute("SELECT * FROM tournament_sports WHERE tournament_id=? ORDER BY sort, id", (tid,)):
        s = sport(r["sport_key"])
        if s:
            s["preset"] = r["preset"] if r["preset"] in PRESETS else s["default"]
            out.append(s)
    return out


def _date(raw):
    raw = (raw or "").strip()[:10]
    try:
        return dt.date.fromisoformat(raw).isoformat() if raw else ""
    except ValueError:
        raise ValueError("Use a real date.")


def _cents(raw):
    raw = (raw or "").replace("$", "").replace(",", "").strip()
    if not raw: return None
    try:
        v = round(float(raw) * 100)
    except ValueError:
        raise ValueError("Fees are dollar amounts, like 220.")
    if v < 0: raise ValueError("Fees can't go below zero.")
    return int(v)


def save_basics(d, tid, form, member_id):
    name = (form.get("name") or "").strip()[:120]
    if not name: raise ValueError("Give the tournament a name.")
    starts, ends = _date(form.get("starts")), _date(form.get("ends"))
    if not starts: raise ValueError("Add a start date.")
    if not ends: ends = starts
    if ends < starts: raise ValueError("The end date is before the start date.")
    hosting = form.get("hosting") if form.get("hosting") in ("individual", "organization", "several") else "individual"
    host_org = (form.get("host_org") or "").strip()[:120] if hosting != "individual" else ""
    if hosting != "individual" and not host_org: raise ValueError("Name the host organization.")
    vals = (name, (form.get("summary") or "").strip()[:240], starts, ends, (form.get("tz") or "America/Los_Angeles").strip()[:60], hosting,
            host_org, (form.get("cohosts") or "").strip()[:200] if hosting == "several" else "",
            (form.get("venue") or "").strip()[:120], (form.get("city") or "").strip()[:80])
    if tid:
        d.execute("""UPDATE tournaments SET name=?, summary=?, starts=?, ends=?, tz=?, hosting=?, host_org=?, cohosts=?, venue=?, city=?
            WHERE id=?""", vals + (tid,))
        return tid
    cur = d.execute("""INSERT INTO tournaments(name, summary, starts, ends, tz, hosting, host_org, cohosts, venue, city, status, token, created_by)
        VALUES(?,?,?,?,?,?,?,?,?,?,'draft',?,?)""", vals + (secrets.token_urlsafe(9), member_id))
    return cur.lastrowid


def save_sports(d, tid, keys, presets):
    keys = [k for k in dict.fromkeys(keys) if k in SPORTS]
    if not keys: raise ValueError("Pick at least one sport.")
    have = {r["sport_key"] for r in d.execute("SELECT sport_key FROM tournament_sports WHERE tournament_id=?", (tid,))}
    for i, k in enumerate(keys):
        s = sport(k)
        p = presets.get(k) if presets.get(k) in s["allowed"] else s["default"]
        if k in have:
            d.execute("UPDATE tournament_sports SET preset=?, sort=? WHERE tournament_id=? AND sport_key=?", (p, i, tid, k))
        else:
            d.execute("INSERT INTO tournament_sports(tournament_id, sport_key, preset, sort) VALUES(?,?,?,?)", (tid, k, p, i))
    for k in have - set(keys):
        # The organizer took this sport off the setup. Interest answers that named it keep their own text.
        d.execute("DELETE FROM tournament_sports WHERE tournament_id=? AND sport_key=?", (tid, k))


def save_registration(d, tid, form):
    base = _cents(form.get("base"))
    if base is None: raise ValueError("Set the base fee (0 is fine).")
    opens, closes = _date(form.get("opens")), _date(form.get("closes"))
    if opens and closes and closes < opens: raise ValueError("Registration closes before it opens.")
    early, late = _cents(form.get("early")), _cents(form.get("late"))
    early_until, late_from = _date(form.get("early_until")), _date(form.get("late_from"))
    if early is not None and not early_until: raise ValueError("Add the date early-bird pricing ends.")
    if late is not None and not late_from: raise ValueError("Add the date late pricing starts.")
    chans = [c for c in form.getlist("channels") if c in ("app", "link", "organizer")] or ["app"]
    d.execute("""UPDATE tournaments SET base_cents=?, opens=?, closes=?, channels=?, early_cents=?, early_until=?, late_cents=?, late_from=?
        WHERE id=?""", (base, opens, closes, ",".join(chans), early, early_until if early is not None else "",
                         late, late_from if late is not None else "", tid))


def set_status(d, tid, status):
    if status in STATUS:
        d.execute("UPDATE tournaments SET status=? WHERE id=?", (status, tid))


def add_interest(d, t, form, member_id=None):
    kind = form.get("kind") if form.get("kind") in ("team", "athlete") else "athlete"
    name = (form.get("name") or "").strip()[:80]
    if not name: raise ValueError("Add your name.")
    email = (form.get("email") or "").strip()[:120]
    if not member_id and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email): raise ValueError("Add an email so the host can reach you.")
    team = (form.get("team") or "").strip()[:80]
    if kind == "team" and not team: raise ValueError("Add the team or club name.")
    try:
        players = max(1, min(200, int(form.get("players") or 1)))
    except ValueError:
        players = 1
    if kind == "athlete": players = 1
    allowed = {s["key"] for s in sports_of(d, t["id"])}
    picked = [k for k in form.getlist("sports") if k in allowed]
    d.execute("""INSERT INTO tournament_interest(tournament_id, kind, name, team, email, players, sports, note, member_id)
        VALUES(?,?,?,?,?,?,?,?,?)""", (t["id"], kind, name, team, email, players, ",".join(picked), (form.get("note") or "").strip()[:280], member_id))


def interest_summary(d, tid):
    rows = d.execute("SELECT * FROM tournament_interest WHERE tournament_id=? ORDER BY id DESC", (tid,)).fetchall()
    per = {}
    for r in rows:
        for k in (r["sports"] or "").split(","):
            if k: per[k] = per.get(k, 0) + (r["players"] or 1)
    return {"rows": rows, "teams": sum(1 for r in rows if r["kind"] == "team"), "athletes": sum(r["players"] or 1 for r in rows),
            "responses": len(rows), "per_sport": per}


def money(cents):
    if cents is None: return ""
    return ("$%d" % (cents // 100)) if cents % 100 == 0 else ("$%.2f" % (cents / 100))


def fee_today(t, today):
    """The fee someone registering today pays: early bird, then regular, then late. Never below zero."""
    if t["base_cents"] is None: return None
    if t["early_cents"] is not None and t["early_until"] and today <= t["early_until"]: return max(0, t["early_cents"])
    if t["late_cents"] is not None and t["late_from"] and today >= t["late_from"]: return max(0, t["late_cents"])
    return max(0, t["base_cents"])


def short(iso):
    try:
        x = dt.date.fromisoformat(iso)
        return "%s %d, %d" % (x.strftime("%b"), x.day, x.year)
    except (TypeError, ValueError):
        return ""


def window(a, b):
    if a and b: return "%s – %s" % (short(a).rsplit(",", 1)[0], short(b).rsplit(",", 1)[0])
    return short(a or b) or "Dates not set"


def date_line(t):
    try:
        a, b = dt.date.fromisoformat(t["starts"]), dt.date.fromisoformat(t["ends"] or t["starts"])
    except (TypeError, ValueError):
        return ""
    if a == b: return "%s %d, %d" % (a.strftime("%b"), a.day, a.year)
    if a.year == b.year and a.month == b.month: return "%s %d–%d, %d" % (a.strftime("%b"), a.day, b.day, a.year)
    return "%s %d – %s %d, %d" % (a.strftime("%b"), a.day, b.strftime("%b"), b.day, b.year)


def meta_line(t):
    bits = [date_line(t)]
    if t["venue"] or t["city"]: bits.append(", ".join(x for x in (t["venue"], t["city"]) if x))
    if t["hosting"] == "individual" or not t["host_org"]: bits.append("Hosted by you")
    else: bits.append(("co-host " + t["cohosts"]) if t["cohosts"] else "Hosted by " + t["host_org"])
    return " · ".join(b for b in bits if b)


def checklist(d, t):
    sp = sports_of(d, t["id"])
    iv = interest_summary(d, t["id"])
    reg = ("%s · %s" % (money(t["base_cents"]), window(t["opens"], t["closes"]))) if t["base_cents"] is not None else "Set the base fee"
    return [
        ("basics", "Basics", "Name, dates, hosts", bool(t["name"] and t["starts"])),
        ("sports", "Sports", ", ".join(s["name"] for s in sp) or "Pick at least one sport", bool(sp)),
        ("interest", "Interest", ("%d responses · %d athletes" % (iv["responses"], iv["athletes"])) if iv["responses"]
            else ("Share link is open" if t["status"] == "interest" else "Optional · share a link first"), True),
        ("registration", "Registration", reg, t["base_cents"] is not None),
    ]
