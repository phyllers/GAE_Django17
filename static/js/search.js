$(document).ready(function() {
    var elements_selected = {};
    var platforms_selected = {};
    var tumors_selected = {};

    var update_search = function(section, items) {
        $('#'+ section +'-search-criteria').empty();
        if (!$.isEmptyObject(items)) {
            $('#'+ section +'-search-criteria').append('<h5>'+section+' selected:</h5');
            $('#'+ section +'-search-criteria').append('<ul></ul>');
            for (var e in items) {
                var item = $('<li class="' + e + '">'+items[e]+'</li>');
                $('#'+ section +'-search-criteria ul').append(item);
            }
        }
    };

    $('[name="elements-selected"]').on('change', function(){
        if (this.checked) {
            elements_selected[this.id] = this.labels[0].innerText.replace(/^\s+|\s+$/g, '');
        } else {
            delete elements_selected[this.id];
        }
        update_search('elements', elements_selected);
    });

    $('[name="platforms-selected"]').on('change', function(){
        if (this.checked) {
            platforms_selected[this.id] = this.labels[0].innerText.replace(/^\s+|\s+$/g, '');
        } else {
            delete platforms_selected[this.id];
        }
        update_search('platforms', platforms_selected);
    });

    $('[name="tumors-selected"]').on('change', function(){
        if (this.checked) {
            tumors_selected[this.id] = this.labels[0].innerText.replace(/^\s+|\s+$/g, '');
        } else {
            delete tumors_selected[this.id];
        }
        update_search('tumors', tumors_selected);
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
});