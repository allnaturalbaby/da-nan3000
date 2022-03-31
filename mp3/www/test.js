let myUrl = 'http://localhost/cgi-bin/diktbase.cgi/';
let loggedInEmail = "";

function checkIfLoggedIn() {
    if (sessionStorage.getItem('status') != '') {
        return true;
    } else {
        return false;
    }
}

function getAllPoems() {
    
    fetch(`${myUrl}dikt/`, {
        method: 'GET',
        Origin: 'http://localhost'
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")
        const count = xml.getElementsByTagName("dikt").length
        const noe = document?.getElementById("userLoggedIn")?.textContent;
        console.log(noe);
        let deletePoem;
        let doChangePoem;
        document.getElementById("alleDikt").innerHTML+=
            `<table id='test'>
            <tr>
            <td class='diktID'>Dikt ID</td>
            <td class='tekst'>Dikt</td>
            <td class='epost'>Eier av dikt</td>
            <td class='slettDikt'>Slett dikt</td>
            <td class='slettDikt'>Endre dikt</td>
            </tr>
            </table>`
        if (count > 0) {
            for (var i = 0; i < count; i++){
                const id = xml.getElementsByTagName("diktID")[i].childNodes[0].nodeValue;
                const tekst = xml.getElementsByTagName("tekst")[i].childNodes[0].nodeValue;
                const epost = xml.getElementsByTagName("epostadresse")[i].childNodes[0].nodeValue;
                if (noe === epost) {
                    deletePoem = `<input type='button' class='slettDiktButton'
                    value='Slett dikt' onClick='deleteOnePoem(${id})'>`;
                    doChangePoem = `<input type='button' class='slettDiktButton' 
                    value='Endre dikt' onClick='showChangePoem(${id}, "${tekst}")'>`;
                } else {
                    deletePoem = "";
                    doChangePoem= "";
                }
                document.getElementById("test").innerHTML += 
                    `<tr class='jupp'>
                        <td class='diktID'>${id}</td>
                        <td class='tekst'>${tekst}</td>
                        <td class='epost'>${epost}</td>
                        <td class='slettDikt'>${deletePoem}</td>
                        <td class='slettDikt'>${doChangePoem}</td>
                    </tr>`
            }
        }
    })
}

function showChangePoem(id, dikt) {
    document.getElementById("showChangePoem").innerHTML+=
    `<form class='endreDiktForm'>
        <textarea class='diktInput' rows='5' cols='60' id='changedPoem' spellcheck='false'>${dikt}</textarea>
        <input class='slettDiktButton' type='button' value='Lagre endringer' onclick='changePoem(${id})'>
    </form>`
}

function showMakeNewPoem() {
    document.getElementById("showMakeNewPoem").innerHTML+=
    `<form class='endreDiktForm'>
        <textarea class='diktInput' rows='5' cols='60' id='addPoem' spellcheck='false'></textarea>
        <input class='slettDiktButton' type='button' value='Lagre dikt' onclick='addNewPoem()'> 
    </form>`
}

function getOnePoem() { //Endre slik at bruker bestemmer id som dikt skal ha som også i lenger ned bytte ut med
    
    fetch(`${myUrl}dikt/2`, {
        method: 'GET',
        Origin: 'http://localhost'
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")
        const count = xml.getElementsByTagName("dikt").length
        document.getElementById("ettDikt").innerHTML+=
            `<table id='test2'>
            <tr>
            <td class='diktID'>Dikt ID</td>
            <td class='tekst'>Dikt</td>
            <td class='epost'>Eier av dikt</td>
            </tr>
            </table>`
        for (var i = 0; i < count; i++){
            const id = xml.getElementsByTagName("diktID")[i].childNodes[0].nodeValue;
            const tekst = xml.getElementsByTagName("tekst")[i].childNodes[0].nodeValue;
            const epost = xml.getElementsByTagName("epostadresse")[i].childNodes[0].nodeValue;
            document.getElementById("test2").innerHTML += 
                `<tr class='jupp'>
                    <td class='diktID'>${id}</td>
                    <td class='tekst'>${tekst}</td>
                    <td class='epost'>${epost}</td>
                </tr>`
        }
    })
}

function login(event) {
    if (event.keyCode == 13 || event == "login")  {

        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;
        
        fetch(`${myUrl}login`, {
            method: 'POST',
            mode: 'no-cors',
            body: "<user><username>"+username+"</username><password>"+password+"</password></user>"
        })
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const xml = parser.parseFromString(data, 
                "application/xml")
            const callStatus = xml.getElementsByTagName("status")[0].textContent;
            loggedInEmail = xml.getElementsByTagName("user")[0].textContent;
            
            if (callStatus == 1) {
                window.location = "test1.html";
                localStorage["loggedInEmail"] = loggedInEmail;
                sessionStorage.setItem('status','loggedIn');
            } else {
                alert("Something went wrong");
            }
        })
    }
}

function getUsername() {
    let user = localStorage["loggedInEmail"];
    document.getElementById("userLoggedIn").innerHTML+=user;
}


function logout() {
    //let sessionId = "07cf470e-3c65-4635-aabb-e8f9417e79b4";
   
    fetch(`${myUrl}logout`, {
        method: 'POST',
        mode: 'no-cors',
        //body: "<user><sessionid>"+sessionId+"</sessionid></user>"
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")
        const callStatus = xml.getElementsByTagName("status")[0].textContent;
        if (callStatus == 1) {
            window.location = "test.html";
            sessionStorage.setItem('status','');
        } else {
            alert("Something went wrong");
        } 
        
    })
}

function addNewPoem() {

    let newPoem = document.getElementById("addPoem").value;

    fetch(`${myUrl}dikt`, {
        method: 'POST',
        mode: 'no-cors',
        body: "<dikt><tekst>"+newPoem+"</tekst></dikt>"
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")
        const callStatus = xml.getElementsByTagName("status")[0].textContent;
        if (callStatus == 1) {
            location.reload();
        } else {
            alert("Something went wrong");
        } 
    })

}



function changePoem(id) {
    let changedPoem = document.getElementById("changedPoem").value;
    //let poemId = document.getElementById("poemId").value;

    fetch(`${myUrl}dikt/${id}`, {
        method: 'PUT',
        body: "<dikt><tekst>"+changedPoem+"</tekst></dikt>"
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")
        const callStatus = xml.getElementsByTagName("status")[0].textContent;
        if (callStatus == 1) {
            location.reload();
        } else {
            alert("Something went wrong");
        } 
    })
}

function deleteOnePoem(id) {
    //let poemIdForDelete = document.getElementById("poemIdForDelete").value;

    fetch(`${myUrl}dikt/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")
        const callStatus = xml.getElementsByTagName("status")[0].textContent;
        if (callStatus == 1) {
            location.reload();
        } else {
            alert("Something went wrong");
        } 
    })
}

function deleteAllMyPoems() {

    if (confirm("Er du sikker på at du vil slette alle dine dikt?") == true) {
        fetch(`${myUrl}dikt`, {
            method: 'DELETE',
        })
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const xml = parser.parseFromString(data, 
                "application/xml")
            const callStatus = xml.getElementsByTagName("status")[0].textContent;
            if (callStatus == 1) {
                location.reload();
            } else {
                alert("Something went wrong");
            } 
        })
    } 
}




