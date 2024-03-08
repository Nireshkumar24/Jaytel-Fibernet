/*! https://github.com/norin89/jquery-spaNav v1.4.0 Marcin Gościcki <http://goscicki.eu/> */
(function($) {
    $.fn.spaNav = function(options) {

        var $nav = $(this),
            $sections = getSections(),
            baseUrl = window.location.href.split('#')[0];

        /* default settings */
        var defaults = {
            navOffset : $nav.css('position') == 'fixed' ? $nav.position().top : $nav.offset().top, // breakpoint for adding/removing 'sticky' class
            sectionOffset : 0, // offset (in px) added to sections - can be negative
            changeHash : true, // affect page address bar or not
            centerOffset : true, // if true we activate/navigate to section in middle of the page in case it's lower than viewport
            stickyClass : 'sticky', // class added to navigation when body offset is bigger than nav height
            navActivityClass : 'active', // navigation activity class
            sectionActivityClass : 'active', // sections activity class
            clearSectionActivity : false, // whether to clear section activity class on section leave or not
            scrollTime : 1000 // scroll time to element [ms]
        };
        var settings = $.extend( {}, defaults, options );

        function scrollTo(hash) {
            var top = $(hash).length > 0 ? getOffset($(hash)) : 0;
            $('html, body').animate({
                scrollTop: top
            }, settings.scrollTime);
        }

        function setHash(hash, force) {
            // setting activity classes when on hash change or when forced
            if ((!settings.changeHash) || (hash != window.location.hash || force)) {
                $nav.find('a').removeClass(settings.navActivityClass).filter('[href="'+hash+'"]').addClass(settings.navActivityClass);
                if (settings.clearSectionActivity) {
                    $.each($sections, function(){
                        $(this).removeClass(settings.sectionActivityClass);
                    });
                }
                $(hash).addClass(settings.sectionActivityClass);
            }

            if (hash != window.location.hash && settings.changeHash) {
                // Temp suffix in id removes page jump effect
                $(hash).attr('id',$(hash).attr('id')+'Temp');
                window.location.replace(baseUrl + hash); // unlike the above this one doesn't affect browser back/forward history
                $(hash+'Temp').attr('id', hash.substring(1));
            }
        }

        function getSections() {
            var secions = [];
            $nav.find('a').each(function(){
                var $link = $(this), href = $link.attr('href');
                if ((href.charAt(0) === '#') && ($(href).length > 0)) secions.push($(href));
            });

            // sorting sections by offset (reversed) so order of links in $nav doesn't matter
            secions.sort(function($a, $b) {
                if ($a.offset().top < $b.offset().top) return 1; else return -1;
                return $a - $b;
            });

            return secions;
        }

        function getOffset($el){
            var offset = $el.offset().top;
            if (settings.centerOffset) {
                // used to change hash when container's in the middle of the page
                offset = $el.outerHeight() < $(window).height() ? offset - ($(window).height() - $el.outerHeight()) / 2 : offset;
                offset = offset > 0 ? offset : 0;
            }
            return parseInt(offset + settings.sectionOffset);
        }

        function onScroll() {
            // add "sticky" class when srollTop is bigger that nav height
            if ($(window).scrollTop() > settings.navOffset) $nav.addClass(settings.stickyClass);
            else $nav.removeClass(settings.stickyClass);

            // setting hash of first array element when bottom of page reached
            if ($(window).scrollTop() + $(window).height() >= $(document).height()) {
                if ($sections.length > 0) setHash('#'+$sections[0].attr('id'));
            } else {
                $.each($sections, function(){
                    var $section = $(this);
                    if (getOffset($section) <= $(window).scrollTop()) {
                        setHash('#'+$section.attr('id'));
                        return false; // break each
                    }
                });
            }
        }

        /* hash change on page scroll */
        $(window).on('scroll', function(){ onScroll(); });
        $(window).on('touchmove', function(){ onScroll(); });

        /* triggering actions on page entry */
        $(document).ready(function(e){
            onScroll();
            if (settings.changeHash) {
                setHash(window.location.hash, true);
                scrollTo(window.location.hash);
            }
        });

        /* body of the plugin */
        return this.each(function() {

            // nav element click
            $nav.find('a').on('click', function(e){
                var href = $(this).attr('href');
                if (href.charAt(0) === '#') {
                    e.preventDefault();
                    scrollTo(href);
                }
            });

        });

    }
})(jQuery, window, document);