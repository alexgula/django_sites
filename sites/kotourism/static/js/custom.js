/**
 * Created by .
 * User: Tayg
 * Date: 14.03.11
 * Time: 14:10
 * To change this template use File | Settings | File Templates.
 */

String.prototype.format = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

var setup_visicom_map = function(media_url, data) {
    var map = new VMap(document.getElementById('visicom-viewport'));

    for(var place_type_slug in data)
    {
        var places = data[place_type_slug].places;
        var icon = new VMarkerIcon(32, 37, media_url + data[place_type_slug].icon);
        if(places.length > 0)
        {
            var layer = new VLayer();
            layer.visible(true);
            for(var i=0; i < places.length; i++)
            {
                var place = places[i];
                var marker = new VMarker({lng: place.lon, lat: place.lat});
                marker.hint(place.name);
                marker.icon(icon);
                if(place.url)
                    marker.info('<a href="' + place.url + '" target="_blank">' + place.name + '</a>');
                else
                    marker.info(place.name);
                layer.add(marker);
            }
            map.add(layer);
        }
    }

    var point = {lng: 30.2280, lat: 50.3754};

    map.center(point, 8);
    map.repaint();
};

(function($) {
    $.fn.event_calendar = function(language_code, service_link_generator, day_link_generator, month_link_generator, month_link_title, month_link_selector) {
        var calendar = this; // Capture this for refreshing
        var events = {};
        function clear(year, month) {
            set_days(year, month, {});
        }
        function set_days(year, month, days) {
            var cal_year = events[year];
            if(!(cal_year instanceof Object))
                events[year] = {};
            events[year][month] = days;
        }
        function get_days(year, month) {
            if(events[year] && events[year][month])
                var e = events[year][month];
                if(e && e.calendar && e.events)
                    return e;
            return {calendar: {}, events: {}};
        }
        function load(year, month, on_success, on_error) {
            year = year + Math.floor(month / 12);
            month = month % 12;
            if(month == 0)
            {
                year = year - 1;
                month = 12;
            }
            if(events[year] != undefined && events[year][month] != undefined)
                return;
            clear(year, month);
            $.ajax({
                // Have to use suffix to disable browser chaching, otherwise browser is confused with JSON/HTML outputs
                url: service_link_generator(year, month) + '?format=json',
                dataType: 'json',
                success: function(data) {
                    set_days(year, month, {calendar: data.calendar, events: data.events});
                    if(on_success instanceof Function)
                        on_success(data);
                },
                error: function(data) {
                    if(on_error instanceof Function)
                        on_error(data);
                }
            });
        }
        function show_date(date) {
            var days = get_days(date.getFullYear(), date.getMonth()+1);
            var events = days.calendar[date.getDate()];
            var has_events = events instanceof Array;
            if(has_events) {
                var tooltip = "";
                for(var i = 0; i < events.length; i++) {
                    if(i>0)
                        tooltip += ", ";
                    tooltip += days.events[events[i]].name;
                }
            }
            return [has_events, '', tooltip];
        }
        function select_date(date_text, inst) {
            var link = day_link_generator(inst.selectedYear, inst.selectedMonth, inst.selectedDay);
            window.location = link;
        }
        function refresh(data) {
            calendar.datepicker('refresh');
        }
        function load_month(year, month, inst) {
            load(year, month-1);
            load(year, month+1);
            load(year, month, refresh);
            if(month_link_selector) {
                $(month_link_selector).html(
                    "<a href='" + month_link_generator(year, month-1) + "' title='" + month_link_title + "'>" +
                        month_link_title +
                    "</a>");
            }
        }

        var locale_settings = $.datepicker.regional[language_code];
        var dp_settings = $.extend(locale_settings, {
            showOtherMonths: true,
            selectOtherMonths: true,
            showButtonPanel: true,
            onChangeMonthYear: load_month,
            beforeShowDay: show_date,
            onSelect: select_date
        });
        var dp = $(this).datepicker(dp_settings);
        dp = $(this).datepicker('getDate');
        load_month(dp.getFullYear(), dp.getMonth()+1, dp);

        return this;
    };

    $('#currency').hover(function() {
        $('#currency').find('.currencies').stop(true, true).slideDown('fast');
    }, function() {
        $('#currency').find('.currencies').slideUp('slow');
    });

    $('#menu-main').find('.menu-item.active:not(:has(.menu-item.active))').addClass('active-selected');

    // Add target for all external RestructuredText links
    $("a.external").attr('target', '_blank');
    // Add target for all external content links
    //$("#content .event a[href^='http:']:not([href*='" + window.location.host + "'])").attr('target', '_blank');
})(jQuery);


/* DJANGO CSRF
----------------------------------------------------------*/

$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


/* COLORBOX
----------------------------------------------------------*/
(function($){
    $("a.colorbox").colorbox();
})(jQuery);


/* OPACITY
----------------------------------------------------------*/
/**
 * jQuery Opacity Rollover plugin
 *
 * Copyright (c) 2009 Trent Foley (http://trentacular.com)
 * Licensed under the MIT License:
 *   http://www.opensource.org/licenses/mit-license.php
 */
(function($) {
    var defaults = {
        mouseOutOpacity:   0.67,
        mouseOverOpacity:  1.0,
        fadeSpeed:         'fast',
        exemptionSelector: '.selected'
    };

    $.fn.opacityrollover = function(settings) {
        // Initialize the effect
        $.extend(this, defaults, settings);

        var config = this;

        function fadeTo(element, opacity) {
            var $target = $(element);

            if (config.exemptionSelector)
                $target = $target.not(config.exemptionSelector);

            $target.fadeTo(config.fadeSpeed, opacity);
        }

        this.css('opacity', this.mouseOutOpacity)
            .hover(
                function () {
                    fadeTo(this, config.mouseOverOpacity);
                },
                function () {
                    fadeTo(this, config.mouseOutOpacity);
                });

        return this;
    };
})(jQuery);
