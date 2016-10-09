function make_auto_complete() {
    // Setup search auto complete functionality
    $("#trainer-search").autocomplete({
        source: "/search/trainer/",
        minLength: 0,
        delay: 250,
        focus: function(event, ui) {
            return false;
        },
        select: function(event, ui) {
            // $("#trainer-search").val(ui.item.label);
            $("#trainer-search").val("");
            url = "/trainer/profile/" + ui.item.id;
            $(location).attr('href', url);
            return false;
        },
        response: function(event, ui) {}
    }).bind('focus', function(){$(this).autocomplete("search");});

    $("#student-search").autocomplete({
        source: "/search/student/",
        minLength: 0,
        delay: 250,
        focus: function(event, ui) {
            return false;
        },
        select: function(event, ui) {
            // $("#student-search").val(ui.item.label);
            $("#student-search").val("");
            url = "/student/profile/" + ui.item.id;
            $(location).attr('href', url);
            return false;
        },
        response: function(event, ui) {}
    }).bind('focus', function(){$(this).autocomplete("search");});

    $("#location-search").autocomplete({
        source: "/search/location/",
        minLength: 0,
        delay: 250,
        focus: function(event, ui) {
            return false;
        },
        select: function(event, ui) {
            // $("#trainer-search").val(ui.item.label);
            $("#location-search").val("");
            url = "/booking/show_booking/" + ui.item.id;
            $(location).attr('href', url);
            return false;
        },
        response: function(event, ui) {}
    }).bind('focus', function(){$(this).autocomplete("search");});
}

// When all the DOM-objects is done loading
$(document).ready(function() {
    make_auto_complete()
});
