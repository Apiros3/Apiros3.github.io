function initialize() {
    add_recent_events()

}

/*
Add Recent Events Here:
Order: Date, content
*/

events = [
    ["May 18, 2024", 'The OEIS entries <a href="https://oeis.org/A372141">A372141</a> and <a href="https://oeis.org/A372141">A372141</a> regarding palindromic primes for a general base has been approved and is now public.'],
    ["Apr 12 2024", 'I participated in <a href="https://www.cs.le.ac.uk/events/mgs2024/">Midlands Graduate School (MGS) 2024</a> hosted at the University of Leicester, taking Category Theory, Proof Theory, Type Theory, and Session Types courses.'],
    ["Feb 25 2024", 'The OEIS entry <a href="https://oeis.org/A369580">A369580</a> regarding a probability sequence on a coin flipping game was approved and is now public.']
]

function add_recent_events() {
    var max_event_count = 10;
    var table = document.getElementById("recent_events")
    for(let i = 0; i < Math.min(events.length, max_event_count+1); i++) {
        var row = table.insertRow(i);
        row.insertCell(0).innerHTML = `<div class="event_date">${events[i][0]}</div><div class="event_context">${events[i][1]}</div>`
    }
}

