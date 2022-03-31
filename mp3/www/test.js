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
    
    //Get kall for å hente alle dikt
    fetch(`${myUrl}dikt/`, {
        method: 'GET',
        Origin: 'http://localhost'
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")

        //Teller antall dikt 
        const count = xml.getElementsByTagName("dikt").length

        //Henter epost til innlogget bruker
        const userEmail = document?.getElementById("userLoggedIn")?.textContent;

        //Variabler som skal bruker til å vise slette og endre dikt knapper
        let deletePoem;
        let doChangePoem;

        //Sjekker om det er dikt i databasen
        if (count > 0) {

        //Sender dokument med html som viser overskriftene
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

            //Looper gjennom alle diktene for å vise alle
            for (var i = 0; i < count; i++){

                //Henter ut id, dikt og epost til hver av diktene
                const id = xml.getElementsByTagName("diktID")[i].childNodes[0].nodeValue;
                const tekst = xml.getElementsByTagName("tekst")[i].childNodes[0].nodeValue;
                const epost = xml.getElementsByTagName("epostadresse")[i].childNodes[0].nodeValue;

                //Hvis innlogget bruker er samme som eier av dikt vis knappene, hvis ikke, ikke vis dem
                if (userEmail === epost) {
                    deletePoem = `<input type='button' class='slettDiktButton'
                    value='Slett dikt' onClick='deleteOnePoem(${id})'>`;
                    doChangePoem = `<input type='button' class='slettDiktButton' 
                    value='Endre dikt' onClick='showChangePoem(${id}, "${tekst}")'>`;
                } else {
                    deletePoem = "";
                    doChangePoem= "";
                }

                //Sender dokument med html med alle diktene i databasen
                document.getElementById("test").innerHTML += 
                    `<tr>
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

function showChangePoem(showChangePoemId, dikt) {
    document.getElementById("showMakeNewPoem").innerHTML=""
    document.getElementById("showChangePoem").innerHTML=""
    document.getElementById("showChangePoem").innerHTML+=
    `<form class='endreDiktForm'>
        <textarea class='diktInput' rows='5' cols='60' id='changedPoem' spellcheck='false'>${dikt}</textarea>
        <input class='slettDiktButton' type='button' value='Lagre endringer' onclick='changePoem(${showChangePoemId})'>
    </form>`
}

function showMakeNewPoem() {
    document.getElementById("showChangePoem").innerHTML=""
    document.getElementById("showMakeNewPoem").innerHTML=""
    document.getElementById("showMakeNewPoem").innerHTML+=
    `<form class='endreDiktForm'>
        <textarea class='diktInput' rows='5' cols='60' id='addPoem' spellcheck='false'></textarea>
        <input class='slettDiktButton' type='button' value='Lagre dikt' onclick='addNewPoem()'> 
    </form>`
}

function getOnePoem() { //Endre slik at bruker bestemmer id som dikt skal ha som også i lenger ned bytte ut med
    
    //Fjerner forrige resultat hvis det er noe
    document.getElementById("ettDikt").innerHTML="";
    
    //Henter diktid som er tastet inn
    let id = document.getElementById("diktId").value;

    //Setter diktid feltet tomt etter at diktid er hentet
    document.getElementById("diktId").value = "";
    
    //Kjører GET kallet for å hente et dikt ved hjelp av id
    fetch(`${myUrl}dikt/${id}`, {
        method: 'GET',
        Origin: 'http://localhost'
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const xml = parser.parseFromString(data, 
            "application/xml")

        //Antall tegn i diktet
        const count = xml.getElementsByTagName("dikt")[0].textContent.length;

        //Lagrer eposten til bruker som er logget inn
        const userEmail = document?.getElementById("userLoggedIn")?.textContent;

        //Variabler som skal vise slett dikt og endre dikt knappene
        let deletePoem;
        let doChangePoem;

        //Sjekker at kallet inneholder et dikt
        if (count > 0) {

            //Sender dokument med html som viser overskriftene
            document.getElementById("ettDikt").innerHTML+=
                `<table id='test2'>
                <tr>
                <td class='diktID'>Dikt ID</td>
                <td class='tekst'>Dikt</td>
                <td class='epost'>Eier av dikt</td>
                <td class='slettDikt'>Slett dikt</td>
                <td class='slettDikt'>Endre dikt</td>
                </tr>
                </table>`

                //Henter id, dikt og epost til valgt dikt fra databasen
                const id = xml.getElementsByTagName("diktID")[0].childNodes[0].nodeValue;
                const poem = xml.getElementsByTagName("tekst")[0].childNodes[0].nodeValue;
                const email = xml.getElementsByTagName("epostadresse")[0].childNodes[0].nodeValue;

                //Hvis eier av dikt er samme som er logget inn, vis knappene, hvis ikke: ikke vis dem
                if (userEmail === email) {
                    deletePoem = `<input type='button' class='slettDiktButton'
                    value='Slett dikt' onClick='deleteOnePoem(${id})'>`;
                    doChangePoem = `<input type='button' class='slettDiktButton' 
                    value='Endre dikt' onClick='showChangePoem(${id}, "${poem}")'>`;
                } else {
                    deletePoem = "";
                    doChangePoem= "";
                }

                //Sender document med html for å vise diktet som er valgt
                document.getElementById("test2").innerHTML+= 
                    `<tr>
                        <td class='diktID'>${id}</td>
                        <td class='tekst'>${poem}</td>
                        <td class='epost'>${email}</td>
                        <td class='slettDikt'>${deletePoem}</td>
                        <td class='slettDikt'>${doChangePoem}</td>
                    </tr>`
        } else {
            document.getElementById("ettDikt").innerHTML=""
            document.getElementById("test2").innerHTML=""
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

    if (confirm("Er du sikker på at du vil slette alle diktene dine?") == true) {
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




