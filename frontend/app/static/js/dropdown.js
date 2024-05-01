function fetchTeachings () {
    fetch("http://localhost:8081/get_teachings", { mode: 'no-cors' })
        .then((data) => {
            console.log(data);
         });
}

fetchTeachings();