from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                 Table, TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

OUTPUT = "/mnt/user-data/outputs/Geography_Complete_SRP_Guide.pdf"
W = A4[0] - 3.6*cm

# ── colour palettes by section ──────────────────────────────────────────────
PALETTES = {
    "tectonic":  {"hdr":"#1a237e","acc":"#3949ab","bg":"#e8eaf6","num":"#283593"},
    "rocks":     {"hdr":"#4a148c","acc":"#7b1fa2","bg":"#f3e5f5","num":"#6a1b9a"},
    "rivers":    {"hdr":"#006064","acc":"#00838f","bg":"#e0f7fa","num":"#00695c"},
    "physical":  {"hdr":"#1b5e20","acc":"#388e3c","bg":"#e8f5e9","num":"#2e7d32"},
    "human":     {"hdr":"#e65100","acc":"#ef6c00","bg":"#fff3e0","num":"#bf360c"},
    "rainforest":{"hdr":"#1b5e20","acc":"#2e7d32","bg":"#e8f5e9","num":"#1b5e20"},
    "desert":    {"hdr":"#bf360c","acc":"#e64a19","bg":"#fbe9e7","num":"#bf360c"},
}

def hx(h): h=h.lstrip('#'); return colors.Color(int(h[0:2],16)/255,int(h[2:4],16)/255,int(h[4:6],16)/255)
def safe(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def topic_header(story, pal_key, topic_num, title, marks_note):
    p = PALETTES[pal_key]
    hdr_style = ParagraphStyle('H',fontName='Helvetica-Bold',fontSize=13,textColor=colors.white,leading=16)
    sub_style = ParagraphStyle('S',fontName='Helvetica',fontSize=8,textColor=colors.Color(1,1,1,.8),leading=10)
    num_style = ParagraphStyle('N',fontName='Helvetica-Bold',fontSize=22,textColor=colors.Color(1,1,1,.3),leading=24)
    t = Table([[
        Paragraph(f"{topic_num}", num_style),
        Table([[Paragraph(safe(title),hdr_style)],[Paragraph(safe(marks_note),sub_style)]],
              colWidths=[W-2.5*cm]),
    ]], colWidths=[2.2*cm, W-2.2*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),hx(p["hdr"])),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(0,-1),10),('LEFTPADDING',(1,0),(1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ROUNDEDCORNERS',[6,6,6,6]),
    ]))
    story.append(t)
    story.append(Spacer(1,6))

def srp_card(story, pal_key, idx, label, text, total):
    p = PALETTES[pal_key]
    lbl_s = ParagraphStyle('L',fontName='Helvetica-Bold',fontSize=9,textColor=hx(p["num"]),leading=11,spaceAfter=1)
    bod_s = ParagraphStyle('B',fontName='Helvetica',fontSize=9.5,textColor=colors.HexColor('#1a1a1a'),leading=13.5)
    num_s = ParagraphStyle('Ns',fontName='Helvetica-Bold',fontSize=9,textColor=colors.white,leading=11)
    mk_s  = ParagraphStyle('Mk',fontName='Helvetica',fontSize=7.5,textColor=colors.Color(1,1,1,.8),leading=10)

    num_cell = Table([[Paragraph(f"SRP {idx}",num_s)],[Paragraph("2 marks",mk_s)]],colWidths=[1.55*cm])
    num_cell.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),hx(p["num"])),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    content_cell = Table([[Paragraph(safe(label),lbl_s)],[Paragraph(safe(text),bod_s)]],
                         colWidths=[W-1.75*cm])
    content_cell.setStyle(TableStyle([
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    row = Table([[num_cell,content_cell]],colWidths=[1.6*cm,W-1.6*cm])
    row.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),hx(p["bg"])),
        ('BACKGROUND',(0,0),(0,-1),hx(p["num"])),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ROUNDEDCORNERS',[4,4,4,4]),
    ]))
    story.append(KeepTogether(row))
    story.append(Spacer(1,4))

def geoecology_aspect_header(story, pal_key, title, marks):
    p = PALETTES[pal_key]
    s = ParagraphStyle('GH',fontName='Helvetica-Bold',fontSize=11,textColor=colors.white,leading=13)
    m = ParagraphStyle('GM',fontName='Helvetica',fontSize=8,textColor=colors.Color(1,1,1,.8),leading=10)
    t = Table([[Paragraph(safe(title),s),Paragraph(safe(marks),m)]],
              colWidths=[W*0.68,W*0.32])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),hx(p["acc"])),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(0,-1),12),('RIGHTPADDING',(-1,0),(-1,-1),10),
        ('ALIGN',(-1,0),(-1,-1),'RIGHT'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ROUNDEDCORNERS',[4,4,4,4]),
    ]))
    story.append(t)
    story.append(Spacer(1,5))

def cover_biome(story, pal_key, title, sub, note, scheme_lines):
    p = PALETTES[pal_key]
    ts = ParagraphStyle('T',fontName='Helvetica-Bold',fontSize=20,textColor=colors.white,leading=24)
    ss = ParagraphStyle('S',fontName='Helvetica',fontSize=11,textColor=colors.Color(1,1,1,.85),leading=14)
    ns = ParagraphStyle('N',fontName='Helvetica-Oblique',fontSize=9,textColor=colors.Color(1,1,1,.75),leading=12)
    rows = [[Paragraph(safe(title),ts)],[Paragraph(safe(sub),ss)],[Spacer(1,4)],[Paragraph(safe(note),ns)]]
    for l in scheme_lines:
        rows.append([Paragraph('• '+safe(l), ParagraphStyle('sl',fontName='Helvetica',fontSize=8.5,
                                textColor=colors.Color(1,1,1,.9),leading=12,leftIndent=6))])
    t = Table(rows,colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),hx(p["hdr"])),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
        ('LEFTPADDING',(0,0),(-1,-1),18),('RIGHTPADDING',(0,0),(-1,-1),18),
        ('ROUNDEDCORNERS',[7,7,7,7]),
    ]))
    story.append(t)
    story.append(Spacer(1,10))

# ═══════════════════════════════════════════════════════════════════════════
#  ALL TOPICS DATA
# ═══════════════════════════════════════════════════════════════════════════
TOPICS = [

# ── 1. PLATE TECTONIC THEORY ─────────────────────────────────────────────
{"num":"01","pal":"tectonic",
 "title":"Plate Tectonic Theory – Continental Drift & Seafloor Spreading",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Plate Tectonic Theory","The theory of plate tectonics states that the Earth's lithosphere is divided into approximately 15 large tectonic plates that float on the semi-molten asthenosphere and move slowly relative to each other."),
  ("Continental Drift – Wegener","Alfred Wegener proposed the theory of continental drift in 1912, arguing that all continents were once joined as a supercontinent called Pangaea approximately 300 million years ago, which subsequently broke apart and drifted to current positions."),
  ("Evidence – Jigsaw Fit","The coastlines of South America and Africa fit together like puzzle pieces, particularly the bulge of Brazil and the Gulf of Guinea in Africa, suggesting they were once joined as part of Gondwana."),
  ("Evidence – Fossil Records","Identical fossil species (e.g. Mesosaurus, Glossopteris fern) have been found on continents now separated by thousands of kilometres of ocean, indicating these landmasses were once connected."),
  ("Evidence – Rock Matching","Identical rock types and geological structures of the same age are found on opposite sides of the Atlantic Ocean — e.g. matching Precambrian rock sequences in eastern Brazil and West Africa."),
  ("Evidence – Ancient Climates","Coal deposits (formed in tropical swamps) have been found in Antarctica, and glacial deposits exist in tropical Africa, indicating these continents were once in entirely different climate zones."),
  ("Seafloor Spreading – Hess","Harry Hess proposed seafloor spreading in 1960: magma rises from the mantle at mid-ocean ridges (divergent boundaries), solidifies to form new oceanic crust, and pushes existing crust outward on both sides."),
  ("Mid-Atlantic Ridge","The Mid-Atlantic Ridge is a constructive plate boundary where the North American and Eurasian plates diverge. New basaltic oceanic crust is continuously being generated, causing the Atlantic Ocean to widen by approximately 2.5cm per year."),
  ("Magnetic Striping","When magma solidifies at mid-ocean ridges, iron minerals align with the Earth's magnetic field. As Earth's field reverses periodically, symmetric parallel magnetic striping on either side of ridges confirms seafloor spreading."),
  ("Subduction","Oceanic crust is denser than continental crust and is destroyed at destructive plate margins by subduction — it sinks into the mantle where it is melted and recycled. This balances the creation of new crust at ridges."),
  ("Convection Currents","The mechanism driving plate movement is convection currents in the mantle. Radioactive decay heats the mantle; hot material rises, spreads laterally beneath the lithosphere, drags plates, then cools and sinks — forming a convection cell."),
  ("Slab Pull","Slab pull is the dominant force driving plate movement. As dense, cool oceanic crust at a subduction zone sinks into the mantle, it pulls the rest of the plate behind it — contributing significantly to overall plate velocity."),
  ("Ridge Push","At mid-ocean ridges, newly formed elevated crust slides downslope away from the ridge under gravity. This ridge push force adds to the movement of plates away from constructive boundaries."),
  ("Hotspot Volcanism","Hotspots are fixed mantle plumes that burn through the lithosphere regardless of plate boundaries. As the Pacific Plate moves over the Hawaiian hotspot, a chain of progressively older volcanic islands has formed, confirming plate movement direction."),
  ("Age of Ocean Floor","Oceanic crust is youngest at mid-ocean ridges and oldest near subduction zones — confirmed by radiometric dating. The oldest ocean floor (~200 million years) is far younger than continental crust (~4 billion years), as oceanic crust is continuously recycled."),
]},

# ── 2. CONSTRUCTIVE/DIVERGENT BOUNDARIES ────────────────────────────────
{"num":"02","pal":"tectonic",
 "title":"Constructive/Divergent Boundaries – Forces and Landforms",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Definition","A constructive (divergent) plate boundary occurs where two tectonic plates move apart from each other. Magma rises from the mantle to fill the gap, solidifying to form new basaltic oceanic crust. No crust is destroyed — hence 'constructive'."),
  ("Driving Force","The plates are driven apart by convection currents in the asthenosphere, combined with ridge push — where newly formed elevated crust at the ridge slides downslope under gravity away from the boundary."),
  ("Mid-Atlantic Ridge – Location","The Mid-Atlantic Ridge is the world's longest mountain range at approximately 16,000km, running north-south through the Atlantic Ocean floor. It marks the diverging boundary between the North American and Eurasian plates (and South American and African plates further south)."),
  ("Iceland Example","Iceland sits directly on the Mid-Atlantic Ridge and is the only place where the ridge rises above sea level. The island is being split apart as the North American and Eurasian plates diverge at approximately 2.5cm per year, creating a visible rift valley through the country."),
  ("Rift Valley Formation","As plates diverge, tensional forces stretch and fracture the crust. Central sections collapse downward between parallel faults (normal faults), forming a rift valley — a long, linear depression. The East African Rift Valley is a continental example of this process."),
  ("Mid-Ocean Ridge Landform","The mid-ocean ridge is the primary landform at divergent boundaries — a continuous underwater mountain range formed by repeated eruptions of basaltic lava. The ridge can rise 2,000–3,000 metres above the surrounding ocean floor."),
  ("Basaltic Volcanism","Eruptions at constructive boundaries are effusive (non-explosive) because basaltic magma is low in silica and has low viscosity, allowing gases to escape gradually. Lava flows freely, building up the ridge and occasionally producing shield volcanoes (e.g. Skjaldbreidur, Iceland)."),
  ("Shallow Earthquakes","Earthquakes at constructive boundaries are shallow-focus (0–70km depth) and generally low magnitude, caused by tensional fracturing of the crust as plates pull apart. They are not typically as destructive as those at convergent boundaries."),
  ("Normal Faulting","As the crust is stretched at divergent boundaries, it fractures along normal faults — where one block drops down relative to the other. This produces stepped terrain along the rift zone and is responsible for the rift valley structure."),
  ("Geothermal Activity – Iceland","The proximity of magma to the surface at constructive boundaries produces intense geothermal activity. Iceland exploits this — approximately 90% of homes are heated geothermally, and geothermal energy accounts for approximately 65% of the country's primary energy use."),
  ("Geysers & Hot Springs","Groundwater heated by shallow magma produces geysers and hot springs along divergent boundaries. Iceland's Geysir (the original geyser) and the Blue Lagoon geothermal spa are direct results of the constructive boundary beneath Iceland."),
  ("New Ocean Formation","Continental rifting at divergent boundaries can eventually produce a new ocean. The East African Rift Valley is currently in the early stage of this process — in tens of millions of years, East Africa will separate and a new ocean basin will form between the fragments."),
  ("Red Sea Example","The Red Sea was formed by rifting of the African and Arabian plates beginning approximately 30 million years ago. It represents an intermediate stage between a continental rift valley (like East Africa) and a full ocean (like the Atlantic)."),
  ("Pillow Lavas","When basaltic lava erupts underwater at mid-ocean ridges, it cools rapidly on contact with seawater, forming rounded pillow-shaped structures called pillow lavas. These are found along the entire length of mid-ocean ridges and confirm underwater volcanic activity."),
  ("New Crust Thickness","Newly formed oceanic crust at constructive boundaries is approximately 6–10km thick. It is composed of basalt at the surface (from lava flows) with gabbro beneath (same composition but coarser crystals from slower cooling), overlying the mantle."),
]},

