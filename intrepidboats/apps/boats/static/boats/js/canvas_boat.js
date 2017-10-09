/**
 *  Welcome to this (poor) Jquery plugin!
 *  Version: 0.1
 *
 *  Draw a boat according to its "layers" on a html5 canvas.
 *  Requirements:
 *      - The canvas must have the following data attributes (all prefixed with "data-boat-"):
 *          * slug: boat slug for future colorize requests
 *          * base: a url to the background boat image. Must match the src attr from base-img
 *          * hull: a url to the default hull boat image. Must match the src attr from hull-img
 *
 *  Public API:
 *
 *  $el.boatCanvas("init"):
 *      Draw the initial state of the boat on a canvas tag.
 *
 *  $el.boatCanvas("download", $link, fileName):
 *      $link: Jquery object, should be wrapping anchor tags
 *      fileName: name for the downloaded file (e.g. "boat.png")
 *
 *      Setup event for downloading the canvas as a PNG image called "fileName" when clicking on $link
 *
 *  $el.boatCanvas("redraw", layerKey, color):
 *      layerKey: Layer to colorize
 *      color: hexadecimal color without "#" (e.g. 5499C7)
 *
 *      Request to the server the specific layer colorized with a color.
 *      Colors must be hexadecimal.
 *      Available layers are described at BOAT_DRAW_ORDER (see source)
 *
 *  $el.boatCanvas("clear", layerKey or "all")
 *      Restore a layer to its default.
 *      Must of them aren't shown, but hull image is back to default color.
 *      if "all" keyword is used, all layers are cleared
 *
 *  Limitations:
 *      - Canvas
 *      - I highly recommend loading the images in some img tags, avoiding rendering errors
 *
 * */
