var images = {
    up: [
        "static/img/sprite_charactere/ashup1.svg",
        "static/img/sprite_charactere/ashup2.svg",
    ],
    down: [
        "static/img/sprite_charactere/ashdown1.svg",
        "static/img/sprite_charactere/ashdown2.svg",
    ],
    left: [
        "static/img/sprite_charactere/ashleft1.svg",
        "static/img/sprite_charactere/ashleft2.svg",
    ],
    right: [
        "static/img/sprite_charactere/ashright1.svg",
        "static/img/sprite_charactere/ashright2.svg",
    ],
};
var currentImageIndex = { up: 0, down: 0, left: 0, right: 0 };

document.addEventListener("keydown", function (event) {
    var image = document.getElementById("movingImage");
    var top = parseInt(image.style.top) || 0;
    var left = parseInt(image.style.left) || 0;
    var step = 10;
    var direction;

    switch (event.key) {
        case "ArrowUp":
            image.style.top = top - step + "px";
            direction = "up";
            break;
        case "ArrowDown":
            image.style.top = top + step + "px";
            direction = "down";
            break;
        case "ArrowLeft":
            image.style.left = left - step + "px";
            direction = "left";
            break;
        case "ArrowRight":
            image.style.left = left + step + "px";
            direction = "right";
            break;
    }

    if (direction) {
        image.src = images[direction][currentImageIndex[direction]];
        currentImageIndex[direction] = 1 - currentImageIndex[direction]; // switch between 0 and 1
    }
});