
// Logic to deal with front page image carosel
var images = ['/static/images/bg_img1.png', '/static/images/bg_img2.png', '/static/images/bg_img3.png']
var imgIndex = 0

var main_bg_img = document.getElementById('main_bg_img')
var nextbtn = document.getElementById('next')
var prevbtn = document.getElementById('previous')

// Function that updates the displayed background image depending on the indexed position of the array above called images
document.addEventListener('DOMContentLoaded', () => {
    function updateBackground() {
        main_bg_img.style.backgroundImage = "url('" + images[imgIndex] + "')"
    }

    // Sets up next button that loops through images array and wraps in infinite loop
    nextbtn.addEventListener('click', function() {
        imgIndex++
        if (imgIndex >= images.length) {
            imgIndex = 0
        }
        updateBackground()
    })

    // Same as above but loops backwards through array in infinite loop
    prevbtn.addEventListener('click', function() {
        imgIndex--
        if (imgIndex < 0) {
            imgIndex = images.length - 1
        }
        updateBackground()
    })
})

// Logic to deal with image carousel on each car type 

// The carousel for loop loops through each carousel e.g skoda, then vw, then audi and applies the logic 
// below the loop to each loop with basically the same logic as above
document.addEventListener('DOMContentLoaded', () => {
    const carousels = document.querySelectorAll('.car-info-pic')

    carousels.forEach(carousel => {
        const images = carousel.querySelectorAll('.carousel_image')
        const next = carousel.querySelector('.next2')
        const prev = carousel.querySelector('.previous2')
        let currentIndex = 0

        function showImage(index) {
            images.forEach((img, i) => {
                img.style.display = i === index ? 'block' : 'none';
            });
        }

        showImage(currentIndex)

        next.addEventListener('click', function() {
            currentIndex++
            if (currentIndex >= images.length) currentIndex = 0;
            showImage(currentIndex)
        })

        prev.addEventListener('click', function() {
            currentIndex--
            if (currentIndex < 0) currentIndex = images.length - 1;
            showImage(currentIndex);
        })
    })
})

// Search bar logic

const searchInput = document.getElementById('search')
const resultsContainer = document.getElementById('carData')

// When user types will search cars in database, if what is typed doesn't match the title or description from the db
// then nothing with show
searchInput.addEventListener('input', e => {
    const value = e.target.value.toLowerCase()
    if (value === "") {
        resultsContainer.innerHTML = ""
        return
    }
    const filtered = allInfo.filter(item => 
        item.title.toLowerCase().includes(value) || item.description.toLowerCase().includes(value)
    )
    renderResults(filtered)
})


function renderResults(cars) {
    resultsContainer.innerHTML = ""
    if (cars.length === 0) {
        resultsContainer.innerHTML = "<p>No cars found</p>"
    }

    cars.forEach(car => {
        const carDiv = document.createElement('div')
        carDiv.innerHTML = `<h3>${car.title}</h3><p>${car.description}</p>`;
        resultsContainer.appendChild(carDiv)
    })
}