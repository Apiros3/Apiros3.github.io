function initialize() {
    add_recent_events()

}

/*
Add Recent Events Here:
Order: Date, content
*/

events = [
    ["Date:","Content:"],
    ["Apr 12 2024", 'I participated in <a href="https://www.cs.le.ac.uk/events/mgs2024/">Midlands Graduate School (MGS) 2024</a>, taking Category Theory, Proof Theory, Type Theory, and Session Types courses'],
    ["Feb 25 2024", 'The OEIS entry <a href="https://oeis.org/A369580">A369580</a> was approved and is now public.']
]

function add_recent_events() {
    var max_event_count = 10;
    var table = document.getElementById("recent_events")
    for(let i = 0; i < Math.min(events.length, max_event_count+1); i++) {
        var row = table.insertRow(i);
        row.insertCell(0).innerHTML = events[i][0];
        row.insertCell(1).innerHTML = events[i][1];
    }
}

