/**
 * Event listener for the form submission.
 * Fetches events data from the server, saves it to local storage, and shows the calendar container.
 */
document.getElementById('teaching-form').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent the actual form submission

  document.getElementById('download-container').style.display = 'block';

  // Retrieve form values and encode them for URL usage
  var final_teaching = encodeURIComponent(document.querySelector('[name="teaching"]').value);

  // Construct the URL with proper encoding
  var url = `http://localhost:8081/query/${final_teaching}/`;

  // Fetch the data
  fetch(url)
    .then(response => response.json()) // Assume the server returns a JSON
    .then(events => {
      // Save events to local storage to be used later
      localStorage.setItem('events', JSON.stringify(events));
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
});

/**
 * Event listener for the download button click.
 * Retrieves events from local storage, constructs an ICS file content, and triggers the download.
 */
document.getElementById('download-button').addEventListener('click', function () {
  // Retrieve events from local storage
  let events = JSON.parse(localStorage.getItem('events'));

  if (events && Object.keys(events).length > 0) {
    // Start constructing the ICS content
    let icsContent = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Product//Your Application//EN
CALSCALE:GREGORIAN
TZID:Europe/Rome\n`; // Added TZID parameter with Rome time zone

    // Iterate over the events and add each one to the ICS content
    Object.values(events).forEach(event => {
      // Format the start and end dates to the correct ICS format (no changes needed here)
      let dtstart = event.START_ISO8601.replace(/[-:]/g, '').split('.')[0] + 'Z';
      let dtend = event.END_ISO8601.replace(/[-:]/g, '').split('.')[0] + 'Z';
  
      icsContent += `BEGIN:VEVENT
DTSTART:${dtstart}
DTEND:${dtend}
SUMMARY:${event.TEACHING}
DESCRIPTION:Professor: ${event.LECTURER_NAME}\nLocation: ${event.LOCATION_NAME}\nDetails: ${event.URLS_INSEGNAMENTO}
LOCATION:${event.ADDRESS}
URL:${event.URLS_INSEGNAMENTO}
END:VEVENT\n`;
    });

    // Close the VCALENDAR
    icsContent += `END:VCALENDAR`;

    // Create a blob with the content of the file
    var blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });

    // Create a link to download the file
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `calendar.ics`;

    // Append the link to the DOM and trigger the download
    document.body.appendChild(link);
    link.click();

    // Remove the link from the DOM
    document.body.removeChild(link);
  } else {
    console.error('No events available for download or events data is not valid.');
  }
});
