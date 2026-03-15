const cityData = {
  melbourne: {
    image: "https://images.unsplash.com/photo-1514395462725-fb4566210144",
    universities: ["University of Melbourne", "Monash University"],
    description:
      "Melbourne is Australia's academic capital with world-class universities. University of Melbourne and Monash University are renowned for research across medicine, engineering, law, and data science.",
    cheapFood: [
      "$6–$8 Bahn Mi in Footscray",
      "Cheap dumpling houses in Chinatown",
      "$5 campus coffee deals",
      "Student lunch specials near Swanston Street"
    ],
    rent: "Shared accommodation near universities costs around $250–$350 per week. CBD apartments can range from $350–$500 weekly.",
    transport:
      "Melbourne uses the Myki transport card. The CBD has a Free Tram Zone, making it easy for students to travel within the city center.",
    scams: [
      "Fake rental listings targeting international students",
      "Scammers posing as immigration officers demanding visa payments",
      "Fake job offers asking for upfront training fees",
      "Facebook Marketplace rental deposit scams"
    ]
  },

  sydney: {
    image:
      "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: [
      "University of Sydney",
      "University of New South Wales (UNSW)"
    ],
    description:
      "Sydney is Australia's global hub, home to University of Sydney and UNSW, both top-tier universities excelling in medicine, business, and engineering.",
    cheapFood: [
      "$7 sushi rolls near Town Hall",
      "Student lunch deals in Chinatown",
      "Food courts around Central Station",
      "Affordable Korean food in Strathfield"
    ],
    rent: "Shared housing typically ranges from $300–$420 per week. Living close to the CBD can exceed $450 weekly.",
    transport:
      "Sydney uses the Opal card system for trains, buses, and ferries. Students get capped daily fares.",
    scams: [
      "Fake apartment listings near universities",
      "Fake tax refund messages",
      "Uber or taxi overcharging tourists",
      "Fake job recruitment scams"
    ]
  },

  brisbane: {
    image:
      "https://plus.unsplash.com/premium_photo-1694475701659-444e11e512d9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["University of Queensland"],
    description:
      "Brisbane offers a relaxed student lifestyle with excellent research universities like the University of Queensland.",
    cheapFood: [
      "$6 student meals near UQ campus",
      "Affordable Asian food in Sunnybank",
      "Campus food trucks",
      "Cheap dumpling restaurants"
    ],
    rent: "Shared student housing typically ranges from $220–$320 per week.",
    transport:
      "Brisbane uses the Go Card system for buses, trains, and ferries.",
    scams: [
      "Fake student housing advertisements",
      "Phone scams pretending to be government agencies",
      "Fake internship offers",
      "Online marketplace payment scams"
    ]
  },

  canberra: {
    image:
      "https://images.unsplash.com/photo-1510546020578-a35ae9fcfb0f?q=80&w=1204&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["Australian National University (ANU)"],
    description:
      "Canberra is home to the Australian National University (ANU), one of Australia's leading research universities with strengths in policy, science, and engineering.",
    cheapFood: [
      "$6–$8 meals near ANU campus",
      "Affordable cafés in Civic",
      "Student specials at local eateries",
      "Budget Asian restaurants"
    ],
    rent: "Shared student housing typically costs $250–$350 per week.",
    transport:
      "Canberra uses the ACTION bus network; students often walk or cycle to campus.",
    scams: [
      "Fake rental ads targeting students",
      "Phishing emails pretending to be university staff",
      "Fake internship offers",
      "Online marketplace scams"
    ]
  },

  perth: {
    image:
      "https://images.unsplash.com/photo-1580014942344-ce423d2b885a?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["University of Western Australia (UWA)"],
    description:
      "Perth is home to UWA, a globally ranked university known for research in science, medicine, and engineering.",
    cheapFood: [
      "$7–$10 meals near UWA",
      "Student specials at local cafes",
      "Affordable Asian and Middle Eastern restaurants",
      "Campus food deals"
    ],
    rent: "Shared student accommodation ranges from $220–$350 weekly, depending on location.",
    transport:
      "Perth uses the Transperth system with buses, trains, and ferries. Students often get discounted fare passes.",
    scams: [
      "Fake rental listings",
      "Phone scams pretending to be landlords",
      "Fake tutoring offers",
      "Online shopping scams"
    ]
  },

  adelaide: {
    image:
      "https://plus.unsplash.com/premium_photo-1733317321940-594f2dea8d18?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["University of Adelaide"],
    description:
      "Adelaide is home to the University of Adelaide, a research-intensive university with global recognition in health sciences, engineering, and business.",
    cheapFood: [
      "$5–$8 student meals near North Terrace",
      "Affordable Asian eateries",
      "Campus café specials",
      "Budget-friendly sandwich shops"
    ],
    rent: "Shared accommodation typically costs $200–$300 per week.",
    transport:
      "Adelaide Metro buses and trams service the city; students may use discounted travel cards.",
    scams: [
      "Fake rental ads",
      "Job offer scams",
      "Phishing emails targeting students",
      "Fraudulent online marketplace listings"
    ]
  },
  london: {
    image: "https://images.unsplash.com/photo-1467269204594-9661b134dd2b",
    universities: [
      "University College London (UCL)",
      "Imperial College London",
      "King’s College London"
    ],
    description:
      "London is one of the world's leading academic cities with globally ranked universities like UCL, Imperial College London, and King's College London, known for excellence in research and innovation.",
    cheapFood: [
      "£5 meal deals from Tesco and Sainsbury’s",
      "Cheap street food in Camden Market",
      "Student lunch specials near Bloomsbury",
      "Affordable food stalls in Shoreditch"
    ],
    rent: "Shared accommodation typically ranges from £700–£1200 per month depending on location.",
    transport:
      "London uses the Oyster card and contactless payments across buses, underground trains, and trams.",
    scams: [
      "Fake apartment listings targeting international students",
      "Rental deposit scams",
      "Fake job recruitment emails",
      "Ticket resale scams"
    ]
  },

  paris: {
    image: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34",
    universities: ["Sorbonne University", "Paris Sciences et Lettres (PSL)"],
    description:
      "Paris is home to historic universities like Sorbonne and PSL University, offering world-class education in science, humanities, and arts.",
    cheapFood: [
      "€5–€8 baguette sandwiches",
      "Student cafeterias (CROUS)",
      "Affordable crepes near universities",
      "Budget meals in Latin Quarter"
    ],
    rent: "Student accommodation typically ranges from €500–€900 per month.",
    transport: "Paris uses the Navigo card for metro, buses, and RER trains.",
    scams: [
      "Fake rental listings",
      "Pickpocketing in tourist areas",
      "Ticket machine scams",
      "Online marketplace fraud"
    ]
  },

  berlin: {
    image: "https://images.unsplash.com/photo-1505761671935-60b3a7427bad",
    universities: [
      "Humboldt University of Berlin",
      "Technical University of Berlin"
    ],
    description:
      "Berlin is a vibrant student city with strong universities like Humboldt University and TU Berlin known for engineering, research, and innovation.",
    cheapFood: [
      "€3–€5 kebabs",
      "Student cafeterias (Mensa)",
      "Cheap currywurst stands",
      "Affordable bakeries"
    ],
    rent: "Shared apartments range from €400–€700 per month.",
    transport:
      "Berlin uses the BVG transport system with U-Bahn, S-Bahn, trams, and buses.",
    scams: [
      "Fake rental listings",
      "Apartment viewing scams",
      "Online marketplace fraud",
      "Fake job offers"
    ]
  },

  newyork: {
    image: "https://images.unsplash.com/photo-1496588152823-86ff7695e68f",
    universities: ["Columbia University", "New York University (NYU)"],
    description:
      "New York is a global education hub with prestigious universities like Columbia and NYU, offering strong programs across business, technology, and research.",
    cheapFood: [
      "$5 pizza slices",
      "$7 halal food carts",
      "Cheap Chinatown dumplings",
      "Student meal deals near NYU"
    ],
    rent: "Shared apartments typically range from $900–$1600 per month depending on borough.",
    transport:
      "The NYC Subway and MetroCard system provides 24-hour transportation across the city.",
    scams: [
      "Fake apartment listings",
      "Craigslist rental scams",
      "Job scams targeting students",
      "Ticket resale fraud"
    ]
  },

  tokyo: {
    image: "https://images.unsplash.com/photo-1503899036084-c55cdd92da26",
    universities: ["University of Tokyo", "Tokyo Institute of Technology"],
    description:
      "Tokyo is a global technology and research center with top universities such as the University of Tokyo and Tokyo Tech.",
    cheapFood: [
      "¥500 ramen shops",
      "Affordable bento boxes",
      "Convenience store meals",
      "University cafeteria meals"
    ],
    rent: "Student housing typically ranges from ¥50,000–¥90,000 per month.",
    transport:
      "Tokyo uses the Suica and Pasmo cards across trains, subways, and buses.",
    scams: [
      "Apartment deposit scams",
      "Online job scams",
      "Fake tutoring offers",
      "Fraudulent rental agencies"
    ]
  },

  singapore: {
    image: "https://images.unsplash.com/photo-1525625293386-3f8f99389edd",
    universities: [
      "National University of Singapore (NUS)",
      "Nanyang Technological University (NTU)"
    ],
    description:
      "Singapore is a leading education hub in Asia with globally ranked universities like NUS and NTU.",
    cheapFood: [
      "$4–$6 hawker center meals",
      "Affordable campus cafeterias",
      "Student meals in food courts",
      "Budget noodle stalls"
    ],
    rent: "Shared accommodation ranges from SGD $600–$1200 per month.",
    transport: "Singapore uses the EZ-Link card for MRT trains and buses.",
    scams: [
      "Fake job offers",
      "Rental scams targeting students",
      "Online payment fraud",
      "Phishing emails"
    ]
  },

  delhi: {
    image: "https://images.unsplash.com/photo-1587474260584-136574528ed5",
    universities: ["Delhi University", "Jawaharlal Nehru University"],
    description:
      "Delhi is home to some of India's most prestigious universities including Delhi University and JNU.",
    cheapFood: [
      "₹40–₹60 street food meals",
      "Student canteens",
      "Affordable North Indian thalis",
      "Cheap campus cafés"
    ],
    rent: "Shared accommodation typically ranges from ₹8,000–₹18,000 per month.",
    transport: "Delhi Metro provides fast transport across the city.",
    scams: [
      "Fake PG accommodation listings",
      "Online job scams",
      "Phone scams",
      "Fraudulent rental deposits"
    ]
  },

  dubai: {
    image: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c",
    universities: ["University of Dubai", "American University in Dubai"],
    description:
      "Dubai is an international education hub with many global university campuses and strong business programs.",
    cheapFood: [
      "AED 10 shawarma",
      "Affordable Pakistani and Indian restaurants",
      "Student cafeteria meals",
      "Cheap cafeteria combos"
    ],
    rent: "Shared accommodation ranges from AED 800–1500 per month.",
    transport: "Dubai uses the Nol card for metro, buses, and trams.",
    scams: [
      "Fake job recruitment scams",
      "Rental deposit scams",
      "Online shopping scams",
      "Visa processing scams"
    ]
  },

  capetown: {
    image: "https://images.unsplash.com/photo-1501594907352-04cda38ebc29",
    universities: ["University of Cape Town"],
    description:
      "Cape Town offers stunning landscapes and strong universities like the University of Cape Town known for research and innovation.",
    cheapFood: [
      "Affordable campus meals",
      "Cheap local cafés",
      "Student food trucks",
      "Budget street food"
    ],
    rent: "Shared student housing typically ranges from R3500–R7000 per month.",
    transport:
      "Students often rely on MyCiTi buses and campus transport services.",
    scams: [
      "Fake rental listings",
      "Online payment scams",
      "Phone scams",
      "Marketplace fraud"
    ]
  },

  saopaulo: {
    image: "https://images.unsplash.com/photo-1551593831-b8d1f9c0c34c",
    universities: ["University of São Paulo (USP)"],
    description:
      "São Paulo is Brazil's largest academic and economic center, home to the prestigious University of São Paulo.",
    cheapFood: [
      "Cheap street food stalls",
      "Student cafeterias",
      "Affordable Brazilian buffets",
      "Campus snack bars"
    ],
    rent: "Shared accommodation typically ranges from R$800–R$1500 per month.",
    transport:
      "São Paulo uses the Bilhete Único card for metro and bus systems.",
    scams: [
      "Fake rental ads",
      "Online shopping scams",
      "Fraudulent job offers",
      "Phone scams"
    ]
  }
};

export default cityData;
