
function check() {
    if(document.getElementById('433').checked) {
        move433(".player");
    }
    
    if(document.getElementById('442').checked) {
        move442(".player");
    }
    
    if(document.getElementById('343').checked) {
        move343(".player");
    }
    if(document.getElementById('451').checked) {
        move451(".player");
    }
    if(document.getElementById('352').checked) {
        move352(".player");
    }
};

function opponentShape(formation) {
    if(formation == '4-3-3') {
        move433(".opponent");
    }
    
    if(formation == '4-4-2') {
        move442(".opponent");
    }
    
    if(formation == '3-4-3') {
        move343(".opponent");
    }
    if(formation == '4-5-1') {
        move451(".opponent");
    }
    if(formation == '3-5-2') {
        move352(".opponent");
    }
}

function move433(className) {
    span3 = document.querySelectorAll(`${className}.player-one, ${className}.player-two, ${className}.player-three, ${className}.player-four`);
    span4 = document.querySelectorAll(`${className}.player-five, ${className}.player-six, ${className}.player-seven, ${className}.player-eight, ${className}.player-nine, ${className}.player-ten`);

    for (var i = 0, len = span3.length; i < len; i++) {
    span3[i].style.setProperty("grid-column", "span 3");
    }

    for (var i = 0, len = span4.length; i < len; i++) {
    span4[i].style.setProperty("grid-column", "span 4");
    }
}

function move442(className) {
    span3 = document.querySelectorAll(`${className}.player-one, ${className}.player-two, ${className}.player-three, ${className}.player-four, ${className}.player-five, ${className}.player-six, ${className}.player-seven, ${className}.player-eight`);
    span6 = document.querySelectorAll(`${className}.player-nine, ${className}.player-ten`);

    for (var i = 0, len = span3.length; i < len; i++) {
    span3[i].style.setProperty("grid-column", "span 3");
    }

    for (var i = 0, len = span6.length; i < len; i++) {
    span6[i].style.setProperty("grid-column", "span 6");
    }
}

function move343(className) {
    span3 = document.querySelectorAll(`${className}.player-four, ${className}.player-five, ${className}.player-six, ${className}.player-seven`);
    span4 = document.querySelectorAll(`.player ${className}.player-one, ${className}.player-two, ${className}.player-three, ${className}.player-eight, ${className}.player-nine, ${className}.player-ten`);

    for (var i = 0, len = span3.length; i < len; i++) {
    span3[i].style.setProperty("grid-column", "span 3");
    }

    for (var i = 0, len = span4.length; i < len; i++) {
    span4[i].style.setProperty("grid-column", "span 4");
    }
}

function move451(className) {
    span2 = document.querySelectorAll(`${className}.player-six, ${className}.player-seven, ${className}.player-eight`);
    span3 = document.querySelectorAll(`.player ${className}.player-one, ${className}.player-two, ${className}.player-three, ${className}.player-four, ${className}.player-five, ${className}.player-nine`);
    span12 = document.querySelectorAll(`${className}.player-ten`);

    for (var i = 0, len = span2.length; i < len; i++) {
        span2[i].style.setProperty("grid-column", "span 2");
    }
    
    for (var i = 0, len = span3.length; i < len; i++) {
        span3[i].style.setProperty("grid-column", "span 3");
    }

    for (var i = 0, len = span12.length; i < len; i++) {
        span12[i].style.setProperty("grid-column", "span 12");
    }
}

function move352(className) {
    span2 = document.querySelectorAll(`${className}.player-five, ${className}.player-six, ${className}.player-seven`);
    span3 = document.querySelectorAll(`${className}.player-four, ${className}.player-eight`);
    span4 = document.querySelectorAll(`.player ${className}.player-one, ${className}.player-two, ${className}.player-three`);
    span6 = document.querySelectorAll(`${className}.player-nine, ${className}.player-ten`);

    for (var i = 0, len = span2.length; i < len; i++) {
        span2[i].style.setProperty("grid-column", "span 2");
    }
    
    for (var i = 0, len = span3.length; i < len; i++) {
        span3[i].style.setProperty("grid-column", "span 3");
    }

    for (var i = 0, len = span4.length; i < len; i++) {
        span4[i].style.setProperty("grid-column", "span 4");
    }

    for (var i = 0, len = span6.length; i < len; i++) {
        span6[i].style.setProperty("grid-column", "span 6");
    }
}
    