// Start counting for the time to be displayed
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    // add a zero in front of numbers<10
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('txt').innerHTML=h+":" + m + ":" + s;
    t = setTimeout('startTime()',500);
}

// Formatting for the time
function checkTime(i) {
    if (i<10) {
        i="0" + i;
    }
    return i;
}

// This function will make the default field in the spot where the user inputs the name of the pill
// Not necessary just provides for ease of use
function chkind(){
    var dropdown1 = document.getElementById('pills');
    var a = dropdown1.options[pills.selectedIndex].text;
    if(a === 'Add New'){
        a = ' ';
    }
    var name = document.getElementById('name');
    name.value = a;
}