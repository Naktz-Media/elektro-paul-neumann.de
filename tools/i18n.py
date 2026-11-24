"""UI strings written for the new site, in English, with (German, Spanish) translations.
Content from the old site (services, projects, FAQ, imprint) comes from tools/source-<lang>.json instead.
Keys must match the visible text exactly (whitespace-trimmed). RULES handle repeating patterns."""
import re

TR = {
    # navigation / chrome
    "Home": ("Start", "Inicio"),
    "Services": ("Leistungen", "Servicios"),
    "Projects": ("Projekte", "Proyectos"),
    "Careers": ("Karriere", "Empleo"),
    "Contact": ("Kontakt", "Contacto"),
    "Let’s talk": ("Kontakt aufnehmen", "Hablemos"),
    "Menu": ("Menü", "Menú"),
    "Main": ("Hauptmenü", "Menú principal"),
    "Mobile": ("Mobiles Menü", "Menú móvil"),
    "Language": ("Sprache", "Idioma"),
    "Appearance": ("Darstellung", "Apariencia"),
    "Dark": ("Dunkel", "Oscuro"),
    "Hybrid": ("Hybrid", "Híbrido"),
    "Light": ("Hell", "Claro"),
    "Skip to content": ("Zum Inhalt springen", "Saltar al contenido"),
    "Breadcrumb": ("Brotkrümelnavigation", "Ruta de navegación"),
    "Quick contact": ("Schnellkontakt", "Contacto rápido"),
    "Call": ("Anrufen", "Llamar"),
    "Email": ("E-Mail", "Correo"),
    "Call +49 (0) 221 - 431 351": ("Anrufen: +49 (0) 221 - 431 351", "Llamar al +49 (0) 221 - 431 351"),
    "Elektro Paul Neumann – Smart Buildings, home": ("Elektro Paul Neumann – Smart Buildings, Startseite", "Elektro Paul Neumann – Smart Buildings, inicio"),
    "Image viewer": ("Bildbetrachter", "Visor de imágenes"),
    "Close": ("Schließen", "Cerrar"),
    "Previous image": ("Vorheriges Bild", "Imagen anterior"),
    "Next image": ("Nächstes Bild", "Imagen siguiente"),
    "14 reference projects": ("14 Referenzprojekte", "14 proyectos de referencia"),
    "From villas on Mallorca to stadiums and studios →": ("Von Villen auf Mallorca bis zu Stadien und Studios →", "De villas en Mallorca a estadios y estudios →"),
    # footer
    "Electrical, KNX and security technology in Cologne and on Mallorca. Planning, installation and maintenance – since 1980.":
        ("Elektro-, KNX- und Sicherheitstechnik in Köln und auf Mallorca. Planung, Installation und Wartung – seit 1980.",
         "Tecnología eléctrica, KNX y de seguridad en Colonia y Mallorca. Planificación, instalación y mantenimiento – desde 1980."),
    "Request consultation": ("Beratung anfragen", "Solicitar asesoramiento"),
    "Cologne": ("Köln", "Colonia"),
    "Mallorca": ("Mallorca", "Mallorca"),
    "Illes Balears, Spain": ("Illes Balears, Spanien", "Illes Balears, España"),
    "Company": ("Unternehmen", "Empresa"),
    "Imprint & privacy": ("Impressum & Datenschutz", "Aviso legal y privacidad"),
    "Imprint": ("Impressum", "Aviso legal"),
    "Privacy": ("Datenschutz", "Privacidad"),
    "Back to top ↑": ("Nach oben ↑", "Volver arriba ↑"),
    "© Elektro Paul Neumann · Dirk Woronow · Since 1980": ("© Elektro Paul Neumann · Dirk Woronow · Seit 1980", "© Elektro Paul Neumann · Dirk Woronow · Desde 1980"),
    "Designed by": ("Design von", "Diseño de"),
    # CTA
    "Get in touch": ("Kontakt", "Contacto"),
    "Let’s talk.": ("Sprechen wir.", "Hablemos."),
    "From the first consultation to the final installation – in Cologne, throughout Germany and on Mallorca.":
        ("Von der ersten Beratung bis zur fertigen Installation – in Köln, deutschlandweit und auf Mallorca.",
         "Desde la primera consulta hasta la instalación final – en Colonia, en toda Alemania y en Mallorca."),
    "Your project next?": ("Ihr Projekt als Nächstes?", "¿Su proyecto, el próximo?"),
    # home – hero
    "Paul Neumann Smart Buildings · Cologne & Mallorca": ("Paul Neumann Smart Buildings · Köln & Mallorca", "Paul Neumann Smart Buildings · Colonia y Mallorca"),
    "Intelligent building technology. Perfectly planned. Precisely implemented.":
        ("Intelligente Gebäudetechnik. Perfekt geplant. Präzise umgesetzt.", "Tecnología de edificios inteligente. Perfectamente planificada. Ejecutada con precisión."),
    "Intelligent": ("Intelligente", "Inteligente"),
    "Secure": ("Sichere", "Segura"),
    "Connected": ("Vernetzte", "Conectada"),
    "Efficient": ("Effiziente", "Eficiente"),
    "building": ("Gebäude-", "Tecnología"),
    "technology.": ("technik.", "de edificios."),
    "Perfectly planned. Precisely implemented. Your partner for electrical installations, smart home, KNX building automation, lighting and security technology – since 1980.":
        ("Perfekt geplant. Präzise umgesetzt. Ihr Partner für Elektroinstallationen, Smart Home, KNX Gebäudeautomation, Beleuchtung und Sicherheitstechnik – seit 1980.",
         "Perfectamente planificada. Ejecutada con precisión. Su socio para instalaciones eléctricas, casa inteligente, automatización KNX, iluminación y seguridad – desde 1980."),
    "Explore services": ("Leistungen entdecken", "Ver servicios"),
    "Try a scene": ("Szene testen", "Probar una escena"),
    # home – intro
    "Your partner for": ("Ihr Partner für", "Su socio para"),
    "Smart solutions for electrical & security technology.": ("Smarte Lösungen für Elektro- & Sicherheitstechnik.", "Soluciones inteligentes en tecnología eléctrica y de seguridad."),
    "In Cologne and Mallorca – for high-quality residential and commercial projects, from planning to installation. Since 1980.":
        ("In Köln und auf Mallorca – für hochwertige Projekte im privaten und gewerblichen Bereich, von der Planung bis zur Installation. Seit 1980.",
         "En Colonia y Mallorca – para proyectos residenciales y comerciales de alta calidad, desde la planificación hasta la instalación. Desde 1980."),
    "Certified": ("Zertifizierter", "Partner"),
    "KNX partner": ("KNX-Partner", "KNX certificado"),
    "Since": ("Seit", "Desde"),
    "& Mallorca": ("& Mallorca", "y Mallorca"),
    # home – scenes
    "KNX building automation": ("KNX Gebäudeautomation", "Automatización KNX"),
    "One touch.": ("Ein Tippen.", "Un toque."),
    "Every system.": ("Jedes System.", "Todos los sistemas."),
    "Light, heating, blinds, ventilation and security – centrally controlled, automated and adapted to your life. Try it: tap a scene.":
        ("Licht, Heizung, Jalousien, Lüftung und Sicherheit – zentral gesteuert, automatisiert und an Ihr Leben angepasst. Probieren Sie es aus: Tippen Sie auf eine Szene.",
         "Luz, calefacción, persianas, ventilación y seguridad – control central, automatizado y adaptado a su vida. Pruébelo: toque una escena."),
    "Living room": ("Wohnzimmer", "Salón"),
    "Live demo": ("Live-Demo", "Demo en vivo"),
    "Lighting scenes": ("Lichtszenen", "Escenas de luz"),
    "Day": ("Tag", "Día"), "Evening": ("Abend", "Tarde"), "Cinema": ("Kino", "Cine"), "Away": ("Abwesend", "Ausente"),
    "Daylight mode": ("Tageslicht-Modus", "Modo luz de día"),
    "Blinds open, lights off – the building uses the sun.": ("Jalousien offen, Licht aus – das Gebäude nutzt die Sonne.", "Persianas abiertas, luces apagadas – el edificio aprovecha el sol."),
    "Evening scene": ("Abendszene", "Escena de tarde"),
    "Warm light at 60 %, blinds half down, music on low.": ("Warmes Licht auf 60 %, Jalousien halb unten, leise Musik.", "Luz cálida al 60 %, persianas a media altura, música suave."),
    "Cinema scene": ("Kinoszene", "Escena de cine"),
    "Blinds closed, accent light only, sound up.": ("Jalousien zu, nur Akzentlicht, Ton laut.", "Persianas cerradas, solo luz de acento, sonido alto."),
    "Away mode": ("Abwesend-Modus", "Modo ausente"),
    "Everything off, heating lowered, alarm armed.": ("Alles aus, Heizung abgesenkt, Alarm scharf.", "Todo apagado, calefacción reducida, alarma activada."),
    "Blinds open": ("Jalousien offen", "Persianas abiertas"), "Audio": ("Audio", "Audio"), "Temperature": ("Temperatur", "Temperatura"),
    "Lighting": ("Licht", "Iluminación"), "Scenes, schedules and presence control": ("Szenen, Zeitpläne und Präsenzsteuerung", "Escenas, horarios y control de presencia"),
    "Shading": ("Beschattung", "Sombreado"), "Blinds and shutters that follow the sun": ("Jalousien und Rollläden, die der Sonne folgen", "Persianas que siguen al sol"),
    "Climate": ("Klima", "Clima"), "Room-by-room heating for real savings": ("Einzelraumregelung für echte Einsparungen", "Calefacción por estancias para ahorrar de verdad"),
    "Security": ("Sicherheit", "Seguridad"), "Alarm, video and status messages on your phone": ("Alarm, Video und Statusmeldungen auf dem Smartphone", "Alarma, vídeo y avisos en su móvil"),
    # home – services / counters
    "Our services": ("Unsere Leistungen", "Nuestros servicios"),
    "Every project": ("Jedes Projekt", "Cada proyecto"),
    "is unique.": ("ist einzigartig.", "es único."),
    "All services": ("Alle Leistungen", "Todos los servicios"),
    "Electricians in Cologne since": ("Elektriker in Köln seit", "Electricistas en Colonia desde"),
    "Reference projects – villas, stadiums, studios": ("Referenzprojekte – Villen, Stadien, Studios", "Proyectos de referencia – villas, estadios, estudios"),
    "Disciplines from a single source": ("Gewerke aus einer Hand", "Especialidades en una sola empresa"),
    "Locations with own teams – Cologne & Mallorca": ("Standorte mit eigenen Teams – Köln & Mallorca", "Sedes con equipos propios – Colonia y Mallorca"),
    "Work we’re proud of.": ("Projekte, auf die wir stolz sind.", "Proyectos de los que estamos orgullosos."),
    "All 14 projects": ("Alle 14 Projekte", "Los 14 proyectos"),
    "Residential": ("Privat", "Residencial"), "Commercial": ("Gewerbe", "Comercial"),
    # home – security split
    "Tailor-made solutions – from experts in Cologne": ("Maßgeschneiderte Lösungen – von Experten aus Köln", "Soluciones a medida – de expertos en Colonia"),
    "Security technology for the highest demands.": ("Sicherheitstechnik für höchste Ansprüche.", "Tecnología de seguridad para las máximas exigencias."),
    "Since 1980, we have been offering customized security solutions for your home and industry. From smart home installations to alarm systems – everything from a single source.":
        ("Seit 1980 bieten wir individuelle Sicherheitskonzepte für Ihr Zuhause und in der Industrie. Von Smart-Home-Installationen bis Alarmanlagen – alles aus einer Hand.",
         "Desde 1980 ofrecemos soluciones de seguridad a medida para su hogar y la industria. De la casa inteligente a los sistemas de alarma – todo en una sola empresa."),
    "With high-quality branded products and personal service, we accompany you from the initial consultation to the final installation – whether in your city apartment, holiday home or business.":
        ("Mit hochwertigen Markenprodukten und persönlichem Service begleiten wir Sie von der ersten Beratung bis zur finalen Installation – ob in der Stadtwohnung, im Ferienhaus oder im Betrieb.",
         "Con productos de primeras marcas y un servicio personal le acompañamos desde la primera consulta hasta la instalación final – en su piso, su casa de vacaciones o su empresa."),
    "Woman using a wall-mounted smart building touch panel": ("Frau bedient ein Touch-Panel der Gebäudesteuerung", "Mujer usando un panel táctil de domótica"),
    # home – process
    "How we work": ("So arbeiten wir", "Cómo trabajamos"),
    "Idea. Conception.": ("Idee. Konzeption.", "Idea. Concepción."),
    "Implementation.": ("Umsetzung.", "Ejecución."),
    "01 — Idea": ("01 — Idee", "01 — Idea"), "02 — Conception": ("02 — Konzeption", "02 — Concepción"), "03 — Implementation": ("03 — Umsetzung", "03 — Ejecución"),
    "We listen.": ("Wir hören zu.", "Escuchamos."), "We plan.": ("Wir planen.", "Planificamos."), "We deliver.": ("Wir setzen um.", "Ejecutamos."), "You tell us.": ("Sie erzählen.", "Usted nos cuenta."),
    "We look at your property on site and understand what you want to achieve.": ("Wir besichtigen Ihr Objekt vor Ort und verstehen, was Sie erreichen möchten.", "Visitamos su inmueble y entendemos lo que quiere conseguir."),
    "System design and a binding quote with a detailed description of the work.": ("Systemplanung und ein verbindliches Angebot mit genauer Leistungsbeschreibung.", "Diseño del sistema y un presupuesto vinculante con descripción detallada."),
    "Professional installation, commissioning, handover – and long-term service.": ("Fachgerechte Installation, Inbetriebnahme, Übergabe – und langfristiger Service.", "Instalación profesional, puesta en marcha, entrega – y servicio a largo plazo."),
    # home – locations
    "For you": ("Für Sie", "Para usted"),
    "Two locations.": ("Zwei Betriebsstätten.", "Dos sedes."),
    "Two teams.": ("Zwei Teams.", "Dos equipos."),
    "Due to many successful projects in industry and private homes, inquiries from Mallorca followed – today we serve both with our own teams.":
        ("Aufgrund vieler erfolgreicher Projekte in Industrie und Privatbereich kamen Anfragen aus Mallorca – heute betreuen wir beide Standorte mit eigenen Teams.",
         "Gracias a numerosos proyectos en la industria y en viviendas llegaron solicitudes desde Mallorca – hoy atendemos ambas sedes con equipos propios."),
    "Since 1980": ("Seit 1980", "Desde 1980"), "Since 2017": ("Seit 2017", "Desde 2017"),
    "Sophisticated electrical and security technology in the city and the surrounding area – specializing in planning, KNX integration and excellent execution. Managed since 2010 by master electrician Dirk Woronow.":
        ("Anspruchsvolle Elektro- und Sicherheitstechnik in Stadt und Umland – spezialisiert auf Planung, KNX-Integration und exzellente Ausführung. Seit 2010 geführt von Elektromeister Dirk Woronow.",
         "Tecnología eléctrica y de seguridad exigente en la ciudad y sus alrededores – especializados en planificación, integración KNX y ejecución impecable. Dirigida desde 2010 por el maestro electricista Dirk Woronow."),
    "Active on the island since 2017, with our own office and team since 2022: KNX planning and integration, smart home, video, alarm, multi-room audio and media systems.":
        ("Seit 2017 auf der Insel tätig, seit 2022 mit eigener Betriebsstätte und eigenem Team: KNX Planung und Integration, Smart Home, Video, Alarm, Multiroom-Audio und Mediensysteme.",
         "Activos en la isla desde 2017, con oficina y equipo propios desde 2022: planificación e integración KNX, casa inteligente, vídeo, alarma, audio multiroom y sistemas multimedia."),
    "Route between Cologne and Mallorca, about 1,320 kilometres": ("Strecke Köln – Mallorca, rund 1.320 Kilometer", "Ruta entre Colonia y Mallorca, unos 1.320 kilómetros"),
    "Mallorca office": ("Büro Mallorca", "Oficina Mallorca"), "Headquarters": ("Hauptsitz", "Sede central"),
    "≈ 1,320 km · one team standard": ("≈ 1.320 km · ein Qualitätsstandard", "≈ 1.320 km · un mismo estándar"),
    "Electricians in Cologne": ("Elektriker in Köln", "Electricistas en Colonia"),
    "Takeover by master electrician Dirk Woronow": ("Übernahme durch Elektromeister Dirk Woronow", "Relevo por el maestro electricista Dirk Woronow"),
    "First major projects on Mallorca": ("Erste Großprojekte auf Mallorca", "Primeros grandes proyectos en Mallorca"),
    "Own office and team on Mallorca": ("Eigene Betriebsstätte und Team auf Mallorca", "Oficina y equipo propios en Mallorca"),
    "Branded products we install": ("Markenprodukte, die wir installieren", "Marcas que instalamos"),
    # services overview / detail
    "Everything for intelligent buildings.": ("Alles für intelligente Gebäude.", "Todo para edificios inteligentes."),
    "From a single source.": ("Aus einer Hand.", "En una sola empresa."),
    "Planning, installation and maintenance of electrical, KNX, lighting, security and media technology for private homes, businesses and industry.":
        ("Planung, Installation und Wartung von Elektro-, KNX-, Licht-, Sicherheits- und Medientechnik für Privathaushalte, Unternehmen und Industrie.",
         "Planificación, instalación y mantenimiento de tecnología eléctrica, KNX, iluminación, seguridad y multimedia para hogares, empresas e industria."),
    "Services – Elektro Paul Neumann, Electrician Cologne & Mallorca": ("Leistungen – Elektro Paul Neumann, Elektriker Köln & Mallorca", "Servicios – Elektro Paul Neumann, electricista en Colonia y Mallorca"),
    "KNX system integration, smart home, lighting, alarm systems, video surveillance, video intercoms, multi-room audio and electrical service in Cologne and Mallorca.":
        ("KNX Systemintegration, Smart Home, Beleuchtung, Alarmanlagen, Videoüberwachung, Video-Gegensprechanlagen, Multiroom-Audio und Elektroservice in Köln und auf Mallorca.",
         "Integración KNX, casa inteligente, iluminación, alarmas, videovigilancia, videoporteros, audio multiroom y servicio eléctrico en Colonia y Mallorca."),
    "Get advice": ("Beraten lassen", "Asesorarse"),
    "Frequently asked questions": ("Häufige Fragen", "Preguntas frecuentes"),
    "FAQ": ("FAQ", "Preguntas"),
    "In our projects": ("In unseren Projekten", "En nuestros proyectos"),
    "Gallery": ("Galerie", "Galería"),
    "Additional services": ("Weitere Leistungen", "Más servicios"),
    "Everything from a single source.": ("Alles aus einer Hand.", "Todo en una sola empresa."),
    "To protect your data, the YouTube video only loads after you click. By playing it you agree to a connection to YouTube (privacy-enhanced mode).":
        ("Zum Schutz Ihrer Daten wird das YouTube-Video erst nach Ihrem Klick geladen. Mit dem Abspielen stimmen Sie einer Verbindung zu YouTube zu (erweiterter Datenschutzmodus).",
         "Para proteger sus datos, el vídeo de YouTube solo se carga tras su clic. Al reproducirlo acepta una conexión con YouTube (modo de privacidad mejorada)."),
    # service names + taglines
    "Lighting systems": ("Beleuchtungssysteme", "Sistemas de iluminación"),
    "KNX system integration": ("KNX Systemintegration", "Integración de sistemas KNX"),
    "Alarm systems": ("Alarmanlagen", "Sistemas de alarma"),
    "Smart Home": ("Smart Home", "Casa inteligente"),
    "Video surveillance": ("Videoüberwachung", "Videovigilancia"),
    "Video intercom systems": ("Video-Gegensprechanlagen", "Videoporteros"),
    "Multi-room audio": ("Multiroom-Audio", "Audio multiroom"),
    "Electrical service": ("Service-Elektriker", "Servicio eléctrico"),
    "Lighting design at the highest level": ("Lichtgestaltung auf höchstem Niveau", "Diseño de iluminación al más alto nivel"),
    "Intelligent building technology with high standards": ("Intelligente Gebäudetechnik mit Anspruch", "Tecnología de edificios inteligente y exigente"),
    "Your protection starts with the right alarm system": ("Ihr Schutz beginnt mit der richtigen Alarmanlage", "Su protección empieza con la alarma adecuada"),
    "Comfort, security and efficiency – controlled from anywhere": ("Komfort, Sicherheit und Effizienz – von überall gesteuert", "Confort, seguridad y eficiencia – controlados desde cualquier lugar"),
    "Your protection starts with a clear picture": ("Ihr Schutz beginnt mit einem klaren Bild", "Su protección empieza con una imagen nítida"),
    "More safety through visual control": ("Mehr Sicherheit durch visuelle Kontrolle", "Más seguridad gracias al control visual"),
    "Sound comfort in every room": ("Klangkomfort in jedem Raum", "Confort sonoro en cada estancia"),
    "Tailor-made electrical support for every project": ("Maßgeschneiderter Elektrosupport für jedes Projekt", "Soporte eléctrico a medida para cada proyecto"),
    # projects
    "Villas, stadiums, studios": ("Villen, Stadien, Studios", "Villas, estadios, estudios"),
    "& headquarters.": ("& Firmenzentralen.", "y sedes corporativas."),
    "A selection of our projects around Cologne and Mallorca – electrical engineering, KNX, security, lighting, network and media technology.":
        ("Eine Auswahl unserer Projekte rund um Köln und Mallorca – Elektrotechnik, KNX, Sicherheits-, Licht-, Netzwerk- und Medientechnik.",
         "Una selección de nuestros proyectos en Colonia y Mallorca – electricidad, KNX, seguridad, iluminación, redes y multimedia."),
    "Projects – Elektro Paul Neumann, Electrician Cologne | KNX & Security Technology": ("Projekte – Elektro Paul Neumann, Elektriker Köln | KNX & Sicherheitstechnik", "Proyectos – Elektro Paul Neumann, electricista en Colonia | KNX y seguridad"),
    "A selection of our projects around Cologne and Mallorca: villas, penthouses, Bayer 04 Leverkusen, WDR, TÜV Rheinland, hotels and offices.":
        ("Eine Auswahl unserer Projekte rund um Köln und Mallorca: Villen, Penthouses, Bayer 04 Leverkusen, WDR, TÜV Rheinland, Hotels und Büros.",
         "Una selección de nuestros proyectos en Colonia y Mallorca: villas, áticos, Bayer 04 Leverkusen, WDR, TÜV Rheinland, hoteles y oficinas."),
    "Filter projects": ("Projekte filtern", "Filtrar proyectos"),
    "Scope of work": ("Leistungsumfang", "Alcance del trabajo"),
    "Project": ("Projekt", "Proyecto"), "Details": ("Details", "Detalles"), "Category": ("Kategorie", "Categoría"), "Photos": ("Fotos", "Fotos"),
    "Project details on request.": ("Projektdetails auf Anfrage.", "Detalles del proyecto bajo petición."),
    "Click a photo – then use the arrows, your keyboard or swipe.": ("Foto anklicken – dann mit den Pfeilen, der Tastatur oder per Wischen blättern.", "Haga clic en una foto – luego use las flechas, el teclado o deslice."),
    "Next project": ("Nächstes Projekt", "Siguiente proyecto"),
    "Exclusive villa · 2017 – 2020": ("Exklusive Villa · 2017 – 2020", "Villa exclusiva · 2017 – 2020"),
    "Cologne · 2017 – 2018": ("Köln · 2017 – 2018", "Colonia · 2017 – 2018"),
    "Cologne · 2015": ("Köln · 2015", "Colonia · 2015"),
    "Cologne, Pulheim": ("Köln, Pulheim", "Colonia, Pulheim"),
    "Office renovation": ("Büroumbau", "Reforma de oficinas"),
    "KNX building technology": ("KNX Gebäudetechnik", "Tecnología de edificios KNX"),
    "Office & building technology": ("Büro- & Gebäudetechnik", "Oficinas y tecnología de edificios"),
    # careers
    "Become part of the team": ("Werde Teil des Teams", "Forme parte del equipo"),
    "Build the": ("Bauen Sie die", "Construya los"),
    "smart buildings": ("Smart Buildings", "edificios inteligentes"),
    "of tomorrow.": ("von morgen.", "del mañana."),
    "As a specialist company for electrical and security technology with demanding customers in Germany and Mallorca, we rely on team members who think for themselves, take responsibility – and are passionate about what they do.":
        ("Als spezialisiertes Unternehmen für Elektro- und Sicherheitstechnik mit anspruchsvollen Kunden in Deutschland und auf Mallorca setzen wir auf Teammitglieder, die mitdenken, Verantwortung übernehmen – und mit Leidenschaft bei der Sache sind.",
         "Como empresa especializada en tecnología eléctrica y de seguridad con clientes exigentes en Alemania y Mallorca, apostamos por personas que piensan por sí mismas, asumen responsabilidad y disfrutan de su trabajo."),
    "Open positions": ("Offene Stellen", "Ofertas de empleo"),
    "Apply by email": ("Per E-Mail bewerben", "Enviar candidatura"),
    "You": ("Sie", "Usted"), "Us": ("Wir", "Nosotros"),
    "What you bring with you": ("Was Sie mitbringen", "Lo que usted aporta"),
    "What we offer you": ("Was wir Ihnen bieten", "Lo que le ofrecemos"),
    "You enjoy working in a team, are reliable, flexible, and approach our customers with professionalism and friendliness. Technical understanding and manual dexterity are just as much a given for you as a willingness to develop yourself and think outside the box.":
        ("Sie arbeiten gerne im Team, sind zuverlässig, flexibel und treten unseren Kunden mit Professionalität und Freundlichkeit gegenüber. Technisches Verständnis und handwerkliches Geschick sind für Sie ebenso selbstverständlich wie die Bereitschaft, sich weiterzuentwickeln und über den Tellerrand hinauszuschauen.",
         "Le gusta trabajar en equipo, es fiable, flexible y trata a nuestros clientes con profesionalidad y amabilidad. La comprensión técnica y la habilidad manual son tan naturales para usted como las ganas de seguir aprendiendo."),
    "Completed training in electrical engineering": ("Abgeschlossene Ausbildung im Bereich Elektrotechnik", "Formación completa en electrotecnia"),
    "Ideally, initial experience in service, project management or on construction sites": ("Idealerweise erste Erfahrung in Service, Projektabwicklung oder auf Baustellen", "Idealmente, primera experiencia en servicio, gestión de proyectos u obras"),
    "Class B driving license": ("Führerschein Klasse B", "Carné de conducir clase B"),
    "Desire for long-term cooperation": ("Wunsch nach einer langfristigen Zusammenarbeit", "Deseo de una colaboración a largo plazo"),
    "More than just a job – we offer you prospects. A professional environment with high-quality projects, personal appreciation and genuine future security.":
        ("Mehr als nur ein Arbeitsplatz – wir bieten Ihnen Perspektive. Ein professionelles Umfeld mit hochwertigen Projekten, persönlicher Wertschätzung und echter Zukunftssicherheit.",
         "Más que un empleo – le ofrecemos perspectivas. Un entorno profesional con proyectos de calidad, reconocimiento personal y un futuro seguro."),
    "Permanent position after successful probationary period": ("Festanstellung nach erfolgreicher Probezeit", "Contrato indefinido tras el periodo de prueba"),
    "Attractive earning opportunities": ("Attraktive Verdienstmöglichkeiten", "Remuneración atractiva"),
    "High-quality service vehicle": ("Hochwertig ausgestattetes Servicefahrzeug", "Vehículo de servicio de alta gama"),
    "Thorough training and collegial cooperation": ("Gründliche Einarbeitung und kollegiales Miteinander", "Formación inicial completa y buen compañerismo"),
    "Regular training – technical and safety-related": ("Regelmäßige Schulungen – fachlich und sicherheitsrelevant", "Formación periódica – técnica y de seguridad"),
    "Social security and a modern working environment": ("Soziale Absicherung und modernes Arbeitsumfeld", "Seguridad social y un entorno de trabajo moderno"),
    "We also welcome career changers with technical expertise – and we have been training apprentices for years, with numerous successes.":
        ("Auch Quereinsteiger mit technischem Verständnis sind bei uns willkommen – und wir engagieren uns seit Jahren in der Ausbildung, mit zahlreichen Erfolgen.",
         "También damos la bienvenida a perfiles de otros sectores con conocimientos técnicos – y llevamos años formando aprendices con éxito."),
    "Become part of a team": ("Werden Sie Teil eines Teams,", "Forme parte de un equipo"),
    "that lives quality.": ("das Qualität lebt.", "que vive la calidad."),
    "Construction fitter": ("Baumonteur", "Montador de obra"),
    "Service technician": ("Servicetechniker", "Técnico de servicio"),
    "Trainee (apprentice)": ("Auszubildender", "Aprendiz"),
    "Helper (m/f/d)": ("Helfer (m/w/d)", "Ayudante (h/m/d)"),
    "Realization and execution of large and small projects, property management, building and office conversions, renovations of practices, villas, houses and apartments.":
        ("Realisierung und Abwicklung von Groß- und Kleinprojekten, Hausverwaltungen, Gebäude- und Büroumbauten, Sanierungen von Praxen, Villen, Häusern und Wohnungen.",
         "Realización de proyectos grandes y pequeños, administración de fincas, reformas de edificios y oficinas, renovación de consultas, villas, casas y pisos."),
    "Service and support for regular customers, video intercom systems, KNX building management systems, alarm systems, video surveillance, smart home.":
        ("Service und Support für Stammkunden, Videosprechanlagen, KNX Gebäudemanagementsysteme, Alarmanlagen, Videoüberwachung, Smart Home.",
         "Servicio y soporte para clientes habituales, videoporteros, sistemas KNX, alarmas, videovigilancia y casa inteligente."),
    "Training in a future-oriented profession with innovative technology.": ("Ausbildung in einem zukunftsorientierten Beruf mit innovativer Technik.", "Formación en una profesión con futuro y tecnología innovadora."),
    "We are now looking for energetic helpers for our team!": ("Wir suchen ab sofort tatkräftige Helfer für unser Team!", "¡Buscamos ayudantes con energía para nuestro equipo!"),
    "Apply now": ("Jetzt bewerben", "Enviar candidatura"),
    "Apply now.": ("Jetzt bewerben.", "Envíe su candidatura."),
    "Send your detailed application to info@elektro-paul-neumann.de – we look forward to meeting you.":
        ("Schicken Sie Ihre ausführliche Bewerbung an info@elektro-paul-neumann.de – wir freuen uns auf Sie.",
         "Envíe su candidatura completa a info@elektro-paul-neumann.de – estaremos encantados de conocerle."),
    "Team at work": ("Team bei der Arbeit", "Equipo trabajando"),
    "Careers – Elektro Paul Neumann, KNX professional from Cologne": ("Karriere – Elektro Paul Neumann, KNX Profi aus Köln", "Empleo – Elektro Paul Neumann, profesionales KNX de Colonia"),
    # contact
    "For you in Cologne and Mallorca": ("Für Sie in Köln und auf Mallorca", "Para usted en Colonia y Mallorca"),
    "Let’s build something": ("Lassen Sie uns etwas", "Construyamos algo"),
    "smart.": ("Smartes bauen.", "inteligente."),
    "Call us, write us an email or visit us. After an on-site appointment you receive a binding quote with a detailed description of the work.":
        ("Rufen Sie uns an, schreiben Sie uns oder besuchen Sie uns. Nach einem Vor-Ort-Termin erhalten Sie ein verbindliches Angebot mit genauer Leistungsbeschreibung.",
         "Llámenos, escríbanos o visítenos. Tras una visita in situ recibirá un presupuesto vinculante con descripción detallada."),
    "Visit · Cologne": ("Besuch · Köln", "Visita · Colonia"),
    "Germany · Headquarters": ("Deutschland · Hauptsitz", "Alemania · Sede central"),
    "Cologne office": ("Büro Köln", "Oficina Colonia"),
    "Open in Google Maps": ("In Google Maps öffnen", "Abrir en Google Maps"),
    "Spain · Since 2022": ("Spanien · Seit 2022", "España · Desde 2022"),
    "What happens next": ("Wie es weitergeht", "Próximos pasos"),
    "Three steps to your project.": ("In drei Schritten zum Projekt.", "Tres pasos hacia su proyecto."),
    "About your property and your plans – by phone or email.": ("Von Ihrem Objekt und Ihren Plänen – telefonisch oder per E-Mail.", "Sobre su inmueble y sus planes – por teléfono o correo."),
    "On-site appointment, then a binding quote with a detailed description of the work.": ("Vor-Ort-Termin, dann ein verbindliches Angebot mit genauer Leistungsbeschreibung.", "Visita in situ y después un presupuesto vinculante con descripción detallada."),
    "Installation, commissioning, handover – and service and maintenance afterwards.": ("Installation, Inbetriebnahme, Übergabe – und danach Service und Wartung.", "Instalación, puesta en marcha, entrega – y después servicio y mantenimiento."),
    # imprint
    "Legal": ("Rechtliches", "Legal"),
    "Imprint &": ("Impressum &", "Aviso legal y"),
    "privacy.": ("Datenschutz.", "privacidad."),
    "Imprint & privacy policy – Elektro Paul Neumann": ("Impressum & Datenschutz – Elektro Paul Neumann", "Aviso legal y privacidad – Elektro Paul Neumann"),
}

