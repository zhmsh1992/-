jQuery(function ($) {
    $.supersized({
        slide_interval: 6000,
        transition: 1,
        transition_speed: 3000,
        performance: 1,
        min_width: 0,
        min_height: 0,
        vertical_center: 1,
        horizontal_center: 1,
        fit_always: 0,
        fit_portrait: 1,
        fit_landscape: 0,
        slide_links: 'blank',
        slides: [{image: '/static/img/1.jpg'}, {image: '/static/img/2.jpg'}, {image: '/static/img/3.jpg'}]
    });
});