/**
 * Event listener for DOMContentLoaded event.
 * Initializes the calendar and handles form submission.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Set the maximum height of the calendar element
    document.getElementById('calendar').style.maxHeight = '350px';
    // Initialize the FullCalendar instance
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridWeek', // Initial view of the calendar
        eventClick: function(info) {
            info.jsEvent.preventDefault(); // Prevent the default event behavior
            if (info.event.url) {
                window.open(info.event.url, '_blank'); // Open the event URL in a new tab
            }
        },
        eventDidMount: function(info) {
            // Add tooltip to the event element
            var tooltipContent = `
                <strong>${info.event.title}</strong><br>
                <strong>Lecturer:</strong> ${info.event.extendedProps.lecturer}<br>
                <strong>Classroom:</strong> ${info.event.extendedProps.classroom}<br>
                <strong>Location:</strong> ${info.event.extendedProps.location}<br>
                <strong>Address:</strong> ${info.event.extendedProps.address}<br>
                <strong>Start time:</strong> ${info.event.extendedProps.start_time}<br>
                <strong>End time:</strong> ${info.event.extendedProps.end_time}<br>
                <strong>Credits:</strong> ${info.event.extendedProps.credits}<br>
            `;
            tippy(info.el, {
                content: tooltipContent,
                allowHTML: true,
                theme: 'light',
            });
        }
    });

    // Event listener for form submission
    document.getElementById('teaching-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the actual form submission
        // Show the calendar container
        document.getElementById('calendar-container').style.display = 'block';
        document.getElementById('calendar-container').style.height = '350px';
        // Retrieve form values and encode them for URL usage
        var final_teaching = encodeURIComponent(document.querySelector('[name="teaching"]').value);
        // Construct the URL with proper encoding
        var url = `http://localhost:8081/query/${final_teaching}/`;
        // Fetch data from the server
        fetch(url)
           .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ', response.statusText);
                }
                return response.json();
            })
           .then(data => {
                console.log(data);
                var errorMessageEl = document.getElementById('error-message');
                if (data && Object.keys(data).length > 0) {
                    errorMessageEl.textContent = ''; // Clear any previous error messages
                    var events = [];
                    for (var key in data) {
                        if (data.hasOwnProperty(key)) {
                            var lesson = data[key];
                            // Create an event object for each lesson
                            events.push({
                                title: lesson.TEACHING,
                                start: lesson.START_ISO8601,
                                end: lesson.END_ISO8601,
                                url: lesson.URLS_INSEGNAMENTO,
                                extendedProps: {
                                    lecturer: lesson.LECTURER_NAME,
                                    classroom: lesson.CLASSROOM_NAME,
                                    location: lesson.LOCATION_NAME,
                                    address: lesson.ADDRESS,
                                    start_time: lesson.LECTURE_START,
                                    end_time: lesson.LECTURE_END,
                                    credits: lesson.CREDITS,
                                }
                            });
                        }
                    }
                    calendar.removeAllEvents(); // Clear existing events
                    calendar.addEventSource(events); // Add new data
                    // Find the earliest event date and move the calendar to that date
                    var earliestEvent = events.reduce((earliest, event) => {
                        return!earliest || new Date(event.start) < new Date(earliest.start)? event : earliest;
                    }, null);
                    if (earliestEvent) {
                        calendar.gotoDate(new Date(earliestEvent.start));
                    }
                    // Render the calendar after setting the container height
                    calendar.render();
                }
            })
           .catch(error => {
                var errorMessageEl = document.getElementById('error-message');
                errorMessageEl.textContent = 'Error loading the calendar data', error.message;
                console.error('Error loading the calendar data', error);
            });
    });
});