# (regex, German template, Spanish template); \1, \2 … refer to groups, {t1} = translated group 1
RULES = [
    (r"^(.+) – photo (\d+)$", r"\1 – Foto \2", r"\1 – foto \2"),
    (r"^(.+) – reference photo (\d+)$", r"{t1} – Referenzfoto \2", r"{t1} – foto de referencia \2"),
    (r"^(\d+) photos$", r"\1 Fotos", r"\1 fotos"),
    (r"^(\d+) photos – click to enlarge\.$", r"\1 Fotos – zum Vergrößern anklicken.", r"\1 fotos – haga clic para ampliar."),
    (r"^Project (\d+) / (\d+) · (\w+)$", r"Projekt \1 / \2 · {t3}", r"Proyecto \1 / \2 · {t3}"),
    (r"^(.+) – Project by Elektro Paul Neumann$", r"\1 – Projekt von Elektro Paul Neumann", r"\1 – proyecto de Elektro Paul Neumann"),
    (r"^(.+) – a project by Elektro Paul Neumann, (.+)\.$", r"\1 – ein Projekt von Elektro Paul Neumann, {t2}.", r"\1 – un proyecto de Elektro Paul Neumann, {t2}."),
    (r"^(.+) in Cologne & Mallorca – Elektro Paul Neumann$", r"{t1} in Köln & Mallorca – Elektro Paul Neumann", r"{t1} en Colonia y Mallorca – Elektro Paul Neumann"),
    (r"^Living room – (.+) scene$", r"Wohnzimmer – Szene {t1}", r"Salón – escena {t1}"),
    (r"^(.+?) – (.+)$", r"\1 – {t2}", r"\1 – {t2}"),   # "Name – subtitle" alt texts
    (r"^All (\d+)$", r"Alle \1", r"Todos (\1)"),
    (r"^\+(\d+) more$", r"+\1 weitere", r"+\1 más"),
    (r"^Application: (.+)$", r"Bewerbung: {t1}", r"Candidatura: {t1}"),
]


def apply_rules(core, lang_idx):
    """Translate patterned strings; {tN} = group N looked up in TR (left as is when unknown)."""
    look = lambda s: TR[s][lang_idx] if s in TR else s
    for pat, de, es in RULES:
        m = re.match(pat, core)
        if m:
            tpl = de if lang_idx == 0 else es
            tpl = re.sub(r"\{t(\d)\}", lambda k: look(m.group(int(k.group(1)))).replace("\\", "\\\\"), tpl)
            return m.expand(tpl)
    return None