# ── 3. DESTRUCTIVE/CONVERGENT BOUNDARIES ────────────────────────────────
{"num":"03","pal":"tectonic",
 "title":"Destructive/Convergent Boundaries – Forces and Landforms",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Definition","A destructive (convergent) plate boundary occurs where two tectonic plates move toward each other. At least one plate is destroyed through subduction into the mantle. The denser plate always subducts beneath the less dense plate."),
  ("Ocean–Continent Subduction","When dense oceanic crust (basalt, ~3.0 g/cm³) converges with less dense continental crust (granite, ~2.7 g/cm³), the oceanic plate subducts. As it descends into the mantle it melts, generating magma that rises through the continental crust."),
  ("Ocean–Ocean Subduction","When two oceanic plates converge, the older and denser plate subducts. As it melts in the mantle, magma rises through the overlying oceanic crust, erupting on the seafloor to form a chain of volcanic islands — an island arc (e.g. Japan, Philippines)."),
  ("Continent–Continent Collision","When two continental plates collide (both too buoyant to subduct), they buckle and fold upward forming fold mountain ranges. The Himalayas formed when the Indian plate collided with the Eurasian plate approximately 50 million years ago."),
  ("Fold Mountains – Formation","Compressional forces at convergent boundaries cause horizontal sedimentary rock layers to buckle and fold upward, forming fold mountains. Sediments from the ocean floor (geosyncline) are compressed, uplifted, and deformed into anticlines and synclines."),
  ("Andes – Example","The Andes of South America formed where the Nazca oceanic plate subducts beneath the South American continental plate. This ongoing subduction has produced the world's longest continental mountain range (~7,000km) with peaks exceeding 6,900m."),
  ("Subduction Zone Volcanism","As the subducting oceanic plate descends, it releases water from hydrated minerals into the mantle, lowering the melting point of surrounding rock. The resulting silica-rich, viscous magma rises through the overlying plate to form stratovolcanoes (composite cones)."),
  ("Stratovolcanoes","Stratovolcanoes (e.g. Mt. Fuji, Japan; Mt. Pinatubo, Philippines) form at subduction zones. They are characterised by steep sides, alternating layers of ash and lava, and explosive eruptions. The high silica content traps gases, building tremendous pressure before eruption."),
  ("Deep Oceanic Trenches","As the oceanic plate bends downward into the mantle, it creates a deep oceanic trench — the deepest landforms on Earth. The Marianas Trench (Pacific) reaches 11,034m depth. Trenches mark the surface expression of subduction zones."),
  ("Deep-Focus Earthquakes","Earthquakes at destructive boundaries range from shallow to deep-focus (up to 700km depth) as the subducting slab descends through the mantle. The Wadati-Benioff zone marks the path of the subducting plate through earthquake distribution."),
  ("Japan Example – Island Arc","Japan is formed by subduction of the Pacific plate beneath the Eurasian plate. This has produced a volcanic island arc, frequent and powerful earthquakes (e.g. 2011 Tōhoku earthquake, magnitude 9.0), and a deep offshore trench (Japan Trench)."),
  ("Himalayan Collision","The Indian plate began colliding with the Eurasian plate approximately 50 million years ago. The collision is ongoing — the Himalayas are still rising approximately 5mm per year. Mount Everest (8,849m) is the result of this continent-continent collision."),
  ("Accretionary Wedge","As the oceanic plate subducts, sediments scraped off the descending plate accumulate at the margin as an accretionary wedge (or prism). These deformed sedimentary rocks can be found in ancient fold mountain belts, providing geological evidence of past subduction."),
  ("Benioff Zone","The Benioff Zone is the inclined plane of seismic activity that follows the path of the subducting oceanic plate from the trench down into the mantle. Earthquake foci become progressively deeper further from the trench, confirming the angle of subduction."),
  ("Back-Arc Spreading","Behind some island arcs, the overlying plate can be stretched and thinned by the sinking of the subducting slab, creating a back-arc basin. This tensional environment can produce small spreading centres behind volcanic arcs, e.g. behind the Mariana Islands."),
]},

# ── 4. POSITIVE & NEGATIVE IMPACTS OF VOLCANIC ACTIVITY ─────────────────
{"num":"04","pal":"tectonic",
 "title":"Positive and Negative Impacts of Volcanic Activity",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Volcanic Hazards Overview","Volcanic activity produces a range of hazards. Primary hazards include lava flows, pyroclastic flows, and tephra fall. Secondary hazards include lahars (volcanic mudflows), tsunamis triggered by submarine eruptions, and volcanic gases."),
  ("Pyroclastic Flows","Pyroclastic flows are superheated mixtures of gas, ash, and rock fragments travelling at speeds up to 700km/h at temperatures exceeding 800°C. They are the deadliest volcanic hazard — the 79AD eruption of Vesuvius destroyed Pompeii by pyroclastic flow, killing approximately 2,000 people."),
  ("Lava Flows – Negative","Lava flows destroy settlements, farmland, and infrastructure in their path. The 2021 Cumbre Vieja eruption (La Palma, Canary Islands) destroyed over 2,000 buildings and 1,200 hectares of farmland including vital banana plantations."),
  ("Ash Fall – Negative","Volcanic ash can collapse roofs, contaminate water supplies, disrupt aviation, and damage crops. The 2010 Eyjafjallajökull eruption in Iceland ejected ash that closed European airspace for 6 days, costing airlines approximately €1.3 billion."),
  ("Lahars – Volcanic Mudflows","Lahars form when volcanic material mixes with water (rainfall, melting glaciers, crater lakes). The 1985 Nevado del Ruiz eruption in Colombia triggered lahars that buried the town of Armero, killing approximately 23,000 people — one of the deadliest volcanic disasters of the 20th century."),
  ("Fertile Soils – Positive","Volcanic rock weathers over time into exceptionally fertile soils rich in minerals such as phosphorus, potassium, and calcium. Volcanic soils (andisols) support highly productive agriculture — the slopes of Mt. Etna (Sicily) produce rich harvests of citrus, grapes, and olives."),
  ("Geothermal Energy – Positive","Volcanic regions offer geothermal energy — heat from magma near the surface is used to generate electricity and heat buildings. Iceland generates approximately 25% of its electricity and 90% of its space heating from geothermal sources, providing cheap, renewable, low-carbon energy."),
  ("Tourism – Positive","Volcanoes attract significant tourism revenue. Mt. Etna (Sicily), Kilauea (Hawaii), and Vesuvius (Italy) draw millions of visitors annually. Hawaii Volcanoes National Park generates approximately $166 million annually for the local economy through volcano tourism."),
  ("New Land Creation","Volcanic activity builds new land. The Hawaiian island chain was entirely created by hotspot volcanism. The island of Surtsey emerged from the ocean off Iceland between 1963 and 1967, providing scientists with a unique opportunity to study ecosystem colonisation."),
  ("Mineral Resources – Positive","Volcanic activity concentrates valuable mineral deposits including copper, gold, silver, and sulfur. The Andean copper belt (Chile, Peru) — world's largest copper reserve — is directly associated with subduction-related volcanism and hydrothermal activity."),
  ("Volcanic Gases – Negative","Eruptions release large quantities of SO₂, CO₂, and HCl. SO₂ reacts with water vapour to form sulfuric acid aerosols, which can cool global temperatures. The 1991 Pinatubo eruption lowered global temperatures by approximately 0.5°C for two years."),
  ("Tsunamis – Negative","Submarine volcanic eruptions and caldera collapses can trigger devastating tsunamis. The 1883 Krakatau eruption generated waves up to 30m high, killing approximately 36,000 people in Java and Sumatra. The 2022 Hunga Tonga eruption produced a tsunami affecting coastlines across the Pacific."),
  ("Disruption to Agriculture – Negative","Ash fall smothers crops and pastures, acidic rain damages vegetation, and lava flows permanently destroy farmland. The 1783 Laki eruption in Iceland released toxic fluorine gases, killing 75% of Iceland's livestock and causing a famine that killed 25% of the population."),
  ("Monitoring & Prediction Benefit","Modern volcano monitoring (seismometers, tiltmeters, GPS, gas sensors) allows increasingly accurate eruption prediction. The successful 1991 evacuation of 58,000 people before the Pinatubo eruption in the Philippines saved thousands of lives."),
  ("Settlement Despite Risk","Despite hazards, dense populations live near volcanoes attracted by fertile soils, geothermal energy, tourism, and mining. The slopes of Merapi (Indonesia) support approximately 1 million people — illustrating how perceived benefits outweigh perceived risks for many communities."),
]},

# ── 5. OCCURRENCE OF EARTHQUAKES – PREDICTION & EFFECTS REDUCED ─────────
{"num":"05","pal":"tectonic",
 "title":"Occurrence of Earthquakes – Prediction and Effects Reduced",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Earthquake Definition & Cause","An earthquake is the sudden release of energy from the Earth's crust causing ground shaking. 90% of earthquakes occur at tectonic plate boundaries where stress accumulates as plates lock and strain builds until rupture occurs along fault planes."),
  ("Seismic Waves","Energy released during an earthquake travels as seismic waves. P-waves (primary/compressional) travel fastest and arrive first; S-waves (secondary/shear) arrive second; Surface waves cause the most ground motion and damage."),
  ("Richter Scale","The Richter Scale measures the energy released by an earthquake logarithmically — each step represents a 10× increase in ground motion. Japan's 2011 Tōhoku earthquake measured 9.0 on the Richter Scale — one of the most powerful ever recorded."),
  ("Mercalli Scale","The Mercalli Scale measures the intensity (observable damage) of an earthquake on a scale of I (imperceptible) to XII (total destruction). Unlike Richter, it varies with distance from the epicentre and local ground conditions."),
  ("Seismometers – Monitoring","Networks of seismometers continuously record ground motion along fault lines (e.g. San Andreas Fault, California). Historical seismic data is analysed to identify seismic gaps — sections of fault with no recent activity — indicating potential future earthquake locations."),
  ("GPS & Tiltmeters","GPS satellites and tiltmeters detect tiny ground deformations (uplift, tilting) that indicate stress accumulation in the crust. Systems along the San Andreas Fault in California measure millimetric movements that help scientists assess rupture probability."),
  ("Radon Gas Emissions","Increased radon gas emissions from rock fractures have been detected before some earthquakes. As stress builds, microfractures allow radon to escape to the surface — used as a potential precursor signal alongside other monitoring tools."),
  ("Seismic Gap Theory","The seismic gap theory identifies sections of active fault zones that have not experienced major earthquakes recently, suggesting stress is accumulating there. While not perfectly reliable for prediction, it helps prioritise monitoring and preparedness efforts."),
  ("Earthquake-Resistant Buildings","Earthquake-resistant structures use: cross-bracing (diagonal steel girders resisting lateral forces), base isolation (rubber-steel shock absorbers beneath foundations), and flexible frames. Japanese skyscrapers are designed to sway without collapsing during major earthquakes."),
  ("Strict Building Codes","Countries like Japan, California (USA), and New Zealand enforce strict seismic building codes requiring earthquake-resistant design for all new construction. Japan's codes have significantly reduced casualties in modern earthquakes compared to equivalent magnitude events in less-prepared countries."),
  ("Early Warning Systems","Japan's earthquake early warning system detects fast-moving P-waves and broadcasts alerts (via TV, phone, sirens) seconds before the more destructive S-waves and surface waves arrive — allowing people to take cover and automated systems to halt trains and machinery."),
  ("Tsunami Warning Systems","Deep-ocean pressure sensors (DART buoys) and coastal tide gauges detect tsunami-generating earthquakes and transmit warnings. The Pacific Tsunami Warning Centre provides warnings to 26 countries. The 2004 Indian Ocean Tsunami (220,000 deaths) highlighted the cost of lacking such systems."),
  ("Liquefaction","Liquefaction occurs when waterlogged, loose sediment temporarily behaves like liquid during earthquake shaking — foundations sink and buildings topple. The 2011 Christchurch earthquake caused widespread liquefaction, damaging approximately 15,000 homes in riverside suburbs."),
  ("Education & Preparedness","Japan's 'Drop, Cover, Hold' education campaign, regular earthquake drills in schools, and public preparedness culture significantly reduce casualties. Community awareness of evacuation routes, emergency supplies, and post-earthquake protocols is a critical non-structural mitigation measure."),
  ("Impossibility of Precise Prediction","Despite advances in monitoring, it remains impossible to predict the precise time, location, and magnitude of an earthquake with certainty. Probabilistic hazard assessments (e.g. 70% chance of major San Andreas earthquake within 30 years) guide long-term planning without enabling specific warnings."),
]},

# ── 6. GLOBAL DISTRIBUTION – VOLCANOES, EARTHQUAKES, FOLD MOUNTAINS ─────
{"num":"06","pal":"tectonic",
 "title":"Global Distribution of Volcanoes, Earthquakes and Fold Mountains",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Plate Boundary Control","The global distribution of volcanoes, earthquakes, and fold mountains is not random — approximately 90% are concentrated along tectonic plate boundaries. The pattern directly reflects the location of constructive, destructive, and conservative boundaries."),
  ("Pacific Ring of Fire","The Pacific Ring of Fire is a 40,000km horseshoe-shaped zone around the Pacific Ocean where approximately 90% of the world's earthquakes and 75% of its active volcanoes are concentrated. It marks where multiple oceanic plates subduct beneath continental plates."),
  ("Subduction Zone Volcanoes","Active volcanoes are concentrated at destructive (subduction) plate boundaries. The Cascades (Oregon/Washington), Andes, and Japanese island arc are all volcanic chains produced by subduction. These are stratovolcanoes characterised by explosive silica-rich eruptions."),
  ("Constructive Boundary Volcanoes","Effusive basaltic volcanoes occur at constructive boundaries along mid-ocean ridges. Iceland and the Azores are located on the Mid-Atlantic Ridge. Hotspot volcanoes (Hawaii) form far from plate boundaries where mantle plumes penetrate the lithosphere."),
  ("Fold Mountain Distribution","Fold mountains are distributed along destructive and collision plate boundaries. Major ranges include: the Himalayas (India-Eurasia collision), Andes (Nazca-South America subduction), Alps (Africa-Eurasia collision), and Rockies (Pacific-North America subduction)."),
  ("Earthquake Distribution – Plate Boundaries","Earthquakes are concentrated at all three types of plate boundary: constructive boundaries produce shallow, moderate earthquakes; destructive boundaries produce shallow to very deep earthquakes; conservative boundaries produce shallow, potentially very large earthquakes."),
  ("Conservative Boundaries – Earthquakes","At conservative (transform) boundaries, plates slide horizontally past each other with no creation or destruction of crust. Friction locks plates until stress ruptures in a major earthquake. The San Andreas Fault (California) is a conservative boundary between the Pacific and North American plates."),
  ("Intraplate Earthquakes","A small percentage of earthquakes (~10%) occur away from plate boundaries — intraplate earthquakes. These occur along ancient fault lines within plates. The 1811-1812 New Madrid earthquakes (central USA) are a historical example of major intraplate seismic activity."),
  ("Himalayan Example","The Himalayas are the result of the Indian plate (moving north at approximately 5cm/year) colliding with the Eurasian plate for the past 50 million years. The collision has produced the world's highest peaks, intense seismicity (e.g. 2015 Nepal earthquake, 7.8M), and no volcanic activity (no subduction)."),
  ("Alpine-Himalayan Belt","The Alpine-Himalayan mountain belt extends from the Alps through Turkey, Iran, and the Himalayas to Southeast Asia. It marks the collision zone between the African, Arabian, and Indian plates with the Eurasian plate — producing fold mountains and frequent earthquakes."),
  ("Rift Valley Distribution","Rift valleys form at divergent boundaries where continents are being pulled apart. The East African Rift System (extending from the Afar Triangle to Mozambique) is the world's most active continental rift, accompanied by volcanism (Kilimanjaro, Nyiragongo) and shallow earthquakes."),
  ("Volcanic Hotspots – Off-Boundary","Hotspot volcanoes form away from plate boundaries over stationary mantle plumes. As the overlying plate moves, a chain of progressively older volcanic islands forms. The Hawaiian Emperor Seamount Chain (6,000km long) records the Pacific Plate's movement over the Hawaiian hotspot."),
  ("Subduction Trench Location","Deep ocean trenches (>6,000m) are found parallel to and seaward of subduction-related volcanic arcs, marking where the oceanic plate bends into the mantle. The Marianas Trench (11,034m), Peru-Chile Trench, and Japan Trench all coincide with active subduction zones."),
  ("Caledonian & Hercynian Fold Mountains","Ancient fold mountains — Caledonides (Scotland, Norway, Appalachians) and Hercynides (southern Europe) — mark ancient plate collision zones. Now heavily eroded, they record past convergent boundaries. Ireland's Munster Ridge-and-Valley topography reflects Hercynian folding."),
  ("Mid-Ocean Ridge Global Network","The mid-ocean ridge system is the world's longest mountain chain (~60,000km), encircling the globe. It marks the global network of constructive boundaries where new oceanic crust is continuously being generated — the motor of seafloor spreading and continental drift."),
]},

