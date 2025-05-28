// const speed = 0.7;

// window.addEventListener('scroll', () => {
//     // how far the page has scrolled
//     const scrolled = window.pageYOffset;
//     // update the body's background-position Y
//     document.body.style.backgroundPosition = `center ${scrolled * speed}px`;
//   });


function initialize() {
    add_grants_and_scholarships();
    add_recent_events();
    add_papers();
    // add_notesupd();
    // add_graph();
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
        content.style.display = "none";
        } else {
        content.style.display = "block";
        }
        // this.textContent += "a";
        var tmp = this.textContent[this.textContent.length-2] == '+' ? '–' : '+';
        this.textContent = this.textContent.slice(0,-2) + tmp + "]"
    });
    }

}

/*
Add Recent Events Here:
Order: Date, content
*/

papers = [
    ["Formalising Subject Reduction and Progress for Multiparty Session Types","Interactive Theorem Proving 2025 (To Appear)","B.Ekici, T.Kamegai, N.Yoshida"]
]

notesupd = [
    ["<a href = notes/coinduction/notes.pdf>Notes regarding coinduction</a>","Notes aimed for briding the intuition between induction and coinduction, with examples of proofs in coq."],
    ["<a href = notes/linalg/notes.pdf>Notes on basics of Linear Algebra</a>","Notes on Linear Algebra based on Oxford's Mathematics course."],
    ["<a href = notes/pl-general/notes.pdf>Notes on Concepts Tied to Programming Languages</a>","Notes aimed to cover a wide range of basic concepts regarding PL Theory from a Topological and Categorical perspective"],
]

grants = [
    ["Oct 2022 - Jun 2026", '<a href="https://www.yanaitadashi-foundation.or.jp/">Yanai-Tadashi Foundation</a> Scholarship, full funding of expenses during the undergraduate degree'],
    ["Oct 2024", 'Postmaster Scholarship by Merton College, following results of Year 2 Examinations'],
    ["Jul 2024 - Sep 2024", 'Merton Summer Project Scheme, covering accomodation and hall expenses during summer research'],
    ["Dec 2023", 'Exhibition Scholarship by Merton College, following results of the Preliminary Examinations']
]

events = [
    // ["Nov 23, 2024", 'I made notes on coinduction titled \"<a href = "notes/coinduction/notes.pdf">A Duality in Proof Structures: Intuition for Bridging Induction and Coinduction</a>\".'],
    ["May 23, 2025", 'The paper "Formalising Subject Reduction and Progress for Multiparty Session Types" got accepted to ITP\'25.'],
    ["May 18, 2024", 'The OEIS entries <a href="https://oeis.org/A372141">A372141</a> and <a href="https://oeis.org/A372142">A372142</a> regarding palindromic primes for a general base has been approved and is now public.'],
    // ["Apr 12 2024", 'I participated in <a href="https://www.cs.le.ac.uk/events/mgs2024/">Midlands Graduate School (MGS) 2024</a> hosted at the University of Leicester, taking Category Theory, Proof Theory, Type Theory, and Session Types courses.'],
    ["Feb 25 2024", 'The OEIS entry <a href="https://oeis.org/A369580">A369580</a> regarding a probability sequence on a coin flipping game was approved and is now public.']
]

function add_papers() {
    var max_paper_count = 1000;
    var table = document.getElementById("publication_list")
    for(let i = 0; i < Math.min(papers.length, max_paper_count+1); i++) {
        var row = table.insertRow(i);
        row.insertCell(0).innerHTML = `<div class="paper_title">${papers[i][0]}</div>
                                       <div class="paper_people">${papers[i][2]}</div>
                                       <div class="paper_conf">${papers[i][1]}</div>`
    }
}

function add_grants_and_scholarships() {
    var max_grant_count = 100;
    var table = document.getElementById("grants_and_scholarships")
    for(let i = 0; i < Math.min(grants.length, max_grant_count+1); i++) {
        var row = table.insertRow(i);
        row.insertCell(0).innerHTML = `<div class="grant_date">${grants[i][0]}:</div>`
        row.insertCell(1).innerHTML = `<div class="grant_context">${grants[i][1]}</div>`
    }
}

function add_recent_events() {
    var max_event_count = 10;
    var table = document.getElementById("recent_events")
    for(let i = 0; i < Math.min(events.length, max_event_count+1); i++) {
        var row = table.insertRow(i);
        row.insertCell(0).innerHTML = `<div class="event_date">${events[i][0]}</div><div class="event_context">${events[i][1]}</div>`
    }
}

function add_notesupd() {
    var max_note_count = 10000;
    var table = document.getElementById("notesupd")
    for(let i = 0; i < Math.min(events.length, max_note_count+1); i++) {
        var row = table.insertRow(i);
        row.insertCell(0).innerHTML = `<div class="note_link">${notesupd[i][0]}</div><div class="note_context">${notesupd[i][1]}</div>`
    }
}


