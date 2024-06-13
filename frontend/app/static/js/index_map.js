// Center the map
var map = L.map('mapid').setView([45.56725098422657, 12.334428207238425], 10);

// Add base layer from OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Ca' Foscari icon
var icon = L.icon({
    iconUrl: '../static/img/index/icon_map.png',
    iconSize: [30, 45], // size of the icon (same as Leaflet default)
    popupAnchor: [0, -15] // point from which the popup should open relative to the iconAnchor
});

// Auditorium Santa Margherita - Emanuele Severino
var santa_margherita = L.marker([45.43511855743733, 12.324109784032798], {icon: icon}).addTo(map);

santa_margherita.bindPopup('Auditorium Santa Margherita - Emanuele Severino');

santa_margherita.on('mouseover', function (e) {
    this.openPopup();
});
santa_margherita.on('mouseout', function (e) {
    this.closePopup();
});

// Aula Barbarigo
var barbarigo = L.marker([45.43220955105785, 12.3182890245113], { icon: icon }).addTo(map);

barbarigo.bindPopup('Aula Barbarigo');

barbarigo.on('mouseover', function (e) {
    this.openPopup();
});
barbarigo.on('mouseout', function (e) {
    this.closePopup();
});

// Aula San Trovaso
var san_trovaso = L.marker([45.431472340352116, 12.321119026361222], { icon: icon }).addTo(map);

san_trovaso.bindPopup('Aula San Trovaso');

san_trovaso.on('mouseover', function (e) {
    this.openPopup();
});
san_trovaso.on('mouseout', function (e) {
    this.closePopup();
});

// Ca' Bernardo
var ca_bernardo = L.marker([45.433998954133536, 12.326750527719181], { icon: icon }).addTo(map);

ca_bernardo.bindPopup('Ca\' Bernardo');

ca_bernardo.on('mouseover', function (e) {
    this.openPopup();
});
ca_bernardo.on('mouseout', function (e) {
    this.closePopup();
});

// Ca' Bottacin
var ca_bottacin = L.marker([45.43567624200541, 12.326510611018529], { icon: icon }).addTo(map);

ca_bottacin.bindPopup('Ca\' Bottacin');

ca_bottacin.on('mouseover', function (e) {
    this.openPopup();
});
ca_bottacin.on('mouseout', function (e) {
    this.closePopup();
});

// Ca' Dolfin - Saoneria
var ca_dolfin = L.marker([45.435158071807344, 12.325491224511394], { icon: icon }).addTo(map);

ca_dolfin.bindPopup('Ca\' Dolfin - Saoneria');

ca_dolfin.on('mouseover', function (e) {
    this.openPopup();
});
ca_dolfin.on('mouseout', function (e) {
        this.closePopup();
});

// Campus scientifico via Torino (edificio Alfa)
var via_torino_alfa = L.marker([45.47823471602134, 12.254419026967057], { icon: icon }).addTo(map);

via_torino_alfa.bindPopup('Campus scientifico via Torino (edificio Alfa)');

via_torino_alfa.on('mouseover', function (e) {
    this.openPopup();
});
via_torino_alfa.on('mouseout', function (e) {
    this.closePopup();
});

// Campus scientifico via Torino (edificio Beta)
var via_torino_beta = L.marker([45.47882807744185, 12.25467700647536], { icon: icon }).addTo(map);

via_torino_beta.bindPopup('Campus scientifico via Torino (edificio Beta)');

via_torino_beta.on('mouseover', function (e) {
    this.openPopup();
});
via_torino_beta.on('mouseout', function (e) {
    this.closePopup();
});

// Campus scientifico via Torino (edificio Delta)
var via_torino_delta = L.marker([45.47813835557259, 12.255994557756196], { icon: icon }).addTo(map);

via_torino_delta.bindPopup('Campus scientifico via Torino (edificio Delta)');

via_torino_delta.on('mouseover', function (e) {
    this.openPopup();
});
via_torino_delta.on('mouseout', function (e) {
    this.closePopup();
});

// Campus scientifico via Torino (edificio Epsilon)
var via_torino_epsilon = L.marker([45.477930929370324, 12.255207235362874], { icon: icon }).addTo(map);

via_torino_epsilon.bindPopup('Campus scientifico via Torino (edificio Epsilon)');

via_torino_epsilon.on('mouseover', function (e) {
    this.openPopup();
});
via_torino_epsilon.on('mouseout', function (e) {
    this.closePopup();
});

// Campus scientifico via Torino (edificio Zeta)
var via_torino_zeta = L.marker([45.47915625306922, 12.256161940647212], { icon: icon }).addTo(map);

via_torino_zeta.bindPopup('Campus scientifico via Torino (edificio Zeta)');

via_torino_zeta.on('mouseover', function (e) {
    this.openPopup();
});
via_torino_zeta.on('mouseout', function (e) {
    this.closePopup();
});

// Cinema Multisala Rossini
var multisala_rossini = L.marker([45.43530778578384, 12.333141999375671], { icon: icon }).addTo(map);

multisala_rossini.bindPopup('Cinema Multisala Rossini');

multisala_rossini.on('mouseover', function (e) {
    this.openPopup();
});
multisala_rossini.on('mouseout', function (e) {
    this.closePopup();
});