# ── 7. TECTONIC ACTIVITY ON IRISH LANDSCAPE ──────────────────────────────
{"num":"07","pal":"tectonic",
 "title":"Impact of Tectonic Activity on the Irish Landscape (Volcanic/Folding)",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Overview of Irish Tectonic History","Ireland's landscape has been shaped by two major phases of tectonic activity: Caledonian folding (~400 million years ago) and Hercynian folding (~300 million years ago), plus limited volcanic activity associated with the opening of the North Atlantic ~65 million years ago."),
  ("Caledonian Orogeny","The Caledonian orogeny occurred approximately 400–420 million years ago when the Laurentian (North American) and Baltic plates converged. Compressional forces folded and uplifted rock layers in a NE-SW direction, forming the structural grain of northwest Ireland."),
  ("Caledonian Landscapes – Northwest Ireland","The Caledonian orogeny produced the NE-SW trending mountain ranges of northwest Ireland — Donegal Hills, Mayo's Nephin Beg Range, and the Galway/Connemara highlands. These are ancient, heavily eroded roots of once much higher mountain ranges."),
  ("Connemara Marble","Connemara marble formed during the Caledonian orogeny when limestone was subjected to intense heat and pressure (contact/regional metamorphism) as magma intruded into the rock approximately 400–450 million years ago, transforming it into distinctive green-veined marble."),
  ("Leinster Batholith","The Leinster Batholith is a large granite intrusion stretching from South Dublin to Wicklow, formed approximately 400 million years ago as magma was injected into the crust during the Caledonian orogeny. It now forms the Wicklow Mountains — Ireland's highest mountain range."),
  ("Hercynian Orogeny","The Hercynian (Variscan) orogeny occurred approximately 280–320 million years ago as the African and European plates converged. This compressed rocks in southern Ireland in an E-W direction, creating the distinctive ridge-and-valley topography of Munster."),
  ("Munster Ridge-and-Valley Topography","Hercynian folding produced alternating E-W anticlines (upfolds) and synclines (downfolds) across Munster. Harder Old Red Sandstone resists erosion to form ridges (e.g. Macgillycuddy's Reeks, Caha Mountains), while softer limestone synclines were eroded to form river valleys and bays."),
  ("Cork and Kerry Landscape","The distinctive 'grain' of the Cork and Kerry landscape — parallel E-W ridges and valleys — directly reflects Hercynian fold structures. River valleys like the Lee and Bandon follow synclinal axes, while peninsulas (Beara, Iveragh) follow anticlinal ridges."),
  ("Antrim Basalts – Volcanic Activity","Approximately 60–65 million years ago, the North American and Eurasian plates began to diverge, opening the North Atlantic Ocean. Associated volcanic activity produced massive basalt lava flows covering much of northeast Ireland, forming the Antrim Plateau."),
  ("Giant's Causeway","The Giant's Causeway on the Antrim coast formed approximately 60 million years ago as basaltic lava cooled slowly and contracted, fracturing into approximately 40,000 hexagonal columns. It is Ireland's only UNESCO World Heritage Site and a direct product of this volcanic episode."),
  ("Antrim Plateau","The Antrim Plateau is an extensive area of basaltic rock covering approximately 3,800km² in northeast Ireland. The basalt was extruded as runny lava flows from fissure eruptions during the opening of the North Atlantic, building up layers of dark rock visible in coastal cliffs."),
  ("Igneous Intrusions – Ring Dykes","Volcanic activity also produced igneous intrusions (dykes and sills) across Ireland. The Mourne Mountains in County Down are a complex of granite intrusions (ring dykes) associated with the same North Atlantic volcanic episode that produced the Antrim basalts."),
  ("Fold Mountains and Agriculture","Hercynian fold mountains in Munster have influenced land use — mountain ridges support sheep farming and forestry while fertile river valleys support dairy farming. The soils derived from Old Red Sandstone support grass growth, underpinning Cork's important dairy industry."),
  ("Tourism from Tectonic Features","Ireland's tectonic heritage generates significant tourism revenue. The Giant's Causeway attracts approximately 1 million visitors annually. Connemara's marble quarries, the Wicklow Mountains National Park, and the Kerry Mountains are major attractions rooted in Ireland's tectonic history."),
  ("Geological Timescale Context","The tectonic features shaping Ireland span over 400 million years of Earth history. Ireland provides a remarkable geological record — from ancient Precambrian rocks in Connemara (600+ million years old) to relatively recent Antrim basalts (60 million years) — making it an important site for geological research."),
]},

# ── 8. IGNEOUS ROCKS ─────────────────────────────────────────────────────
{"num":"08","pal":"rocks",
 "title":"Igneous Rock Formation – Basalt and Granite",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Igneous Rock Definition","Igneous rocks form from the cooling and solidification of magma (molten rock beneath the surface) or lava (molten rock above the surface). They are classified as volcanic (extrusive) if they cool at the surface or plutonic (intrusive) if they cool underground."),
  ("Crystal Size Principle","The rate of cooling determines crystal size in igneous rocks. Rapid cooling at the surface produces small crystals (no time for growth); slow cooling underground allows large crystals to form. This is the fundamental difference between volcanic and plutonic igneous rocks."),
  ("Basalt – Classification","Basalt is a volcanic (extrusive) igneous rock that forms when lava erupts onto the Earth's surface and cools rapidly. Its rapid cooling produces very small crystals — fine-grained texture. It is dark/black in colour, dense (~3.0 g/cm³), and rich in iron and magnesium (mafic)."),
  ("Basalt – Formation at Divergent Boundaries","Basalt forms primarily at constructive plate boundaries where the Eurasian and North American plates diverge. Decompression melting of mantle rock produces basaltic magma that erupts as low-viscosity lava flows. The Mid-Atlantic Ridge continuously generates new basaltic ocean floor."),
  ("Antrim Plateau – Basalt Ireland","The Antrim Plateau formed approximately 60–65 million years ago during the opening of the North Atlantic. Fissure eruptions produced extensive basalt lava flows covering approximately 3,800km². The Giant's Causeway — hexagonal basalt columns — formed as lava cooled and contracted."),
  ("Basalt – Crystal Minerals","Basalt contains small crystals of augite (pyroxene) and plagioclase feldspar, with olivine in some varieties. Crystals are too small to see with the naked eye. Obsidian is an extreme case — basaltic lava cooled so rapidly (e.g. contact with water) that no crystals formed, producing volcanic glass."),
  ("Granite – Classification","Granite is a plutonic (intrusive) igneous rock that forms when magma cools very slowly deep underground over millions of years. This slow cooling produces large, visible crystals. It is light grey-pink in colour, less dense (~2.7 g/cm³), and rich in silica and aluminium (felsic)."),
  ("Granite – Formation at Convergent Boundaries","Granite typically forms at destructive plate boundaries. When the subducting oceanic plate melts, silica-rich magma rises into the overlying continental crust. Rather than reaching the surface, it solidifies slowly underground as a large igneous body called a batholith."),
  ("Leinster Batholith","The Leinster Batholith is Ireland's largest granite intrusion, extending from South Dublin to Wicklow (~90km long). It formed approximately 400 million years ago during the Caledonian orogeny as magma intruded into surrounding sedimentary rock, cooling slowly to form granite with large visible crystals."),
  ("Granite – Crystal Minerals","Granite contains large, visible crystals of quartz (glassy), feldspar (pink or white), mica (flaky, black or silver), and sometimes hornblende. The interlocking large crystals give granite its characteristic speckled appearance and exceptional hardness and durability."),
  ("Dolerite – Intermediate","Dolerite is an intermediate igneous rock between basalt and granite in terms of crystal size, forming in thin intrusions (dykes and sills) where magma cools at a moderate rate. It has the same mineral composition as basalt but medium-sized crystals, visible with a hand lens."),
  ("Differential Weathering","Granite weathers more slowly than basalt due to its interlocking crystal structure and lower porosity. However, the feldspar in granite is susceptible to chemical weathering (hydrolysis), producing clay minerals and releasing quartz grains — forming sandy soils on granite uplands."),
  ("Uses of Basalt","Basalt has numerous economic uses: road aggregate and railway ballast (hard-wearing), building stone (durable), rock wool insulation (fibres from melted basalt), and increasingly as basalt fibre (stronger than glass fibre) for composite materials. The Giant's Causeway makes it a major tourist resource."),
  ("Uses of Granite","Granite is widely used in: construction (kerbstones, paving, building facades), monuments and memorials (durability), kitchen worktops (polished surfaces), and civil engineering (bridge piers, dam cores). Wicklow granite was used in the construction of Dublin's Custom House and GPO."),
  ("Tor Formation from Granite","When granite is deeply weathered underground along joint planes, rounded rock masses (corestones) form. If the overlying weathered material is later removed by erosion, isolated rounded granite boulders (tors) are exposed — a distinctive landform on granite uplands such as Dartmoor and the Wicklow Mountains."),
]},

# ── 9. SEDIMENTARY ROCKS ─────────────────────────────────────────────────
{"num":"09","pal":"rocks",
 "title":"Sedimentary Rock Formation – Limestone and Sandstone",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Sedimentary Rock Definition","Sedimentary rocks form from the compaction and cementation of sediments (rock fragments, mineral grains, organic material) deposited in layers over time. They cover approximately 75% of Earth's surface and are the only rock type to contain fossils."),
  ("Stages of Formation","Sedimentary rocks form through: (1) Weathering — breaking down existing rock; (2) Erosion and Transport — carrying particles by water, wind, ice; (3) Deposition — settling in layers (strata); (4) Compaction — pressure of overlying sediment squeezes layers; (5) Cementation — minerals bond particles together."),
  ("Limestone – Formation","Limestone is an organic sedimentary rock formed mainly from the compacted skeletal remains of marine organisms (corals, molluscs, foraminifera) that accumulated on ancient sea floors. Most Irish limestone formed approximately 300–360 million years ago during the Carboniferous period when Ireland lay beneath a warm tropical sea."),
  ("Limestone – Composition","Limestone is composed primarily of calcium carbonate (CaCO₃). It is light grey in colour, relatively soft (Mohs hardness 3), and contains fossils. It is jointed and bedded, making it permeable — water flows through joints rather than the rock mass itself."),
  ("Limestone Landscapes – Karst","Limestone is chemically weathered by carbonation, producing distinctive karst landscapes. Features include: limestone pavements (clints and grikes), sinkholes, caves, underground streams, stalactites and stalagmites. The Burren, Co. Clare is Ireland's finest karst landscape."),
  ("The Burren","The Burren in Co. Clare is a 360km² area of exposed Carboniferous limestone pavement. Clints (limestone slabs) are separated by grikes (deep fissures formed by carbonation along joints). The Burren's unique microclimate and soil chemistry support Arctic, Mediterranean, and alpine plant species simultaneously."),
  ("Sandstone – Formation","Sandstone is a clastic sedimentary rock formed from compacted and cemented sand-sized grains (quartz, feldspar). Sand is deposited in deserts, riverbeds, beaches, or shallow marine environments, then buried, compacted under pressure, and cemented by silica, calcium carbonate, or iron oxide."),
  ("Old Red Sandstone","Old Red Sandstone formed approximately 350–420 million years ago during the Devonian period in desert and river environments. It is red/brown due to iron oxide staining. In Ireland, it forms the hard, resistant ridges of Munster — e.g. Macgillycuddy's Reeks (Kerry) and the Caha Mountains."),
  ("Sandstone – Properties","Sandstone is porous and permeable (water moves through pore spaces), making it an important aquifer. It is generally more resistant to chemical weathering than limestone but weaker than granite. Colour varies — red (iron oxide), yellow, brown, or grey depending on cement type."),
  ("Carboniferous Limestone in Ireland","Carboniferous limestone underlies approximately 50% of Ireland's Central Lowlands, forming a relatively flat landscape. Where limestone is exposed, karst features develop. The limestone is extensively quarried for cement, road aggregate, and agricultural lime."),
  ("Fossils in Sedimentary Rock","Sedimentary rocks are the only rock type to preserve fossils — remains or traces of ancient organisms preserved in rock. Limestone commonly contains coral and shell fossils. Fossil evidence in Irish limestone confirms Ireland's ancient tropical marine environment during the Carboniferous period."),
  ("Economic Uses of Limestone","Limestone has major economic importance: cement manufacture (heated with clay to produce clinker); agricultural lime (neutralises acidic soil); building stone (historic buildings, walls); road aggregate; and chemical industry (iron smelting, glass making). Ireland quarries approximately 15 million tonnes annually."),
  ("Economic Uses of Sandstone","Sandstone is used as: building stone (many historic Irish buildings), paving stone, and as an aquifer providing water supplies. Old Red Sandstone's resistance makes it important for road aggregate in Munster. Some sandstone formations contain oil and gas (petroleum reservoir rocks)."),
  ("Strata & Unconformity","Sedimentary rocks form in horizontal layers (strata). Tectonic forces can tilt, fold, or fault these strata. An unconformity is a gap in the geological record where strata are missing (due to erosion or non-deposition), representing a significant interval of geological time."),
  ("Comparison – Limestone vs Sandstone","Limestone: organic origin, CaCO₃ composition, chemically weathered, karst landscapes, jointed permeability. Sandstone: clastic origin, quartz grains, physically and chemically weathered, porous permeability, often forms ridges. Both are Sedimentary but with contrasting compositions, origins, and landscape expressions."),
]},

