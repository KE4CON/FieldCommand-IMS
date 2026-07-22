"""
NIMS Resource Type Full Definitions
Keyed by nims_id — provides plain-language explanation of what each resource IS,
what it does, minimum standards, and ordering guidance.
Source: FEMA NIMS Resource Typing Library, NWCG Incident Response Pocket Guide,
IFSTA manuals, and operational ICS doctrine.
"""

NIMS_DEFINITIONS = {

# ── ENGINES ──────────────────────────────────────────────────────────────────
'1-508-1001': {
    'what_it_is': (
        "A Type I engine is a full-size structural fire suppression apparatus — what most "
        "people think of as a 'fire truck.' It is built on a heavy commercial chassis and "
        "carries a large pump, substantial water tank, and a full complement of hose, tools, "
        "and self-contained breathing apparatus (SCBA). Type I engines are staffed with a "
        "minimum of 4 personnel and are the primary resource for attacking structure fires, "
        "commercial fires, and large-volume water delivery."
    ),
    'minimum_standards': (
        "1,000 GPM or greater pump capacity. 400-gallon minimum water tank. "
        "1,200 feet of 2.5-inch hose. 400 feet of 1.5-inch hose. "
        "Minimum 4 personnel (officer, engineer/driver, 2 firefighters). "
        "Full SCBA complement. Ground ladders. Basic rescue tools."
    ),
    'ordering_guidance': (
        "Order Type I when you need maximum water flow for structure fires, "
        "exposure protection on large incidents, or sustained offensive attack capability. "
        "If road access is limited or the terrain is rough, consider Type III or IV instead. "
        "Type I is NOT suitable for off-road wildland fire work."
    ),
    'common_confusion': (
        "Confusion: People sometimes call any fire truck a 'Type I.' "
        "The type designation is about PUMP CAPACITY and TANK SIZE, not the truck's age or size. "
        "A newer smaller truck may be Type II or III while an older large truck is Type I."
    ),
},

'1-508-1002': {
    'what_it_is': (
        "A Type II engine is similar to a Type I but with a smaller pump (500 GPM) "
        "and slightly reduced hose load. Common in suburban and smaller municipal departments. "
        "Requires minimum 3 personnel. Fully capable of structural fire attack but with "
        "less sustained flow than Type I."
    ),
    'minimum_standards': (
        "500 GPM or greater pump. 400-gallon minimum tank. "
        "1,000 feet of 2.5-inch hose. 3 personnel minimum."
    ),
    'ordering_guidance': (
        "Good general-purpose structural engine when Type I supply is exhausted or unavailable. "
        "Suitable for most structure fire assignments, water supply, and exposure protection."
    ),
    'common_confusion': (
        "Often indistinguishable from Type I visually. The difference is pump capacity. "
        "Many mutual aid engines from smaller departments will be Type II."
    ),
},

'1-508-1003': {
    'what_it_is': (
        "A Type III engine is specifically designed for wildland-urban interface (WUI) and "
        "light structural fire work. It is built on a 4-wheel-drive chassis capable of "
        "operating on unpaved roads, fire roads, and rough terrain. The pump is smaller "
        "(120 GPM minimum) but the engine can go where Type I and II cannot. "
        "Standard crew is 3 personnel. This is the most versatile engine for "
        "interface fires where you need both off-road mobility and some structure protection capability."
    ),
    'minimum_standards': (
        "120 GPM pump. 500-gallon minimum tank. 4WD/AWD. "
        "Ground clearance for unpaved roads. 3 personnel. "
        "Can pump and roll (attack while moving)."
    ),
    'ordering_guidance': (
        "Order Type III when your fire is in or near the interface, when access roads are "
        "unpaved or steep, or when you need engines that can follow dozers and hand crews "
        "into rough terrain. NOT suitable for large-volume structure fire attack."
    ),
    'common_confusion': (
        "People often confuse Type III with Type VI (patrol). Type III is a real engine "
        "with a substantial tank and crew. Type VI is a much smaller patrol unit. "
        "Type III can do structure work in a pinch; Type VI cannot."
    ),
},

'1-508-1004': {
    'what_it_is': (
        "A Type IV engine is a wildland initial attack engine — smaller than Type III, "
        "optimized for rapid deployment on initial attack fires. It has a 50 GPM pump, "
        "750-gallon tank, and full off-road capability. Typically staffed with 3 personnel. "
        "The large tank relative to its pump makes it good for sustained water application "
        "on grass and brush fires."
    ),
    'minimum_standards': "50 GPM pump. 750-gallon tank. Off-road capable. 3 personnel.",
    'ordering_guidance': (
        "Order for wildland initial attack, mop-up, and patrol on grass and brush fires. "
        "Not appropriate for structure protection or large-volume flow needs."
    ),
    'common_confusion': "Often confused with Type V. Type IV has a LARGER tank (750 gal vs 400 gal) than Type V.",
},

'1-508-1005': {
    'what_it_is': (
        "A Type V engine is a wildland initial attack engine with a 50 GPM pump and "
        "400-gallon tank. Slightly smaller than Type IV. Commonly used for initial attack "
        "on grass, brush, and timber fires. 2-3 person crew."
    ),
    'minimum_standards': "50 GPM pump. 400-gallon tank. Off-road capable. 2-3 personnel.",
    'ordering_guidance': "Initial attack on grass and brush. Mop-up support. Patrol.",
    'common_confusion': "Type V has a smaller tank than Type IV (400 vs 750 gallons), but same pump size.",
},

'1-508-1006': {
    'what_it_is': (
        "A Type VI engine (patrol engine) is a light wildland patrol unit. Small truck "
        "or SUV-based with a small pump (30 GPM) and only 150 gallons of water. "
        "Used for patrol, spot fire detection and initial knockdown, mop-up, and scouting. "
        "2-person crew. Cannot sustain a serious fire attack."
    ),
    'minimum_standards': "30 GPM pump. 150-gallon tank. Off-road. 2 personnel.",
    'ordering_guidance': (
        "Order for patrol and reconnaissance, spot fire knockdown, and mop-up. "
        "NOT for primary attack on going fires. Often used to follow hand crews."
    ),
    'common_confusion': (
        "People sometimes order Type VI thinking they're getting a real engine. "
        "Type VI is a PATROL unit. 150 gallons runs out in 5 minutes at full flow. "
        "If you need fire attack, order Type III-V."
    ),
},

'1-508-1007': {
    'what_it_is': (
        "A Type VII engine is the smallest engine type — essentially a pickup truck "
        "with a small slip-on pump unit and 50-gallon tank. Used for initial attack "
        "on very small fires, mop-up, and patrol. 1-2 person crew. "
        "Common in rural volunteer departments and federal land management."
    ),
    'minimum_standards': "10 GPM pump. 50-gallon tank. 1-2 personnel.",
    'ordering_guidance': "Mop-up, patrol, small spot fire knockdown only.",
    'common_confusion': "Not suitable for any sustained fire attack. This is a 50-gallon tank on a pickup truck.",
},

# ── HAND CREWS ───────────────────────────────────────────────────────────────
'1-508-1010': {
    'what_it_is': (
        "An Interagency Hotshot Crew (IHC) — the elite of wildland firefighting. "
        "A fully self-contained crew of 20 specially trained and physically fit firefighters "
        "led by a Superintendent with extensive experience. Hotshot crews are certified "
        "through a rigorous annual review process and can be deployed anywhere in the country. "
        "They are trained and equipped to work the most difficult terrain and fire conditions, "
        "and are self-sufficient for 2 weeks without resupply. Every crew member holds "
        "multiple qualifications. They carry their own equipment, tools, shelter, and rations."
    ),
    'minimum_standards': (
        "20 personnel minimum. IHC certification (annual review required). "
        "Superintendent qualified as Operations Section Chief. "
        "All members meet arduous fitness standard (Work Capacity Test). "
        "Self-sufficient 14 days. Chainsaw operators. Medical first responder capability. "
        "Can work night operations."
    ),
    'ordering_guidance': (
        "Order Type I when you need the best available crew for the most difficult and "
        "dangerous assignments — critical line construction in rough terrain, direct attack "
        "in extreme conditions, complex burnout operations. They are in high demand and "
        "may have longer lead times. Request through NICC or your geographic coordination center."
    ),
    'common_confusion': (
        "All hotshot crews are Type I hand crews, but NOT all Type I hand crews are hotshots. "
        "A crew can achieve Type I status through training and experience without IHC certification. "
        "IHC crews wear green hard hats with their crew name; other crews do not. "
        "If you specifically need a hotshot crew, specify 'IHC' in your resource order."
    ),
},

'1-508-1011': {
    'what_it_is': (
        "A Type II hand crew is an experienced 20-person wildland fire crew capable of "
        "sustained fireline construction, burnout operations, and mop-up. They have "
        "chainsaw operators and are deployable for 2-week assignments. Less elite than "
        "hotshots but capable of most wildland fire assignments. Crews may come from "
        "federal agencies, state forestry, tribal governments, or contractors."
    ),
    'minimum_standards': (
        "20 personnel. Crew boss qualified at Crew Boss (CRWB) or higher. "
        "Chainsaw operators certified. Arduous fitness for all members. "
        "Self-sufficient 14 days. Night operations capable."
    ),
    'ordering_guidance': (
        "The workhorse of large fire operations. Order when you need sustained "
        "fireline production and hotshots are unavailable. Good for indirect attack, "
        "mop-up, holding line, and secondary assignments."
    ),
    'common_confusion': (
        "Type II crews vary widely in experience and capability. Some are nearly as capable "
        "as hotshots; others are newer crews still building experience. "
        "A 'Type II IA' (Initial Attack) crew has only 10 people — see separate definition."
    ),
},

'1-508-1012': {
    'what_it_is': (
        "A Type II Initial Attack (IA) crew is a 10-person initial attack hand crew — "
        "half the size of a standard Type II. Designed for rapid mobilization on initial "
        "attack fires where a full 20-person crew would be excessive or unavailable. "
        "Same individual qualification standards as Type II but smaller team. "
        "Cannot sustain as long as a full crew but mobilizes faster."
    ),
    'minimum_standards': "10 personnel. Crew boss qualified. Arduous fitness. Chainsaw operator.",
    'ordering_guidance': (
        "Order when you need faster initial attack response with a smaller footprint, "
        "or when you need to fill a specific tactical need without committing a full 20-person crew."
    ),
    'common_confusion': (
        "'Type II-IA' is NOT a lesser Type II — it is a deliberately smaller crew. "
        "Do not order Type II-IA expecting 20 people."
    ),
},

# ── WATER TENDERS ────────────────────────────────────────────────────────────
'1-508-1020': {
    'what_it_is': (
        "A Type I tactical water tender is a large mobile water supply unit designed "
        "for off-road wildland fire operations. It carries a minimum of 4,000 gallons "
        "of water, has a 250 GPM pump, and is built on a heavy-duty chassis with "
        "off-road capability. The term 'tactical' means it can actively fight fire, "
        "not just deliver water to other apparatus. It can pump and roll, draft from "
        "static sources (ponds, streams), and serve as a mobile water supply point "
        "for engines in areas without hydrants."
    ),
    'minimum_standards': (
        "4,000-gallon minimum capacity. 250 GPM pump. Off-road capable (4WD or tandem drive). "
        "Capable of drafting from static sources. 3 personnel. "
        "Can fill other apparatus while maintaining forward progress."
    ),
    'ordering_guidance': (
        "Order when working in areas with no water supply infrastructure — "
        "wildland fires, rural interface fires, remote locations. "
        "One Type I tender can supply 4-6 engines depending on flow demands."
    ),
    'common_confusion': (
        "People confuse tactical tenders (which can fight fire) with support tenders "
        "(which just haul water). All three types here are tactical. "
        "A milk truck or tanker truck is NOT a NIMS water tender unless it meets the specifications."
    ),
},

'1-508-1021': {
    'what_it_is': (
        "A Type II tactical water tender carries 2,500+ gallons and has a 200 GPM pump. "
        "Similar capability to Type I but smaller capacity. Common in rural fire departments "
        "and state forestry. Off-road capable and can draft from static sources."
    ),
    'minimum_standards': "2,500-gallon minimum. 200 GPM pump. Off-road capable. 2-3 personnel.",
    'ordering_guidance': "Same uses as Type I when Type I is unavailable. Good for smaller operations.",
    'common_confusion': "The 200 GPM pump of a Type II tender feeds engines slower than a Type I (250 GPM).",
},

'1-508-1022': {
    'what_it_is': (
        "A Type III support water tender is the smallest tender type — 1,500+ gallons "
        "and highway-capable but NOT required to be off-road capable. "
        "It can deliver water to engines at a staging area but may not be able to "
        "follow engines off-road. More of a water delivery vehicle than a tactical unit."
    ),
    'minimum_standards': "1,500-gallon minimum. 200 GPM pump. Highway capable. 2 personnel.",
    'ordering_guidance': (
        "Use for water shuttle operations between a static source and a staging/fill point. "
        "Do not send off-road without confirming it can handle the terrain."
    ),
    'common_confusion': (
        "Type III tenders may look identical to Type II but lack off-road capability. "
        "Always confirm terrain capability before assigning."
    ),
},

# ── BULLDOZERS ───────────────────────────────────────────────────────────────
'1-508-1030': {
    'what_it_is': (
        "A Type I (heavy) bulldozer is the largest class of tracked dozer used on fires — "
        "Caterpillar D8, D9, or equivalent. Weighing 80,000+ pounds with 200+ horsepower, "
        "these machines can push through heavy timber, cut through rocky terrain, and "
        "build fireline at rates of 0.5-2+ acres per hour depending on fuel type. "
        "Operated by 1 highly skilled dozer operator. Transported on a heavy lowboy trailer. "
        "Used for initial attack on fast-moving fires, containment line construction, "
        "and dozer line in heavy fuel types."
    ),
    'minimum_standards': (
        "200+ HP. D8/D9 class Caterpillar or equivalent. ROPS (rollover protection). "
        "Brush guard. Blade capable of full cut in heavy fuels. 1 qualified operator (DOQY)."
    ),
    'ordering_guidance': (
        "Order Type I for heavy timber, rocky terrain, steep slopes where smaller dozers "
        "cannot work effectively. They move slower and cost more but can work conditions "
        "that would stop a Type II or III. Require a lowboy and heavy transport."
    ),
    'common_confusion': (
        "Bigger is not always better. Type I dozers cause more environmental damage, "
        "take longer to transport, and cannot access narrow roads or tight terrain. "
        "Many dozer bosses prefer Type II for most wildland assignments. "
        "Know your terrain before ordering."
    ),
},

'1-508-1031': {
    'what_it_is': (
        "A Type II (medium) bulldozer — Caterpillar D6, D7, or equivalent. "
        "100-200 HP. The most commonly ordered dozer on wildland fires. "
        "More maneuverable than Type I, faster to transport, and capable of "
        "working most terrain types. Can be transported on a standard lowboy. "
        "Effective in medium-to-heavy fuels."
    ),
    'minimum_standards': "100-200 HP. D6/D7 class or equivalent. ROPS. 1 qualified operator.",
    'ordering_guidance': (
        "Default dozer order for most wildland fire situations. "
        "More versatile than Type I and faster to mobilize."
    ),
    'common_confusion': "D6 vs D7 are both Type II — they vary in HP within the type band.",
},

'1-508-1032': {
    'what_it_is': (
        "A Type III (light) bulldozer — Caterpillar D4, D5, or equivalent. "
        "50-100 HP. Small, fast, and easy to transport — can go on roads where "
        "larger dozers cannot. Effective in grass, light brush, and light timber. "
        "Often used for mop-up, line improvement, and access road construction."
    ),
    'minimum_standards': "50-100 HP. D4/D5 class or equivalent. ROPS. 1 qualified operator.",
    'ordering_guidance': (
        "Order Type III when terrain requires a smaller footprint, roads cannot support "
        "larger equipment, or fuels are light enough that extra power isn't needed. "
        "Good for mop-up and cleanup work."
    ),
    'common_confusion': "Small dozers are not necessarily faster or cheaper — they just fit different terrain.",
},

# ── HELICOPTERS ──────────────────────────────────────────────────────────────
'1-508-1040': {
    'what_it_is': (
        "A Type I heavy fire helicopter is a large aircraft capable of carrying 700+ gallons "
        "of water in a fixed tank or bucket, with 5,000+ pounds of payload capacity. "
        "Examples include the Sikorsky S-64 Skycrane (Aircrane), "
        "the Kaman K-MAX, and large military surplus helicopters. "
        "These aircraft can make multiple drops on a fire with short turnaround times "
        "if a water source is nearby. They can also transport crews, sling-load cargo, "
        "and support long-line operations. Requires 3+ crew (pilot, copilot, and often "
        "a helitack crew member or helicopter manager)."
    ),
    'minimum_standards': (
        "700+ gallon retardant/water capacity (fixed tank or bucket). "
        "5,000+ pound payload. Minimum 700 HP. "
        "5+ passenger capacity. IFR capable preferred. "
        "Certified NIMS helicopter manager."
    ),
    'ordering_guidance': (
        "Order Type I for large fires requiring high water/retardant volume, "
        "remote locations needing heavy sling-load capability, or when multiple "
        "smaller helicopters would be less effective. High daily cost — justify with volume needs."
    ),
    'common_confusion': (
        "The Skycrane (S-64) is the most recognized Type I but it is NOT the only one. "
        "The type is defined by capacity, not aircraft model. "
        "Do not confuse with air ambulance or law enforcement helicopters — "
        "those are NOT fire helicopters and lack fire operations certification."
    ),
},

'1-508-1041': {
    'what_it_is': (
        "A Type II medium fire helicopter carries 300+ gallons in a fixed tank or bucket "
        "with 2,500+ pound payload. Typical aircraft include the Sikorsky S-61, "
        "Bell 212, UH-1H (Huey), and similar medium-twin helicopters. "
        "Capable of crew transport (9+ seats), aerial reconnaissance, short-haul rescue, "
        "and water/retardant drops. The most versatile fire helicopter type. "
        "Common on large complex fires as the primary utility aircraft."
    ),
    'minimum_standards': (
        "300+ gallon tank/bucket. 2,500+ lb payload. 9+ passenger capacity. "
        "IFR capable. Certified helicopter manager."
    ),
    'ordering_guidance': (
        "The default helicopter order for most complex fires. "
        "Good balance of capacity, speed, and versatility. "
        "Can do crew transport, aerial supervision, cargo, and water drops."
    ),
    'common_confusion': (
        "The Huey (UH-1H) is the most commonly confused. In good condition with "
        "a certified operator it qualifies as Type II. A worn-out or improperly "
        "equipped Huey may not meet minimums. Verify certification."
    ),
},

'1-508-1042': {
    'what_it_is': (
        "A Type III light fire helicopter carries 100+ gallons in a bucket "
        "with 1,200+ pound payload. Examples include the Bell 206 JetRanger, "
        "Hughes 500, and similar light single-engine helicopters. "
        "Primary uses are aerial reconnaissance, initial attack on small fires, "
        "personnel transport (3-4 people), and observation. "
        "Cannot carry significant water/retardant volume."
    ),
    'minimum_standards': "100+ gallon bucket. 1,200+ lb payload. IFR not required. Certified helicopter manager.",
    'ordering_guidance': (
        "Order for reconnaissance, aerial supervision, initial attack spotting, "
        "and short personnel hauls. NOT appropriate when volume water drops are needed."
    ),
    'common_confusion': (
        "People sometimes order Type III expecting it to make meaningful water drops. "
        "100 gallons on a going fire makes very little difference. "
        "Type III helicopters are primarily reconnaissance and transport assets."
    ),
},

# ── HAZMAT ───────────────────────────────────────────────────────────────────
'1-508-1060': {
    'what_it_is': (
        "A Type I HazMat Response Team is the highest level of hazardous materials response — "
        "capable of fully offensive operations including Level A (vapor-protective suit) entry "
        "into the hot zone, identification and sampling of unknown substances, "
        "emergency containment and mitigation, decontamination operations, and "
        "victim rescue from contaminated areas. "
        "Minimum 10 personnel with multiple specialties. "
        "Teams typically carry specialized detection equipment, chemical reference databases, "
        "entry suits, decon equipment, and reference libraries. "
        "Examples: FEMA USAR task force HazMat component, regional HazMat teams."
    ),
    'minimum_standards': (
        "10+ personnel. Level A entry capability. Multiple chemical detection instruments "
        "(photoionization detector, multi-gas meter, radiation detector, pH paper, etc.). "
        "Full decontamination capability. Reference resources. "
        "At minimum one Hazardous Materials Technician (HAZTECH) per entry team pair. "
        "Self-sufficient 12+ hours."
    ),
    'ordering_guidance': (
        "Order Type I when you have an unknown substance with significant life safety risk, "
        "a confirmed dangerous gas or liquid release requiring entry to mitigate, "
        "or a mass decontamination situation. "
        "These teams are expensive and may have long mobilization times."
    ),
    'common_confusion': (
        "Not all fire departments with HazMat placards on their apparatus are Type I teams. "
        "Many departments have HazMat awareness or operations level training but "
        "NO entry capability. A true Type I team must have Level A suits and "
        "trained technicians. Always confirm actual capability when ordering."
    ),
},

'1-508-1061': {
    'what_it_is': (
        "A Type II HazMat Response Team operates at the defensive/operations level — "
        "capable of Level B (splash-protective suit) entry, monitoring perimeter, "
        "plugging and patching small leaks, and diverting spills from storm drains. "
        "They do NOT enter the hot zone for offensive mitigation. "
        "Minimum 6 personnel. Common in municipal fire departments with operations-level training."
    ),
    'minimum_standards': (
        "6+ personnel. Level B entry. Detection instruments. "
        "Operations-level certification. Defensive mitigation capability."
    ),
    'ordering_guidance': (
        "Order for fuel spills, small chemical releases where offensive entry is not required, "
        "and situations where your goal is containment and perimeter control "
        "rather than aggressive mitigation."
    ),
    'common_confusion': "Type II can NOT do offensive hot zone entry — that requires Type I.",
},

# ── SAR ──────────────────────────────────────────────────────────────────────
'8-508-1001': {
    'what_it_is': (
        "A Type I ground search and rescue team is a highly trained, fully equipped "
        "team capable of operating in all terrain types, at night, in adverse weather, "
        "and for extended periods without resupply. Minimum 6 personnel who collectively "
        "possess technical rope rescue, swiftwater, wilderness medicine, navigation, "
        "and survival skills. They can treat and package injured patients for extraction "
        "in technical terrain. Self-sufficient for 72 hours. "
        "May include a K9 component. "
        "Examples: Mountain rescue teams, NASAR-certified teams, county SAR teams with technical training."
    ),
    'minimum_standards': (
        "6+ personnel. Night operations. Technical rescue capable. "
        "Wilderness First Responder (WFR) or equivalent. "
        "Navigation (map/compass/GPS). 72-hour self-sufficient. "
        "NASAR or equivalent training."
    ),
    'ordering_guidance': (
        "Order for missing persons in wilderness or technical terrain, "
        "technical rope rescues, cliff rescues, and any situation where "
        "the terrain makes access difficult and victims may require field medical care."
    ),
    'common_confusion': (
        "Not all volunteer SAR teams are Type I. Many county SAR teams have "
        "excellent training but limited technical capability. "
        "Always ask about the specific team's actual skill set. "
        "'SAR team' means very different things in different counties."
    ),
},

'8-508-1020': {
    'what_it_is': (
        "A FEMA Urban Search and Rescue (US&R) Heavy Task Force — the highest level "
        "of structural collapse search and rescue. 80 personnel organized into "
        "four functional elements: search, rescue, medical, and technical. "
        "Capable of locating victims in collapsed structures using acoustic/optical "
        "search equipment and trained search dogs, then physically removing them "
        "through technical breaching, cutting, and shoring operations. "
        "Fully self-sufficient for 72+ hours. "
        "FEMA has 28 national US&R task forces pre-positioned across the country."
    ),
    'minimum_standards': (
        "80 personnel. Two 4-person rescue squads, two medical teams, "
        "two K9 search teams, technical, logistics, and command components. "
        "Victim location technology. Heavy rescue tools. "
        "Structural assessment capability. 72-hour self-sufficient. "
        "FEMA certification required for national deployment."
    ),
    'ordering_guidance': (
        "Request through your state Emergency Management for earthquake, tornado, "
        "building explosion, or any structural collapse with multiple trapped victims. "
        "These teams require hours to mobilize from their home bases. "
        "Request early — do not wait until you have confirmed entrapment."
    ),
    'common_confusion': (
        "A fire department's 'technical rescue team' is NOT a US&R Type I task force "
        "unless FEMA-certified. Many departments have basic collapse rescue capability "
        "but lack the personnel, equipment, and self-sufficiency of a true task force. "
        "Type II (35 personnel) and Type III (8 personnel) exist for smaller incidents."
    ),
},

# ── EMS ──────────────────────────────────────────────────────────────────────
'3-508-1001': {
    'what_it_is': (
        "A Type I ALS ambulance is the standard Advanced Life Support ground ambulance "
        "built on a truck (Class C) chassis with a modular patient compartment. "
        "Equipped to provide ALS care including cardiac monitoring, IV therapy, "
        "advanced airway management, cardiac defibrillation, and drug therapy. "
        "Staffed with a minimum of a paramedic and EMT. "
        "The modular body gives more patient compartment space than a van-based unit. "
        "Common in urban and suburban EMS systems."
    ),
    'minimum_standards': (
        "Type I chassis (truck-based). ALS equipment. "
        "Cardiac monitor/defibrillator. IV supplies. Advanced airway equipment. "
        "Drug box per state protocols. 2 personnel (at least 1 paramedic)."
    ),
    'ordering_guidance': (
        "Standard ALS transport unit. Order when you need advanced life support capability "
        "and transport. If you only need transport without ALS, Type IV (BLS) is less expensive."
    ),
    'common_confusion': (
        "Type I, II, and III ambulances all look similar and all can be ALS. "
        "The type designates the CHASSIS, not the level of care. "
        "A Type I is truck-based, Type II is van-type, Type III is modular on van chassis. "
        "Always confirm ALS vs BLS when ordering."
    ),
},

'3-508-1010': {
    'what_it_is': (
        "A Type I Mass Casualty Incident (MCI) unit is a large trailer or vehicle "
        "that carries supplies and equipment to treat and transport a large number "
        "of patients (100+) simultaneously. It does NOT provide ALS care on its own — "
        "it provides the SUPPLIES and ORGANIZATION structure for a large treatment area. "
        "Contents typically include triage tags, treatment tarps, IV supplies in bulk, "
        "bandages, splints, backboards, and litters for 100+ patients. "
        "Staffed by a team of 5+ who set up and manage the treatment area."
    ),
    'minimum_standards': (
        "100+ patient capacity supplies. Treatment area setup equipment. "
        "Triage system. Sector organization materials. 5+ trained personnel. "
        "Typically trailer-mounted."
    ),
    'ordering_guidance': (
        "Order for mass casualty events — multi-vehicle accidents, building collapses, "
        "large-scale violence, or any event with 10+ serious patients. "
        "Request early — MCI units need time to set up. "
        "An MCI unit does NOT replace ambulances; it organizes care until ambulances arrive."
    ),
    'common_confusion': (
        "An MCI unit does NOT transport patients. It is a supply cache and treatment area setup. "
        "You still need ambulances to transport patients to hospitals. "
        "Ordering an MCI unit is NOT a substitute for ordering more ambulances."
    ),
},

# ── IMTs ─────────────────────────────────────────────────────────────────────
'2-508-2001': {
    'what_it_is': (
        "A Type I Incident Management Team (IMT) is the highest level of all-hazards "
        "incident management capability. A standing, pre-organized team of 50+ "
        "credentialed ICS professionals who fill every position in the ICS organization "
        "from Incident Commander through all Section Chiefs, Branch Directors, Unit Leaders, "
        "and technical specialists. Nationally deployable. "
        "Team members are pre-qualified to national standards. "
        "The team is self-sufficient — they bring their own communications, logistics, "
        "planning resources, and documentation. They take over complete management "
        "of an incident and can operate continuously for 14+ days. "
        "Examples: FEMA IMTs, National Wildfire Coordinating Group (NWCG) Type I teams, "
        "and some state all-hazards Type I teams."
    ),
    'minimum_standards': (
        "50+ personnel. 100% fill of all ICS positions. "
        "IC qualified at Operations Section Chief or higher on previous incidents. "
        "Self-sufficient 14 days. Full documentation capability. "
        "Nationally deployable within 12-24 hours. "
        "Annual certification review."
    ),
    'ordering_guidance': (
        "Request Type I through your State Emergency Management or FEMA Region "
        "for incidents that exceed local and regional capability — "
        "large/complex disasters, long-duration events, multi-jurisdictional incidents. "
        "These teams require coordination through official channels. "
        "Allow 12-24 hours minimum lead time for national teams."
    ),
    'common_confusion': (
        "A Type I team is NOT just a group of experienced people. "
        "It is a CERTIFIED, STANDING TEAM with defined membership and annual qualification. "
        "Assembling local personnel and calling it a Type I team is incorrect and dangerous — "
        "those personnel may not be qualified to the national standard. "
        "Types III and IV (local teams) are assembled from local/regional personnel. "
        "Types I and II are standing certified teams."
    ),
},

'2-508-2003': {
    'what_it_is': (
        "A Type III IMT is a locally or regionally assembled team with the key ICS "
        "positions filled — typically Incident Commander, Operations Section Chief, "
        "Planning Section Chief, Logistics Section Chief, and Safety Officer at minimum. "
        "NOT a standing certified team — assembled from available qualified personnel "
        "in your county, region, or mutual aid area. "
        "Capable of managing multi-operational period incidents with complex logistics. "
        "This is what most county emergency management agencies are building toward."
    ),
    'minimum_standards': (
        "15+ personnel. Key ICS positions filled with credentialed individuals. "
        "IC qualified through local/state credentialing. "
        "Multi-operational period capability. Can expand to full ICS as needed."
    ),
    'ordering_guidance': (
        "Activate a Type III for incidents that exceed single-agency response but "
        "don't require a national team — complex multi-day events, large-scale "
        "local emergencies, and incidents requiring coordination across multiple agencies."
    ),
    'common_confusion': (
        "This is where MCESV/K9ESV operates. A Type III is YOUR level of incident management. "
        "Building a Type III team means identifying who fills each key ICS position "
        "in your county and training them to that standard. "
        "FieldCommand IMS is designed to support Type III and Type IV operations."
    ),
},

# ── MOBILE COMMAND ────────────────────────────────────────────────────────────
'2-508-2020': {
    'what_it_is': (
        "A Type I Mobile Command Post is a large trailer or vehicle configured as "
        "a fully functional Incident Command Post with 12+ workstations, "
        "integrated communications (satellite, VHF/UHF, cellular, internet), "
        "large-format video displays, conference capability, and a dedicated generator. "
        "It can serve as the ICP for a Type I or II incident. "
        "Examples include county/state EOC trailers, FEMA Mobile Emergency Response "
        "Support (MERS) vehicles, and large utility company command vehicles."
    ),
    'minimum_standards': (
        "12+ workstations. Satellite communications. VHF/UHF radio suite. "
        "Internet/LTE connectivity. Video display capability. "
        "Dedicated generator for 72+ hours. Climate controlled. "
        "Secure communications capability preferred."
    ),
    'ordering_guidance': (
        "Deploy for major incidents requiring a dedicated, self-contained ICP "
        "when no suitable fixed facility is available. "
        "Also used when the incident command must be mobile or rapidly relocatable."
    ),
    'common_confusion': (
        "Not every large vehicle with radios is a Type I command post. "
        "A pickup truck with a radio in it might be a Type III. "
        "The defining characteristic is the number of SIMULTANEOUS WORKSTATIONS "
        "and the communications suite. "
        "Also: a command post is NOT an EOC. "
        "The ICP is at the scene; the EOC is at the jurisdiction level."
    ),
},

# ── UAS ──────────────────────────────────────────────────────────────────────
'8-508-2001': {
    'what_it_is': (
        "A Type I UAS (Unmanned Aircraft System) team operates a large commercial or "
        "professional-grade drone with thermal imaging AND optical cameras, "
        "45+ minutes of flight endurance, and is capable of night operations. "
        "Two crew minimum (pilot and visual observer). "
        "FAA Part 107 certified. Can be used for missing persons searches (thermal), "
        "fire perimeter mapping, damage assessment, structure evaluation after collapse, "
        "and situational awareness without risking manned aircraft. "
        "Modern Type I UAS platforms include the DJI Matrice 300, Autel EVO II, "
        "and dedicated public safety drones."
    ),
    'minimum_standards': (
        "2 crew (FAA Part 107 pilot + visual observer). "
        "Thermal and optical payload. 45+ minute endurance per battery set. "
        "Night operations capable. Data link to ground station. "
        "Range >1 mile. Weather capability (light wind/rain)."
    ),
    'ordering_guidance': (
        "Order Type I UAS for missing persons in terrain where ground search is slow, "
        "night SAR operations, fire perimeter mapping, post-disaster damage assessment, "
        "and any situation where aerial eyes are needed but manned aircraft are unavailable "
        "or it's too dangerous for helicopters."
    ),
    'common_confusion': (
        "Consumer drones (DJI Mini, Phantom) are NOT Type I UAS. "
        "They lack thermal capability, have short endurance, and their pilots "
        "may not be Part 107 certified. "
        "The 'drone guy' in your county may or may not have a Type I platform. "
        "Ask about: thermal camera? Night capability? Part 107 certification? "
        "Flight endurance? If the answers are no/short/no/under 30 minutes — that's Type III at best."
    ),
},

# ── COMMUNICATIONS ────────────────────────────────────────────────────────────
'2-508-1001': {
    'what_it_is': (
        "A Type I Mobile Communications Unit is a fully self-contained communications "
        "platform that can establish and maintain a complete tactical communications "
        "infrastructure for a complex incident — independent of commercial infrastructure. "
        "It provides satellite uplink for phone and internet, VHF/UHF tactical radio "
        "repeaters, HF radio for long-distance, P25 digital radio connectivity, "
        "data network, and a working environment for the Communications Unit Leader. "
        "Staffed by 8 people including the COML and technical specialists. "
        "Operates 72+ hours on internal power. "
        "Examples: FEMA Mobile Emergency Response Support (MERS) comms trailers, "
        "state ARES/RACES comms vans, utility communications trailers."
    ),
    'minimum_standards': (
        "Satellite uplink (voice and data). VHF/UHF repeater capability. "
        "HF radio. P25 digital radio. Internet connectivity. "
        "8 personnel. 72-hour self-powered. Backup power."
    ),
    'ordering_guidance': (
        "Order when the incident location has no communications infrastructure, "
        "when commercial systems are damaged or saturated, or when you need "
        "to establish a complete radio/data network from scratch. "
        "These are high-value resources — request early and plan for setup time."
    ),
    'common_confusion': (
        "A ham radio operator with a go-kit is NOT a Type I Comms Unit. "
        "Amateur radio provides valuable supplemental communications but "
        "does NOT replace a NIMS communications unit. "
        "The type designations require specific equipment AND personnel capability. "
        "FieldCommand IMS with its 44Net connection and radio infrastructure "
        "contributes to but does not replace a full Type I comms unit."
    ),
},

# ── SAR K9 ────────────────────────────────────────────────────────────────────
'8-508-1030': {
    'what_it_is': (
        "A Type I Canine Search Team consists of one FAA/FEMA or NASAR-certified "
        "disaster search dog and its handler. The dog is trained to locate living "
        "human victims buried in structural collapse rubble, debris, or wilderness terrain "
        "by detecting human scent. Type I teams are certified to the highest standard — "
        "the dog can work at night, in rubble piles, and can distinguish live victims "
        "from cadavers. The handler is also a trained rescue technician. "
        "These teams often travel with FEMA US&R task forces or state SAR teams."
    ),
    'minimum_standards': (
        "1 certified search dog. 1 handler. "
        "FEMA certification, NASAR WSAR, or state equivalent. "
        "Disaster/rubble certification preferred for collapse work. "
        "12-hour operational capability. Handler is WFR or EMT."
    ),
    'ordering_guidance': (
        "Order for structural collapse with potential live victims, "
        "missing persons in wilderness terrain (especially if victim has been "
        "missing more than 4-6 hours and scent trail may be degraded), "
        "and any situation where human scent detection would speed the search."
    ),
    'common_confusion': (
        "Not all search dogs are the same. A trained search dog is NOT "
        "a pet dog that 'finds things.' The difference between a certified "
        "disaster search dog and an uncertified dog on a SAR call is enormous. "
        "Also: dogs find SCENT, not people. Wind, terrain, time elapsed, "
        "and weather all affect how well a dog can work. "
        "A dog is a tool, not a guarantee."
    ),
},

}

if __name__ == '__main__':
    print(f"Full definitions: {len(NIMS_DEFINITIONS)}")
