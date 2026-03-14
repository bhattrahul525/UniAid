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
    rent:
      "Shared accommodation near universities costs around $250–$350 per week. CBD apartments can range from $350–$500 weekly.",
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
    image: "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["University of Sydney", "University of New South Wales (UNSW)"],
    description:
      "Sydney is Australia's global hub, home to University of Sydney and UNSW, both top-tier universities excelling in medicine, business, and engineering.",
    cheapFood: [
      "$7 sushi rolls near Town Hall",
      "Student lunch deals in Chinatown",
      "Food courts around Central Station",
      "Affordable Korean food in Strathfield"
    ],
    rent:
      "Shared housing typically ranges from $300–$420 per week. Living close to the CBD can exceed $450 weekly.",
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
    image: "https://plus.unsplash.com/premium_photo-1694475701659-444e11e512d9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["University of Queensland"],
    description:
      "Brisbane offers a relaxed student lifestyle with excellent research universities like the University of Queensland.",
    cheapFood: [
      "$6 student meals near UQ campus",
      "Affordable Asian food in Sunnybank",
      "Campus food trucks",
      "Cheap dumpling restaurants"
    ],
    rent:
      "Shared student housing typically ranges from $220–$320 per week.",
    transport: "Brisbane uses the Go Card system for buses, trains, and ferries.",
    scams: [
      "Fake student housing advertisements",
      "Phone scams pretending to be government agencies",
      "Fake internship offers",
      "Online marketplace payment scams"
    ]
  },

  canberra: {
    image: "https://images.unsplash.com/photo-1510546020578-a35ae9fcfb0f?q=80&w=1204&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["Australian National University (ANU)"],
    description:
      "Canberra is home to the Australian National University (ANU), one of Australia's leading research universities with strengths in policy, science, and engineering.",
    cheapFood: [
      "$6–$8 meals near ANU campus",
      "Affordable cafés in Civic",
      "Student specials at local eateries",
      "Budget Asian restaurants"
    ],
    rent:
      "Shared student housing typically costs $250–$350 per week.",
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
    image: "https://images.unsplash.com/photo-1580014942344-ce423d2b885a?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["University of Western Australia (UWA)"],
    description:
      "Perth is home to UWA, a globally ranked university known for research in science, medicine, and engineering.",
    cheapFood: [
      "$7–$10 meals near UWA",
      "Student specials at local cafes",
      "Affordable Asian and Middle Eastern restaurants",
      "Campus food deals"
    ],
    rent:
      "Shared student accommodation ranges from $220–$350 weekly, depending on location.",
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
    image: "https://plus.unsplash.com/premium_photo-1733317321940-594f2dea8d18?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    universities: ["University of Adelaide"],
    description:
      "Adelaide is home to the University of Adelaide, a research-intensive university with global recognition in health sciences, engineering, and business.",
    cheapFood: [
      "$5–$8 student meals near North Terrace",
      "Affordable Asian eateries",
      "Campus café specials",
      "Budget-friendly sandwich shops"
    ],
    rent:
      "Shared accommodation typically costs $200–$300 per week.",
    transport:
      "Adelaide Metro buses and trams service the city; students may use discounted travel cards.",
    scams: [
      "Fake rental ads",
      "Job offer scams",
      "Phishing emails targeting students",
      "Fraudulent online marketplace listings"
    ]
  }
};

export default cityData;