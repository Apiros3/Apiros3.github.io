function change_html() {

    document.getElementById("dev-stuff").innerHTML = '<div style="font-weight: 600; font-size: 18px;">・てすと</div>' 


}

function display(id) {
    var display_id_list = ["othello-ai", "epidemic-model", "cp-library", "discord-problem-bot"]
    var list_size = display_id_list.length;
    for(let i = 0; i < list_size; i++) {
        if (i == id) {
            document.getElementById(display_id_list[i]).style.display = 'block';
            document.getElementById(display_id_list[i]+"-button").disabled = true;
        }
        else {
            document.getElementById(display_id_list[i]).style.display = 'none';
            document.getElementById(display_id_list[i]+"-button").disabled = false;
        }
    }

}