# ── 10. METAMORPHIC ROCKS ────────────────────────────────────────────────
{"num":"10","pal":"rocks",
 "title":"Metamorphic Rock Formation – Marble and Quartzite",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Metamorphic Rock Definition","Metamorphic rocks form when existing rocks (igneous, sedimentary, or other metamorphic) are subjected to intense heat, pressure, or both, causing mineralogical and textural changes without the rock melting. The word 'metamorphic' means 'changed form'."),
  ("Contact Metamorphism","Contact (thermal) metamorphism occurs when magma intrudes into existing rock, baking the surrounding rock by intense heat. The affected zone — called the metamorphic aureole or contact zone — can extend tens to hundreds of metres from the intrusion."),
  ("Regional Metamorphism","Regional metamorphism occurs over large areas during mountain building (orogeny) when tectonic plates collide. Enormous compressional forces and increased temperature at depth affect vast volumes of rock simultaneously, producing metamorphic rocks over thousands of square kilometres."),
  ("Marble – Origin","Marble forms from limestone that has been subjected to heat and pressure (contact or regional metamorphism). The calcite crystals in limestone recrystallise into interlocking, larger crystals of calcite, transforming the rock into harder, denser, crystalline marble."),
  ("Connemara Marble – Formation","Connemara marble formed approximately 400–450 million years ago during the Caledonian orogeny when the Laurentian and Baltic plates converged. Magma intruded into surrounding limestone, baking it by contact metamorphism. The distinctive green colour results from serpentine and chromite minerals."),
  ("Marble – Properties","Marble is harder and denser than limestone (Mohs hardness ~3–4), with a crystalline texture and typically white, grey, or coloured appearance. It takes a high polish, making it aesthetically valuable. Like limestone, it reacts with acid (HCl fizzes) confirming its CaCO₃ composition."),
  ("Quartzite – Origin","Quartzite forms when sandstone undergoes regional or contact metamorphism. Heat and pressure cause the quartz grains in sandstone to recrystallise and fuse together. Quartzite is extremely hard (Mohs 7), resistant to weathering, and often forms prominent ridges."),
  ("Quartzite Formation in Ireland","Quartzite in Ireland formed during the Caledonian orogeny approximately 400 million years ago when sandstone was subjected to intense heat and pressure during mountain building. The Leinster Batholith baked surrounding sandstone during intrusion, producing quartzite in the contact zone."),
  ("Croagh Patrick – Quartzite","Croagh Patrick (Co. Mayo, 764m) is composed of quartzite — its brilliant white appearance results from the reflective crystalline quartz. The hardness of quartzite has made it highly resistant to glacial and other erosion, preserving the distinctive conical summit shape."),
  ("Quartzite – Properties","Quartzite is extremely hard and resistant (Mohs hardness 7), non-porous, and tough — more resistant than granite or limestone. It does not react with acid (unlike limestone). These properties mean quartzite forms durable ridges and peaks in metamorphic terrains."),
  ("Foliation","Foliation is a planar fabric that develops in metamorphic rocks when platy minerals (mica, chlorite) align perpendicular to the direction of maximum compressional stress. It produces a layered appearance (like pages in a book) in rocks such as slate and schist."),
  ("Slate – Contact Metamorphism","Slate forms from mudstone/shale subjected to low-grade metamorphism. Increased pressure causes clay minerals to recrystallise as tiny mica flakes aligned parallel to each other (cleavage), allowing slate to split into thin sheets. Used extensively as a roofing material."),
  ("Economic Uses of Marble","Marble is used in: sculpture and art (Michelangelo's David is Carrara marble); architecture (floors, walls, countertops); Connemara marble is Ireland's national gemstone, quarried near Clifden and internationally exported as decorative stone and jewellery. Global marble trade is worth billions annually."),
  ("Economic Uses of Quartzite","Quartzite is used as: road aggregate (highly durable), building stone, and refractory brick (resists very high temperatures in furnaces and kilns). Its hardness makes it an excellent abrasive. White quartzite sand is used in glass manufacture."),
  ("Comparison – Marble vs Quartzite","Marble: from limestone, CaCO₃, contact/regional metamorphism, reacts with acid, takes a polish, decorative uses. Quartzite: from sandstone, SiO₂, regional metamorphism, extremely hard, acid-resistant, resistant ridges. Both require heat/pressure but differ in parent rock, composition and properties."),
]},

# ── 11. ROCK TYPES & DISTINCTIVE LANDSCAPES ──────────────────────────────
{"num":"11","pal":"rocks",
 "title":"Rock Types Produce Distinctive Landscapes – Karst and Basalt/Granite",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Rock & Landscape Principle","The type of rock underlying an area fundamentally controls the landscape, as different rocks respond differently to weathering, erosion, and deposition. Three contrasting landscapes — Karst (limestone), basalt plateaux, and granite uplands — illustrate this clearly."),
  ("Carbonation – Chemical Weathering of Limestone","Limestone is chemically weathered by carbonation: rainwater absorbs CO₂ to form weak carbonic acid (H₂CO₃), which dissolves calcium carbonate in limestone (CaCO₃ + H₂CO₃ → Ca(HCO₃)₂). This process creates all karst features."),
  ("Limestone Pavement","Limestone pavements form where glaciers stripped the soil from flat limestone surfaces. Exposed to carbonation, the rock is dissolved along vertical joints, creating grikes (deep fissures) and clints (limestone slabs). The Burren (Co. Clare) is Ireland's finest limestone pavement."),
  ("Sinkholes & Caves","As carbonation widens joints vertically, surface water drains underground. Enlarged underground chambers form caves (e.g. Ailwee Cave, Burren; Dunmore Cave, Kilkenny). Roofs of shallow caves may collapse, forming sinkholes (dolines) on the surface."),
  ("Stalactites & Stalagmites","Inside limestone caves, calcium-rich groundwater drips from the ceiling. As CO₂ is released, calcium carbonate recrystallises: downward-growing stalactites and upward-growing stalagmites form over thousands of years. Where they meet, a column forms."),
  ("Basalt Plateau Landscapes","Basalt lava flows produce flat, stepped plateau landscapes. The Antrim Plateau (NE Ireland) is a classic basalt plateau — layers of dark basalt form flat-topped hills (mesas), with stepped cliff profiles where harder and softer lava flows weather at different rates."),
  ("Giant's Causeway","The Giant's Causeway formed as basaltic lava (~60 million years ago) cooled and contracted slowly, fracturing into approximately 40,000 interlocking hexagonal columns (averaging 45cm diameter). It is Ireland's only UNESCO World Heritage Site, attracting approximately 1 million visitors annually."),
  ("Basalt Weathering","Basalt weathers relatively quickly by chemical weathering (hydrolysis, oxidation of iron-rich minerals). Weathered basalt produces fertile soils (especially in humid climates). The Antrim Plateau's basalt soils support rich agriculture and grassland."),
  ("Granite Upland Landscapes","Granite forms high, rounded uplands. The Wicklow Mountains (Leinster Batholith) and Mourne Mountains are Ireland's main granite uplands. Granite's resistance to erosion maintains these elevated massifs. Glacial erosion has deepened valleys between rounded summits."),
  ("Tor Formation","Tors are isolated, rounded granite outcrops on upland summits. Formed by deep chemical weathering along joint planes underground, then exposed by erosion of the surrounding weathered material (regolith). Found on the Wicklow Mountains and Dartmoor (England)."),
  ("Granite – Differential Weathering","Feldspar crystals in granite are susceptible to hydrolysis, producing clay (kaolinite). Quartz grains resist weathering and accumulate as sandy material. This produces acidic, sandy, poorly-drained soils on granite uplands — supporting heathland and blanket bog rather than farmland."),
  ("Joints & Permeability","Limestone's joint system makes it permeable (water flows through joints) — producing underground drainage and dry valleys on the surface. Granite and basalt have different permeability characteristics. Sandstone is porous (water through pores). This determines drainage pattern and landscape."),
  ("Burren – Unique Ecology","The Burren's limestone pavement produces a unique ecological environment. Grikes provide frost-free, sheltered microhabitats that support rare plant communities — including Mediterranean orchids and Arctic mountain avens growing side-by-side. The Burren supports over 70% of Ireland's native plant species in just 360km²."),
  ("Economic Impact of Rock Type","Rock type shapes land use: Karst limestone areas (Burren) support low-intensity grazing and tourism; basalt plateaux (Antrim) support dairy farming on fertile soils; granite uplands (Wicklow) support sheep farming, forestry, and water catchments (Poulaphouca Reservoir supplies Dublin). Each rock type creates a distinct economic landscape."),
  ("Comparison Summary","Limestone: chemical weathering dominant, karst landscape, underground drainage. Basalt: hexagonal columns, fertile plateau soils, stepped cliffs. Granite: rounded uplands, tors, acidic soils, high resistance to erosion. All three rock types produce fundamentally different Irish landscapes from the same climatic conditions."),
]},

# ── 12. HUMAN INTERACTION WITH ROCK CYCLE – GEOTHERMAL ENERGY ───────────
{"num":"12","pal":"rocks",
 "title":"Human Interaction with the Rock Cycle – Geothermal Energy",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Rock Cycle Definition","The rock cycle is the continuous, slow process by which rocks are created, destroyed, and transformed between igneous, sedimentary, and metamorphic forms through weathering, erosion, deposition, compaction, melting, and cooling. Human activity can intervene at several stages."),
  ("Quarrying – Human Intervention","Quarrying dramatically accelerates the rock cycle by artificially exposing and removing rock at rates far exceeding natural erosion. Ireland quarries approximately 15–20 million tonnes of limestone annually for cement, aggregate, and agricultural lime — permanently altering landscapes."),
  ("Cement Production & CO₂","Cement manufacture (heating limestone with clay) releases stored CO₂ from CaCO₃ as well as from fuel combustion. Cement production accounts for approximately 8% of global CO₂ emissions — making it one of the largest contributors to anthropogenic climate change from rock cycle interference."),
  ("Geothermal Energy – Definition","Geothermal energy is heat energy derived from the Earth's interior — generated by radioactive decay in the mantle and crust and residual heat from Earth's formation. This heat is exploited at the surface as a renewable energy source in volcanically active regions."),
  ("Iceland – Geothermal Leader","Iceland is the world's leading user of geothermal energy, enabled by its location on the Mid-Atlantic Ridge where magma is close to the surface. Approximately 90% of Icelandic homes are heated geothermally, and geothermal sources provide approximately 25% of Iceland's electricity generation."),
  ("Geothermal Electricity Generation","High-temperature geothermal systems (>150°C) use steam from underground to drive turbines generating electricity. Iceland's Hellisheiði Power Plant is one of the world's largest geothermal plants, producing 303 MW of electricity and 400 MW of thermal energy for Reykjavik."),
  ("Geothermal Heating Systems","Lower-temperature geothermal water (~60–100°C) is used directly for space heating, district heating networks, greenhouses, and swimming pools. Iceland's geothermal district heating system supplies water at approximately 88°C to Reykjavik's 220,000 residents."),
  ("Hot Dry Rock (HDR) Systems","In areas without natural hydrothermal systems, Enhanced Geothermal Systems (EGS/HDR) inject water into hot fractured rock deep underground, extract the heated water, and use it to generate electricity. Potential exists globally, including in Ireland's deep granite formations."),
  ("Advantages of Geothermal Energy","Geothermal energy is: renewable (continuously replenished by Earth's heat); low-carbon (minimal emissions during operation); reliable (unlike solar/wind, provides baseload power regardless of weather); and cost-effective once infrastructure is established. Iceland's cheap geothermal power attracts energy-intensive industries."),
  ("Geothermal in Ireland – Potential","Ireland lacks high-temperature geothermal resources but has potential for low-temperature shallow systems using ground-source heat pumps. These extract heat from shallow ground (10–15°C) for space heating. Ireland's government has identified geothermal energy as a component of future renewable energy strategy."),
  ("Mining & Rock Cycle Acceleration","Mining accelerates the rock cycle by extracting minerals formed over millions of years. Irish examples: Tara Mines (Navan) — Europe's largest zinc/lead mine, extracting approximately 2.6 million tonnes of ore per year; Tara produces approximately 850,000 tonnes of zinc concentrate annually."),
  ("Oil & Gas Extraction","Oil and gas extraction removes hydrocarbons formed from ancient organic sediments over millions of years — permanently removing them from the rock cycle. Ireland has offshore gas reserves (Corrib Field, Co. Mayo) and explored petroleum potential in the Celtic Sea."),
  ("Land Reclamation","Humans use rock materials for land reclamation — creating new land from water. Offshore sand/gravel dredging for this purpose disrupts sediment transport cycles, affecting coastal erosion patterns. Dublin Port's expansion and Amsterdam's Schiphol Airport were built on reclaimed land."),
  ("Soil Erosion – Accelerated Weathering","Human activities (deforestation, agriculture, construction) accelerate weathering and erosion, dramatically speeding up the sediment production stage of the rock cycle. Ireland loses an estimated 1.3 million tonnes of topsoil annually to erosion — soil that takes thousands of years to form naturally."),
  ("Sustainable Rock Cycle Management","Sustainable management of rock resources requires: regulation of quarrying to minimise environmental impact; rehabilitation of quarried land; development of recycled aggregate to reduce primary extraction; and transition from carbon-intensive cement to lower-carbon alternatives (geopolymer cement)."),
]},

# ── 13. PHYSICAL/MECHANICAL WEATHERING ──────────────────────────────────
{"num":"13","pal":"physical",
 "title":"Physical/Mechanical Weathering – Freeze-Thaw and Exfoliation",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Weathering Definition","Weathering is the in-situ breakdown of rock at or near the Earth's surface by physical, chemical, or biological processes without significant transportation of material. It is the first stage of the rock cycle and provides the raw material for erosion and soil formation."),
  ("Mechanical Weathering Overview","Mechanical (physical) weathering breaks rock into smaller fragments without changing its chemical composition. The two main types affecting Irish and global landscapes are freeze-thaw action (frost shattering) and exfoliation (onion-skin weathering). Both exploit weaknesses in rock structure."),
  ("Freeze-Thaw – Process","Freeze-thaw occurs where temperatures fluctuate above and below 0°C. Water enters cracks in exposed rock and freezes. Water expands by approximately 9–10% on freezing, exerting pressures up to 2,000 kg/cm² on surrounding rock. On thawing, water re-enters deeper cracks. Repeated cycles widen cracks until pieces fracture off."),
  ("Freeze-Thaw – Conditions","Freeze-thaw is most effective at high altitudes (thin air, rapid temperature fluctuations) and high latitudes where daily or seasonal temperature cycles cross 0°C frequently. Irish mountains (e.g. Wicklow, Kerry) experience dozens of freeze-thaw cycles annually, especially in winter."),
  ("Scree – Landform","Broken rock fragments produced by freeze-thaw accumulate at the base of slopes as scree (talus) slopes. Scree consists of angular, unsorted rock fragments. Classic examples include the scree slopes beneath the Matterhorn (Switzerland) and Errigal Mountain (Co. Donegal)."),
  ("Frost Heaving","Freeze-thaw also causes frost heaving — ice forming beneath soil particles pushes them upward. This disrupts agricultural soils, lifts fence posts and foundations, and creates patterned ground features (stone circles, polygons) on cold upland surfaces — visible on Irish mountain plateaux."),
  ("Exfoliation – Process","Exfoliation (onion-skin weathering or insolation weathering) occurs in desert environments where diurnal temperature ranges exceed 30°C. Daytime heating causes surface rock to expand; rapid night cooling causes contraction. Repeated thermal stress causes outer layers of rock to peel away in concentric shells, like peeling an onion."),
  ("Exfoliation – Conditions","Exfoliation is most effective in hot deserts where: (1) Diurnal temperature ranges are extreme (daytime >40°C, night near 0°C); (2) Little moisture is present (preventing chemical weathering); (3) Rock is homogeneous (so expansion/contraction affects the whole surface simultaneously). The Sahara provides ideal conditions."),
  ("Exfoliation – Landforms","Exfoliation produces rounded rock outcrops (bornhardts or inselbergs) rising above desert plains. Smooth, curved rock surfaces are characteristic. In hot deserts, loose surface rock (rock varnish, desert pavement) results from millennia of exfoliation. Sugarloaf Mountain (Rio de Janeiro) is a classic exfoliation dome."),
  ("Desert Pavement","Repeated exfoliation in deserts produces a surface layer of angular rock fragments (desert pavement or reg). Fine material is removed by wind, leaving a concentrated veneer of coarser rock. This surface actually protects the underlying rock from further exfoliation once established."),
  ("Pressure Release / Dilatation","Pressure release (sheeting/dilatation) is another mechanical process: when overlying rock is removed by erosion, underlying rock expands and fractures parallel to the surface (sheet joints), producing curved slabs on granite domes and quarry faces. Often confused with exfoliation but driven by pressure not temperature."),
  ("Salt Crystal Growth","In arid coastal and desert environments, saline water enters rock pores and evaporates, leaving salt crystals. As crystals grow and hydrate, they exert pressure on surrounding rock, prising open pores and causing disintegration. Common in limestone sea cliffs and arid rock outcrops."),
  ("Biological Weathering","Plant roots grow into rock cracks, and as roots thicken, they exert pressure — a form of mechanical weathering. Lichens and mosses on rock surfaces contribute to both mechanical (root penetration) and chemical (acid secretion) breakdown. Significant on Irish limestone pavements."),
  ("Importance of Rock Type","Different rock types respond differently to mechanical weathering. Jointed rocks (limestone, sandstone) are most susceptible to freeze-thaw as water can penetrate joints. Massive, unjointed rocks (quartzite) are more resistant. Pre-existing weaknesses (bedding planes, faults, mineral grain boundaries) concentrate weathering."),
  ("Role in Soil Formation","Mechanical weathering is the essential first stage of soil formation, breaking bedrock into smaller fragments that can then be chemically weathered and biologically processed. The size of rock fragments produced determines soil texture — coarser fragments produce sandy soils; finer fragments support clay-rich soils."),
]},