function add_graph() {
    // 1. Construct the Viz instance
    const viz = new Viz();

    // 2. Render to an SVGElement, asynchronously
    
    const dot = `
      digraph CourseDependencies {
  rankdir=LR;
  node [shape=box, style=rounded];

  Logic_and_Proof [label="Logic & Proof"];
  Linear_Algebra [label="Linear Algebra"];
  Real_Analysis [label="Real Analysis"];
  Metric_Spaces [label="Metric Spaces"];
  Complex_Analysis [label="Complex Analysis"];
  Topology [label="Topology"];
  Groups [label="Groups"];
  Rings_Modules [label="Rings & Modules"];
  Commutative_Algebra [label="Commutative Algebra"];
  Galois_Theory [label="Galois Theory"];
  Algebraic_Number_Theory [label="Algebraic Number Theory"];
  Representation_Theory [label="Representation Theory"];
  Algebraic_Topology [label="Algebraic Topology", fontcolor="blue"];
  LCT [label="Lambda Calculus"];
  PoPL [label="Principles of Programming Languages"];
  Functional_Programming [label="Functional Programming"];
  Domain_Theory [label="Domain Theory", fontcolor="blue"];
  CAFV [label="Computer-Aided Formal Verification"];
  MoC[label="Models of Computation"];
  DPTP[label="Distributed Types, Proofs, and Processes" fontcolor="blue"];
  Number_Theory[label="Number Theory"];
  Set_Theory[label="Set Theory", fontcolor="red"];
  Model_Theory[label="Model Theory", fontcolor="red"];
  Homological_Algebra[label="Homological Algebra", fontcolor="green"];
  Category_Theory[label="Category Theory", fontcolor="blue"];
  Geometry[label="Geometry", fontcolor="red"];
  Projective_Geometry[label="Projective Geometry", fontcolor="red"];
  Algebraic_Curve[label="Algebraic Curves", fontcolor="red"];
  Geometry_Surface[label="Geometry of Surfaces", fontcolor="red"];
  Algebraic_Geometry[label="Algebraic Geometry", fontcolor="red"];
  MLTT[label="MLTT / Dependent Types", fontcolor="blue"];
  Schemes[label="Schemes", fontcolor="green"];
  HoTT[label="Homotopy Type Theory", fontcolor="green"];
  AMG[label="Automata, Logic, and Games", fontcolor="green"];
  Topology_Group[label="Topology and Groups"];

  Geometry -> Projective_Geometry;
  Projective_Geometry -> Algebraic_Curve;
  Geometry_Surface -> Algebraic_Curve;
  # Topology -> Algebraic_Curve;
  Geometry -> Geometry_Surface;
  Algebraic_Curve -> Algebraic_Geometry;
  Commutative_Algebra -> Algebraic_Geometry;
  Algebraic_Geometry -> Category_Theory;
  
  Real_Analysis -> Metric_Spaces;
  Real_Analysis -> Complex_Analysis;
  Metric_Spaces -> Topology;

  Linear_Algebra -> Representation_Theory;
  Groups -> Representation_Theory;
  Rings_Modules -> Representation_Theory;
  Representation_Theory -> Category_Theory;

  Groups -> Galois_Theory;
  Rings_Modules -> Commutative_Algebra;
  Commutative_Algebra -> Algebraic_Number_Theory;
  Galois_Theory -> Algebraic_Number_Theory;
  Rings_Modules -> Galois_Theory;
  Number_Theory -> Algebraic_Number_Theory;

  Commutative_Algebra -> Homological_Algebra;
  Algebraic_Number_Theory -> Category_Theory;
  Homological_Algebra -> Algebraic_Topology;
  Algebraic_Topology -> Category_Theory;
  Category_Theory -> Schemes;

  Topology -> Topology_Group;
  Groups -> Topology_Group;
  Topology_Group -> Algebraic_Topology;
  # Groups -> Algebraic_Topology;
  Topology -> Domain_Theory;
  Topology -> Geometry_Surface;

  PoPL -> HoTT;
  Category_Theory -> HoTT;
  MLTT -> HoTT;

  # Logic_and_Proof -> PoPL;
  # Functional_Programming -> Logic_and_Proof;
  Functional_Programming -> LCT;
  Logic_and_Proof -> CAFV;
  Logic_and_Proof -> Set_Theory;
  Set_Theory -> Model_Theory;

  LCT -> PoPL;
  LCT -> MLTT;
  LCT -> Domain_Theory;
  LCT -> DPTP;
  CAFV -> DPTP;
  CAFV -> AMG;

  # Functional_Programming -> PoPL;
  Domain_Theory -> CAFV;
  # Functional_Programming -> CAFV;
  Domain_Theory -> PoPL;
  PoPL -> Category_Theory;
  MoC -> CAFV
}
    `;

    // 3. Render with a specific layout engine
    viz
      .renderSVGElement(dot, { engine: "dot", format: "svg" })
      .then(svgEl => {
        document.getElementById("graph").appendChild(svgEl);
      })
      .catch(err => console.error("Viz.js error:", err));
    }