$(function () {

    /* PLUGIN FUNCTIONS AND VARS */

    var BOAT_DATA_IMAGES = "boatImages",
        BOAT_BASE = "boatBase",
        BOAT_HULL = "boatHull",
        BOAT_SLUG = "boatSlug",
        BOAT_LOGO = "boatLogo",
        BOAT_MOTOR = "boatMotor";

    var TOP_FEATURE = "boatTop",
        ANCHOR_FEATURE = "boatAnchor",
        BOW_RAIL = "boatBowRail",
        RUB_RAIL = "boatRubRail",
        REAR_CLOSEOUT = "boatRearCloseout",
        DIVE_DOOR = "boatDiveDoor",
        PORT_LIGHTS = "boatPortLight",
        SS_RUB_RAIL_INSERT = "boatSsRubRailInsert";

    var BOAT_DRAW_ORDER = [
        BOAT_BASE,
        BOAT_HULL,
        'boatBootStripe',
        'boatBootStripeAccent',
        'boatSheerStripe',
        'boatSheerStripeAccent',
        BOAT_MOTOR,
        TOP_FEATURE, // <-- Boolean feature
        ANCHOR_FEATURE, // <-- Boolean feature

        BOW_RAIL,
        RUB_RAIL, // <-- Feature with options!
        REAR_CLOSEOUT,
        DIVE_DOOR, // <-- Boolean feature
        PORT_LIGHTS,
        SS_RUB_RAIL_INSERT, // <-- Boolean feature
        BOAT_LOGO
    ];

    var initBoat = function (canvas) {
        var data = getDefaultData(canvas);
        saveData(canvas, BOAT_DATA_IMAGES, data);
        redrawBoat(canvas);
    };

    var resetBoat = function (canvas) {
        initBoat(canvas)
    };

    var resetImage = function (canvas, imageKey) {
        var data = getData(canvas, BOAT_DATA_IMAGES);
        data.images[imageKey] = getDefaultData(canvas).images[imageKey];
        saveData(canvas, BOAT_DATA_IMAGES, data);
        redrawBoat(canvas);
    };


    var drawImage = function (canvas, name, path) {
        var data = getData(canvas, BOAT_DATA_IMAGES);
        data.images[name] = path;
        saveData(canvas, BOAT_DATA_IMAGES, data);
        var tmpImage = new Image();
        tmpImage.onload = function () {
            redrawBoat(canvas);
        };
        tmpImage.src = path;
    };

    var _drawNext = function (others, canvas, images, ctx) {
        if (others.length > 0) {
            var value = others.shift();
            _drawInOrder(value, others, canvas, images, ctx);
        }
    };

    var _drawInOrder = function (value, others, canvas, images, ctx) {
        if (value && images[value]) {
            var src = images[value];
            var img = new Image();
            img.onload = function () {
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                _drawNext(others, canvas, images, ctx);
            };
            img.src = src;
        } else {
            _drawNext(others, canvas, images, ctx);
        }
    };

    var redrawBoat = function (canvas) {
        var data = getData(canvas, BOAT_DATA_IMAGES);
        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height); // <<---- Magic "reset" o/
        var images = data.images;

        var _drawOrder = BOAT_DRAW_ORDER.slice(0);
        var value = _drawOrder.shift(); // I'm assuming there's at least one layer
        _drawInOrder(value, _drawOrder, canvas, images, ctx);

    };

    var drawColorized = function (aCanvas, imageKey, color) {
        var image = getImageKey(imageKey);
        var path = buildImagePath(aCanvas, image, color);
        drawImage(aCanvas, imageKey, path);
    };

    /* JUST UTILS FUNCTIONS */

    var buildData = function (base, hull, logo, rubRail) {
        return {
            images: {
                boatBase: base,
                boatHull: hull,
                boatLogo: logo,
                boatRubRail: rubRail
            }
        };
    };

    var getDefaultData = function (canvas) {
        var boatBase = canvas.dataset[BOAT_BASE],
            boatLogo = canvas.dataset[BOAT_LOGO],
            boatHull = canvas.dataset[BOAT_HULL],
            boatRubRail = canvas.dataset[RUB_RAIL];
        return buildData(boatBase, boatHull, boatLogo, boatRubRail);
    };

    var buildImagePath = function (canvas, image, color) {
        var slug = canvas.dataset[BOAT_SLUG];
        return Urls["boats:colorize"](slug, image, color)
    };

    function firstToLowerCase(str) {
        return str.substr(0, 1).toLowerCase() + str.substr(1);
    }

    var toUnderscore = function (string) {
        return string.replace(/([A-Z])/g, function ($1) {
            return "_" + $1.toLowerCase();
        });
    };

    var getImageKey = function (key) {
        var realKey = toUnderscore(firstToLowerCase(key.replace(/^boat/, "")));
        return realKey.toLowerCase();
    };


    var _assertArgument = function (args, expected, error) {
        if (args.length != expected) {
            throw error;
        }
    };

    var getData = function (canvas, key) {
        return JSON.parse(canvas.dataset[key]);
    };

    var saveData = function (canvas, key, data) {
        canvas.dataset[key] = JSON.stringify(data);

    };


    (function ($) {

        $.fn.boatCanvas = function () {
            if (arguments.length == 0) {
                throw "Must pass an action: init or draw"
            }
            var action = arguments[0];

            if (action === "init") {
                // Only apply to canvas!
                this.filter("canvas").each(function (index, aCanvas) {
                    initBoat(aCanvas);
                });
                return this;
            }

            if (action === "redraw") {
                _assertArgument(arguments, 3, "Must pass 'imageKey' and hexadecimal 'color'");
                var imageKey = arguments[1], color = arguments[2];
                this.filter("canvas").each(function (index, aCanvas) {
                    drawColorized(aCanvas, imageKey, color);
                });
                return this;
            }
            if (action === "drawMotor") {
                _assertArgument(arguments, 2, "Must pass an image 'path'");
                var imagePath = arguments[1];
                this.filter("canvas").each(function (index, aCanvas) {
                    drawImage(aCanvas, BOAT_MOTOR, imagePath);
                });
                return this;
            }
            if (action === "setLayer") {
                _assertArgument(arguments, 3, "Must pass an layer name and a image path");
                var layerName = arguments[1], layerImage = arguments[2];
                this.filter("canvas").each(function (index, aCanvas) {
                    if (layerImage === "" || layerImage === undefined) {
                        resetImage(aCanvas, layerName);
                    } else {
                        drawImage(aCanvas, layerName, layerImage);
                    }
                });
                return this;
            }

            if (action == "clear") {
                _assertArgument(arguments, 2, "Must pass a 'imageKey' to be cleared or 'all' keyword");
                var clearImageKey = arguments[1];
                if (clearImageKey === "all") {
                    this.filter("canvas").each(function (index, aCanvas) {
                        resetBoat(aCanvas);
                    });
                } else {
                    this.filter("canvas").each(function (index, aCanvas) {
                        resetImage(aCanvas, clearImageKey);
                    });
                }
            }
            if (action === "download") {
                _assertArgument(arguments, 3, "Must pass download 'anchor'");
                var $link = arguments[1], fileName = arguments[2];
                this.filter("canvas").each(function (index, aCanvas) {
                    $link.click(function () {
                        $link.attr("href", aCanvas.toDataURL());
                        $link.attr("download", fileName);
                    });
                });
            }

            if (action === "getLink") {
                var aCanvas = this.get(0);
                return aCanvas.toDataURL();
            }

        };

    }(jQuery));

});
