/**
 * In your face angular/react developer!
 *
 * You are not expected to understand this.
 *
 * */

$(document).ready(function () {
    var shareButton = $('#build-a-boat-share-button');
    var submit_button_background = shareButton.css('background');

    function toggleShareButtonDisabled(selectedStep) {
        shareButton.attr('disabled', !(selectedStep.id == 'features-tab'));
        if (shareButton.attr('disabled') == 'disabled') {
            shareButton.css('background', 'grey');
        } else {
            shareButton.css('background', submit_button_background);
        }
    }

    function uncheckAllRadioButtons() {
        $('#match-color-to div input').removeClass('active').prop('checked', false);
    }

    function toggleHiddenRadioButtons(tabId) {
        var radioButtonsContainer = $('#match-color-to');
        radioButtonsContainer.find('div').removeClass('hidden');
        var buttonToBeHidden = $('#' + tabId + 'RadioButton');
        if (buttonToBeHidden.length) {
            buttonToBeHidden.addClass('hidden');
            radioButtonsContainer.removeClass('one-is-hidden');
        } else {
            radioButtonsContainer.addClass('one-is-hidden');
        }
    }

    var drawColorPicker = function ($link, event, canvas, $pickerContainer) {
        $link.addClass("active").siblings().removeClass('active');
        var idString = event.target.id;
        var sampleId = $(".sample#" + idString + 'Sample');

        $pickerContainer.empty().append('<span id="color-container"></span>').find('span').ColorPickerSliders({
            color: sampleId.data("color"),
            flat: true,
            swatches: false,
            order: {
                hsl: 1
            },
            labels: {
                hslhue: 'Color',
                hsllightness: 'Shade'
            },
            onchange: function (container, color) {
                sampleId
                    .css("background-color", color.tiny.toRgbString())
                    .data("color", color.tiny.toHex());
            }
        }).bind({
            // Catch mouseup anywhere, if mousedown was inside color picker
            mousedown: function () {
                $(document).on('mouseup.colorPicker', function () {
                    sampleId.css("visibility", "initial");
                    canvas.boatCanvas("redraw", idString, sampleId.data("color"));
                    $(this).off('mouseup.colorPicker');
                    uncheckAllRadioButtons();
                });
            }
        });

    };

    $('.close-color-picker').click(function (e) {
        e.preventDefault();
        $('.dropup').removeClass('open');
        $('a.tab-option, a.color-select').removeClass('active');
    });

    /*
     Just draw the boat on a canvas!
     * */
    var drawBoat = function ($buildABoatTab, $shareElement) {

        var canvas = $buildABoatTab.find("#built-boat");
        canvas.boatCanvas("init");
        canvas.boatCanvas("download", $shareElement, "boat.png");

        return canvas;
    };


    /*
     * currently there're 4 sections:
     * - The progress list at the left: ".left-progress-list"
     * - the progress list over the boat: ".inline-progress-list"
     * - Where color picker and options per tab are rendered: ".progress-list-options"
     * - Extra content for showing info: ".progress-list-contents"
     * */
    var enableProgressList = function (canvas, $buildABoatTab) {
        var $inlineProgressList = $buildABoatTab.find(".inline-progress-list");
        var $options = $buildABoatTab.find(".progress-list-options");
        var $progressList = $buildABoatTab.find(".left-progress-list");
        var $contents = $buildABoatTab.find('.progress-list-contents');

        var $hullTab = $progressList.find("#hull-tab");
        var $motorTab = $progressList.find("#motor-tab");
        var $otherFeatures = $progressList.find("#features-tab");

        // On selecting a tab at the left, select the same at list over boat.
        // Also Show options and content if any.

        var hideOptionsAndContent = function () {
            $options.removeClass("hidden"); // Content and options are hidden by default!
            $contents.removeClass("hidden");
            $options.children("div.progress-list-option").hide();
            $contents.children("div.progress-list-content").hide();
            // deactivate progress list items!
            $inlineProgressList.find("li.inline-item").removeClass("active disabled-link");
            $progressList.find("li.left-item").removeClass("active")
                .find(".link-collapse").removeClass("disabled-link");
            $('.dropup').removeClass('open');
            $('a.tab-option, a.color-select').removeClass('active');
        };

        var displayTab = function ($el) {
            var formSubmitted = ($('#share-success-message').css('display') != 'none');
            if (!formSubmitted) {
                toggleShareButtonDisabled($el[0]);
            }
            hideOptionsAndContent();
            $el.addClass("active"); // Activate this tab!
            $el.siblings().find(".table.list").fadeOut();
            $el.find(".table.list").fadeIn();

            // Something like 'motor' or 'hull'
            var activatingElement = $el.data("activate-item");
            // Activate inline progress list item
            $inlineProgressList.find("#" + activatingElement + "-inline").addClass("active disabled-link");
            $progressList.find("#" + activatingElement + "-tab").addClass("active")
                .find(".link-collapse").addClass("disabled-link");
            // Show contents and options!
            $options.find("#" + activatingElement + "-options").fadeIn();
            $contents.find("#" + activatingElement + "-content").fadeIn();

        };

        var all = [$hullTab, $motorTab, $otherFeatures];
        displayTab($hullTab);
        all.forEach(function ($el) {
            $el.click(function (e) {
                e.preventDefault();
                displayTab($el);
            })
        });

    };

    var defaultClose = function ($elements, canvas, callback) {

        // When pressing those "x", remove the color or image!
        $elements.click(function (event) {
            event.preventDefault();
            var imageKey = $(this).data("boatKey");
            canvas.boatCanvas("clear", imageKey);
            $( '.sample#' + imageKey + 'Sample' ).css("visibility", "hidden");
            if (callback !== undefined) {
                callback($(this));
            }
        });
    };

    var enableHull = function (canvas, $buildABoatTab) {
        var $options = $buildABoatTab.find('#hull-options');
        $options.find(".color-select").click(function (event) {
            event.preventDefault();
            var $colorContainer = $options.find(".color-container");
            $colorContainer.hide();
            $('.dropup#hull-options').addClass('open');
            drawColorPicker($(this), event, canvas, $options.find(".color-container"));
            $colorContainer.slideDown(200);
            $colorContainer[0].style.display = "block";
            var $matchColorButtons = $('#match-color-to');
            toggleHiddenRadioButtons($(this)[0].id);
            uncheckAllRadioButtons();
            $matchColorButtons.hide();
            $matchColorButtons.fadeIn();
        });

        $('#match-color-to').find('div').on('click', function () {
            // color: color of associated boat part: boatBootStripeRadioButton -> boatBootStripeSample
            var color = $('#' + $(this)[0].id.replace('RadioButton', '') + 'Sample').data('color');
            var colorPickerSliders = $('#color-container');
            colorPickerSliders.trigger("colorpickersliders.updateColor", color);
            colorPickerSliders.trigger('mousedown');
            colorPickerSliders.trigger('mouseup');
            // clicking a slider unchecks all radio buttons, this re-selects the clicked one
            $(this).find('input').addClass('active').end().find('[type="radio"]').prop('checked', true);
        });
    };

    var enableMotor = function (canvas, $buildABoatTab) {
        var $progressList = $buildABoatTab.find(".left-progress-list");

        var $options = $buildABoatTab.find('#motor-options');
        var $content = $buildABoatTab.find('#motor-content');
        var $imageOptions = $options.find(".sub-options");
        var $clickableItems = $imageOptions.find('.clickable-item');

        $options.find("a.tab-option").click(function (e) {
            $(this).addClass("active").siblings().removeClass('active');
            e.preventDefault();
            var model = $(this).data("model-id");
            $content.find(".content-item").hide();
            var key = ".content-item-" + model;
            $content.find(key).removeClass("hidden").show();
            $imageOptions.removeClass("hidden");
            $imageOptions.find(".sub-option-item").hide();
            $imageOptions.find(".sub-option-item-" + model).slideDown(200).css("display", "block");
            $('.dropup#motor-options').addClass('open');
        });

        $imageOptions.find(".clickable-item").click(function (e) {
            e.preventDefault();
            var imagePath = $(this).data("motor-image");
            var motorTitle = $(this).data("motor-title");
            var motorOptionTitle = $(this).data("motor-option-title");
            canvas.boatCanvas("drawMotor", imagePath);
            $progressList.find(".motor-row .title").text(motorTitle);
            $progressList.find(".motor-row .chosen-option").text(motorOptionTitle);
            $clickableItems.find('.motor-rectangle').removeClass('selected');
            $(this).find('.motor-rectangle').addClass('selected');
        });

        var onResetMotor = function ($anchor) {
            var chosenOption = $anchor.parents(".motor-row").find(".chosen-option");
            chosenOption.text(chosenOption.data("default-text"));
            $anchor.parents(".motor-row").find(".title").text("");
            $('.motor-rectangle').removeClass('selected');
        };

        defaultClose($progressList.find("a.motor-close"), canvas, onResetMotor);
    };

    var enableFeatures = function (canvas, $buildABoatTab) {
        var $progressList = $buildABoatTab.find(".left-progress-list");

        var $options = $buildABoatTab.find('#features-options');
        var $subOptions = $options.find(".sub-options");

        $options.find("a.tab-option").click(function (e) {
            $(this).addClass("active").siblings().removeClass('active');
            e.preventDefault();
            var featureId = $(this).data("featureId");
            $subOptions.removeClass("hidden");
            $subOptions.find(".sub-option-item").hide();
            $subOptions.find(".sub-option-item-" + featureId).slideDown(200);
            $subOptions.find(".sub-option-item-" + featureId)[0].style.display = "block";
            $('.dropup#features-options').addClass('open');
        });

        $subOptions.find(".sub-option-item input").change(function (e) {
            canvas.boatCanvas("setLayer", e.target.name, e.target.value);
            var $input = $(this);
            var featurePk = $input.data("feature-pk"),
                displayValue = $input.data("feature-display");

            $progressList.find(".feature-row.feature-" + featurePk + " .chosen-option").text(displayValue);
        });
        $options.find(".color-select").click(function (event) {
            event.preventDefault();
            $subOptions.removeClass("hidden");
            $subOptions.find(".sub-option-item").hide();
            $('.dropup#features-options').addClass('open');
            drawColorPicker($(this), event, canvas, $subOptions.find(".color-container"));
            $subOptions.find(".sub-option-item-logo").slideDown(200);
            $subOptions.find(".sub-option-item-logo")[0].style.display = "block"
        });
        var onResetFeature = function ($anchor) {
            var name = $anchor.data("boatKey");
            $subOptions.find('.sub-option-item input[name="' + name + '"][data-default="default"]').click()
        };
        var defaults =  $subOptions.find('.sub-option-item input[data-default="default"]');
        defaults.trigger("click"); // Select default! Trigger images download and rendering!

        defaultClose($progressList.find("a.feature-close"), canvas, onResetFeature);
    };

    function successSharingBuiltBoat() {
        $('#shareModal').modal('toggle'); // Close modal
        $('#share-success-message').show();
        var shareButton = $('#build-a-boat-share-button');
        shareButton.prop('disabled', true);
        shareButton.css('background','grey');

    }

    var enableShareModal = function ($buildABoatTab, canvas) {

        $buildABoatTab.find(".share-panel form.sendEmailForm").submit(function (e) {
            e.preventDefault();
            var $form = $(this);
            $form.find("button:submit").attr("disabled", "disabled");
            var url = canvas.boatCanvas("getLink");
            var data = $form.serializeArray();
            data.push({name: 'image_url', value: url});
            $.post($form.attr("action"), data).done(function () {
                successSharingBuiltBoat();
            });
        });
        $buildABoatTab.find(".share-panel form#shareOnFacebook").submit(function (e) {
            e.preventDefault();
            var $form = $(this);
            $form.find("button:submit").attr("disabled", "disabled");
            var url = canvas.boatCanvas("getLink");
            var data = $form.serializeArray();
            data.push({name: 'image_url', value: url});
            $.post($form.attr("action"), data).done(function (responseData) {

                FB.ui({
                    name: 'Facebook Dialogs',
                    link: 'https://developers.facebook.com/docs/dialogs/',
                    picture: responseData.url,
                    caption: responseData.current_site,
                    quote: responseData.text_post,
                    description: responseData.text_post,
                    method: 'share',
                    version: 'v2.8',
                    xfbml: true,
                    href: responseData.url
                }, function () {
                    successSharingBuiltBoat();
                });
            })
        });

        var inputs = $buildABoatTab.find("form#select-share input");
        // TODO: We could do this async!
        inputs.change(function () {
            var $input = $(this);
            var value = $input.val();
            var $panels = $buildABoatTab.find(".share-panel");
            $panels.addClass("hidden");
            $panels.filter("#" + value).removeClass("hidden");
        });
        $(inputs.get(0)).click();
    };

    var eneableClickableSteps = function () {
        var steps = ['hull', 'motor', 'features'];
        for (var i = 0; i < steps.length; i++) {
            var step = steps[i];
            $('#' + step + '-inline').click({step: step}, function (event) {
                event.preventDefault();
                $('#' + event.data.step + '-tab').click();
            });
        }
    };

    var init = function () {
        var $buildABoatTab = $("#build-a-boat");
        var canvas = drawBoat($buildABoatTab, $buildABoatTab.find(".progress-list a#share-button"));
        enableHull(canvas, $buildABoatTab);
        enableProgressList(canvas, $buildABoatTab);
        enableMotor(canvas, $buildABoatTab);
        enableFeatures(canvas, $buildABoatTab);

        var $progressList = $buildABoatTab.find(".left-progress-list");
        defaultClose($progressList.find("a.color-close"), canvas);// TODO: clear rectangle color!

        enableShareModal($buildABoatTab, canvas);

        eneableClickableSteps();
    };

    $(window).on("load", init);

});
