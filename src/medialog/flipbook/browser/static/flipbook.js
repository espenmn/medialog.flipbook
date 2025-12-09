function addPage(page, book) {
    var element = $('<div />', {});
    book.turn('addPage', element, page);
    loadSmallPage(page, element);
}

function loadSmallPage(page, pageElement) {
    var url = FLIPBOOK_IMAGES[page - 1]; // pages start at 1
    $('<img />', { src: url }).appendTo(pageElement);
}

function loadLargePage(page, pageElement) {
    var url = FLIPBOOK_IMAGES[page - 1];
    $('<img />', {
        src: url,
        style: "width:100%; height:100%;"
    }).appendTo(pageElement);
}

function loadApp() {

    $('#canvas').fadeIn(500);

    var flipbook = $('.magazine');

    flipbook.turn({
        width: 922,
        height: 600,
        duration: 1000,
        acceleration: true,
        gradients: true,
        autoCenter: true,
        elevation: 50,
        pages: FLIPBOOK_IMAGES.length,

        when: {
            missing: function (event, pages) {
                for (var i = 0; i < pages.length; i++) {
                    addPage(pages[i], $(this));
                }
            }
        }
    });

    // Zoom
    $('.magazine-viewport').zoom({
        flipbook: flipbook,
        max: function() {
            return 922 / flipbook.width();
        },
        when: {
            resize: function(e, scale, page, pageElement) {
                if (scale == 1) {
                    loadSmallPage(page, pageElement);
                } else {
                    loadLargePage(page, pageElement);
                }
            }
        }
    });

    // Thumbnails click
    $('.thumbnails').on('click', function(event) {
        var cls = $(event.target).attr('class');
        var match = /page-([0-9]+)/.exec(cls);
        if (match) {
            flipbook.turn('page', parseInt(match[1], 10));
        }
    });
}

$(document).ready(function() {
    $('#canvas').hide();
    loadApp();
});