# ── 14. CHEMICAL WEATHERING ──────────────────────────────────────────────
{"num":"14","pal":"physical",
 "title":"Chemical Weathering – Carbonation and Oxidation",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Chemical Weathering Definition","Chemical weathering is the decomposition of rock by chemical reactions that change the mineral composition of the rock. Unlike mechanical weathering, it alters the rock's chemistry. It is most intense in warm, humid environments where water and reactive gases are abundant."),
  ("Carbonation – Process","Carbonation is the most important chemical weathering process for limestone. Rainwater absorbs CO₂ from the atmosphere and soil to form weak carbonic acid (H₂CO₃). This reacts with calcium carbonate in limestone: CaCO₃ + H₂CO₃ → Ca(HCO₃)₂. Soluble calcium bicarbonate is carried away in solution, dissolving the rock."),
  ("Carbonation – Conditions","Carbonation is most effective where: rainfall is high (more water for reaction); CO₂ levels are elevated (soil CO₂ from plant respiration); temperatures are moderate (reactions faster when warm); and the rock is calcium carbonate-rich (limestone, chalk, marble)."),
  ("Limestone Pavement – Carbonation","Carbonation of exposed limestone produces the distinctive pavement of the Burren, Co. Clare. Vertical joints are widened by carbonation into grikes; horizontal bedding planes become clints. This process has occurred since the last Ice Age removed the protective soil cover ~10,000 years ago."),
  ("Cave Systems – Carbonation","Underground carbonation creates elaborate cave systems. As acidic groundwater flows through limestone joints, it dissolves rock to form passages and chambers. Aillwee Cave (Burren) and Dunmore Cave (Kilkenny) are formed by carbonation along joint and bedding planes."),
  ("Stalactite & Stalagmite Formation","When carbonation-saturated water drips into air-filled caves, CO₂ is released and CaCO₃ precipitates (recrystallises) as calcium carbonate. Downward-growing stalactites and upward-growing stalagmites form over thousands of years. Growth rates of 0.1–1mm per year are typical."),
  ("Oxidation – Process","Oxidation involves the reaction of minerals with oxygen (often dissolved in water). The most common example is the oxidation of iron-bearing minerals: Fe²⁺ is oxidised to Fe³⁺, producing iron oxides (rust/limonite). This weakens the rock structure and contributes to its breakdown."),
  ("Oxidation – Visible Evidence","The distinctive red-brown colour of Old Red Sandstone and many desert rocks results from iron oxide (haematite/limonite) coating mineral grains. The red soils of Co. Kerry are largely derived from oxidised Old Red Sandstone. Rust-coloured rock surfaces are evidence of oxidation weathering."),
  ("Oxidation – Pyrite Weathering","Pyrite (iron sulphide, FeS₂) in rocks oxidises rapidly when exposed to air and water. The reaction produces sulphuric acid — a highly aggressive acid that attacks surrounding rock and soil. Pyrite oxidation in construction materials has caused serious structural damage to Irish homes built with pyrite-contaminated hardcore."),
  ("Hydrolysis","Hydrolysis is the reaction between minerals and water. It is particularly important in breaking down feldspars in granite: feldspar + water → clay minerals (kaolinite) + silica + dissolved cations. This produces the clay-rich, sandy soils found on granite uplands and is the dominant weathering process in wet climates like Ireland."),
  ("Solution / Chelation","Organic acids from decomposing plant matter (humic acids) can dissolve minerals through chelation — organic molecules binding with metal ions and removing them from the rock structure. This is particularly significant in peat-covered areas where organic acids leach through soil, weathering underlying rock."),
  ("Carbonation vs Oxidation Comparison","Carbonation: primarily affects carbonate rocks (limestone, chalk, marble); produces soluble bicarbonates; creates karst features; effective in humid, CO₂-rich environments. Oxidation: primarily affects iron-rich minerals; produces insoluble iron oxides; reddens rocks and soils; effective wherever oxygen and moisture are present."),
  ("Role in Soil Development","Chemical weathering converts rock minerals into clay minerals and soluble compounds — the essential inorganic component of soil. The type of chemical weathering determines soil chemistry: carbonation produces lime-rich soils; hydrolysis of granite produces acidic, clay-sandy soils; oxidation produces iron-rich, often impermeable soils."),
  ("Irish Examples","Irish examples of chemical weathering: (1) Burren limestone pavement — carbonation; (2) Kerry Red Sandstone — oxidation; (3) Wicklow Mountain soils — hydrolysis of granite feldspar; (4) Blanket bog formation — organic acid chelation dissolving minerals from underlying rock and creating impermeable iron pan."),
  ("Climate Control on Chemical Weathering","Chemical weathering rates increase with temperature (reaction rates roughly double per 10°C rise — van't Hoff's Law) and with moisture availability. Tropical rainforests experience approximately 5–10× the chemical weathering rate of temperate regions. Ireland's mild, wet climate promotes moderate-to-high rates of chemical weathering year-round."),
]},

# ── 15. FEATURE OF FLUVIAL EROSION – WATERFALL ──────────────────────────
{"num":"15","pal":"rivers",
 "title":"Feature of Fluvial Erosion – Waterfall Formation",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Fluvial Erosion Overview","Fluvial erosion is the wearing away of rock and sediment by river action. The four main processes of river erosion are: hydraulic action (force of water), abrasion (sandpaper effect of carried material), attrition (collision of particles), and solution/corrosion (chemical dissolution). All four contribute to waterfall formation."),
  ("Waterfall Definition","A waterfall is a vertical or near-vertical drop in the long profile of a river, typically occurring in the upper course where the gradient is steep. Waterfalls form where a band of resistant rock overlies softer rock, creating differential erosion. The Torc Waterfall, Co. Kerry, is an Irish example."),
  ("Differential Erosion – Hard/Soft Rock","Waterfalls form where a river crosses a boundary between hard rock (e.g. granite, quartzite) upstream and softer rock (e.g. limestone, shale) downstream. The softer rock is eroded faster by hydraulic action and abrasion, creating a step in the riverbed — the waterfall."),
  ("Hydraulic Action","Hydraulic action is the sheer force and pressure of moving water crashing against the riverbed and banks. Water is forced into cracks and pores, compressing air — which, when released, chips fragments from the rock (cavitation). This is particularly powerful at the base of the waterfall."),
  ("Cavitation","Cavitation occurs when fast-moving water creates regions of very low pressure. Tiny water bubbles collapse violently, releasing energy that erodes the riverbed. Cavitation significantly increases erosion rates at the base of waterfalls where water velocity is highest."),
  ("Abrasion at Waterfall Base","As water falls, it carries sediment load including sand, gravel, and boulders. These are hurled against the plunge pool floor and walls with great force, abrading the rock like sandpaper. This deepens and widens the plunge pool over time."),
  ("Plunge Pool Formation","The impact of falling water at the base of a waterfall excavates a circular depression called a plunge pool. Swirling water and trapped rock fragments abrade the pool floor and walls, deepening and widening it. The Torc Waterfall's plunge pool has been carved by thousands of years of abrasion and cavitation."),
  ("Undercutting","Hydraulic action and abrasion erode the softer rock beneath the resistant cap rock faster than the cap itself. This creates an overhang — the hard rock protrudes unsupported over the plunge pool. Water splashing upward from the plunge pool also attacks the base of the hard cap by corrosion (especially if carbonate-rich water acts on limestone)."),
  ("Cap Rock Collapse","As undercutting deepens, the overhanging cap rock loses support and eventually collapses due to gravity. Large blocks fall into the plunge pool where they are broken down by attrition. The exposed new cliff face then begins the undercutting process again."),
  ("Headward Erosion / Retreat","Each cycle of undercutting and collapse causes the waterfall to migrate upstream — a process called headward erosion or waterfall retreat. Over thousands of years this can move the waterfall significant distances, leaving behind a steep-sided gorge downstream of the original position."),
  ("Gorge Formation","As a waterfall retreats upstream, the abandoned riverbed downstream is left as a deep, steep-sided gorge. The width of the gorge reflects the retreat distance; the depth reflects erosional intensity. Gorge du Verdon (France) and the Niagara Gorge (11km long) are formed by waterfall retreat."),
  ("Niagara Falls Example","Niagara Falls (USA/Canada) straddles a boundary between hard dolomite cap rock and softer shale beneath. The waterfall retreats approximately 1 metre per year through the undercutting-collapse cycle. It has retreated approximately 11km from its original position at the Niagara Escarpment over 12,000 years since the last ice age."),
  ("Solution/Corrosion","Where the rocks contain carbonate minerals, carbonic acid in river water dissolves calcium carbonate (solution/corrosion), contributing to undercutting. This is especially significant where waterfalls flow over limestone — carbonation enlarges joints in the cap rock, accelerating collapse."),
  ("Attrition","Attrition occurs when particles carried by the river collide with each other and with the riverbed. Rocks in the plunge pool become progressively smaller, rounder, and smoother as they are broken down. The resulting fine material is more easily transported downstream, removing material from the waterfall zone."),
  ("Long Profile Change","Waterfalls represent a 'nick point' — a sudden step in the river's long profile. Over geological time, as the waterfall retreats upstream, it smooths the long profile toward the theoretical graded profile — a smooth, concave curve from source to sea. Waterfall formation and retreat is thus a self-eliminating feature on a geological timescale."),
]},

# ── 16. FEATURE OF FLUVIAL DEPOSITION – DELTA ───────────────────────────
{"num":"16","pal":"rivers",
 "title":"Feature of Fluvial Deposition – Delta Formation",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Fluvial Deposition Overview","Deposition occurs when a river loses energy and can no longer transport its sediment load. Energy loss is caused by: reduced gradient, increased load, entering a standing body of water, or vegetation obstruction. Deltas form specifically where rivers enter seas, lakes, or oceans."),
  ("Delta Definition","A delta is an accumulation of sediment deposited where a river enters a standing body of water (sea, lake, or ocean), loses velocity, and drops its load. The term comes from the Greek letter Δ, as the Nile Delta resembles this shape. Deltas require more sediment input than wave/tidal removal."),
  ("Loss of Velocity","As a river enters standing water (sea/lake), it immediately loses forward momentum. The contrast between moving fresh water and standing salt water, combined with the absence of a gradient, causes rapid velocity reduction, triggering mass deposition of the river's entire sediment load."),
  ("Flocculation","Flocculation is a crucial process in delta formation. Fine clay particles (negatively charged) carried in suspension flocculate (clump together) when they encounter salt water (electrolyte). Electrical charge differences cause clay particles to form larger flocs that sink rapidly — much faster than individual clay particles would settle."),
  ("Three-Layer Structure","Deltas form with a characteristic three-part sedimentary structure: (1) Bottomset beds — finest clay deposited furthest into the sea, laid horizontally; (2) Foreset beds — coarser sand/silt deposited at the advancing delta front, inclined; (3) Topset beds — coarsest material on the delta surface, nearly horizontal."),
  ("Distributaries","As sediment builds up, the river channel becomes blocked by its own deposits and splits into multiple branching channels called distributaries, which spread across the delta surface like a fan. Each distributary distributes the river's flow and sediment across the growing delta."),
  ("Arcuate (Fan-Shaped) Delta","Arcuate deltas are fan-shaped with a smooth curved coastline, formed where wave action is moderate. Strong waves rework and redistribute sediment evenly along the delta front. The Nile Delta (Egypt) is the classic arcuate delta, covering approximately 22,000km² and fanning into the Mediterranean Sea."),
  ("Bird's Foot Delta","Bird's foot deltas (e.g. Mississippi, USA) form where river discharge is high and wave/tidal energy is low. Sediment is deposited rapidly in long, finger-like distributaries that extend into the Gulf of Mexico. The lack of wave energy means sediment is not redistributed, creating the distinctive bird's foot shape."),
  ("Cuspate Delta","Cuspate deltas form where wave energy acts from two opposing directions, producing a roughly triangular, pointed delta. The Tiber River delta (Italy) is an example. Wave action from both sides prevents the fan-shape of arcuate deltas from developing."),
  ("Lacustrine Delta","A lacustrine delta forms where a river enters a lake. Lake water has minimal tidal or wave energy, allowing rapid sediment accumulation. The Shannon's delta into the Shannon Estuary shows some lacustrine characteristics. The Ganges-Brahmaputra delta is the world's largest delta at approximately 100,000km²."),
  ("Nile Delta – Human Modification","The Nile Delta is critically threatened by the 1970 Aswan High Dam, which traps approximately 98% of the Nile's sediment load upstream. Without replenishment, wave erosion now removes approximately 35–100m of delta coastline annually. Egypt's most fertile agricultural land and home to approximately 40 million people is threatened."),
  ("Mississippi Delta – Issues","The Mississippi Delta is sinking (subsidence) at approximately 1–2cm per year due to compaction of delta sediments and rising sea levels. Reduced sediment supply (upstream dams and levees) means the delta is no longer growing. New Orleans is at serious risk of inundation as protective wetlands shrink."),
  ("Shannon Estuary / Tidal Influence","The Shannon Estuary (Ireland) demonstrates how tidal energy limits delta formation. Strong tides redistribute deposited sediment, preventing a classic delta from forming — instead producing extensive mudflats and salt marshes. Delta formation requires sediment supply to exceed the redistribution capacity of tidal and wave energy."),
  ("Agricultural Importance","River deltas are among the world's most fertile agricultural areas. Delta soils are annually replenished by nutrient-rich flood sediments (alluvium). The Nile Delta, Mekong Delta (Vietnam), and Ganges-Brahmaputra Delta support hundreds of millions of people in some of the world's most intensive agricultural systems."),
  ("Environmental Threats to Deltas","Deltas globally face multiple threats: (1) Reduced sediment supply from upstream dams; (2) Subsidence from groundwater extraction and sediment compaction; (3) Sea level rise (average deltas are <2m above sea level); (4) Saline intrusion into agricultural land. The IPCC identifies major delta cities (Dhaka, Ho Chi Minh City, Cairo) as severely threatened."),
]},

