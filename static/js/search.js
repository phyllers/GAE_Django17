$(document).ready(function() {

    var search_criteria = {};


    var update_search = function() {
        $('#search-criteria').empty();
        if (!$.isEmptyObject(search_criteria)) {
            $('#search-criteria').append('<ul></ul>');
            for (var e in search_criteria) {
                var cat = e.split('-')[0];
                var item = $('<li class=' + e + '">' + cat + ': ' + search_criteria[e].split(' - ')[1] + '</li>');
                $('#search-criteria').append(item);
            }
        }
    }

    $('.panel-body input[type=checkbox]').on('change', function() {
        if (this.checked) {
            search_criteria[this.id] = this.labels[0].innerText.replace(/^\s+|\s+$/g, '');
        } else {
            delete search_criteria[this.id];
        }
        update_search();
    });

    $('#select-all').on('click', function() {
        if (this.checked) {
            $('table input[type="checkbox"]').each(function() {
                this.checked="checked";
            })
        } else {
            $('table input[type="checkbox"]').each(function() {
                this.checked="";
            })
        }
    });

    $('table input[type="checkbox"]').on('click', function() {
        if (!this.checked) {
            $('#select-all')[0].checked="";
        }
    })

    $('#search-filters').submit(function(e) {
        $('<input />').attr('type', 'hidden')
            .attr('name', 'search_filter')
            .attr('value', JSON.stringify(search_criteria))
            .appendTo('#search-filters');
        return true;
    })
});