// H-Campus
45.56593722994548, 12.43053660767573
var h_campus = L.marker([45.56593722994548, 12.43053660767573], { icon: icon }).addTo(map);

h_campus.bindPopup('H-Campus');

h_campus.on('mouseover', function (e) {
    this.openPopup();
});
h_campus.on('mouseout', function (e) {
    this.closePopup();
});

// Malcanton Marcorà
var malcanton_marcora = L.marker([45.43499238683551, 12.321784124511414], { icon: icon }).addTo(map);

malcanton_marcora.bindPopup('Malcanton Marcorà');

malcanton_marcora.on('mouseover', function (e) {
    this.openPopup();
});
malcanton_marcora.on('mouseout', function (e) {
    this.closePopup();
});

// Marghera - Vega
var marghera_vega = L.marker([45.47401917548411, 12.252929212870168], { icon: icon }).addTo(map);

marghera_vega.bindPopup('Marghera - Vega');

marghera_vega.on('mouseover', function (e) {
    this.openPopup();
});
marghera_vega.on('mouseout', function (e) {
    this.closePopup();
});

// Palazzina Briati
var palazzo_briati = L.marker([45.43389986020116, 12.320509997525628], { icon: icon }).addTo(map);

palazzo_briati.bindPopup('Palazzina Briati');

palazzo_briati.on('mouseover', function (e) {
    this.openPopup();
});
palazzo_briati.on('mouseout', function (e) {
    this.closePopup();
});

// Palazzo Cosulich
var palazzo_cosulich = L.marker([45.4304343380146, 12.323546619776113], { icon: icon }).addTo(map);

palazzo_cosulich.bindPopup('Palazzo Cosulich');

palazzo_cosulich.on('mouseover', function (e) {
    this.openPopup();
});
palazzo_cosulich.on('mouseout', function (e) {
    this.closePopup();
});

// Palazzo Moro
var palazzo_moro = L.marker([45.44676095973912, 12.321201355990127], { icon: icon }).addTo(map);

palazzo_moro.bindPopup('Palazzo Moro');

palazzo_moro.on('mouseover', function (e) {
    this.openPopup();
});
palazzo_moro.on('mouseout', function (e) {
    this.closePopup();
});

// Polo didattico San Basilio (Architettura temporanea)
var basilio_architettura = L.marker([45.43188809381335, 12.316072739854128], { icon: icon }).addTo(map);

basilio_architettura.bindPopup('Polo didattico San Basilio (Architettura temporanea)');

basilio_architettura.on('mouseover', function (e) {
    this.openPopup();
});
basilio_architettura.on('mouseout', function (e) {
    this.closePopup();
});

// Polo didattico San Basilio (Magazzino 5)
var basilio_5 = L.marker([45.431983064548234, 12.317514226361292], { icon: icon }).addTo(map);

basilio_5.bindPopup('Polo didattico San Basilio (Magazzino 5)');

basilio_5.on('mouseover', function (e) {
    this.openPopup();
});
basilio_5.on('mouseout', function (e) {
    this.closePopup();
});

// Rio Nuovo
var rio_nuovo = L.marker([45.43472735904168, 12.326172353347136], { icon: icon }).addTo(map);

rio_nuovo.bindPopup('Rio Nuovo');

rio_nuovo.on('mouseover', function (e) {
    this.openPopup();
});
rio_nuovo.on('mouseout', function (e) {
    this.closePopup();
});

// San Giobbe
var san_giobbe = L.marker([45.44613080667995, 12.318038015048456], { icon: icon }).addTo(map);

san_giobbe.bindPopup('San Giobbe');

san_giobbe.on('mouseover', function (e) {
    this.openPopup();
});
san_giobbe.on('mouseout', function (e) {
    this.closePopup();
});

// San Sebastiano
45.43222381997808, 12.32035429195265
var san_sebastiano = L.marker([45.44613080667995, 12.318038015048456], { icon: icon }).addTo(map);

san_sebastiano.bindPopup('San Sebastiano');

san_sebastiano.on('mouseover', function (e) {
    this.openPopup();
});
san_sebastiano.on('mouseout', function (e) {
    this.closePopup();
});

// Santa Marta
45.433266104554306, 12.313814988449053
var santa_marta = L.marker([45.433266104554306, 12.313814988449053], { icon: icon }).addTo(map);

santa_marta.bindPopup('Santa Marta');

santa_marta.on('mouseover', function (e) {
    this.openPopup();
});
santa_marta.on('mouseout', function (e) {
    this.closePopup();
});

// Treviso - Palazzo San Leonardo
var treviso_san_leonardo = L.marker([45.66455042583218, 12.249722870549677], { icon: icon }).addTo(map);

treviso_san_leonardo.bindPopup('Treviso - Palazzo San Leonardo');

treviso_san_leonardo.on('mouseover', function (e) {
    this.openPopup();
});
treviso_san_leonardo.on('mouseout', function (e) {
    this.closePopup();
});

// Treviso - Palazzo San Paolo
var treviso_san_paolo = L.marker([45.66382354750634, 12.25014985520678], { icon: icon }).addTo(map);

treviso_san_paolo.bindPopup('Treviso - Palazzo San Paolo');

treviso_san_paolo.on('mouseover', function (e) {
    this.openPopup();
});
treviso_san_paolo.on('mouseout', function (e) {
    this.closePopup();
});