# ── 17. HUMAN IMPACT ON FLUVIAL PROCESSES – ASWAN DAM ───────────────────
{"num":"17","pal":"rivers",
 "title":"Impact of Human Activity on Fluvial Processes – Aswan High Dam, Egypt",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Context – River Nile & Aswan Dam","The River Nile (6,650km, world's longest river) flows north through Sudan and Egypt to the Mediterranean. The Aswan High Dam, completed in 1970, is a 111m high, 3.8km long dam creating Lake Nasser — approximately 550km long. It dramatically altered the natural fluvial system downstream."),
  ("Purpose – Flood Control","Before the dam, the Nile flooded annually (July–October), depositing nutrient-rich silt across Egyptian farmland. Devastating floods in 1964 and 1967 destroyed crops. A key purpose of the dam was flood regulation — eliminating unpredictable destructive flooding and enabling year-round controlled water release."),
  ("Purpose – Irrigation","The dam provides year-round controlled irrigation water to Egyptian farmland, enabling double and triple cropping of land previously only cultivated seasonally. Approximately 3.3 million hectares of land are now irrigated, including approximately 1 million hectares of newly reclaimed desert land."),
  ("Purpose – Hydroelectric Power","The Aswan dam generates approximately 2,100 MW of hydroelectric power, supplying approximately 15% of Egypt's electricity at the time of completion (lower percentage today due to population growth). This provided affordable power for industrialisation and significantly improved rural electrification."),
  ("Negative – Sediment Trapping","The dam traps approximately 98% of the Nile's natural sediment load in Lake Nasser. Before the dam, approximately 100–130 million tonnes of silt were deposited annually on the Nile floodplain, maintaining soil fertility. This silt is now accumulating behind the dam, reducing reservoir capacity over time."),
  ("Negative – Loss of Soil Fertility","Without annual silt deposition, Egyptian agricultural soils have become progressively less fertile. Farmers now depend entirely on expensive artificial fertilisers to replace the nutrients formerly supplied free by annual flooding — increasing agricultural costs and creating dependency on chemical inputs."),
  ("Negative – Delta Erosion","Without sediment replenishment, the Nile Delta is eroding at rates of 35–100 metres per year along its coastline. Wave action now removes more material than the river deposits. The delta — home to approximately 40 million people and 60% of Egypt's agricultural output — is threatened by both erosion and sea level rise."),
  ("Negative – Waterlogging & Salinisation","Year-round irrigation without adequate drainage has caused waterlogging and salinisation in approximately 35% of Egypt's irrigated land. Capillary action draws dissolved salts to the surface as water evaporates, reducing soil fertility and crop yields. This is a major long-term agricultural problem."),
  ("Negative – Downstream Channel Erosion","Without its sediment load, the Nile downstream of the dam now flows with excess erosive energy — 'hungry water'. The river is actively eroding its own bed and banks downstream of Aswan, undermining bridges and eroding riverbanks — increasing infrastructure maintenance costs."),
  ("Negative – Fisheries Decline","The Mediterranean Sea receives approximately 70% less nutrient-rich Nile sediment than before the dam. This has dramatically reduced phytoplankton productivity — the base of the marine food chain. Eastern Mediterranean fish catches declined by approximately 80% in the 1970s following dam completion, affecting fishing communities."),
  ("Negative – Population Displacement","The creation of Lake Nasser required the resettlement of approximately 100,000 Nubian people from their ancestral homelands in southern Egypt and northern Sudan. Archaeological sites including the Abu Simbel temples had to be physically relocated at enormous cost."),
  ("Positive – Food Security","By enabling year-round irrigation, the dam allowed Egypt to significantly increase agricultural output, supporting a population that has grown from approximately 30 million (1970) to over 100 million (2024). Without the dam, Egypt's food insecurity would be far more severe."),
  ("Positive – Flood Elimination","The dam successfully eliminated devastating annual floods. Since 1970, no destructive Nile flood has occurred. This has protected lives, property, and infrastructure, and has enabled permanent settlement and cultivation on the Nile floodplain without annual flood risk."),
  ("Lake Nasser – Benefits","Lake Nasser provides a strategic water reserve for Egypt — critical for a country receiving less than 25mm of rainfall annually. The lake supports a significant fishing industry (approximately 35,000 tonnes annually), and hosts Lake Nasser tourism cruises. The reservoir provides water security during drought years."),
  ("Evaluation – Benefits vs Costs","The Aswan Dam illustrates the complex cost-benefit relationship of large dam projects. While it delivered flood control, irrigation, and power, long-term costs — sediment trapping, delta erosion, soil salinisation, fishery decline — were underestimated. Modern dam projects require more thorough environmental impact assessment before construction."),
]},

# ── 18. ISOSTATIC PROCESSES ──────────────────────────────────────────────
{"num":"18","pal":"rivers",
 "title":"Isostatic Processes – Base Level Change, Knick Points and Paired Terraces",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Isostasy Definition","Isostasy is the principle of gravitational equilibrium between the Earth's lithosphere and asthenosphere. The crust 'floats' on the denser, semi-fluid mantle. When weight is added (e.g. ice sheets), the crust sinks; when weight is removed (e.g. ice melts), the crust slowly rebounds upward — isostatic rebound."),
  ("Glacial Isostatic Depression","During the last glacial maximum (~20,000 years ago), ice sheets up to 1km thick covered Ireland and Britain. The enormous weight of ice (approximately 3 million tonnes per km²) depressed the crust downward by 50–100 metres, pushing it into the underlying asthenosphere."),
  ("Post-Glacial Isostatic Rebound","As ice sheets melted (~15,000–10,000 years ago), the weight was removed and the crust slowly began to rebound upward — a process called isostatic rebound. Rebound is still ongoing in Scotland and Scandinavia, which are rising at approximately 3–10mm per year."),
  ("Ireland – Isostatic Rebound","Ireland has experienced post-glacial isostatic rebound, though less dramatically than Scotland (which was more heavily glaciated). Evidence includes raised beaches — ancient beach deposits now found metres above current sea level — along Ireland's north and west coasts."),
  ("Base Level Definition","A river's base level is the lowest level to which it can erode — effectively sea level (or the level of a lake for tributary rivers). Any change in base level alters the river's gradient and therefore its erosive energy along its entire course."),
  ("Fall in Base Level – Cause","Isostatic rebound causes relative sea level to fall — the land rises relative to the sea. This lowers the river's base level, steepening its gradient and giving it renewed erosive power. Sea level fall (eustatic fall, e.g. during glacials when water is locked in ice) has the same effect."),
  ("River Rejuvenation","When base level falls, a river responds by downcutting (vertical erosion) into its former floodplain to re-establish its graded profile. This renewed erosive activity — called rejuvenation — produces distinctive landforms that record the change in base level."),
  ("Knick Point Definition","A knick point (nick point) is a sudden break of slope in a river's long profile — a step or waterfall that marks the point where the rejuvenated lower course meets the older, pre-rejuvenation upper course. It represents the upstream-migrating wave of erosion following base level fall."),
  ("Knick Point Formation","After base level falls, the river begins downcutting at its mouth. This erosion migrates upstream as a knick point — a wave of incision that progressively works its way up the river course over time, steepening the gradient downstream of the knick point while leaving the upper course initially unchanged."),
  ("Knick Point Migration","Knick points migrate upstream at a rate depending on rock type and discharge. In resistant rock, migration is slow and the knick point may persist as a waterfall for millions of years. In soft rock, migration is rapid. The River Nore knick point in Ireland is an example of a knick point formed by isostatic rebound."),
  ("Paired Terraces – Formation","When rejuvenation causes a river to downcut into its old floodplain, the former floodplain surface is left elevated on both sides of the new, lower channel — as river terraces. Where matching terraces appear on both sides of the valley at the same height, they are called paired terraces."),
  ("Paired Terraces – Structure","Terraces consist of a flat upper surface (the remnant of the old floodplain, covered in river gravel/alluvium) and a steep inner face (the bluff) where the river cut downward. Multiple phases of rejuvenation produce multiple stepped terraces at different heights — like a staircase down the valley sides."),
  ("River Dodder – Dublin Example","The River Dodder in Dublin displays paired river terraces formed by post-glacial rejuvenation. The flat terrace surfaces on both sides of the valley floor are remnants of former floodplains, now elevated above the current river level as the Dodder cut down following isostatic rebound."),
  ("Eustatic Sea Level Change","Eustatic changes in sea level (global sea level rise or fall) also cause rejuvenation. During glacials, global sea level fell approximately 120m (water locked in ice sheets), exposing continental shelves and triggering massive river rejuvenation worldwide. During interglacials (like today), rising sea level raises base level, causing deposition."),
  ("Raised Beaches – Evidence","Raised beaches are ancient beach deposits (sand, gravel, shells) now found above current sea level. They provide evidence of former sea levels and isostatic/eustatic change. Raised beaches at 5–8m above sea level along the Irish coast date from approximately 6,000–8,000 years ago when isostatic rebound exceeded eustatic sea level rise."),
]},

]

# ── GEOECOLOGY DATA (abbreviated here, full data from previous script) ──

RAINFOREST_ASPECTS = [
  ("Climate",
   "4 marks identifying + 8 SRPs × 2 marks = 20 marks",
   [
    ("Biome & Location","A biome is a large community of flora and fauna shaped by climate. The tropical rainforest biome is located between 5°N and 10°S of the equator, encompassing the Amazon Basin, Congo Basin, and Indo-Malaysia."),
    ("Average Temperature","Average daily temperature is ~27°C year-round. The sun is almost perpendicular to the ground, and the region experiences approximately 12 hours of sunlight daily, 365 days a year, maintaining consistently warm conditions."),
    ("Annual Temperature Range","Annual temperature range is just 2°C. However the diurnal range (day–night) reaches up to 10°C, with daytime highs of 26–32°C. Nights rarely fall below 20°C due to insulating cloud cover and high humidity."),
    ("ITCZ & Convectional Rainfall","The Amazon lies in the path of the Intertropical Convergence Zone (ITCZ) where trade winds from both hemispheres converge, creating persistent low pressure. Warm moist air rises, cools, and condenses into frequent convectional rainfall almost daily."),
    ("Precipitation – Amount","Annual precipitation ranges from 2,000–3,500mm, occurring almost daily as heavy short-lived afternoon thunderstorms. Rainfall is heaviest during the wet season, providing the moisture base for the entire ecosystem."),
    ("Humidity","Humidity ranges between 77% and 88% year-round. Evapotranspiration — trees releasing moisture into the atmosphere — sustains the rainforest's own rainfall cycle. Thick cloud cover further traps moisture, maintaining the warm, damp atmosphere."),
    ("Evapotranspiration","Evapotranspiration is a key process: trees and plants release moisture from leaf surfaces into the atmosphere. This moisture recycles within the rainforest system, contributing up to 50% of its own rainfall — making the rainforest self-sustaining."),
    ("Climate–Ecosystem Link","The combination of 27°C temperatures, 2,000–3,500mm rainfall, and 77–88% humidity creates ideal conditions for the highest biodiversity of any biome on Earth, supporting dense multi-layered vegetation and thousands of animal species."),
   ]),
  ("Soils (Latosols)",
   "4 marks identifying + 8 SRPs × 2 marks = 20 marks",
   [
    ("Latosol Definition","Latosols (tropical red soils) are the zonal soils of the Amazon. They are mature soils developed over long periods in response to tropical climate and vegetation. Despite supporting lush forest, latosols are paradoxically nutrient-poor."),
    ("Depth","Latosols are exceptionally deep — up to 30 metres — among the deepest soils on Earth. This depth results from intense chemical weathering over millions of years in the warm, humid climate."),
    ("Laterisation & Colour","Laterisation is the dominant soil-forming process. Deep leaching and intense chemical weathering leave behind iron oxide and aluminium oxide, giving latosols their characteristic reddish-yellow colour. Nutrients are washed away, leaving iron-rich, infertile soils."),
    ("Leaching","Constant heavy rainfall leaches nutrients continuously downward through the soil profile and away from plant roots. The A horizon (surface layer) is left infertile despite the luxuriant vegetation above."),
    ("Rapid Decomposition","Decomposition in the Amazon occurs approximately 10 times faster than average due to warm, humid conditions. Fungi, bacteria, and insects break down organic matter rapidly, recycling nutrients back into the thin topsoil — creating a very short nutrient cycle."),
    ("pH & Humus","Latosols are moderately acidic (pH ~5) with very low humus content. Organic matter decomposes so rapidly it cannot accumulate. The soil is clay-rich (kaolin), giving a sticky texture."),
    ("Short Nutrient Cycle","The short nutrient cycle means plants must absorb nutrients immediately before rainfall leaches them away. Most nutrients at any time are stored in the living biomass, not in the soil — making the system extremely vulnerable to deforestation."),
    ("Deforestation Impact","When forest is cleared, the protective canopy is removed, exposing soil to direct sunlight. The soil bakes hard, becomes compacted, loses its ability to absorb water, and rapidly degrades. It takes up to 400 years to develop just 1cm of topsoil."),
   ]),
  ("Flora – Vegetation",
   "4 marks identifying + 8 SRPs × 2 marks = 20 marks",
   [
    ("Biodiversity & Overview","The Amazon has the highest biodiversity of any biome — 27°C temperatures, 2,000–3,000mm rainfall and 88% humidity support dense evergreen vegetation. Emergent trees reach nearly 70 metres. Tropical rainforests cover just 6% of Earth's surface but contain over 50% of its species."),
    ("Stratification","The rainforest is divided into four distinct vertical layers (stratification): Forest Floor, Understory, Canopy, and Emergent. Stratification developed as plants adapted to reduce competition for light, water, and nutrients."),
    ("Forest Floor","Extends to ~2 metres. Receives only 1% of sunlight. Vegetation consists mainly of shrubs, ferns, and decomposing fungi. Plants grow only where light penetrates through fallen tree gaps. Rapid decomposition of leaf litter recycles nutrients."),
    ("Understory Layer","Extends 2–20 metres. Receives approximately 5% of sunlight. Plants have adapted by developing large, broad, dark-green leaves to maximise photosynthesis in low-light conditions. Young trees wait here for canopy gaps."),
    ("Canopy Layer","Situated 20–40 metres above ground, receiving 98% of sunlight. Home to up to 90% of all rainforest species. Leaf 'drip tips' shed excess rainwater rapidly, preventing fungal growth. Epiphytes (orchids, bromeliads) grow on branches, obtaining nutrients from air and rain."),
    ("Emergent Layer","Tallest layer (60–70 metres): kapok and Brazil nut trees. Exposed to strong winds and lower humidity — trees have small, waxy, leathery leaves to minimise water loss. Develop buttress roots for stability and nutrient absorption in shallow, poor soil."),
    ("Buttress Roots","Buttress roots are large above-ground root flanges supporting emergent trees in shallow, nutrient-poor latosol soil. They provide structural stability for 60–70 metre trees and greatly increase surface area for absorbing nutrients from the thin topsoil layer."),
    ("Plant Adaptations","Plants have evolved multiple adaptations: drip tips (shed excess water, prevent fungal growth), waxy leaf coatings, toxin production (tannins, alkaloids to deter herbivores), no seasonal rhythm (grow and shed leaves year-round), and epiphytic growth strategies."),
   ]),
  ("Fauna – Animals",
   "4 marks identifying + 6 SRPs × 2 marks = 15 marks (4-aspect scheme)",
   [
    ("Biodiversity","One hectare contains ~42,000 species — more than any other biome. Species include toucans, parrots, sloths, jaguars, howler monkeys, piranhas, river dolphins, and poison dart frogs. High biodiversity results from consistent warmth, moisture, and diverse food sources."),
    ("Nocturnal Behaviour","Many rainforest animals are nocturnal (e.g. sloths, many frog/bat species), avoiding daytime predators and competition. Some bats and frogs feed on nectar from flowers that have co-evolved to bloom at night, creating specialised nocturnal pollination relationships."),
    ("Camouflage","The Brazilian tree sloth moves so slowly that algae grow on its fur, providing camouflage. Jaguars' patterned coats mimic dappled forest light. Moths and tree frogs resemble leaves — illustrating how the multi-layered, light-varying forest environment has driven camouflage evolution."),
    ("Warning Colouration","Poison dart frogs display vivid blue, red, or yellow colouration (aposematism) — warning predators of their toxicity. This strategy is the opposite of camouflage and is only viable when the cost of predation attempt is high for the predator."),
    ("Physical Adaptations","Howler monkeys and lemurs have prehensile tails functioning as a 5th limb for treetop movement. Jaguars can swim — preying on fish and caimans in flooded forest. The flying fox has wing membranes for gliding between trees, conserving energy."),
    ("Flora-Fauna Interdependence","The Amazon ecosystem depends on plant-animal mutualism. The sword-billed hummingbird's elongated beak accesses Datura flower nectar, pollinating in exchange. Monkeys, bats, and toucans disperse seeds across the forest, maintaining plant diversity across the ecosystem."),
   ]),
]

