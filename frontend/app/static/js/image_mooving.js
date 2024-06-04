/**
 * Selects the aperitivo image and adds event listeners for resize and mousemove.
 * Calculates and stores the initial center position of the image.
 */
const aperitivoImage = document.querySelector('.img_aperitivo'); // Select the aperitivo image

window.addEventListener('resize', calculateAperitivoCenterPosition); // Add resize event listener
aperitivoImage.addEventListener('mousemove', handleAperitivoMouseMove); // Add mousemove event listener

/**
 * Calculates the center position of the aperitivo image and stores it in data attributes.
 */
function calculateAperitivoCenterPosition() {
  const offsetX = aperitivoImage.offsetWidth / 2; // Calculate horizontal center position
  const offsetY = aperitivoImage.offsetHeight / 2; // Calculate vertical center position

  aperitivoImage.dataset.offsetX = offsetX; // Store horizontal center in data attribute
  aperitivoImage.dataset.offsetY = offsetY; // Store vertical center in data attribute
}

/**
 * Handles mousemove event for the aperitivo image.
 * Calculates the mouse movement and applies translation to the image.
 * @param {MouseEvent} event - The mousemove event object
 */
function handleAperitivoMouseMove(event) {
  const offsetX = parseFloat(aperitivoImage.dataset.offsetX); // Retrieve horizontal center from data attribute
  const offsetY = parseFloat(aperitivoImage.dataset.offsetY); // Retrieve vertical center from data attribute

  const dx = event.offsetX - offsetX; // Calculate horizontal mouse movement
  const dy = event.offsetY - offsetY; // Calculate vertical mouse movement

  const translateX = -dx / 10; // Calculate horizontal image translation (divided by a value for sensitivity)
  const translateY = -dy / 10; // Calculate vertical image translation (divided by a value for sensitivity)

  aperitivoImage.style.transform = `translate(${translateX}px, ${translateY}px)`; // Apply translation to image style
}

calculateAperitivoCenterPosition(); // Call function to calculate initial center position

/**
 * Selects the university image and adds event listeners for resize and mousemove.
 * Calculates and stores the initial center position of the image.
 */
const universityImage = document.querySelector('.img_unive'); // Select the university image

window.addEventListener('resize', calculateUniversityCenterPosition); // Add resize event listener
universityImage.addEventListener('mousemove', handleUniversityMouseMove); // Add mousemove event listener

/**
 * Calculates the center position of the university image and stores it in data attributes.
 */
function calculateUniversityCenterPosition() {
  const offsetX = universityImage.offsetWidth / 2; // Calculate horizontal center position
  const offsetY = universityImage.offsetHeight / 2; // Calculate vertical center position

  universityImage.dataset.offsetX = offsetX; // Store horizontal center in data attribute
  universityImage.dataset.offsetY = offsetY; // Store vertical center in data attribute
}

/**
 * Handles mousemove event for the university image.
 * Calculates the mouse movement and applies translation to the image.
 * @param {MouseEvent} event - The mousemove event object
 */
function handleUniversityMouseMove(event) {
  const offsetX = parseFloat(universityImage.dataset.offsetX); // Retrieve horizontal center from data attribute
  const offsetY = parseFloat(universityImage.dataset.offsetY); // Retrieve vertical center from data attribute

  const dx = event.offsetX - offsetX; // Calculate horizontal mouse movement
  const dy = event.offsetY - offsetY; // Calculate vertical mouse movement

  const translateX = -dx / 10; // Calculate horizontal image translation (divided by a value for sensitivity)
  const translateY = -dy / 10; // Calculate vertical image translation (divided by a value for sensitivity)

  universityImage.style.transform = `translate(${translateX}px, ${translateY}px)`; // Apply translation to image style
}

calculateUniversityCenterPosition(); // Call function to calculate initial center position