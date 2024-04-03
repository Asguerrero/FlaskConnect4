function fetchState() {
    number = document.getElementById("game_num").innerHTML;
    URL = "/gamestate/" + number;
    fetch(URL).then( response => response.json()).then( the_json => updateState(the_json) );

}

function updateState(the_json) {
    new_state = the_json['state'];
  
    the_gameboard = document.getElementById("gameboard");
    the_gameboard.innerHTML = '';
    state_table = makeTable(new_state)
    the_gameboard.appendChild(state_table)
}

function initializeState(){
    //fetchState();

    //Update the board state every 2 seconds (2000 milliseconds)
    setInterval(fetchState, 2000)
}

function makeTable(state){
    tbl = document.createElement('table');
    tbl.style.width = '30px';
    tbl.style.fontSize = '25px';
    tbl.style.border = '1px solid black';
    tbl.style.marginLeft = 'auto';
    tbl.style.marginRight = 'auto';

    for (let i = 0; i < 6; i++){
	const tr = tbl.insertRow();
	for (let j = 0; j < 7; j++){
	    const td = tr.insertCell();
	    // Compute the character position in the state string
	    chr = state.charAt(2 + j + i*7);
	    if (chr == '-'){ chr = '--'; }
	    td.appendChild(document.createTextNode(chr));
	    td.style.border = '1px solid black';
	}
    }
    return tbl;
}
		

    
