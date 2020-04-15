// get the title of the page

let title = document.querySelector('title');
// create a new string, which repeats the title 5 times

function newString() {
    let str = "";
    for (let i = 0; i < 5; i++)
    {
        str = str + title.innerHTML
    }
    return str;
};

// update the title of the page
function doThing() {
    title.innerHTML = newString();
};