DESERT_ASPECTS = [
  ("Climate",
   "4 marks identifying + 8 SRPs × 2 marks = 20 marks",
   [
    ("Biome & Location","Hot deserts are found between 15° and 30° north and south of the equator. The North American deserts include the Sonoran (Arizona), Mojave (California), Chihuahuan (Texas) — all hot deserts — and the Great Basin (Nevada/Utah), a cold desert at 40°N."),
    ("High-Pressure Belt","Deserts lie beneath permanent subtropical high-pressure belts where cold air descends, warms, and becomes very dry. Dry north-east trade winds blow over these areas. This year-round high pressure and dry airflow is the fundamental cause of desert aridity."),
    ("Daytime Temperature","Daytime temperatures exceed 30°C in the hot deserts. The high angle of the sun, absence of cloud cover (no reflection of solar radiation), and sparse vegetation (no shade) allow maximum solar radiation to reach and heat the surface."),
    ("Diurnal Temperature Range","The diurnal temperature range exceeds 30°C in hot deserts — the greatest of any biome. Without cloud cover to trap heat, night temperatures drop rapidly, sometimes below 0°C. The Great Basin cold desert reaches sub-zero temperatures regularly in winter."),
    ("Precipitation","Hot deserts receive less than 150mm annually — the Mojave receives approximately 125mm. Rainfall is highly seasonal, occurring in short, violent bursts after prolonged drought. The Great Basin averages 250mm, receiving precipitation year-round as snow in winter."),
    ("California Current","Many deserts lie on the western edges of continents near cold ocean currents. The California Current cools coastal air, reducing its moisture capacity. Rainfall occurs at sea rather than over land, contributing to the aridity of California and Arizona's deserts."),
    ("Rain Shadow Effect","Mountain ranges (Sierra Nevada) intercept moist Pacific air. Moisture falls on the windward side; descending dry air on the leeward side warms and desiccates, creating the rain shadow that intensifies dryness in the desert interior."),
    ("Rapid Run-off & Evaporation","After desert rainfall, water rapidly runs off baked, compacted soil surfaces. High temperatures cause intense evaporation of what little water does infiltrate. Plants benefit minimally from rainfall events — explaining why even small precipitation amounts fail to support dense vegetation."),
   ]),
  ("Soils (Aridisols)",
   "4 marks identifying + 8 SRPs × 2 marks = 20 marks",
   [
    ("Aridisol Definition","Aridisols (from Latin 'dry') are the dry soils of desert and semi-desert regions. They form in areas with very low precipitation and extreme temperatures, are characterised by their light grey colour, and are among the least developed soils on Earth."),
    ("Low Organic Matter","Aridisols contain very little organic matter due to sparse vegetation and low plant productivity. Without organic matter, clearly defined soil horizons do not develop. Micro-organisms (earthworms, fungi) are scarce, so humus formation is minimal — giving aridisols their pale grey colour."),
    ("Calcification","Calcification is the dominant soil-forming process. As water evaporates, dissolved calcium is drawn upward, depositing calcite near the surface over time. This creates a solid calcite-rich hardpan layer called caliche — nearly impermeable, restricting root penetration."),
    ("Caliche Layer","The caliche hardpan within the B horizon is almost impermeable, preventing water infiltration and deep root growth. It contributes to the alkaline nature of desert soils and causes waterlogging of the thin surface soil during the rare intense rainfall events."),
    ("Salinisation","In extremely dry conditions, moisture is drawn to the surface by capillary action. Evaporation leaves crystallised salts on the soil surface, creating saltpans where little to no vegetation survives. Salinisation is worsened by irrigation in arid regions."),
    ("Texture & Parent Material","Aridisol texture ranges from sandy to coarse and gravelly. Deep soils in lowland basins formed from mountain erosion over thousands of years — transported by torrential rainfall and dry winds forming the parent material."),
    ("Alkaline Nature","Intense evaporation concentrates calcium and sodium near the surface, producing alkaline soils. High pH restricts nutrient availability to plants, further limiting plant growth — compounding the effects of low rainfall and high temperature."),
    ("Impact on Flora","Caliche and salinisation force desert plants to develop specialised roots: shallow radial roots (cactus) to capture surface rainfall rapidly, or deep taproots (mesquite: 30ft, elephant tree: 50ft) to penetrate below the caliche layer to reach the water table."),
   ]),
  ("Flora – Vegetation",
   "4 marks identifying + 8 SRPs × 2 marks = 20 marks",
   [
    ("Sparse Vegetation","Sparse vegetation defines North American deserts. Productivity is extremely low — plants are widely spaced to reduce competition. Two main plant categories: succulents (store water; e.g. cacti, Joshua Tree) and ephemerals (short life cycle; e.g. Paper Daisy, Creosote Bush). Ephemerals constitute ~40% of desert plants."),
    ("Succulents – Water Storage","Succulent plants store water in roots, stem tissue, and fruit during wet periods. The cactus stores water in its fleshy, sponge-like interior; ribbed grooves allow expansion. Stem tissue can hold hundreds of litres — a Saguaro cactus can store up to 200 litres after rainfall."),
    ("Cactus Adaptations","The cactus has: thick waxy skin (prevents evaporation, reflects heat); spines replacing leaves (eliminating transpiration, deterring animals); ribbed trunk (expands to store water); shallow radial roots (rapidly absorb surface rainfall). The Saguaro's root system covers an area equal to its height."),
    ("Joshua Tree","The Joshua Tree has a two-way root system: shallow roots (10ft) spread radially to absorb surface rainfall; deep taproot (30ft) accesses sub-surface moisture. A thick waxy skin prevents evaporative water loss. Found exclusively in the Mojave Desert — it is the ecosystem's keystone species."),
    ("Ephemerals – Life Cycle","Ephemerals complete their full lifecycle (germination, growth, flowering, seed production) within weeks following rainfall, then die. Seeds are protected by a waxy coating through years of drought. The Paper Daisy can transform barren desert into a carpet of colour within days of rain — as seen in Australian and American deserts."),
    ("Radial Roots","Radial (shallow lateral) roots spread outward in a radial pattern close to the surface, covering a large area. The cactus's shallow root system captures rainfall immediately before evaporation removes it, maximising water absorption during the brief window after rare rainfall events."),
    ("Deep Taproots","Deep taproots penetrate below the caliche hardpan to the water table. The mesquite plant (30ft taproot) and elephant tree (50ft taproot) can survive extended droughts by accessing deep groundwater unavailable to shallow-rooted competitors."),
    ("Defensive Systems & Salt Tolerance","The creosote bush produces chemical toxins with an unpleasant taste/smell that deter herbivores. Cacti spines protect stored water from animal attack. Many desert plants tolerate toxic salt levels from salinisation by either excreting salt compounds or storing them in specialised tissues."),
   ]),
  ("Fauna – Animals",
   "4 marks identifying + 6 SRPs × 2 marks = 15 marks (4-aspect scheme)",
   [
    ("Small Animal Dominance","Large mammals cannot store sufficient water or regulate body temperature effectively in extreme heat — only small animals (e.g. elf owl, rattlesnake, desert fox, jackrabbit, Gila monster) are generally present. Small body size reduces water requirements and allows easier sheltering from heat."),
    ("Nocturnal & Crepuscular Behaviour","Many desert animals are nocturnal (active at night) or crepuscular (dawn/dusk): elf owl, rattlesnake, desert fox. This avoids peak daytime temperatures (>40°C), minimises water loss through respiration/activity, and enables hunting when cooler prey is active."),
    ("Burrowing & Hibernation","Desert tortoise and desert toad burrow up to 3 feet deep during peak midday heat. Desert squirrels and toads aestivate (summer hibernation) throughout the hottest months. Grasshoppers shelter in the shade of leaves. These behavioural adaptations reduce water loss and thermal stress."),
    ("Physical Adaptations","Desert animals have evolved paler colouring (absorbing less heat, providing camouflage). The Blacktail Jackrabbit and desert Kit fox have large ears — acting as radiators, dissipating excess body heat rapidly by increasing the surface area exposed to cooler air."),
    ("Physiological Adaptations","Reptiles produce concentrated uric acid instead of liquid urine, minimising water loss in excretion. Waterproof scaly skin prevents moisture loss. These physiological adaptations make reptiles (rattlesnakes, Gila monsters, desert tortoises) among the most successful desert animals."),
    ("Energy Conservation","The roadrunner bird runs rather than flies, conserving energy and reducing metabolic heat generation and water loss. Many desert animals lower their metabolic rate during extreme heat. Energy conservation is as important as water conservation for desert survival."),
   ]),
]

# ═══════════════════════════════════════════════════════════════════════════
#  ELECTIVE TOPICS (from handwritten notes)
# ═══════════════════════════════════════════════════════════════════════════
ELECTIVE_TOPICS = [
{"num":"E1","pal":"human",
 "title":"GNP vs HDI – Measuring Economic Development",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("GNP Definition","GNP (Gross National Product) is the total wealth produced by a country's citizens both domestically and abroad, divided by population to give GNP per capita. It is a crude measure of economic development as it only captures monetary output."),
  ("GNP – Excludes MNC Profits","GNP excludes profits repatriated abroad by Multinational Companies (MNCs). This makes Ireland's GNP appear artificially high — the GNP Paradox — as pharmaceutical and tech MNCs (Apple, Google) book large profits in Ireland but repatriate them to the US."),
  ("GNP – Distribution Ignored","GNP does not measure the distribution of wealth within a country. In Ireland, the wealthiest 10% own approximately 33% of total economic wealth, yet GNP treats all citizens equally. A high GNP can mask significant internal inequality."),
  ("GNP – Shadow Economy","GNP fails to account for shadow economies (tax evasion, subsistence farming, illegal activities). In developing nations, informal economic activity can represent a significant proportion of real economic activity — making GNP a serious underestimate."),
  ("GNP – Ireland Example","Ireland's GNP was 58% of the EU average in 1973 when it joined the EU. By 2017, Irish GNP exceeded the EU average by 13% — demonstrating rapid economic development, but also GNP volatility due to MNC activity distorting the figure."),
  ("GNP Maps","GNP maps show global economic patterns — highest GNP in the EU, USA, and Japan; lowest in Sub-Saharan Africa. However they oversimplify by hiding internal inequality, shadow economies, and the distorting effect of MNC profits in small open economies like Ireland."),
  ("HDI Definition","The Human Development Index (HDI) is a composite measure compiled by the UN combining: life expectancy, years of schooling/literacy rate, and GNP per capita. It gives a broader measure of human wellbeing than GNP alone, ranging from 0 to 1."),
  ("HDI Scale","HDI ranges from 0 to 1. Highly developed countries score above 0.8. The world's 28 least developed countries score below 0.55, most located in Sub-Saharan Africa. This highlights persistent global development inequality beyond what GNP alone reveals."),
  ("HDI – Advantage over GNP","HDI captures health and education dimensions of development that GNP ignores. A country may have high GNP but poor health outcomes and low education (e.g. some oil-rich states). HDI reveals this discrepancy, highlighting where long-term investment in human capital is needed."),
  ("HDI – Limitation: Inequality","HDI uses national averages — it does not capture inequality within a country. A country with a high HDI average may contain regions of extreme poverty. The Inequality-Adjusted HDI (IHDI) was developed to address this limitation."),
  ("HDI – Limitation: Security","HDI does not measure political stability, personal security, human rights, or environmental quality — all important aspects of human wellbeing. A country can score relatively high on HDI while experiencing significant political repression or conflict (e.g. some Gulf states)."),
  ("HDI – Limitation: Short-term Change","HDI reflects long-term structural indicators (life expectancy, years of schooling) that change slowly over decades. It cannot capture rapid short-term changes in human welfare from economic crisis, conflict, or natural disaster — a limitation compared to more immediate indicators."),
  ("Sub-Saharan Africa – HDI","The 28 countries with the lowest HDI globally are all in Sub-Saharan Africa, reflecting compound disadvantages: low life expectancy (disease burden, especially HIV/AIDS and malaria), low educational attainment, low incomes, and governance challenges — all captured simultaneously by the HDI."),
  ("GNP vs HDI Comparison","GNP: purely economic, monetary measure; easily distorted by MNCs; ignores health/education; does not measure distribution. HDI: composite measure; captures health, education and income; better reflects human wellbeing; but still uses averages and ignores security/environment. HDI is a more comprehensive but imperfect measure."),
  ("Development Goals","Both GNP and HDI contribute to measuring progress toward the UN Sustainable Development Goals (SDGs) — 17 global goals adopted in 2015 targeting poverty, health, education, inequality, and climate by 2030. HDI more directly tracks SDG 3 (Health), SDG 4 (Education) and SDG 10 (Inequality) than GNP alone."),
]},

