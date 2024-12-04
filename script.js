function initialize() {
    add_grants_and_scholarships()
    add_recent_events()

}

/*
Add Recent Events Here:
Order: Date, content
*/

grants = [
    ["Oct 2022 - Jun 2026", '<a href="https://www.yanaitadashi-foundation.or.jp/">Yanai-Tadashi Foundation</a> Scholarship, full funding of expenses during the undergraduate degree'],
    ["Jul 2024 - Sep 2024", 'Merton Summer Project Scheme, covering accomodation and hall expenses during summer research'],
    ["Dec 2023", 'Exhibition Scholarship by Merton College, following results of the Preliminary Examinations']
]

events = [
    ["Nov 23, 2024", 'I made notes on coinduction titled \"<a href = "notes/coinduction/notes.pdf">A Duality in Proof Structures: Intuition for Bridging Induction and Coinduction</a>\".'],
    ["May 18, 2024", 'The OEIS entries <a href="https://oeis.org/A372141">A372141</a> and <a href="https://oeis.org/A372142">A372142</a> regarding palindromic primes for a general base has been approved and is now public.'],
    ["Apr 12 2024", 'I participated in <a href="https://www.cs.le.ac.uk/events/mgs2024/">Midlands Graduate School (MGS) 2024</a> hosted at the University of Leicester, taking Category Theory, Proof Theory, Type Theory, and Session Types courses.'],
    ["Feb 25 2024", 'The OEIS entry <a href="https://oeis.org/A369580">A369580</a> regarding a probability sequence on a coin flipping game was approved and is now public.']
]

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