{"num":"E2","pal":"human",
 "title":"Colonialism and the Developing Economy – India",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Context – British Colonisation","India was colonised by the British East India Company from the mid-1700s, headquartered in Kolkata. Britain maintained control of India until independence in 1947 — approximately 200 years of colonial rule that fundamentally restructured India's economy."),
  ("Commercialisation of Agriculture","The British introduced commercial plantation agriculture on the best Indian agricultural land — growing cotton, coffee, tea, indigo, and sugar for export. Local subsistence food farming was displaced, reducing food security for Indian farmers."),
  ("Food Insecurity & Famine","With the best land devoted to export cash crops and farmers left with little land for food production, food insecurity became widespread. Multiple devastating famines occurred under British rule — the 1943 Bengal Famine killed approximately 2–3 million people — worsened by British wartime food export policies."),
  ("Deindustrialisation","India's share of global GDP declined from approximately 27% pre-colonially to below 3% by 1947. Britain deliberately deindustrialised India by destroying local industries to create dependence on imported British manufactured goods — dismantling India's advanced textile, iron, and steel industries."),
  ("Destruction of Textile Industry","India was once the world's leading producer of fine cotton and silk textiles. Under British rule, local cottage industries were systematically destroyed — raw cotton was exported cheaply to British mills, processed into cloth, and the finished goods sold back to India at a profit."),
  ("Mercantilism","Britain operated a strict mercantilist policy — India was used as a source of cheap raw materials (cotton, jute, indigo, iron ore) and as a captive market for British manufactured goods. Indians were not permitted to trade directly with other nations outside the British Empire."),
  ("Railways – Infrastructure","A major railway network (~67,000km) was built across India — the world's largest at the time. However, it was British-owned and designed primarily to transport raw materials from the interior to ports for export, not to develop India's economy. It primarily served British commercial interests."),
  ("Taxation & Poverty","The British imposed heavy land taxes (zamindari system) on Indian farmers, regardless of harvest success or market prices. Tax collection was enforced even during famines, driving millions into debt and poverty. Revenues were remitted to Britain rather than reinvested in India."),
  ("Trade Restrictions","Indians were not allowed to export finished goods or trade independently with other powers. Indian merchants were excluded from the most profitable trade routes and sectors, permanently limiting the development of an Indian merchant class and domestic industrial capital."),
  ("Impact on Iron & Steel","India had a sophisticated iron and steel industry pre-colonially. Under British rule, iron and steel production collapsed as British industrialists took over remaining production and cheap British steel flooded the Indian market, making local production uncompetitive."),
  ("Independence & Legacy","When India gained independence in 1947, it inherited a fundamentally underdeveloped economy — low industrialisation, poor infrastructure (except railways), widespread poverty, low literacy, and dependence on agriculture. Colonial extraction had prevented India from accumulating the capital needed for development."),
  ("Post-Colonial Recovery","Since independence, India has pursued policies of import substitution industrialisation, green revolution agriculture, and IT services development — growing to become the world's 5th largest economy by 2024 (GDP ~$3.7 trillion). However, significant poverty and inequality persist as legacies of colonial underdevelopment."),
  ("Cultural Impact","British colonialism imposed English language, education, and legal systems on India. While English has become a unifying language and IT advantage, colonial education was designed to produce clerical workers serving British administration rather than engineers or scientists needed for industrial development."),
  ("Evaluation of Colonialism","Colonial apologists cite railway infrastructure, legal system, and English language as benefits. Critics counter that these served British interests primarily, and that the immense economic extraction — estimated at $45 trillion by economist Utsa Patnaik — vastly outweighed any infrastructure investment."),
  ("Comparison – Pre/Post Colonial India","Pre-colonial India: 27% of global GDP, advanced textile/metallurgical industries, extensive trade networks. Under colonialism: deindustrialisation, famine, poverty, dependency. Post-independence: gradual recovery, IT boom, space programme. The contrast illustrates the profound and lasting economic impact of 200 years of colonial extraction."),
]},

{"num":"E3","pal":"human",
 "title":"Footloose Industries – Ireland and MNCs",
 "marks":"30-mark question → 15 SRPs × 2 marks",
 "srps":[
  ("Footloose Industry Definition","Footloose industries are those not tied to raw materials, energy sources, or markets — they can locate almost anywhere based on cost and business environment factors. High-tech industries (pharmaceuticals, ICT), financial services, and data centres are examples of footloose industries attracted to Ireland."),
  ("EU Membership – 1973","Ireland joined the EU in 1973 as one of its poorest members — GNP at 58% of EU average. EU membership provided access to EU structural funds for infrastructure development and, crucially, access to the single market — giving MNCs based in Ireland tariff-free access to 450 million EU consumers."),
  ("Low Corporate Tax – 12.5%","Ireland's 12.5% corporate tax rate — among the lowest in the EU — is a fundamental driver of MNC investment. Introduced in the 1980s, it has attracted hundreds of US technology and pharmaceutical companies. Companies booking EU profits in Ireland benefit from significantly lower tax than in their home countries."),
  ("IDA Ireland","The Industrial Development Authority (IDA) was established to actively market Ireland to potential foreign investors. It provides financial incentives (grants, tax relief), site assistance, and aftercare services. IDA Ireland attracted companies including Apple, Google, Facebook, Intel, Pfizer, and Boston Scientific."),
  ("Infrastructure Investment","EU structural funds financed major infrastructure upgrades: motorway network, ports, airports, broadband, and energy infrastructure. These improvements reduced business costs and increased Ireland's attractiveness as a European base for US MNCs needing efficient logistics and communications."),
  ("Skilled Labour Force","Ireland has the highest proportion of third-level graduates in the EU — approximately 55% of 25–64 year olds have a third-level qualification compared to an EU average of 35%. Universities (TCD, UCD, UCC, NUI Galway) produce graduates in science, engineering, and business demanded by MNCs."),
  ("English Language","Ireland is the only English-speaking country in the Eurozone. This provides US MNCs with seamless communication between US headquarters and their European operations, eliminating language barriers in management, legal, financial, and technical operations."),
  ("Intel – Leixlip","Intel's Leixlip (Co. Kildare) facility is Europe's most advanced semiconductor manufacturing plant, employing approximately 5,000 people directly. Intel has invested over $30 billion in Ireland since establishing in 1989 — demonstrating long-term MNC commitment to Ireland as a manufacturing location."),
  ("Pfizer – Ringaskiddy","Pfizer in Ringaskiddy (Co. Cork) is one of the world's largest pharmaceutical manufacturing sites, producing approximately 40% of Pfizer's global output including key medicines. Ireland manufactures approximately 80 of the world's 100 best-selling medicines, generating massive export revenue."),
  ("Boston Scientific – Galway","Boston Scientific employs approximately 6,000 people across multiple Galway sites — one of its largest global manufacturing locations. Medical devices manufactured in Galway are exported globally, demonstrating Ireland's specialisation in high-value, knowledge-intensive manufacturing."),
  ("Export Performance","Ireland is the world's 5th largest pharmaceutical exporter and 8th largest exporter of ICT services. Exports reached €567 billion in 2022 — approximately twice Ireland's GNP — largely driven by MNC activity. This makes Ireland's economy highly open and export-oriented."),
  ("Criticism – Tax Avoidance","Ireland's tax structure has attracted criticism from EU partners and the US. The 2016 EU Commission ruling that Apple received illegal state aid (a tax deal worth €13 billion) highlighted tensions between Ireland's competitive tax policy and EU state aid rules. The OECD's global minimum 15% corporate tax rate (2021) has significant implications for Ireland's model."),
  ("Regional Concentration","MNC investment in Ireland is heavily concentrated in Dublin and Cork, creating regional imbalance. Efforts to attract MNCs to the west (IDA's regional strategy) have had limited success. Over 70% of IDA-supported jobs are in the Dublin and Cork regions."),
  ("Cluster Effects","MNC concentration creates cluster effects — related industries, suppliers, and services develop around established MNCs. The ICT cluster in Dublin's 'Silicon Docks' (Google, Facebook, Twitter, LinkedIn) and the pharmaceutical cluster in Cork create self-reinforcing competitive advantages."),
  ("Skills Development","MNC presence has raised skill levels in the Irish workforce through on-the-job training, knowledge transfer, and R&D activity. Ireland's shift from low-skill manufacturing (1960s–70s) to high-skill technology and pharmaceutical production reflects how MNC investment has upgraded the economy's human capital over 50 years."),
]},
]

# ═══════════════════════════════════════════════════════════════════════════
#  BUILD PDF
# ═══════════════════════════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=1.8*cm, leftMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

story = []

# ── MASTER COVER PAGE ────────────────────────────────────────────────────
cover_bg = hx("#1a237e")
cover_acc = hx("#3949ab")
def_s = ParagraphStyle('DC',fontName='Helvetica-Bold',fontSize=28,textColor=colors.white,leading=32)
sub_s = ParagraphStyle('DS',fontName='Helvetica',fontSize=12,textColor=colors.Color(1,1,1,.85),leading=16)
note_s = ParagraphStyle('DN',fontName='Helvetica-Oblique',fontSize=9,textColor=colors.Color(1,1,1,.75),leading=12)

cover_rows = [
    [Paragraph("Leaving Certificate Geography", def_s)],
    [Spacer(1,6)],
    [Paragraph("Complete SRP Study Guide", ParagraphStyle('DS2',fontName='Helvetica-Bold',fontSize=18,textColor=colors.Color(1,1,1,.9),leading=22))],
    [Spacer(1,8)],
    [Paragraph("18 Physical Geography Topics + 3 Elective Topics + Geoecology 80-Mark Essays", sub_s)],
    [Spacer(1,4)],
    [Paragraph("Each 30-mark topic: 15 SRPs × 2 marks = 30 marks", sub_s)],
    [Paragraph("Each Geoecology aspect: 4 marks identifying + 8 SRPs × 2 marks + 20 marks OC = 80 marks", sub_s)],
    [Spacer(1,8)],
    [Paragraph("Exam Date: Friday 5th June 2026  |  Total Marks: 400  |  Duration: 2hr 50min", note_s)],
]
cover_t = Table(cover_rows, colWidths=[W])
cover_t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),cover_bg),
    ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
    ('LEFTPADDING',(0,0),(-1,-1),20),('RIGHTPADDING',(0,0),(-1,-1),20),
    ('ROUNDEDCORNERS',[8,8,8,8]),
]))
story.append(cover_t)
story.append(Spacer(1,10))

# Contents note
cnt_s = ParagraphStyle('cnt',fontName='Helvetica',fontSize=9,textColor=colors.HexColor('#333333'),leading=13)
sections = [
    "PHYSICAL GEOGRAPHY (Topics 01–18):",
    "01 Plate Tectonic Theory  |  02 Constructive Boundaries  |  03 Destructive Boundaries",
    "04 Volcanic Activity  |  05 Earthquakes – Prediction & Effects  |  06 Global Distribution",
    "07 Tectonic Activity – Irish Landscape  |  08 Igneous Rocks  |  09 Sedimentary Rocks",
    "10 Metamorphic Rocks  |  11 Rock Types & Landscapes  |  12 Human Interaction & Rock Cycle",
    "13 Mechanical Weathering  |  14 Chemical Weathering  |  15 Waterfall (Fluvial Erosion)",
    "16 Delta (Fluvial Deposition)  |  17 Aswan Dam – Human Impact  |  18 Isostatic Processes",
    "",
    "ELECTIVE TOPICS (E1–E3):",
    "E1 GNP vs HDI  |  E2 Colonialism – India  |  E3 Footloose Industries – Ireland",
    "",
    "GEOECOLOGY – 80-MARK ESSAYS:",
    "Amazon Rainforest: Climate | Soils | Flora | Fauna",
    "Hot Desert Biome: Climate | Soils | Flora | Fauna",
]
for line in sections:
    story.append(Paragraph(safe(line), cnt_s))
    story.append(Spacer(1,1))

# ── PHYSICAL TOPICS ──────────────────────────────────────────────────────
for topic in TOPICS:
    story.append(PageBreak())
    topic_header(story, topic["pal"], topic["num"], topic["title"], topic["marks"])
    total = len(topic["srps"])
    for i,(label,text) in enumerate(topic["srps"],1):
        srp_card(story, topic["pal"], i, label, text, total)

# ── ELECTIVE TOPICS ──────────────────────────────────────────────────────
for topic in ELECTIVE_TOPICS:
    story.append(PageBreak())
    topic_header(story, topic["pal"], topic["num"], topic["title"], topic["marks"])
    total = len(topic["srps"])
    for i,(label,text) in enumerate(topic["srps"],1):
        srp_card(story, topic["pal"], i, label, text, total)

# ── GEOECOLOGY – AMAZON RAINFOREST ───────────────────────────────────────
story.append(PageBreak())
cover_biome(story, "rainforest",
    "Amazon Rainforest – Geoecology 80-Mark Essay",
    "Option 7 | Questions 16, 17, 18 | 80 Marks | 35 Minutes",
    "Structure: 3 aspects × 20 marks each + 20 marks Overall Coherence",
    [
        "Each aspect: 4 marks (identifying) + 8 × SRPs @ 2 marks = 20 marks",
        "Overall Coherence: graded 0/6/10/14/17/20 marks",
        "Allow up to 3 named examples (max 3 SRPs) across different aspects",
        "Allow up to 2 labelled diagrams (max 2 SRPs) in different aspects",
        "4-aspect option: 4 aspects × 15 marks each (3 marks + 6 SRPs) + 20 OC",
    ])

for asp_title, asp_marks, asp_srps in RAINFOREST_ASPECTS:
    story.append(PageBreak())
    geoecology_aspect_header(story, "rainforest", asp_title, asp_marks)
    for i,(label,text) in enumerate(asp_srps, 1):
        srp_card(story, "rainforest", i, label, text, len(asp_srps))

# ── GEOECOLOGY – HOT DESERT ──────────────────────────────────────────────
story.append(PageBreak())
cover_biome(story, "desert",
    "Hot Desert Biome – Geoecology 80-Mark Essay",
    "North American Deserts | Option 7 | Questions 16, 17, 18 | 80 Marks | 35 Minutes",
    "Structure: 3 aspects × 20 marks each + 20 marks Overall Coherence",
    [
        "Each aspect: 4 marks (identifying) + 8 × SRPs @ 2 marks = 20 marks",
        "Overall Coherence: graded 0/6/10/14/17/20 marks",
        "North American Deserts: Sonoran (AZ), Mojave (CA), Chihuahuan (TX), Great Basin (NV/UT)",
        "Allow up to 3 named examples (max 3 SRPs) across different aspects",
        "Allow up to 2 labelled diagrams (max 2 SRPs) in different aspects",
    ])

for asp_title, asp_marks, asp_srps in DESERT_ASPECTS:
    story.append(PageBreak())
    geoecology_aspect_header(story, "desert", asp_title, asp_marks)
    for i,(label,text) in enumerate(asp_srps, 1):
        srp_card(story, "desert", i, label, text, len(asp_srps))

doc.build(story)
print(f"Done → {OUTPUT}")
